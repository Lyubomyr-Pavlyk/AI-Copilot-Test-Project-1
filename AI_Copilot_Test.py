# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 18:11:08 2026

@author: Lyubomyr
"""

from openai import OpenAI
from utils import *




file_name = "d:/Projects/AI Copilot Test Projects/Data.xlsx"

Numbers = Read_Data_FIle(file_name)

av = calculate_average(Numbers)

print(f"Average value = {av}")


client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)


models = client.models.list()

for model in models.data:
    print(model.id)

question = """
    You have access to the function calculate_average.
    
    Take the kist of numbers: numbers = [10, 20, 30, 40]
    and give me the result returned by this function. Also explain what this functio does.
    
    """

response = client.chat.completions.create(
    model="qwen2.5-7b-instruct-1m",
    messages=[
        {
            "role": "user",
            "content": question
        }
    ]
)

print(response.choices[0].message.content)