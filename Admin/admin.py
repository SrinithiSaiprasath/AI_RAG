import boto3
import streamlit as st
import os
import uuid

## s3_client
s3_client = boto3.client("s3")
# BUCKET_NAME = os.getenv("BUCKET_NAME")
BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

## Bedrock
# from langchain_community.embeddings import BedrockEmbeddings
from langchain_aws.embeddings import BedrockEmbeddings
## Text Splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

## Pdf Loader
from langchain_community.document_loaders import PyPDFLoader

## import FAISS
from langchain_community.vectorstores import FAISS

bedrock_client = boto3.client(service_name="bedrock-runtime" , region_name= "")
bedrock_embeddings = BedrockEmbeddings(model_id="", client=bedrock_client)

def get_unique_id():
    return str(uuid.uuid4())


## Split the pages / text into chunks
def split_text(pages, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(pages)
    return docs

## create vector store
def create_vector_store(request_id, documents):
    vectorstore_faiss=FAISS.from_documents(documents, bedrock_embeddings)
    file_name=f"{request_id}.bin"
    folder_path="/tmp/"
    vectorstore_faiss.save_local(index_name=file_name, folder_path=folder_path)

    ## upload to S3
    # s3_client.upload_file(Filename=folder_path + "/" + file_name + ".faiss", Bucket=os.getenv("BUCKET_NAME"), Key="my_faiss.faiss")
    # s3_client.upload_file(Filename=folder_path + "/" + file_name + ".pkl", Bucket=os.getenv("BUCKET_NAME"), Key="my_faiss.pkl")

    s3_client.upload_file(Filename=os.path.join(folder_path, file_name + ".faiss"), Bucket=BUCKET_NAME, Key="my_faiss.faiss")
    s3_client.upload_file(Filename=os.path.join(folder_path, file_name + ".pkl"), Bucket=BUCKET_NAME, Key="my_faiss.pkl")
    st.write("Vector store created and uploaded to S3 successfully.")
    st.write(f"Vector store file name: {file_name}")

    return True

## main method
def main():
    st.write("This is Admin Site for Chat with PDF demo")
    uploaded_file = st.file_uploader("Choose a file", type = ["pdf","csv","txt","docx"] , allow_multiple_files=True)
    if uploaded_file is not None:
        request_id = get_unique_id()
        st.write(f"Request Id: {request_id}")
        saved_file_name = f"{request_id}.pdf"
        with open(saved_file_name, mode="wb") as w:
            w.write(uploaded_file.getvalue())

        loader = PyPDFLoader(saved_file_name)
        pages = loader.load_and_split()

        st.write(f"Total Pages: {len(pages)}")

        progress = st.progress(0, text="Starting vector store creation...")

        progress.progress(10, "Splitting text...")
        splitted_docs = split_text(pages, 1000, 200)
        st.write(f"Splitted Docs length: {len(splitted_docs)}")

        progress.progress(40, "Creating vector embeddings...")
        progress.progress(70, "Saving vector store and uploading to S3...")
        result = create_vector_store(request_id, splitted_docs)

        progress.progress(100, "Completed!")

        if result:
            st.success("✅ Hurray!! PDF processed successfully")
        else:
            st.error("❌ Error!! Please check logs.")
        os.remove(saved_file_name)
        st.balloons()
        st.write("You can now go to the chat page to interact with the PDF.")
        st.write("Go to [Chat Page](http://localhost:8501/chat)")

if __name__ == "__main__":
    main()
