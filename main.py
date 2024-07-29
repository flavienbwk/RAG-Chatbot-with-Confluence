import os
import streamlit as st
from help_desk import HelpDesk

from config import FORCE_EMBEDDINGS_DB_RELOAD, COMPANY_NAME


@st.cache_resource
def get_model():
    model = HelpDesk(new_db=FORCE_EMBEDDINGS_DB_RELOAD)
    return model

if os.path.exists("logo.png"):
    brand_logo = "logo.png"
else:
    brand_logo = "brand.png"
st.set_page_config(page_title=f"Base de connaissance {COMPANY_NAME}", page_icon=brand_logo)

model = get_model()

col1, col2 = st.columns([6, 1])
with col1:
    st.title(f"Base de connaissance {COMPANY_NAME}")
with col2:
    st.image(brand_logo, width=64, use_column_width=True)
    st.write("")  # Add empty space to push the image up


with st.status("Informations d'usage"):
    st.info(
        "Bienvenue dans notre base de connaissances. Posez vos questions et notre assistant vous aidera à trouver les informations dont vous avez besoin. Les données utilisées sont celles de la documentation Confluence de l'entreprise.",
        icon="ℹ️",
    )
    st.warning(
        "Attention : ce moteur de recherche peut produire des explications inexactes (appelées hallucinations), veuillez vérifier les sources."
    )


if "messages" not in st.session_state:
    # Refer to https://platform.openai.com/docs/api-reference/chat/create
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": "Tu t'appelles Olivia OBLIGÉE et tu es une experte de l'assistance à l'analyse de documentation interne. Tu aides les employés à trouver de l'information dans la documentation Confluence de notre organisation. Quand tu penses ne pas savoir, il est important que tu le dises. Tu restes toujours respectueuse.",
        },
        {"role": "assistant", "content": "Comment puis-je vous aider ?"},
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"], avatar="confluence.png").write(msg["content"])


if prompt := st.chat_input("Comment puis-je vous aider ?"):
    # Add prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Get answer
    result, sources = model.retrieval_qa_inference(prompt, verbose=False)

    # Add answer and sources
    st.chat_message("assistant", avatar="confluence.png").write(
        result + "  \n  \n" + sources
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": result + "  \n  \n" + sources}
    )
