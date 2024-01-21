import streamlit as st
import os

session_state = st.session_state

# Landing page
if "session_id" not in session_state:
    st.title("AI Interviewer App")
    st.write("Welcome to the AI-powered interview experience!")
    if st.button("Get Started"):
        import requests  # Import the requests library
        response = requests.get("http://localhost:8000/get_started")  # Send a request to the Flask endpoint
        # print(response)
        session_id = response.json()["session_id"]  # Extract the session ID from the response
        session_state["session_id"] = session_id  # Store the session ID in session state

# Entry page
else:
    # Create a folder for the user's data if it doesn't exist
    if not os.path.exists(f"user_data/{session_state['session_id']}"):
        os.makedirs(f"user_data/{session_state['session_id']}")
    user_data_folder = f"user_data/{session_state['session_id']}"

    st.title("Enter Role and Skills")
    role = st.selectbox("Select Role", ["Software Engineer", "ML Engineer", "React Engineer", "Other"])
    skills = st.multiselect("Select Skills", ["C++", "Java", "Python", "React", "TensorFlow"])

    # Save role and skills to user's folder
    with open(f"{user_data_folder}/role.txt", "w") as f:
        f.write(role)
    with open(f"{user_data_folder}/skills.txt", "w") as f:
        f.write("\n".join(skills))

    st.write("Role and skills saved successfully!")
    # Proceed to the interview page (code not shown)
