# research_tool.py v2.1
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
import re
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
BASE_STORAGE_DIR = os.path.join(os.getenv("HOME"), "storage", "shared", "Faizan AI Tool")
NOTES_DIR = os.path.join(BASE_STORAGE_DIR, "Research Notes")
CODE_DIR = os.path.join(BASE_STORAGE_DIR, "Generated Code")
IMAGE_DIR = os.path.join(BASE_STORAGE_DIR, "Generated Images")
AUDIO_DIR = os.path.join(BASE_STORAGE_DIR, "Generated Audio")
CHAT_DIR = os.path.join(BASE_STORAGE_DIR, "AI Chats")

def setup_environment():
    """Creates all necessary directories in shared storage."""
    try:
        for path in [BASE_STORAGE_DIR, NOTES_DIR, CODE_DIR, IMAGE_DIR, AUDIO_DIR, CHAT_DIR]:
            os.makedirs(path, exist_ok=True)
    except OSError:
        console.print("[bold red]Error:[/bold red] Could not create directories in shared storage.")
        console.print("Please run [bold]'termux-setup-storage'[/bold], grant permission, and restart the script.")
        sys.exit(1)

console = Console()
BRANDING_HEADER = "--- Tool by FAIZAN AHMAD KHICHI ---"
BRANDING_FOOTER = "--- Join my WhatsApp Channel: https://whatsapp.com/channel/0029Vb2y2umF6sn16F6Zm20k ---"

# --- 🎨 UI & Helper Functions ---
def print_header():
    header_panel = Panel(
        "[bold cyan]Research & Knowledge Assistant v2.1[/bold cyan]\n[dim]All outputs are saved in your 'Faizan AI Tool' folder.[/dim]",
        title="[bold magenta]Tool by FAIZAN AHMAD KHICHI[/bold magenta]", border_style="magenta"
    )
    console.print(header_panel)

def print_footer():
    console.print(f"\n[dim cyan]🔹 {BRANDING_HEADER} 🔹[/dim cyan]")
    console.print(f"[dim yellow]🔹 Join for Updates: https://whatsapp.com/channel/0029Vb2y2umF6sn16F6Zm20k 🔹[/dim yellow]")

def print_menu():
    menu_text = "1. [bold green]📚 Research Topic[/bold green]\n2. [bold cyan]💬 AI Chat[/bold cyan]\n3. [bold yellow]💻 Code Generation[/bold yellow]\n4. [bold blue]🎨 Image Generation[/bold blue]\n5. [bold red]🔊 Text-to-Voice[/bold red]\n6. [bold]🚪 Exit[/bold]"
    console.print(Panel(menu_text, title="[bold]Main Menu[/bold]", border_style="bold blue"))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_safe_filename(prompt_text):
    """Creates a safe, short filename from a prompt."""
    text = re.sub(r'[^\w\s-]', '', prompt_text).strip().lower()
    return re.sub(r'[-\s]+', '_', text)[:40] # Limit length for file systems

# --- 🌐 Core API & Network Functions ---
def call_api(payload: dict, spinner_text: str = "Contacting AI..."):
    try:
        with console.status(f"[bold green]{spinner_text}[/bold green]", spinner="dots8Bit"):
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=240)
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return response.json()
            elif "audio/" in content_type:
                return response.content
            else: # Fallback for unexpected types
                return response.text
    except requests.exceptions.Timeout:
        console.print(Panel("[bold red]API Error:[/bold red] The request timed out. Please try again.", title="[bold red]Timeout[/bold red]"))
        return None
    except requests.exceptions.RequestException as e:
        console.print(Panel(f"[bold red]Network Error:[/bold red] Could not connect.\nDetails: {e}", title="[bold red]Error[/bold red]"))
        return None

# --- 📝 Feature Implementations ---

