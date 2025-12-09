from datetime import datetime
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import os
from llm_client import get_llm

# Config
CHROMA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'chroma_db')
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'

class RAGTools:
    def __init__(self):
        self.embedding_func = self._get_embedding_func()
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = self.client.get_or_create_collection(
            name="hr_policies",
            embedding_function=self.embedding_func
        )
        self.llm = get_llm()

    def _get_embedding_func(self):
        class LocalEmbeddingFunction(chromadb.EmbeddingFunction):
            def __init__(self, model_name):
                self.model = SentenceTransformer(model_name)
            def __call__(self, input):
                return self.model.encode(input).tolist()
        return LocalEmbeddingFunction(EMBEDDING_MODEL_NAME)

    def _retrieve(self, query, category=None, k=3):
        where_filter = {"category": category} if category else None
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=k,
                where=where_filter
            )
        except Exception as e:
            print(f"Retrieval Error: {e}")
            # Fallback without filter if filter fails (e.g. wrong category name)
            if category:
                print("Retrying without category filter...")
                return self._retrieve(query, category=None, k=k)
            return "", []
        
        chunks = []
        sources = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i]
                chunks.append(doc)
                sources.append(f"{meta.get('source', 'Unknown')} (Category: {meta.get('category', 'N/A')})")
        
        return "\n\n".join(chunks), sources

    def _generate_response(self, system_prompt, user_query, context, history=[]):
        # Build messages with history
        messages = [{"role": "system", "content": f"{system_prompt}\n\nCONTEXT FROM POLICIES:\n{context}"}]
        
        # Add recent history (last 2 turns to save tokens)
        for msg in history[-2:]:
            messages.append(msg)
            
        messages.append({"role": "user", "content": user_query})
        
        return self.llm.chat(messages)

    # --- Tools ---

    def handle_chitchat(self, query, history=[]):
        # Sanitize "hiii", "heya", etc to standard "Hello" to prevent LLM hallucination
        import re
        if re.search(r"^(h+i+|h+e+y+a?|h+e+l+o+|who\s+are\s+you|help)$", query.lower().strip()):
             sanitized_query = "Hello"
        else:
             sanitized_query = query
        
        messages = [{"role": "system", "content": "You are a helpful and friendly HR Assistant. Answer questions politely. If the user asks about specific policies, suggest they ask that directly."}]
        for msg in history[-2:]:
            messages.append(msg)
        messages.append({"role": "user", "content": sanitized_query})
        return self.llm.chat(messages), []

    def handle_general_knowledge(self, query, history=[]):
        # Direct LLM call without RAG context to avoid HR hallucinations
        messages = [{"role": "system", "content": "You are a helpful assistant. Answer the user's general knowledge or logic question directly and concisely. Do NOT mention HR policies or corporate context unless explicitly asked."}]
        for msg in history[-2:]:
            messages.append(msg)
        messages.append({"role": "user", "content": query})
        return self.llm.chat(messages), []

    def lookup_leave_policy(self, query, history=[]):
        context, sources = self._retrieve(query, category="leave")
        prompt = """Role: HR policy assistant.
Provide a short answer plus key points and conditions.
Include types of leave, eligibility, documents, limitations.
Format:
- Summary
- Rules list
- Important conditions
- Source references"""
        answer = self._generate_response(prompt, query, context, history)
        return answer, sources

    def generate_reimbursement_checklist(self, query, history=[]):
        context, sources = self._retrieve(query, category="reimbursement")
        prompt = """Extract required documents, steps in order, and approval flow.
Output Format:
### Documents required
...
### Step by step process
...
### Approvals
..."""
        answer = self._generate_response(prompt, query, context, history)
        return answer, sources

    def lookup_onboarding_steps(self, query, history=[]):
        context, sources = self._retrieve(query, category="onboarding")
        prompt = """Extract Pre joining requirements, Day 1 steps, and IT/HR tasks.
Output as a clear checklist."""
        answer = self._generate_response(prompt, query, context, history)
        return answer, sources

    def lookup_offboarding_policy(self, query, history=[]):
        context, sources = self._retrieve(query, category="offboarding")
        prompt = """Explain notice period rules, exit clearance checklist, and FNF timeline."""
        answer = self._generate_response(prompt, query, context, history)
        return answer, sources

    def summarize_performance_guidelines(self, query, history=[]):
        context, sources = self._retrieve(query, category="performance")
        prompt = """Summarize Appraisal cycle, Rating model, and Criteria."""
        answer = self._generate_response(prompt, query, context, history)
        return answer, sources

    def extract_conduct_rule(self, query, history=[]):
        context, sources = self._retrieve(query, category="code_of_conduct")
        prompt = """Answer with a clear Yes or No if possible, then cite the policy section."""
        answer = self._generate_response(prompt, query, context, history)
        return answer, sources

    def grievance_and_safety_steps(self, query, history=[]):
        context, sources = self._retrieve(query, category="grievance")
        prompt = """Explain how to report issues, contact points, and confidentiality rules."""
        answer = self._generate_response(prompt, query, context, history)
        return answer, sources

    def generic_rag_answer(self, query, history=[]):
        context, sources = self._retrieve(query) # No category filter
        prompt = """Answer the user question based on the context provided. If unsure, say so."""
        answer = self._generate_response(prompt, query, context, history)
        return answer, sources

    def lookup_salary_policy(self, query, history=[]):
        context, sources = self._retrieve(query, category="salary")
        prompt = """Role: HR Compensation Expert.
Explain salary components (Basic, HRA), deductions (PF, Tax), and payout cycle.
If asked about benefits, mention the flexible benefit plan."""
        answer = self._generate_response(prompt, query, context, history)
        return answer, sources

    def lookup_compliance_policy(self, query, history=[]):
        context, sources = self._retrieve(query, category="compliance")
        prompt = """Role: Corporate Governance Officer.
Explain the statutory framework, acts (Maternity, Minimum Wage), and Data Privacy (DPDP)."""
        answer = self._generate_response(prompt, query, context, history)
        return answer, sources

    def lookup_welfare_benefits(self, query, history=[]):
        context, sources = self._retrieve(query, category="welfare")
        prompt = """Role: HR Wellness Coordinator.
Explain insurance coverage (GHI, GPA), wellness benefits (Gym, EAP), and office perks."""
        answer = self._generate_response(prompt, query, context, history)
        return answer, sources
