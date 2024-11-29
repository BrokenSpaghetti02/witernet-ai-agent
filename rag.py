from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain_unstructured import UnstructuredLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata
from dotenv import load_dotenv
import os

from unstructured.partition.pdf import partition_pdf
from langchain.docstore.document import Document

class ChatPDF:
    vector_store = None
    retriever = None
    chain = None

    def __init__(self):
        self.model = ChatOllama(model="llama3.2")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        self.prompt = PromptTemplate.from_template(
            """
            <s> [INST] You are an expert on networking topics. Use the following context to answer the question. 
            Ensure that your answer includes ALL THE RELEVANT DETAILS AND CODE required to perform the task.
            You will ALWAYS focus more on the CODE than the text description.
            If you don't know the answer, say you don't know. 
            [/INST] 
            </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer (include all steps): [/INST]
            """
        )
        load_dotenv()
        self.UNSTRUCTURED_API_KEY = os.getenv("UNSTRUCTURED_API_KEY")

    def ingest(self, pdf_file_path: str):
        docs = PyPDFLoader(file_path=pdf_file_path).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)
        
        vector_store = Chroma.from_documents(documents=chunks, embedding=FastEmbedEmbeddings())
        self.retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3,
                "score_threshold": 0.5,
            },
        )
        
        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                      | self.prompt
                      | self.model
                      | StrOutputParser())

    def ask(self, query: str):
        if not self.chain:
            return "Please, add a PDF document first."

        return self.chain.invoke(query)

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None