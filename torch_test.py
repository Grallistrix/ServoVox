import torch

if torch.cuda.is_available():
    print(f"GPU detected: {torch.cuda.get_device_name(0)}")
    print(f"Number of GPUs: {torch.cuda.device_count()}")
else:
    print("No GPU detected. Using CPU.")


import requests

prompt = "Hello, servo!"
response = requests.post(
    "http://localhost:11434/v1/completions",
    json={"model": "llama3.1:8b", "prompt": prompt}
)
print(response.json())
