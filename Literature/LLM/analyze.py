import sys
import os
from openai import OpenAI
from openai.types.beta.threads.message_create_params import Attachment, AttachmentToolFileSearch

# Ensure correct number of arguments
if len(sys.argv) != 4:
    print("Usage: python analyze.py <pdf_filename> <paper_number> <response_filename>")
    sys.exit(1)

pdf_filename = sys.argv[1]
paper_number = sys.argv[2]
response_filename = sys.argv[3]

# Validate PDF file
if not pdf_filename.lower().endswith(".pdf") or not os.path.exists(pdf_filename):
    print("Error: Provide a valid PDF file.")
    sys.exit(1)

client = OpenAI()

# Upload the PDF
try:
    file = client.files.create(
        file=open(pdf_filename, 'rb'),
        purpose='assistants'
    )
except Exception as e:
    print(f"Error uploading file: {e}")
    sys.exit(1)

# Create a thread
thread = client.beta.threads.create()

def get_assistant():
    """Retrieve or create the Literature Analysis Assistant."""
    assistants = list(client.beta.assistants.list())
    for assistant in assistants:
        if assistant.name == 'Literature Analysis Assistant':
            return assistant

    return client.beta.assistants.create(
        model='gpt-4o',
        instructions="You are a research assistant specializing in clone detection. Your task is to analyze how BigCloneBench is used in a given research paper. You will extract key metadata, summarize the study, answer specific research questions, and evaluate the paper’s validity based on recent findings regarding BigCloneBench’s accuracy. Your responses should be well-structured, concise, and supported with direct quotes and page numbers where possible.",
        tools=[{"type": "file_search"}],
        name='Literature Analysis Assistant',
    )

assistant = get_assistant()

# Read and send first prompt
with open('PROMPT.md', 'r') as f:
    prompt1 = f.read()

prompt1 = prompt1.replace("PAPER_NUMBER", paper_number)

client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content=prompt1,
    attachments=[Attachment(file_id=file.id, tools=[AttachmentToolFileSearch(type='file_search')])]
)

# Run assistant processing
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    timeout=300,
    temperature=0.00000000000001,
    top_p=0.00000000000001
)

if run.status != "completed":
    print(f"Run failed with status: {run.status}")
    sys.exit(1)

# Fetch response
messages = list(client.beta.threads.messages.list(thread_id=thread.id))
message1 = messages[0]
assert message1.content[0].type == "text"
res_txt1 = message1.content[0].text.value

# Read and send second prompt
with open('PROMPT2.md', 'r') as f:
    prompt2 = f.read()

prompt2 = prompt2.replace("PAPER_NUMBER", paper_number)

client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content=prompt2,
    attachments=[Attachment(file_id=file.id, tools=[AttachmentToolFileSearch(type='file_search')])]
)

# Run assistant processing again
run2 = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    timeout=300,
    temperature=0.00000000000001,
    top_p=0.00000000000001
)

if run2.status != "completed":
    print(f"Run 2 failed with status: {run2.status}")
    sys.exit(1)

# Fetch second response
messages2 = list(client.beta.threads.messages.list(thread_id=thread.id))
message2 = messages2[0]
assert message2.content[0].type == "text"
res_txt2 = message2.content[0].text.value

# Write output to the markdown file
with open(response_filename, 'w', encoding='utf-8') as f:
    f.write(f"# Analysis of Paper {paper_number}\n\n")
    f.write(res_txt1 + "\n\n")
    f.write("# Summary\n\n")
    f.write(res_txt2 + "\n")

print(f"Output saved to {response_filename}")

# Clean up uploaded file
try:
    if file and hasattr(file, 'id'):
        client.files.delete(file.id)
except Exception as e:
    print(f"Error deleting file: {e}")
