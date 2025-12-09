import streamlit as st
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# We import HRAgent inside the app to avoid loading it at module level 
# before streamlit runs, although it's fine.
# But good to cache the agent instance.

st.set_page_config(page_title="HR Policy Assistant", layout="wide")

@st.cache_resource
def get_agent():
    # Lazy import to speed up initial UI render
    from agent import HRAgent
    return HRAgent()

def main():
    st.title("🤖 Offline HR Policy Assistant")
    st.markdown("Ask questions about leaves, reimbursement, policies, and more.")

    # Sidebar
    st.sidebar.header("System Status")
    status_placeholder = st.sidebar.empty()
    
    # Check if agent is ready without blocking UI render immediately
    if "agent_ready" not in st.session_state:
        status_placeholder.info("⏳ Initializing AI Engine... Please wait.")
        try:
            get_agent()
            st.session_state.agent_ready = True
            status_placeholder.success("✅ System Ready (Local LLM Loaded)")
        except Exception as e:
            status_placeholder.error(f"❌ Error loading model: {e}")
    else:
        status_placeholder.success("✅ System Ready (Local LLM Loaded)")

    st.sidebar.markdown("---")
    st.sidebar.header("💡 What can I ask?")
    st.sidebar.markdown("""
    - **Leaves**: "How many sick leaves do I get?"
    - **Claims**: "What is the travel food allowance?"
    - **Salary**: "Explain my salary components."
    - **Compliance**: "What are the labor laws?"
    - **Welfare**: "Do we have gym reimbursement?"
    - **Offboarding**: "What is the notice period?"
    """)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hi! I'm your HR Policy Assistant. I can answer questions about **Leave, Reimbursement, Performance, and more**. \n\nWhat would you like to know?"}
        ]

    # --- DEV: Stress Test UI ---
    with st.sidebar.expander("🔧 Developer Diagnostics"):
        if st.button("Run Stress Test (10 Qs)"):
            with st.spinner("Running system evaluation..."):
                try:
                    import sys
                    sys.path.append(os.getcwd()) # Ensure path
                    from stress_test import run_stress_test_logic
                    
                    # Get agent instance
                    agent_instance = get_agent()
                    results = run_stress_test_logic(agent_instance)
                    st.session_state.stress_results = results
                    st.success("Test Complete!")
                except Exception as e:
                    st.error(f"Test failed: {e}")
    
    if "stress_results" in st.session_state:
        st.subheader("📊 System Verification Results")
        res_data = st.session_state.stress_results
        st.dataframe(res_data)
        if st.button("Close Results"):
            del st.session_state.stress_results
            st.rerun()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Type your question here..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            try:
                agent = get_agent()
                with st.spinner("Analyzing policies..."):
                    result = agent.handle_query(prompt, st.session_state.messages[:-1])
                
                response_text = result["answer"]
                intent = result["intent"]
                sources = result["sources"]
                
                # Show intent only for policy queries
                if intent != "chitchat":
                    st.markdown(f"*Detected Topic: `{intent}`*")
                
                st.markdown(response_text)
                
                # Only show sources if they exist
                if sources:
                    with st.expander("📚 View Policy Sources"):
                        for s in sources:
                            st.write(f"- {s}")
                
                # Add assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
