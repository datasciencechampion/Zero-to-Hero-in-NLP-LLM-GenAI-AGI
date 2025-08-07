import streamlit as st
import ollama

def chat_with_ollama(model_name, user_input, conversation_history):
    """
    Function to interact with an Ollama model, appending user input and getting AI response.
    """
    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # Call Ollama's chat API
        response = ollama.chat(
            model=model_name,
            messages=conversation_history
        )
        ai_response = response["message"]["content"]

        # Add AI response to conversation history
        conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response, conversation_history
    except Exception as e:
        return f"Error: {e}", conversation_history

# Streamlit app setup
st.title("Ollama Chat App")
st.write("Interact with a local Ollama model. Select a model and start chatting!")

# Initialize session state for conversation history and model selection
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "model_name" not in st.session_state:
    st.session_state.model_name = "llama3.2"

# Model selection dropdown
available_models = ["llama3.2", "gpt-oss:20b","mistral", "gemma"]  # Adjust based on your Ollama models
st.session_state.model_name = st.selectbox(
    "Select Model", available_models, index=available_models.index(st.session_state.model_name)
)

# Input box for user message
user_input = st.text_input("Your Message:", placeholder="Type your message here...", key="user_input")

# Send button
if st.button("Send"):
    if user_input.strip():
        # Get AI response and update conversation history
        ai_response, st.session_state.conversation_history = chat_with_ollama(
            st.session_state.model_name, user_input, st.session_state.conversation_history
        )
        # Force a rerun to update the UI
        st.rerun()
    else:
        st.warning("Please enter a message.")

# Display conversation history
st.subheader("Conversation")
for message in st.session_state.conversation_history:
    if message["role"] == "user":
        st.markdown(f"**You**: {message['content']}")
    else:
        st.markdown(f"**AI**: {message['content']}")

# Clear conversation button
if st.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.rerun()