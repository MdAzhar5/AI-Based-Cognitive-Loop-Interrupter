import streamlit as st
from chains.master_chain import master_chain

# ---------- Page Config ----------
st.set_page_config(
    page_title="Agentic LangChain Assistant",
    page_icon="🧠",
    layout="centered",
)

st.title("🧠 Agentic AI Assistant")
st.caption("LangChain • Runnables • Ollama • Chroma Memory")

# ---------- User Identity ----------
with st.sidebar:
    st.header("User Identity")
    user_id = st.text_input(
        "Enter User ID",
        placeholder="email / phone / username",
    )

    if not user_id:
        st.warning("Please enter a User ID to start.")
        st.stop()

# ---------- Session State ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Chat History ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- User Input ----------
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Run Agentic Chain
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = master_chain.invoke(
                {
                    "user_id": user_id,
                    "input": user_input,
                }
            )
            st.markdown(response)

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
