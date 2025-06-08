import streamlit as st
from cryptography.fernet import Fernet
from PIL import Image
import io

# -----------------------------
# 🔐 ENCRYPTED TOKEN SECTION
# -----------------------------
ENCRYPTED_TOKEN = b'gAAAAABmAegTLH6-s6Hk5NjHtCG6ZNi35vv0mhgXKTyE21bBmvWVLUyGjLvz7mvnQF6lvNexV0yy4s6x2c_jgZAg0kOIFv5ZDAyKnIWq4GXi7tzX7Zpu4tk='
FERNET_KEY = b'N1N3FtvMfDdv20dAr9l2gWnEwJEr8ADJ1e_RH4DFe8g='

try:
    decrypted_token = Fernet(FERNET_KEY).decrypt(ENCRYPTED_TOKEN).decode()
except Exception as e:
    st.error("❌ Failed to decrypt token.")
    st.stop()

# -----------------------------
# 📤 Upload + View Media
# -----------------------------
st.set_page_config(page_title="📂 Media Uploader", layout="centered")
st.title("🖼️ Upload + Preview Media")
st.caption("Supports: JPG, PNG, SVG, GIF, MP4, MOV, WebM")

file = st.file_uploader("🎯 Drop your file here", type=["jpg", "jpeg", "png", "gif", "svg", "mp4", "webm", "mov"])

if file:
    file_type = file.type
    content = file.read()

    st.subheader("👀 Preview:")

    if "image" in file_type:
        if file_type == "image/svg+xml":
            svg = content.decode("utf-8")
            st.components.v1.html(svg, height=400)
        else:
            img = Image.open(io.BytesIO(content))
            st.image(img, use_column_width=True)

    elif "video" in file_type:
        st.video(content)

    else:
        st.warning("⚠️ Unsupported file type")

# -----------------------------
# (Optional) Show decrypted token (for dev only)
# -----------------------------
with st.expander("🔐 Show decrypted token (for debugging)", expanded=False):
    st.code(decrypted_token, language="text")
