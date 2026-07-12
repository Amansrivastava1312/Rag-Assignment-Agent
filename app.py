import streamlit as st
import time

from src.rag_pipeline import RagPipeLine

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"      # <-- sidebar open by default
)

# ==================================
# CSS
# ==================================

st.markdown("""
<style>

/* ---------- APP BACKGROUND ---------- */
.stApp{
    background: radial-gradient(circle at top, #0f1e3d 0%, #0B1120 60%);
    color:#E2E8F0;
}

/* Hide Streamlit chrome */
header, footer {visibility:hidden;}
#MainMenu {visibility:hidden;}

/* keep sidebar toggle button visible */
[data-testid="stSidebarCollapsedControl"]{
    visibility:visible !important;
    color:white !important;
}

/* ---------- CENTER CONTAINER ---------- */
.block-container{
    max-width:780px;
    margin:auto;
    padding-top:1rem;
    padding-bottom:120px;
}

/* ---------- TITLE ---------- */
.title{
    text-align:center;
    font-size:34px;
    font-weight:800;
    background:linear-gradient(90deg,#60A5FA,#A78BFA);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:25px;
}

/* ---------- USER MESSAGE (RIGHT) ---------- */
.user-container{
    display:flex;
    justify-content:flex-end;
    margin:10px 0;
}
.user-message{
    background:linear-gradient(135deg,#2563EB,#3B82F6);
    color:#ffffff;
    padding:12px 16px;
    border-radius:18px 18px 4px 18px;
    max-width:75%;
    font-size:15px;
    line-height:1.5;
    box-shadow:0 4px 12px rgba(37,99,235,0.35);
    word-wrap:break-word;
}

/* ---------- BOT MESSAGE (LEFT) ---------- */
.bot-container{
    display:flex;
    justify-content:flex-start;
    margin:10px 0;
}
.bot-message{
    background:#1E293B;
    color:#F1F5F9;
    padding:12px 16px;
    border-radius:18px 18px 18px 4px;
    max-width:75%;
    font-size:15px;
    line-height:1.5;
    border:1px solid #334155;
    box-shadow:0 4px 12px rgba(0,0,0,0.25);
    word-wrap:break-word;
}

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"]{
    background:#0d1526;
    border-right:1px solid #1e293b;
}

/* ---------- CHAT INPUT WRAPPER ---------- */
[data-testid="stChatInput"]{
    background:#0B1120 !important;
    border:none !important;
}

/* input box itself */
[data-testid="stChatInput"] > div{
    background:#1E293B !important;
    border:1px solid #334155 !important;
    border-radius:16px !important;
}

/* THE ACTUAL TEXT — force visible white */
[data-testid="stChatInput"] textarea{
    color:#FFFFFF !important;
    background:transparent !important;
    font-size:15px !important;
}
[data-testid="stChatInput"] textarea::placeholder{
    color:#94A3B8 !important;
}

/* send button */
[data-testid="stChatInput"] button{
    background:#2563EB !important;
    border-radius:12px !important;
}
[data-testid="stChatInput"] button:hover{
    background:#1D4ED8 !important;
}
[data-testid="stChatInput"] button svg{
    color:#ffffff !important;
    fill:#ffffff !important;
}

/* ---------- FIX BOTTOM WHITE AREA ---------- */
[data-testid="stBottom"]{
    background:#0B1120 !important;
}
[data-testid="stBottom"] > div{
    background:#0B1120 !important;
}
[data-testid="stBottomBlockContainer"]{
    background:#0B1120 !important;
}
.stChatFloatingInputContainer{
    background:#0B1120 !important;
}

/* scrollbar */
::-webkit-scrollbar{width:8px;}
::-webkit-scrollbar-track{background:#0B1120;}
::-webkit-scrollbar-thumb{background:#334155;border-radius:10px;}

</style>
""", unsafe_allow_html=True)

# ==================================
# LOAD RAG
# ==================================

@st.cache_resource
def initialize_rag():
    rg = RagPipeLine()
    if rg.check_db_exist():
        rg.load_db()
    else:
        rg.create_embedding()
    return rg

rg = initialize_rag()

# ==================================
# SIDEBAR
# ==================================

with st.sidebar:
    st.title("🤖 AI Assistant")
    st.markdown("---")
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown(
        """
        ### About
        Ask any question from your documents.

        **Powered By**
        - LangChain
        - ChromaDB
        - HuggingFace
        - Streamlit
        """
    )

# ==================================
# SESSION STATE
# ==================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================================
# TITLE
# ==================================

st.markdown(
    "<div class='title'>AI Document Assistant</div>",
    unsafe_allow_html=True
)

# ==================================
# WELCOME MESSAGE
# ==================================

if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="bot-container">
        <div class="bot-message">
            👋 Hello! How can I help you? Ask me about Python, ML, DL,
            MLOps, LLMs, SLMs, their evolution, architecture, and related AI topics.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================================
# CHAT HISTORY
# ==================================

for msg in st.session_state.messages:

    if msg["role"] == "user":
        st.markdown(
            f"""
            <div class="user-container">
                <div class="user-message">{msg["content"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="bot-container">
                <div class="bot-message">{msg["content"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==================================
# CHAT INPUT
# ==================================

question = st.chat_input("Ask anything from your documents...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )
    st.rerun()

# ==================================
# GENERATE RESPONSE
# ==================================

if (
    len(st.session_state.messages) > 0
    and st.session_state.messages[-1]["role"] == "user"
):
    latest_question = st.session_state.messages[-1]["content"]

    with st.spinner("🔍 Searching documents..."):
        answer = rg.ask_question(latest_question)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
    st.rerun()