import re
import base64
import logging
import streamlit as st
from ollama import chat
import requests

# Configuration
OLLAMA_MODEL = "gemma3:270m"
OLLAMA_API_URL = "http://localhost:11434"
OLLAMA_API_TIMEOUT = 5
STREAM_PROCESSING_TIMEOUT = 30
CHAT_OPERATION_TIMEOUT = 60
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = 'app.log'
STREAMLIT_PAGE_TITLE = "Ollama Gemma3 Chat"
STREAMLIT_LAYOUT = "centered"
SYSTEM_MESSAGE = "You are a helpful assistant."
CHUNK_LOG_INTERVAL = 10
MAX_LOG_LENGTH = 50

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE)
    ]
)
logger = logging.getLogger(__name__)

# Set Streamlit page configuration (optional)
st.set_page_config(page_title=STREAMLIT_PAGE_TITLE, layout=STREAMLIT_LAYOUT)
logger.info("Streamlit page configured")

def check_ollama_running():
    """Check if Ollama is running."""
    try:
        logger.info("Checking if Ollama is running")
        response = requests.get(f"{OLLAMA_API_URL}/api/tags", timeout=OLLAMA_API_TIMEOUT)
        if response.status_code == 200:
            logger.info("Ollama is running")
            return True
        else:
            logger.error(f"Ollama returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        logger.error("Ollama is not running or not accessible")
        return False
    except Exception as e:
        logger.error(f"Error checking if Ollama is running: {str(e)}")
        return False

def check_ollama_model():
    """Check if the required Ollama model is available."""
    try:
        # First check if Ollama is running
        if not check_ollama_running():
            return False
            
        logger.info(f"Checking if Ollama model '{OLLAMA_MODEL}' is available")
        response = requests.get(f"{OLLAMA_API_URL}/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model.get("name", "") for model in models]
            logger.info(f"Available models: {model_names}")
            
            if OLLAMA_MODEL in model_names:
                logger.info(f"Model '{OLLAMA_MODEL}' is available")
                return True
            else:
                logger.warning(f"Model '{OLLAMA_MODEL}' not found in available models")
                return False
        else:
            logger.error(f"Failed to get models from Ollama: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error checking Ollama model: {str(e)}")
        return False

def process_thinking_stream(stream):
    """Process streaming response from Ollama."""
    logger.info("Starting to process stream")
    response_content = ""
    
    try:
        with st.status("Generating response...", expanded=True) as status:
            logger.info("Status widget created for response generation")
            chunk_count = 0
            
            # Add timeout and error handling for the stream
            import time
            start_time = time.time()
            timeout = STREAM_PROCESSING_TIMEOUT
            
            for chunk in stream:
                chunk_count += 1
                current_time = time.time()
                
                # Check for timeout
                if current_time - start_time > timeout:
                    logger.error(f"Stream processing timed out after {timeout} seconds")
                    status.update(label="Timeout occurred!", state="error", expanded=False)
                    return response_content
                
                logger.debug(f"Processing chunk {chunk_count}: {chunk}")
                
                # Handle response content
                if chunk["message"].get("content"):
                    response_content += chunk["message"]["content"]
                    logger.debug(f"Added response content: {chunk['message']['content'][:MAX_LOG_LENGTH]}...")
                
                # Log progress every N chunks
                if chunk_count % CHUNK_LOG_INTERVAL == 0:
                    logger.info(f"Processed {chunk_count} chunks so far...")
            
            logger.info(f"Processed {chunk_count} chunks total")
            logger.info(f"Final response content length: {len(response_content)}")
            
            # Update status when done
            status.update(label="Response complete!", state="complete", expanded=False)
            logger.info("Status updated to complete")
    
    except Exception as e:
        logger.error(f"Error in process_thinking_stream: {str(e)}", exc_info=True)
        st.error(f"Error processing stream: {str(e)}")
        return response_content
    
    return response_content

def display_message(message):
    """Display a single message in the chat interface."""
    logger.info(f"Displaying message from role: {message['role']}")
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        if role == "assistant":
            logger.debug(f"Displaying assistant message")
            display_assistant_message(message["content"])
        else:
            logger.debug(f"Displaying user message: {message['content'][:MAX_LOG_LENGTH]}...")
            st.markdown(message["content"])

def display_assistant_message(content):
    """Display assistant message."""
    logger.info("Displaying assistant message")
    
    # Display response content in the main chat area
    if content:
        logger.debug(f"Displaying response content: {content[:MAX_LOG_LENGTH]}...")
        st.markdown(content)
    else:
        logger.warning("No content to display for assistant message")

def display_chat_history():
    """Display all previous messages in the chat history."""
    logger.info(f"Displaying chat history with {len(st.session_state['messages'])} messages")
    for i, message in enumerate(st.session_state["messages"]):
        if message["role"] != "system":  # Skip system messages
            logger.debug(f"Displaying message {i+1}: {message['role']}")
            display_message(message)

@st.cache_resource
def get_chat_model():
    """Get a cached instance of the chat model."""
    logger.info("Creating cached chat model instance")
    try:
        return lambda messages: chat(
            model=OLLAMA_MODEL,
            messages=messages,
            stream=True,
        )
    except Exception as e:
        logger.error(f"Error creating chat model: {str(e)}", exc_info=True)
        raise e

def handle_user_input():
    """Handle new user input and generate assistant response."""
    logger.info("Checking for user input")
    if user_input := st.chat_input("Type your message here..."):
        logger.info(f"Received user input: {user_input[:MAX_LOG_LENGTH]}...")
        st.session_state["messages"].append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            try:
                # Check if Ollama model is available
                if not check_ollama_model():
                    error_msg = f"Ollama model '{OLLAMA_MODEL}' is not available. Please ensure Ollama is running and the model is installed."
                    logger.error(error_msg)
                    st.error(error_msg)
                    # Remove the user message from session state
                    if st.session_state["messages"] and st.session_state["messages"][-1]["role"] == "user":
                        st.session_state["messages"].pop()
                    return
                
                logger.info("Getting chat model for response generation")
                chat_model = get_chat_model()
                logger.info("Starting chat stream")
                
                # Add timeout for the entire chat operation
                import time
                start_time = time.time()
                timeout = CHAT_OPERATION_TIMEOUT
                
                stream = chat_model(st.session_state["messages"])
                logger.info("Chat stream created successfully")
                
                logger.info("Processing stream")
                response_content = process_thinking_stream(stream)
                
                # Check if we got any response
                if not response_content:
                    logger.warning("No response content received from model")
                    st.warning("No response received from the model. Please try again.")
                    return
                
                # Display response using the same function as historical messages
                display_assistant_message(response_content)
                
                # Save the complete response
                st.session_state["messages"].append(
                    {"role": "assistant", "content": response_content}
                )
                logger.info("Response saved to session state")
                
            except Exception as e:
                logger.error(f"Error in handle_user_input: {str(e)}", exc_info=True)
                st.error(f"Error generating response: {str(e)}")
                # Remove the user message from session state if there was an error
                if st.session_state["messages"] and st.session_state["messages"][-1]["role"] == "user":
                    st.session_state["messages"].pop()
    else:
        logger.debug("No user input received")

def main():
    """Main function to handle the chat interface and streaming responses."""
    logger.info("Starting main function")
    
    # Header styling configuration (local to this function)
    header_logo_width = 40
    header_logo_margin = "10px"
    
    try:
        # Load and encode logos
        logger.info("Loading and encoding logos")
        gemma_logo = base64.b64encode(open("assets/gemma.png", "rb").read()).decode()
        logger.info("Google Gemma logo loaded successfully")
        ollama_logo = base64.b64encode(open("assets/ollama.png", "rb").read()).decode()
        logger.info("Ollama logo loaded successfully")
        
        # Add logo to top right corner using custom CSS
        logger.info("Adding top-right logo with CSS")
        st.markdown(f"""
        <style>
        .top-right-logo {{
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 1000;
            padding: 8px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }}
        .top-right-logo:hover {{
            background: rgba(255, 255, 255, 1);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        </style>
        <div class="top-right-logo">
            <img src="data:image/png;base64,{ollama_logo}" width="60" alt="Ollama Logo">
        </div>
        """, unsafe_allow_html=True)
        
        # Check status for sidebar display
        logger.info("Checking Ollama status for sidebar display")
        ollama_running = check_ollama_running()
        model_available = check_ollama_model()
        
        logger.info(f"Ollama running: {ollama_running}")
        logger.info(f"Model available: {model_available}")
        
        # Add sidebar with status information (open by default)
        st.sidebar.header("🔧 System Status")
        
        if ollama_running:
            st.sidebar.success("✅ Ollama is running")
        else:
            st.sidebar.error("❌ Ollama is not running")
            
        if model_available:
            st.sidebar.success(f"✅ Model {OLLAMA_MODEL} is available")
        else:
            st.sidebar.error(f"❌ Model {OLLAMA_MODEL} is not available")
        
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h2 style='margin-bottom: 0.5rem;'>
                <img src="data:image/png;base64,{gemma_logo}" width="{header_logo_width}" style="vertical-align: middle; margin-right: {header_logo_margin};">
                Google Gemma3 270M
            </h2>
            <h6 style='color: #666; margin-top: 0;'>Streaming Chat Interface 💬</h6>
        </div>
        """, unsafe_allow_html=True)
        
        logger.info("Displaying chat history")
        display_chat_history()
        logger.info("Handling user input")
        handle_user_input()
        
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    logger.info("Application starting")
    # Initialize session state
    if "messages" not in st.session_state:
        logger.info("Initializing session state with system message")
        st.session_state["messages"] = [
            {"role": "system", "content": SYSTEM_MESSAGE}
        ]
    else:
        logger.info(f"Session state already exists with {len(st.session_state['messages'])} messages")
    
    logger.info("Calling main function")
    main()
    logger.info("Application finished")