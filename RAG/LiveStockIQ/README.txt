Steps to Create Virtual Environment
1. Create a Virtual Environment
	Run the following command in your terminal to create a virtual environment named env:
	python -m venv env

2. Activate the Virtual Environment	
	For Windows
	env\Scripts\activate

	For Linux
	source env/bin/activate

Note : After activation, your terminal will show the name of the environment (e.g., (env)), indicating that the
virtual environment is active.


3. Install Required Libraries:

	There are two options to install.
	If you are using requirements.txt file then
		pip install -r requirements.txt

	Else
		pip install streamlit PyPDF2 python-docx openai python-dotenv plotly

4. Freeze Installed Libraries (Optional)
	If you want to save the list of installed libraries for future reference, run:
	pip freeze > requirements.txt


5. Create a .env File: Add your OpenAI API key:
	OPENAI_API_KEY=your_openai_api_key

6. Run the App:
	streamlit run talk2CV.py

7. Deactivate the Virtual Environment
	When you're done working, deactivate the virtual environment:
	deactivate


How It Works
File Upload:

Users upload their CV as a .pdf or .docx file.
Retriever:

Extracts the entire content of the CV for further processing.
Generator:

Combines the user's query and the retrieved CV content into a prompt for OpenAI's GPT-4 Turbo model.
Generates a context-aware response.
Chat History:

Records the interaction session (queries and responses).
Displays the history for seamless follow-up questions.