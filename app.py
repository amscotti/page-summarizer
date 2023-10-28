import argparse
import requests
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from bs4 import BeautifulSoup
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

load_dotenv()

MODEL_NAME = "gpt-4-1106-preview"
SUMMARY_TEMPLATE = """
You are tasked with writing a comprehensive summary the following text so that readers will have a full understanding of the text, without need of referencing the source material.
Your summary should reflect the length of the source material, and provide enough details, that the reader can fully understand the subject and speak of it at a high-level.
You will also providing list of 3 or more brief key points from the article that may not be covered by the initial report, additional key points can be keep together under 'KEY POINTS'.

{text}

Use the format,

SUMMARY:
<Summary>

KEY POINTS:
- <Key Point>
- <Key Point>
- <Key Point>
- ...
"""

SUMMARY_PROMPT = ChatPromptTemplate.from_template(SUMMARY_TEMPLATE)


def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The URL to create a summary from")
    args = parser.parse_args()

    summary = (
        RunnablePassthrough.assign(text=lambda x: extract_text_from_url(x["url"]))
        | SUMMARY_PROMPT
        | ChatOpenAI(temperature=1, model_name=MODEL_NAME, streaming=True)
        | StrOutputParser()
    ).invoke({"url": args.url})

    print(summary)


if __name__ == "__main__":
    main()
