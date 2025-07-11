# Standard libraries for time delays, CSV parsing, JSON handling, threading, and GUI
import time
import csv
import json
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
# Selenium components for browser automation and element interaction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# A stealthy version of ChromeDriver to bypass bot detection
import undetected_chromedriver as uc

running = False


# Load usernames from a CSV file (expects a 'username' column)
def load_usernames(csv_file):
    usernames = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            usernames.append(row['username'])
    return usernames


# Load cookies from a local JSON file for session persistence
def load_cookies():
    try:
        with open("instagram_cookies.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


# Save cookies to a JSON file for future logins
def save_cookies(driver):
    cookies = driver.get_cookies()
    with open("instagram_cookies.json", "w") as f:
        json.dump(cookies, f)


# Log messages to a local file and print them to the console
def log_message(message):
    with open("removal_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    print(message)


# Main automation logic to remove followers from the given list
def start_removal(csv_path, limit, chromium_path, ig_username):
    global running
    running = True
    usernames = load_usernames(csv_path)

    options = uc.ChromeOptions()
    options.binary_location = chromium_path
    driver = uc.Chrome(options=options)

    cookies = load_cookies()
    if cookies:
        driver.get("https://www.instagram.com/")
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            log_message("✅ Logged in using saved cookies")
        except:
            log_message("⚠️ Cookies invalid, prompting manual login")
            cookies = None

    if not cookies:
        driver.get("https://www.instagram.com/accounts/login/")
        WebDriverWait(driver, 30).until(EC.url_contains("instagram.com"))
        input("Log in manually and press Enter to continue...")
        try:
            WebDriverWait(driver, 30).until(EC.url_contains("instagram.com"))
            save_cookies(driver)
            log_message("✅ Manual login successful, cookies saved")
        except Exception as e:
            log_message(f"⚠️ Manual login failed: {e}")
            driver.quit()
            return

    driver.get(f"https://www.instagram.com/{ig_username}/")
    try:
        # Click followers link
        followers_link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//li[2]//a//span"))
        )
        followers_link.click()
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Followers')]")))
        log_message("✅ Opened followers list")
    except Exception as e:
        log_message(f"⚠️ Failed to open followers list: {e}")
        driver.quit()
        return

    removed_count = 0
    for username in usernames:
        if not running or removed_count >= limit:
            break
        try:
            # Search for username
            search_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))
            )
            search_input.clear()
            search_input.send_keys(username)
            time.sleep(2)

            # Click Remove button
            remove_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'x6nl9eh')]//div[contains(text(), 'Remove')]"))
            )
            remove_btn.click()
            time.sleep(2)  # Wait for popup

            # Click confirmation Remove button in popup
            confirm_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Remove']"))
            )
            confirm_btn.click()
            log_message(f"✅ Removed: {username}")
            removed_count += 1
            time.sleep(3 + (removed_count % 5))
        except Exception as e:
            log_message(f"⚠️ Error with {username}: {str(e)}")
            continue

    driver.quit()
    log_message("✅ Script finished.")


# Stop the follower removal loop by setting the running flag to False
def stop_removal():
    global running
    running = False
    log_message("🛑 Script stopped by user.")


# Create and run the GUI for the Instagram Follower Remover tool
def run_gui():

        # Start the follower removal in a separate thread
    def start_thread():
        csv_path = csv_entry.get()
        chromium_path = chrome_entry.get()
        ig_username = username_entry.get()
        try:
            limit = int(limit_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Limit must be an integer.")
            return
        threading.Thread(target=start_removal, args=(csv_path, limit, chromium_path, ig_username)).start()


        # File dialog to select the followers CSV file
    def browse_csv():
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            csv_entry.delete(0, tk.END)
            csv_entry.insert(0, path)


        # File dialog to select the path to Chromium/Chrome executable
    def browse_chrome():
        path = filedialog.askopenfilename(filetypes=[("Chrome Executable", "*.exe")])
        if path:
            chrome_entry.delete(0, tk.END)
            chrome_entry.insert(0, path)

    root = tk.Tk()
    root.title("Instagram Follower Remover")

    tk.Label(root, text="Followers CSV:").grid(row=0, column=0, sticky="w")
    csv_entry = tk.Entry(root, width=50)
    csv_entry.grid(row=0, column=1)
    tk.Button(root, text="Browse", command=browse_csv).grid(row=0, column=2)

    tk.Label(root, text="Chromium Path:").grid(row=1, column=0, sticky="w")
    chrome_entry = tk.Entry(root, width=50)
    chrome_entry.grid(row=1, column=1)
    tk.Button(root, text="Browse", command=browse_chrome).grid(row=1, column=2)

    tk.Label(root, text="Instagram Username:").grid(row=2, column=0, sticky="w")
    username_entry = tk.Entry(root, width=50)
    username_entry.grid(row=2, column=1)

    tk.Label(root, text="Max Removals:").grid(row=3, column=0, sticky="w")
    limit_entry = tk.Entry(root, width=10)
    limit_entry.insert(0, "50")
    limit_entry.grid(row=3, column=1, sticky="w")

    tk.Button(root, text="Start", bg="green", fg="white", command=start_thread).grid(row=4, column=0, pady=10)
    tk.Button(root, text="Stop", bg="red", fg="white", command=stop_removal).grid(row=4, column=1, pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()