from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

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
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "canvas[aria-label='Scan me!'], div[role='textbox']"))
)
print("✅ WhatsApp Web loaded.")

while True:
    search_term = input("🔎 Enter a name to search (group/contact): ")
    try:
        # Search for contact
        search_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Search input textbox' and @contenteditable='true']"))
        )
        search_input.click()
        search_input.clear()
        search_input.send_keys(search_term)
        time.sleep(2)

        # Get search results
        results = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@role='listitem']"))
        )
        chat_options = []
        print(f"\n🔍 Found {len(results)} result(s):")
        for idx, item in enumerate(results):
            try:
                title_element = item.find_element(By.XPATH, ".//span[@dir='auto']")
                title = title_element.text.strip()
                chat_options.append((title, item))
                print(f"{idx + 1}. {title}")
            except:
                continue

        if not chat_options:
            print("❌ No matching chats found.")
        else:
            choice = int(input("\n🟢 Enter the number of the chat to open: ")) - 1
            if 0 <= choice < len(chat_options):
                selected_title, selected_element = chat_options[choice]
                selected_element.click()
                print(f"✅ Opened chat: {selected_title}")
                time.sleep(3)

                # --- Click Profile Info Header ---
                try:
                    chat_header = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, "//header//div[@role='button']"))
                    )
                    chat_header.click()
                    print("👤 Profile info panel opened.")
                    time.sleep(3)
                except Exception as e:
                    print("⚠️ Could not open profile panel:", e)

                # --- Click on Group Members container ---
                try:
                    members_container = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH,
                            "//div[contains(@class, 'x12lumcd') and .//div[contains(text(), 'members')]]"
                        ))
                    )
                    members_container.click()
                    print("👥 Group members container clicked and list opened.")
                    time.sleep(3)
                except Exception as e:
                    print("⚠️ Could not open group members list:", e)

                # --- Extract Group Members ---
                try:
                    print("⏳ Extracting group member names and numbers...")

                    # Wait for member elements to load
                    member_elements = WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.XPATH,
                            "//div[@role='button' and @tabindex='0' and descendant::span[@dir='auto']]"
                        ))
                    )

                    data = []
                    for member in member_elements:
                        try:
                            # Get all span texts with dir='auto' or 'ltr' inside the member element
                            spans = member.find_elements(By.XPATH, ".//span[@dir='auto' or @dir='ltr']")
                            texts = [s.text.strip() for s in spans if s.text.strip() != ""]

                            # Skip invalid entries (like "You" or date headers) or if too many texts found
                            if not texts or any(x.lower() == 'you' for x in texts) or len(texts) > 2:
                                continue

                            if len(texts) == 2:
                                name, number = texts[0], texts[1]
                            elif len(texts) == 1:
                                name = texts[0]
                                number = "N/A"
                            else:
                                continue

                            name = clean_non_bmp(name)
                            data.append({"Name": name, "Number": number})

                        except Exception as e:
                            print("⚠️ Skipping a member due to error:", e)

                    if data:
                        df = pd.DataFrame(data)
                        filename = f"group_members_{search_term.replace(' ', '_')}.xlsx"
                        df.drop_duplicates(inplace=True)
                        df.to_excel(filename, index=False)
                        print(f"✅ Saved member list to '{filename}'")
                    else:
                        print("❌ No valid members extracted.")

                except Exception as e:
                    print("❌ Error extracting members:", e)

                cont = input("🔚 Press Enter to close the browser or type 'yes' to keep it open: ")
                contin(cont)
            else:
                print("❌ Invalid selection.")
    except Exception as e:
        print("❌ Error:", e)
