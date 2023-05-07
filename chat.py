# 
# build a question answer over docs with langchain. Load text from cursor.txt and supabase.txt. Use openai to tokennize. Use gpt3 to generate answer.
# see https://python.langchain.com/en/latest/modules/chains/index_examples/qa_with_sources.html to add metadata
# @todo use webloader
from langchain import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import os
from rich import pretty
from rich.console import Console
pretty.install()
console = Console()
# query = "I would like to have four AI tools to help me speed up my coding and programming workflow. I can use the tool to chat with my code and it can help me write codes with AI and GPT. List some Tools and their intros in bullet points. Think about why they fits my needs. "
# query = 'Can you recommend four AI-powered coding and programming tools that enable a conversational interface with the code, utilize AI and GPT technology for code generation, and provide brief descriptions of their key features in bullet points, while also explaining how each tool is particularly suited to enhance and expedite my coding workflow?'
# query = "Do you think cursor.io would be a good fit to for me to use to speed up my coding with the help of AI and GPT? In this way I can chat with my code."
query = "I would like a tool to speed up my coding with the help of AI and GPT? In this way I can chat with my code. Give the name of the tool and the url"
# query = 'I would like to have four tools to help me increase the resolution of my photo. Think setp by stpe and why it might fit my needs.'
# query = 'I would like to have a tool to access NFT data. Think step by step why it fits my needs.'

loader = DirectoryLoader('./text/', loader_cls=TextLoader)
# go over each documents in text directory and load them with textLoader and put them in a array
docs_array = []
metadata_array = []
directory = "text"

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        loader = TextLoader(file_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        for t in texts:
            t.metadata = {'source': filename.split(
                '.txt')[0], 'url': documents[0].page_content.split('.\n')[1]}
        # join docs_array and docs two arrays
        docs_array = docs_array + texts
docsearch = Chroma.from_documents(
    docs_array, embeddings, metadatas=metadata_array)
docs = docsearch.similarity_search(query)[:-2]
question_prompt_template = """Use the following portion of a long document to see if any of the text is relevant to answer the question. 
Return any relevant text in English.
{context}
Question: {question}
Relevant text, if any, in English:"""
QUESTION_PROMPT = PromptTemplate(
    template=question_prompt_template, input_variables=["context", "question"]
)

combine_prompt_template = """Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES"). 
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
console.log(
    chain({"input_documents": docs, "question": query}, return_only_outputs=True))
