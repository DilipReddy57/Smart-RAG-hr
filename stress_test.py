import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))

from src.agent import HRAgent
import time

def get_stress_test_questions():
    return [
        "Hiii", "Good morning", 
        "What is casual leave?", "How to claim travel expenses?", 
        "What is the notice period?", "Can I do freelance work?", 
        "Explain my salary structure", "What is the maternity leave policy?", 
        "Does apple color is blue?", "Sky is brown in color",
        "What is the capital of France?",
        "I am NOT asking about leave, just saying hi", 
        "Don't tell me about reimbursement, tell me about gym",
        "Who are you?", "Help me",
        "What is my bonus?", "What happens if I get fired?",
        "sky is brown is also chitchat not hr info"
    ]

def run_stress_test_logic(agent):
    questions = get_stress_test_questions()
    results = []
    history = []
    
    for i, q in enumerate(questions, 1):
        try:
            start = time.time()
            res = agent.handle_query(q, history)
            duration = time.time() - start
            
            results.append({
                "ID": i,
                "Question": q,
                "Intent": res['intent'],
                "Answer": res['answer'],
                "Duration": f"{duration:.2f}s"
            })
        except Exception as e:
            results.append({
                "ID": i,
                "Question": q,
                "Intent": "ERROR",
                "Answer": str(e),
                "Duration": "0s"
            })
    return results

def run_stress_test_cli():
    print("Initializing Agent...")
    try:
        agent = HRAgent()
        results = run_stress_test_logic(agent)
        
        print(f"\nRunning {len(results)} Question Stress Test...\n")
        print(f"{'ID':<3} | {'Question':<35} | {'Intent':<20} | {'Duration'}")
        print("-" * 80)
        
        for r in results:
            print(f"{r['ID']:<3} | {r['Question']:<35} | {r['Intent']:<20} | {r['Duration']}")
            
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    run_stress_test_cli()
