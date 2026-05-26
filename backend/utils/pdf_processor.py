import PyPDF2
from pathlib import Path

def extract_text_from_pdf(pdf_path: str) -> str:
    """从PDF文件中提取文本内容"""
    text = ""
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"无法提取PDF文本: {str(e)}")
    
    return text.strip()

def save_summary_to_file(summary: str, filename: str, output_dir: Path) -> str:
    """将摘要保存到文件"""
    safe_filename = filename.replace(' ', '_').replace('/', '_').replace('\\', '_')
    if not safe_filename.endswith('.txt'):
        safe_filename += '.txt'
    
    output_path = output_dir / safe_filename
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    return str(output_path)
