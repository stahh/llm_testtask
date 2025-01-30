import chromadb
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from transformers import pipeline

# Chroma setup
client = chromadb.Client()
vector = client.create_collection("rss-aggregator", get_or_create=True)

# LangChain setup
model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"
llama_pipeline = pipeline(
    "text-generation",
    model=model_id,
    device_map="auto",
)
llm = HuggingFacePipeline(pipeline=llama_pipeline)
prompt_template = PromptTemplate(template="Summarize the following article: {article}")
llm_chain = LLMChain(llm=llm, prompt=prompt_template)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
