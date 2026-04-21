import os
from datetime import datetime
from PyPDF2 import PdfReader
from docx import Document


def read_file(filepath: str) -> dict:
    try:
        ext = os.path.splitext(filepath)[1].lower()
        content = ""

        if ext == ".txt":
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

        elif ext == ".pdf":
            reader = PdfReader(filepath)
            for page in reader.pages:
                content += page.extract_text() or ""

        elif ext == ".docx":
            doc = Document(filepath)
            content = "\n".join([p.text for p in doc.paragraphs])

        else:
            return {"status": "error", "message": "Unsupported file type"}

        return {
            "status": "success",
            "content": content,
            "metadata": {
                "file": filepath,
                "size": os.path.getsize(filepath),
                "modified": str(datetime.fromtimestamp(os.path.getmtime(filepath)))
            }
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


def list_files(directory: str, extension: str = None) -> list:
    try:
        results = []
        for file in os.listdir(directory):
            path = os.path.join(directory, file)

            if not os.path.isfile(path):
                continue

            if extension and not file.lower().endswith(extension.lower()):
                continue

            results.append({
                "name": file,
                "size": os.path.getsize(path),
                "modified": str(datetime.fromtimestamp(os.path.getmtime(path)))
            })

        return results

    except Exception as e:
        return [{"error": str(e)}]


def write_file(filepath: str, content: str) -> dict:
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return {"status": "success", "file": filepath}

    except Exception as e:
        return {"status": "error", "message": str(e)}


def search_in_file(filepath: str, keyword: str) -> dict:
    try:
        data = read_file(filepath)

        if data["status"] != "success":
            return data

        text = data["content"]
        lower_text = text.lower()
        keyword = keyword.lower()

        matches = []
        idx = lower_text.find(keyword)

        while idx != -1:
            start = max(0, idx - 40)
            end = min(len(text), idx + 40)

            matches.append(text[start:end])
            idx = lower_text.find(keyword, idx + 1)

        return {"status": "success", "matches": matches}

    except Exception as e:
        return {"status": "error", "message": str(e)}




if __name__ == "__main__":
    print(read_file("resumes/resume1.txt"))