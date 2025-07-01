from langchain.docstore.document import Document as LangchainDocument
import fitz  # PyMuPDF
from google.cloud import storage
from google.api_core.exceptions import Conflict, NotFound
import base64
import os
from langchain.chat_models import init_chat_model

# Set biến môi trường xác thực GCP
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Admin/Data/MultimodalRag_Web_app/serene-craft-464519-j1-963d43d7e20e.json"

# Khởi tạo client GCS
gcs_client = storage.Client()

def create_bucket_if_not_exists(bucket_name, location="asia-southeast1"):
    try:
        bucket = gcs_client.get_bucket(bucket_name)
        print(f"[+] Bucket '{bucket_name}' đã tồn tại.")
        return bucket
    except NotFound:
        print(f"[-] Bucket '{bucket_name}' chưa tồn tại. Đang tạo mới...")
        try:
            bucket = gcs_client.create_bucket(bucket_name, location=location)
            print(f"[+] Bucket '{bucket_name}' đã được tạo thành công!")
            return bucket
        except Conflict as e:
            print(f"[!] Lỗi: Có thể bucket đã được tạo bởi người khác hoặc tên bị trùng?")
            raise e
        except Exception as e:
            print(f"[!] Lỗi khi kiểm tra bucket: {e}")
            raise e

def upload_to_gcs(bucket_name, source_file_path, destination_blob_name):
    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)
    return blob.public_url

def extract_images_from_pdf(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    image_paths = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"page_{page_num+1}_img_{img_index+1}.{image_ext}"
            image_path = os.path.join(output_folder, image_filename)

            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

            image_paths.append({
                'path': image_path,
                'page_num': page_num + 1,
                'img_index': img_index + 1,
                'bbox': fitz.Rect(img[1]['bbox']) if isinstance(img, dict) and 'bbox' in img[1] else page.rect
            })
    doc.close()
    return image_paths

def get_text_near_image(pdf_path, page_num, image_bbox):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num - 1)
    text_dict = page.get_text("dict")
    blocks = text_dict.get("blocks", [])

    nearby_texts = []
    for block in blocks:
        if "lines" in block and block["type"] == 0:  # Chỉ văn bản thường
            for line in block["lines"]:
                for span in line["spans"]:
                    span_rect = fitz.Rect(span["bbox"])
                    if image_bbox.intersects(span_rect):
                        nearby_texts.append(span["text"])

    doc.close()
    return " ".join(nearby_texts[:5]) or "No description found"

def describe_image_with_gemini(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    llm = init_chat_model("google_genai:gemini-2.0-flash-001")
    message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Describe this image in detail:",
            },
            {
                "type": "image",
                "source_type": "base64",
                "data": image_b64,
                "mime_type": "image/png",
            },
        ],
    }
    response = llm.invoke([message])
    return response.text
