import streamlit as st
import pandas as pd
import time
import re
import io
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Setup ---
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

def clean_non_bmp(text):
    return ''.join(c if ord(c) <= 0xFFFF else '' for c in text)

def extract_members(driver, group_name):
    st.info("Opening WhatsApp Web and waiting for load...")
    driver.get("https://web.whatsapp.com/")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "canvas[aria-label='Scan me!'], div[role='textbox']"))
    )

    # Search group
    search_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Search input textbox' and @contenteditable='true']"))
    )
    search_input.clear()
    search_input.send_keys(group_name)
    time.sleep(2)

    results = WebDriverWait(driver, 10).until(
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

    time.sleep(1)
    try:
        chat_header = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//header//div[@role='button']"))
        )
        chat_header.click()
    except:
        st.warning("Could not open profile panel.")
        return None

    try:
        members_container = WebDriverWait(driver, 7).until(
            EC.element_to_be_clickable((By.XPATH,
                "//div[contains(@class, 'x12lumcd') and .//div[contains(text(), 'members')]]"
            ))
        )
        members_container.click()
    except:
        st.warning("Could not open members list.")
        return None

    # Scroll through members
    scroll_box_xpath = "//div[@aria-label='Group info']//div[@role='list']"
    scroll_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, scroll_box_xpath))
    )

    last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)
    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
        time.sleep(1)
        new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)
        if new_height == last_height:
            break
        last_height = new_height

    member_elements = scroll_box.find_elements(By.XPATH, ".//div[contains(@class, '_ak72')]")
    data = []
    for member in member_elements:
        try:
            name = "None"
            number = "None"

            name_elements = member.find_elements(By.XPATH, ".//span[@dir='auto']")
            for el in name_elements:
                text = el.text.strip()
                if text and text.lower() != "you" and not re.match(r"^\+\d{1,}", text):
                    name = clean_non_bmp(text)
                    break

            number_elements = member.find_elements(By.XPATH, ".//div[@role='gridcell' and @aria-colindex='1']//span")
            for el in number_elements:
                text = el.text.strip()
                if re.match(r"^\+\d{1,}", text):
                    number = clean_non_bmp(text)
                    break

            if name == "None" and number != "None":
                name = number

            if name.lower() != "you" and (name != "None" or number != "None"):
                data.append({"Name": name, "Number": number})
        except:
            continue

    return pd.DataFrame(data).drop_duplicates()

# --- Streamlit UI ---
st.set_page_config(page_title="WhatsApp Group Member Extractor", layout="centered")
st.title("📥 WhatsApp Group Member Extractor")

with st.expander("ℹ️ Instructions", expanded=True):
    st.markdown("""
        - Make sure you're **logged in to WhatsApp Web** on Chrome with the same profile path.
        - This app opens Chrome and loads your profile to access WhatsApp group info.
        - Group names must match or partially match.
    """)

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
