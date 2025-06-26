"""Utility functions for the model comparison tool."""

import os
import json
import time
import requests
import tiktoken
from typing import Dict, Any, Optional
from colorama import init, Fore, Style
from tabulate import tabulate

# Initialize colorama for Windows compatibility
init()

def count_tokens(text: str, model_name: str = "gpt-3.5-turbo") -> int:
    """Count tokens in text using tiktoken."""
    try:
        encoding = tiktoken.encoding_for_model(model_name)
        return len(encoding.encode(text))
    except Exception:
        # Fallback: rough estimation
        return len(text.split()) * 1.3

def generate_response(query: str, model_info: Dict[str, Any], api_config: Dict[str, Any], default_config: Dict[str, Any]) -> Dict[str, Any]:
    """Generate response from the specified model."""
    provider = model_info["provider"].lower()
    
    if provider == "openai":
        return _call_openai_api(query, model_info, api_config, default_config)
    elif provider == "anthropic":
        return _call_anthropic_api(query, model_info, api_config, default_config)
    elif provider == "hugging face":
        return _call_huggingface_api(query, model_info, api_config, default_config)
    else:
        return {"error": f"Provider {provider} not supported"}

def _call_openai_api(query: str, model_info: Dict[str, Any], api_config: Dict[str, Any], default_config: Dict[str, Any]) -> Dict[str, Any]:
    """Call OpenAI API."""
    if not api_config["api_key"]:
        return {"error": "OpenAI API key not found. Please set OPENAI_API_KEY in your .env file."}
    
    try:
        import openai
        client = openai.OpenAI(api_key=api_config["api_key"])
        
        start_time = time.time()
        
        # Handle different model types
        if model_info["type"] == "base" and "instruct" in model_info["name"]:
            # Use completion API for base instruct models
            response = client.completions.create(
                model=model_info["name"],
                prompt=query,
                max_tokens=default_config["max_tokens"],
                temperature=default_config["temperature"]
            )
            response_text = response.choices[0].text.strip()
            tokens_used = response.usage.total_tokens
        else:
            # Use chat API for chat models
            response = client.chat.completions.create(
                model=model_info["name"],
                messages=[{"role": "user", "content": query}],
                max_tokens=default_config["max_tokens"],
                temperature=default_config["temperature"]
            )
            response_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
        
        end_time = time.time()
        
        return {
            "response": response_text,
            "tokens_used": tokens_used,
            "response_time": end_time - start_time,
            "success": True
        }
    except Exception as e:
        return {"error": str(e), "success": False}

def _call_anthropic_api(query: str, model_info: Dict[str, Any], api_config: Dict[str, Any], default_config: Dict[str, Any]) -> Dict[str, Any]:
    """Call Anthropic API."""
    if not api_config["api_key"]:
        return {"error": "Anthropic API key not found. Please set ANTHROPIC_API_KEY in your .env file."}
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_config["api_key"])
        
        start_time = time.time()
        
        response = client.messages.create(
            model=model_info["name"],
            max_tokens=default_config["max_tokens"],
            temperature=default_config["temperature"],
            messages=[{"role": "user", "content": query}]
        )
        
        end_time = time.time()
        
        response_text = response.content[0].text
        tokens_used = response.usage.input_tokens + response.usage.output_tokens
        
        return {
            "response": response_text,
            "tokens_used": tokens_used,
            "response_time": end_time - start_time,
            "success": True
        }
    except Exception as e:
        return {"error": str(e), "success": False}

def _call_huggingface_api(query: str, model_info: Dict[str, Any], api_config: Dict[str, Any], default_config: Dict[str, Any]) -> Dict[str, Any]:
    """Call Hugging Face API or use local model."""
    try:
        # First try API if key is available
        if api_config.get("api_key"):
            result = _call_huggingface_hosted_api(query, model_info, api_config, default_config)
            # If API fails, try different approach or return informative error
            if not result.get("success"):
                return {
                    "error": f"HuggingFace API unavailable. This might be due to: \n1. Model not available on Inference API\n2. Rate limiting\n3. API permissions\n\nSuggestion: Try again later or use OpenAI/Anthropic models.",
                    "success": False
                }
            return result
        else:
            # Fall back to local model (but warn about performance)
            return {
                "error": "No HuggingFace API key provided. Local model execution requires significant computational resources.",
                "success": False
            }
    except Exception as e:
        return {"error": f"HuggingFace integration error: {str(e)}", "success": False}

