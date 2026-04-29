import streamlit as st 
import httpx
import os 

API_URL = os.getenv("API_URL","http://localhost:8000")

def layout():
    st.set_page_config(page_title="404 Brain Not found", page_icon="🧠")
    
    st.markdown("# 404 brain not found ")
    st.markdown("Ask me about onboarding")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hi! I am your onboarding copilot. Ask me anything about onboarding."
            }
        ]
    
    st.markdown(
    """
    <div style="
        background-color: #f5f5f7;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-top: 1rem;
        margin-bottom: 2rem;
    ">
        <h4 style="margin-bottom: 0.5rem;">Your AI onboarding copilot</h4>
        <p style="margin-bottom: 0;">
            Ask questions about team practices, code reviews, communication norms,
            rookie mistakes, and when to ask for help.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
    
    st.markdown("### Try Asking:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("🧑‍💻 **How do we do code reviews?**")
        st.markdown("⚠️ **What are common rookie mistakes?**")

    with col2:
        st.markdown("🟡 **When should I ask for help?**")
        st.markdown("💬 **How should I communicate with the team?**")
        
    st.divider()
    st.markdown("### Chat")
    
        
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    user_question = st.chat_input("Ask a question")        
    
    if user_question:
        st.session_state.messages.append(
            {"role": "user", "content": user_question}
            )
        
        with st.chat_message("user"):
            st.markdown(user_question)
            
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = httpx.post(
                    f"{API_URL}/ask", 
                    json={"question": user_question}, 
                    timeout=120
        )
                    response.raise_for_status()
                    data = response.json()
                
                    answer = data.get("answer", "I could not find an answer.")
                    sources = data.get("sources")
                
                    st.markdown(answer)
                
                    if sources:
                     with st.expander("Sources"):
                         for source in sources:
                             document_name = source.get("document_name", "Unknown document")
                             content_preview = source.get("content_preview", "")
                             
                             clean_preview = content_preview.replace("#", "").replace("\n", " ")
                             
                             st.markdown(f"**{document_name}**")
                             
                             if clean_preview:
                                 st.markdown(clean_preview[:300] + "...")
                                 
                                 st.divider()
                        
                    assistant_message = answer
                
                    if sources:
                        source_name = [
                            source.get("document_name","Unknown document")
                            for source in sources
                        ]
                        
                        assistant_message += "\n\n**Sources:**\n"
                        assistant_message +="\n".join(
                            [f"-{name}" for name in source_name]
                        )
                        
                    
                    st.session_state.messages.append(
                        {"role": "assistant", "content": assistant_message}
                )
                
                except httpx.RequestError:
                    error_message = "Colud not connect to the backend API."
                    st.error(error_message)
                    
                except httpx.HTTPStatusError:
                    error_message = "The backend returned an error"
                    st.error(error_message)
                    
        


if __name__ == "__main__":
    layout()
        
    