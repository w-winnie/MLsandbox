import os

from openai import OpenAI
import ollama
# from mistralai.client import MistralClient
import google.generativeai as genai
from anthropic import Anthropic
from groq import Groq

def create_model_client(model_name):
    provider_mapping = {
        'openai': ['gpt'],
        'google': ['gemini'],
        'anthropic': ['claude'],
        'grok': ['grok'],
        'ollama': ['llama3.2', 'meta', 'deepseek'],
        'mistral': ['mistral', 'mixtral', 'codestral'],
        'groq': ['groq','gemma2-9b-it','llama-3.3-70b-versatile','llama-3.1-8b-instant','llama-guard-3-8b','llama3-70b-8192','llama3-8b-8192','whisper-large-v3', 'whisper-large-v3-turbo','distil-whisper-large-v3-en'],
    }
    
    provider = 'ollama'  # default provider
    for prov, prefixes in provider_mapping.items():
        if any(model_name.startswith(prefix) for prefix in prefixes):
            provider = prov
            break

    print(f"Detected provider: {provider}")
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
    
    elif provider == 'grok':  
        grok_api_key = os.getenv('GROK_API_KEY') 
        return OpenAI(api_key=grok_api_key, base_url="https://api.x.ai/v1"), model_name, 'Grok with OpenAIAPI'
    
    else:
        raise ValueError(f"Unsupported model provider: {model_name},{provider}")


def chat_with_model(model_name, user_message, system_message=None):
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
            messages=[{"role": "user", "content": user_message}],
            max_tokens=500
        ).content[0].text,
        
        'Groq': lambda: client.chat.completions.create(
            model=model,
            messages=messages
        ).choices[0].message.content,

        'Google Gemini': lambda: client.GenerativeModel(model).generate_content(
            [{
                "role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]
            } for msg in messages]
        ).text if system_message else client.GenerativeModel(model).generate_content(user_message).text,

        'Grok with OpenAIAPI': lambda: client.chat.completions.create(
            model=model,
            messages=messages
        ).choices[0].message.content
    }

    handler = provider_handlers.get(provider_name)
    if handler:
        return handler()
    else:
        return "Unsupported provider"



def chat_with_model_history(model_name, messages):
    client, model, provider_name = create_model_client(model_name)
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
            system=[msg["content"] for msg in messages if msg["role"] == "system"][0] if any(msg["role"] == "system" for msg in messages) else None,
            messages=[msg for msg in messages if msg["role"] != "system"],
            max_tokens=500
        ).content[0].text,

        'Groq': lambda: client.chat.completions.create(
            model=model,
            messages=messages
        ).choices[0].message.content,

        'Google Gemini': lambda: client.GenerativeModel(model).generate_content(
            [{
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [msg["content"]]
            } for msg in messages]
        ).text,

        'Grok with OpenAIAPI': lambda: client.chat.completions.create(
            model=model,
            messages=messages
        ).choices[0].message.content
    }

    handler = provider_handlers.get(provider_name)
    if handler:
        return handler()
    else:
        raise ValueError(f"Unsupported provider: {provider_name}")