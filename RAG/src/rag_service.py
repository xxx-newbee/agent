import os

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
import embedding
import vectorstore
from openai import OpenAI

llm_client = OpenAI(api_key="who care", base_url="http://localhost:11434/v1")

def retrieve_context(question: str, top_k: int = 3):
    query_embedding = embedding.get_embedding(question)

    search_res = vectorstore.milvus_client.search(
        collection_name=vectorstore.collention_name,
        data=[query_embedding],
        limit=top_k,
        search_params={"metric_type": "IP"},
        output_fields=["text"]
    )

    context = ""
    for hit in search_res[0]:
        context += hit.get("text") + "\n\n"
    return context.strip()


if __name__ == "__main__":
    question = "什么是RAG？"
    context = retrieve_context(question)

    prompt = f"""
    你是一个智能助手。请根据以下提供的上下文信息来回答用户的问题。如果无法从上下文中找到答案，请直接说明。

    <context>
    {context}
    /context>

    <question>
    {question}
    </question>
    """

    response = llm_client.chat.completions.create(
        model="qwen/qwen3.5-9b",
        messages=[{"role":"user", "content": prompt}],
        stream=True
    )
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
    print()
