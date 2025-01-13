# Quiz-Doc_RAG_Model - Document QA with Google Gemini

Quiz-Doc_RAG_Model is an interactive Document Question Answering (QA) application powered by Google Gemini and LangChain. It helps users analyze documents (PDF, DOCX, or CSV format), extract answers for exam-related questions, identify important topics for exam preparation, and interact with the AI to clarify doubts on specific topics.

## Features

- **Upload Documents**: Supports PDF, DOCX, and CSV file uploads.
- **Answer Extraction**: Automatically extracts answers for questions from the uploaded documents.
- **Topic Identification**: Identifies key topics that are important for exam preparation.
- **Interactive Doubt Resolution**: Ask questions based on important topics and get AI-powered responses for clarification.

## Prerequisites

To run the application, you'll need the following:

- **Python 3.7 or higher**: Ensure you're using Python 3.7 or higher.
- **Google Gemini API Key**: You’ll need a Google Gemini API key to use the model. You can obtain this from [here](https://aistudio.google.com/prompts/new_chat).

## Setup Instructions

### Step 1: Clone the Repository

Clone the repository to your local machine:

```
git clone https://github.com/suryanarayananr7/Quiz-Doc_RAG_Model.git
cd Quiz-Doc_RAG_Model
```

### Step 2: Install Dependencies

After cloning the repository, install the necessary dependencies using `pip`. Run the following command in your terminal:

```
pip install --upgrade torch transformers langchain langchain-core langchain-community langchain_google_genai python-docx PyPDF2 pandas streamlit

```

The command will install the following essential libraries:

- `torch`: Deep learning framework for model inference.
- `transformers`: For working with transformer-based models like Google Gemini.
- `langchain`: A framework for integrating AI models into applications.
- `langchain-google-genai`: Google Gemini integration.
- `python-docx`: For reading DOCX files.
- `PyPDF2`: For reading PDF files.
- `pandas`: For reading CSV files.
- `streamlit`: To build and run the UI.

### Step 3: Set Up Google Gemini API Key

1. **Obtain your Google Gemini API key** from [Google Gemini](https://aistudio.google.com/prompts/new_chat).
2. After obtaining the API key, you will be prompted to enter it in the application when you run it.
3. You can also use the Default API key provided.

### Step 4: Run the Application

To run the application, use the following command:

```
streamlit run app.py
```

This will start the Streamlit server, and you can access the app in your web browser at `http://localhost:8501`.

### Step 5: Using the Application

1. **Upload a Document**:
   - Use the file uploader in the app to upload a PDF, DOCX, or CSV file.

2. **Enter your Google Gemini API Key**:
   - Use the default API key or Paste your Google Gemini API key by selecting the appropriate radio button .

3. **Get the Answers**:
   - The app will automatically extract answers to exam-related questions from the uploaded document.

4. **View Important Topics**:
   - The app will display important topics based on the document’s content.

5. **Ask Doubts**:
   - You can interact with the AI by typing in questions related to important topics. The AI will respond with explanations.

### Step 6: Customize the Application

If you wish to customize the application, you can modify the following files:

- `LangChain_model.py`: Contains functions for initializing the model, processing documents, extracting answers, identifying important topics, and handling Q&A.
- `app.py`: The main Streamlit app file responsible for setting up the user interface and calling functions from `LangChain_model.py`.

### Troubleshooting

- **Error: "API key is invalid"**:
  - Ensure you have entered a valid Google Gemini API key.

- **Error: "Unsupported file type"**:
  - Verify that the uploaded file is in PDF, DOCX, or CSV format.

- **Error: "No questions found"**:
  - Make sure the document contains questions that can be extracted for answering.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project leverages LangChain and Google Gemini for powerful document analysis and question answering.

