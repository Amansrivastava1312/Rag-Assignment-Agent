import json
import os
import streamlit as st
from src.rag_pipeline import RagPipeLine

st.set_page_config(page_title="Agentic RAG — Dev View", page_icon="🤖", layout="wide")

INTENT_LOG = "logs/intent_log.json"


def read_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


# ---------- init pipeline once ----------
if "rg" not in st.session_state:
    with st.spinner("Initializing RAG pipeline..."):
        rg = RagPipeLine()
        if not rg.check_db_exist():
            rg.create_embedding()
        else:
            rg.load_db()
        st.session_state.rg = rg
    st.session_state.messages = []
    st.session_state.last_plan = None

# ---------- layout: left dev panel | right chat ----------
dev, chat = st.columns([1, 1.4], gap="large")

# ================= LEFT: DEVELOPER WINDOW =================
with dev:
    st.markdown("### 🛠️ Developer Console")

    st.markdown("#### 🧭 Last Intent (LLM JSON)")
    if st.session_state.last_plan:
        st.json(st.session_state.last_plan)
    else:
        st.caption("Ask something to see the parsed intent here.")

    with st.expander("🧾 Intent Log (full history)", expanded=False):
        intents = read_json(INTENT_LOG)
        st.caption(f"{len(intents)} entries")
        st.json(intents[-10:] if intents else [])

    with st.expander("📁 Output Files", expanded=False):
        files = os.listdir("outputs") if os.path.exists("outputs") else []
        if files:
            for fn in sorted(files, reverse=True)[:10]:
                st.text(f"• {fn}")
        else:
            st.caption("No files exported yet.")

# ================= RIGHT: CHATBOT =================
with chat:
    st.markdown("### 🤖 AI Advisor Chatbot")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask about LLMs, SLMs, AI... (try 'explain LoRA as pdf and mail me')")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("🤖 thinking..."):
                plan, answer, file_path = st.session_state.rg.ask_question_agentic(question)
            st.markdown(answer)
            if file_path:
                st.success(f"📎 Exported: {os.path.basename(file_path)}")

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.last_plan = plan
        st.rerun()      # refresh dev panel with new logs