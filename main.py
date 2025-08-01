import os, time, socket, zipfile, requests, cloudscraper
from bs4 import BeautifulSoup
from pystyle import Colors, Colorate

banner = r"""

                 ▄████▄▓██   ██▓  ██████  ▄▄▄       █     █░▄▄▄█████▓ ▒█████   ▒█████   ██▓    
                ▒██▀ ▀█ ▒██  ██▒▒██    ▒ ▒████▄    ▓█░ █ ░█░▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    
                ▒▓█    ▄ ▒██ ██░░ ▓██▄   ▒██  ▀█▄  ▒█░ █ ░█ ▒ ▓██░ ▒░▒██░  ██▒▒██░ ██▒▒██░    
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

def get_download_link_from_api(application_id):
    api_headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://cysaw.org",
        "referer": "https://cysaw.org/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        api_response = requests.post("https://cysaw.org/api.php", json={"appId": application_id}, headers=api_headers)
        api_response.raise_for_status()
        response_data = api_response.json()
        return response_data["downloadUrl"] if response_data.get("status") == "success" else None
    except Exception as error:
        print_status(f"API request failed: {error}")
        return None

def bypass_shrink_protection(protected_url):
    scraper = cloudscraper.create_scraper(allow_brotli=False)
    shrink_domain = "https://en.shrinke.me"
    url_code = protected_url.rstrip("/").split("/")[-1]
    target_url = f"{shrink_domain}/{url_code}"

    print_status("Processing protected link...")
    
    try:
        page_response = scraper.get(target_url, headers={"referer": "https://mrproblogger.com/"})
        page_soup = BeautifulSoup(page_response.content, "html.parser")
        form_inputs = page_soup.find_all("input")
        form_data = {input_field.get('name'): input_field.get('value') for input_field in form_inputs if input_field.get('name')}

        print_status("Waiting for bypass timer...")
        time.sleep(15)

        bypass_response = scraper.post(f"{shrink_domain}/links/go", data=form_data, headers={"x-requested-with": "XMLHttpRequest"})
        direct_url = bypass_response.json().get("url")
        
        if direct_url:
            print_status("Downloading and extracting file...")
            download_and_extract_zip(direct_url)
        else:
            print_status("Bypass failed: No download URL found")
    except Exception as error:
        print_status(f"Bypass error: {error}")

def download_and_extract_zip(download_url):
    try:
        file_response = requests.get(download_url, stream=True, timeout=20, allow_redirects=True)
        content_disposition = file_response.headers.get('Content-Disposition', '')
        
        if "filename=" in content_disposition:
            zip_filename = content_disposition.split("filename=")[1].strip("\"'")
        else:
            zip_filename = download_url.split("/")[-1].split("?")[0]

        if not zip_filename.endswith(".zip"):
            print_status("File is not a ZIP archive")
            return

        with open(zip_filename, "wb") as zip_file:
            for chunk in file_response.iter_content(chunk_size=8192):
                if chunk: zip_file.write(chunk)
        print_status(f"Downloaded: {zip_filename}")

        extract_folder = os.path.splitext(zip_filename)[0]
        with zipfile.ZipFile(zip_filename, 'r') as archive:
            archive.extractall(extract_folder)
        print_status(f"Extracted to: {extract_folder}")

        os.remove(zip_filename)
        print_status(f"Cleaned up: {zip_filename}")
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

            protected_link = get_download_link_from_api(user_input)
            if protected_link:
                bypass_shrink_protection(protected_link)
            else:
                print_status("No valid download link found for this AppID.")
        except KeyboardInterrupt:
            print("\nExiting by user request.")
            break
