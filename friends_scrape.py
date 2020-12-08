import bs4
import requests
import argparse



parser = argparse.ArgumentParser(description='Retreive a Steam Friends List.')
parser.add_argument('steam_num', metavar='S', type=int, help='numeric steam id')
args = parser.parse_args()


# https://steamcommunity.com/profiles/76561197988661740/friends/
url_prefix = 'https://steamcommunity.com/profiles/'
# url_steam_num = 76561197988661740  #args.steam_num
url_steam_num = args.steam_num
url_suffix = '/friends/'
url = url_prefix + str(url_steam_num) + url_suffix


res = requests.get(url)
res.raise_for_status()


# save website to a html file
dl_file = open('download_data.html', 'wb')
for chunk in res.iter_content(10000):
    dl_file.write(chunk)
dl_file.close()
print('scrape file for {} saved as download_data.html'.format(url_steam_num))


soup_file = open('download_data.html', 'rb')  # ! add rb here since file was saved wb
soup = bs4.BeautifulSoup(soup_file.read(), 'html5lib')


# In-game - ResultSet
print('\n[In-game]')
in_game = soup.find_all('div', class_='selectable friend_block_v2 persona in-game')
in_game_lst = [', '.join(item.stripped_strings) for item in in_game]
if (len(in_game_lst)) == 0:
    print('None')
else:
    print('\n'.join(in_game_lst))


# online - ResultSet
print('\n[Online Friends]')
online = soup.find_all('div', class_='selectable friend_block_v2 persona online')
online_lst = [', '.join(item.stripped_strings) for item in online]
if (len(online_lst)) == 0:
    print('None')
else:
    print('\n'.join(online_lst))


# offline - ResultSet
print('\n[Offline Friends]')
offline = soup.find_all('div', class_='selectable friend_block_v2 persona offline')
offline_lst = [', '.join(item.stripped_strings) for item in offline]
if (len(offline_lst)) == 0:
    print('None')
else:
    print('\n'.join(offline_lst))
