
import bs4
import requests

res = requests.get('https://steamcommunity.com/profiles/76561197988661740/friends/')
res.raise_for_status()

# save website to a html file
dl_file = open('download_data.html', 'wb')
for chunk in res.iter_content(10000):
    dl_file.write(chunk)
dl_file.close()
print('scrape file saved as download_data.html')

soup_file = open('download_data.html', 'rb')  # ! add rb here since file was saved wb
soup = bs4.BeautifulSoup(soup_file.read(), 'html5lib')

# save data as a list of strings (gamertag and status combined)
# ingame - ResultSet (list) of div classes
print('\n[In-game]')
in_game = soup.find_all('div', class_='selectable friend_block_v2 persona in-game')
in_game_lst = [', '.join(item.stripped_strings) for item in in_game]
if (len(in_game_lst)) == 0: print('None')
else: print('\n'.join(in_game_lst))

# online - ResultSet
print('\n[Online Friends]')
online = soup.find_all('div', class_='selectable friend_block_v2 persona online')
online_lst = [', '.join(item.stripped_strings) for item in online]
if (len(online_lst)) == 0: print('None')
else: print('\n'.join(online_lst))

# offline - ResultSet
print('\n[Offline Friends]')
offline = soup.find_all('div', class_='selectable friend_block_v2 persona offline')
offline_lst = [', '.join(item.stripped_strings) for item in offline]
if (len(offline_lst)) == 0: print('None')
else: print('\n'.join(offline_lst))

## use for saving list of tuples
# print('\n\n[Offline-tuple-generator-listcomp-saved-to list]\n')
# list2 = [tuple(item.stripped_strings) for item in offline]
# print(list2)


## offline-old way from downloadStream0web.py file
# offline = soup.find_all('div', class_='selectable friend_block_v2 persona offline')
# oFlist = []
# for i in range(len(offline)):
#     oFlist.append(', '.join(offline[i].stripped_strings))
# print('\n\n[Offline]\n')
# print('\n'.join(oFlist))

"""
NOTE: wrt .stripped_strings
is a generator object that can be used on the bs4 ResultSet object
it generates in memory all the strings in that ResultSet
the ResultSet being the result from a find, find_all, or select method of bs4
you can loop thru that memory space and print
or you can just join all the data in a tuple, list, etc without having to loop
since it is a generator set already (iterator by nature)
"""





