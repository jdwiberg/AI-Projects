# PDF Summarizer

A Python tool that summarizes PDF documents using an LLM (Large Language Model). The program extracts text from a PDF, cleans and chunks it, sends each chunk to an LLM for summarization, and then synthesizes a final summary.

## Features

- Extracts and cleans text from PDF files
- Splits text into overlapping chunks for LLM processing
- Summarizes each chunk using OpenAI's GPT models
- Synthesizes a cohesive summary from chunk summaries
- Outputs the final summary in Markdown format

## Requirements

- Python 3.8+
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [tiktoken](https://pypi.org/project/tiktoken/)
- [openai](https://pypi.org/project/openai/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

Install dependencies with:

```sh
pip install -r requirements.txt
```

## Setup

1. Obtain an OpenAI API key and add it to a `.env` file in the `summarizer/` directory:

    ```
    OPEN_AI_KEY=your_openai_api_key_here
    ```

2. Place the PDF you want to summarize in the `summarizer/` directory.

## Usage

Run the summarizer script:

```sh
python summarizer.py
```

You will be prompted to enter the name of the PDF file (including `.pdf`). The script will process the file and print the summary to the terminal.

## File Structure

- [`summarizer.py`](summarizer/summarizer.py): Main script for running the summarizer.
- [`aid_funct.py`](summarizer/aid_funct.py): Helper functions for PDF reading, text cleaning, chunking, and LLM interaction.
- `requirements.txt`: Python dependencies.

## Notes

- The summary is generated using OpenAI's GPT models. Ensure your API key has sufficient quota.
- The script currently supports only PDF files.

## License

MIT License