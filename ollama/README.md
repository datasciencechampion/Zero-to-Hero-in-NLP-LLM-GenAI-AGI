Ollama Chat Applications
This project contains two Python applications to interact with locally hosted large language models (LLMs) using Ollama:

Command-line Chat App (ollama_chat.py): A simple terminal-based interface for chatting with an Ollama model.
Streamlit Chat App (ollama_streamlit_chat.py): A web-based interface built with Streamlit for interactive chatting with Ollama models.

Both applications use the ollama Python library to communicate with models like llama3.2 or mistral running on your local Ollama server.
Prerequisites

Operating Systems: macOS, Windows, or Linux
Hardware: At least 8GB RAM (16GB+ recommended for larger models).
Tools: Terminal (macOS/Linux) or Command Prompt/PowerShell (Windows), curl, and a package manager (Homebrew for macOS, Chocolatey for Windows, or apt/yum for Linux).
Python: Version 3.8 or higher.

Setup Instructions
1. Install Prerequisites
macOS
Install Xcode Command Line Tools:
xcode-select --install

Windows
Install Chocolatey (package manager):

Open PowerShell as Administrator and run:Set-ExecutionPolicy Bypass -Scope CurrentUser -Force; iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex


Install Git (for curl and other tools):choco install git



Linux (Ubuntu/Debian)
Install essential tools:
sudo apt update
sudo apt install curl git

Linux (CentOS/RHEL)
Install essential tools:
sudo yum install curl git

2. Install uv for Virtual Environment Management
uv is a fast Python package and project manager.
macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

Add to PATH in ~/.zshrc:
export PATH="$HOME/.local/bin:$PATH"

Apply changes:
source ~/.zshrc

Windows
Install uv using PowerShell:
iwr -useb https://astral.sh/uv/install.ps1 | iex

Add to PATH in PowerShell profile (e.g., ~\Documents\WindowsPowerShell\profile.ps1):
$env:Path += ";$env:USERPROFILE\.local\bin"

Apply changes:
. $PROFILE

Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

Add to PATH in ~/.bashrc or ~/.zshrc:
export PATH="$HOME/.local/bin:$PATH"

Apply changes:
source ~/.bashrc

Verify installation:
uv --version

3. Install Ollama
macOS
curl -fsSL https://ollama.com/install.sh | sh

Windows
Download and install from Ollama Releases (e.g., ollama-setup.exe) and follow the installer.
Linux
curl -fsSL https://ollama.com/install.sh | sh

Verify installation:
ollama --version

4. Start the Ollama Server
macOS/Linux
Run in a Terminal:
ollama serve

Windows
Run in Command Prompt or PowerShell:
ollama serve

Keep this window open. Verify it’s running by visiting http://localhost:11434 in a browser (expect a blank page or API info).
5. Pull Ollama Models
Pull the models you want to use (e.g., llama3.2 and mistral):
ollama pull llama3.2
ollama pull mistral

List available models:
ollama list

Note: Model sizes vary (llama3.2 is ~2GB, mistral is ~4GB). Ensure sufficient disk space and RAM.
6. Set Up the Project
Create a project directory and set up a virtual environment using uv:
mkdir ollama_chat_project
cd ollama_chat_project
uv venv

Activate the virtual environment:

macOS/Linux:source .venv/bin/activate


Windows:.venv\Scripts\activate



7. Install Dependencies
Install the required Python packages using the provided requirements.txt:
uv pip install -r requirements.txt

The requirements.txt includes:

ollama: For interacting with the Ollama API.
streamlit: For the web-based chat interface.

8. Save Application Files
Ensure the following files are in your project directory (ollama_chat_project):

ollama_chat.py: Command-line chat application.
ollama_streamlit_chat.py: Streamlit web-based chat application.
requirements.txt: Dependency file.
ollama_gui_chat.py: GUI chat application (optional, from later context).

ollama_chat.py
import ollama

def chat_with_ollama(model_name="llama3.2"):
    """
    Simple chat function to interact with an Ollama model.
    """
    print(f"Chatting with {model_name}. Type 'quit' to exit.")
    conversation_history = []

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break

        conversation_history.append({"role": "user", "content": user_input})

        try:
            response = ollama.chat(
                model=model_name,
                messages=conversation_history
            )
            ai_response = response["message"]["content"]
            print(f"AI: {ai_response}")

            conversation_history.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    chat_with_ollama()

ollama_streamlit_chat.py
import streamlit as st
import ollama

def chat_with_ollama(model_name, user_input, conversation_history):
    """
    Function to interact with an Ollama model, appending user input and getting AI response.
    """
    conversation_history.append({"role": "user", "content": user_input})

    try:
        response = ollama.chat(
            model=model_name,
            messages=conversation_history
        )
        ai_response = response["message"]["content"]
        conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response, conversation_history
    except Exception as e:
        return f"Error: {e}", conversation_history

