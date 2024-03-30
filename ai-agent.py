from extract_10k import *
from pydantic import BaseModel, Field
from openai import OpenAI 
import json

financials_dict = main()

# define class for items we want
class BalanceSheet(BaseModel):
    cash_and_cash_equivalents: int

class IncomeStatement(BaseModel):
    revenue: int
    gross_profit: int
    Selling_And_Marketing_Expense: int
    General_And_Administrative_Expense: int
    operating_profit: int
    net_income: int
    Share_Based_Compensation: int

# Openai stuff
client = OpenAI(api_key="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")

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
        "role": "system", 
        "content": "You are a financial analyst. You are an expert at analyzing financial statements."
    },
    {
        "role": "user", 
        "content": f"Extract the following fields {IncomeStatement.schema()} for FY2023, FY2022, and FY2021 from this data: {financials_dict}. The output should be 1 number, not code or suggestions"
    }
  ],
  temperature=0
)

# below code just uses OAI's standard API output structure. It returns a dict with a list of nested dicts
output = completion.choices[0].message.content
print(output)
print(type(output))

#print(completion.model_dump_json(indent=2))

