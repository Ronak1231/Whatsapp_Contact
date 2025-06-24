import streamlit as st
import pandas as pd
import io
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

# ===================== SETUP DATABASE =====================
Base = declarative_base()
DATABASE_URL = "sqlite:///users.db"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

# ===================== STREAMLIT LOGIN SYSTEM =====================
def register_user(username, password):
    db = SessionLocal()
    hashed_pw = generate_password_hash(password)
    user = User(username=username, password=hashed_pw)
    try:
        db.add(user)
        db.commit()
        return True, "User registered successfully!"
    except IntegrityError:
        db.rollback()
        return False, "Username already exists."

def login_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return True
    return False

# ===================== SELENIUM EXTRACTOR =====================
CHROMEDRIVER_PATH = r"C:\Users\91982\Desktop\Python\Messages_Project\chromedriver.exe"
PROFILE_PATH = r"C:\Users\91982\Desktop\Python\Messages_Project\selenium_chrome_profile"

@st.cache_resource(show_spinner=False)
def start_browser():
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={PROFILE_PATH}")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def extract_members(driver, group_name):
    st.info("Opening WhatsApp Web and waiting for load...")
    driver.get("https://web.whatsapp.com/")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "canvas[aria-label='Scan me!'], div[role='textbox']"))
    )

    search_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Search input textbox' and @contenteditable='true']"))
    )
    search_input.clear()
    search_input.send_keys(group_name)
    time.sleep(2)

    results = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@role='listitem']"))
    )

    group_found = False
    for result in results:
        try:
            result_title = result.find_element(By.XPATH, ".//span[@dir='auto']").text.strip()
            if group_name.lower() in result_title.lower():
                result.click()
                group_found = True
                break
        except:
            continue

    if not group_found:
        st.error("Group not found. Try again.")
        return None

    time.sleep(5)
    try:
        members_span = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'selectable-text copyable-text')]"))
        )
        members_text = members_span.get_attribute("title")
        members_list = members_text.split(", ")

        data = []
        for member in members_list:
            if member.startswith("+"):
                data.append({"Number": member})

        return pd.DataFrame(data).drop_duplicates()
    except Exception as e:
        st.warning(f"Error extracting members: {e}")
        return None

# ===================== STREAMLIT APP =====================
st.set_page_config(page_title="WhatsApp Group Member Extractor", layout="centered")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("🔐 WhatsApp Extractor")

# ---- LOGIN / REGISTER FORM ----
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab1:
        login_username = st.text_input("Username")
        login_password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(login_username, login_password):
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.rerun()
            else:
                st.error("Invalid credentials.")

    with tab2:
        new_username = st.text_input("Create Username")
        new_password = st.text_input("Create Password", type="password")
        if st.button("Register"):
            success, message = register_user(new_username, new_password)
            if success:
                st.success(message)
            else:
                st.error(message)

# ---- MAIN APP ----
else:
    st.success(f"Welcome, {st.session_state.username}!")
    with st.expander("ℹ️ Instructions", expanded=True):
        st.markdown("""
            - ✅ Make sure you're **logged in to WhatsApp Web** on Chrome with the same profile path.
            - 💡 This app opens Chrome and loads your profile to access WhatsApp group info.
            - 🔍 Group names must match or partially match.
            - ⚠️ **Note:** If you're unable to extract members on the first try, please click **'🚀 Extract Members'** again.
        """, unsafe_allow_html=True)


    group_name = st.text_input("🔍 Enter WhatsApp Group Name")
    if st.button("🚀 Extract Members") and group_name:
        with st.spinner("Launching browser and extracting data..."):
            driver = start_browser()
            df = extract_members(driver, group_name)
            if df is not None and not df.empty:
                st.success("✅ Member list extracted!")
                st.dataframe(df)
                excel_buffer = io.BytesIO()
                df.to_excel(excel_buffer, index=False)
                st.download_button(
                    label="📥 Download as Excel",
                    data=excel_buffer.getvalue(),
                    file_name=f"{group_name}_members.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("❌ No members extracted or group not found.")

    st.button("🔓 Logout", on_click=lambda: st.session_state.update({"logged_in": False}))
