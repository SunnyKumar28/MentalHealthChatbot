# import streamlit as st
# import numpy as np
# import re
# import random
# import pickle
# import json
# import tensorflow as tf
# from tensorflow import keras
# from keras.utils import pad_sequences
# import os
# import openai

# # Set up your OpenAI API key
# openai.api_key = "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"

# def chatgpt_fallback(user_input):
#     """
#     Use OpenAI's GPT model to generate a response for unrecognized intents.
#     """
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are a highly empathetic and supportive mental health assistant."},
#                 {"role": "user", "content": user_input},
#             ],
#             temperature=0.7,
#             max_tokens=150,
#         )
#         return response['choices'][0]['message']['content'].strip()
#     except Exception as e:
#         return "I'm here to help, but I'm experiencing some technical difficulties. Please try again later."

# # Load the saved model and preprocessors
# model = keras.models.load_model('updated_model.h5')
# with open('updated_tokenizer.pkl', 'rb') as f:
#     tokenizer = pickle.load(f)
# with open('updated_label_encoder.pkl', 'rb') as f:
#     lbl_enc = pickle.load(f)

# # Load intents data
# with open('intents.json', 'r') as f:
#     intents_data = json.load(f)

# # Function to preprocess the input text
# def preprocess_text(text):
#     text = re.sub('[^a-zA-Z\']', ' ', text)
#     text = text.lower()
#     return " ".join(text.split())

# # Function to generate a response
# def generate_response(user_input):
#     preprocessed_input = preprocess_text(user_input)
#     x_test = tokenizer.texts_to_sequences([preprocessed_input])
#     x_test = pad_sequences(x_test, padding='post', maxlen=24)
#     y_pred = model.predict(x_test)
#     y_pred = y_pred.argmax()
#     tag = lbl_enc.inverse_transform([y_pred])[0]

#     responses = [intent['responses'] for intent in intents_data['intents'] if intent['tag'] == tag]
#     if responses:
#         return random.choice(responses[0])
#     else:
#         return chatgpt_fallback(user_input)

# # File to store user credentials
# USER_DATA_FILE = "users.json"

# # Load user data from file
# def load_user_data():
#     if os.path.exists(USER_DATA_FILE):
#         try:
#             with open(USER_DATA_FILE, 'r') as f:
#                 data = json.load(f)
#                 return data if isinstance(data, dict) else {}
#         except json.JSONDecodeError:
#             print("Error: JSON file is invalid or corrupted.")
#             return {}
#     else:
#         return {}

# # Save user data to file
# def save_user_data(user_data):
#     with open(USER_DATA_FILE, 'w') as f:
#         json.dump(user_data, f)

# # Initialize session state
# user_db = load_user_data()
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
# if 'username' not in st.session_state:
#     st.session_state.username = ""
# if 'conversation' not in st.session_state:
#     st.session_state.conversation = []
# if 'user_history' not in st.session_state:
#     st.session_state.user_history = {}
# st.markdown(
#     """
#     <style>
#     /* App Background */
#     body {
#         background: linear-gradient(135deg, #ffffff, #d1e8ff);
#         color: black;
#         font-family: 'Arial', sans-serif;
#     }
#     [data-testid="stAppViewContainer"] {
#         background: linear-gradient(135deg, #ffffff, #d1e8ff);
#         color: black;
#     }
#     [data-testid="stSidebar"] {
#         background: linear-gradient(135deg, #cce7ff, #a1c4fd);
#         color: black;
#     }

#     /* Navigation Bar Styling */
#     [data-testid="stSidebar"] {
#         font-size: 18px;
#         padding: 20px;
#     }
#     [data-testid="stSidebar"] .stRadio>label {
#         display: flex;
#         align-items: center;
#         gap: 10px;
#         font-size: 18px;
#         color: black;
#         margin-bottom: 10px;
#         cursor: pointer;
#     }
#     [data-testid="stSidebar"] .stRadio>label:hover {
#         color: #0078D4;
#         font-weight: bold;
#     }
#     [data-testid="stSidebar"] .stButton>button {
#         background: #0078D4;
#         color: white;
#         border-radius: 10px;
#         padding: 10px;
#         border: none;
#         font-size: 16px;
#         margin-top: 20px;
#         cursor: pointer;
#     }
#     [data-testid="stSidebar"] .stButton>button:hover {
#         background: #005fa3;
#     }

