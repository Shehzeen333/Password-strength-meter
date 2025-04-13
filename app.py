import re
import streamlit as st
import random
import string
import json
import os

# Store last 10 used passwords to prevent reuse
password_history = []
password_file = "passwords.json"

# Load saved passwords
if os.path.exists(password_file):
    with open(password_file, "r") as f:
        password_history = json.load(f)

def save_password(password):
    password_history.append(password)
    if len(password_history) > 10:
        password_history.pop(0)
    with open(password_file, "w") as f:
        json.dump(password_history, f)

def clear_password_history():
    global password_history
    password_history = []
    with open(password_file, "w") as f:
        json.dump(password_history, f)

def generate_password(length):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choice(characters) for _ in range(length))

def check_password_strength(password, email):
    if password in password_history:
        return "❌ This password has been used before. Choose a new one.", []
    
    if email and password.lower() in email.lower():
        return "❌ Password should not contain your email.", []
    
    score = 0
    feedback = []
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    # Strength Rating
    if score == 4:
        save_password(password)
        return "✅ Strong Password!", []
    elif score == 3:
        return "⚠️ Moderate Password - Consider adding more security features.", feedback
    else:
        return "❌ Weak Password - Improve it using the suggestions below.", feedback

# Streamlit App
st.title("🔐 Password Strength Meter")
st.write("Ensure your passwords are secure and strong! \n Enter a password to check its strength or generate a strong one.")


password = st.text_input("Enter your password:", type="password")

if password:
    strength, feedback = check_password_strength(password)
    st.subheader(strength)
    for msg in feedback:
        st.write(msg)

# Password Length Selection
st.subheader(" Select Password Length for Generate")
length_option = st.radio("Choose Length:", [5, 8, 12, "Custom"])
custom_length = 12
if length_option == "Custom":
    custom_length = st.number_input("Enter custom length:", min_value=4, max_value=32, value=12)
else:
    custom_length = length_option

if st.button("Generate  Password"):
    st.session_state["generated_password"] = generate_password(custom_length)
    save_password(st.session_state["generated_password"])

# **Clipboard-Friendly Password Display (Works on Streamlit Cloud)**
generated_password = st.session_state.get("generated_password", "")
if generated_password:
    st.text_input("Generated Password (Copy it manually):", value=generated_password, key="generated_password_display")

# Sidebar for password history
st.sidebar.title("🔑 Password History")
if password_history:
    for idx, past_password in enumerate(password_history[::-1]):
        st.sidebar.write(f"{idx+1}. {past_password}")
    if st.sidebar.button("Clear History"):
        clear_password_history()
        st.sidebar.success("✅ Password history cleared!")
else:
    st.sidebar.write("No password history yet.")

# Footer
st.markdown("---")
st.markdown("🔒 Keep your passwords unique and secure. Never reuse old passwords!")
st.markdown("""
    <hr>
    <p style='text-align: center; color: gray;'>© 2025 Password Strength Meter |Created  ❤️ by Shahzeen</p>
""", unsafe_allow_html=True)