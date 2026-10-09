
import os
import requests
import streamlit as st

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/vehicle-leads/chat",
)

st.set_page_config(
    page_title="Vehicle Lead Agent",
    page_icon="🚗",
    layout="centered",
)

st.title("🚗 Vehicle Lead Agent")
st.caption("Search and manage vehicle leads in AutoLoop")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_message = st.chat_input("Ask about a vehicle lead...")

if user_message:
    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Checking AutoLoop..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"message": user_message},
                    timeout=60,
                )
                response.raise_for_status()
                data = response.json()
                assistant_message = data.get(
                    "response", "No response received."
                )
            except requests.exceptions.RequestException as e:
                assistant_message = (
                    f"Unable to connect to the Vehicle Lead Agent: {e}"
                )
            except Exception as e:
                assistant_message = f"Something went wrong: {e}"

        st.markdown(assistant_message)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_message}
    )