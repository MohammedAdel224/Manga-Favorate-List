Needed Libraries:
- pandas
- pygsheets
- bs4
- httpx

Available Sites:
ID	| Name			| URL									| Notes
----|---------------|---------------------------------------|------
1	| Mangalek		| https://like-manga.net/				|
2	| Ares Manga	| https://fl-ares.com/					|
3	| Manhua Scarlet| https://scarmanga.com/				|
4	| Azora Manga	| https://azoramoon.com/				|
5	| Swat Manga	| https://swatscans.com/				|
6	| Team X		| https://teamoney.site/				|
7	| Gmanga		| https://gmanga.app/					| This site stoped working after collecting manga's links but before writing the scraping code
8	| Lava Scans	| https://lavascans.com/				| 
9	| Area Manga	| https://ar.kenmanga.com/  			| Cookie need to update manualy
10	| Hijala		| https://hijala.com/					|
11	| Area Scans	| https://ar.areascans.org/				| Cookie need to update manualy
12	| Galaxy		| https://gxcomic.xyz/				    |
13	| Dilar			| https://dilar.tube/					| Need to run JavaScript to load chapters
14	| Manga Origin	| https://teammangaorigin.blogspot.com/	|
15	| Manga Rose	| https://mangarose.net/				|
16  | 4U Scans      | https://4uscans.com/                  |

Manga Table:
Column Name 		| Data Type | Desctiption
--------------------|-----------|------------
id          		| Int		|
name        		| Text		| Mange name
last_read   		| Float		| The number of the last chapter read
last_chapter		| Float		| The number of the last chapter released
last_chapter_date	| Date		| The date when the last chapter released, `MMMM dd, yyyy`

Sites Table:
Column Name	| Data Type | Desctiption
------------|-----------|------------
id          | Int		|
name        | Text		| Site name
url			| Text		|

Sources Table:
Column Name	| Data Type | Desctiption
------------|-----------|------------
id          | Int		|
manga_id	| Int		|
site_id		| Int		|
url			| Text		| Domain + the ful path
path		| Int		| Path without domain
manga_name	| Text		|
site_name	| Text		|

New_Chapters Table:
Column Name		| Data Type | Desctiption
----------------|-----------|------------
name        	| Text		| Manga name
chapter_number	| Float		| Chapter number with hyperlink
site			| Text		| Site name

Errors Table:
Column Name	| Data Type | Desctiption
------------|-----------|------------
Error		| Text		|
Site		| Text		|
URL			| Text		| 

Limitations:
- Can't Pass Cloudflare and CAPTCHA
- Can't Run JavaScript before scraping
- Can't update cookies automaticly
