from bs4 import element
from datetime import date
from .manga import Manga
from .functions import get_number_from_text, date_from_Arabic

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
           'Cookie': '__SPK_UID=990630fa-df27-11ee-a26d-8acb09218344; Location=Egypt; FooterLoc=Egypt; _pubcid=cea2be85-d43c-450d-9307-8f40c2e2f9ef; _pubcid_cst=zix7LPQsHA%3D%3D; panoramaId_expiry=1715027517721; _cc_id=b679b9528209654cddda9c3e7d36bd05; panoramaId=fb0459d3faa71c2dc9f96f62232116d5393854895af597c8e155651f0a08bf0a; cto_bundle=GJBnhl9jVE5VdHlEbWpqJTJGaHd6cDRiNFlEajF0b1lKeUJLNm9tMkdBTTAzbG8yMmtNVEM2QU9rMGpNQVdRYjVDQ0Q1U09WNTYxMUt5JTJCWFJHbHVrSmVJc1hOJTJGJTJCNFJ6RzdlS0xhdGg3JTJCSURYc1RmNHElMkJrRHZJM3NaeXM3OVNhSko1U2xFaENNNllZNEp2cmV3S0VKZ01kaUo3VnclM0QlM0Q; cto_bidid=tBpZbF92b20lMkZ6cDdybElHSCUyQmpiT0NFTWNsQkJFUUtaZGNSNVoyeVhTVSUyQkIyZXFqdmxGViUyRnhsVW9Cbm1BWVNnaXBJN1plNjJRU05LTFRIU3p2WllvYlQzUVY4ckVqJTJCQUIlMkZJMnRvWVlWN3E2JTJCaE1BJTNE; cto_dna_bundle=bDVIeF9jVE5VdHlEbWpqJTJGaHd6cDRiNFlEanpvWW40QmolMkIyUlNkYVJ1MGVCT00lMkJpbTFNQzJsd28lMkJiOTFnRzdGRmhmUlhNRmNmUUNaJTJGckljbzRoTnhobndKVGclM0QlM0Q; cf_clearance=VgTESz0_yhvMRGo_ENy2a_AIHaiNT0n5KZzww_M0fKI-1714824975-1.0.1.1-7P.O1sFufiRVmO19AGCr2wfKzHbnDhuMxrKVwZIEAgCyGkHs.IF1zL17dWR5xGlp62T8LNi91_1gS3mMtWmCsQ'}

class AresManga(Manga):
    def __init__(self, name: str, url: str):
        super().__init__(name, 'Ares Manga', url, headers)

    def _find_chapters_list(self, soup: element.Tag) -> element.Tag | None:
        chapters_list_container = soup.find('div', id='chapterlist')
        if chapters_list_container:
            return chapters_list_container.find('ul')
        return None

    def _find_last_chapter(self, chapters_list: element.Tag) -> element.Tag:
        return chapters_list.find('li')
    
    @staticmethod
    def _find_chapter_number(chapter: element.Tag) -> float:
        chapter_title = chapter.find('span', class_='chapternum').text.strip()
        return get_number_from_text(chapter_title)

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
    
    @staticmethod
    def _get_chapter_href(chapter: element.Tag) -> str:
        return chapter.find('a')['href']