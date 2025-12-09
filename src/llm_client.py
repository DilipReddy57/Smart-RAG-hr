from gpt4all import GPT4All
import os
import sys

# Path to the downloaded model
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'models')
MODEL_FILENAME = "Llama-3.2-1B-Instruct-Q4_K_M.gguf"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)

import sys
import contextlib

@contextlib.contextmanager
def suppress_stderr():
    with open(os.devnull, "w") as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr

class LocalLLM:
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Please run download_model.py first.")
        
        print(f"Loading AI Model... (This may take 10-20 seconds)")
        
        # Suppress the "Failed to load llamamodel..." CPU warnings
        with suppress_stderr():
            # allow_download=False ensures offline mode
            self.llm = GPT4All(model_name=MODEL_FILENAME, model_path=MODEL_DIR, allow_download=False, device='cpu')
        print("Model loaded successfully.")

    def chat(self, messages, max_tokens=1024, temperature=0.1):
        """
        Manually formats the prompt for Llama 3 and uses generate().
        messages: list of dicts [{'role': 'system', 'content': '...'}, {'role': 'user', 'content': '...'}]
        """
        try:
            # Llama 3 template construction
            full_prompt = "<|begin_of_text|>"
            for msg in messages:
                role = msg['role']
                content = msg['content']
                full_prompt += f"<|start_header_id|>{role}<|end_header_id|>\n\n{content}<|eot_id|>"
            
            full_prompt += "<|start_header_id|>assistant<|end_header_id|>\n\n"
            
            stop_tokens = ["<|eot_id|>", "<|start_header_id|>"]
            
            response = self.llm.generate(
                full_prompt,
                max_tokens=max_tokens,
                temp=temperature
            )
            
            # Post-processing to stop at eot_id if the model didn't stop
            for stop in stop_tokens:
                if stop in response:
                    response = response.split(stop)[0]
            
            # Aggressive safety stops for hallucinated conversations
            # Llama 3 sometimes leaks "User:" or "assistant:" patterns textually
            heuristic_stops = ["\nUser:", "\nuser:", "\nAssistant:", "\nassistant:", "User:", "user:"]
            for h_stop in heuristic_stops:
                if h_stop in response:
                     response = response.split(h_stop)[0]
                
            return response.strip()
        except Exception as e:
            print(f"Error in LLM Generation: {e}")
            return "I apologize, but I encountered an error generating the response."

_llm_instance = None

def get_llm():
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = LocalLLM()
    return _llm_instance
