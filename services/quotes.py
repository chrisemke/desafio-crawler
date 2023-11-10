"""Web scraping code challenge
Copyright (C) 2023 Christian G. Semke.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from httpx import get
from parsel import Selector


class QuotesToScrape:
    """Scrape elements from quotes.toscrape.com."""

    def get_quotes(self, tag: str = '', page: int = 1) -> list[dict]:
        """Get all quotes from a page."""
        if tag != '':
            tag = f'/tag/{tag}'
        selector = Selector(
            text=get(f'https://quotes.toscrape.com{tag}/page/{page}').text
        )
        quotes = selector.xpath('//div[@class="quote"]')
        return_quotes = []
        for quote in quotes:
            author = quote.xpath('//span[text()="by "]')
            author_dict = {
                'author': author.xpath(
                    '//small[@class="author"]/text()'
                ).get(),
                'about_path': author.xpath('//a').attrib['href'],
            }
            tags = quote.xpath('//div[@class="tags"]/a[@class="tag"]')
            tags_dict = [
                {'tag': tag.xpath('text()').get(), 'link': tag.attrib['href']}
                for tag in tags
            ]

            return_quotes.append(
                {
                    'quote': quote.xpath('//span[@class="text"]/text()').get(),
                    'author': author_dict,
                    'tags': tags_dict,
                }
            )

        return return_quotes

    def get_author(self, about_path: str) -> dict:
        """Get all author information."""
        selector = Selector(
            text=get(f'https://quotes.toscrape.com{about_path}').text
        )
        author = {
            'name': selector.xpath('//h3[@class="author-title"]/text()').get(),
            'birth_date': selector.xpath(
                '//span[@class="author-born-date"]/text()'
            ).get(),
            'birthplace': selector.xpath(
                '//span[@class="author-born-location"]/text()'
            ).get(),
            'description': selector.xpath(
                '//div[@class="author-description"]/text()'
            ).get(),
        }
        return author
