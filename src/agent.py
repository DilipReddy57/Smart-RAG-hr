from llm_client import get_llm
from tools import RAGTools
import re

class HRAgent:
    def __init__(self):
        self.llm = get_llm()
        self.tools = RAGTools()
        self.categories = [
            "leave_policy",
            "reimbursement",
            "onboarding",
            "offboarding",
            "performance",
            "code_of_conduct",
            "grievance_safety",
            "general_hr_info",
            "salary_policy",
            "compliance_policy",
            "welfare_benefits",
            "general_knowledge"
        ]

    def classify_intent(self, query, history=[]):
        # 1. Regex Overrides for Greetings (Robust Chitchat)
        # Match greetings at start, or specific keywords anywhere
        chat_pattern = r"^(h+i+|h+e+y+a?|h+e+l+o+|good\s*(morning|evening|afternoon)|who\s+are\s+you|what\s+is\s+your\s+name|help)|(\b(thanks?|joke)\b)"
        if re.search(chat_pattern, query.lower()):
            return "chitchat"
        
        # 2. Keyword Overrides
        q_lower = query.lower()
        
        # Explicit Negation Handler (e.g. "Not asking about leave")
        if re.search(r"\bnot\s+(asking|related|need|want)\b", q_lower):
            if "hi" in q_lower or "hello" in q_lower: 
                return "chitchat"
            return "general_hr_info"
            
        if "salary" in q_lower or "ctc" in q_lower or "payslip" in q_lower or "tax" in q_lower or "pf" in q_lower or "bonus" in q_lower: return "salary_policy"
        if "compliance" in q_lower or "prevention" in q_lower or "act" in q_lower or "legal" in q_lower: return "compliance_policy"
        if "welfare" in q_lower or "insurance" in q_lower or "gym" in q_lower or "women" in q_lower or "baby" in q_lower or "paternity" in q_lower: return "welfare_benefits"
        if "maternity" in q_lower: return "welfare_benefits"
        if "safety" in q_lower or "harassment" in q_lower: return "grievance_safety"
        
        # Robust Overrides for core categories 
        # Check for negations (e.g. "not related to leave")
        # Use regex to match whole words only to avoid matching "notice", "nothing", etc.
        is_negative = re.search(r"\b(not|don't|no|never)\b", q_lower)
        
        if not is_negative:
            if "leave" in q_lower or "sick" in q_lower or "casual" in q_lower or "vacation" in q_lower: return "leave_policy"
            # reimbursement overrides
            if "expense" in q_lower or "reimburse" in q_lower or "claim" in q_lower or "travel" in q_lower: return "reimbursement"
            if "notice" in q_lower or "resign" in q_lower or "exit" in q_lower or "terminate" in q_lower or "fired" in q_lower: return "offboarding"
            if "onboarding" in q_lower or "joining" in q_lower or "induction" in q_lower: return "onboarding"
            
        if "freelance" in q_lower or "conduct" in q_lower or "ethics" in q_lower: return "code_of_conduct"
        
        # General Knowledge Overrides for known nonsense/fact patterns
        if any(w in q_lower for w in ["apple", "sky", "sun", "moon", "president", "capital", "weather", "color", "pasta", "mars", "earth", "math", "history"]):
             return "general_knowledge"

        # 3. Context-Aware Classification via LLM
        context_str = ""
        if history:
            last_turns = history[-2:] if len(history) >= 2 else history
            context_str = "\nConversation History:\n"
            for msg in last_turns:
                 role = "User" if msg['role'] == 'user' else "Assistant"
                 content = msg['content'][:100] # truncate
                 context_str += f"{role}: {content}\n"
        
        messages = [
            {"role": "user", "content": f"""You are a classification model.
Available categories:
- leave_policy
- reimbursement
- onboarding
- offboarding
- performance
- code_of_conduct
- grievance_safety
- salary_policy
- compliance_policy
- welfare_benefits
- general_hr_info
- chitchat
- general_knowledge

{context_str}
Current Query: "{query}"

Task: Classify the Current Query into exactly one category.
- If it's about common sense, facts, or logic (e.g. "Sky color", "Math"), choose 'general_knowledge'.
- If it's general chat, choose 'chitchat'.
- If it's HR/Company Policy, choose specific category.

Output ONLY the category name."""}
        ]
        
        response = self.llm.chat(messages, max_tokens=20).strip().lower()
        
        # 4. Response Matching
        for cat in self.categories + ["chitchat"]:
            if cat in response:
                return cat
            
        # 5. Fuzzy matching
        if "leave" in response: return "leave_policy"
        if "claim" in response or "reimburse" in response: return "reimbursement"
        if "conduct" in response: return "code_of_conduct"
        if "knowledge" in response or "fact" in response: return "general_knowledge"
        
        return "general_hr_info"

    def handle_query(self, query, history=[]):
        print(f"Agent received query: {query}")
        intent = self.classify_intent(query, history)
        print(f"Detected Intent: {intent}")
        
        answer = ""
        sources = []

        if intent == "leave_policy":
            answer, sources = self.tools.lookup_leave_policy(query, history)
        elif intent == "reimbursement":
            answer, sources = self.tools.generate_reimbursement_checklist(query, history)
        elif intent == "onboarding":
            answer, sources = self.tools.lookup_onboarding_steps(query, history)
        elif intent == "offboarding":
            answer, sources = self.tools.lookup_offboarding_policy(query, history)
        elif intent == "performance":
            answer, sources = self.tools.summarize_performance_guidelines(query, history)
        elif intent == "code_of_conduct":
            answer, sources = self.tools.extract_conduct_rule(query, history)
        elif intent == "grievance_safety":
            answer, sources = self.tools.grievance_and_safety_steps(query, history)
        elif intent == "salary_policy":
            answer, sources = self.tools.lookup_salary_policy(query, history)
        elif intent == "compliance_policy":
            answer, sources = self.tools.lookup_compliance_policy(query, history)
        elif intent == "welfare_benefits":
            answer, sources = self.tools.lookup_welfare_benefits(query, history)
        elif intent == "chitchat":
            answer, sources = self.tools.handle_chitchat(query, history)
        elif intent == "general_knowledge":
            answer, sources = self.tools.handle_general_knowledge(query, history)
        else:
            answer, sources = self.tools.generic_rag_answer(query, history)
            
        return {
            "intent": intent,
            "answer": answer,
            "sources": sources
        }

