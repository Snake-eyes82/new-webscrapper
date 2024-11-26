import scrapy

class AutoWebScraper(scrapy.Spider):
    name = 'auto_scraper'

    def __init__(self, seed_url, criteria):
        super().__init__()
        self.start_urls = [seed_url]
        self.criteria = criteria

    def parse(self, response):
        # ... (same parsing logic as before)
                # Extract relevant content based on criteria
        for item in response.css('//p'):  # Adjust the CSS selector as needed
            text = item.extract()
            if self.criteria in text:
                yield {
                    'text': text,
                    'url': response.url
                }

        # Follow links to other pages
        for link in response.css('a::attr(href)'):
            yield response.follow(link, self.parse)