#     /* Chat Styling */
#     .chat-container {
#         display: flex;
#         flex-direction: column;
#         gap: 15px;
#         max-height: 500px;
#         overflow-y: auto;
#         padding: 10px;
#         background: rgba(255, 255, 255, 0.8);
#         border-radius: 10px;
#         box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
#     }
#     .user-message {
#         background-color: #0078D4;
#         color: white;
#         border-radius: 20px;
#         padding: 10px 15px;
#         max-width: 70%;
#         align-self: flex-end;
#         word-wrap: break-word;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#     }
#     .bot-message {
#         background-color: #90EE90;
#         color: black;
#         border-radius: 20px;
#         padding: 10px 15px;
#         max-width: 70%;
#         align-self: flex-start;
#         word-wrap: break-word;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#     }
#     .input-container {
#         position: fixed;
#         bottom: 0;
#         width: 100%;
#         padding: 20px;
#         background: #cce7ff;
#         border-top: 1px solid #ddd;
#     }
#     .send_button {
#         background: #0078D4;
#         color: white;
#         border-radius: 20px;
#         padding: 10px 15px;
#         border: none;
#         cursor: pointer;
#         font-size: 16px;
#         width: 100%;
#         transition: background 0.3s;
#     }
#     .send_button:hover {
#         background: #005fa3;
#     }
#     h2, h3, h4 {
#         text-align: center;
#         color: #333;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Navigation Sidebar with Icons
# st.sidebar.title("Navigation")
# tabs_with_icons = {
#     "Chat": "💬",
#     "User Profile": "👤",
#     "User History": "📜"
# }
# selected_tab = st.sidebar.radio(
#     "Go to:",
#     list(tabs_with_icons.keys()),
#     format_func=lambda tab: f"{tabs_with_icons[tab]} {tab}"
# )



# # # Sidebar navigation panel
# # st.sidebar.title("Navigation")
# # selected_tab = st.sidebar.radio("Go to:", ["Chat", "User Profile", "User History"])

# # Layout for login/signup or chatbot interface
# if not st.session_state.logged_in:
#     st.markdown("<h2 style='text-align: center; color: #4f8cc9;'>Login to Chatbot</h2>", unsafe_allow_html=True)
#     login_choice = st.radio("Choose an option", ["Login", "Sign Up"])

#     if login_choice == "Login":
#         with st.form("login_form"):
#             username = st.text_input("Username")
#             password = st.text_input("Password", type="password")
#             login_submit = st.form_submit_button("Login")

#         if login_submit:
#             if user_db.get(username) == password:
#                 st.session_state.logged_in = True
#                 st.session_state.username = username
#                 st.session_state.user_history.setdefault(username, [])
#                 st.success("Logged in successfully!")
#             else:
#                 st.error("Incorrect username or password.")
#     else:
#         with st.form("signup_form"):
#             new_username = st.text_input("Choose a username")
#             new_password = st.text_input("Choose a password", type="password")
#             confirm_password = st.text_input("Confirm password", type="password")
#             signup_submit = st.form_submit_button("Sign Up")

#         if signup_submit:
#             if new_username in user_db:
#                 st.warning("Username already taken.")
#             elif new_password != confirm_password:
#                 st.warning("Passwords do not match.")
#             elif new_username and new_password:
#                 user_db[new_username] = new_password
#                 save_user_data(user_db)
#                 st.session_state.user_history[new_username] = []
#                 st.success("Signup successful! Please log in.")
#             else:
#                 st.warning("Please fill out all fields.")
# else:
#     if selected_tab == "Chat":
#         st.markdown(f"<h2 style='text-align: center; color: #4f8cc9;'>Welcome, {st.session_state.username}!</h2>", unsafe_allow_html=True)
#         chat_container = st.empty()

#         user_input = st.text_area("You:", "", height=100, max_chars=500)
#         send_button = st.button("Send", key="send_message")

#         if user_input:
#             response = generate_response(user_input)
#             st.session_state.conversation.append(("User", user_input))
#             st.session_state.conversation.append(("Bot", response))
#             st.session_state.user_history[st.session_state.username].append((user_input, response))

#         with chat_container.container():
#             for role, text in reversed(st.session_state.conversation):
#                 if role == "User":
#                     st.markdown(f"<div class='user-message'><strong>You:</strong> {text}</div>", unsafe_allow_html=True)
#                 else:
#                     st.markdown(f"<div class='bot-message'><strong>Bot:</strong> {text}</div>", unsafe_allow_html=True)

