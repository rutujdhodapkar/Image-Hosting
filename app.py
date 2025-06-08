import streamlit as st
import base64

# Simple Caesar cipher encrypt/decrypt for token (shift 3 for example)
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

# Your GitHub token (encrypted here, replace with your actual token encrypted!)
# Example: 'ghp_1234567890abcdef' encrypted with shift 3
encrypted_token = "lnymzg_ufy_11GGT6RVV0TeMmRXFEijJx_Wr0IJOWzdcjnAV5FL2e9YNY9zIOwvycvhdimJVjzrgRLX5VJNHHTltH9KWQ"

# Decrypt the token to use internally
GITHUB_TOKEN = decrypt(encrypted_token, 3)

st.title("Encrypted Token Media Uploader 🔐📤")

# Show a message about token usage
st.write("Using an encrypted GitHub token (decrypted internally).")

# File uploader that accepts multiple file types including images, video, svg, webp
uploaded_files = st.file_uploader(
    "Upload images, videos, SVG, WebP, or other files",
    accept_multiple_files=True,
    type=["png", "jpg", "jpeg", "gif", "mp4", "svg", "webp", "mov", "avi", "mkv", "bmp", "tiff"],
)

if uploaded_files:
    st.write(f"Uploaded {len(uploaded_files)} file(s):")
    for uploaded_file in uploaded_files:
        file_details = {
            "filename": uploaded_file.name,
            "filetype": uploaded_file.type,
            "filesize": uploaded_file.size,
        }
        st.write(file_details)

        # Show images & videos inline if possible
        if uploaded_file.type.startswith("image/"):
            st.image(uploaded_file)
        elif uploaded_file.type.startswith("video/"):
            st.video(uploaded_file)
        else:
            st.write("Preview not supported for this file type.")

# Dummy: You can add your GitHub API usage here using GITHUB_TOKEN if you want to upload the files to a repo or gist.

