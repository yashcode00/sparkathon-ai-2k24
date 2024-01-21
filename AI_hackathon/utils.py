import os
import json
from openai import OpenAI
import PyPDF2
from prompts import prompts


def get_system_prompt(application_role, job_description, resume_information):
    sys_prompt = prompts.get("system_prompt_ex", '')
    sys_prompt = sys_prompt.format(application_role=application_role, job_description=job_description, resume_information=resume_information)

    return sys_prompt

def extract_resume_information(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def convert_text_to_audio(text, audio_path):

    print("converting texxt to audio: ", text)
    client_tts = OpenAI(
        api_key="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"
    )
    response = client_tts.audio.speech.create(
        model="tts-1",
        voice="nova",
        input = text,
    )
    response.stream_to_file(audio_path)


def transcribe_audio(audio_path):
    client = OpenAI(
        api_key="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"
    )
    audio_file = open(audio_path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file = audio_file
    )
    print("user transcript: ", transcript)
    return transcript

def get_chat_response(user_message, file_path, system_prompt):
    messages = load_messages(file_path, system_prompt)
    messages.append({"role": "user", "content": user_message.text})

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )
    gpt_response = client.chat.completions.create(
        model="mistralai/mixtral-8x7b-instruct",
        messages=messages,
    )
    parsed_gpt_response = gpt_response.choices[0].message.content
    save_messages(user_message.text, parsed_gpt_response, file_path)
    return parsed_gpt_response

def load_messages(file, final_sys_prompt):
    messages = []
    empty = os.stat(file).st_size == 0

    if not empty:
        with open(file) as db_file:
            data = json.load(db_file)
            for item in data:
                messages.append(item)
    else:
        messages.append(
            {
                "role": "system", "content": final_sys_prompt
            }
        )

    return messages

def save_messages(user_message, gpt_response, file):
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    messages.append({"role": "assistant", "content": gpt_response})

    with open(file, 'w') as f:
        json.dump(messages, f)
