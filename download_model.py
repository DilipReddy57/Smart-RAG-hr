from huggingface_hub import hf_hub_download
import os

model_name = "bartowski/Llama-3.2-1B-Instruct-GGUF"
model_file = "Llama-3.2-1B-Instruct-Q4_K_M.gguf"
local_dir = "data/models"

print(f"Downloading {model_file} from {model_name}...")
os.makedirs(local_dir, exist_ok=True)

path = hf_hub_download(
    repo_id=model_name,
    filename=model_file,
    local_dir=local_dir,
    local_dir_use_symlinks=False
)

print(f"Model downloaded to: {path}")
