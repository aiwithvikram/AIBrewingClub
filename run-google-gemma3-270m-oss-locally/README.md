# Run Google Gemma 3 (270M) Locally 🚀

Experience the power of Google's Gemma 3 270M model locally - a lightweight yet capable language model that runs efficiently on your own hardware using Ollama.

## Why This Matters

- 🏠 **100% Local**: Run Gemma 3 on your own hardware using Ollama
- 🚀 **Ultra-Efficient**: 268.1M parameter model that's incredibly fast and resource-friendly
- 🔒 **Privacy First**: Your conversations never leave your machine
- 🧠 **Smart AI**: Powered by Google's latest Gemma 3 architecture
- 💰 **Zero Cost**: No API fees or usage limits
- ⚡ **Fast Response**: Optimized for quick, helpful interactions
- 📱 **Low Resource**: Perfect for laptops, desktops, and even some mobile devices

## Key Features

- **Streaming Chat Interface**: Real-time response generation with smooth streaming
- **Chat History**: Full conversation history preserved across sessions
- **Clean Interface**: Professional UI with Google Gemma and Ollama branding
- **Status Monitoring**: Real-time Ollama service and model availability status
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Fast Inference**: Sub-second response times for most queries

## About Gemma 3 (270M)

Gemma 3 is Google's latest family of open models, designed to be:
- **Efficient**: Optimized for speed and resource usage
- **Capable**: Strong performance despite smaller size
- **Safe**: Built with safety and responsible AI principles
- **Accessible**: Runs on consumer hardware without specialized equipment

### Technical Specifications

| Specification | Value |
|---------------|-------|
| **Parameters** | 268.1M |
| **Context Length** | 32,768 tokens |
| **Embedding Length** | 640 |
| **Quantization** | Q8_0 |
| **Model Size** | 291 MB |
| **Architecture** | Gemma 3 |
| **License** | Gemma Terms of Use |

### Performance Metrics

Based on actual testing with Ollama:
- **Load Time**: ~600ms
- **Prompt Processing**: 214.05 tokens/second
- **Response Generation**: 176.02 tokens/second
- **Total Response Time**: ~2.5 seconds for complex queries

### Capabilities

The 270M parameter version offers an excellent balance of performance and efficiency:
- **Text Generation**: Creative and engaging content creation
- **Conversation**: Natural chat and dialogue capabilities
- **Multilingual Support**: Understanding and generation in multiple languages
- **Code Understanding**: Basic programming and technical text comprehension
- **Creative Writing**: Storytelling, poetry, and creative content
- **Question Answering**: General knowledge and factual responses

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

### Minimum Requirements
- **RAM**: 2GB available
- **Storage**: 500MB free space
- **OS**: Linux, macOS, or Windows (with WSL)
- **Python**: 3.11 or later

### Recommended Requirements
- **RAM**: 4GB+ available
- **Storage**: 1GB+ free space (SSD preferred)
- **CPU**: Modern multi-core processor
- **Network**: Stable internet for initial model download

### Performance Notes
- **First Run**: Model download takes ~2-5 minutes depending on internet speed
- **Subsequent Runs**: Model loads in ~600ms
- **Memory Usage**: ~300MB RAM during operation
- **Storage**: Model file is 291MB

## Model Comparison

| Model | Parameters | Size | Speed | Quality | RAM Usage | Use Case |
|-------|------------|------|-------|---------|-----------|----------|
| **Gemma 3:270M** | 268.1M | 291MB | ⚡⚡⚡ | ⭐⭐⭐ | 💾💾 | **Lightweight tasks, quick responses** |
| Llama 3.2:latest | 2B | 2.0GB | ⚡⚡ | ⭐⭐⭐⭐ | 💾💾💾 | Balanced performance |
| Llama 3:latest | 4B | 4.7GB | ⚡ | ⭐⭐⭐⭐⭐ | 💾💾💾💾 | High quality, slower |
| GPT-OSS:20B | 20B | 13GB | 🐌 | ⭐⭐⭐⭐⭐ | 💾💾💾💾💾 | Maximum quality, high resources |

## Troubleshooting

### Common Issues

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

### Performance Tips

- **Close Background Apps**: Free up RAM for better performance
- **Use SSD Storage**: Faster model loading and inference
- **Stable Internet**: For initial model download
- **Regular Restarts**: Restart Ollama if performance degrades
- **Monitor Resources**: Keep an eye on RAM and CPU usage

### Expected Behavior

- **Model Loading**: 500ms - 1 second on first run
- **Response Time**: 1-3 seconds for typical queries
- **Memory Usage**: 300-500MB during operation
- **Storage**: 291MB model file

## Advanced Usage

### Custom Model Parameters

You can customize the model behavior by modifying Ollama parameters:

```