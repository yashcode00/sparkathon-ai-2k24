import streamlit as st
import json
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from streamlit.components.v1 import html
import streamlit as st
import os
import shutil
import uuid
from pydub import AudioSegment
from st_audiorec import st_audiorec
from utils import (
    extract_resume_information,
    get_system_prompt,
    transcribe_audio,
    get_chat_response,
    convert_text_to_audio,
)

session_state = st.session_state

def get_started():
    session_id = str(uuid.uuid4())
    return session_id


def save_final_system_prompt():
    application_role = ""
    job_description = ""
    resume_information = ""

    user_data_folder = f"user_data/{session_state['session_id']}"
    if os.path.exists(f"{user_data_folder}/role.txt"):
        with open(f"{user_data_folder}/role.txt", "r") as file:
            application_role = file.read()

    if os.path.exists(f"{user_data_folder}/job_requirements.txt"):
        with open(f"{user_data_folder}/job_requirements.txt", "r") as file:
            job_description = file.read()

    if os.path.exists(f"{user_data_folder}/resume.txt"):
        with open(f"{user_data_folder}/resume.txt", "r") as file:
            resume_information = file.read()

    final_system_prompt = get_system_prompt(
        application_role, job_description, resume_information
    )
    with open(f"{user_data_folder}/system_prompt.txt", "w") as f:
        f.write(final_system_prompt)


def conduct_interview():
    user_data_folder = f"user_data/{session_state['session_id']}"

    audio_path = f"{user_data_folder}/uploads/output_data.wav"
    user_message = transcribe_audio(audio_path)

    # Get chat response
    system_prompt = ""
    if os.path.exists(f"{user_data_folder}/system_prompt.txt"):
        with open(f"{user_data_folder}/system_prompt.txt", "r") as file:
            system_prompt = file.read()

    database_path = f"{user_data_folder}/database.json"
    chat_response = get_chat_response(user_message, database_path, system_prompt)
    # chat_response = "Hey, how are you??"
    gpt_audio_path = f"{user_data_folder}/uploads/gpt_audio.wav"
    convert_text_to_audio(chat_response, gpt_audio_path)

    audio_file = open(gpt_audio_path, "rb")
    audio_bytes = audio_file.read()

    st.audio(audio_bytes, format="audio/wav")


def ai_interviewer_page():
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False

    if "session_id" not in session_state:
        st.title("AI Interviewer App")
        st.write("Welcome to the AI-powered interview experience!")
        if st.button("Get Started"):
            session_id = get_started()  # Extract the session ID from the response
            session_state[
                "session_id"
            ] = session_id  # Store the session ID in session state
            st.experimental_rerun()

    # Entry page
    elif not st.session_state.interview_started:
        if not os.path.exists(f"user_data/{session_state['session_id']}"):
            os.makedirs(f"user_data/{session_state['session_id']}")
        user_data_folder = f"user_data/{session_state['session_id']}"

        st.title("Enter Role and Skills")
        role = st.selectbox(
            "Select Role",
            ["Software Engineer", "ML Engineer", "React Engineer", "Other"],
        )
        skills = st.multiselect(
            "Select Skills", ["C++", "Java", "Python", "React", "TensorFlow"]
        )
        job_requirements = st.text_area("Job Requirements:")
        resume = st.file_uploader("Resume (optional):")

        user_data_folder = f"user_data/{session_state['session_id']}"
        with open(f"{user_data_folder}/role.txt", "w") as f:
            f.write(role)
        with open(f"{user_data_folder}/skills.txt", "w") as f:
            f.write("\n".join(skills))
        with open(f"{user_data_folder}/job_requirements.txt", "w") as f:
            f.write(job_requirements)
        if resume is not None:
            resume_text = extract_resume_information(resume)
            print(resume_text)
            with open(f"{user_data_folder}/resume.txt", "w", encoding="utf-8") as f:
                f.write(resume_text)

        st.write("Role and skills saved successfully!")

        if st.button("Start interview"):
            st.session_state.interview_started = True
            save_final_system_prompt()
            with open(f"{user_data_folder}/database.json", "w") as json_file:
                pass
            st.experimental_rerun()

    else:
        st.title("Welcome to your Interview")
        wav_audio_data = st_audiorec()
        user_data_folder = f"user_data/{session_state['session_id']}"

        if wav_audio_data is not None:
            # st.audio(wav_audio_data, format='audio/wav')
            print(type(wav_audio_data))
            audio_segment = AudioSegment(
                wav_audio_data,
            )

            ###
            ### conduct interview

            if not os.path.exists(f"{user_data_folder}/uploads"):
                os.makedirs(f"{user_data_folder}/uploads")
            audio_segment.export(
                f"{user_data_folder}/uploads/output_data.wav", format="wav"
            )

            conduct_interview()
            # st.audio(wav_audio_data, format='audio/wav')

        if st.button("Exit Session"):
            user_data_folder = f"user_data/{session_state['session_id']}"
            if os.path.exists(user_data_folder):
                shutil.rmtree(user_data_folder)  # Delete the entire user data folder
        # Proceed to the interview page (code not shown)
