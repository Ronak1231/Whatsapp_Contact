from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to ChromeDriver
CHROMEDRIVER_PATH = r"C:\Users\91982\Desktop\Python\Messages_Project\chromedriver.exe"

# Chrome options
chrome_options = Options()
chrome_options.add_argument(r"user-data-dir=C:\Users\91982\Desktop\Python\Messages_Project\selenium_chrome_profile")
chrome_options.add_argument("--disable-dev-shm-usage")

# Launch Chrome
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com/")
print("🔄 Waiting for WhatsApp Web to load...")

# Wait for QR scan or chat box
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "canvas[aria-label='Scan me!'], div[role='textbox']"))
)
print("✅ WhatsApp Web loaded.")

# User input
search_term = input("🔎 Enter a name to search (group/contact): ")
message = input("💬 Enter the message to send: ")

try:
    # Wait and locate search input
    search_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Search input textbox' and @contenteditable='true']"))
    )
    search_input.click()
    search_input.clear()
    search_input.send_keys(search_term)
    time.sleep(2)

    # Get list of search result items
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
        choice = int(input("\n🟢 Enter the number of the chat to send message to: ")) - 1

        if 0 <= choice < len(chat_options):
            selected_title, selected_element = chat_options[choice]
            selected_element.click()
            print(f"✅ Opened chat: {selected_title}")
            time.sleep(2)

            # Locate the message box and send message
            message_box = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Type a message' and @contenteditable='true']"))
            )
            message_box.click()
            message_box.send_keys(message)
            time.sleep(1)
            message_box.send_keys("\n")
            print(f"✅ Message sent to {selected_title}: {message}")
        else:
            print("❌ Invalid selection.")

except Exception as e:
    print("❌ Error:", e)

input("🔚 Press Enter to close the browser...")
driver.quit()
