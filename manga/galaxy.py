import httpx
from bs4 import element, BeautifulSoup
from datetime import date
from .manga import Manga
from .functions import get_number_from_text, arabic_period_to_date

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
               'Cookie': 'XSRF-TOKEN=eyJpdiI6IndQRjRJbmhuWnhTNm80ZUdvMHBSWEE9PSIsInZhbHVlIjoiSUpRdWt1TVdrVDRvY3BUQlBUc1BhU1pPZGJnQVlrVzh2cXJIQkdqRk9ua2lTejlPUFpVZC9lanRYMzVCVFlGbzVXWmVFT1RqVGZRc2djMDZsZUJra0g4SXpaVkg2Wjk0ZzVVdmJHeG83eGpMdFVZa0xTZFpoeXNoZzNLY01Vbm8iLCJtYWMiOiIyYWU3MTMwNjk2MmM5MzFlMDkzMzFiYjFmNzFiOGY5YjAzMmFkMDM5ZjY0ODk4M2E2ZDVjZGNmNmJjZDkzYWI4IiwidGFnIjoiIn0%3D; galaxymanga_session=eyJpdiI6Ii8zc2VlV1dkaVZjMjFIaFBKUWxoSEE9PSIsInZhbHVlIjoiSnFIU2ZsUkxSRHhjaUZWZ1lrY3Y0UVhWanFiN2NZUkRJT0hHVHNnRjNFWjNXZE1UZXNLMmx5Q1Mwa011cVM1SmJmc2lmbjhWb1YrODA1T0JUZk5qbzZEckl5aXdCMk9GckJ6Si85VWtibk51RVhlTmJoRUkvUHB3bkM5REkxaEsiLCJtYWMiOiI5N2M5YmFmYThlNDk1OWNkYWFjYmEzMTM5YTdmZDhmOTYyMDU1ZjY5NzRlYmNhMzQ2NzA2MjcwN2JjNzQ0MTAzIiwidGFnIjoiIn0%3D; _ga_G8Q07EYW7C=GS1.1.1718484976.1.0.1718484976.0.0.0; _ga=GA1.1.74901047.1718484976; cf_clearance=g6bi7b4qeyB4GqnBIvsDseV0D_YxF_vkhJzpFCDxNoo-1718484975-1.0.1.1-ST7l_CrDaArbNp5H1PD9C.u80pc_VfGwSNmCcSHc3S.HOgkL8fwdVnzLY9Zov0AWFkLMCYJrVIbatGs.YSgLnA; __gads=ID=737139a2179dc550:T=1718484975:RT=1718484975:S=ALNI_Mb6XBiotIvFvVdNaG3tD-u-nBesuw; __gpi=UID=00000e47f7257ba9:T=1718484975:RT=1718484975:S=ALNI_MbRA-hCkqVEsjpkiK6CLnaQDWBVCw; __eoi=ID=c1e2bbb3bd4e4fd6:T=1718484975:RT=1718484975:S=AA-Afjbna3Ogp_WBmQZkxunHuBN_; FCNEC=%5B%5B%22AKsRol-Yds0FqVG-YToyJt3AKcfs9v4TGvT49VG6psfl_jJfrZxMhbLrHn53t56_JmWpt7jswV3yFurPcLda2aMTLjtO6FzQzzhmQtG3Ql5VqwnpQq4UtxfvYqVGB1OHWe8_VbWfhZOWJDjSrZMnPIbfC8uKE1faUA%3D%3D%22%5D%5D'}

class Galaxy(Manga):
    def __init__(self, name: str, url: str, last_chapter_read_number: float):
        super().__init__(name, 'Galaxy', url, last_chapter_read_number, headers)

    def _change_url(self) -> None:
        client = httpx.Client(http2=True)
        response = client.get(self.url, headers=self.headers, timeout=250, follow_redirects=True)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            manga_div = soup.find("div", class_="px-1 font-poppins line-clamp-1 hover:opacity-70")
            if manga_div:
                manga_a = manga_div.find("a")
                if manga_a:
                    manga_path = manga_a["href"]
                    self.url = self.url.split("/search?")[0] + manga_path
    
    def _find_chapters_list(self, soup: element.Tag) -> element.Tag | None:
        return soup.find('div', class_='md:grid-cols-2')

    def _find_last_chapter(self, chapters_list: element.Tag) -> element.Tag:
        return chapters_list.find('a')
    
    @staticmethod
    def _find_chapter_number(chapter: element.Tag) -> float:
        chapter_title = chapter.find('span', class_='font-normal').string.strip()
        return get_number_from_text(chapter_title)

    @staticmethod
    def _find_chapter_date(chapter: element.Tag) -> date:
        try:
            chapter_date = chapter.find('span', class_='text-xs opacity-50').string.strip()
            return arabic_period_to_date(chapter_date)
        except:
            return date.today()

    @staticmethod
    def _find_previous_chapter(chapter: element.Tag) -> element.Tag | None:
        return chapter.find_next_sibling()
    
    def _get_chapter_href(self, chapter: element.Tag) -> str:
        return self.url.split("/series/")[0] + chapter['href']