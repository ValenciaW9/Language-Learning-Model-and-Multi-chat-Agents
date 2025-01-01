# Multi-Model Agency

`multi_model_agency.py` is a Python script designed to interact with OpenAI's API and Compiler Explorer API. It provides tools for compiling and formatting code, analyzing user input, and creating shortlinks for sharing code snippets and compiler configurations. 

-

## Features

- API Integration**:
  - Supports OpenAI API for language model-based user input analysis.
  - Integrates with Compiler Explorer API for code compilation, formatting, and shortlink generation.

- Code Compilation:
  - Retrieve available compilers for a specific programming language.
  - Submit code for compilation with customizable options, filters, and tools.

- Code Formatting:
  - List available formatters.
  - Format source code using specified style options (e.g., tab width, spaces vs. tabs).

- Shortlink Management:
  - Create shortlinks for sharing code and compiler configurations.
  - Retrieve detailed information about shortlinks.

- User Input Analysis:
  - Extract key details from user requests, including programming language, source code, and desired actions.

---

## Prerequisites

- Python: Version 3.7 or higher.
- Libraries: Install dependencies using `pip install -r requirements.txt`.
- Environment Variables:
  - `OPENAI_API_KEY`: Your OpenAI API key.
  - `COMPILER_EXPLORER_API_URL` (optional): URL for Compiler Explorer API (default: `https://godbolt.org`).

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/multi-model-agency.git
   cd multi-model-agency