def run_research_mode():
    console.print(Panel("Enter a topic to research (e.g., 'Quantum Computing').", title="[bold green]📚 Research Mode[/bold green]"))
    topic = Prompt.ask("[bold]Topic[/bold]")
    wiki_summary, ddg_answer = "", ""
    
    with console.status("[bold green]Gathering information...[/bold green]", spinner="earth"):
        wikipedia.set_lang("en")
        
        # --- Wikipedia Search (Improved Precision) ---
        try:
            # 1. Try for an exact match (auto_suggest=False, redirect=False)
            wiki_summary = wikipedia.summary(topic, sentences=5, auto_suggest=False, redirect=False)
        except wikipedia.exceptions.PageError:
            # 2. If no exact page, try a broader search for page titles
            search_results = wikipedia.search(topic, results=1)
            if search_results:
                try:
                    # Summarize the top search result
                    found_page_title = search_results[0]
                    wiki_summary = wikipedia.summary(found_page_title, sentences=5, auto_suggest=False, redirect=False)
                    wiki_summary = f"[b]Found Wikipedia page for '{topic}':[/b] [italic]{found_page_title}[/italic]\n\n{wiki_summary}"
                except Exception as e:
                    wiki_summary = f"[red]Could not summarize Wikipedia page '{found_page_title}'.[/red] Error: {e}"
            else:
                wiki_summary = f"[red]No direct Wikipedia page or relevant search results found for '{topic}'.[/red]"
        except wikipedia.exceptions.DisambiguationError as e:
            wiki_summary = f"[yellow]'{topic}' is ambiguous on Wikipedia.[/yellow] Possible options include: {', '.join(e.options[:3])}. Please be more specific."
        except requests.exceptions.Timeout:
            wiki_summary = "[red]Wikipedia API timed out.[/red] Please try again."
        except Exception as e:
            wiki_summary = f"[red]An unexpected error occurred with Wikipedia:[/red] {e}"

        # --- DuckDuckGo Quick Answer ---
        try:
            ddg_url = f"https://api.duckduckgo.com/?q={topic}&format=json"
            data = requests.get(ddg_url, timeout=10).json()
            ddg_answer = data.get("AbstractText") or "No quick answer found on DuckDuckGo."
        except requests.exceptions.Timeout:
            ddg_answer = "[red]DuckDuckGo API timed out.[/red] Please try again."
        except Exception as e:
            ddg_answer = f"[red]Failed to fetch from DuckDuckGo:[/red] {e}"

    # --- AI Summary & Analysis ---
    ai_prompt_content = f"Wikipedia: {wiki_summary}\n\nDuckDuckGo: {ddg_answer}"
    prompt_for_ai = f"You are a research analyst. Summarize and provide a brief analysis of the following information. Focus on the key points, potential implications, and any interesting connections. If some sources indicate no direct information, acknowledge that and base your analysis on what is available.\n\n---\n{ai_prompt_content}\n---"
    
    payload = {"mode": "chat", "provider": "openai-gpt4o", "prompt": prompt_for_ai}
    api_response = call_api(payload, spinner_text="AI is analyzing the research...")
    
    ai_summary = "AI analysis failed."
    if api_response and api_response.get("success"):
        ai_summary = api_response.get("data", {}).get("response", ai_summary)
    else:
        ai_summary = "[red]AI analysis could not be generated due to an API error.[/red]"


    console.rule(f"[bold]Research Results for: {topic}[/bold]")
    console.print(Panel(Markdown(wiki_summary), title="📚 Wikipedia", border_style="green"))
    console.print(Panel(ddg_answer, title="🌐 DuckDuckGo", border_style="cyan"))
    console.print(Panel(Markdown(ai_summary), title="🤖 AI Summary & Analysis", border_style="magenta"))

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notes_filepath = os.path.join(NOTES_DIR, "research_log.txt")
    with open(notes_filepath, "a", encoding="utf-8") as f:
        f.write(f"\n\n{'='*50}\n{BRANDING_HEADER}\nResearch Topic: {topic} (at {timestamp})\n{'='*50}\n\n")
        f.write(f"--- 📚 Wikipedia ---\n{wiki_summary}\n\n--- 🌐 DuckDuckGo ---\n{ddg_answer}\n\n--- 🤖 AI Summary & Analysis ---\n{ai_summary}\n\n{BRANDING_FOOTER}\n")
    console.print(f"\n[bold green]✔ Results appended to [underline]{notes_filepath}[/underline][/bold green]")


