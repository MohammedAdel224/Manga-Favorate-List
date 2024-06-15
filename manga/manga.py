import httpx
from bs4 import BeautifulSoup, element
from abc import ABC, abstractmethod
import pandas as pd
from datetime import date


class Manga(ABC):
    def __init__(self, name: str, site: str, url: str, headers: dict | httpx.Headers = None):
        self.name: str = name
        self.site: str = site
        self.url: str = url
        self.__html: str | None = None
        self.__chapters_list: element.Tag | None = None
        self.__last_chapter: element.Tag | None = None
        self.headers: dict | httpx.Headers = headers
        self.error: str | None = None
    
    def request(self) -> None:
        try:
            client = httpx.Client(http2=True)
            response = client.get(self.url, headers=self.headers, timeout=250, follow_redirects=True)
        except Exception as exception:
            self.error = f'{exception}'
            self.__html = f'Error:\n{self.error}'
            print(self.__html)
            print(self.url, '\n')
        else:
            if response.status_code == 200:
                self.__html = response.text
            else:
                self.error = f'{response}'
                self.__html = f'Error:\n{self.error}'
                print(self.__html)
                print(self.url, '\n')
    
    @property
    def html(self) -> str:
        if self.__html == None:
            self.error = 'RequestDoesNotSendYet'
            return f'Error:\n{self.error}'
        return self.__html

    ######################### Start Chapters List #########################
    @abstractmethod
    def _find_chapters_list(self) -> element.Tag | None:
        pass
    
    def __set_chapters_list(self, value: element.Tag) -> None:
        self.__chapters_list = value
            
    @property
    def chapters_list(self) -> element.Tag:
        if self.__chapters_list:
            return self.__chapters_list
        if self.html.startswith('Error'):
            return BeautifulSoup(f'<title>{self.html}</title>', 'html.parser')
        soup = BeautifulSoup(self.html, 'html.parser')
        chapters_list = self._find_chapters_list(soup)
        if chapters_list:
            self.__set_chapters_list(chapters_list)
        else:
            self.error = 'Chapers list does not found'
            self.__set_chapters_list(BeautifulSoup('<title>Error:\n{self.error}</title>', 'html.parser'))
        return self.__chapters_list
    ######################### End Chapters List ##########################

    ######################### Start last Chapter #########################
    @abstractmethod
    def _find_last_chapter(self, chapters_list: element.Tag) -> element.Tag:
        pass

    def __set_last_chapter(self, value: element.Tag) -> None:
        self.__last_chapter = value
    
    @property
    def last_chapter(self) -> element.Tag:
        if self.chapters_list.title: #If it has a title then there is an error
            return self.chapters_list
        last_chapter = self._find_last_chapter(self.chapters_list)
        if last_chapter:
            while last_chapter:
                if self.get_chapter_number(last_chapter) != -2: #chapter number founded
                    self.__set_last_chapter(last_chapter)
                    break
                else:
                    last_chapter = self._find_previous_chapter(last_chapter)
        else:
            self.error = 'Chapers list is empty'
            self.__set_last_chapter(BeautifulSoup('<title>Error:\n{self.error}</title>', 'html.parser'))
        return self.__last_chapter
    ########################### End last Chapter ###########################
    
    ######################### Start Chapter Number #########################
    @abstractmethod
    def _find_chapter_number(self, chapter: element.Tag) -> float:
        pass
    
    def get_chapter_number(self, chapter: element.Tag) -> float | None:
        if chapter.title: #If it has a title then there is an error
            return -1
        chapter_number = self._find_chapter_number(chapter)
        if chapter_number is not None:
            return chapter_number
        print(f'{self.name}: Chapter number not found\n{self.url}')
        return -2
    ######################### End Chapter Number #########################
    
    ######################### Start Chapter Date #########################
    @abstractmethod
    def _find_chapter_date(chapter: element.Tag) -> date:
        pass

    def get_chapter_date(self, chapter: element.Tag) -> date:
        if chapter.title: #If it has a title then there is an error
            return -1
        return self._find_chapter_date(chapter)
    ########################## End Chapter Date ##########################

    ######################### Start New Chapters #########################
    @abstractmethod
    def _find_previous_chapter(chapter: element.Tag) -> element.Tag:
        pass
    
    @abstractmethod
    def _get_chapter_href(chapter: element.Tag) -> str:
        pass

    def get_new_chapters(self, last_chapter_read_number: float) -> pd.DataFrame:
        new_chapters = {'name':[], 'chapter_number':[], 'site':[]}
        if self.last_chapter.title: #If it has a title then there is an error
            return pd.DataFrame(new_chapters)
        chapter = self.last_chapter
        chapter_number = self.get_chapter_number(chapter)
        if chapter_number < 0:
            return pd.DataFrame(new_chapters)
        chapter_link = self._get_chapter_href(chapter)
        while chapter_number > last_chapter_read_number:
            new_chapters['name'].append(self.name)
            new_chapters['chapter_number'].append(f'=HYPERLINK("{chapter_link}", "{chapter_number}")')
            new_chapters['site'].append(self.site)

            chapter = self._find_previous_chapter(chapter)
            if chapter:
                chapter_number = self.get_chapter_number(chapter)
                chapter_link = self._get_chapter_href(chapter)
            else:
                break
        return pd.DataFrame(new_chapters)
    ########################## End New Chapters ##########################