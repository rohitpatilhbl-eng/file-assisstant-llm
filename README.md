#  LLM File Assistant

##  Overview

The **LLM File Assistant** is a Python-based application that integrates Large Language Models (LLMs) with file system tools to perform intelligent file operations such as reading, searching, listing, and summarizing resume files.

This project demonstrates **LLM tool calling**, structured interfaces, and real-world document handling.

---

##  Features

*  Read files (PDF, TXT, DOCX)
*  List files with metadata (size, modified date)
*  Write content to files (auto-create directories)
*  Search keywords across files (case-insensitive)
*  LLM-powered tool calling
*  Hybrid logic for multi-file operations
*  Resume filtering (like a mini ATS system)

---

##  How It Works

1. User enters a natural language query
2. LLM interprets the query and decides which tool to use
3. Tools perform file operations
4. Results are returned in structured format

For complex operations (like searching across multiple files), the system combines **LLM + programmatic logic** for reliability.

---

##  Project Structure

```
llm-file-assistant/
│
├── fs_tools.py                # File system tools
├── llm_file_assistant.py     # LLM integration & tool calling
├── resumes/                  # Sample resume files
├── output/                   # Generated output files
├── requirements.txt
├── README.md
├── .env
```

---

##  Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/your-username/llm-file-assistant.git
cd llm-file-assistant
```

### 2. Create virtual environment

```
python -m venv .venv
.venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Add API Key

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

---

##  Usage

Run the assistant:

```
python llm_file_assistant.py
```

---

##  Example Queries

```
List files in resumes directory
Find Python
Read resumes/resume1.txt
Create summary resume1.txt
```

---

##  Sample Output

```
{
  "resume1.txt": ["Skills: Python, Machine Learning"]
}
```

---

##  Dependencies

* openai
* python-docx
* PyPDF2
* python-dotenv

---

##  Demo

(Attach your demo video link here)

---

##  Key Learning Outcomes

* LLM function calling / tool use
* Structured API design
* File I/O automation
* Document parsing
* Hybrid AI + logic systems

---

##  Conclusion

This project showcases how LLMs can be combined with traditional programming to build intelligent, real-world applications.

---
