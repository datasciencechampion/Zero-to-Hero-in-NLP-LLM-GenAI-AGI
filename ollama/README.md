# Ollama Chat Applications

This project contains two Python applications to interact with locally hosted large language models (LLMs) using Ollama:

1. Command-line Chat App (ollama_chat.py): A simple terminal-based interface for chatting with an Ollama model.
2. Streamlit Chat App (ollama_streamlit_chat.py): A web-based interface built with Streamlit for interactive chatting with Ollama models.

Both applications use the ollama Python library to communicate with models like llama3.2 or mistral running on your local Ollama server.

# Prerequisites
- Operating Systems: macOS, Windows, or Linux
- Hardware: At least 8GB RAM (16GB+ recommended for larger models).
- Tools: Terminal (macOS/Linux) or Command Prompt/PowerShell (Windows), curl, and a package manager (Homebrew for macOS, Chocolatey for Windows, or apt/yum for Linux).
- Python: Version 3.8 or higher.

# Setup Instructions
## 1 Install Prerequisites

**For macOS**

Install Xcode Command Line Tools:

xcode-select --install

**For Windows**

Install Chocolatey (package manager):

Open PowerShell as Administrator and run:

Set-ExecutionPolicy Bypass -Scope CurrentUser -Force; iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex

Install Git (for curl and other tools):

choco install git

**For Linux (Ubuntu/Debian)**

## Install essential tools:

- sudo apt update
- sudo apt install curl git

**Linux (CentOS/RHEL)**

## Install essential tools:

- sudo yum install curl git

## 2. Install uv for Virtual Environment Management

uv is a fast Python package and project manager.

**For macOS**

curl -LsSf https://astral.sh/uv/install.sh | sh

Add to PATH in ~/.zshrc:

export PATH="$HOME/.local/bin:$PATH"

Apply changes:

source ~/.zshrc

**For Windows**

Install uv using PowerShell:

iwr -useb https://astral.sh/uv/install.ps1 | iex

Add to PATH in PowerShell profile (e.g., ~\Documents\WindowsPowerShell\profile.ps1):

$env:Path += ";$env:USERPROFILE\.local\bin"

Apply changes:

. $PROFILE

**For Linux**

curl -LsSf https://astral.sh/uv/install.sh | sh

Add to PATH in ~/.bashrc or ~/.zshrc:

export PATH="$HOME/.local/bin:$PATH"

Apply changes:

source ~/.bashrc

Verify installation:

uv --version

## 3. Install Ollama

**For macOS**

curl -fsSL https://ollama.com/install.sh | sh

**For Windows**

Download and install from Ollama Releases (e.g., ollama-setup.exe) and follow the installer.

**For Linux**

curl -fsSL https://ollama.com/install.sh | sh

Verify installation:

ollama --version

## 4. Start the Ollama Server

**For macOS/Linux**

Run in a Terminal:

ollama serve

**For Windows**

Run in Command Prompt or PowerShell:

ollama serve

Keep this window open. Verify it’s running by visiting http://localhost:11434 in a browser (expect a blank page or API info).

## 5. Pull Ollama Models

Pull the models you want to use (e.g., llama3.2 and mistral):

ollama pull llama3.2
ollama pull mistral

List available models:

ollama list

Note: Model sizes vary (llama3.2 is ~2GB, mistral is ~4GB). Ensure sufficient disk space and RAM.

## 6. Set Up the Project

Create a project directory and set up a virtual environment using uv:

mkdir ollama_chat_project
cd ollama_chat_project
uv venv

Activate the virtual environment:

**For macOS/Linux:**

source .venv/bin/activate


**For Windows:**

.venv\Scripts\activate

## 7. Install Dependencies

Install the required Python packages using the provided requirements.txt:

uv pip install -r requirements.txt

The requirements.txt includes:

- ollama: For interacting with the Ollama API.
- streamlit: For the web-based chat interface.

## 8. Save Application Files

Ensure the following files are in your project directory (ollama_chat_project):
- ollama_chat.py: Command-line chat application.
- ollama_streamlit_chat.py: Streamlit web-based chat application.
- requirements.txt: Dependency file.

## 9. Run the Applications

Command-line Chat App

Activate the virtual environment (if not already active):

**For macOS/Linux:**

source .venv/bin/activate

**For Windows:**

.venv\Scripts\activate

Run the command-line app:

python ollama_chat.py

Type messages to chat with the model (defaults to llama3.2).

Type quit to exit.


Example:

Chatting with llama3.2. Type 'quit' to exit.
You: What is the capital of France?
AI: The capital of France is Paris.
You: quit

**Streamlit Chat App**

Ensure the virtual environment is active, then run the Streamlit app:

- streamlit run ollama_streamlit_chat.py

A browser window opens at http://localhost:8501.

Select a model (e.g., llama3.2 or mistral) from the dropdown.

Type a message and click Send to chat.

Click Clear Conversation to reset the chat history.


## Troubleshooting
Ollama Server Not Running: If you see “Connection refused” errors, ensure ollama serve is running in a separate Terminal/Command Prompt.

Model Not Found: Run ollama list to verify available models. Pull missing models with ollama pull <model_name>.
Permission Issues: On Linux/macOS, fix permissions:
sudo chown -R $USER ~/.local/share/uv

On Windows, ensure you have admin rights for installation.
Memory Issues: Larger models (e.g., mistral) require more RAM. Close other applications or use smaller models like llama3.2.
Streamlit Issues: Ensure streamlit is installed (uv pip install streamlit) and the correct Python version is used.

## Notes

Model Customization: Update available_models in ollama_streamlit_chat.py or ollama_gui_chat.py to include other models you’ve pulled.
Performance: llama3.2 is lightweight (~2GB), suitable for most systems. mistral (~4GB) may require more resources.
Enhancements: Add streaming responses or custom styling to the Streamlit apps as needed.
Deactivate Virtual Environment: When done, deactivate with:

**For macOS/Linux:**

deactivate

**For Windows:**

deactivate

## For more details, refer to:

- Ollama Documentation
- uv Documentation
- Streamlit Documentation

