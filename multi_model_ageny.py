import os
import sys
import json
import base64
import zlib
import re
import requests
import openai
from typing import List, Dict, Any, Optional

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COMPILER_EXPLORER_API_URL = os.getenv("COMPILER_EXPLORER_API_URL", "https://godbolt.org")

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY environment variable not set.")
    sys.exit(1)

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# ---------------------------- Helper Functions ---------------------------- #
def get_authenticated_headers(additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """
    Returns headers with authentication if required in the future.
    Currently, no authentication is implemented.
    """
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    if additional_headers:
        headers.update(additional_headers)
    return headers

def handle_api_response(response: requests.Response) -> Any:
    """
    Handles API responses, checking for success and parsing JSON.
    Raises an exception if the request was unsuccessful.
    """
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text
    else:
        raise Exception(f"API request failed: {response.status_code}, {response.text}")

def get_languages(api_base_url: str) -> Any:
    url = f"{api_base_url}/api/languages"
    headers = get_authenticated_headers()
    response = requests.get(url, headers=headers)
    return handle_api_response(response)

def get_compilers(api_base_url: str, language_id: str, fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    url = f"{api_base_url}/api/compilers/{language_id}"
    headers = get_authenticated_headers()
    params = {}
    if fields:
        params['fields'] = ','.join(fields)
    response = requests.get(url, headers=headers, params=params)
    return handle_api_response(response)

def compile_code(api_base_url: str, compiler_id: str, source_code: str,
                 options: Optional[Dict[str, Any]] = None,
                 filters: Optional[Dict[str, bool]] = None,
                 tools: Optional[List[Dict[str, Any]]] = None,
                 libraries: Optional[List[Dict[str, str]]] = None,
                 lang: Optional[str] = None,
                 allow_store: bool = True,
                 bypass_cache: Optional[int] = None) -> Dict[str, Any]:
    """
    Submits code for compilation.
    """
    url = f"{api_base_url}/api/compiler/{compiler_id}/compile"
    payload = {
        "source": source_code,
        "options": {}
    }
    if options:
        payload["options"].update(options)
    if filters:
        payload["options"]["filters"] = filters
    if tools:
        payload["options"]["tools"] = tools
    if libraries:
        payload["options"]["libraries"] = libraries
    if lang:
        payload["lang"] = lang
    payload["allowStoreCodeDebug"] = allow_store
    if bypass_cache is not None:
        payload["options"]["bypassCache"] = bypass_cache
    
    headers = get_authenticated_headers()
    response = requests.post(url, json=payload, headers=headers)
    return handle_api_response(response)

def get_formatters(api_base_url: str) -> List[Dict[str, Any]]:
    """
    Fetches the list of available code formatters.
    """
    url = f"{api_base_url}/api/formats"
    headers = get_authenticated_headers()
    response = requests.get(url, headers=headers)
    return handle_api_response(response)

def format_code(api_base_url: str, formatter: str, source_code: str,
                base_style: str, use_spaces: bool = True, tab_width: int = 4) -> Dict[str, Any]:
    """
    Formats code using a specified formatter.
    """
    url = f"{api_base_url}/api/format/{formatter}"
    payload = {
        "source": source_code,
        "base": base_style,
        "useSpaces": use_spaces,
        "tabWidth": tab_width
    }
    headers = get_authenticated_headers()
    response = requests.post(url, json=payload, headers=headers)
    return handle_api_response(response)

def create_shortlink(api_base_url: str, client_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a shortlink for the given client state.
    """
    url = f"{api_base_url}/api/shortener"
    headers = get_authenticated_headers()
    response = requests.post(url, json=client_state, headers=headers)
    return handle_api_response(response)

def get_shortlink_info(api_base_url: str, link_id: str) -> Dict[str, Any]:
    """
    Retrieves information about a given shortlink.
    """
    url = f"{api_base_url}/api/shortlinkinfo/{link_id}"
    headers = get_authenticated_headers()
    response = requests.get(url, headers=headers)
    return handle_api_response(response)

def analyze_user_input(user_input: str) -> Dict[str, Any]:
    """
    Uses OpenAI's language model to analyze and interpret user input.
    """
    prompt = (
        "You are a helpful assistant that analyzes user requests for code compilation and formatting.\n"
        "Extract the following information from the user's input:\n"
        "- Programming language\n"
        "- Source code\n"
        "- Desired actions (e.g., compile, format)\n"
        "Respond with a JSON object containing these fields. If any field is not applicable, set it to null.\n"
        f"User input: \"{user_input}\"\nResponse:"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a code assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.2,
        )
        assistant_reply = response['choices'][0]['message']['content']
        extracted_info = json.loads(assistant_reply.strip())
        return extracted_info
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return {}

