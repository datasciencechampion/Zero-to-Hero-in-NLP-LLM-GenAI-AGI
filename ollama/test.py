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

        # Add user message to conversation history
        conversation_history.append({"role": "user", "content": user_input})

        try:
            # Call Ollama's chat API
            response = ollama.chat(
                model=model_name,
                messages=conversation_history
            )
            ai_response = response["message"]["content"]
            print(f"AI: {ai_response}")

            # Add AI response to conversation history
            conversation_history.append({"role": "assistant", "content": ai_response})

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    chat_with_ollama("gpt-oss:20b")