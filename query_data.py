import argparse
import os
import getpass
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from get_embedding_function import get_embedding_function
from dotenv import load_dotenv

# Load variables from .env into os.environ
load_dotenv()

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    response_text = model.invoke(prompt)
    sources = [doc.metadata.get("id", None) for doc, _score in results]

    # Assume 'response_text' is an object or dict with 'content', 'additional_kwargs', etc.
    content = getattr(response_text, "content", None) or response_text.get("content")
    additional_kwargs = getattr(response_text, "additional_kwargs", None) or response_text.get("additional_kwargs", {})
    response_metadata = getattr(response_text, "response_metadata", None) or response_text.get("response_metadata", {})

    formatted_response = f"""\
Response Content:
-----------------
{content}

Response Metadata:
------------------
{response_metadata}

Sources:
--------
"""

    for source in sources:
        formatted_response += f"- {source}\n"

    print(formatted_response)

    return response_text

def main():
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)

if __name__ == "__main__":
    main()