if __name__ == "__main__":
    import sys
    
    print("\n------------------------------------------------")
    print("      Offline HR Policy Assistant (CLI)      ")
    print("------------------------------------------------")
    print("System initializing... Both Llama-3 and Vectors are loading...")
    
    try:
        agent = HRAgent()
        history = []
        
        print("\n" + "="*50)
        print("🤖  OFFLINE HR ASSISTANT READY")
        print("="*50)
        print("I can help you with:")
        print(" - Leave Policies (Sick, Casual, Earned)")
        print(" - Reimbursements & Travel Claims")
        print(" - Onboarding & Offboarding")
        print(" - Code of Conduct & Ethics")
        print("\nTry asking: 'How many sick leaves do I get?'")
        print("Type 'exit' to quit.\n")
        
        while True:
            try:
                q = input("Ask HR > ").strip()
                if not q:
                    continue
                if q.lower() in ['exit', 'quit']:
                    print("Goodbye!")
                    break
                    
                result = agent.handle_query(q, history)
                
                print(f"\n>> Intent: {result['intent']}")
                print(f"\n{result['answer']}\n")
                if result['sources']:
                    print("--- Sources ---")
                    for s in result['sources']:
                        print(f"- {s}")
                print("\n" + "-"*40 + "\n")
                
                # Append to history
                history.append({"role": "user", "content": q})
                history.append({"role": "assistant", "content": result['answer']})
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}\n")
                
    except Exception as e:
        print(f"\nCritical Error during initialization: {e}")
        input("Press Enter to exit...")
