import os
import requests
from playwright.sync_api import sync_playwright

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def notify(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": msg}, timeout=15)
    r.raise_for_status()

def check():
    alerts = ["🧪 PRUEBA OK: Tu bot de Telegram está conectado y funcionando."]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.hwkey.com", wait_until="networkidle", timeout=45000)
        browser.close()

    if alerts:
        notify("\n".join(alerts))

if __name__ == "__main__":
    check()
