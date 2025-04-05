# AI Chat Assistant with Langchain and Groq 🤖

A sleek, customizable AI chatbot built with Streamlit, LangChain, and Groq LLM API. This application allows users to interact with various language models through an intuitive chat interface.

## ✨ Features

- **Multiple LLM Options**: Choose between different models:
  - Gemma2-9b-It: Google's lightweight model for simple tasks
  - llama-3.1-8b-instant: Meta's fast and efficient model for interactive chat
  - qwen-2.5-32b: Alibaba's powerful model for complex responses

- **Customizable Settings**:
  - Adjust temperature to control response randomness
  - Set max tokens for response length
  - Select from various prompt styles: Default, Professional, Creative, and Concise

- **Modern UI**:
  - Dark mode interface
  - Clean chat message styling
  - Responsive design

- **Additional Features**:
  - LangSmith integration for tracking and debugging
  - Conversation session management
  - Response timing information

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Groq API key
- LangChain API key (optional, for tracking)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI-Chat-Assistant-with-Langchain-and-Groq.git
cd ai-assistant-chatbot
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your API keys:
```
GROQ_API_KEY=your_groq_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here
```

### Running the Application

```bash
streamlit run app.py
```

Navigate to the URL provided by Streamlit (typically http://localhost:8501) to interact with the chatbot.

## 📋 Usage Guide

1. Select your preferred model from the sidebar
2. Customize advanced settings if needed
3. Type your question in the input field and press Enter
4. View the AI's response in the chat window
5. Use the "Clear Chat" button to start a new conversation

## 🔧 Customization

### Adding New Models

To add new LLM models, update the `MODEL_INFO` dictionary in the script:

```python
MODEL_INFO = {
    "new-model-name": "Description of the new model",
    # ... existing models
}
```

### Creating Custom Prompt Templates

Add new prompt styles by updating the `PROMPT_TEMPLATES` dictionary:

```python
PROMPT_TEMPLATES = {
    "Technical": "You are a technical assistant specialized in explaining complex concepts clearly...",
    # ... existing templates
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Future Enhancements

- File upload support for document Q&A
- Voice input/output capabilities
- Multi-modal model support
- Chat history export feature
- Custom styling options

---

Built with ❤️ using Streamlit, LangChain and ChatGroq
