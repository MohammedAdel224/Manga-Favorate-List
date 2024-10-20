import httpx
from bs4 import BeautifulSoup, element
from datetime import datetime, date
from .manga import Manga
from .functions import period_to_date


class ForUScans(Manga):
    def __init__(self, name: str, url: str, last_chapter_read_number: float):
        super().__init__(name, '4U Scans', url, last_chapter_read_number)

    def _find_chapters_list(self, soup: element.Tag) -> element.Tag | None:
        chapters_list = soup.find('div', id='chapters')
        return chapters_list

    def _find_last_chapter(self, chapters_list: element.Tag) -> element.Tag:
        return chapters_list.find('a')
    
    @staticmethod
    def _find_chapter_number(chapter: element.Tag) -> float:
        return float(chapter['title'])

    @staticmethod
    def _find_chapter_date(chapter: element.Tag) -> date:
        try:
            chapter_date: str = chapter.find('span').findNextSibling().text.strip()
            if chapter_date.endswith("ago"):
                return period_to_date(chapter_date)
            else:
                return datetime.strptime(chapter_date, '%b %d, %Y').date()
        except:
            return date.today()

    @staticmethod
    def _find_previous_chapter(chapter: element.Tag) -> element.Tag | None:
        return chapter.find_next_sibling()
    
    @staticmethod
    def _get_chapter_href(chapter: element.Tag) -> str:
        return chapter['href']