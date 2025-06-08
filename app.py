import streamlit as st

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

# Encrypted dummy token (replace with your actual encrypted token)
encrypted_token = "lnymzg_ufy_11GGT6RVV0TeMmRXFEijJx_Wr0IJOWzdcjnAV5FL2e9YNY9zIOwvycvhdimJVjzrgRLX5VJNHHTltH9KWQ"
GITHUB_TOKEN = decrypt(encrypted_token, 3)

st.set_page_config(layout="wide")  # Wide layout to fit grid nicely

st.title("Encrypted Token Media Uploader 🔐📤")

# Top bar with upload button on right
upload_col1, upload_col2 = st.columns([9, 1])
with upload_col2:
    uploaded_files = st.file_uploader(
        "Upload",
        accept_multiple_files=True,
        type=["png", "jpg", "jpeg", "gif", "mp4", "svg", "webp", "mov", "avi", "mkv", "bmp", "tiff"],
        key="file_uploader",
    )

# Container for media grid
if 'media_list' not in st.session_state:
    st.session_state.media_list = []

if uploaded_files:
    st.session_state.media_list.extend(uploaded_files)

media_list = st.session_state.media_list

if media_list:
    st.write(f"Showing {len(media_list)} uploaded file(s):")

    # Display in grid 5 per row
    cols = st.columns(5)
    for idx, file in enumerate(media_list):
        col = cols[idx % 5]
        with col:
            st.markdown(f"**{file.name}**")
            if file.type.startswith("image/"):
                st.image(file, use_column_width=True)
            elif file.type.startswith("video/"):
                st.video(file)
            else:
                st.write("No preview")

else:
    st.write("No media uploaded yet. Use the upload button on top-right 👆")

