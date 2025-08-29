import PyPDF2 as pdfr
import re
import tiktoken
from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

def pdf_reader(pdf_path, txt_path):
    # Open pdf file in rb mode
    with open(pdf_path, "rb") as pdf_file:
        reader = pdfr.PdfReader(pdf_file)
        text = ""

        # Loop through each page and extract text
        for page in reader.pages:
            text += page.extract_text() + "\n"

    return text

def text_cleaner(text):
    # Remove broken hyphens, newlines, and extra spaces
    text = text.replace("-\n", "")  # Remove newlines
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def chunk(text, chunk_size, overlap, model):
    # Splits text into chunks of about 'chunk size' tokens with 'overlap' tokens shared between chunks

    # grabs model specific encoder and encodes token
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)

    chunks = []
    start = 0

    # Loop until all tokens are chunked
    while start < len(tokens):
        end = start + chunk_size
        # Grab specific length of token
        chunk_tokens = tokens[start:end]

        # Append the to the chunk array after decoding back into text
        chunks.append(enc.decode(chunk_tokens))
        # Reset the start
        start += chunk_size - overlap

    return chunks

def summarize_chunk(client, model, sys_prompt, task_prompt, chunk_text):
    resp = client.responses.create(
        model = model,
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": sys_prompt}]},
            {"role": "user",   "content": [{"type": "input_text", "text": f"{task_prompt}\n\n---\n{chunk_text}"}]},
        ],
        max_output_tokens = 500
    )
    return resp.output_text

def synthesize(client, model, sys_prompt, synth_prompt, synth_input):
    summary = client.responses.create(
        model = model,
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": sys_prompt}]},
            {"role": "user",   "content": [{"type": "input_text", "text": f"{synth_prompt}\n\n---\n{synth_input}"}]},
        ],
        max_output_tokens = 1000
    )
    return summary.output_text


