# research_tool.py
# A fully featured Research & Knowledge Assistant for Termux
#
# ███████╗ █████╗ ██╗███████╗ █████╗ ███╗   ██╗     ██╗   ██╗██████╗ ██╗  ██╗
# ██╔════╝██╔══██╗██║╚══███╔╝██╔══██╗████╗  ██║     ██║   ██║██╔══██╗╚██╗██╔╝
# █████╗  ███████║██║  ███╔╝ ███████║██╔██╗ ██║     ██║   ██║██████╔╝ ╚███╔╝
# ██╔══╝  ██╔══██║██║ ███╔╝  ██╔══██║██║╚██╗██║     ██║   ██║██╔══██╗ ██╔██╗
# ██║     ██║  ██║██║███████╗██║  ██║██║ ╚████║     ╚██████╔╝██████╔╝██╔╝ ██╗
# ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝      ╚═════╝ ╚═════╝ ╚═╝  ╚═╝
#
# Created by: Faizan Ahmad Khichi

import os
import sys
import json
import requests
import wikipedia
import base64
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm

# --- 🔧 Core API Configuration ---
API_URL = "https://all-in-one.jokerkeep057.workers.dev/"
API_KEY = "FZN-PROJ-A7B3C9-XYZ-ULTRA-SECURE-2025"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

# --- 📂 File & Directory Management ---
def setup_environment():
    """Checks for Termux, sets up working directory in shared storage."""
    base_dir = os.getenv("HOME")
    if 'com.termux' in base_dir:
        # We are in Termux, let's move to a user-accessible directory
        storage_dir = os.path.join(base_dir, "storage", "shared", "FaizanResearchTool")
        if not os.path.exists(storage_dir):
            try:
                os.makedirs(storage_dir)
            except OSError as e:
                console.print(f"[bold red]Error:[/bold red] Could not create directory in shared storage.")
                console.print(f"Please run [bold]'termux-setup-storage'[/bold] and grant permission.")
                sys.exit(1)
        os.chdir(storage_dir)
        return True
    return False

console = Console()
IS_TERMUX = setup_environment()


# --- 📦 Global Variables & Setup ---
NOTES_FILE = "research_notes.txt"
CODE_DIR = "generated_code"
IMAGE_FILE = os.path.join(os.getenv("HOME"), "storage/shared/generated_image.png") # Absolute path
AUDIO_FILE = os.path.join(os.getenv("HOME"), "storage/shared/generated_audio.mp3") # Absolute path
BRANDING_HEADER = "--- Tool by FAIZAN AHMAD KHICHI ---"
BRANDING_FOOTER = "--- Join my WhatsApp Channel: https://whatsapp.com/channel/0029Vb2y2umF6sn16F6Zm20k ---"


# --- 🎨 UI Helper Functions ---
def print_header():
    """Prints the main header of the tool."""
    header_panel = Panel(
        "[bold cyan]Research & Knowledge Assistant[/bold cyan]\n[dim]A powerful AI tool for your terminal[/dim]",
        title="[bold magenta]Tool by FAIZAN AHMAD KHICHI[/bold magenta]",
        border_style="magenta"
    )
    console.print(header_panel)

def print_footer():
    """Prints the branding footer."""
    console.print(f"\n[dim cyan]🔹 {BRANDING_HEADER} 🔹[/dim cyan]")
    console.print(f"[dim yellow]🔹 Join for Updates: https://whatsapp.com/channel/0029Vb2y2umF6sn16F6Zm20k 🔹[/dim yellow]")


def print_menu():
    """Displays the main menu options."""
    menu_text = """
1. [bold green]📚 Research Topic[/bold green]
2. [bold cyan]💬 AI Chat[/bold cyan]
3. [bold yellow]💻 Code Generation[/bold yellow]
4. [bold blue]🎨 Image Generation[/bold blue]
5. [bold red]🔊 Text-to-Voice[/bold red]
6. [bold]🚪 Exit[/bold]
    """
    console.print(Panel(menu_text, title="[bold]Main Menu[/bold]", border_style="bold blue"))

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


