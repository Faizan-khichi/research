# Faizan's Research & AI Assistant (for Termux)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Termux](https://img.shields.io/badge/Termux-000000?style=for-the-badge&logo=termux&logoColor=white)
![API](https://img.shields.io/badge/API-Cloudflare-orange?style=for-the-badge)

A powerful, command-line Research & Knowledge Assistant built to run seamlessly in Termux on Android. This tool leverages a custom Cloudflare Worker API to provide a suite of AI-powered features right from your terminal.

**Created by: Faizan Ahmad Khichi**
**WhatsApp Channel:** [Join for Updates](https://whatsapp.com/channel/0029Vb2y2umF6sn16F6Zm20k)

---

### ✨ Features

-   **📚 Research Mode:** Enter a topic to get a consolidated report from Wikipedia, DuckDuckGo, and a powerful AI analysis.
-   **💬 AI Chat Mode:** Have an interactive, continuous conversation with a GPT-4o powered chatbot.
-   **💻 Code Generation Mode:** Describe a programming task and receive ready-to-use code, which can be saved directly to a file.
-   **🎨 Image Generation Mode:** Create stunning 1024x1024 images from a simple text description.
-   **🔊 Text-to-Voice Mode:** Convert any text into high-quality spoken audio (`.mp3`) using AI voices.

### 🔧 Installation on Termux

Follow these steps to get the tool up and running on your Android device via Termux.

1.  **Update Termux & Install Core Packages:**
    ```bash
    pkg update -y && pkg upgrade -y
    pkg install python git -y
    ```

2.  **Grant Storage Access:** This is crucial for saving images, audio, and notes where you can easily find them.
    ```bash
    termux-setup-storage
    ```

3.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/Termux-AI-Assistant.git
    ```
    *(Replace `YOUR_USERNAME` with your actual GitHub username)*

4.  **Navigate into the Project Directory:**
    ```bash
    cd Termux-AI-Assistant
    ```

5.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 🚀 Quick Launch Setup (Recommended)

To run the tool from anywhere in Termux with a simple command (`research`), create a permanent alias.

1.  **Run this command in Termux:**
    ```bash
    echo "alias research='python ~/Termux-AI-Assistant/research_tool.py'" >> ~/.bashrc
    ```

2.  **Activate the alias:** Close and reopen Termux, or run:
    ```bash
    source ~/.bashrc
    ```

3.  **Done!** Now you can simply type `research` and press Enter to start the assistant.

### ⚙️ Usage

After launching the tool with the `research` command, you will be greeted with the main menu. Simply type the number corresponding to your desired feature and press Enter.

All generated files (notes, code, images, audio) will be saved in a folder named `FaizanResearchTool` in your phone's main internal storage, making them easy to access with any file manager.