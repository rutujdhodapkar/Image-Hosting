import streamlit as st
import requests
import base64
from datetime import datetime

# -------------- 🔐 DECRYPT TOKEN FUNCTION ------------------
def encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            result += char
    return result

def decrypt(cipher_text, shift):
    return encrypt(cipher_text, -shift)

# Encrypted GitHub token (Caesar +5)
encrypted_token = "lnymzg_ufy_11GGT6RVV0TeMmRXFEijJx_Wr0IJOWzdcjnAV5FL2e9YNY9zIOwvycvhdimJVjzrgRLX5VJNHHTltH9KWQ"
GITHUB_TOKEN = decrypt(encrypted_token, 5)

# Repo Info
OWNER = "rutujdhodapkar"
REPO = "Image-Hosting"
BRANCH = "main"
UPLOAD_PATH = ""  # root folder in repo

# ----------------- 🔼 FILE UPLOADER -----------------------
st.set_page_config(layout="wide")
st.markdown("## 🖼️ GitHub Image/Asset Hosting")

with st.sidebar:
    st.markdown("### Upload")
    uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        content = file.read()
        file_name = file.name
        upload_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{UPLOAD_PATH}{file_name}"
        encoded_content = base64.b64encode(content).decode()

        data = {
            "message": f"Upload {file_name} via Streamlit",
            "content": encoded_content,
            "branch": BRANCH
        }

        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        res = requests.put(upload_url, json=data, headers=headers)

        if res.status_code in [200, 201]:
            st.success(f"✅ Uploaded `{file_name}`")
        else:
            st.error(f"❌ Failed to upload `{file_name}`: {res.json().get('message')}")
            st.code(res.text)

# ----------------- 📸 SHOW FILES --------------------------

# Get list of files from repo root
def list_files():
    api_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{UPLOAD_PATH}?ref={BRANCH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    res = requests.get(api_url, headers=headers)

    if res.status_code == 200:
        return res.json()
    else:
        st.error("Failed to fetch file list.")
        st.code(res.text)
        return []

files = list_files()
if files:
    st.markdown("### 🗂️ Files in Repo")
    cols = st.columns(5)
    i = 0
    for file in files:
        if file["name"].lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".mp4", ".mov", ".webm")):
            with cols[i % 5]:
                if file["name"].lower().endswith((".mp4", ".mov", ".webm")):
                    st.video(file["download_url"])
                elif file["name"].lower().endswith(".svg"):
                    svg_html = f'<img src="{file["download_url"]}" width="100%" />'
                    st.markdown(svg_html, unsafe_allow_html=True)
                else:
                    st.image(file["download_url"], use_container_width=True)
            i += 1
