from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import streamlit as st
import io

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

    # Wait for a few seconds to ensure the group is fully loaded
    time.sleep(5)  # Adjust the wait time as necessary

    # Extract members directly from the span
    try:
        members_span = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'selectable-text copyable-text')]"))
        )
        members_text = members_span.get_attribute("title")
        members_list = members_text.split(", ")
        
        # Prepare data for DataFrame with only numbers
        data = []
        for member in members_list:
            if member.startswith("+"):  # Assuming numbers start with '+'
                data.append({"Number": member})

        return pd.DataFrame(data).drop_duplicates()

    except Exception as e:
        st.warning(f"Error extracting members: {e}")
        return None

# --- Streamlit App UI ---
st.set_page_config(page_title="WhatsApp Group Member Extractor", layout="centered")
st.title("\U0001F4E5 WhatsApp Group Member Extractor")

with st.expander("\u2139\ufe0f Instructions", expanded=True):
    st.markdown("""
        - Make sure you're **logged in to WhatsApp Web** on Chrome with the same profile path.
        - This app opens Chrome and loads your profile to access WhatsApp group info.
        - Group names must match or partially match.
    """)

group_name = st.text_input("\U0001F50D Enter WhatsApp Group Name")
if st.button("\U0001F680 Extract Members") and group_name:
    with st.spinner("Launching browser and extracting data..."):
        driver = start_browser()
        df = extract_members(driver, group_name)
        if df is not None and not df.empty:
            st.success("\u2705 Member list extracted!")
            st.dataframe(df)
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False)
            st.download_button(
                label="\U0001F4E5 Download as Excel",
                data=excel_buffer.getvalue(),
                file_name=f"{group_name} members.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("\u274C No members extracted or group not found.")
