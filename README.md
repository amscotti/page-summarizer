# Page Summarizer

<p align="center">
    <img src="images/wizard_in_a_library.jpg" alt="A wizard in a library - Leonardo AI" width="600">
</p>

Page Summarizer is a Python application that extracts text from a given URL and uses OpenAI's GPT-4 model, interfaced through the LangChain library, to generate a comprehensive summary and key points of the extracted text. The application leverages the power of GPT-4's natural language understanding to provide concise and relevant summaries, making it easier to digest large amounts of information quickly.

## How to Run the Project

To run this project, you will need Python installed on your machine along with the necessary packages. Follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Set up your environment variables by creating a `.env` file with your OpenAI API key as `OPENAI_API_KEY`.
4. Run the script using the command `python app.py <URL>`, where `<URL>` is the URL of the webpage you want to summarize.

## References
- [Requests](https://docs.python-requests.org/en/latest/index.html)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [LangChain](https://www.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
