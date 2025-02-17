from scrapper.processor import parse_category_page, parse_product_page
from core.scrapper_helper import transform_anchor
from core.constants import BASE_URL
import scrapy


EXTENSIONS_TO_IGNORE = [
    ".css",".js",".png",".jpg",".jpeg",".gif",".pdf",".doc",
    ".docx",".xls",".xlsx",".zip",".rar",".mp3",".mp4",".avi",
    ".mov",".webp",".svg",".ico",".tiff",".bmp",".woff",".ico",
]

class MainSpider(scrapy.Spider):
    name = "my_spider"
    start_urls = [BASE_URL]
    visited_urls = set()

    def parse(self, response):
        print(f"🔍 Checking [{len(self.visited_urls)}] {response.url}")

        if response.url in self.visited_urls:
            return

        self.visited_urls.add(response.url)

        content_type = response.headers.get("Content-Type", b"").decode(
            "utf-8", "ignore"
        )
        if "text/html" not in content_type:
            self.logger.info(
                f"Ignorando URL no HTML: {response.url} (Content-Type: {content_type})"
            )
            return

        if "category" in response.url:
            parse_category_page(response)
        else:
            parse_product_page(response)

        urls = response.css("::attr(href)").getall()

        valid_urls = []
        valid_category_urls = []
        for anchor in urls:
            url = transform_anchor(response.url, anchor)

            should_ignore = any(
                url.lower().endswith(ext) for ext in EXTENSIONS_TO_IGNORE
            )

            if (
                url.startswith(BASE_URL)
                and url not in self.visited_urls
                and "#" not in url
                and not should_ignore
            ):
                if "category" in url:
                    valid_category_urls.append(url)
                else:
                    valid_urls.append(url)

        combined_urls = valid_category_urls + valid_urls
        for url in combined_urls:
            yield scrapy.Request(url, callback=self.parse, errback=self.errback_handler)

    def errback_handler(self, failure):
        self.logger.error(f"Error al procesar: {failure.request.url} - {repr(failure)}")
