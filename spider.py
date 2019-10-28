import re
import scrapy

from markdownify import markdownify as md


class Spider(scrapy.Spider):
    name = "Over the parapet"
    start_urls = [
        "http://overtheparapet.blogspot.com/2017/02/and-we-will-still-get-shock-or-two.html"
    ]

    def parse(self, response):
        body_html = response.css("div.post-body").get()
        # remove comments
        body_html = re.sub(r"(?=<!--)([\s\S]*?)-->", "", body_html)
        body_md = md(body_html)

        yield {
            "title": response.css("h3.entry-title::text").get().strip(),
            "date": response.xpath("//abbr[@itemprop='datePublished']/@title").get(),
            "content": body_md.strip(),
            "original_url": response.request.url,
        }

        next_page = response.css('a.blog-pager-older-link::attr("href")').get()

        if next_page is not None:
            yield response.follow(next_page, self.parse)
