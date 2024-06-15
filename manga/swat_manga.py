from bs4 import element
from datetime import date
from .manga import Manga
from .functions import get_number_from_text, date_from_Arabic


class SwatManga(Manga):
    def __init__(self, name: str, url: str):
        super().__init__(name, 'Swat Manga', url)

    def _find_chapters_list(self, soup: element.Tag) -> element.Tag | None:
        previous_tag = soup.find('div', class_='releases')
        if previous_tag:
            return previous_tag.find_next_sibling()
        return None

    def _find_last_chapter(self, chapters_list: element.Tag) -> element.Tag:
        return chapters_list.find('li')
    
    @staticmethod
    def _find_chapter_number(chapter: element.Tag) -> float:
        chapter_title = chapter['data-num'].strip()
        return get_number_from_text(chapter_title)

    @staticmethod
    def _find_chapter_date(chapter: element.Tag) -> date:
        chapter_date = chapter.find('span', class_='chapter-date')
        if chapter_date:
            return date_from_Arabic(chapter_date)
        else:
            return date.today()

    @staticmethod
    def _find_previous_chapter(chapter: element.Tag) -> element.Tag | None:
        return chapter.find_next_sibling()