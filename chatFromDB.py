from langchain import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import os
from rich import print, pretty, inspect
from rich.console import Console
from langchain.vectorstores.elastic_vector_search import ElasticVectorSearch
console = Console()
directory = "text"
persist_directory = 'db'
# query = "I would like a tool to speed up my coding with the help of AI and GPT? In this way I can chat with my code. Give the name of the tool and the url"
query="I am looking for a tool to draw grpah from data. Like bar chart, pie chart."
docsearch = Chroma(persist_directory=persist_directory,
                   embedding_function=OpenAIEmbeddings())
docs = docsearch.similarity_search(query)
question_prompt_template = """You are a tech editor. You have reviewd thousands of apps and know a lot about tech and software stuff. Now you are to help people find the things that is suitable for their nedds. Use the following portion of a long document to see if any of the tools is relevant to answer the question.
Return any relevant text in English.
{context}
Question: {question}
Relevant text, if any, in English:"""
QUESTION_PROMPT = PromptTemplate(
    template=question_prompt_template, input_variables=["context", "question"]
)

combine_prompt_template = """Given the following extracted parts of a long list of tools and their intros and a question, create a final answer with references ("SOURCES").
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
ALWAYS return a "SOURCES" part in your answer.
Respond in English.

QUESTION: {question}
=========
{summaries}
=========
FINAL ANSWER:"""
COMBINE_PROMPT = PromptTemplate(
    template=combine_prompt_template, input_variables=["summaries", "question"]
)

chain = load_qa_with_sources_chain(OpenAI(temperature=0), chain_type="map_reduce",
                                   return_intermediate_steps=True, question_prompt=QUESTION_PROMPT, combine_prompt=COMBINE_PROMPT)
# console.log(
# chain({"input_documents": docs, "question": query}, return_only_outputs=True))
response = chain({"input_documents": docs, "question": query},
                 return_only_outputs=False)
# console.log(response["output_text"])
console.log(response)