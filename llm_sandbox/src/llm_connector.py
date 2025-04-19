import os

from openai import OpenAI
import ollama
# from mistralai.client import MistralClient
import google.generativeai as genai
# from anthropic import Anthropic
from groq import Groq

def create_model_client(model_name):
    """
    Create a client for the specified model based on the provider.
    
    Args:
        model_name (str): Name of the model to use
    
    Returns:
        tuple: (client_object, model_name, provider_name)
    """
    provider_mapping = {
        'openai': ['gpt-', 'text-', 'dall-e'],
        'ollama': ['llama3.2', 'meta-', 'deepseek'],
        'mistral': ['mistral', 'mixtral', 'codestral'],
        'google': ['gemini'],
        'anthropic': ['claude'],
        'groq': ['groq',
        'gemma2-9b-it',
        'llama-3.3-70b-versatile','llama-3.1-8b-instant','llama-guard-3-8b','llama3-70b-8192','llama3-8b-8192', 
        'whisper-large-v3', 'whisper-large-v3-turbo','distil-whisper-large-v3-en']
    }
    
    provider = 'ollama'  # default provider
    for prov, prefixes in provider_mapping.items():
        if any(model_name.startswith(prefix) for prefix in prefixes):
            provider = prov
            break

    # if provider == 'mistral' and 'MISTRAL_API_KEY' not in os.environ:
    #     provider = 'ollama'
    
    if provider == 'openai':
        openai_api_key = os.getenv('OPENAI_API_KEY')
        return OpenAI(api_key=openai_api_key), model_name, 'OpenAI'
    
    elif provider == 'mistral':
        # mistral_api_key = os.getenv('MISTRAL_API_KEY')
        # return MistralClient(api_key=mistral_api_key), model_name, 'Mistral'
        provider == 'ollama'

    if provider == 'ollama':
        models = ollama.list().get('models', [])
        model_exists = any(m.get('name') == model_name for m in models)
        if not model_exists:
            print(f"Model '{model_name}' not found locally. Pulling from Ollama...")
            ollama.pull(model_name)
            print(f"Successfully pulled model: {model_name}")
        return ollama, model_name, 'Ollama'
    
    elif provider == 'google':
        google_api_key = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=google_api_key)
        return genai, model_name, 'Google Gemini'
    
    elif provider == 'anthropic':
        anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        return Anthropic(api_key=anthropic_api_key), model_name, 'Anthropic'
    
    elif provider == 'groq':
        groq_api_key = os.getenv('GROQ_API_KEY')
        return Groq(api_key=groq_api_key), model_name, 'Groq'
    
    else:
        raise ValueError(f"Unsupported model provider: {model_name},{provider}")
    

def chat_with_model(model_name, user_message, system_message=None):
    """
    Send a message to the specified model and return the response.
    
    Args:
        model_name (str): Name of the model to use
        user_message (str): Message to send to the model
        system_message (str, optional): System instructions/context
        
    Returns:
        str: Model's response
    """
    client, model, provider_name = create_model_client(model_name)
    
    print(f"Using {provider_name} with model: {model}")
        
    messages = []

    if system_message:
        messages.append({"role": "system", "content": system_message})
    
    messages.append({"role": "user", "content": user_message})
    
    provider_handlers = {
        'OpenAI': lambda: client.chat.completions.create(
            model=model,
            messages=messages
        ).choices[0].message.content,
        
        'Ollama': lambda: client.chat(
            model=model, 
            messages=messages
        )['message']['content'],
        
        'Mistral': lambda: client.chat(
            model=model,
            messages=messages
        ).choices[0].message.content,
        
        'Anthropic': lambda: client.messages.create(
            model=model,
            system=system_message if system_message else None,
            messages=[{"role": "user", "content": user_message}]
        ).content[0].text,
        
        'Groq': lambda: client.chat.completions.create(
            model=model,
            messages=messages
        ).choices[0].message.content,

        'Google Gemini': lambda: client.GenerativeModel(model).generate_content(
            [{
                "role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]
            } for msg in messages]
        ).text if system_message else client.GenerativeModel(model).generate_content(user_message).text
    }
    
    handler = provider_handlers.get(provider_name)
    
    if handler:
        return handler()
    else:
        return "Unsupported provider"
    

def get_model_response(model_name, user_message, system_message=None):
    """
    Get a response from a specified model using provided messages.
    
    Args:
        model_name (str): Name of the model to use
        user_message (str): Message to send to the model
        system_message (str, optional): System instructions/context
        
    Returns:
        str: Model's response
    """
    print(f"Using model: {model_name}")
    if system_message:
        print(f"With system prompt: {system_message[:50]}...")
    if user_message:
        print(f"With user prompt: {user_message[:50]}...")
    try:
        response = chat_with_model(model_name, user_message, system_message)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None