from .azura_manga import AzoraManga
from .manhua_scarlet import ManhuaScarlet
from .mangalek import Mangalek
from .swat_manga import SwatManga
from .team_x import TeamX
from .thunder_scans import ThunderScans
from .area_manga import AreaManga
from .hijala import Hijala
from .area_scans import AreaScans
from .ares_manga import AresManga
from .galaxy import Galaxy
from .dilar import Dilar


sites = {'Azora Manga': AzoraManga, 
         'Ares Manga': AresManga,
         'Manhua Scarlet': ManhuaScarlet,
         'Mangalek': Mangalek,
         'Swat Manga': SwatManga,
         'Team X': TeamX,
         'Thunder Scans': ThunderScans,
         'Area Manga': AreaManga,
         'Area Scans': AreaScans,
         'Hijala':  Hijala, 
         'Galaxy': Galaxy, 
         'Dilar': Dilar}

def create(name: str, site: str, url: str):
    return sites[site](name, url) 

if __name__ == '__main__':
    manga = create('Wind Breaker', 'Hijala', 'https://hijala.com/wind-breaker/')
    manga.request()
    print(manga.last_chapter.encode('utf-8'))
    print(manga.get_chapter_number(manga.last_chapter))
    print(manga.get_chapter_date(manga.last_chapter))
    print(manga.get_new_chapters(490))