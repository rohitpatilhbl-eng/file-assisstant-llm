import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from fs_tools import read_file, list_files, write_file, search_in_file

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read file content",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string"}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string"},
                    "extension": {"type": "string"}
                },
                "required": ["directory"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_in_file",
            "description": "Search keyword in file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string"},
                    "keyword": {"type": "string"}
                },
                "required": ["filepath", "keyword"]
            }
        }
    }
]

def execute_tool(name, args):
    if name == "read_file":
        return read_file(**args)
    elif name == "list_files":
        return list_files(**args)
    elif name == "write_file":
        return write_file(**args)
    elif name == "search_in_file":
        return search_in_file(**args)


def run_assistant(query):
    query_lower = query.lower()


    if "find" in query_lower or "search" in query_lower:
        keyword = query.split()[-1]
        files = list_files("resumes")

        results = {}

        for file in files:
            filepath = f"resumes/{file['name']}"
            search_result = search_in_file(filepath, keyword)

            if search_result["matches"]:
                results[file['name']] = search_result["matches"]

        return results

    if "summary" in query_lower:
        filename = query.split()[-1]

        data = read_file(f"resumes/{filename}")

        if data["status"] == "success":
            summary = data["content"][:200]
            write_file("output/summary.txt", summary)

            return {
                "status": "success",
                "message": "Summary created",
                "file": "output/summary.txt"
            }
        else:
            return data
    messages = [
        {
            "role": "system",
            "content": "You are a file assistant. Use tools to read, search, list, and write files."
        },
        {"role": "user", "content": query}
    ]

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools
        )

        message = response.choices[0].message


        if message.tool_calls:
            tool_call = message.tool_calls[0]
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)


            result = execute_tool(name, args)


            messages.append(message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        else:

            return message.content

if __name__ == "__main__":
    while True:
        query = input("Enter your query: ")
        print(run_assistant(query))