# --- 🌐 Core API & Network Functions ---
def call_api(payload: dict, spinner_text: str = "Contacting AI..."):
    """
    Handles all POST requests to the API with a rich status animation.
    """
    try:
        with console.status(f"[bold green]{spinner_text}[/bold green]", spinner="dots8Bit") as status:
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=240)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")
            status.update("[bold green]Processing response...[/bold green]")
            if "application/json" in content_type:
                return response.json()
            elif "audio/" in content_type or "image/" in content_type:
                return response.content
            else:
                console.print(f"[bold red]Error: Unexpected content type received: {content_type}[/bold red]")
                return None

    except requests.exceptions.Timeout:
        console.print(Panel("[bold red]API Error:[/bold red] The request timed out. The server might be busy. Please try again later.", title="[bold red]Timeout[/bold red]"))
        return None
    except requests.exceptions.RequestException as e:
        console.print(Panel(f"[bold red]Network Error:[/bold red] Could not connect to the API.\nDetails: {e}", title="[bold red]Error[/bold red]"))
        return None


# --- 📝 Feature Implementations ---

def run_research_mode():
    """Handles the entire research workflow."""
    console.print(Panel("Enter a topic to research (e.g., 'Quantum Computing').", title="[bold green]📚 Research Mode[/bold green]"))
    topic = Prompt.ask("[bold]Topic[/bold]")

    wiki_summary, ddg_answer = "", ""
    with console.status("[bold green]Gathering information...[/bold green]", spinner="earth"):
        try:
            wiki_summary = wikipedia.summary(topic, sentences=5, auto_suggest=True, redirect=True)
        except Exception:
            wiki_summary = f"Could not find a clear Wikipedia page for '{topic}'."
        try:
            ddg_url = f"https://api.duckduckgo.com/?q={topic}&format=json"
            data = requests.get(ddg_url).json()
            ddg_answer = data.get("AbstractText", "No quick answer found.")
            if not ddg_answer: ddg_answer = "No quick answer found on DuckDuckGo."
        except Exception:
            ddg_answer = "Failed to fetch from DuckDuckGo."

    if wiki_summary or ddg_answer:
        prompt = f"Summarize and analyze the following research:\n\nWikipedia: {wiki_summary}\n\nDuckDuckGo: {ddg_answer}"
        payload = {"mode": "chat", "provider": "openai-gpt4o", "prompt": prompt}
        api_response = call_api(payload, spinner_text="AI is analyzing the research...")
        ai_summary = api_response.get("response", "AI analysis failed.") if api_response else "API call failed."

        console.rule(f"[bold]Research Results for: {topic}[/bold]")
        console.print(Panel(wiki_summary, title="📚 Wikipedia", border_style="green"))
        console.print(Panel(ddg_answer, title="🌐 DuckDuckGo", border_style="cyan"))
        console.print(Panel(Markdown(ai_summary), title="🤖 AI Summary & Analysis", border_style="magenta"))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(NOTES_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n\n{'='*50}\n{BRANDING_HEADER}\nResearch Topic: {topic} (at {timestamp})\n{'='*50}\n\n")
            f.write(f"--- 📚 Wikipedia ---\n{wiki_summary}\n\n--- 🌐 DuckDuckGo ---\n{ddg_answer}\n\n--- 🤖 AI Summary & Analysis ---\n{ai_summary}\n\n{BRANDING_FOOTER}\n")
        console.print(f"\n[bold green]✔ Results appended to [underline]{os.path.abspath(NOTES_FILE)}[/underline][/bold green]")

def run_chat_mode():
    """Initiates a continuous chat session with the AI."""
    console.print(Panel("You are now chatting with the AI. Type [bold]'exit'[/bold] or [bold]'quit'[/bold] to end.", title="[bold cyan]💬 AI Chat Mode[/bold cyan]"))
    while True:
        prompt = Prompt.ask("[bold]You[/bold]")
        if prompt.lower() in ["exit", "quit"]:
            break
        payload = {"mode": "chat", "provider": "openai-gpt4o", "prompt": prompt}
        response = call_api(payload)
        if response and "response" in response:
            console.print(Panel(Markdown(response["response"]), title="[bold]AI[/bold]", border_style="cyan"))
        else:
            console.print("[bold red]Error: Could not get a response.[/bold red]")

def run_code_mode():
    """Generates code based on a user's request."""
    console.print(Panel("Describe the code you want (e.g., 'a Python function for bubble sort').", title="[bold yellow]💻 Code Generation[/bold yellow]"))
    prompt = Prompt.ask("[bold]Request[/bold]")
    payload = {"mode": "code", "prompt": prompt}
    response = call_api(payload, spinner_text="Generating code...")

    if response and "response" in response:
        code = response["response"].strip()
        if code.startswith("```") and code.endswith("```"):
            code = '\n'.join(code.split('\n')[1:-1])

        console.print(Panel(Syntax(code, "python", theme="monokai", line_numbers=True), title="Generated Code"))

        if Confirm.ask("\n[bold]Do you want to save this code?[/bold]"):
            os.makedirs(CODE_DIR, exist_ok=True)
            filename = Prompt.ask("[bold]Enter filename[/bold]", default="script.py")
            filepath = os.path.join(CODE_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# {BRANDING_HEADER}\n# Code generated for prompt: {prompt}\n\n{code}\n\n# {BRANDING_FOOTER}\n")
            console.print(f"[bold green]✔ Code saved to [underline]{os.path.abspath(filepath)}[/underline][/bold green]")

def run_image_mode():
    """Generates an image from a text prompt."""
    console.print(Panel("Describe the image you want to create.", title="[bold blue]🎨 Image Generation[/bold blue]"))
    prompt = Prompt.ask("[bold]Description[/bold]")
    payload = {"mode": "image", "provider": "openai", "prompt": prompt, "width": 1024, "height": 1024}
    response_data = call_api(payload, spinner_text="Creating your masterpiece...")

    if response_data and isinstance(response_data, dict) and "image_base64" in response_data:
        try:
            with console.status("[bold green]Saving image...[/bold green]", spinner="bouncingBar"):
                image_data = base64.b64decode(response_data["image_base64"])
                with open(IMAGE_FILE, "wb") as f:
                    f.write(image_data)
            console.print(f"\n[bold green]✅ Image saved successfully![/bold green]")
            console.print(f"   [dim]Location: {IMAGE_FILE}[/dim]")
        except Exception as e:
            console.print(f"[bold red]Error saving image: {e}[/bold red]")
    else:
        console.print("[bold red]Error: Failed to generate image.[/bold red]")

def run_voice_mode():
    """Converts text to speech."""
    console.print(Panel("Enter the text to convert to speech.", title="[bold red]🔊 Text-to-Voice[/bold red]"))
    prompt = Prompt.ask("[bold]Text[/bold]")
    payload = {"mode": "voice", "voice": "nova", "prompt": prompt}
    audio_data = call_api(payload, spinner_text="Generating audio...")

    if audio_data and isinstance(audio_data, bytes):
        try:
            with open(AUDIO_FILE, "wb") as f:
                f.write(audio_data)
            console.print(f"\n[bold green]✅ Audio saved as [underline]{os.path.basename(AUDIO_FILE)}[/underline][/bold green]")
            console.print(f"   [dim]Location: {AUDIO_FILE}[/dim]")
        except Exception as e:
            console.print(f"[bold red]Error saving audio file: {e}[/bold red]")
    else:
        console.print("[bold red]Error: Failed to generate audio.[/bold red]")

# --- 🚀 Main Application Logic ---

def main():
    """The main function to run the application loop."""
    while True:
        clear_screen()
        print_header()
        if IS_TERMUX:
            console.print(f"[dim]Working directory: {os.getcwd()}[/dim]")
        print_menu()
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6"], default="1")

        clear_screen()
        print_header()

        actions = {
            '1': run_research_mode,
            '2': run_chat_mode,
            '3': run_code_mode,
            '4': run_image_mode,
            '5': run_voice_mode,
        }
        
        if choice in actions:
            actions[choice]()
        elif choice == '6':
            console.print("[bold]Thank you for using the Faizan Research Tool. Goodbye![/bold]")
            sys.exit()

        print_footer()
        Prompt.ask("\n[dim]Press Enter to return to the menu...[/dim]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_footer()
        console.print("\n[bold red]Program interrupted. Exiting.[/bold red]")
        sys.exit()