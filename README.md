
<h1 align="center"> 📲 WhatsApp Group Contact Extractor & ChatBot Responder</h1>

Welcome to the **WhatsApp Contact Extractor & ChatBot Responder**, a dual-purpose automation tool built using **Selenium**, **Streamlit**, and **Google's Gemini API** to:

1. 📥 **Extract WhatsApp Group Members** (phone numbers only)
2. 🤖 **Auto-generate Smart Replies** using chat history and Gemini AI

---
<h2 align="center">🧰 Technologies Used </h2>
<div align="center">

<table>
  <thead>
    <tr>
      <th>Tool</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Selenium</td><td>Automate WhatsApp Web in Chrome</td></tr>
    <tr><td>Streamlit</td><td>Web Interface for extracting contacts</td></tr>
    <tr><td>Gemini API</td><td>AI-based smart replies to recent chats</td></tr>
    <tr><td>Pandas</td><td>Data handling and export</td></tr>
    <tr><td>ChromeDriver</td><td>Browser automation</td></tr>
    <tr><td>SQLite</td><td>User login and registration database</td></tr>
    <tr><td>SQLAlchemy</td><td>ORM for user model</td></tr>
    <tr><td>Werkzeug</td><td>Secure password hashing</td></tr>
  </tbody>
</table>

</div>

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

![image](https://github.com/user-attachments/assets/6a7ce7da-67ee-49e0-bf1f-4fa1b23fb2fd)

---

![image](https://github.com/user-attachments/assets/14eadbd4-16ed-49fa-8b75-fa65919a8876)


---

## 📝 License

[MIT License](https://github.com/Ronak1231/Whatsapp_Contact/blob/main/LICENSE)

---

## 🙋‍♂️ Author

**Ronak Bansal**  
📎 GitHub: [Ronak1231](https://github.com/Ronak1231)

---

> Made with ❤️ for automation enthusiasts.
