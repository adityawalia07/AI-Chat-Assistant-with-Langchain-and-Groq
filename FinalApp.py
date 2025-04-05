import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
import uuid
import time

# Load environment variables
load_dotenv()

# Langsmith Tracking
if os.getenv("LANGCHAIN_API_KEY"):
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "Enhanced Q&A Chatbot With ChatGroq"

# Page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Model descriptions
MODEL_INFO = {
    "Gemma2-9b-It": "Google's Gemma 2B - Lightweight model good for simple tasks",
    "llama-3.1-8b-instant": "Meta's LLaMA 3.1 - Fast and efficient for interactive chat",
    "qwen-2.5-32b": "Alibaba's Qwen 2.5 32B - Powerful model for complex responses"
}

# Prompt templates
PROMPT_TEMPLATES = {
    "Default": "You are a helpful assistant. Please respond to the user queries.\n\nQuestion: {question}",
    "Professional": "You are a professional consultant with expertise in various fields. Please provide detailed, well-structured, and accurate information.\n\nQuestion: {question}",
    "Creative": "You are a creative assistant with a flair for imaginative responses. Feel free to think outside the box while being helpful.\n\nQuestion: {question}",
    "Concise": "You are a concise assistant. Provide brief, clear answers without unnecessary details.\n\nQuestion: {question}"
}

# Setup session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

# CSS for chat styling and dark mode
st.markdown("""
<style>
:root {
    --text-color: #FFFFFF;
    --background-color: #0E1117;
    --secondary-background: #262730;
    --accent-color: #4B56D2;
    --border-color: #555;
    --user-message-bg: #2E3856;
    --assistant-message-bg: #3A3F51;
    --model-info-bg: #3A3F51;
    --model-info-border: #4B56D2;
}

.main {
    background-color: var(--background-color);
    color: var(--text-color);
}

.stTextInput > div > div > input {
    padding: 12px 15px;
    border-radius: 15px;
    border: 1px solid var(--border-color);
    background-color: var(--secondary-background);
    color: var(--text-color);
}

.chat-message {
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
    display: flex;
    align-items: flex-start;
    color: var(--text-color);
}
.chat-message.user {
    background-color: var(--user-message-bg);
    border-left: 5px solid var(--accent-color);
}
.chat-message.assistant {
    background-color: var(--assistant-message-bg);
    border-left: 5px solid #718096;
}
.chat-message .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}
.chat-message .message {
    flex-grow: 1;
}

.stButton button {
    border-radius: 15px;
    padding: 5px 15px;
    font-weight: 500;
    background-color: var(--secondary-background);
    color: var(--text-color);
    border: 1px solid var(--border-color);
}
.stButton button:hover {
    border-color: var(--accent-color);
}
.sidebar .stButton button {
    width: 100%;
}

.model-info {
    padding: 12px;
    background-color: var(--model-info-bg);
    border-radius: 10px;
    margin-top: 15px;
    border: 1px solid var(--model-info-border);
    color: var(--text-color);
}
.model-name {
    color: var(--accent-color);
    font-weight: bold;
    margin-bottom: 5px;
}

footer {
    text-align: center;
    padding: 10px;
    font-size: 12px;
    color: #999;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# Display chat message
def display_chat_message(message, is_user):
    avatar = "👤" if is_user else "🤖"
    role = "user" if is_user else "assistant"
    st.markdown(f"""
    <div class="chat-message {role}">
        <div class="avatar">{avatar}</div>
        <div class="message">{message}</div>
    </div>
    """, unsafe_allow_html=True)

# Validate and sanitize user input
def validate_input(text):
    # Basic validation - check if input is not just whitespace
    if not text or text.strip() == "":
        return False, "Please enter a valid question."
    
    # Check for reasonable length
    if len(text) > 5000:  # Set a reasonable maximum
        return False, "Your question is too long. Please keep it under 5000 characters."
    
    return True, text.strip()

# Generate response from Groq
def generate_response(question, model, temperature, max_tokens, prompt_style):
    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            return "Error: GROQ_API_KEY not found in environment variables. Please configure your API key.", 0
            
        prompt_template = PROMPT_TEMPLATES[prompt_style]
        prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_template.split("\n\nQuestion:")[0]),
            ("user", f"Question: {question}")
        ])
        llm = ChatGroq(model=model, api_key=groq_api_key, temperature=temperature, max_tokens=max_tokens)
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        start = time.time()
        answer = chain.invoke({'question': question})
        end = time.time()
        return answer, round(end - start, 2)
    except Exception as e:
        # Log the actual error for debugging
        st.error(f"An error occurred: {str(e)}")
        # Return a user-friendly message
        return "I'm sorry, I couldn't process your request. Please try again later.", 0

# Process user message and get response
def process_user_message(user_question, model, temperature, max_tokens, prompt_style):
    st.session_state.messages.append({"role": "user", "content": user_question})
    
    response, duration = generate_response(user_question, model, temperature, max_tokens, prompt_style)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    return response, duration

# Sidebar Settings
with st.sidebar:
    st.title("⚙️ Settings")

    model = st.radio("Select Model:", list(MODEL_INFO.keys()))
    st.markdown(f"""
    <div class="model-info">
        <div class="model-name">{model}</div>
        <div>{MODEL_INFO[model]}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Advanced Settings"):
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
        max_tokens = st.slider("Max Tokens", 50, 1000, 250, 50)
        prompt_style = st.selectbox("Prompt Style", list(PROMPT_TEMPLATES.keys()))

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_id = str(uuid.uuid4())
        st.rerun()

# Title and subtitle
st.title("🤖 AI Assistant")
st.subheader("Your personal AI chatbot powered by Groq")

# Display past messages
for msg in st.session_state.messages:
    display_chat_message(msg["content"], msg["role"] == "user")

# User input using chat_input
if user_input := st.chat_input("Type your question here..."):
    # Validate input
    is_valid, validated_input = validate_input(user_input)
    
    if not is_valid:
        st.error(validated_input)  # Show error message
    else:
        # Display user message
        display_chat_message(validated_input, True)
        
        # Get model response
        response, time_taken = process_user_message(
            validated_input,
            model,
            temperature,
            max_tokens,
            prompt_style
        )
        
        # Display assistant response
        display_chat_message(response, False)
        st.caption(f"Response generated in {time_taken} seconds")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"""
<footer>
    <p>Conversation ID: {st.session_state.conversation_id}</p>
    <p>Built with Streamlit, LangChain & ChatGroq</p>
</footer>
""", unsafe_allow_html=True)