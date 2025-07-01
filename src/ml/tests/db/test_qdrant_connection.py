import pytest
from qdrant_client import QdrantClient
from ml.configs.ml_project_configs import settings
from qdrant_client.http.models import Distance, VectorParams

collection_name = "unit_test_sdk"

@pytest.fixture(scope="module")
def client():
    return QdrantClient(url=settings.QDRANT_HOST)

def test_qdrant_connect_success(client):
    """Kết nối Qdrant thành công"""
    collections = client.get_collections()
    assert collections is not None

def test_qdrant_create_collection(client):
    """Tạo collection thành công"""
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=4, distance=Distance.COSINE)
    )
    assert client.collection_exists(collection_name)

def test_qdrant_get_collection_info(client):
    """Đọc thông tin collection thành công"""
    info = client.get_collection(collection_name)
    assert info.status == "green"

def test_qdrant_list_collections(client):
    """Lấy danh sách collection thành công"""
    collections = client.get_collections().collections
    names = [c.name for c in collections]
    assert collection_name in names

def test_qdrant_delete_collection(client):
    """Xóa collection thành công"""
    client.delete_collection(collection_name)
    assert not client.collection_exists(collection_name)