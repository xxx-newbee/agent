from sentence_transformers import SentenceTransformer

embeding_model = SentenceTransformer("BAAI/bge-m3")

def get_embedding(text: str):
    return embeding_model.encode(text).tolist()

# if __name__ == "__main__":
#     test_vec = get_embedding("测试 Qwen3 嵌入模型")
#     print(f"向量维度: {len(test_vec)}")
#     print(f"向量前五位：{test_vec[:5]}")