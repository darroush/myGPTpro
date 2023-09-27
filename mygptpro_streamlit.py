import streamlit as st
from streamlit_chat import message
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.chains import ChatVectorDBChain
from langchain.document_loaders import DirectoryLoader
import os
import re
import shutil
from PIL import Image
from pdf_loader_tqdm import extract_text, convert_text_to_pdf

os.environ['OPENAI_API_KEY'] = 'put here your openai api'

### initiate streamlit
# import the page icon
img = Image.open('utils/logo_short.png')

# set page configuration
st.set_page_config(page_title="myGPTpro", page_icon= img)

# st.header("Demo version")
st.image('utils/mygptpro.png')

# create columns to align "Beta" to the right
col1, col2, col3, col4 ,col5= st.columns(5)
col5.subheader('Beta')

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "generated_code" not in st.session_state:
    st.session_state["generated_code"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

# Use the uploaded pdf file in the sidebar
with st.sidebar:
    uploaded_file = st.file_uploader('Upload your PDF file')
    st.markdown(":tulip::sunflower::rose: Welcome to :violet[**MyGPTpro**]! :tulip::sunflower::rose:") 
    st.markdown("We are your :orange[AI-powered] companion:robot_face: for document retrieval and information extraction. Upload your PDF file, and let our advanced GPT technology assist you in finding the exact information you need. Our chatbot interface makes it easy to interact and retrieve data effortlessly, saving you time and effort:man-shrugging::full_moon_with_face:. Experience the future of document querying and knowledge extraction with **MyGPTpro**.")

# conditional statement to pause code execution until getting user input
if uploaded_file:
    extract_text(uploaded_file) # use functions from pdf_loader_tqdm.py
    convert_text_to_pdf('output_text.txt', 'data/output_pdf/output.pdf')


    # Create the chroma database
    loader = DirectoryLoader("./data/output_pdf")
    pages = loader.load_and_split()
    
    # Check if the directory exists
    if os.path.exists("./mygpt_DB"):
        # Use shutil.rmtree to remove the directory and its contents to prevent the app from accessing previous data
        shutil.rmtree("./mygpt_DB")

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(pages, embedding=embeddings, persist_directory="./mygpt_DB")
    vectordb.persist()

    # Create the embeddings
    def get_bot():
        embeddings = OpenAIEmbeddings()
        vectordb = Chroma(persist_directory='./mygpt_DB', embedding_function=embeddings)

        #Prediction part
        bot_qa = ChatVectorDBChain.from_llm(OpenAI(temperature=0.9, model_name="gpt-3.5-turbo"),
                                            vectordb, return_source_documents=True)
        
        return bot_qa

    # back to streamlit interface
    def get_text():
        st.header("How can I assist you?")
        input_text = st.text_input("",  key="input")
        return input_text

    user_input = get_text()

    if user_input:
        bot_qa = get_bot()
        result = bot_qa({"question": user_input, "chat_history": ""})
        
        answer_message = result["answer"]
        st.session_state.past.append(user_input)
        st.session_state.generated.append(answer_message)
        
    if st.session_state["generated"]:

        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            # Display the extracted code block(s) with formatting
            message(st.session_state["generated"][i], key=str(i))
        
