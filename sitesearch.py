import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import tldextract
import time
import sys
import itertools
import webbrowser

def is_cdn_cgi_url(url):
    return 'cdn-cgi' in urlparse(url).path

def get_redirected_pages(base_url, visited, base_domain):
    redirected_pages = set()
    all_links = set()
    queue = [base_url]
    
    while queue:
        url = queue.pop(0)
        if url not in visited and not is_cdn_cgi_url(url):
            visited.add(url)
            try:
                print(f"Visiting: {url}")
                response = requests.get(url, allow_redirects=True)
                
                final_url = response.url
                if response.status_code == 200 and urlparse(final_url).netloc.endswith(base_domain):
                    if final_url != url:
                        redirected_pages.add(final_url)
                        print_with_delay([final_url])

                    soup = BeautifulSoup(response.text, 'html.parser')
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        full_url = urljoin(final_url, href)
                        parsed_url = urlparse(full_url)
                        
                        if parsed_url.netloc and parsed_url.netloc.endswith(base_domain) and not is_cdn_cgi_url(full_url):
                            if full_url not in visited:
                                queue.append(full_url)
                        
                        all_links.add(full_url)
                
                time.sleep(0.01)  
            except requests.RequestException as e:
                print(f"Error: {url} - {e}")
                continue

    return redirected_pages, all_links

def print_with_delay(items, delay=0.05):
    """ Prints each item in the list with the specified delay. """
    for item in items:
        print(item)
        time.sleep(delay)
        sys.stdout.flush() 

def display_language_selection():
    """ Displays the language selection prompt and returns the selected language. """
    print("Please select your language / Lütfen dilinizi seçin:")
    print("1. English")
    print("2. Türkçe")
    choice = input("Enter your choice (1/2): ")
    
    if choice == '1':
        return 'en'
    elif choice == '2':
        return 'tr'
    else:
        print("Invalid choice, defaulting to English.")
        return 'en'

def loading_animation(duration=5):
    """ Shows a loading animation for a given duration. """
    end_time = time.time() + duration
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while time.time() < end_time:
        sys.stdout.write(f'\rLoading... {next(spinner)}')
        sys.stdout.flush()
        time.sleep(0.1)

