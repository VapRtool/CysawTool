import os
import re
import time
import socket
import zipfile
import requests
import threading
import cloudscraper
from bs4 import BeautifulSoup
from pystyle import Colors, Colorate
from fake_useragent import UserAgent

ua = UserAgent()

banner = """\n
                 ▄████▄▓██   ██▓  ██████  ▄▄▄       █     █░▄▄▄█████▓ ▒█████   ▒█████   ██▓    
                ▒██▀ ▀█ ▒██  ██▒▒██    ▒ ▒████▄    ▓█░ █ ░█░▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    
                ▒▓█    ▄ ▒██ ██░░ ▓██▄   ▒██  ▀█▄  ▒█░ █ ░█ ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    
                ▒▓▓▄ ▄██▒░ ▐██▓░  ▒   ██▒░██▄▄▄▄██ ░█░ █ ░█ ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░    
                ▒ ▓███▀ ░░ ██▒▓░▒██████▒▒ ▓█   ▓██▒░░██▒██▓   ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒
                ░ ░▒ ▒  ░ ██▒▒▒ ▒ ▒▓▒ ▒ ░ ▒▒   ▓▒█░░ ▓░▒ ▒    ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░
                  ░  ▒  ▓██ ░▒░ ░ ░▒  ░ ░  ▒   ▒▒ ░  ▒ ░ ░      ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░
                ░       ▒ ▒ ░░  ░  ░  ░    ░   ▒     ░   ░    ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   
                ░ ░     ░ ░           ░        ░  ░    ░                 ░ ░      ░ ░      ░  ░
                ░       ░ ░                                                                    

"""

def print_status(message):
    print(f"  {Colors.blue} └──${Colors.white} {message}{Colors.reset}")

def establish_cysaw_session(application_id):
    scraper = cloudscraper.create_scraper(
        allow_brotli=False,
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False
        }
    )
    
    user_agent = ua.random
    headers = {
        "user-agent": user_agent,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.5",
        "accept-encoding": "gzip, deflate",
        "connection": "keep-alive",
        "upgrade-insecure-requests": "1",
        "cache-control": "max-age=0"
    }
    
    try:
        response = scraper.get("https://cysaw.org/", headers=headers, timeout=15)
        
        if response.status_code != 200:
            return None
            
        csrf_token = None
        session_id = None
        content = response.text
        
        csrf_match = re.search(r"const csrfToken = '([^']+)'", content)
        if csrf_match:
            csrf_token = csrf_match.group(1)
        
        session_match = re.search(r"const sessionId = '([^']+)'", content)
        if session_match:
            session_id = session_match.group(1)
        
        return {
            'scraper': scraper,
            'user_agent': user_agent,
            'csrf_token': csrf_token,
            'session_id': session_id,
            'headers': headers
        }
        
    except Exception:
        return None

def get_download_link_from_api(session_data, application_id):
    if not session_data:
        return None
        
    scraper = session_data['scraper']
    user_interactions = 15
    
    api_headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://cysaw.org",
        "referer": "https://cysaw.org/",
        "user-agent": session_data['user_agent'],
        "X-CSRF-Token": session_data['csrf_token'],
        "X-Session-ID": session_data['session_id'],
        "X-User-Interactions": str(user_interactions)
    }
    
    api_payload = {
        "appId": application_id,
        "csrfToken": session_data['csrf_token'],
        "sessionId": session_data['session_id'],
        "userInteractions": user_interactions
    }
    
    try:
        api_response = scraper.post(
            "https://cysaw.org/api.php", 
            json=api_payload, 
            headers=api_headers,
            timeout=15
        )
        
        if api_response.status_code == 403:
            return None
            
        api_response.raise_for_status()
        response_data = api_response.json()
        
        if response_data.get("status") == "success":
            return {
                "downloadUrl": response_data["downloadUrl"],
                "dirName": response_data.get("dirName"),
                "session_data": session_data,
                "full_response": response_data
            }
        else:
            return None
            
    except Exception:
        return None

def mark_downloaded_async(session_data, dir_name):
    try:
        scraper = session_data['scraper']
        
        mark_headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://cysaw.org",
            "referer": "https://cysaw.org/",
            "user-agent": session_data['user_agent'],
            "X-CSRF-Token": session_data['csrf_token'],
            "X-Session-ID": session_data['session_id']
        }
        
        mark_payload = {
            "dirName": dir_name,
            "csrfToken": session_data['csrf_token'],
            "sessionId": session_data['session_id']
        }
        
        scraper.post(
            "https://cysaw.org/mark_downloaded.php",
            json=mark_payload,
            headers=mark_headers,
            timeout=10
        )
            
    except Exception:
        pass

