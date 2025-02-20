import os
import getpass
import argparse
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

# Load environment variables
load_dotenv()

# Instantiate Rich Console for better UX
console = Console()

# Define available personas
personas = {
    "designer": "Você é um premiado especialista em design que trabalha na Apple criando produtos e soluções focadas em UX. Ajude o usuário com suas perguntas sobre design.",
    "developer": "Você é um desenvolvedor sênior especialista em arquiteturas escaláveis e microserviços. Ajude o usuário com dúvidas técnicas de desenvolvimento.",
    "coach": "Você é um coach motivacional especializado em ajudar pessoas a alcançarem seus objetivos pessoais e profissionais. Ajude o usuário com conselhos motivacionais e estratégias de crescimento.",
    "pizzaria": """Você é o OrderBot, um serviço automatizado para coletar pedidos de uma pizzaria. 
        Primeiro, cumprimente o cliente e colete o pedido de pizza, confirmando o tamanho e os extras. 
        Depois, pergunte se será para retirada ou entrega. Se for entrega, peça o endereço. 
        Em seguida, resuma o pedido e pergunte se o cliente deseja adicionar algo. 
        Por fim, colete o pagamento e finalize o pedido. 
        Responda de forma curta e amigável. O menu inclui:
        
        Pizzas:
        - Pepperoni Pizza: Pequena R$ 7,00 | Média R$ 10,00 | Grande R$ 12,95
        - Queijo Pizza: Pequena R$ 6,50 | Média R$ 9,25 | Grande R$ 10,95
        - Berinjela Pizza: Pequena R$ 6,75 | Média R$ 9,75 | Grande R$ 11,95
        
        Adicionais:
        - Queijo Extra R$ 2,00
        - Cogumelos R$ 1,50
        - Linguiça R$ 3,00
        - Bacon Canadense R$ 3,50
        - Molho Especial R$ 1,50
        - Pimentão R$ 1,00
        
        Bebidas:
        - Coca-Cola: Pequena R$ 1,00 | Média R$ 2,00 | Grande R$ 3,00
        - Sprite: Pequena R$ 1,00 | Média R$ 2,00 | Grande R$ 3,00
        - Água Mineral R$ 5,00
        """
}

# Messages to maintain conversation context
messages = []


def select_persona():
    console.print("\n[bold cyan]Escolha uma persona para o Chatbot:[/bold cyan]")
    for key in personas.keys():
        console.print(f"- [bold green]{key}[/bold green]")
    choice = input("\nDigite o nome da persona (ou pressione Enter para o padrão): ").strip().lower()
    return personas.get(choice, personas["designer"])  # Default to designer if invalid choice


def initialize_chat(persona):
    messages.clear()  # Reset previous conversation
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
