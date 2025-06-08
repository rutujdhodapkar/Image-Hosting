import streamlit as st
import base64
import requests

# Caesar cipher encrypt/decrypt for token
def encrypt(text, shift=3):
    result = ""
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            result += char
    return result

def decrypt(text, shift=3):
    return encrypt(text, -shift)

# Replace with your encrypted GitHub token (shift 3)
encrypted_token = "lnymzg_ufy_11GGT6RVV0TeMmRXFEijJx_Wr0IJOWzdcjnAV5FL2e9YNY9zIOwvycvhdimJVjzrgRLX5VJNHHTltH9KWQ"
GITHUB_TOKEN = decrypt(encrypted_token, 3)

# Your repo info
GITHUB_USER = "rutujdhodapkar"  # Your GitHub username
REPO_NAME = "Image-Hosting"     # Repo where you want to upload
BRANCH = "main"                  # Branch to push files to

st.set_page_config(layout="wide")
st.title("Upload Images to GitHub Repo via Encrypted Token 🔐📤")

# Upload button on top-right
_, upload_col = st.columns([9, 1])
with upload_col:
    uploaded_files = st.file_uploader(
        "Upload",
        accept_multiple_files=True,
        type=["png", "jpg", "jpeg", "gif", "svg", "webp", "bmp", "tiff"],
        key="file_uploader",
    )

if 'upload_results' not in st.session_state:
    st.session_state.upload_results = []

def upload_file_to_github(file, path_in_repo):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{path_in_repo}"

    # First, check if file already exists to get sha (required for update)
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    get_resp = requests.get(url, headers=headers)
    sha = None
    if get_resp.status_code == 200:
        sha = get_resp.json().get("sha")

    # Read file content & encode base64
    content = file.read()
    b64_content = base64.b64encode(content).decode()

    # Commit message
    message = f"Upload {file.name} via Streamlit app"

    data = {
        "message": message,
        "content": b64_content,
        "branch": BRANCH,
    }
    if sha:
        data["sha"] = sha

    resp = requests.put(url, headers=headers, json=data)
    if resp.status_code in [200, 201]:
        return True, f"Uploaded {file.name} successfully."
    else:
        return False, f"Failed to upload {file.name}: {resp.text}"

if uploaded_files:
    st.session_state.upload_results = []  # reset results

    for file in uploaded_files:
        # Save in folder 'uploads' inside repo to keep it clean
        path_in_repo = f"uploads/{file.name}"
        success, msg = upload_file_to_github(file, path_in_repo)
        st.session_state.upload_results.append(msg)

for result in st.session_state.upload_results:
    st.write(result)

# Show all images uploaded in this session as grid
if uploaded_files:
    st.write(f"Uploaded {len(uploaded_files)} file(s):")
    cols = st.columns(5)
    for idx, file in enumerate(uploaded_files):
        col = cols[idx % 5]
        with col:
            st.image(file, use_column_width=True)

else:
    st.write("No images uploaded yet. Use the upload button on top-right 👆")
