import os
import streamlit as st  # Import Streamlit
from langchain_google_genai import ChatGoogleGenerativeAI
from docx import Document
import PyPDF2
import pandas as pd
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableParallel, RunnableLambda
from langchain.schema.output_parser import StrOutputParser
import re

# Initialize the Google Gemini model
def initialize_model(api_key):
    os.environ["GOOGLE_API_KEY"] = api_key
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    return model

# Function to read and extract text from a .docx document (from uploaded file)
def read_docx(uploaded_file):
    doc = Document(uploaded_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Function to read and extract text from a .pdf document (from uploaded file)
def read_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    full_text = []
    for page in pdf_reader.pages:
        full_text.append(page.extract_text())
    return '\n'.join(full_text)

# Function to read and extract text from a .csv file (from uploaded file)
def read_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    if 'Question' in df.columns:
        return '\n'.join(df['Question'].dropna().astype(str).tolist())
    raise ValueError("The CSV file does not contain a 'Question' column.")

# Function to chunk the document text by questions (split by question number)
def chunk_text_by_questions(text, num_questions_per_chunk=29):
    questions = text.split("Question")
    questions = [f"Question {q.strip()}" for q in questions if q.strip()]
    chunks = [questions[i:i + num_questions_per_chunk] for i in range(0, len(questions), num_questions_per_chunk)]
    return chunks

# Function to extract answers for each question
def extract_answers(features):
    answer_template = ChatPromptTemplate.from_messages(
        [("system", "You are an expert exam analyzer."),
         ("human", "Given these questions: {features}, provide the answer only in the format 'Question <number>: Option. (No other information must be displayed)'.")]
    )
    return answer_template.format_prompt(features=features)

# Function to identify important topics for the exam
def identify_important_topics(features):
    topics_template = ChatPromptTemplate.from_messages(
        [("system", "You are an expert exam guide."),
         ("human", "Given these questions: {features}, list the important topics that will help in acing the exam.")]
    )
    return topics_template.format_prompt(features=features)

# Function to handle Q&A conversation based on topics
def handle_doubts_based_on_topics(model):
    """
    Function to interact with the user based on their doubts regarding specific topics.
    It uses the model to generate responses to user inputs.
    """
    st.subheader("Ask your doubts about any topic (Type 'exit' to end the conversation):")
    user_input = st.text_input("You: ")

    if user_input:
        if user_input.lower() == "exit":
            st.write("Exiting conversation.")
        else:
            # Use the AI model to generate an explanation for the user's input topic
            response = model.predict(f"Explain a few lines about {user_input} for understanding for an MCQ exam.")
            # Display the generated explanation
            st.write(f"AI: {response}")

# Parallel execution to extract answers and important topics
def process_file_parallel(uploaded_file, model):
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    # Read document based on file extension
    if file_extension == '.docx':
        doc_text = read_docx(uploaded_file)
    elif file_extension == '.pdf':
        doc_text = read_pdf(uploaded_file)
    elif file_extension == '.csv':
        doc_text = read_csv(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a .docx, .pdf, or .csv file.")
    
    # Chunk the document text by questions
    chunks = chunk_text_by_questions(doc_text)

    # Define the parallel branches (answers extraction and topic identification)
    answers_branch_chain = (
        RunnableLambda(lambda x: extract_answers(x)) 
        | model 
        | StrOutputParser()
    )

    topics_branch_chain = (
        RunnableLambda(lambda x: identify_important_topics(x)) 
        | model 
        | StrOutputParser()
    )

    # Create the parallel chain
    chain = (
        RunnableParallel(
            branches={"answers": answers_branch_chain, "topics": topics_branch_chain}
        )
    )

    # Run the parallel chain
    result = chain.invoke(chunks)

    # Extract answers and topics from the result
    answers = result["branches"]["answers"] if "answers" in result["branches"] else []
    topics = result["branches"]["topics"] if "topics" in result["branches"] else []

    # Clean up answers format to display them line by line
    answers = "\n".join(answers).replace("\n", " ") if answers else "No answers found."

    # Clean up important topics format
    important_topics = topics if topics else "No important topics found."

    return answers, important_topics, chunks