def bypass_shrink_protection_and_download(download_data):
    protected_url = download_data["downloadUrl"]
    session_data = download_data["session_data"]
    dir_name = download_data.get("dirName")
    
    shrink_scraper = cloudscraper.create_scraper(
        allow_brotli=False,
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False
        }
    )
    
    shrink_domain = "https://en.shrinke.me"
    url_code = protected_url.rstrip("/").split("/")[-1]
    target_url = f"{shrink_domain}/{url_code}"
    print_status("Processing protected link...")
    
    try:
        user_agent = session_data['user_agent']
        
        shrink_headers = {
            "referer": "https://mrproblogger.com/",
            "user-agent": user_agent,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.5",
            "accept-encoding": "gzip, deflate",
            "connection": "keep-alive",
            "upgrade-insecure-requests": "1"
        }
        
        page_response = shrink_scraper.get(target_url, headers=shrink_headers)
        page_soup = BeautifulSoup(page_response.content, "html.parser")
        
        form_inputs = page_soup.find_all("input")
        form_data = {inp.get('name'): inp.get('value') for inp in form_inputs if inp.get('name')}
        
        print_status("Waiting for bypass timer...")
        
        if dir_name:
            mark_thread = threading.Thread(
                target=mark_downloaded_async, 
                args=(session_data, dir_name)
            )
            mark_thread.start()
        
        time.sleep(15)
        
        bypass_headers = shrink_headers.copy()
        bypass_headers.update({
            "x-requested-with": "XMLHttpRequest",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "referer": target_url
        })
        
        bypass_response = shrink_scraper.post(
            f"{shrink_domain}/links/go", 
            data=form_data, 
            headers=bypass_headers
        )
        
        if bypass_response.status_code != 200:
            print_status("Bypass failed")
            return
            
        response_json = bypass_response.json()
        direct_url = response_json.get("url")

        if direct_url:
            print_status("Downloading and extracting file...")
            
            if dir_name:
                mark_thread.join(timeout=5)
            
            download_with_cysaw_session(session_data, direct_url)
        else:
            print_status("Bypass failed: No download URL found")
            
    except Exception as error:
        print_status(f"Bypass error: {error}")

def download_with_cysaw_session(session_data, download_url):
    try:
        scraper = session_data['scraper']
        
        download_headers = {
            "user-agent": session_data['user_agent'],
            "accept": "application/octet-stream,*/*",
            "accept-language": "en-US,en;q=0.5", 
            "accept-encoding": "gzip, deflate",
            "referer": "https://cysaw.org/",
            "connection": "keep-alive"
        }
        
        file_response = scraper.get(download_url, stream=True, timeout=30, headers=download_headers)

        if file_response.status_code != 200:
            print_status(f"Failed to download file. Status code: {file_response.status_code}")
            return

        content_disposition = file_response.headers.get('Content-Disposition', '')
        if "filename=" in content_disposition:
            zip_filename = content_disposition.split("filename=")[1].strip("\"'")
        else:
            zip_filename = download_url.split("/")[-1].split("?")[0]

        if not zip_filename.endswith(".zip"):
            if not any(zip_filename.endswith(ext) for ext in ['.rar', '.7z', '.tar.gz']):
                zip_filename += ".zip"

        print_status(f"Downloaded: {zip_filename}")

        with open(zip_filename, "wb") as zip_file:
            for chunk in file_response.iter_content(chunk_size=8192):
                if chunk:
                    zip_file.write(chunk)

        if zip_filename.endswith(".zip"):
            try:
                extract_folder = os.path.splitext(zip_filename)[0]
                with zipfile.ZipFile(zip_filename, 'r') as archive:
                    archive.extractall(extract_folder)
                print_status(f"Extracted to: {extract_folder}")
                
                os.remove(zip_filename)
                print_status(f"Cleaned up: {zip_filename}")
            except zipfile.BadZipFile:
                print_status("File is not a valid ZIP archive, keeping as-is")

    except Exception as error:
        print_status(f"Download error: {error}")

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print(Colorate.Vertical(Colors.blue_to_white, banner))
    print()
    computer_name = socket.gethostname()
    print(f"   {Colors.blue}┌───({Colors.white}{computer_name}{Colors.blue}){Colors.reset}")
    
    while True:
        try:
            user_input = input(f"{Colors.blue}   └──$ {Colors.reset}Enter AppID: ").strip()
            if not user_input:
                print_status("No AppID provided. Exiting.")
                break
                
            session_data = establish_cysaw_session(user_input)
            if not session_data:
                print_status("Failed to establish session")
                continue
                
            download_data = get_download_link_from_api(session_data, user_input)
            if not download_data:
                print_status("No valid download link found for this AppID.")
                continue
                
            bypass_shrink_protection_and_download(download_data)
                
        except KeyboardInterrupt:
            print("\nExiting by user request.")
            break
