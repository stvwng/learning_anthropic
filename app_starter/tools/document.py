from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pydantic import Field
import os


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(description="Absolute path to the document file to convert"),
) -> str:
    """Convert a document file to markdown-formatted text.

    Reads a document from the filesystem and converts it to markdown.
    Supports PDF, DOCX, and other formats supported by markitdown.

    When to use:
    - When you have a file path and need its contents as markdown
    - When processing local documents for text extraction

    When NOT to use:
    - When you already have binary data (use binary_document_to_markdown instead)

    Examples:
    >>> document_path_to_markdown("/path/to/document.pdf")
    "# Document Title\\n\\nDocument content..."
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Get extension without the dot
    _, ext = os.path.splitext(file_path)
    file_type = ext.lstrip(".")

    with open(file_path, "rb") as f:
        binary_data = f.read()

    return binary_document_to_markdown(binary_data, file_type)
