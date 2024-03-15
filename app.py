import argparse
import os
import sys
from urllib.parse import urlparse

import html2text
import requests
from dotenv import load_dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader, YoutubeLoader
from langchain_openai import ChatOpenAI

load_dotenv()

MODEL_NAME = "gpt-4-turbo-preview"
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

h = html2text.HTML2Text()
h.ignore_links = True

YOUTUBE_URLS = ["www.youtube.com", "youtube.com", "youtu.be"]


def extract_text_from_url(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Content-Type": "text/html; charset=UTF-8",
    }
    response = requests.get(url, headers=headers)
    return h.handle(response.text)


def extract_text_from_pdf(url: str) -> str:
    loader = PyPDFLoader(url)
    return loader.load()


def extract_text_from_youtube(url: str) -> str:
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
    return loader.load()


def extract_text(source: str) -> str:
    try:
        parsed_url = urlparse(source)
        if parsed_url.netloc in YOUTUBE_URLS:
            return extract_text_from_youtube(source)
        elif parsed_url.path.endswith(".pdf"):
            return extract_text_from_pdf(source)
        else:
            return extract_text_from_url(source)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while trying to fetch the text: {e}")
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The URL to create a summary from")
    args = parser.parse_args()

    (
        RunnablePassthrough.assign(text=lambda x: extract_text(x["url"]))
        | SUMMARY_PROMPT
        | ChatOpenAI(
            temperature=1,
            model_name=MODEL_NAME,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
        )
    ).invoke({"url": args.url})


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: The OPENAI_API_KEY environment variable is not set.")
        sys.exit(1)

    main()
