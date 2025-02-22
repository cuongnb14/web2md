import argparse
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse

import requests
import trafilatura
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class Web2Md:
    def __init__(self, start_url, output_file, max_workers, is_rendering, is_only_main):
        self.start_url = start_url
        self.base_domain = urlparse(start_url).netloc

        self.output_file = output_file
        self.max_workers = max_workers
        self.is_rendering = is_rendering
        self.is_only_main = is_only_main

    def _get_internal_links(self, url, content):
        soup = BeautifulSoup(content, "html.parser")

        links = set()
        for a_tag in soup.find_all("a", href=True):
            link = urljoin(url, a_tag["href"])
            if urlparse(link).netloc == self.base_domain:
                links.add(link)

        return links

    def _fetch_page(self, url):
        """Download the page and convert it to Markdown"""
        is_rendering = self.is_rendering

        if self.is_only_main and url != self.start_url:
            is_rendering = False

        try:
            if is_rendering:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    page.goto(url)

                    # Get page content
                    content = page.content()

                    browser.close()
            else:
                response = requests.get(url, timeout=10)
                content = response.content
        except Exception as e:
            print(f'Error when crawl: {url}: {e}')
            content = ''

        extracted_text = trafilatura.extract(content, output_format="markdown")
        if not extracted_text:
            extracted_text = "Failed to extract content"

        internal_links = self._get_internal_links(url, content)

        return extracted_text, internal_links

    def _crawl_page(self, url, lock):
        """Fetch content and save to file safely"""
        print(f"crawling: {url}")
        markdown_content, internal_links = self._fetch_page(url)

        # Write to file with thread safety
        with lock:
            with open(self.output_file, "a", encoding="utf-8") as f:
                f.write(f"# {url}\n\n" + markdown_content + "\n\n")

    def crawl_site(self):
        """Crawl the main page and its internal links"""
        start_time = time.time()
        visited_urls = set()
        lock = threading.Lock()

        # Open file in write mode to clear previous content
        with open(self.output_file, "w", encoding="utf-8") as f:
            pass

        print(f"crawling: {self.start_url}")
        markdown_main, internal_links = self._fetch_page(self.start_url)

        # Write main page content first
        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write(f"# {self.start_url}\n\n" + markdown_main + "\n\n")
        visited_urls.add(self.start_url)

        urls_to_crawl = [url for url in internal_links if url not in visited_urls]

        # Crawl each internal link concurrently
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._crawl_page, url, lock): url
                for url in urls_to_crawl
            }
            for future in futures:
                future.result()  # Wait for all threads to complete

        total_time = time.time() - start_time
        print(f"\n✅ Done crawling. Content saved to {self.output_file}")
        print(f"Total time taken: {total_time:.2f} seconds")
        print(f"Total pages crawled: {len(urls_to_crawl)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Crawl a website and extract Markdown content"
    )
    parser.add_argument("start_url", type=str, help="Starting URL to crawl")
    parser.add_argument(
        "--output_file", type=str, default="crawled_content.md", help="Output file name"
    )
    parser.add_argument(
        "--max_workers", type=int, default=5, help="Number of concurrent workers"
    )
    parser.add_argument(
        "--rendering", action="store_true", help="Enable JS rendering mode"
    )
    parser.add_argument(
        "--only-main",
        action="store_true",
        help="Enable JS rendering mode only start page",
    )

    args = parser.parse_args()

    web2md = Web2Md(
        args.start_url,
        args.output_file,
        args.max_workers,
        is_rendering=args.rendering,
        is_only_main=args.only_main,
    )
    web2md.crawl_site()