st.title("Ollama Chat App")
st.write("Interact with a local Ollama model. Select a model and start chatting!")

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "model_name" not in st.session_state:
    st.session_state.model_name = "llama3.2"

available_models = ["llama3.2", "mistral"]
st.session_state.model_name = st.selectbox(
    "Select Model", available_models, index=available_models.index(st.session_state.model_name)
)

user_input = st.text_input("Your Message:", placeholder="Type your message here...", key="user_input")

if st.button("Send"):
    if user_input.strip():
        ai_response, st.session_state.conversation_history = chat_with_ollama(
            st.session_state.model_name, user_input, st.session_state.conversation_history
        )
        st.rerun()
    else:
        st.warning("Please enter a message.")

st.subheader("Conversation")
for message in st.session_state.conversation_history:
    if message["role"] == "user":
        st.markdown(f"**You**: {message['content']}")
    else:
        st.markdown(f"**AI**: {message['content']}")

if st.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.rerun()

ollama_gui_chat.py (Optional)
import streamlit as st
import ollama
from streamlit.components.v1 import html

def chat_with_ollama(model_name, user_input, conversation_history):
    """
    Function to interact with an Ollama model, appending user input and getting AI response.
    """
    conversation_history.append({"role": "user", "content": user_input})

    try:
        response = ollama.chat(
            model=model_name,
            messages=conversation_history
        )
        ai_response = response["message"]["content"]
        conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response, conversation_history
    except Exception as e:
        return f"Error: {e}", conversation_history

st.markdown(
    """
    <style>
    .stTextInput > div > div > input {
        padding-left: 40px;
    }
    .llama-icon {
        position: absolute;
        left: 10px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 24px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

html("""
<div class="llama-icon">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
    </svg>
</div>
""", height=0)

st.title("Ollama GUI Chat")
st.write("Interact with a local Ollama model. Select a model and send a message!")

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "model_name" not in st.session_state:
    st.session_state.model_name = "gemma:3b"

available_models = ["gemma:3b", "llama3.2", "mistral"]
st.session_state.model_name = st.selectbox(
    "Select Model", available_models, index=available_models.index(st.session_state.model_name),
    key="model_select", label_visibility="collapsed"
)

user_input = st.text_input("Send a message", placeholder="Send a message...", key="user_input")

if st.button("Send"):
    if user_input.strip():
        ai_response, st.session_state.conversation_history = chat_with_ollama(
            st.session_state.model_name, user_input, st.session_state.conversation_history
        )
        st.rerun()
    else:
        st.warning("Please enter a message.")

st.subheader("Conversation")
for message in st.session_state.conversation_history:
    if message["role"] == "user":
        st.markdown(f"**You**: {message['content']}")
    else:
        st.markdown(f"**AI**: {message['content']}")

if st.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.rerun()

9. Run the Applications
Command-line Chat App
Activate the virtual environment (if not already active):

macOS/Linux:source .venv/bin/activate


Windows:.venv\Scripts\activate



Run the command-line app:
python ollama_chat.py


Type messages to chat with the model (defaults to llama3.2).
Type quit to exit.
Example:Chatting with llama3.2. Type 'quit' to exit.
You: What is the capital of France?
AI: The capital of France is Paris.
You: quit



Streamlit Chat App
Ensure the virtual environment is active, then run the Streamlit app:
streamlit run ollama_streamlit_chat.py


A browser window opens at http://localhost:8501.
Select a model (e.g., llama3.2 or mistral) from the dropdown.
Type a message and click Send to chat.
Click Clear Conversation to reset the chat history.

Ollama GUI Chat App (Optional)
Run the GUI app:
streamlit run ollama_gui_chat.py


A browser window opens with a llama icon next to the input field.
Select a model (e.g., gemma:3b) and type a message to chat.

Troubleshooting

Ollama Server Not Running: If you see “Connection refused” errors, ensure ollama serve is running in a separate Terminal/Command Prompt.
Model Not Found: Run ollama list to verify available models. Pull missing models with ollama pull <model_name>.
Permission Issues: On Linux/macOS, fix permissions:sudo chown -R $USER ~/.local/share/uv

On Windows, ensure you have admin rights for installation.
Memory Issues: Larger models (e.g., mistral) require more RAM. Close other applications or use smaller models like llama3.2.
Streamlit Issues: Ensure streamlit is installed (uv pip install streamlit) and the correct Python version is used.

Notes

Model Customization: Update available_models in ollama_streamlit_chat.py or ollama_gui_chat.py to include other models you’ve pulled.
Performance: llama3.2 is lightweight (2GB), suitable for most systems. mistral (4GB) may require more resources.
Enhancements: Add streaming responses or custom styling to the Streamlit apps as needed.
Deactivate Virtual Environment: When done, deactivate with:
macOS/Linux:deactivate


Windows:deactivate





For more details, refer to:

Ollama Documentation
uv Documentation
Streamlit Documentation
