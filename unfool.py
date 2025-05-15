import streamlit as st
import zipfile
import os
import tempfile
from bs4 import BeautifulSoup

st.title("🔍 Kita cek siapa nih yg belum follback Instagram :v")

uploaded_file = st.file_uploader("Upload file ZIP nya dimari", type="zip")

def extract_usernames_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        links = soup.find_all("a")
        usernames = set()
        for link in links:
            href = link.get("href")
            if href and href.startswith("https://www.instagram.com/"):
                username = href.replace("https://www.instagram.com/", "").strip("/")
                usernames.add(username)
        return usernames

if uploaded_file is not None:
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "data.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        target_dir = None
        for root, dirs, files in os.walk(temp_dir):
            if "followers_1.html" in files and "following.html" in files:
                target_dir = root
                break

        if not target_dir:
            st.error("❌ Tidak ditemukan file followers_1.html atau following.html")
        else:
            followers_path = os.path.join(target_dir, "followers_1.html")
            following_path = os.path.join(target_dir, "following.html")

            followers = extract_usernames_from_file(followers_path)
            following = extract_usernames_from_file(following_path)
            not_following_back = sorted(following - followers)

            if not_following_back:
                st.success(f"🔎 Ditemukan {len(not_following_back)} akun yang belum follow balik:")
                for username in not_following_back:
                    st.markdown(f"- [{username}](https://instagram.com/{username})")
            else:
                st.success("🎉 Semua sudah follback! GG!")

# Credit
st.markdown("---")
st.markdown("👨‍💻 Created by [budimanword](https://github.com/budimanword)")
st.markdown("📷 Jangan lupa follow juga: [arifbman_](https://instagram.com/arifbman_)")
st.markdown("🔍 Link Tutorial: [Klik disini](https://docs.google.com/document/d/1tKlQaotdzgQlsmNWAO3SlKIfg6TeGuKZZJKZxpmuIuk/edit?usp=sharing)")
