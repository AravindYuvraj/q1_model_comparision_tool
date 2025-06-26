# Model Comparison Tool

A comprehensive command-line tool for comparing different types of AI models across multiple providers (OpenAI, Anthropic, and Hugging Face). This tool demonstrates the differences between base models, instruction-tuned models, and fine-tuned models.

## Features

- **Multi-Provider Support**: OpenAI, Anthropic, and Hugging Face
- **Model Type Comparison**: Base, Instruct, and Fine-tuned models
- **Performance Analytics**: Token usage, response time, and context window analysis
- **Professional CLI**: Beautiful formatted output with colored tables
- **Comprehensive Error Handling**: Graceful handling of API limitations
- **Secure Configuration**: Environment-based API key management

## Requirements

- Python 3.8+
- API keys for desired providers (see setup instructions below)

## 🛠 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AravindYuvraj/q1_model_comparision_tool.git
   cd model-comparison-tool
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   HUGGINGFACE_API_KEY=your_huggingface_api_key_here
   ```

## API Key Setup

### OpenAI
1. Visit https://platform.openai.com/api-keys
2. Create a new API key
3. Add it to your `.env` file

### Anthropic
1. Visit https://console.anthropic.com/
2. Create an account and generate an API key
3. Add it to your `.env` file

### Hugging Face (Optional)
1. Visit https://huggingface.co/settings/tokens
2. Create a new token with "Read" permissions
3. Add it to your `.env` file

## Usage

### Basic Usage

```bash
python main.py --query "Your question here" --model-type [base|instruct|fine_tuned] --provider [openai|anthropic|huggingface]
```

### Examples

1. **Compare instruction-following capabilities**:
   ```bash
   python main.py --query "Explain quantum computing in simple terms" --model-type "instruct" --provider "openai"
   ```

2. **Test text completion with base models**:
   ```bash
   python main.py --query "The future of artificial intelligence is" --model-type "base" --provider "openai"
   ```

3. **Analyze different providers**:
   ```bash
   python main.py --query "Write a Python function to sort a list" --model-type "instruct" --provider "anthropic"
   ```

## Output Features

The tool provides comprehensive analysis including:

- **Response Content**: The actual model output
- **Performance Metrics**: 
  - Token usage
  - Response time
  - Context window size
- **Model Characteristics**:
  - Model description
  - Fine-tuning strategy
  - Instruction following capability
  - Recommended use cases

## Project Structure

```
model-comparison-tool/
├── main.py              # CLI interface and main application
├── config.py            # Model configurations and API settings
├── utils.py             # Core functionality and API calls
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── README.md           # This file
├── comparisons.md      # Model comparison analysis
└── .gitignore          # Git ignore rules
```

## 🔧 Configuration

The tool uses three main configuration components:

1. **Models**: Defined in `config.py` with characteristics for each model type
2. **API Configuration**: Endpoint URLs and authentication
3. **Default Settings**: Token limits, temperature, and other parameters

## 🐛 Troubleshooting

### Common Issues

1. **"API key not found"**: Make sure your `.env` file is properly configured
2. **"Model not available"**: Some Hugging Face models may not be available on the Inference API
3. **Rate limiting**: Wait a moment and try again, or upgrade your API plan

### Support

If you encounter issues, please:
1. Check the error message for specific guidance
2. Verify your API keys are valid
3. Ensure all dependencies are installed
