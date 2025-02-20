import os
import getpass
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

# Load variables from .env into os.environ
load_dotenv()

# Instantiate Rich Console for better UX
console = Console()

# Define available personas
personas = {
    "designer": "Você é um premiado especialista em design que trabalha na Apple criando produtos e soluções focadas em UX. Ajude o usuário com suas perguntas sobre design.",
    "developer": "Você é um desenvolvedor sênior especialista em arquiteturas escaláveis e microserviços. Ajude o usuário com dúvidas técnicas de desenvolvimento.",
    "coach": "Você é um coach motivacional especializado em ajudar pessoas a alcançarem seus objetivos pessoais e profissionais. Ajude o usuário com conselhos motivacionais e estratégias de crescimento.",
    "default": "Você é um assistente inteligente pronto para ajudar com qualquer pergunta."
}

# Messages to maintain conversation context
messages = []


def select_persona():
    console.print("\n[bold cyan]Escolha uma persona para o Chatbot:[/bold cyan]")
    for key in personas.keys():
        console.print(f"- [bold green]{key}[/bold green]")
    choice = input("\nDigite o nome da persona (ou pressione Enter para o padrão): ").strip().lower()
    return personas.get(choice, personas["default"])


def initialize_chat(persona):
    messages.append({
        'role': 'system',
        'content': persona
    })


def chat(message):
    messages.append({
        'role': 'user',
        'content': message
    })
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    response = model.invoke(messages)
    response_text = response.content if hasattr(response, 'content') else str(response)
    messages.append({
        'role': 'assistant',
        'content': response_text
    })
    return response_text


def display_response(response_text):
    if not isinstance(response_text, str):
        response_text = str(response_text)
    markdown = Markdown(response_text)
    console.print(markdown)


def main():
    # Check if API Key is set
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

    # Select Persona
    persona = select_persona()
    initialize_chat(persona)
    console.print(f"\n[bold yellow]Persona selecionada:[/bold yellow] {persona}\n")

    # Real-time conversation loop
    console.print("[bold cyan]Iniciando o chatbot... (digite 'sair' para encerrar)[/bold cyan]")
    while True:
        user_input = input("\nVocê: ")
        if user_input.lower() in ['sair', 'exit', 'quit']:
            console.print("\n[bold red]Chat encerrado. Até a próxima![/bold red]")
            break
        response = chat(user_input)
        display_response(response)


if __name__ == "__main__":
    main()
