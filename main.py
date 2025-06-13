from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re

# --- Utility ---
def clean_non_bmp(text):
    return ''.join(c if ord(c) <= 0xFFFF else '' for c in text)

def contin(text):
    if text.strip().lower() == "yes":
        print("🟢 Browser will remain open.")
        return True
    elif text.strip().lower() == "no":
        driver.quit()
        print("🛑 Browser closed.")
        return False

# --- Chrome Setup ---
CHROMEDRIVER_PATH = r"C:\Users\91982\Desktop\Python\Messages_Project\chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument(r"user-data-dir=C:\Users\91982\Desktop\Python\Messages_Project\selenium_chrome_profile")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# --- Open WhatsApp ---
driver.get("https://web.whatsapp.com/")
print("🔄 Waiting for WhatsApp Web to load...")
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "canvas[aria-label='Scan me!'], div[role='textbox']"))
)
print("✅ WhatsApp Web loaded.")

a = True
while a:
    search_term = input("🔎 Enter a name to search (group/contact): ")
    try:
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Search input textbox' and @contenteditable='true']"))
        )
        search_input.clear()
        search_input.send_keys(search_term)

        time.sleep(2)
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@role='listitem']"))
        )

        chat_options = []
        print(f"\n🔍 Found {len(results)} result(s):")
        for idx in range(len(results)):
            try:
                fresh_results = driver.find_elements(By.XPATH, "//div[@role='listitem']")
                item = fresh_results[idx]
                title_elements = item.find_elements(By.XPATH, ".//span[@dir='auto']")
                title = next((t.text.strip() for t in title_elements if t.text.strip()), "Unknown Chat")
                chat_options.append((title, item))
                print(f"{idx + 1}. {title}")
            except Exception as e:
                print(f"⚠️ Could not extract title from result {idx + 1}: {e}")

        if not chat_options:
            print("❌ No matching chats found.")
            continue

        try:
            choice = int(input("\n🟢 Enter the number of the chat to open: ")) - 1
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")
            continue

        if 0 <= choice < len(chat_options):
            selected_title, selected_element = chat_options[choice]
            selected_element.click()
            print(f"✅ Opened chat: {selected_title}")
            time.sleep(1)

            try:
                chat_header = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//header//div[@role='button']"))
                )
                chat_header.click()
                print("👤 Profile info panel opened.")
            except Exception as e:
                print("⚠️ Could not open profile panel:", e)

            try:
                members_container = WebDriverWait(driver, 7).until(
                    EC.element_to_be_clickable((By.XPATH,
                        "//div[contains(@class, 'x12lumcd') and .//div[contains(text(), 'members')]]"
                    ))
                )
                members_container.click()
                print("👥 Group members list opened.")
            except Exception as e:
                print("⚠️ Could not open members list:", e)

            # --- Extract Group Members ---
            try:
                print("⏳ Scrolling and extracting group member names and numbers...")

                scroll_box_xpath = "//div[@aria-label='Group info']//div[@role='list']"
                scroll_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, scroll_box_xpath))
                )
                WebDriverWait(driver, 5).until(EC.visibility_of(scroll_box))

                last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)
                while True:
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
                    time.sleep(1)
                    new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)
                    if new_height == last_height:
                        break
                    last_height = new_height

                member_elements = scroll_box.find_elements(By.XPATH, ".//div[@role='button' and @tabindex='0']")
                print(f"🔢 Total members found (raw): {len(member_elements)}")
                data = []

                for idx, member in enumerate(member_elements, 1):
                    try:
                        spans = member.find_elements(By.XPATH, ".//span[@dir='auto']")
                        span_texts = [s.text.strip() for s in spans if s.text.strip()]
                        print(f"👤 Member {idx}: {span_texts}")  # Debug print

                        name, number = "None", "None"
                        for text in span_texts:
                            if re.match(r"^\+\d+", text):  # Phone number
                                number = text
                            elif text.lower() != "you":
                                name = text

                        name = clean_non_bmp(name)
                        number = clean_non_bmp(number)

                        if name.lower() == "you" or name == "None":
                            continue
                        data.append({"Name": name, "Number": number})
                    except Exception as e:
                        print(f"⚠️ Skipping member due to error: {e}")

                if data:
                    df = pd.DataFrame(data).drop_duplicates()
                    safe_term = re.sub(r'[^\w\d_]', '_', search_term.strip())
                    filename = f"group_members_{safe_term}.xlsx"
                    df.to_excel(filename, index=False)
                    print(f"✅ Saved to '{filename}'")
                else:
                    print("❌ No valid members extracted.")

            except Exception as e:
                print("❌ Error extracting members:", e)

    except Exception as e:
        print(f"❌ Error searching for chat: {e}")

    choice = input("\n❓ Keep browser open? Type 'yes' or 'no': ")
    a = contin(choice)
