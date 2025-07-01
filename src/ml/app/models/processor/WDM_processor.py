from langchain.docstore.document import Document as LangchainDocument
import fitz  # PyMuPDF
from google.cloud import storage
from google.api_core.exceptions import Conflict, NotFound
import base64
import os
from langchain.chat_models import init_chat_model
from .utils import (
    create_bucket_if_not_exists,
    upload_to_gcs,
    extract_images_from_pdf,
    get_text_near_image,
    describe_image_with_gemini
)
# Set biến môi trường xác thực GCP
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Admin/Data/MultimodalRag_Web_app/serene-craft-464519-j1-963d43d7e20e.json"




class WDMProcessor:
    def __init__(self, pdf_path, output_folder, gcs_bucket_name):
        self.pdf_path = pdf_path
        self.output_folder = output_folder
        self.gcs_bucket_name = gcs_bucket_name
        self.documents = []

    def extract_text(self):
        doc = fitz.open(self.pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text().strip()
            if text:
                self.documents.append(
                    LangchainDocument(
                        page_content=text,
                        metadata={
                            "source": self.pdf_path,
                            "page_numbers": [page_num + 1],
                            "is_table": False,
                            "is_image": False,
                            "type": "text"
                        }
                    )
                )
        doc.close()

    def extract_tables(self):
        doc = fitz.open(self.pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            for tab in page.find_tables(strategy="text"):
                table_bbox = tab.bbox
                table_text = "\n".join([row.strip() for row in tab.text.splitlines() if row.strip()])
                if table_text:
                    self.documents.append(
                        LangchainDocument(
                            page_content=table_text,
                            metadata={
                                "source": self.pdf_path,
                                "page_numbers": [page_num + 1],
                                "is_table": True,
                                "is_image": False,
                                "type": "table",
                                "bbox": list(table_bbox)
                            }
                        )
                    )
        doc.close()

    def extract_images(self):
        image_info_list = extract_images_from_pdf(self.pdf_path, self.output_folder)
        for info in image_info_list:
            image_path = info['path']
            page_num = info['page_num']
            image_bbox = info['bbox']

            try:
                caption = get_text_near_image(self.pdf_path, page_num, image_bbox)
                gemini_description = describe_image_with_gemini(image_path)
                image_url = upload_to_gcs(self.gcs_bucket_name, image_path, f"images/{os.path.basename(image_path)}")

                full_description = f"{caption}\n\n{gemini_description}"

                self.documents.append(
                    LangchainDocument(
                        page_content=full_description,
                        metadata={
                            "source": self.pdf_path,
                            "page_numbers": [page_num],
                            "is_table": False,
                            "is_image": True,
                            "type": "image",
                            "image_url": image_url,
                            "caption": caption,
                            "gemini_description": gemini_description
                        }
                    )
                )
            except Exception as e:
                print(f"[!] Lỗi xử lý ảnh: {e}")

    def process_pdf(self):
        create_bucket_if_not_exists(self.gcs_bucket_name)

        self.extract_text()
        self.extract_tables()
        self.extract_images()

        return self.documents
    
if __name__ == "__main__":
    PDF_PATH = "C:/Users/Admin/Data/MultimodalRag_Web_app/src/ml/tests/sample/2c98e99a08ec5392d50e60370d871319.pdf"
    OUTPUT_FOLDER = "./extracted_images"
    GCS_BUCKET_NAME = "my-multimodalrag-images"

    processor = WDMProcessor(PDF_PATH, OUTPUT_FOLDER, GCS_BUCKET_NAME)
    documents = processor.process_pdf()

    print("Hoàn tất xử lý. Kết quả:")
    for i, doc in enumerate(documents):
        print(f"\n--- Document {i+1} ---")
        print(f"Type: {doc.metadata['type']}")
        print(f"Metadata: {doc.metadata}")
        print(f"Content:\n{doc.page_content[:200]}...")  # Hiển thị 200 ký tự đầu tiên