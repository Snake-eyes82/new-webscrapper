import scrapy
from urllib.parse import urlparse
import tkinter as tk
from tkinter import ttk
from scrapy.crawler import CrawlerProcess

class AutoWebScraper(scrapy.Spider):
    name = 'auto_scraper'

    def __init__(self, seed_url, criteria):
        super().__init__()
        self.start_urls = [seed_url]
        self.criteria = criteria
        self.visited_urls = set()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={'User-Agent': self.user_agent}, callback=self.parse)
            # yield scrapy.Request(url, headers={'User-Agent': 'Your User-Agent'}, callback=self.parse)

    def parse(self, response):
        # Extract relevant content based on user input
        for selector in self.criteria.split():
            for item in response.css(selector):
                text = item.extract_first()
                if text and response.url not in self.visited_urls:
                    self.visited_urls.add(response.url)
                    yield {
                        'text': text,
                        'url': response.url
                    }
                    print(f"Found text: {text} at URL: {response.url}")

        # Follow links, filtering by domain and depth
        for link in response.css('a::attr(href)'):
            parsed_url = urlparse(link)
            if parsed_url.netloc.endswith('.google.com') and parsed_url.netloc not in self.visited_urls:  # Adjust domain filtering as needed
                yield response.follow(link, callback=self.parse, meta={'depth': response.meta.get('depth', 0) + 1})

    def should_follow(self, link):
        # Implement a more flexible filtering strategy, e.g., based on domain TLDs
        parsed_url = urlparse(link)
        allowed_tlds = ['com', 'org', 'net', 'edu', 'gov']  # Add more TLDs as needed

        return parsed_url.netloc.endswith(tuple(allowed_tlds))

    # def parse(self, response):
    #     # ... (rest of the parsing logic remains the same)

        # Yield extracted data to be processed by the GUI
        # for item in extracted_data:
        #     yield item

class MyPipeline(object):

    def __init__(self):
        self.results = []

    def open_spider(self, spider):
        self.results = []

    def process_item(self, item, spider):
        self.results.append(item)
        return item

    def close_spider(self, spider):
        global extracted_data
        extracted_data = self.results

def start_scraping():
    seed_url = entry_seed_url.get()
    criteria = entry_criteria.get()

    process = CrawlerProcess (settings={'ITEM_PIPELINES': {'your_project.pipelines.MyPipeline': 300}})
    process.crawl(AutoWebScraper, seed_url=seed_url, criteria=criteria)
    process.start()

    # Update the output text box (assuming extracted data is in a list)
    output_text.delete('1.0', tk.END)
    for item in extracted_data:
        output_text.insert(tk.END, f"Text: {item['text']}\nURL: {item['url']}\n\n")

    def parse(self, response):
        # Extract relevant content based on user input
        for selector in self.criteria.split():
            for item in response.css(selector):
                text = item.extract_first()
                if text and response.url not in self.visited_urls:
                    self.visited_urls.add(response.url)
                    yield {
                        'text': text,
                        'url': response.url
                    }
                    print(f"Found text: {text} at URL: {response.url}")

        # Follow links, filtering by domain and depth
        for link in response.css('a::attr(href)'):
            parsed_url = urlparse(link)
            if parsed_url.netloc.endswith('.example.com') and parsed_url.netloc not in self.visited_urls:  # Adjust domain filtering as needed
                yield response.follow(link, callback=self.parse, meta={'depth': response.meta.get('depth', 0) + 1})

    def should_follow(self, link):
        # Implement a more flexible filtering strategy, e.g., based on domain TLDs
        parsed_url = urlparse(link)
        allowed_tlds = ['com', 'org', 'net', 'edu', 'gov']  # Add more TLDs as needed
        return parsed_url.netloc.endswith(tuple(allowed_tlds))

    root = tk.Tk()
    root.title("Web Scraper")

# Create input fields
    label_seed_url = tk.Label(root, text="Seed URL:")
    label_seed_url.pack()
    entry_seed_url = tk.Entry(root)
    entry_seed_url.pack()

    label_criteria = tk.Label(root, text="Criteria:")
    label_criteria.pack()
    entry_criteria = tk.Entry(root)
    entry_criteria.pack()

# Create a button to start the scraping process
    start_button = tk.Button(root, text="Start Scraping", command=start_scraping)
    start_button.pack()

# Create an output text box
    output_text = tk.Text(root)
    output_text.pack()

    root.mainloop()