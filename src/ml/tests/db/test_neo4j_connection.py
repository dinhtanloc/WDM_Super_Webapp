import pytest
from neo4j import GraphDatabase
from ml.configs.ml_project_configs import settings

test_node_label = "TestNode"

@pytest.fixture(scope="module")
def driver():
    uri = settings.NEO4J_URI
    auth = (settings.NEO4J_USER, settings.NEO4J_PASSWORD)
    driver = GraphDatabase.driver(uri, auth=auth)
    yield driver
    driver.close()

def test_neo4j_authentication(driver):
    """Xác thực với Neo4j thành công"""
    with driver.session() as session:
        result = session.run("RETURN 1 AS number")
        assert result.single()["number"] == 1

def test_neo4j_connection(driver):
    """Kết nối tới Neo4j thành công"""
    with driver.session() as session:
        result = session.run("CALL db.info() YIELD name RETURN name")
        name = result.single()["name"]
        assert isinstance(name, str)

def test_neo4j_create_node(driver):
    """Tạo một node demo"""
    with driver.session() as session:
        result = session.run(f"CREATE (n:{test_node_label} {{name: 'Test'}}) RETURN n")
        record = result.single()
        assert record is not None

def test_neo4j_query_node(driver):
    """Truy vấn và hiển thị node"""
    with driver.session() as session:
        result = session.run(f"MATCH (n:{test_node_label}) RETURN n.name AS name")
        names = [r["name"] for r in result]
        assert "Test" in names

def test_neo4j_delete_node(driver):
    """Xóa node"""
    with driver.session() as session:
        session.run(f"MATCH (n:{test_node_label}) DELETE n")
        result = session.run(f"MATCH (n:{test_node_label}) RETURN COUNT(n) AS count")
        count = result.single()["count"]
        assert count == 0