def run_chat_mode():
    console.print(Panel("Chat with the AI. Type [bold]'exit'[/bold] or [bold]'quit'[/bold] to end and save the conversation.", title="[bold cyan]💬 AI Chat Mode[/bold cyan]"))
    chat_history = []
    while True:
        prompt = Prompt.ask("[bold]You[/bold]")
        if prompt.lower() in ["exit", "quit"]:
            break
        chat_history.append(f"**You:** {prompt}")
        payload = {"mode": "chat", "provider": "openai-gpt4o", "prompt": prompt}
        response = call_api(payload)
        ai_response = "Error: Could not get a response."
        if response and response.get("success"):
            ai_response = response.get("data", {}).get("response", ai_response)
        
        console.print(Panel(Markdown(ai_response), title="[bold]AI[/bold]", border_style="cyan"))
        chat_history.append(f"**AI:**\n{ai_response}\n\n---\n")

    if chat_history:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_{timestamp}.md"
        filepath = os.path.join(CHAT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Chat Session: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(f"{BRANDING_HEADER}\n\n")
            f.write("\n".join(chat_history))
            f.write(f"\n\n{BRANDING_FOOTER}\n")
        console.print(f"\n[bold green]✔ Chat history saved to [underline]{filepath}[/underline][/bold green]")

def run_code_mode():
    console.print(Panel("Describe the code you want (e.g., 'a Python function for bubble sort').", title="[bold yellow]💻 Code Generation[/bold yellow]"))
    prompt = Prompt.ask("[bold]Request[/bold]")
    payload = {"mode": "code", "prompt": prompt}
    response = call_api(payload, spinner_text="Generating code...")

    if response and response.get("success"):
        code = response.get("data", {}).get("response", "# Code generation failed.").strip()
        # Attempt to strip markdown code blocks
        if code.startswith("```") and code.endswith("```"):
            code_lines = code.split('\n')
            # Check if the first line also has a language specifier (e.g., ```python)
            if len(code_lines) > 1 and code_lines[0].strip().lower().startswith('```'):
                code = '\n'.join(code_lines[1:-1])
            else:
                code = '\n'.join(code_lines[1:-1]) # Regular case
        
        console.print(Panel(Syntax(code, "python", theme="monokai", line_numbers=True), title="Generated Code"))

        if Confirm.ask("\n[bold]Do you want to save this code?[/bold]"):
            safe_name = get_safe_filename(prompt)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{safe_name}.py"
            filepath = os.path.join(CODE_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# {BRANDING_HEADER}\n# Code for prompt: {prompt}\n\n{code}\n\n# {BRANDING_FOOTER}\n")
            console.print(f"[bold green]✔ Code saved to [underline]{filepath}[/underline][/bold green]")
    else:
        console.print("[bold red]Error: Could not generate code.[/bold red]")


def run_image_mode():
    console.print(Panel("Describe the image you want to create.", title="[bold blue]🎨 Image Generation[/bold blue]"))
    prompt = Prompt.ask("[bold]Description[/bold]")
    payload = {"mode": "image", "provider": "openai", "prompt": prompt, "width": 1024, "height": 1024}
    api_response = call_api(payload, spinner_text="Creating your masterpiece...")

    if api_response and api_response.get("success"):
        image_url = api_response.get("data", {}).get("url")
        if not image_url:
            console.print("[bold red]Error: API returned success but no image URL was found.[/bold red]")
            return
        
        try:
            with console.status("[bold blue]Downloading image...[/bold blue]", spinner="bouncingBar"):
                image_data = requests.get(image_url, timeout=60).content
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = get_safe_filename(prompt)
            filename = f"{timestamp}_{safe_name}.png"
            filepath = os.path.join(IMAGE_DIR, filename)

            with open(filepath, "wb") as f:
                f.write(image_data)
            
            console.print(f"\n[bold green]✅ Image downloaded and saved successfully![/bold green]")
            console.print(f"   [dim]You can find it in your gallery or at:[/] [underline]{filepath}[/underline]")
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]Error downloading image: {e}[/bold red]")
            console.print(f"[dim]Direct URL: {image_url}[/dim]")
    else:
        console.print("[bold red]Error: Failed to generate image from API.[/bold red]")

def run_voice_mode():
    console.print(Panel("Enter the text to convert to speech.", title="[bold red]🔊 Text-to-Voice[/bold red]"))
    prompt = Prompt.ask("[bold]Text[/bold]")
    payload = {"mode": "voice", "voice": "nova", "prompt": prompt}
    audio_data = call_api(payload, spinner_text="Generating audio...")

    if audio_data and isinstance(audio_data, bytes):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = get_safe_filename(prompt)
            filename = f"{timestamp}_{safe_name}.mp3"
            filepath = os.path.join(AUDIO_DIR, filename)

            with open(filepath, "wb") as f:
                f.write(audio_data)
            console.print(f"\n[bold green]✅ Audio saved successfully![/bold green]")
            console.print(f"   [dim]Listen to it at:[/] [underline]{filepath}[/underline]")
        except Exception as e:
            console.print(f"[bold red]Error saving audio file: {e}[/bold red]")
    else:
        console.print("[bold red]Error: Failed to generate audio data.[/bold red]")

# --- 🚀 Main Application Logic ---
def main():
    setup_environment()
    while True:
        clear_screen()
        print_header()
        print_menu()
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6"], default="1")
        clear_screen()
        print_header()
        
        actions = {'1': run_research_mode, '2': run_chat_mode, '3': run_code_mode, '4': run_image_mode, '5': run_voice_mode}
        
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
