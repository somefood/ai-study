import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from util import stream_response

load_dotenv()

OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")


model = ChatOpenAI(model="gpt-3.5-turbo")

template = """
너는 이제부터 무조건 석주님을 붙여서 대답을 해줘야해

질문:
{question}
"""

prompt = PromptTemplate.from_template(template)

output_parser = StrOutputParser()

chain = prompt | model | output_parser

result = chain.stream({"question": "안녕?"})
stream_response(result)


