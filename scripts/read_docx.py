#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取Word文档内容
"""

from docx import Document
import sys


def read_docx(file_path):
    """读取docx文件的所有段落文本"""
    try:
        doc = Document(file_path)
        paragraphs = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                paragraphs.append(text)
        return '\n'.join(paragraphs)
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python read_docx.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    content = read_docx(file_path)
    print(content)
