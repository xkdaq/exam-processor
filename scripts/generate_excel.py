#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
考研真题Excel生成脚本
根据题目数据生成标准格式的Excel文件
"""

import pandas as pd
import numpy as np
import sys
import json


def generate_excel(data_list, output_path):
    """
    生成Excel文件
    
    Args:
        data_list: 题目数据列表，每个元素是一个字典
        output_path: 输出文件路径
    """
    # 确保每个题目都有完整的字段
    required_fields = ['ID', '题目', '题型', '分数', '难度', 
                       '选项A', '选项B', '选项C', '选项D', '选项E',
                       '答案', '解析', '一级目录', '二级目录']
    
    for item in data_list:
        for field in required_fields:
            if field not in item:
                item[field] = np.nan
    
    df = pd.DataFrame(data_list)
    
    # 确保列顺序正确
    df = df[required_fields]
    
    # 生成Excel
    df.to_excel(output_path, index=False, engine='openpyxl')
    
    return len(df)


def format_analysis(text):
    """
    格式化解析内容，在合适位置添加换行
    """
    import re
    
    if not text or pd.isna(text):
        return text
    
    # 在【】标记后添加换行
    text = re.sub(r'([^\n]【[^】]+】)', r'\1\n', text)
    
    # 在数字编号前添加换行
    text = re.sub(r'([^\n])(（[一二三四五六七八九十1234567890]+）)', r'\1\n\2', text)
    
    # 在中文编号前添加换行
    text = re.sub(r'([^\n])([一二三四五六七八九十]+、)', r'\1\n\2', text)
    
    # 处理多个连续换行
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 去除开头换行
    text = text.lstrip('\n')
    
    return text


if __name__ == '__main__':
    # 从命令行参数读取数据
    if len(sys.argv) < 3:
        print("Usage: python generate_excel.py '<json_data>' <output_path>")
        sys.exit(1)
    
    data_json = sys.argv[1]
    output_path = sys.argv[2]
    
    data_list = json.loads(data_json)
    count = generate_excel(data_list, output_path)
    
    print(f"Excel generated successfully: {count} questions")
