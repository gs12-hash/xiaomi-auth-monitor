import os
import requests
from playwright.sync_api import sync_playwright

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def notify(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg}, timeout=15)

def check():
    alerts = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Revisar HW-Key (Xiaomi MTK V6 Auth)
        try:
            page.goto("https://www.hwkey.com", wait_until="networkidle", timeout=45000)
            page.wait_for_timeout(4000)
            text_hw = page.inner_text("body")
            for line in text_hw.splitlines():
                if "Xiaomi MTK V6 Auth" in line or "New SLA MTK V6 Auth" in line:
                    idx = text_hw.find(line)
                    snippet = text_hw[idx:idx+120]
                    if "ONLINE" in snippet.upper() and "OFFLINE" not in snippet.upper():
                        alerts.append(f"🟢 HW-KEY ONLINE: {line.strip()}")
        except Exception as e:
            print("Error HW-Key:", e)

        # 2. Revisar Typhon Tool (NEW MTK V6)
        try:
            page.goto("https://typhontool.com/server_status", wait_until="networkidle", timeout=45000)
            page.wait_for_timeout(4000)
            text_ty = page.inner_text("body")
            if "NEW MTK V6" in text_ty:
                idx = text_ty.find("NEW MTK V6")
                snippet = text_ty[max(0, idx-80):idx+80]
                if "Outage" not in snippet and ("Online" in snippet or "Operational" in snippet):
                    alerts.append("🟢 TYPHON TOOL ONLINE: NEW MTK V6 activo")
        except Exception as e:
            print("Error Typhon:", e)

        browser.close()

    if True:
    alerts.append("🧪 PRUEBA DE SISTEMA: El bot se conecta perfecto a tu Telegram.")
    else:
        print("Siguen offline.")

if __name__ == "__main__":
    check()
