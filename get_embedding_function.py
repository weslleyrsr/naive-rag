import getpass
import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load variables from .env into os.environ
load_dotenv()

def get_embedding_function():
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        # With the `text-embedding-3` class
        # of models, you can specify the size
        # of the embeddings you want returned.
        # dimensions=1024
    )
    return embeddings

if __name__ == "__main__":
    get_embedding_function()