def _call_huggingface_hosted_api(query: str, model_info: Dict[str, Any], api_config: Dict[str, Any], default_config: Dict[str, Any]) -> Dict[str, Any]:
    """Call Hugging Face hosted API."""
    headers = {
        "Authorization": f"Bearer {api_config['api_key']}",
        "Content-Type": "application/json"
    }
    url = f"{api_config['base_url']}/{model_info['name']}"
    
    # Different payload format based on model type
    if "DialoGPT" in model_info['name']:
        payload = {
            "inputs": {
                "text": query
            },
            "parameters": {
                "max_length": min(default_config["max_tokens"], 100),
                "temperature": default_config["temperature"],
                "do_sample": True
            }
        }
    else:
        payload = {
            "inputs": query,
            "parameters": {
                "max_new_tokens": min(default_config["max_tokens"], 100),
                "temperature": default_config["temperature"],
                "return_full_text": False
            }
        }
    
    start_time = time.time()
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            
            # Handle different response formats
            if isinstance(result, list) and len(result) > 0:
                if "generated_text" in result[0]:
                    response_text = result[0]["generated_text"]
                    # Remove the original query from the response if it's included
                    if response_text.startswith(query):
                        response_text = response_text[len(query):].strip()
                elif "text" in result[0]:
                    response_text = result[0]["text"]
                else:
                    response_text = str(result[0])
            elif isinstance(result, dict):
                if "generated_text" in result:
                    response_text = result["generated_text"]
                    if response_text.startswith(query):
                        response_text = response_text[len(query):].strip()
                else:
                    response_text = str(result)
            else:
                response_text = str(result)
            
            tokens_used = count_tokens(query + response_text, model_info["name"])
            
            return {
                "response": response_text,
                "tokens_used": tokens_used,
                "response_time": end_time - start_time,
                "success": True
            }
        elif response.status_code == 503:
            return {"error": f"Model is loading. Please wait a moment and try again.", "success": False}
        else:
            return {"error": f"API call failed: {response.status_code} - {response.text}", "success": False}
            
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. The model might be loading.", "success": False}
    except Exception as e:
        return {"error": f"API call error: {str(e)}", "success": False}

def _call_huggingface_local(query: str, model_info: Dict[str, Any], default_config: Dict[str, Any]) -> Dict[str, Any]:
    """Use local Hugging Face model."""
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
        import torch
        
        model_name = model_info["name"]
        
        start_time = time.time()
        
        # Load model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Create pipeline
        generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Generate response
        result = generator(
            query,
            max_new_tokens=default_config["max_tokens"],
            temperature=default_config["temperature"],
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
        
        end_time = time.time()
        
        response_text = result[0]["generated_text"]
        # Remove the original query from the response
        if response_text.startswith(query):
            response_text = response_text[len(query):].strip()
        
        tokens_used = count_tokens(query + response_text, model_name)
        
        return {
            "response": response_text,
            "tokens_used": tokens_used,
            "response_time": end_time - start_time,
            "success": True
        }
    except Exception as e:
        return {"error": f"Local model error: {str(e)}", "success": False}

def display_summary(query: str, response_data: Dict[str, Any], model_info: Dict[str, Any]):
    """Display the response and model characteristics in a formatted way."""
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Query:{Style.RESET_ALL} {query}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    if response_data.get("success"):
        print(f"\n{Fore.GREEN}Response:{Style.RESET_ALL}")
        print(f"{response_data['response']}")
        
        # Display metrics
        print(f"\n{Fore.MAGENTA}Response Metrics:{Style.RESET_ALL}")
        metrics_table = [
            ["Tokens Used", response_data.get("tokens_used", "N/A")],
            ["Response Time", f"{response_data.get('response_time', 0):.2f}s"],
            ["Context Window", f"{model_info['context_window']} tokens"]
        ]
        print(tabulate(metrics_table, headers=["Metric", "Value"], tablefmt="grid"))
        
    else:
        print(f"\n{Fore.RED}Error:{Style.RESET_ALL} {response_data.get('error', 'Unknown error')}")
    
    # Display model characteristics
    print(f"\n{Fore.BLUE}Model Characteristics:{Style.RESET_ALL}")
    characteristics = model_info["characteristics"]
    char_table = [
        ["Model Name", model_info["name"]],
        ["Provider", model_info["provider"]],
        ["Type", model_info["type"].replace("_", " ").title()],
        ["Description", characteristics["description"]],
        ["Fine-tuning Strategy", characteristics["fine_tuning_strategy"]],
        ["Instruction Following", characteristics["instruction_following"]],
        ["Use Cases", characteristics["use_cases"]]
    ]
    print(tabulate(char_table, headers=["Characteristic", "Details"], tablefmt="grid"))
    
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

def create_visualization(token_usage_data: Dict[str, int], output_path: str = "token_usage.png"):
    """Create a simple visualization of token usage."""
    try:
        import matplotlib.pyplot as plt
        
        models = list(token_usage_data.keys())
        tokens = list(token_usage_data.values())
        
        plt.figure(figsize=(10, 6))
        plt.bar(models, tokens, color=['blue', 'green', 'red', 'orange', 'purple'])
        plt.title('Token Usage Comparison Across Models')
        plt.xlabel('Models')
        plt.ylabel('Tokens Used')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        
        return output_path
    except Exception as e:
        print(f"Visualization error: {e}")
        return None
