import boto3
import streamlit as st
import os
import uuid
import dotenv
dotenv.load_dotenv()

## s3_client
s3_client = boto3.client("s3")
BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

## Bedrock
# from langchain_community.embeddings import BedrockEmbeddings
# from langchain.llms.bedrock import Bedrock
## prompt and chain
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.llms import Bedrock
from langchain_aws.embeddings import BedrockEmbeddings
from langchain_aws.llms import BedrockLLM 
## Text Splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

## Pdf Loader
from langchain_community.document_loaders import PyPDFLoader

## import FAISS
from langchain_community.vectorstores import FAISS

bedrock_client = boto3.client(service_name="bedrock-runtime")
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0", client=bedrock_client)

folder_path="/tmp/"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def get_unique_id():
    return str(uuid.uuid4())

## load index
def load_index():
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.faiss", Filename=f"{folder_path}my_faiss.faiss")
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.pkl", Filename=f"{folder_path}my_faiss.pkl")

def get_llm():
    llm = BedrockLLM(
        model_id="",  # ✅ valid model ID
        client=bedrock_client,
        model_kwargs={'max_tokens': 512}
    )
    return llm

# get_response()
def get_response(llm,vectorstore, question ):
    ## create prompt / template
    prompt_template = """

    Human: Please use the given context to provide concise answer to the question
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context}
    </context>

    Question: {question}

    Assistant:"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_type="mmr", search_kwargs={"k": 5 , "lambda_mult": 0.5} # keep search_type as similarity search if required
    ),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)
    answer=qa({"query":question})
    return answer['result']


## main method
def main():
    st.header("This is Client Site for Chat with PDF demo using Bedrock, RAG etc")

    load_index()

    dir_list = os.listdir(folder_path)
    # st.write(f"Files and Directories in {folder_path}")
    # st.write(dir_list)

    ## create index
    faiss_index = FAISS.load_local(
        index_name="my_faiss",
        folder_path = folder_path,
        embeddings=bedrock_embeddings,
        allow_dangerous_deserialization=True
    )

    st.write("MODEL INDEXED FOR RETRIVAL")
    question = st.text_input("Please ask your question")
    if st.button("Ask Question"):
        with st.spinner("Querying..."):

            llm = get_llm()

            # get_response
            st.write(get_response(llm, faiss_index, question))
            st.success("Done")
            st.balloons()
            st.write("You can ask another question or upload a new PDF file.")
            st.write("Go to [Admin Page](http://localhost:8501/admin) to upload a new PDF file.")
    

if __name__ == "__main__":
    main()
