import scrapy
from urllib.parse import urlparse
import tkinter as tk
from tkinter import ttk
from scrapy.crawler import CrawlerProcess

class AutoWebScraper(scrapy.Spider):
    name = "google_scraper"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

    def __init__(self, seed_url, criteria):
        super().__init__()
        self.start_urls = [seed_url]
        self.criteria = criteria
        self.visited_urls = set()

    def start_requests(self):
                yield scrapy.Request("https://www.google.com",
                headers={'User-Agent': self.user_agent}, callback=self.parse)
        # for url in self.start_urls:
        #     yield scrapy.Request(url, headers={'User-Agent': self.user_agent}, callback={self.parse})

    def parse(self, response):
        # Attempt to parse using CSS selectors
        items = response.css('selector::text').extract()

        # Handle non-text responses
        if not items:
            # Check the content type
            try:
                content_type = response.headers.get('Content-Type', '').decode().split(';')[0]
            # content_type = response.headers.get('Content-Type', '').split(';')[0]
            except UnicodeDecodeError:
      # Handle potential decoding issues (e.g., log an error)
                pass

            if content_type in ['image/jpeg', 'image/png', 'application/pdf', ...]:
                # Download the file
                filename = response.url.split('/')[-1]
                with open(filename, 'wb') as f:
                    f.write(response.body)

        # Yield items or requests
        for item in items:
            yield {'item': item}

            next_page_links = response.css('a::attr(href)').getall()
        # Follow links to other pages
            for next_page in next_page_links:
                if not next_page.startswith('mailto:'):
                    yield response.follow(next_page, self.parse)
        # for next_page in response.css('a::attr(href)').extract():
        #     yield response.follow(next_page, self.parse)

    # def parse(self, response):
    #     for selector in self.criteria.split():
    #         for item in response.css(selector):
    #             text = item.extract_first()
    #             if text and response.url not in self.visited_urls:
    #                 self.visited_urls.add(response.url)
    #                 yield {
    #                     'text': text,
    #                     'url': response.url
    #                 }

    #     for link in response.css('a::attr(href)'):
    #         parsed_url = urlparse(link.get())
    #         # parsed_url = urlparse(link)
    #         if parsed_url.netloc.endswith('.google.com') and parsed_url.netloc not in self.visited_urls:
    #             yield response.follow(link, callback=self.parse, meta={'depth': response.meta.get('depth', 0) + 1})

    def should_follow(self, link):
        parsed_url = urlparse(link.get())
        # parsed_url = urlparse(link)
        allowed_tlds = ['com', 'org', 'net', 'edu', 'gov']
        return parsed_url.netloc.endswith(tuple(allowed_tlds))

class MyPipeline(object):
    def __init__(self):
        self.results = []

    def open_spider(self, spider):
        self.results = []

    def process_item(self, item, spider):
        self.results.append(item)
        return item

    def close_spider(self, spider):
        return self.results

def start_scraping():
    seed_url = entry_seed_url.get()
    criteria = entry_criteria.get()

    # process = CrawlerProcess(settings={'ITEM_PIPELINES': {'your_project.pipelines.MyPipeline': 300}})
    process = CrawlerProcess()
    process.crawl(AutoWebScraper, seed_url=seed_url, criteria=criteria)
    scraped_data = process.start()

    output_text.delete('1.0', tk.END)
    for item in scraped_data:
        output_text.insert(tk.END, f"Text: {item['text']}\nURL: {item['url']}\n\n")
    else:
        output_text.insert(tk.END, "No data was scraped.")

# Create the main window
root = tk.Tk()
root.title("Web Scraper")

# Create input fields
label_seed_url = tk.Label(root, text="Seed URL:")
label_seed_url.grid(row=0, column=0)
entry_seed_url = tk.Entry(root)
entry_seed_url.grid(row=0, column=1)

label_criteria = tk.Label(root, text="Criteria:")
label_criteria.grid(row=1, column=0)
entry_criteria = tk.Entry(root)
entry_criteria.grid(row=1, column=1)

# Create a button to start the scraping process
start_button = tk.Button(root, text="Start Scraping", command=start_scraping)
start_button.grid(row=2, columnspan=2)

# Create an output text box
output_text = tk.Text(root)
output_text.grid(row=3, columnspan=2)

root.mainloop()