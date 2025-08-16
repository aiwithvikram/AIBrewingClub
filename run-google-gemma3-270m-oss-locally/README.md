# Run Google Gemma 3 (270M) Locally 🚀

Experience the power of Google's Gemma 3 270M model locally - a lightweight yet capable language model that runs efficiently on your own hardware using Ollama.

## ✨ Features

- 🚀 **Ultra-Efficient**: 268.1M parameter model that's incredibly fast and resource-friendly
- 📱 **Low Resource**: Perfect for laptops, desktops, and even some mobile devices
- 🧠 **Smart AI**: Powered by Google's latest Gemma 3 architecture
- ⚡ **Fast Response**: Optimized for quick, helpful interactions
- **Streaming Chat Interface**: Real-time response generation with smooth streaming
- **Chat History**: Full conversation history preserved across sessions
- **Clean Interface**: Professional UI with Google Gemma and Ollama branding
- **Status Monitoring**: Real-time Ollama service and model availability status
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Installation and Setup

### Prerequisites
- Python 3.11 or later
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- [Ollama](https://ollama.com/) installed and running

### 1. Setup Ollama

```bash
# Install Ollama (Linux/macOS)
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# Pull the Gemma 3 model
ollama pull gemma3:270m
```

### 2. Install Dependencies

**Using uv (recommended):**
```bash
uv sync
```

**Using pip:**
```bash
pip install streamlit ollama
```

### 3. Run the App

```bash
uv run streamlit run app.py
# or with pip: streamlit run app.py
```

The app will be available at `http://localhost:8501` (or 8502 if 8501 is busy).

## Usage

1. **Start the App**: Run the Streamlit command above
2. **Check Status**: Verify Ollama is running and the model is available
3. **Start Chatting**: Type your message and press Enter
4. **View Responses**: See the model's responses stream in real-time
5. **Chat History**: Your conversation history is automatically saved

## System Requirements

- **RAM**: 2GB minimum, 4GB+ recommended
- **Storage**: 500MB free space
- **OS**: Linux, macOS, or Windows (with WSL)
- **Python**: 3.11 or later

## Quick Start

```bash
# 1. Install and start Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama serve

# 2. Pull the model
ollama pull gemma3:270m

# 3. Install dependencies
pip install streamlit ollama

# 4. Run the app
streamlit run app.py
```

## Troubleshooting

**Ollama not running:**
```bash
ollama serve
```

**Model not found:**
```bash
ollama pull gemma3:270m
```

**Port already in use:**
```bash
streamlit run app.py --server.port 8502
```

**Out of memory:**
- Close other applications
- Restart Ollama service
- Ensure adequate RAM is available

---

## 🤝 **Connect & Learn More**

**Vikram Pawar** - AI Engineer passionate about making AI accessible through local deployment.

- **LinkedIn**: [@aiwithvikram](https://www.linkedin.com/in/aiwithvikram/)
- **Twitter**: [@AIwithVikram](https://x.com/AIwithVikram)
- **AI Brewing Club**: [Subscribe](http://aibrewingclub.com/) for AI insights & coding techniques