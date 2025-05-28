# 📄 AI\_RAG: AWS-Powered PDF Chatbot with Admin/User Dashboards

AI\_RAG is a Streamlit-based chatbot platform that allows users to upload PDFs, trains a context-aware RAG (Retrieval Augmented Generation) system using **AWS Bedrock**, and answers questions based on the uploaded documents. It features role-based **Admin** and **User dashboards**, **S3 integration** for secure PDF storage, and **AWS Bedrock** for scalable inference.

---

## 🧠 Features

* 🔐 Role-based login system (Admin & User)
* 📁 Upload PDFs and store securely on **AWS S3**
* 🧠 Perform question answering using **AWS Bedrock** (Claude or Titan)
* 📊 Admin dashboard to monitor user activity and system stats
* 📄 User dashboard to upload, view, and chat with PDFs
* 📦 Fully serverless architecture with **AWS-native services**

---

## 🧰 Tech Stack

| Layer       | Tool/Service               |
| ----------- | -------------------------- |
| Frontend    | Streamlit                  |
| Backend     | Python                     |
| Storage     | AWS S3                     |
| Inference   | AWS Bedrock (Claude/Titan) |
| Auth        | Streamlit session state    |
| PDF Parsing | pdfplumber, PyMuPDF        |

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/SrinithiSaiprasath/AI_RAG.git
cd AI_RAG
```

### 2. Set Up Python Environment

```bash
python -m venv venv
# Activate on Windows
venv\Scripts\activate
# or on Linux/Mac
source venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 🔐 AWS Configuration

### Required AWS Services

* **Amazon S3** (PDF storage)
* **Amazon Bedrock** (Model inference)

### Required IAM Policies

* `AmazonS3FullAccess`
* `AmazonBedrockFullAccess`

### Set Environment Variables in `.env`

Create a `.env` file in the root folder with:

```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
S3_BUCKET_NAME=your_bucket_name
BEDROCK_MODEL_ID=anthropic.claude-v2
```
---

## Docker Setup

### 1. Build the Docker image

```

docker build -t ai_rag_app .
docker run -d -p 8501:8501 --name ai_rag_container ai_rag_app
docker stop ai_rag_container
docker rm ai_rag_container
```

---

## 🚀 Running the Application

```bash
streamlit run app.py
```
---

## 🧠 How It Works

1. **User uploads PDF**
2. **Text parsed** using `pdfplumber` and `PyMuPDF`
3. **Context is prepared** and stored
4. **User types a question**
5. **Bedrock invoked** with context + question
6. **Answer returned** and displayed in Streamlit chat UI


---


## 📦 requirements.txt (Example)

```text
streamlit
boto3
pdfplumber
PyMuPDF
python-dotenv
```

---

## 🛠️ Future Enhancements

* ✅ Integrate Cognito for secure login
* ✅ Embed tracking of usage history
* ✅ Store chat logs per document
* ✅ Add Claude streaming for real-time answers
* ✅ Index content into FAISS for fast retrieval

---

## 👩‍💼 Author

**Srinithi Saiprasath**
🔗 [GitHub](https://github.com/SrinithiSaiprasath) | [LinkedIn](https://linkedin.com/in/srinithisaiprasath)

---

## 📜 License

MIT License © Srinithi Saiprasath
