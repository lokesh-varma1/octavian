from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from tempfile import NamedTemporaryFile
from langchain_cohere.llms import Cohere
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere.embeddings import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

app = Flask(__name__)
CORS(app)

# Secret key for session management (replace with your secure key)
app.secret_key = 'your_secret_key'

# Initialize LangChain components
cohere_api_key = "uml0lVi8lxTjTL10Bkb42inOlNFk3zDf7sELxPDN"  # Replace with your actual API key
llm = Cohere(cohere_api_key=cohere_api_key)
prompt = hub.pull("rlm/rag-prompt")

def save_and_process_document(file):
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        file.save(temp_file.name)
        temp_file_path = temp_file.name

    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()

    embeddings_model = CohereEmbeddings(cohere_api_key=cohere_api_key)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1100, chunk_overlap=150)
    splits = text_splitter.split_documents(docs)

    db = FAISS.from_documents(splits, embeddings_model)
    retriever = db.as_retriever(kwargs={"score_threshold": 0.5})

    return retriever

def rag_pipeline(query, retriever):
    rag_chain = (
        {"context": retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain.invoke(query)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    retriever = save_and_process_document(file)
    
    # Store retriever information in session
    session['retriever'] = retriever.serialize()  # Ensure retriever has a serialize method or similar

    return jsonify({"message": "File processed successfully"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    retriever_data = session.get('retriever')  # Retrieve retriever from session
    if not retriever_data:
        return jsonify({"error": "No document has been uploaded"}), 400

    # Deserialize retriever object if needed
    retriever = deserialize_retriever(retriever_data)

    try:
        bot_response = rag_pipeline(user_message, retriever)
    except Exception as e:
        print(f"Error: {e}")
        bot_response = "Sorry, I encountered an error while processing your request."

    return jsonify({'response': bot_response})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
