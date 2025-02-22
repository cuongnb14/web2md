import requests
import trafilatura
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
import threading
import argparse
import time

def fetch_markdown(url):
    """Download the page and convert it to Markdown"""
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        extracted_text = trafilatura.extract(response.text, output_format="markdown")
        return extracted_text if extracted_text else "Failed to extract content"
    return "Failed to fetch page"

def get_internal_links(url, base_domain):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    
    links = set()
    for a_tag in soup.find_all("a", href=True):
        link = urljoin(url, a_tag["href"])
        if urlparse(link).netloc == base_domain:
            links.add(link)
    
    return links

def crawl_page(link, lock, output_file):
    """Fetch content and save to file safely"""
    print(f"crawling: {link}")
    markdown_content = fetch_markdown(link)
    
    # Write to file with thread safety
    with lock:
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"# {link}\n\n" + markdown_content + "\n\n")

def crawl_site(start_url, output_file, max_workers):
    """Crawl the main page and its internal links """
    start_time = time.time()
    base_domain = urlparse(start_url).netloc
    visited = set()
    lock = threading.Lock()
    
    # Open file in write mode to clear previous content
    with open(output_file, "w", encoding="utf-8") as f:
        pass
    
    print(f"crawling: {start_url}")
    markdown_main = fetch_markdown(start_url)
    
    # Write main page content first
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(f"# {start_url}\n\n" + markdown_main + "\n\n")
    visited.add(start_url)

    internal_links = get_internal_links(start_url, base_domain)
    links_to_crawl = [link for link in internal_links if link not in visited]
    
    # Crawl each internal link concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(crawl_page, link, lock, output_file): link for link in links_to_crawl}
        for future in futures:
            future.result()  # Wait for all threads to complete
    
    total_time = time.time() - start_time
    print(f"\n✅ Done crawling. Content saved to {output_file}")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Total pages crawled: {len(links_to_crawl)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl a website and extract Markdown content")
    parser.add_argument("start_url", type=str, help="Starting URL to crawl")
    parser.add_argument("--output_file", type=str, default="crawled_content.md", help="Output file name")
    parser.add_argument("--max_workers", type=int, default=5, help="Number of concurrent workers")
    
    args = parser.parse_args()
    crawl_site(args.start_url, args.output_file, args.max_workers)
