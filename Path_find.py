from pathlib import Path

folder_path = Path("../../texts")

files = [
    p.name for p in folder_path.rglob("*")
    if p.is_file()
]

print(files)

import nltk
try:
    nltk.data.find("tokenizers/punkt")
    print("NLTK punkt found!")
except Exception as e:
    print("NOT FOUND", e)
