"""Entry point for the application."""

import streamlit as st
import requests
from chatbot_ui.core.config import config


def api_call(url, method, **kwargs):
    """API call to backend"""

    def show_error(message):
        """Streamlit error message"""
        st.error(message)

    try:
        response = getattr(requests, method)(url, **kwargs)
        json_response = response.json()
        if response.status_code != 200:
            error_msg = json_response.get('message', 'Unknown error')
            show_error(error_msg)
            return False, error_msg
        return True, json_response.get('message', '')
    except requests.exceptions.RequestException as e:
        show_error(f"API call failed: {e}")
        return False, str(e)


def main() -> None:
    """Main function"""
    with st.sidebar:
        st.header("Choose Provider and Model")

        provider = st.selectbox(
            "Select provider",
            ["openai", "anthropic", "cohere", "nvidia"]
        )

        if provider == "openai":
            model = st.selectbox(
                "Select model",
                ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
            )
        elif provider == "anthropic":
            model = st.selectbox(
                "Select model",
                ["claude-3-5-sonnet", "claude-3-5-haiku",
                    "claude-3-5-sonnet-20240620"]
            )
        elif provider == "cohere":
            model = st.selectbox(
                "Select model",
                ["xlarge", "large", "medium", "small"]
            )
        elif provider == "nvidia":
            model = 'nvidia/nemotron-3-nano-30b-a3b:free'
        else:
            model = None

        if st.button("Apply"):
            st.session_state.provider = provider
            st.session_state.model = model

    st.title("LLM Chat")

    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {'role': 'assistant', 'content': 'Hello! How can I help you today?'},
        ]

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if prompt := st.chat_input("Hello how can I help you today?"):
        st.session_state.messages.append(
            {'role': 'user', 'content': prompt}
        )
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                success, message = api_call(
                    f'{config.BACKEND_API}/chat',
                    "post",
                    json={
                        "provider": st.session_state.provider,
                        "model": st.session_state.model,
                        "messages": st.session_state.messages
                    }
                )
                if success and isinstance(message, str):
                    st.markdown(message)
                    st.session_state.messages.append(
                        {'role': 'assistant', 'content': message}
                    )


if __name__ == "__main__":
    main()