#     elif selected_tab == "User Profile":
#         st.markdown("<h2 style='text-align: center; color: #4f8cc9;'>User Profile</h2>", unsafe_allow_html=True)
#         st.write(f"**Username**: {st.session_state.username}")

#     elif selected_tab == "User History":
#         st.markdown("<h2 style='text-align: center; color: #4f8cc9;'>Conversation History</h2>", unsafe_allow_html=True)
#         history = st.session_state.user_history.get(st.session_state.username, [])
#         if history:
#             for i, (user_msg, bot_reply) in enumerate(history, 1):
#                 st.markdown(f"**Conversation {i}**")
#                 st.markdown(f"- **User**: {user_msg}")
#                 st.markdown(f"- **Bot**: {bot_reply}")
#         else:
#             st.write("No conversation history available.")

#     if st.sidebar.button("Logout"):
#         st.session_state.logged_in = False
#         st.session_state.username = ""
#         st.session_state.conversation = []
#         st.session_state.user_history = {}
#         st.session_state.logout_trigger = True

#     if st.session_state.get("logout_trigger"):
#         del st.session_state["logout_trigger"]
#         st.experimental_set_query_params()
import streamlit as st
import numpy as np
import re
import random
import pickle
import json
import tensorflow as tf
from tensorflow import keras
from keras.utils import pad_sequences
import os
import openai
import datetime



# Set up your OpenAI API key
openai.api_key = "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"

