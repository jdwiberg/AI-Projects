## Goal is to create a program that sends a pdf to an LLM and gets back a summary
import aid_funct as af


## Prompting user for a pdf file
file = input("Enter the name of the pdf or txt file (include '.pdf'): ")
print("Summarizing: ", file, " ...")

## Read in the pdf or txt file
text = ""
if ".pdf" in file:
    # Read pdf and conver to text
    text = af.pdf_reader(file, "text.txt")
elif ".txt" in file:
    with open(file, "r") as f:
        text = f.read()
        f.close()
else:
    print("Please enter a pdf or txt file")
    exit()

# Clean text
text = af.text_cleaner(text)

# Split the text into chunks
chunks = af.chunk(text, chunk_size=4000, overlap=200, model="gpt-4o-mini")

# System, user, and synthesis prompts
sys_prompt = "You are a precise, faithful scientific summarizer. You avoid speculation and clearly label you limitations."
task_prompt = "Summarize the following text for a college‑level audience. Constraints: Max 6 bullet points, each ≤ 25 words. Include 2–4 key findings, 1–2 caveats. Mention important numbers, dates, or definitions exactly as written. If a term is introduced, define it once succinctly. Return only Markdown bullet points."
synth_prompt = "you are merging multiple chunk summaries from the same document. produce a cohesive summary of about 250 - 300 words with: 5-7 bullet points under 'Main takeaways', a short 'Why It Matters' Paragraph, and a 'Limitations' bullet list. Do not invent facts and only use what appears in chunk summaries."

# Summarize each chunk with LLM
mini_summaries = []
for c in chunks:
    mini_summaries.append(af.summarize_chunk(af.client, "gpt-4o-mini", sys_prompt, task_prompt, c))

# Send mini summaries to LLM for synthesis
synth_input = "\n\n---\n\n".join(mini_summaries)
final_output = af.synthesize(af.client, "gpt-4o-mini", sys_prompt, synth_prompt, synth_input)

print(final_output)