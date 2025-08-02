import os
import time
import socket
import zipfile
import cloudscraper
import random
import string
import json
from bs4 import BeautifulSoup
from pystyle import Colors, Colorate
from fake_useragent import UserAgent

banner = r"""
                 ▄████▄▓██   ██▓  ██████  ▄▄▄       █     █░▄▄▄█████▓ ▒█████   ▒█████   ██▓
                ▒██▀ ▀█ ▒██  ██▒▒██    ▒ ▒████▄    ▓█░ █ ░█░▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒
                ▒▓█    ▄ ▒██ ██░░ ▓██▄   ▒██  ▀█▄  ▒█░ █ ░█ ▒ ▓██░ ▒░▒██░  ██▒▒██░ ██▒▒██░
                ▒▓▓▄ ▄██▒░ ▐██▓░  ▒   ██▒░██▄▄▄▄██ ░█░ █ ░█ ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░
                ▒ ▓███▀ ░░ ██▒▓░▒██████▒▒ ▓█   ▓██▒░░██▒██▓   ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░ ████▓▒░░██████▒
                ░ ░▒ ▒  ░ ██▒▒▒ ▒ ▒▓▒ ▒ ░ ▒▒   ▓▒█░░ ▓░▒ ▒    ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░
                  ░  ▒  ▓██ ░▒░ ░ ░▒  ░ ░  ▒   ▒▒ ░  ▒ ░ ░      ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░
                ░       ▒ ▒ ░░  ░  ░  ░    ░   ▒     ░   ░    ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░
                ░ ░     ░ ░           ░        ░  ░    ░                 ░ ░      ░ ░      ░  ░
                ░       ░ ░
"""

def print_status(msg, err=False):
    color = Colors.red if err else Colors.white
    print(f"   {Colors.blue}└──${Colors.reset} {color}{msg}{Colors.reset}")

ua = UserAgent()
user_agent = ua.random
scraper = cloudscraper.create_scraper()
scraper.headers.update({"User-Agent": user_agent})

_0x1a2b = '5ff1e8b450d52e78678e870c629d6d07737a211572db5739a40caee6f5fa6ee8'
_0x3c4d = '688e0e86d5f1a'
_0x7g8h = 'e1e68f2c4a59734be909a9a5e0dfdc6b'
_0x9i0j = 'd69c73b965f15bc267c39fcc0916e976'
_0xk1l2 = '3'
rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
csrf_token = f"{_0x1a2b}{_0x9i0j[:8]}_{rand_str}"
session_id = f"{_0x3c4d}{_0x9i0j[8:16]}_{rand_str}"
user_interactions = random.randint(5, 20)

def get_download_link(app_id):
    print_status(f"Requesting download link for AppID: {app_id}")
    headers = {
        "accept": "*/*", "content-type": "application/json", "origin": "https://cysaw.org",
        "referer": "https://cysaw.org/", "X-CSRF-Token": csrf_token,
        "X-Session-ID": session_id, "X-User-Interactions": str(user_interactions)
    }
    payload = {"appId": app_id, "csrfToken": csrf_token, "sessionId": session_id,
               "userInteractions": user_interactions, "sessionHash": _0x7g8h, "pageVisits": _0xk1l2}
    try:
        r = scraper.post("https://cysaw.org/api.php", json=payload, headers=headers, timeout=15)
        r.raise_for_status()
        j = r.json()
        if j.get("status") == "success" and j.get("downloadUrl"):
            print_status("Successfully retrieved protected link.")
            return j["downloadUrl"]
        print_status("API Failure: " + j.get("message", "No link"), True)
    except Exception as e:
        print_status(f"API error: {e}", True)
    return None

def bypass_shrink(url):
    print_status(f"Processing protected link: {url}")
    try:
        code = url.rstrip("/").split("/")[-1]
        page = f"https://en.shrinke.me/{code}"
        r1 = scraper.get(page, headers={"referer": "https://mrproblogger.com/"}, timeout=20)
        r1.raise_for_status()
        soup = BeautifulSoup(r1.content, "html.parser")
        data = {i.get('name'): i.get('value') for i in soup.find_all("input") if i.get('name')}
        if not data:
            print_status("Bypass failed: No form inputs.", True)
            return None
        print_status("Waiting for bypass timer (15 seconds)...")
        time.sleep(15)
        r2 = scraper.post("https://en.shrinke.me/links/go", data=data,
                          headers={"x-requested-with": "XMLHttpRequest", "referer": page}, timeout=20)
        r2.raise_for_status()
        j = r2.json()
        if j.get("url"):
            print_status("Direct link obtained. Proceeding to download...")
            return j["url"]
        print_status("Bypass failed: " + j.get("message", "No URL found"), True)
    except Exception as e:
        print_status(f"Bypass error: {e}", True)
    return None

def download_and_extract(url):
    print_status(f"Attempting to download from: {url}")
    try:
        headers = {'User-Agent': user_agent, 'Referer': 'https://en.shrinke.me/',
                   'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8', 'Connection': 'keep-alive'}
        print_status("Adding a small delay before final download...")
        time.sleep(2)
        r = scraper.get(url, stream=True, timeout=30, allow_redirects=True, headers=headers)
        r.raise_for_status()
        cd = r.headers.get('Content-Disposition', '')
        filename = "downloaded_file.zip"
        if "filename=" in cd:
            filename = cd.split("filename=")[1].strip("\"'")
        else:
            name = os.path.basename(url.split("?")[0])
            if name.endswith(".zip"):
                filename = name
        print_status(f"Downloading file: {filename}")
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
        print_status(f"Downloaded: {filename}")
        extract_to = os.path.splitext(filename)[0]
        os.makedirs(extract_to, exist_ok=True)
        with zipfile.ZipFile(filename, 'r') as archive: archive.extractall(extract_to)
        print_status(f"Extracted to: {extract_to}")
        os.remove(filename)
        print_status(f"Cleaned up: Removed {filename}")
    except Exception as e:
        print_status(f"Unexpected download error: {e}", True)

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print(Colorate.Vertical(Colors.blue_to_white, banner))
    hostname = socket.gethostname()
    print(f"   {Colors.blue}┌───({Colors.white}{hostname}{Colors.blue}){Colors.reset}")
    print_status("Session started. Cloudscraper initialized.")
    scraper.get("https://cysaw.org/")
    print_status(f"Using User-Agent: {user_agent}")
    while True:
        try:
            user_input = input(f"   {Colors.blue}└──$ {Colors.reset}Enter AppID (or 'exit'): ").strip()
            if user_input.lower() == 'exit': print_status("Exiting."); break
            if not user_input: print_status("AppID cannot be empty.", True); continue
            p = get_download_link(user_input)
            if p:
                d = bypass_shrink(p)
                if d: download_and_extract(d)
                else: print_status("Bypass failed.", True)
            else: print_status("No valid link.", True)
        except KeyboardInterrupt:
            print(); print_status("Interrupted."); break
        except Exception as e:
            print_status(f"Error: {e}", True)
    print_status("Session ended.")
