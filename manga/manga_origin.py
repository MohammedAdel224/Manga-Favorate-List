import httpx
from bs4 import BeautifulSoup, element
from datetime import datetime, date
from .manga import Manga
from .functions import get_number_from_text, date_from_Arabic


class MangaOrigin(Manga):
    def __init__(self, name: str, url: str):
        super().__init__(name, 'Manga Origin', url)

    def _find_chapters_list(self, soup: element.Tag) -> element.Tag | None:
        return soup.find('div', class_='blog-posts hfeed container')

    def _find_last_chapter(self, chapters_list: element.Tag) -> element.Tag:
        return chapters_list.find('article')
    
    @staticmethod
    def _find_chapter_number(chapter: element.Tag) -> float:
        chapter_title = chapter.find('div', class_='r-snippetized').text.strip()
        return get_number_from_text(chapter_title)

    @staticmethod
    def _find_chapter_date(chapter: element.Tag) -> date:
        chapter_date = chapter.find('time')
        if chapter_date:
            return datetime.strptime(chapter_date['datetime'], '%Y-%m-%dT%H:%M:%S%z').date()
        else:
            return date.today()

    def _find_previous_chapter(self, chapter: element.Tag) -> element.Tag | None:
        previous_chapter = chapter.find_next_sibling()
        if previous_chapter == None:
            next_page_button = chapter.find_parent().find_parent().find('a', title='المزيد من المشاركات')
            if next_page_button == None:
                return None
            next_page_url = next_page_button['href']
            next_page = BeautifulSoup(httpx.get(next_page_url), 'html.parser')
            chapter_list = self._find_chapters_list(next_page)
            previous_chapter = chapter_list.find('article')
        return previous_chapter
    
    @staticmethod
    def _get_chapter_href(chapter: element.Tag) -> str:
        return chapter.findAll('a')[1]['href']