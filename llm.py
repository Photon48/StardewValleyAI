from openai import OpenAI
import streamlit as st

import os


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Create Thread:
thread = client.beta.threads.create()

def run_assistant(prompt):
    print(prompt)
    messages = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content= prompt
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id="asst_rHOJBVNrcUVvFHB6aHxArpUy"
    )
    if run.status == 'completed':
        messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")
        print(message_content.value)
        print("\n".join(citations))
        return f"{message_content.value}\n" + "\n".join(citations)
    else:
        print(run.status)
    