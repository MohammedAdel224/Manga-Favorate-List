from bs4 import element
from datetime import date
from .manga import Manga
from .functions import date_from_Arabic


class ManhuaScarlet(Manga):
    def __init__(self, name: str, url: str):
        super().__init__(name, 'Manhua Scarlet', url)

    def _find_chapters_list(self, soup: element.Tag) -> element.Tag | None:
        chapters_list_container = soup.find('div', id='chapterlist')
        if chapters_list_container:
            return chapters_list_container.find('ul')
        return None

    def _find_last_chapter(self, chapters_list: element.Tag) -> element.Tag:
        return chapters_list.find('li')
    
    @staticmethod
    def _find_chapter_number(chapter: element.Tag) -> float:
        return float(chapter['data-num'])

    @staticmethod
    def _find_chapter_date(chapter: element.Tag) -> date:
        chapter_date = chapter.find('span', class_='chapterdate')
        if chapter_date:
            return date_from_Arabic(chapter_date)
        else:
            return date.today()

    @staticmethod
    def _find_previous_chapter(chapter: element.Tag) -> element.Tag | None:
        return chapter.find_next_sibling()