def main(domain, language):
    global base_domain
    extracted = tldextract.extract(domain)
    base_domain = f"{extracted.domain}.{extracted.suffix}"
    
    if language == 'en':
        print(f"Scanning started: {domain}")
    elif language == 'tr':
        print(f"Tarama başlatılıyor: {domain}")

    visited = set()
    
    start_time = time.time()  
    

    redirected_pages, all_links = get_redirected_pages(f"http://{domain}", visited, base_domain)
    
    end_time = time.time()  
    elapsed_time = end_time - start_time
    

    with open("site_page.txt", "w", encoding="utf-8") as file:
        for page in redirected_pages:
            file.write(f"{page}\n")

    with open("redirect_links.txt", "w", encoding="utf-8") as file:
        for link in all_links:
            file.write(f"{link}\n")


    webbrowser.open_new("https://github.com/who0ze")

    if language == 'en':
        print(r"            .______       _______  _______   __  .______       _______   ______ .___________.")
        print(r"            |   _  \     |   ____||       \ |  | |   _  \     |   ____| /      ||           |")
        print(r"            |  |_)  |    |  |__   |  .--.  ||  | |  |_)  |    |  |__   |  ,----'`---|  |----`")
        print(r"            |      /     |   __|  |  |  |  ||  | |      /     |   __|  |  |         |  |    ")
        print(r"            |  |\  \----.|  |____ |  '--'  ||  | |  |\  \----.|  |____ |  `----.    |  |   ")
        print(r"            | _| `._____||_______||_______/ |__| | _| `._____||_______| \______|    |__|     ")
        print(r"            __       __  .__   __.  __  ___      _______.         ")
        print(r"            |  |     |  | |  \ |  | |  |/  /     /       |    ")
        print(r"            |  |     |  | |   \|  | |  '  /     |   (----`                                   ")
        print(r"            |  |     |  | |  . `  | |    <       \   \                                       ")
        print(r"            |  `----.|  | |  |\   | |  .  \  .----)   |                                      ")
        print(r"            |_______||__| |__| \__| |__|\__\ |_______/                                       ")
    elif language == 'tr':
        print(r"            .______       _______  _______   __  .______       _______   ______ .___________.")
        print(r"            |   _  \     |   ____||       \ |  | |   _  \     |   ____| /      ||           |")
        print(r"            |  |_)  |    |  |__   |  .--.  ||  | |  |_)  |    |  |__   |  ,----'`---|  |----`")
        print(r"            |      /     |   __|  |  |  |  ||  | |      /     |   __|  |  |         |  |    ")
        print(r"            |  |\  \----.|  |____ |  '--'  ||  | |  |\  \----.|  |____ |  `----.    |  |   ")
        print(r"            | _| `._____||_______||_______/ |__| | _| `._____||_______| \______|    |__|     ")
        print(r"            __       __  .__   __.  __  ___      _______.         ")
        print(r"            |  |     |  | |  \ |  | |  |/  /     /       |    ")
        print(r"            |  |     |  | |   \|  | |  '  /     |   (----`                                   ")
        print(r"            |  |     |  | |  . `  | |    <       \   \                                       ")
        print(r"            |  `----.|  | |  |\   | |  .  \  .----)   |                                      ")
        print(r"            |_______||__| |__| \__| |__|\__\ |_______/                                       ")

    loading_animation(3)
    
    print("\nRedirected Links:")
    if all_links:
        print_with_delay(list(all_links))
    else:
        print("No redirected links found.")

    if language == 'en':
        print(f"\nScan completed. Results saved in 'site_page.txt' and 'redirect_links.txt'.")
    elif language == 'tr':
        print(f"\nTarama tamamlandı. Sonuçlar 'site_page.txt' ve 'redirect_links.txt' dosyalarına kaydedildi.")

    print(f"Scan duration: {elapsed_time:.2f} seconds")

    for i in range(3):
        print("\033[1;34mScanning complete...\033[0m", end="\r")
        time.sleep(0.5)
        print(" " * 22, end="\r")
        time.sleep(0.5)

if __name__ == "__main__":
    print("""
         _______ .______       _______  _______         _______. __  .___________. _______                             
        |   ____||   _  \     |   ____||   ____|       /       ||  | |           ||   ____|                            
        |  |__   |  |_)  |    |  |__   |  |__         |   (----`|  | `---|  |----`|  |__              Created by who0ze        
        |   __|  |      /     |   __|  |   __|         \   \    |  |     |  |     |   __|          https://github.com/who0ze              
        |  |     |  |\  \----.|  |____ |  |____    .----)   |   |  |     |  |     |  |____                             
        |__|     | _| `._____||_______||_______|   |_______/    |__|     |__|     |_______|                            
                                                                                                                    
        .______      ___       _______  _______         _______. _______     ___      .______        ______  __    __  
        |   _  \    /   \     /  _____||   ____|       /       ||   ____|   /   \     |   _  \      /      ||  |  |  | 
        |  |_)  |  /  ^  \   |  |  __  |  |__         |   (----`|  |__     /  ^  \    |  |_)  |    |  ,----'|  |__|  | 
        |   ___/  /  /_\  \  |  | |_ | |   __|         \   \    |   __|   /  /_\  \   |      /     |  |     |   __   | 
        |  |     /  _____  \ |  |__| | |  |____    .----)   |   |  |____ /  _____  \  |  |\  \----.|  `----.|  |  |  | 
        | _|    /__/     \__\ \______| |_______|   |_______/    |_______/__/     \__\ | _| `._____| \______||__|  |__| 
""")
    
    language = display_language_selection()
    domain = input("Enter the domain to scan (e.g., example.com): ").strip()
    main(domain, language)
