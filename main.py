import manga
import pygsheets
import pandas as pd
from threading import Thread
################################


################################
def update_manga(manga: pd.Series) -> tuple[pd.Series, pd.Series]:
    if manga.sources_last_chapter > manga.last_chapter:
        return manga.sources_last_chapter, manga.sources_last_chapter_date
    elif (manga.sources_last_chapter == manga.last_chapter) & (manga.sources_last_chapter_date < manga.last_chapter_date):
        return manga.sources_last_chapter, manga.sources_last_chapter_date
    else:
        return manga.last_chapter, manga.last_chapter_date
################################


################################
print('(01/19) Client authorizing...')
client = pygsheets.authorize(service_account_file=r'key.json')

print('(02/19) Manga sheet openning...')
sheet = client.open('Manga')
print('(03/19) Manga worksheet openning...')
manga_worksheet = sheet.worksheet('title', 'Manga')
print('(04/19) Sources worksheet openning...')
sources_worksheet = sheet.worksheet('title', 'Temp')

print('(05/19) manga_df preparing...')
manga_df = manga_worksheet.get_as_df()
manga_df.set_index('id', inplace=True)
manga_df['last_chapter_date'] = manga_df['last_chapter_date'].astype('datetime64[ms]')

print('(06/19) sources_df preparing...')
sources_df = sources_worksheet.get_as_df()
sources_df = sources_df[sources_df['site_name'] != "Gmanga"]
sources_df['manga'] = sources_df.apply(lambda source: manga.create(source.manga_name, source.site_name, source.url), axis=1, result_type='expand')
max_threads = 20
number_of_sources = len(sources_df['manga'])
for i in range(0, number_of_sources, max_threads):
    threads = []
    for m in sources_df['manga'][i:i+max_threads]:
        thread = Thread(target=m.request)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print(f'{i+len(sources_df["manga"][i:i+max_threads])} link is done')
sources_df[['last_chapter', 'last_chapter_date', 'new_chapters']] = (pd.merge(sources_df, manga_df['last_read'], how='left', left_on='manga_id', right_index=True)
                                                                       .apply(lambda source: (source.manga.get_chapter_number(source.manga.last_chapter), 
                                                                                              source.manga.get_chapter_date(source.manga.last_chapter),
                                                                                              source.manga.get_new_chapters(source.last_read)), 
                                                                              axis=1, result_type='expand'))
sources_df['last_chapter_date'] = sources_df['last_chapter_date'].astype('datetime64[ms]')

print('(07/19) last_chapters preparing...')
last_chapters = sources_df.groupby('manga_id')['last_chapter'].agg('max').rename('sources_last_chapter')
print('(08/19) sources_df and last_chapters merging...')
sources_last_chapters_df = pd.merge(sources_df, last_chapters, how='left', on='manga_id')
print('(09/19) last chapter filtering...')
sources_last_chapters_df = sources_last_chapters_df[sources_last_chapters_df['last_chapter'] == sources_last_chapters_df['sources_last_chapter']]
print('(10/19) last_chapters_date preparing...')
sources_last_chapters_date_df = sources_last_chapters_df.groupby('manga_id')['last_chapter_date'].agg('min').rename('sources_last_chapter_date')
print('(11/19) last chapter date filtering...')
update = pd.merge(sources_last_chapters_df, sources_last_chapters_date_df, how='left', on='manga_id').set_index('manga_id')

print('(12/19) Creating a data frame for comparing this update with the previous update...')
temp = manga_df[['last_chapter', 'last_chapter_date']].join(update[['sources_last_chapter', 'sources_last_chapter_date']], how='left').drop_duplicates()
print('(13/19) comparing...')
manga_df[['last_chapter', 'last_chapter_date']] = temp.apply(lambda manga: update_manga(manga), axis=1, result_type='expand')
print('(15/19) formating...')
manga_df['last_chapter_date'] = manga_df['last_chapter_date'].dt.strftime('%B %d, %Y')

print('(16/19) manga_worksheet updating...')
manga_worksheet.set_dataframe(manga_df[['last_chapter', 'last_chapter_date']], 'D1', copy_index=False)

print('(17/19) new_chapters_df dataframe creating...')
new_chapters_df = pd.concat(sources_df['new_chapters'].tolist()).reset_index(drop=True)
new_chapters_df = new_chapters_df.sort_values(by=['name', 'chapter_number'], ascending=[True, False])
print('(18/19) New_chapters updating...')
# sheet.worksheet('title', 'New_chapters').clear()
# sheet.worksheet('title', 'New_chapters').set_dataframe(new_chapters_df, 'A1', copy_index=False)

print('(19/19) Errors reporting...')
errors = pd.DataFrame()
errors[['Error', 'Site', 'URL']] = sources_df[['manga']].apply(lambda s: ( s.manga.error, s.manga.site, s.manga.url),  axis=1, result_type='expand')
errors.dropna(inplace=True)
errors = errors.sort_values(['Site', 'Error'])
print(errors)
# sheet.worksheet('title', 'Errors').clear()
# sheet.worksheet('title', 'Errors').set_dataframe(errors, 'A1', copy_index=False)
print('DONE!!')
