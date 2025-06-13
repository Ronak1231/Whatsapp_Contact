from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import google.generativeai as genai

# --- Gemini API Configuration ---
genai.configure(api_key="AIzaSyAMfhNHujEGHmLil682h7Q6bWuQpBTDawo")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Utility to clean non-BMP characters like emojis ---
def clean_non_bmp(text):
    return ''.join(c if ord(c) <= 0xFFFF else '' for c in text)

def contin(text):
    # --- Close Prompt ---
    if cont.strip().lower() == "yes":
        print("🟢 Browser will remain open.")
        return True
    elif(cont.strip().lower() == "no"):
        driver.quit()
        print("🛑 Browser closed.")
        return False


# --- Generate AI reply from last messages ---
def generate_reply_from_messages(messages):
    system_prompt = f"""You are a person named Ronak who speaks Hindi as well as English.
You are from India and you are a person talking with {search_term} . Talk casually and in a funny way.
You analyze chat history and answer.
Output should be the next chat response (text message only).
Do not start like this [21:02, 12/6/2024] {search_term}:
"""
    chat_history = "\n".join(messages)
    try:
        response = model.generate_content([system_prompt, chat_history])
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini API Error:", e)
        return "😅 Arre kuch gadbad ho gayi Gemini ke saath!"

# --- Setup ChromeDriver Path ---
CHROMEDRIVER_PATH = r"C:\Users\91982\Desktop\Python\Messages_Project\chromedriver.exe"

# --- Chrome Options ---
chrome_options = Options()
chrome_options.add_argument(r"user-data-dir=C:\Users\91982\Desktop\Python\Messages_Project\selenium_chrome_profile")
chrome_options.add_argument("--disable-dev-shm-usage")

# --- Launch Chrome ---
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# --- Open WhatsApp Web ---
driver.get("https://web.whatsapp.com/")
print("🔄 Waiting for WhatsApp Web to load...")

WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "canvas[aria-label='Scan me!'], div[role='textbox']"))
)
print("✅ WhatsApp Web loaded.")

while (True):

    # --- Search and Select Chat ---
    search_term = input("🔎 Enter a name to search (group/contact): ")

    try:
        search_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Search input textbox' and @contenteditable='true']"))
        )
        search_input.click()
        search_input.clear()
        search_input.send_keys(search_term)
        time.sleep(2)

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

                # --- Extract Messages ---
                messages_elements = driver.find_elements(By.CSS_SELECTOR, "div.copyable-text")
                all_texts = [msg.text.strip() for msg in messages_elements if msg.text.strip()]
                last_10_msgs = all_texts[-10:] if len(all_texts) >= 10 else all_texts

                print("\n📝 Last 10 messages from chat:")
                for msg in last_10_msgs:
                    print("-", msg)

                # --- Generate and Clean Reply ---
                reply_text = generate_reply_from_messages(last_10_msgs)
                print(f"\n🤖 Original reply:\n{reply_text}")

                cleaned_reply = clean_non_bmp(reply_text)
                print(f"\n🧹 Cleaned reply (for ChromeDriver):\n{cleaned_reply}")

                # --- Send Reply ---
                message_box = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Type a message' and @contenteditable='true']"))
                )
                message_box.click()
                time.sleep(0.5)
                message_box.send_keys(Keys.CONTROL + "a")
                message_box.send_keys(Keys.BACKSPACE)

                message_box.send_keys(cleaned_reply)
                time.sleep(0.5)
                message_box.send_keys("\n")
                print(f"✅ Reply sent to {selected_title}")

                cont = input("🔚 Press Enter to close the browser or type 'yes' to keep it open: ")

                contin(cont)

            else:
                print("❌ Invalid selection.")

    except Exception as e:
        print("❌ Error:", e)
    
    

