import streamlit as st
from openai import OpenAI
from datetime import datetime


# Get the current date and format it as m/d/yyyy
date_str = datetime.now().strftime("%m/%d/%Y")

# Access the key from secrets
API_KEY = st.secrets["general"]["OPENAI_API_KEY"]

client = OpenAI(api_key=API_KEY)

# Read the content from a text file
with open('gpt4_dr2tracker_preprompt.txt', 'r') as file:
    preprompt = file.read()

# Replace the date "11/08/2024" in the preprompt with the current date
drtracker_preprompt = preprompt.replace("11/08/2024", date_str)

# Initialize the messages structure
messages = [
    {
        "role": "system",
        "content": drtracker_preprompt
    }
]

# Define the function for interaction
def CustomChatGPT(user_input):
    if len(messages) > 1:
        messages.pop()

    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    ChatGPT_reply = response.choices[0].message.content
    return ChatGPT_reply

# Streamlit UI elements
st.title("AI DRtrack Builder: from HTML to TSV")

user_input = st.text_area("Enter the HTML code for the Daily Report:", height=300)

if st.button("Submit"):
    if user_input:
        response = CustomChatGPT(user_input)
        st.text_area("Response", response, height=200)
    else:
        st.warning("Please enter some input before submitting.")
