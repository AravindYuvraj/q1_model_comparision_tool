"""Configuration module for model comparison tool."""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model definitions with characteristics
MODELS = {
    "base": {
        "openai": {
            "name": "gpt-3.5-turbo-instruct",
            "type": "base",
            "provider": "OpenAI",
            "context_window": 4096,
            "characteristics": {
                "description": "Base completion model without instruction tuning",
                "fine_tuning_strategy": "Pre-trained on diverse text data",
                "instruction_following": "Limited - requires careful prompting",
                "use_cases": "Text completion, creative writing, code generation with examples"
            }
        },
        "huggingface": {
            "name": "distilgpt2",
            "type": "base",
            "provider": "Hugging Face",
            "context_window": 1024,
            "characteristics": {
                "description": "Smaller, faster version of GPT-2",
                "fine_tuning_strategy": "Distilled from GPT-2",
                "instruction_following": "Limited - text completion style",
                "use_cases": "Text generation, completion, creative writing"
            }
        }
    },
    "instruct": {
        "openai": {
            "name": "gpt-3.5-turbo",
            "type": "instruct",
            "provider": "OpenAI",
            "context_window": 16385,
            "characteristics": {
                "description": "Instruction-tuned chat model",
                "fine_tuning_strategy": "RLHF (Reinforcement Learning from Human Feedback)",
                "instruction_following": "Excellent - follows instructions reliably",
                "use_cases": "Chat, Q&A, instruction following, general assistance"
            }
        },
        "anthropic": {
            "name": "claude-3-haiku-20240307",
            "type": "instruct",
            "provider": "Anthropic",
            "context_window": 200000,
            "characteristics": {
                "description": "Constitutional AI instruction-tuned model",
                "fine_tuning_strategy": "Constitutional AI + RLHF",
                "instruction_following": "Excellent - helpful, harmless, honest",
                "use_cases": "Complex reasoning, analysis, safe AI assistance"
            }
        },
        "huggingface": {
            "name": "microsoft/DialoGPT-small",
            "type": "instruct",
            "provider": "Hugging Face",
            "context_window": 1024,
            "characteristics": {
                "description": "Small conversational model",
                "fine_tuning_strategy": "Fine-tuned for dialogue",
                "instruction_following": "Good - conversational responses",
                "use_cases": "Chat, conversation, dialogue systems"
            }
        }
    },
    "fine_tuned": {
        "openai": {
            "name": "ft:gpt-3.5-turbo",
            "type": "fine_tuned",
            "provider": "OpenAI",
            "context_window": 16385,
            "characteristics": {
                "description": "Custom fine-tuned model (example)",
                "fine_tuning_strategy": "Task-specific fine-tuning on custom dataset",
                "instruction_following": "Domain-specific - optimized for specific tasks",
                "use_cases": "Specialized tasks, domain-specific applications"
            }
        },
        "huggingface": {
            "name": "microsoft/DialoGPT-medium",
            "type": "fine_tuned",
            "provider": "Hugging Face",
            "context_window": 1024,
            "characteristics": {
                "description": "Fine-tuned for conversational responses",
                "fine_tuning_strategy": "Fine-tuned on Reddit conversations",
                "instruction_following": "Moderate - conversational but not instruction-specific",
                "use_cases": "Dialogue systems, chatbots, conversational AI"
            }
        }
    }
}

# Default configuration
DEFAULT_CONFIG = {
    "max_tokens": int(os.getenv("DEFAULT_MAX_TOKENS", 1000)),
    "temperature": float(os.getenv("DEFAULT_TEMPERATURE", 0.7)),
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
}

# API endpoints and configuration
API_CONFIG = {
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "base_url": "https://api.openai.com/v1"
    },
    "anthropic": {
        "api_key": os.getenv("ANTHROPIC_API_KEY")
    },
    "huggingface": {
        "api_key": os.getenv("HUGGINGFACE_API_KEY"),
        "base_url": "https://api-inference.huggingface.co/models"
    }
}
