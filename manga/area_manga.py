from bs4 import element
from datetime import date
from .manga import Manga
from .functions import date_from_Arabic



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
           'Cookie': 'cf_clearance=MLYVR5huclTEVfxu2jfj_pZkx0YRIVofy0BdvZtk57I-1718476686-1.0.1.1-14Af_9ddANTXFUV0M97uaKDDikFESSD4zQy2NiuFVSBTptg6bwXYgvIMDOr4R5.M0rqtqBo5V5.c1FHeHMWWSQ; __gads=ID=fbfe1fd7ff17deba:T=1713735229:RT=1718476686:S=ALNI_Ma6eZLV-VnIsVfzlnyp9IseZ7MTeA; __gpi=UID=00000d637a028ac9:T=1713735229:RT=1718476686:S=ALNI_MbfX39Jh0_AwaC916-ZKszWoOX5rw; __eoi=ID=03293e77b404879e:T=1712184050:RT=1718476686:S=AA-AfjZXO7vlTE4j0CRK2ajBUdbw; _cc_id=b679b9528209654cddda9c3e7d36bd05; panoramaId_expiry=1719081487444; panoramaId=cee4995199076cfbb981bcbec7634945a702a271d3e138a4afe20535c0e4608a; panoramaIdType=panoIndiv; cto_bundle=yr5_BF9jVE5VdHlEbWpqJTJGaHd6cDRiNFlEajRMdWM4UzRxZ1MzTFBaTklvTVpST0tHSEpmaThNZHE1S1lUcFo0cjVTbUJwZ0xDaVRoOEUlMkI4Rkt5RlFXRnJRNlBnSHV0VTFYZUZFcTNsSkk4UUhHRjdjYUFZdGNnMm5TMSUyRjZSRUoyYmQ4Qk1semJwTDh5UXFPaCUyQll5SFRtZ3NDQSUzRCUzRA; FCNEC=%5B%5B%22AKsRol_gRe0J3I0jpo3JC1RYcwWCravOFb5TYX75pE5zyvcLxlqBCf3Uzi5Gaix4LZFPRl0n2VhAwZfqpr785yi0zMfD_i692WuvSTVJwJ8IZg1GZi0AP7oGnqrTlID0aVMCtZDstJsuP2YNSTC4ZykPpEV2x32xiA%3D%3D%22%5D%5D'}


class AreaManga(Manga):
    def __init__(self, name: str, url: str, last_chapter_read_number: float):
        super().__init__(name, 'Area Manga', url, last_chapter_read_number, headers)

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
    
    @staticmethod
    def _get_chapter_href(chapter: element.Tag) -> str:
        return chapter.find('a')['href']