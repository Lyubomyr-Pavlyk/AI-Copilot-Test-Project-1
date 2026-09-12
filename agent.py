# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 12:16:33 2026

@author: Lyubomyr


A very small coding agent for the Excel-average project.

It uses LM Studio as the local LLM and gives the model four tools:
    - list_files()
    - read_file()
    - write_file()
    - run_python()

Start LM Studio's local server before running this file.


"""


from openai import OpenAI
from pathlib import Path
import subprocess
import json


# ---------------------------------------------------------
# 1. Project and LM Studio settings
# ---------------------------------------------------------

PROJECT_DIR = Path(r"d:\Projects\AI Copilot Test Projects\AI Copilot Test Project 1")

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)


# ---------------------------------------------------------
# 2. Tools the agent is allowed to use
# ---------------------------------------------------------

def list_files():
    """List Python files in the project."""
    files = []

    for pattern in ("*.py", "*.md"):
        for path in PROJECT_DIR.glob(pattern):
            files.append(path.name)

    return files


def read_file(filename):
    """Read a Python file from the project."""
    path = PROJECT_DIR / filename

    if path.suffix != ".py":
        return "ERROR: I can only read .py files."

    if not path.exists():
        return f"ERROR: {filename} does not exist."

    return path.read_text(encoding="utf-8")


def write_file(filename, content):
    """Write a Python or .md file in the project."""
    path = PROJECT_DIR / filename
    
    allowed_extensions = {".py", ".md"}
    
    if path.suffix.lower() not in allowed_extensions:
        return "ERROR: I can only write .py or .md files."

    # Safety: don't allow the agent to write outside the project folder.
    try:
        path.resolve().relative_to(PROJECT_DIR.resolve())
    except ValueError:
        return "ERROR: File must be inside the project folder."

    path.write_text(content, encoding="utf-8")

    return f"{filename} was written successfully."


def run_python(filename):
    """Run a Python file from the project."""
    path = PROJECT_DIR / filename

    if path.suffix != ".py":
        return "ERROR: I can only run .py files."

    if not path.exists():
        return f"ERROR: {filename} does not exist."

    result = subprocess.run(
        ["python", str(path)],
        cwd=str(PROJECT_DIR),
        capture_output=True,
        text=True
    )

    return json.dumps({
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }, indent=2)


# ---------------------------------------------------------
# 3. Tell the model about the tools
# ---------------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List Python files in the project.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a Python file from the project.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of the .py file to read"
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Replace the contents of a Python file in the project. A .bak backup is created first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of the .py file to modify"
                    },
                    "content": {
                        "type": "string",
                        "description": "Complete new contents of the Python file"
                    }
                },
                "required": ["filename", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_python",
            "description": "Run a Python file and return its output and errors.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of the .py file to run"
                    }
                },
                "required": ["filename"]
            }
        }
    }
]


# ---------------------------------------------------------
# 4. Connect model tool calls to our Python functions
# ---------------------------------------------------------

available_functions = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "run_python": run_python
}


# ---------------------------------------------------------
# 5. The agent loop
# ---------------------------------------------------------

def run_agent(request):

    messages = [
        {
            "role": "system",
            "content": """
You are a coding agent working on a small Python project.

Your job is to modify the existing project, not rewrite it unnecessarily.

Before changing code:
1. Inspect the project files.
2. Read the relevant Python files.
3. Understand how they work together.

When you make changes:
1. Modify only files that need changing.
2. Keep the code understandable for a beginner.
3. Run main.py after making changes.
4. If there is an error, inspect it and fix the code.
5. Explain what you changed at the end.

You may only work with the project files exposed by the available tools.
"""
        },
        {
            "role": "user",
            "content": request
        }
    ]

    while True:

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Add the assistant's response to the conversation.
        messages.append(message)

        # If there are no tool calls, the agent is finished.
        if not message.tool_calls:
            print("\nAGENT:")
            print(message.content)
            break

        # Execute each requested tool.
        for tool_call in message.tool_calls:

            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"\n[Agent is using: {function_name}]")
            print(arguments)

            function = available_functions.get(function_name)

            if function is None:
                result = f"ERROR: Unknown tool {function_name}"
            else:
                try:
                    result = function(**arguments)
                except Exception as e:
                    result = f"ERROR while running {function_name}: {e}"

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })


# ---------------------------------------------------------
# 6. Main program
# ---------------------------------------------------------

if __name__ == "__main__":

    # Ask LM Studio which model is available.
    models = client.models.list()

    if not models.data:
        raise RuntimeError(
            "LM Studio is running, but no model is loaded/available."
        )

    MODEL_NAME = models.data[0].id

    print("Using model:", MODEL_NAME)
    print("Project:", PROJECT_DIR)

    request = input("\nWhat would you like the agent to change? ")

    run_agent(request)
