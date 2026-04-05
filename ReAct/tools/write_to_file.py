import io

def write_to_file(filename: str, content: str) -> str:
    """
    讲给定的内容写入指定文件
    """
    try:
        with io.open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
            return f"write to {filename} success"
    except Exception as e:
        return f"write to file error: {e}"