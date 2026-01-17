"""Entry point for the application."""

import streamlit as st
from openai import OpenAI
from core.config import config


def run_llm(provider, model, messages):
    """Return LLM model based on provider and model"""
    if provider:
        client = OpenAI(api_key=config.OPENAI_API_KEY,
                        base_url="https://openrouter.ai/api/v1",)
        model = model or 'nvidia/nemotron-3-nano-30b-a3b:free'
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            extra_body={"reasoning": {"enabled": False}}
        )
        return response.choices[0].message.content or ""
    else:
        return "Provider not supported"


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
                response = run_llm(
                    "openai",
                    "nvidia/nemotron-3-nano-30b-a3b:free",
                    st.session_state.messages
                )
                st.markdown(response)
                st.session_state.messages.append(
                    {'role': 'assistant', 'content': response}
                )


if __name__ == "__main__":
    main()
