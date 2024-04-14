import os
import shutil
import streamlit as st
from PIL import Image
from lyzr import ChatBot

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]

# Set Streamlit page configuration
st.set_page_config(
    page_title="Lyzr",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png",
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Library Assistant")
st.markdown("### Built using Lyzr SDK🚀")
st.markdown("Discover personalized book recommendations tailored to your preferred genre with the help of this Library Assistant app, powered by Lyzr's ChatBot.")

# Function to remove existing files in the directory
def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")

# Set the local directory
data_directory = "data"

# Create the data directory if it doesn't exist
os.makedirs(data_directory, exist_ok=True)

# Remove existing files in the data directory
remove_existing_files(data_directory)

# Function to implement RAG Lyzr Chatbot
def rag_implementation(file_path):
    # Check the file extension
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == ".pdf":
        # Initialize the PDF Lyzr ChatBot
        rag = ChatBot.pdf_chat(
            input_files=[file_path],
            llm_params={"model": "gpt-4"},
        )
    elif file_extension.lower() == ".docx":
        # Initialize the DOCX Lyzr ChatBot
        rag = ChatBot.docx_chat(
            input_files=[file_path],
            llm_params={"model": "gpt-4"},
        )
    else:
        # Handle unsupported file types
        raise ValueError("Unsupported file type. Only PDF and DOCX files are supported.")

    return rag

# Function to get Lyzr response
def advisor_response(file_path, preferred_genre):
    rag = rag_implementation(file_path)
    prompt = f""" You are an Expert LIBRARY ASSISTANT BOT. Always introduce yourself. Your task is to ANALYZE an uploaded document and USER INPUT concerning their preferred genres. 
                  
                  Based on this information, you MUST RECOMMEND relevant books to the user.
                  
                  Here's your step-by-step guide:

                  1. First, EXAMINE the uploaded documents CAREFULLY, categorize and display them accordingly in a tabular format.

                  2. Next, After the user enters their (genre{preferred_genre}).Use this information in the next step.

                  3. Then, COMPARE the user's preferred genre with your categorized list to IDENTIFY potential book matches.

                  4. After that, SELECT a variety of titles from the matched list that you believe will best suit the user's genre taste. 
                     If the preferred genre cannot be matched with the book list, state that the books are currently not available and kindly suggest the user to select an another genre or explore different genres.
                     
                  5. Now, PRESENT these recommendations to the user in an organized manner, perhaps by ranking them or grouping similar titles together.
                   
                  Follow these steps thoroughly and make sure after that display the recommendations.
                   """
    response = rag.chat(prompt)
    return response.response

# File upload widget
uploaded_file = st.file_uploader("Upload your book list here⬇️", type=["pdf", "docx"])

# If a file is uploaded
if uploaded_file is not None:
    # Save the uploaded file to the data directory
    file_path = os.path.join(data_directory, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getvalue())
    
    # Display the path of the stored file
    st.success("File successfully saved")

    # Get preferred genre after file upload
    preferred_genre = st.text_input("Enter your preferred genre")

    # Generate advice button
    if st.button("Get Recommendation"):
        automatic_response = advisor_response(file_path, preferred_genre)
        st.markdown(automatic_response)

# Footer or any additional information
with st.expander("ℹ️ - About this App"):
    st.markdown(
        """Experience the seamless integration of Lyzr's ChatBot as you refine your documents with ease. For any inquiries or issues, please contact Lyzr."""
    )
    st.link_button("Lyzr", url="https://www.lyzr.ai/", use_container_width=True)
    st.link_button(
        "Book a Demo", url="https://www.lyzr.ai/book-demo/", use_container_width=True
    )
    st.link_button(
        "Discord", url="https://discord.gg/nm7zSyEFA2", use_container_width=True
    )
    st.link_button(
        "Slack",
        url="https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw",
        use_container_width=True,
    )
