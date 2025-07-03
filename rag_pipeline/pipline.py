from dotenv import load_dotenv
load_dotenv()

"""
Docling은 convert() 메서드를 통해 문서 변환 기능을 제공함
"""
from docling.document_converter import DocumentConverter

source = "data/transformer.pdf"
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown()) # 마크다운으로 출력
