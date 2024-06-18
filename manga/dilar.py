from bs4 import element
from datetime import date
from .manga import Manga
from .functions import get_number_from_text

class Dilar(Manga):
    def __init__(self, name: str, url: str):
        super().__init__(name, 'Dilar', url)

    def _find_chapters_list(self, soup: element.Tag) -> element.Tag | None:
        chapters_list_container = soup.find('div', id='ui divided list')
        if chapters_list_container:
            return chapters_list_container.find('div')
        return None

    def _find_last_chapter(self, chapters_list: element.Tag) -> element.Tag:
        return chapters_list.find('div')
    
    @staticmethod
    def _find_chapter_number(chapter: element.Tag) -> float:
        chapter_title = chapter.find('a').string.strip()
        return get_number_from_text(chapter_title)

    @staticmethod
    def _find_chapter_date(chapter: element.Tag) -> date:
        chapter_date_container = chapter.find('div', class_='sub-text')
        if chapter_date_container:
            try:
                chapter_date = chapter_date_container.text.split()[1]
                return chapter_date
            except:
                return date.today()
        return date.today()

    @staticmethod
    def _find_previous_chapter(chapter: element.Tag) -> element.Tag | None:
        return chapter.find_next_sibling()
    
    @staticmethod
    def _get_chapter_href(chapter: element.Tag) -> str:
        return chapter.find('a')['href']