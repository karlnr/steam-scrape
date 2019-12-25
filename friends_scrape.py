
import bs4
import requests

res = requests.get('https://steamcommunity.com/profiles/76561197988661740/friends/')
res.raise_for_status

## save website to a html file
dlFile = open('download_data.html', 'wb')
for chunk in res.iter_content(10000):
    dlFile.write(chunk)
dlFile.close()
print('scrape file saved as download_data.html')

# make soup
soupFile = open('download_data.html', 'rb') # ! MUST add rb here since file was saved wb
soup = bs4.BeautifulSoup(soupFile.read(), 'html5lib')

# test 2.c - save data as a list of strings (gamertag and status combined)
# ingame - ResultSet (list) of div classes
print('\n\n[In-game]\n')
ingame = soup.find_all('div', class_='selectable friend_block_v2 persona in-game')
ingList = [', '.join(item.stripped_strings) for item in ingame]
print('\n'.join(ingList))

# online - ResultSet
print('\n\n[Online]\n')
online = soup.find_all('div', class_='selectable friend_block_v2 persona online')
onlList = [', '.join(item.stripped_strings) for item in online]
print('\n'.join(onlList))

# offline - ResultSet
print('\n\n[Offline]\n')
offline = soup.find_all('div', class_='selectable friend_block_v2 persona offline')
offList = [', '.join(item.stripped_strings) for item in offline]
print('\n'.join(offList))

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





