from bs4 import element
from datetime import date
from .manga import Manga
from .functions import date_from_Arabic


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
           'Cookie': 'cf_clearance=e6lty.bpLXCjC9jcRDM3v5yvAC.QEbOSELom6hrFhl0-1714825098-1.0.1.1-EiFwSkDrPL2EZ4dyRxUfMRwL3q.WZbgOTrmarr5P9S9hVJG6iwZTtJKn5kqvK1eflY9TcPBPfNT3aBYFSZoAcQ; __eoi=ID=a7488dce439ed962:T=1714421086:RT=1714825106:S=AA-AfjYq7C8zS6OLHfsqutX--aev'}

class AreaScans(Manga):
    def __init__(self, name: str, url: str):
        super().__init__(name, 'Area Scans', url, headers)

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