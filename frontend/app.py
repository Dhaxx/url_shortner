import os

import requests
import streamlit as st

# ===========================
# Configurações
# ===========================

API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000"
)

st.set_page_config(
    page_title="URL Shortener",
    page_icon="🔗",
    layout="centered",
)

# ===========================
# Session State
# ===========================

if "short_url" not in st.session_state:
    st.session_state.short_url = None

# ===========================
# Modal
# ===========================

@st.dialog("✅ URL encurtada com sucesso!")
def show_result():
    st.write("Copie o link abaixo:")

    st.code(
        st.session_state.short_url,
        language=None,
    )

    st.info(
        "Clique no ícone de copiar no canto superior direito do campo acima."
    )

# ===========================
# Interface
# ===========================

st.title("🔗 URL Shortener")

st.write(
    "Cole uma URL abaixo para gerar um link temporário."
)

url = st.text_input(
    "URL",
    placeholder="https://www.google.com",
)

# ===========================
# Botão
# ===========================

if st.button(
    "🚀 Encurtar URL",
    use_container_width=True,
):

    if not url.strip():
        st.warning("Informe uma URL.")
        st.stop()

    try:

        response = requests.post(
            f"{API_URL}/shorten",
            json={
                "url": url
            },
            timeout=10,
        )

        if response.status_code in (200, 201):

            data = response.json()

            st.session_state.short_url = data["short_url"]

            show_result()

        else:

            try:
                detail = response.json()["detail"]
            except Exception:
                detail = response.text

            st.error(detail)

    except requests.exceptions.ConnectionError:

        st.error(
            "Não foi possível conectar à API."
        )

    except requests.exceptions.Timeout:

        st.error(
            "Tempo de conexão com a API excedido."
        )

    except Exception as exc:

        st.error(str(exc))