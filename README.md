# AXI Instagram Follower Remover With GUI 🧹

A Python GUI tool that helps you mass-remove followers from your Instagram account using Selenium and a list of usernames.

## ⚙️ Features

- Auto stops when reached daily cap and continues after 24 hours from where it left off.
– Detailed explanation of code for beginners!
- Remove followers from a CSV list.
- Supports login via saved cookies or manual login.
- GUI built with Tkinter.
- Uses undetected ChromeDriver for stealth automation.
- Logs every removal action.


---

## 🖥️ GUI Overview

<img width="509" height="172" alt="image" src="https://github.com/user-attachments/assets/7ecd4769-3e92-4b25-995a-27944defebe8" />

---

## 🧰 Requirements

- Python 3.7+
- Google Chrome or Chromium
- ChromeDriver (compatible with your Chrome version)
- `undetected-chromedriver`
- `selenium`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📄 CSV Format

The CSV must contain a `username` column:

```csv
username
user_one
user_two
user_three
```

---

## 🚀 How to Use

1. Clone the repo:
    ```bash
    git clone https://github.com/yourusername/insta-follower-remover.git
    cd insta-follower-remover
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the script:
    ```bash
    python insta_remover_gui.py
    ```

4. Fill in:
    - Path to your `followers.csv`
    - Path to your Chrome/Chromium executable
    - Instagram username
    - Max number of followers to remove

---

## 📝 Log Output

Each session logs actions to `removal_log.txt`.

---

## 🛑 Notes

- You must manually log in the first time; cookies will be saved for future runs.
- Instagram rate-limits may apply. Use this responsibly.

---

## 📜 License

MIT License
