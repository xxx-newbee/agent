import os

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from pymilvus import MilvusClient
from loader import UniversalLoader
import embedding

milvus_client = MilvusClient(uri="http://localhost:19530")
collention_name = "local_rag_kb"

def create_collection_and_insert(docs, embedding_func):
    test_embedding = embedding_func("test")
    dim = len(test_embedding)

    if milvus_client.has_collection(collention_name):
        milvus_client.drop_collection(collention_name)

    milvus_client.create_collection(
        collection_name=collention_name,
        dimension=dim,
        metric_type="IP",
    )

    data = []
    for i, doc in enumerate(docs):
        data.append({
            "id": i,
            "vector": embedding_func(doc.page_content),
            "text": doc.page_content,
            "source": doc.metadata.get("source", "")
        })
    insert_result = milvus_client.insert(collection_name=collention_name, data=data)
    print(f"成功插入数据到 Milvus")


if __name__ == "__main__":
    print("读取数据...")
    loader = UniversalLoader("../data")
    print("加载数据...")
    docs = loader.load()
    print("插入向量数据库...")
    create_collection_and_insert(docs, embedding.get_embedding)