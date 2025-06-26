"""Main script for the model comparison tool."""

import os
import click
import requests
from dotenv import load_dotenv
from config import MODELS, API_CONFIG, DEFAULT_CONFIG
from utils import generate_response, display_summary

# Load environment variables from .env file
load_dotenv()

@click.command()
@click.option('--query', prompt='Enter your query', help='The query to be processed by the models.')
@click.option('--model-type', type=click.Choice(['base', 'instruct', 'fine_tuned']), prompt='Choose model type', help='Type of model to use for the query.')
@click.option('--provider', type=click.Choice(['openai', 'huggingface', 'anthropic']), prompt='Choose provider', help='Model provider.')
def main(query: str, model_type: str, provider: str):
    """Main function to handle user input and generate model responses."""
    model_info = MODELS[model_type][provider]
    api_config = API_CONFIG[provider]

    click.echo(f'Using {model_info["name"]} from {provider.capitalize()} for {model_type} query...')

    response = generate_response(query, model_info, api_config, DEFAULT_CONFIG)
    display_summary(query, response, model_info)

if __name__ == '__main__':
    main()
