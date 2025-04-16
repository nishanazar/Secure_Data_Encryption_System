import streamlit as st
import hashlib
import json
import os
from cryptography.fernet import Fernet


# Generate or load a key 
KEY_FILE = "secret.key"
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        KEY = f.read()
else:
    KEY = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(KEY)

cipher = Fernet(KEY)

# Load or initialize stored data
DATA_FILE = "data.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        stored_data = json.load(f)
else:
    stored_data = {}

# Track failed attempts
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

# Function to hash passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Function to encrypt data
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

# Function to decrypt data
def decrypt_data(encrypted_text):
    return cipher.decrypt(encrypted_text.encode()).decode()

# Save to JSON
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(stored_data, f)

# Streamlit UI
st.title("🔐 Secure Data Encryption System")

menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.radio("Navigation", menu)

if choice == "Home":
    st.subheader("🏠 Welcome to Secure Storage")
    st.write("Welcome to **Secure Storage**, your ultimate solution for keeping sensitive information safe.")
    st.write("This app allows you to **store and retrieve** sensitive information using a secure passkey.")
    
    # Adding a more interactive element
    st.markdown("""
        ## How It Works
        1. **Store Information:** Save your passwords, notes, or other sensitive data securely.
        2. **Retrieve Anytime:** Access your stored information at any time using your passkey.
        3. **Fully Encrypted:** Your data is encrypted and accessible only to you.
    """)

    # Optional: Adding a fun or motivational message
    st.write("🔒 **Your Data, Your Privacy, Your Control**")
    st.write("We believe in making data storage both secure and user-friendly.")
    
    # You could also add a nice image to enhance the page's visual appeal.
    st.image("https://www.wartsila.com/images/default-source/twentyfour7/master-images/cybersecurity-looks-to-the-cloud-to-protect-data-at-sea.tmb-1920x690.jpg?Culture=en&sfvrsn=d2e0ad44_3", caption="Secure Your Data, Secure Your Future")

    # Optional: Show features of the app
    st.markdown("""
        ### Features:
        - **Simple to Use**: Easy to store and retrieve information
        - **High-Level Security**: Encryption ensures your data is always safe
        - **User-Friendly Interface**: Designed to be intuitive and efficient
    """)


elif choice == "Store Data":
    st.subheader("📦 Store Your Secure Data")
    identifier = st.text_input("Unique Identifier (e.g. username or key):")
    user_data = st.text_area("Enter Data to Encrypt:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Encrypt & Store"):
        if identifier and user_data and passkey:
            hashed = hash_passkey(passkey)
            encrypted = encrypt_data(user_data)
            stored_data[identifier] = {"encrypted_text": encrypted, "passkey": hashed}
            save_data()
            st.success("✅ Data encrypted and saved successfully!")
        else:
            st.error("⚠️ Please fill in all fields.")

elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Stored Data")
    identifier = st.text_input("Enter Identifier:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Decrypt"):
        if identifier in stored_data:
            hashed = hash_passkey(passkey)
            if hashed == stored_data[identifier]["passkey"]:
                decrypted = decrypt_data(stored_data[identifier]["encrypted_text"])
                st.success(f"🔓 Decrypted Data: {decrypted}")
                st.session_state.failed_attempts = 0
            else:
                st.session_state.failed_attempts += 1
                st.error(f"❌ Incorrect passkey! Attempts left: {3 - st.session_state.failed_attempts}")
                if st.session_state.failed_attempts >= 3:
                    st.warning("🚫 Too many failed attempts. Please login again.")
                    st.experimental_rerun()
        else:
            st.error("❌ Identifier not found.")

elif choice == "Login":
    st.subheader("🔑 Reauthorize Access")
    master_key = st.text_input("Enter Master Password:", type="password")
    if st.button("Login"):
        if master_key == "admin123":  # Replace with secure method later
            st.session_state.failed_attempts = 0
            st.success("✅ Access granted. You may now retrieve data again.")
            st.rerun()
        else:
            st.error("❌ Incorrect master password.")
