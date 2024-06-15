import httpx
from bs4 import BeautifulSoup, element
from datetime import datetime, date
from .manga import Manga


class TeamX(Manga):
    def __init__(self, name: str, url: str):
        super().__init__(name, 'Team X', url)

    def _find_chapters_list(self, soup: element.Tag) -> element.Tag | None:
        chapters_list_container = soup.find('div', class_='ts-chl-collapsible-content')
        if chapters_list_container:
            return chapters_list_container.find('ul')
        return None

    def _find_last_chapter(self, chapters_list: element.Tag) -> element.Tag:
        return chapters_list.find('li')
    
    @staticmethod
    def _find_chapter_number(chapter: element.Tag) -> float:
        return float(chapter.find_all('div', class_='epl-num')[1].text.split()[1])

    @staticmethod
    def _find_chapter_date(chapter: element.Tag) -> date:
        chapter_date = chapter.find('div', class_='epl-date').text.strip()
        if chapter_date:
            return datetime.strptime(chapter_date, '%Y-%m-%d %H:%M:%S').date()
        else:
            return date.today()

    def _find_previous_chapter(self, chapter: element.Tag) -> element.Tag | None:
        previous_chapter = chapter.find_next_sibling()
        if previous_chapter == None:
            next_page_button = chapter.find_parent().find_parent().find_parent().find_parent().find('a', rel='next')
            if next_page_button == None:
                return None
            next_page_url = next_page_button['href']
            next_page = BeautifulSoup(httpx.get(next_page_url), 'html.parser')
            chapter_list = self._find_chapters_list(next_page)
            previous_chapter = chapter_list.find('li')
        return previous_chapter