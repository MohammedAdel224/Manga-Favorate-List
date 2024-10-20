from .azura_manga import AzoraManga
from .manhua_scarlet import ManhuaScarlet
from .mangalek import Mangalek
from .swat_manga import SwatManga
from .team_x import TeamX
from .lava_scans import LavaScans
from .area_manga import AreaManga
from .hijala import Hijala
from .area_scans import AreaScans
from .ares_manga import AresManga
from .galaxy import Galaxy
from .dilar import Dilar
from .manga_origin import MangaOrigin
from .manga_rose import MangaRose
from .for_u_scans import ForUScans


sites = {'Azora Manga': AzoraManga, 
         'Ares Manga': AresManga,
         'Manhua Scarlet': ManhuaScarlet,
         'Mangalek': Mangalek,
         'Swat Manga': SwatManga,
         'Team X': TeamX,
         'Lava Scans': LavaScans,
         'Area Manga': AreaManga,
         'Area Scans': AreaScans,
         'Hijala':  Hijala, 
         'Galaxy': Galaxy, 
         'Dilar': Dilar, 
         'Manga Origin': MangaOrigin, 
         'Manga Rose': MangaRose, 
         "4U Scans": ForUScans}

def create(name: str, site: str, url: str, last_chapter_read_number: float):
    return sites[site](name, url, last_chapter_read_number) 

if __name__ == '__main__':
    manga = create('Wind Breaker', 'Hijala', 'https://hijala.com/wind-breaker/', 490)
    manga.request()
    print(manga.last_chapter.encode('utf-8'))
    print(manga.get_chapter_number(manga.last_chapter))
    print(manga.get_chapter_date(manga.last_chapter))
    print(manga.get_new_chapters(490))