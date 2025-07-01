import pytest
from pathlib import Path
from ml.utils.WDMParser import WDMPDFParser  
from langchain_core.documents import Document

TEST_PDF_PATH = "C:/Users/Admin/Data/MultimodalRag_Web_app/src/ml/tests/sample/2c98e99a08ec5392d50e60370d871319.pdf"  

def test_extract_text_basic():
    parser = WDMPDFParser(
        file_path=TEST_PDF_PATH,
        debug=True,
    )
    documents = parser.extract_text(pages=[1])
    assert isinstance(documents, list)
    assert all(isinstance(doc, Document) for doc in documents)
    assert all("text" in doc.metadata["type"] for doc in documents)
    assert len(documents) > 0


def test_extract_tables_without_credentials():
    parser = WDMPDFParser(
        file_path=TEST_PDF_PATH,
        debug=True,
    )
    with pytest.raises(ValueError) as e:
        parser.extract_tables(merge_span_tables=True)
    assert "Credentials required" in str(e.value)





def test_text_extraction_empty_page(monkeypatch):
    """Giả lập page không có text"""
    parser = WDMPDFParser(
        file_path=TEST_PDF_PATH,
        debug=True,
    )

    # Mock internal method để trả về trang rỗng
    def mock_extract(*args, **kwargs):
        return []
    
    monkeypatch.setattr(parser, "_extract_text_internal", mock_extract)
    docs = parser.extract_text(pages=[99])
    assert docs == []
