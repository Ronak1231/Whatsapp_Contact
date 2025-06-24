
# 📲 WhatsApp Group Contact Extractor & ChatBot Responder

Welcome to the **WhatsApp Contact Extractor & ChatBot Responder**, a dual-purpose automation tool built using **Selenium**, **Streamlit**, and **Google's Gemini API** to:

1. 📥 **Extract WhatsApp Group Members** (phone numbers only)
2. 🤖 **Auto-generate Smart Replies** using chat history and Gemini AI

---

## 🧰 Technologies Used

| Tool          | Purpose                                 |
|---------------|------------------------------------------|
| Selenium      | Automate WhatsApp Web in Chrome         |
| Streamlit     | Web Interface for extracting contacts   |
| Gemini API    | AI-based smart replies to recent chats  |
| Pandas        | Data handling and export                |
| ChromeDriver  | Browser automation                      |
| SQLite        | User login and registration database    |
| SQLAlchemy    | ORM for user model                      |
| Werkzeug      | Secure password hashing                 |

---

## 📁 Project Structure

```bash
Whatsapp_Contact/
│
├── Member_trials/                    # Intermediate tests
│   ├── test.py
│   └── update_upto_17_june.py
│
├── selenium_chrome_profile/         # Chrome user profile for WhatsApp Web session
│
├── text_reply_python/               # ChatBot code using Gemini API
│   └── main.py
│
├── venv/                            # Python virtual environment
│
├── whatsapp_profile/                # Another chrome profile folder
│
├── whatsapp-tools/                  # Utility tools (if any)
│
├── .env                             # Environment variables
├── chromedriver.exe                 # Required for Selenium browser automation
├── main.py                          # Streamlit app for member extraction
├── requirements.txt                 # Python dependencies
└── users.db                         # SQLite database for storing user login information
└── README.md                        # Project documentation
```

---

## 🌟 Features

### ✅ WhatsApp Group Member Extractor (with Streamlit)
- Opens WhatsApp Web with your Chrome profile.
- Searches for group and extracts members' phone numbers.
- Exports the list to Excel (`.xlsx`).
- Fully interactive interface with search and feedback.

### 🔐 Login & Registration System
- Secure login and registration using **Streamlit**, **SQLite**, and **Werkzeug**.
- Passwords are securely hashed.
- Prevents unauthorized access to the extraction tool.

### ✅ WhatsApp ChatBot Responder (CLI-based)
- Search and open any group or personal chat.
- Retrieves the last 10 messages.
- Uses Gemini AI to generate human-like responses.
- Auto-sends the response directly in the chat.

---

## 🚀 How to Get Started

### 1. Clone the Repository
```bash
git clone https://github.com/Ronak1231/Whatsapp_Contact.git
cd Whatsapp_Contact
```

### 2. Set Up Environment
```bash
pip install -r requirements.txt
```

### 3. Ensure Chrome Profile is Set
- Log in to [https://web.whatsapp.com](https://web.whatsapp.com) in Chrome.
- Save your Chrome profile folder and use its path in the script.

### 4. Run the Streamlit Member Extractor (with login system)
```bash
streamlit run main.py
```

### 5. Run the CLI ChatBot Responder
```bash
python text_reply_python/main.py
```

> ⚠️ **Make sure `chromedriver.exe` version matches your Chrome version.**

---

## 📸 Screenshots

> *(Insert screenshots of login page, extraction interface, and chatbot CLI here)*

---

## 📝 License

MIT License

---

## 🙋‍♂️ Author

**Ronak Bansal**  
📎 GitHub: [Ronak1231](https://github.com/Ronak1231)

---

> Made with ❤️ for automation enthusiasts.
