import scrapy
from urllib.parse import urlparse

class AutoWebScraper(scrapy.Spider):
    name = 'auto_scraper'

    def __init__(self, seed_url, criteria):
        super().__init__()
        self.start_urls = [seed_url]
        self.criteria = criteria

#     def __init__(self, seed_url, criteria):
#         super().__init__()
#         self.start_urls = [seed_url]
#         self.criteria = criteria
#         self.allowed_domains = ['example.com']  # Adjust allowed domains
# # Define the user-agent
#         self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={'User-Agent': self.user_agent})

    def parse(self, response):
        # Extract relevant content based on user input
        for selector in self.criteria.split():
            for item in response.css(selector):
                text = item.extract_first()
                if text:
                    yield {
                        'text': text,
                        'url': response.url
                    }
                    print(f"Found text: {text} at URL: {response.url}")

        # Follow links, filtering by domain
        for link in response.css('a::attr(href)'):
            if self.should_follow(link.extract()):
                yield response.follow(link, callback=self.parse)

    # def parse(self, response):
    #     # Extract relevant content
    #     for item in response.css('//p'):
    #         text = item.extract_first()
    #         if self.criteria in text:
    #             yield {
    #                 'text': text,
    #                 'url': response.url
    #             }
    #             print(f"Found text: {text} at URL: {response.url}")

    #     # Follow links, filtering by domain
    #     for link in response.css('a::attr(href)'):
    #         if self.should_follow(link.extract()):
    #             yield response.follow(link, callback=self.parse)

def should_follow(self, link):
        # Implement a more flexible filtering strategy, e.g., based on domain TLDs
        parsed_url = urlparse(link)
        allowed_tlds = ['com', 'org', 'net', 'edu', 'gov']  # Add more TLDs as needed
        return parsed_url.netloc.endswith(tuple(allowed_tlds))

    # def should_follow(self, link):
    #     parsed_url = urlparse(link)
    #     return parsed_url.netloc in self.allowed_domains