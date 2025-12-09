# Smart HR RAG Agent

A robust, offline-capable HR Assistant powered by **Local LLMs (Llama 3 via GPT4All)** and **RAG (Retrieval Augmented Generation)**.

## 🚀 Features

- **Offline Privacy**: Runs entirely on your local machine using `gpt4all`. No data leaves your network.
- **RAG Architecture**: Accurately answers policy questions by retrieving context from local PDF documents (`data/hr_policies`).
- **Intelligent Routing**: Uses Intent Classification (Regex + Keyword + LLM) to handle:
  - Specific Policies (Leave, Salary, Welfare).
  - General Knowledge (filtered out or handled specifically).
  - Chitchat (Sanitized to prevent hallucinations).
- **Dual Interfaces**:
  - **Web UI**: Modern chat interface built with **Streamlit**.
  - **CLI**: Fast terminal-based agent for testing and debugging.

## 🛠️ Installation

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/smart-hr-rag-agent.git
    cd smart-hr-rag-agent
    ```

2.  **Install Dependencies**:
    Requires Python 3.10+.

    ```bash
    pip install -r requirements.txt
    ```

3.  **Download Model**:
    The system uses `Llama-3.2-1B-Instruct-Q4_0.gguf`. Run the setup script to download it automatically:
    ```bash
    python download_model.py
    ```

## ▶️ Usage

### Web Interface (Recommended)

Launch the Streamlit app:

```bash
streamlit run app.py
# or double-click run_app.bat on Windows
```

### CLI Agent

Run the terminal agent:

```bash
python src/agent.py
# or double-click run_cli.bat on Windows
```

## 📂 Project Structure

- `src/`: Core logic (`agent.py`, `tools.py`, `llm_client.py`).
- `data/`:
  - `hr_policies/`: Place your PDF documents here.
  - `chroma_db/`: Vector database (auto-generated).
  - `models/`: Local LLM weights.
- `app.py`: Streamlit frontend.

## 🧠 Architecture

1.  **Ingestion**: PDFs are parsed and embedded using `sentence-transformers` into ChromaDB.
2.  **Query Handling**:
    - **Intent Classifier**: Determines if query is about HR, Chitchat, or General Knowledge.
    - **Retrieval**: Fetches relevant chunks from ChromaDB.
    - **Generation**: Llama 3 generates a response using the retrieved context.
3.  **Safety**:
    - **Hallucination Guard**: Sanitizes inputs (e.g., "hiii" -> "Hello") and uses aggressive stop tokens.
    - **Negation Logic**: Correctly handles "I am NOT asking about..." queries.

## 📄 License

MIT
