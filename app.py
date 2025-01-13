import streamlit as st
from src.LangChain_model import initialize_model, process_file_parallel, handle_doubts_based_on_topics
import os

# Load environment variables from .env
#load_dotenv()

# Fetch API key
#default_api_key = os.getenv("GOOGLE_GEMINI_API_KEY", "")
default_api_key = "AIzaSyDgkFl-vSLFuQPfh2nx5lujZ8ZBPpwVqWk"

# Streamlit UI
st.title("Document QA with Google Gemini")

# Option for API key selection
api_key_option = st.radio(
    "How would you like to provide the API Key?",
    ("Use Default API Key", "Enter My Own API Key")
)

# Determine the API key to use
if api_key_option == "Enter My Own API Key":
    user_api_key = st.text_input("Enter your Google Gemini API Key:", type="password")
    api_key = user_api_key if user_api_key else None
else:
    api_key = default_api_key

if api_key:
    # Initialize the model with the API key
    model = initialize_model(api_key)

    # File upload section
    uploaded_file = st.file_uploader("Choose a document", type=["docx", "pdf", "csv"])

    if uploaded_file:
        # Check if the answers and important topics are already stored in session state
        if "answers" not in st.session_state or "important_topics" not in st.session_state:
            try:
                # Process the file to extract answers and important topics
                answers, important_topics, chunks = process_file_parallel(uploaded_file, model)

                # Store the extracted answers and important topics in session state
                st.session_state.answers = answers
                st.session_state.important_topics = important_topics
                st.session_state.chunks = chunks

                # Display answers and important topics
                st.subheader("Final Answers:")
                st.write(st.session_state.answers)

                st.subheader("Important Topics to Ace the Exam:")
                st.write(st.session_state.important_topics)

            except Exception as e:
                st.error(f"Error processing the document: {e}")
        else:
            # If answers and topics are already in session state, just display them
            st.subheader("Final Answers:")
            st.write(st.session_state.answers)

            st.subheader("Important Topics to Ace the Exam:")
            st.write(st.session_state.important_topics)

        # Start the doubt Q&A session
        handle_doubts_based_on_topics(model)

    else:
        st.warning("Please upload a document to get started.")
else:
    st.warning("Please select an API key option or enter your API key to proceed.")
