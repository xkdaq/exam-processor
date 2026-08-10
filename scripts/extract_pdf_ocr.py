#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用OCR提取扫描版PDF中的文本内容
支持普通PDF和扫描版PDF（图片型PDF）

依赖安装:
    pip install PyMuPDF Pillow pytesseract
    
注意: 需要安装tesseract-ocr引擎
    macOS: brew install tesseract tesseract-lang
    Ubuntu: apt-get install tesseract-ocr tesseract-ocr-chi-sim
"""

import fitz  # PyMuPDF
from PIL import Image
import os
import sys

try:
    import pytesseract
except ImportError:
    print("错误: 未安装pytesseract，请运行: pip install pytesseract")
    sys.exit(1)


def extract_text_from_pdf(pdf_path, max_pages=None, lang='chi_sim+eng'):
    """
    从PDF中提取文本，使用OCR识别扫描版
    
    Args:
        pdf_path: PDF文件路径
        max_pages: 最大处理页数，None表示处理所有页面
        lang: OCR语言，默认中文+英文
        
    Returns:
        提取的文本内容
    """
    doc = fitz.open(pdf_path)
    all_text = []
    
    pages_to_process = len(doc) if max_pages is None else min(max_pages, len(doc))
    
    for page_num in range(pages_to_process):
        page = doc[page_num]
        
        # 先尝试直接提取文本
        text = page.get_text()
        
        # 如果没有文本或文本很少（可能是扫描版），使用OCR
        if len(text.strip()) < 50:
            # 将页面转换为图片，2x缩放提高清晰度
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # OCR识别
            text = pytesseract.image_to_string(img, lang=lang)
        
        all_text.append(f"=== 第{page_num + 1}页 ===\n{text}\n")
        
        if (page_num + 1) % 5 == 0:
            print(f"已处理 {page_num + 1}/{pages_to_process} 页")
    
    doc.close()
    return "\n".join(all_text)


def extract_to_file(pdf_path, output_path=None, max_pages=None):
    """
    提取PDF内容并保存到文件
    
    Args:
        pdf_path: PDF文件路径
        output_path: 输出文件路径，默认为同名.txt文件
        max_pages: 最大处理页数
        
    Returns:
        输出文件路径
    """
    if output_path is None:
        output_path = os.path.splitext(pdf_path)[0] + '_extracted.txt'
    
    print(f"正在处理: {pdf_path}")
    print(f"总页数: {fitz.open(pdf_path).__len__()}")
    
    text = extract_text_from_pdf(pdf_path, max_pages)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"提取完成，结果保存在: {output_path}")
    return output_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf_ocr.py <pdf_path> [output_path] [max_pages]")
        print("Example: python extract_pdf_ocr.py 真题.pdf 输出.txt 10")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    extract_to_file(pdf_path, output_path, max_pages)
