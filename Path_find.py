from pathlib import Path

folder_path = Path("../texts")

files = [
    p for p in folder_path.rglob("*")
    if p.is_file()
]

print(files)