# Load the saved model and preprocessors
model = keras.models.load_model('updated_model.h5')
with open('updated_tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)
with open('updated_label_encoder.pkl', 'rb') as f:
    lbl_enc = pickle.load(f)

# Load intents data
with open('intents.json', 'r') as f:
    intents_data = json.load(f)

# Function to preprocess the input text
def preprocess_text(text):
    text = re.sub('[^a-zA-Z\']', ' ', text)
    text = text.lower()
    return " ".join(text.split())

# Function to generate a response
def generate_response(user_input):
    preprocessed_input = preprocess_text(user_input)
    x_test = tokenizer.texts_to_sequences([preprocessed_input])
    x_test = pad_sequences(x_test, padding='post', maxlen=24)
    y_pred = model.predict(x_test)
    y_pred = y_pred.argmax()
    tag = lbl_enc.inverse_transform([y_pred])[0]

    responses = [intent['responses'] for intent in intents_data['intents'] if intent['tag'] == tag]
    if responses:
        return random.choice(responses[0])
    else:
        return chatgpt_fallback(user_input)

# ChatGPT fallback function
def chatgpt_fallback(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a highly empathetic and supportive mental health assistant."},
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
            max_tokens=150,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "I'm here to help, but I'm experiencing some technical difficulties. Please try again later."

# File to store user credentials
USER_DATA_FILE = "users.json"

# Load user data from file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            print("Error: JSON file is invalid or corrupted.")
            return {}
    else:
        return {}

# Save user data to file
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(user_data, f)

# Initialize session state
user_db = load_user_data()
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'user_history' not in st.session_state:
    st.session_state.user_history = {}

# Apply CSS for styling
st.markdown(
    """
    <style>
    /* App Background */
    body {
        background: linear-gradient(135deg, #ffffff, #d1e8ff);
        color: black;
        font-family: 'Arial', sans-serif;
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #ffffff, #d1e8ff);
        color: black;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #cce7ff, #a1c4fd);
        color: black;
    }

    /* Navigation Bar Styling */
    [data-testid="stSidebar"] {
        font-size: 18px;
        padding: 20px;
    }
    [data-testid="stSidebar"] .stRadio>label {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 18px;
        color: black;
        margin-bottom: 10px;
        cursor: pointer;
    }
    [data-testid="stSidebar"] .stRadio>label:hover {
        color: #0078D4;
        font-weight: bold;
    }
    [data-testid="stSidebar"] .stButton>button {
        background: #0078D4;
        color: white;
        border-radius: 10px;
        padding: 10px;
        border: none;
        font-size: 16px;
        margin-top: 20px;
        cursor: pointer;
    }
    [data-testid="stSidebar"] .stButton>button:hover {
        background: #005fa3;
    }

    /* Chat Styling */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        max-height: 500px;
        overflow-y: auto;
        padding: 10px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    .user-message {
        background-color: #0078D4;
        color: white;
        border-radius: 20px;
        padding: 10px 15px;
        max-width: 70%;
        align-self: flex-end;
        word-wrap: break-word;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .bot-message {
        background-color: #90EE90;
        color: black;
        border-radius: 20px;
        padding: 10px 15px;
        max-width: 70%;
        align-self: flex-start;
        word-wrap: break-word;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h2, h3, h4 {
        text-align: center;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navigation Sidebar
st.sidebar.title("Navigation")
tabs_with_icons = {
    "Chat": "💬",
    "User Profile": "👤",
    "User History": "📜"
}
selected_tab = st.sidebar.radio(
    "Go to:",
    list(tabs_with_icons.keys()),
    format_func=lambda tab: f"{tabs_with_icons[tab]} {tab}"
)
import datetime

# Layout for login/signup or chatbot interface
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; color: #4f8cc9;'>Login to Chatbot</h2>", unsafe_allow_html=True)
    login_choice = st.radio("Choose an option", ["Login", "Sign Up"])

    if login_choice == "Login":
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_submit = st.form_submit_button("Login")

        if login_submit:
            user = user_db.get(username)
            if user and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.name = user["name"]  # Store the name for display
                st.session_state.user_history.setdefault(username, [])
                st.success("Logged in successfully!")
            else:
                st.error("Incorrect username or password.")
    else:
        with st.form("signup_form"):
            new_name = st.text_input("Name")
            new_dob = st.date_input(
                "Date of Birth",
                min_value=datetime.date(1900, 1, 1),
                max_value=datetime.date.today(),
            )
            new_username = st.text_input("Choose a username")
            new_password = st.text_input("Choose a password", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            signup_submit = st.form_submit_button("Sign Up")

        if signup_submit:
            if new_username in user_db:
                st.warning("Username already taken.")
            elif new_password != confirm_password:
                st.warning("Passwords do not match.")
            elif new_name and new_dob and new_username and new_password:
                # Save the new user data with name, dob, and password
                user_db[new_username] = {
                    "name": new_name,
                    "dob": str(new_dob),
                    "password": new_password,
                }
                save_user_data(user_db)  # Save to file
                st.session_state.user_history[new_username] = []  # Initialize user history
                st.success("Signup successful! Please log in.")
            else:
                st.warning("Please fill out all fields.")

else:
    if selected_tab == "Chat":
        st.markdown(f"<h2 style='text-align: center; color: #4f8cc9;'>Welcome, {st.session_state.name}!</h2>", unsafe_allow_html=True)
        chat_container = st.empty()
        

        user_input = st.text_area("You:", "", height=100, max_chars=500)
        send_button = st.button("Send", key="send_message")

        if user_input:
            response = generate_response(user_input)
            st.session_state.conversation.append(("User", user_input))
            st.session_state.conversation.append(("Bot", response))
            st.session_state.user_history[st.session_state.username].append((user_input, response))

        with chat_container.container():
            for role, text in reversed(st.session_state.conversation):
                if role == "User":
                    st.markdown(f"<div class='user-message'><strong>You:</strong> {text}</div>", unsafe_allow_html=True)
                elif role == "Bot":
                    st.markdown(f"<div class='bot-message'><strong>Bot:</strong> {text}</div>", unsafe_allow_html=True)
    

    elif selected_tab == "User Profile":
        user = user_db[st.session_state.username]
        st.markdown(f"### Name: {user['name']}")
        st.markdown(f"### Date of Birth: {user['dob']}")
        st.markdown(f"### Username: {st.session_state.username}")
        st.markdown(f"### Password: {'*' * len(user['password'])}")

    elif selected_tab == "User History":
        st.markdown("## Chat History")
        if st.session_state.username in st.session_state.user_history:
            for user_query, bot_response in st.session_state.user_history[st.session_state.username]:
                st.markdown(f"**You:** {user_query}")
                st.markdown(f"**Bot:** {bot_response}")
                st.write("---")
        else:
            st.info("No chat history available.")
            
if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.conversation = []
        st.session_state.user_history = {}
        st.session_state.logout_trigger = True

if st.session_state.get("logout_trigger"):
        del st.session_state["logout_trigger"]
        st.experimental_set_query_params()
