import bs4
import requests
import argparse

x_auth = 'SECRET'  # api authentication key
headers = {'X-AUTH': x_auth}
api_prefix = 'https://xapi.us/v2'

def main():
    xuid_default = 2611015498272098
    gamertag_default = 'vnillagoriIIa'

    xuid = get_xuid(gamertag_default)
    friends_json = get_friends_json(xuid)
    friends_json_status = append_presence_json(friends_json)

    for d in friends_json_status:
        presence_json = get_presence_json(xuid)
        friend = [d['id'], d['Gamertag'], d['status']]
        print(friend)


def get_xuid(gamertag):
    api_xuid_suffix = '/xuid/{}'.format(gamertag)  # This is the XUID for a specified Gamertag (Xbox Account User ID)
    res_xuid = requests.get(api_prefix + api_xuid_suffix, headers=headers)
    res_xuid.raise_for_status()
    xuid = res_xuid.json()
    return xuid


def get_friends_json(xuid):
    api_friends_suffix = '/{}/friends'.format(xuid)  # This is the friends information for a specified XUID
    res_friends = requests.get(api_prefix + api_friends_suffix, headers=headers)
    res_friends.raise_for_status()
    friends_json = res_friends.json()
    return friends_json


def get_presence_json(xuid):
    # {"xuid":2611015498272098,"state":"Offline"}
    api_presence_suffix = '/{}/presence'.format(xuid)
    res_presence = requests.get(api_prefix + api_presence_suffix, headers=headers)
    res_presence.raise_for_status()
    presence_json = res_presence.json()
    return presence_json


# friends_json_debug_one = [{'id': 2533274807364943, 'hostId': 2533274807364943, 'Gamertag': 'manger d',
#                            'GameDisplayName': 'manger d', 'AppDisplayName': 'manger d', 'Gamerscore': 25988,
#                            'GameDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=z951ykn43p4FqWbbFvR2Ec.8vbDhj8G2Xe7JngaTToBrrCmIEEXHC9UNrdJ6P7KIm2RQQtfSX9jMSatOYowOzHw85AZLC27nsz23FMcGDOLegZ9.jGJFEkelaXl1zuDI&format=png',
#                            'AppDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=z951ykn43p4FqWbbFvR2Ec.8vbDhj8G2Xe7JngaTToBrrCmIEEXHC9UNrdJ6P7KIm2RQQtfSX9jMSatOYowOzHw85AZLC27nsz23FMcGDOLegZ9.jGJFEkelaXl1zuDI&format=png',
#                            'AccountTier': 'Gold', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'http://dlassets.xboxlive.com/public/content/ppl/colors/00012.json',
#                            'TenureLevel': 13, 'isSponsoredUser': False},]


def append_presence_json(friends_json):
    for d in friends_json:
        xuid = d['id']
        gamertag = d['Gamertag']
        presence_json = get_presence_json(xuid)
        d['status'] = presence_json['state']
    return friends_json



def steam_scraper():
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
    print('scrape file for {} saved as download_data.html'.format(xuid))



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





# friends_json_debug_full = [{'id': 2533274807364943, 'hostId': 2533274807364943, 'Gamertag': 'manger d', 'GameDisplayName': 'manger d', 'AppDisplayName': 'manger d', 'Gamerscore': 25988, 'GameDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=z951ykn43p4FqWbbFvR2Ec.8vbDhj8G2Xe7JngaTToBrrCmIEEXHC9UNrdJ6P7KIm2RQQtfSX9jMSatOYowOzHw85AZLC27nsz23FMcGDOLegZ9.jGJFEkelaXl1zuDI&format=png', 'AppDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=z951ykn43p4FqWbbFvR2Ec.8vbDhj8G2Xe7JngaTToBrrCmIEEXHC9UNrdJ6P7KIm2RQQtfSX9jMSatOYowOzHw85AZLC27nsz23FMcGDOLegZ9.jGJFEkelaXl1zuDI&format=png', 'AccountTier': 'Gold', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'http://dlassets.xboxlive.com/public/content/ppl/colors/00012.json', 'TenureLevel': 13, 'isSponsoredUser': False},
#                       {'id': 2533274799413553, 'hostId': 2533274799413553, 'Gamertag': 'zzoSCUBAozz', 'GameDisplayName': 'zzoSCUBAozz', 'AppDisplayName': 'zzoSCUBAozz', 'Gamerscore': 39579, 'GameDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=Hr2eiH8yWKd4q_oa.xgbMnOHX9HRDEMKjkwIswRQCT4jE324VJHdcCl8SxAtO7EPv017sozs5RTWvzwhMQyPH_Re0aPl57groPtcMEoKj0vucheidUE.WEnDENGn7UmIr1iQx438kbRl7IjIaQGfrUK420VxanwJlAWFpcpki9M-&format=png', 'AppDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=Hr2eiH8yWKd4q_oa.xgbMnOHX9HRDEMKjkwIswRQCT4jE324VJHdcCl8SxAtO7EPv017sozs5RTWvzwhMQyPH_Re0aPl57groPtcMEoKj0vucheidUE.WEnDENGn7UmIr1iQx438kbRl7IjIaQGfrUK420VxanwJlAWFpcpki9M-&format=png', 'AccountTier': 'Gold', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'https://dlassets-ssl.xboxlive.com/public/content/ppl/colors/00011.json', 'TenureLevel': 13, 'isSponsoredUser': False},
#                       {'id': 2789282983510157, 'hostId': 2789282983510157, 'Gamertag': 'McCracken5', 'GameDisplayName': 'McCracken5', 'AppDisplayName': 'McCracken5', 'Gamerscore': 23736, 'GameDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=mHGRD8KXEf2sp2LC58XhBQKNl2IWRp.J.q8mSURKUUe1JVMI2s9.h8P4P7.oGaMi0Vw7v906sS35eD181hjLxb6SwbpJ6Onj1gCDxtP55mM-&background=0xababab&format=png', 'AppDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=mHGRD8KXEf2sp2LC58XhBQKNl2IWRp.J.q8mSURKUUe1JVMI2s9.h8P4P7.oGaMi0Vw7v906sS35eD181hjLxb6SwbpJ6Onj1gCDxtP55mM-&background=0xababab&format=png', 'AccountTier': 'Gold', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'http://dlassets.xboxlive.com/public/content/ppl/colors/00012.json', 'TenureLevel': 16, 'isSponsoredUser': False},
#                       {'id': 2533274880080504, 'hostId': 2533274880080504, 'Gamertag': 'ThaddeusPrime1', 'GameDisplayName': 'ThaddeusPrime1', 'AppDisplayName': 'ThaddeusPrime1', 'Gamerscore': 38910, 'GameDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=wHwbXKif8cus8csoZ03RW3apWESZjav65Yncai8aRmVbSlZ3zqRpg1sdxEje_JmFlsCH851QV03uNA_q543uL.A5uBY8UGeYl.qKaqcqglWDh8N1MGg_EwMOSnbGEORNNerv33dMXOETHfXwH0EpyGXEqEydVLyOkkl7sdRYBuA-&format=png', 'AppDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=wHwbXKif8cus8csoZ03RW3apWESZjav65Yncai8aRmVbSlZ3zqRpg1sdxEje_JmFlsCH851QV03uNA_q543uL.A5uBY8UGeYl.qKaqcqglWDh8N1MGg_EwMOSnbGEORNNerv33dMXOETHfXwH0EpyGXEqEydVLyOkkl7sdRYBuA-&format=png', 'AccountTier': 'Silver', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'http://dlassets.xboxlive.com/public/content/ppl/colors/00003.json', 'TenureLevel': 0, 'isSponsoredUser': False},
#                       {'id': 2533274846576174, 'hostId': 2533274846576174, 'Gamertag': 'MrSilent 420', 'GameDisplayName': 'MrSilent 420', 'AppDisplayName': 'MrSilent 420', 'Gamerscore': 52841, 'GameDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=wHwbXKif8cus8csoZ03RW8ke8ralOdP9BGd4wzwl0MJ9z6QzuGwZjtvbE7sSsMVWkdN.MGgUp_Toe2uLFjkQ3cZvcwg7jzEXymFYLt_i5lADzA0iyiKC4SqfuYoygR1qjP_hK3StERRYbuogjxHg624RUYSzx9mR0_M9D7D4Ovw-&format=png', 'AppDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=wHwbXKif8cus8csoZ03RW8ke8ralOdP9BGd4wzwl0MJ9z6QzuGwZjtvbE7sSsMVWkdN.MGgUp_Toe2uLFjkQ3cZvcwg7jzEXymFYLt_i5lADzA0iyiKC4SqfuYoygR1qjP_hK3StERRYbuogjxHg624RUYSzx9mR0_M9D7D4Ovw-&format=png', 'AccountTier': 'Gold', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'https://dlassets-ssl.xboxlive.com/public/content/ppl/colors/00017.json', 'TenureLevel': 11, 'isSponsoredUser': False},
#                       {'id': 2535449467275183, 'hostId': 2535449467275183, 'Gamertag': 'Corgi Kohmander', 'GameDisplayName': 'Corgi Kohmander', 'AppDisplayName': 'Corgi Kohmander', 'Gamerscore': 9645, 'GameDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=8Oaj9Ryq1G1_p3lLnXlsaZgGzAie6Mnu24_PawYuDYIoH77pJ.X5Z.MqQPibUVTcS9jr0n8i7LY1tL3U7AiafYLdFPsGSCt2INPq2MzbGVD6vrQ1qkmzUGwb0NJZ9WKe&format=png', 'AppDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=8Oaj9Ryq1G1_p3lLnXlsaZgGzAie6Mnu24_PawYuDYIoH77pJ.X5Z.MqQPibUVTcS9jr0n8i7LY1tL3U7AiafYLdFPsGSCt2INPq2MzbGVD6vrQ1qkmzUGwb0NJZ9WKe&format=png', 'AccountTier': 'Gold', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'http://dlassets.xboxlive.com/public/content/ppl/colors/00012.json', 'TenureLevel': 5, 'isSponsoredUser': False},
#                       {'id': 2533274811261107, 'hostId': 2533274811261107, 'Gamertag': 'AngusMaximus89', 'GameDisplayName': 'AngusMaximus89', 'AppDisplayName': 'AngusMaximus89', 'Gamerscore': 22020, 'GameDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=z951ykn43p4FqWbbFvR2Ec.8vbDhj8G2Xe7JngaTToBrrCmIEEXHC9UNrdJ6P7KId46ktn4AUxk.ghIPeRshxXIh9vFRWxvg3EjVB5wItza8UzuLI19uRK.GD4huCeBU&format=png', 'AppDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=z951ykn43p4FqWbbFvR2Ec.8vbDhj8G2Xe7JngaTToBrrCmIEEXHC9UNrdJ6P7KId46ktn4AUxk.ghIPeRshxXIh9vFRWxvg3EjVB5wItza8UzuLI19uRK.GD4huCeBU&format=png', 'AccountTier': 'Gold', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'http://dlassets.xboxlive.com/public/content/ppl/colors/00001.json', 'TenureLevel': 10, 'isSponsoredUser': False},
#                       {'id': 2533274919754969, 'hostId': 2533274919754969, 'Gamertag': 'MikeGz82', 'GameDisplayName': 'MikeGz82', 'AppDisplayName': 'MikeGz82', 'Gamerscore': 1650, 'GameDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=mHGRD8KXEf2sp2LC58XhBQKNl2IWRp.J.q8mSURKUUeQDtobyN5xmswIs1qggzrwQxYUhJaxndAbl4sfze_GRT11c3fBYjXx5IeWxbIOCLQ-&background=0xababab&format=png', 'AppDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=mHGRD8KXEf2sp2LC58XhBQKNl2IWRp.J.q8mSURKUUeQDtobyN5xmswIs1qggzrwQxYUhJaxndAbl4sfze_GRT11c3fBYjXx5IeWxbIOCLQ-&background=0xababab&format=png', 'AccountTier': 'Silver', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'http://dlassets.xboxlive.com/public/content/ppl/colors/00000.json', 'TenureLevel': 0, 'isSponsoredUser': False},
#                       {'id': 2533274857116189, 'hostId': 2533274857116189, 'Gamertag': 'ki11er r0b', 'GameDisplayName': 'ki11er r0b', 'AppDisplayName': 'ki11er r0b', 'Gamerscore': 2700, 'GameDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=rwljod2fPqLqGP3DBV9F_yK9iuxAt3_MH6tcOnQXTc_J5xosqot.bzehqnXOJ2Jo64xjH2q_zGSKdsshMOmvwfEealMWEJyUqT9mS60BZec-&background=0xababab&format=png', 'AppDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=rwljod2fPqLqGP3DBV9F_yK9iuxAt3_MH6tcOnQXTc_J5xosqot.bzehqnXOJ2Jo64xjH2q_zGSKdsshMOmvwfEealMWEJyUqT9mS60BZec-&background=0xababab&format=png', 'AccountTier': 'Silver', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'http://dlassets.xboxlive.com/public/content/ppl/colors/00002.json', 'TenureLevel': 0, 'isSponsoredUser': False},
#                       {'id': 2533274813592659, 'hostId': 2533274813592659, 'Gamertag': 'iamquarteyog', 'GameDisplayName': 'iamquarteyog', 'AppDisplayName': 'iamquarteyog', 'Gamerscore': 410, 'GameDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=rwljod2fPqLqGP3DBV9F_yK9iuxAt3_MH6tcOnQXTc.G0ejc9nZ5dqA1.6JgzphlEml5wKJ8S8.lVMkCQXyajwMukqYvPFbBAg8OL0stvdk-&background=0xababab&format=png', 'AppDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=rwljod2fPqLqGP3DBV9F_yK9iuxAt3_MH6tcOnQXTc.G0ejc9nZ5dqA1.6JgzphlEml5wKJ8S8.lVMkCQXyajwMukqYvPFbBAg8OL0stvdk-&background=0xababab&format=png', 'AccountTier': 'Silver', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'http://dlassets.xboxlive.com/public/content/ppl/colors/00000.json', 'TenureLevel': 0, 'isSponsoredUser': False},
#                       {'id': 2533274799609131, 'hostId': 2533274799609131, 'Gamertag': 'H0 Sheezy', 'GameDisplayName': 'H0 Sheezy', 'AppDisplayName': 'H0 Sheezy', 'Gamerscore': 23478, 'GameDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=mHGRD8KXEf2sp2LC58XhBQKNl2IWRp.J.q8mSURKUUdTlD3UQV1n6kXo7spL0qbQNmIDhmvv9qwiVnNNywMx8VxE8XBN9J6bJRdq2lQ5e60-&background=0xababab&format=png', 'AppDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=mHGRD8KXEf2sp2LC58XhBQKNl2IWRp.J.q8mSURKUUdTlD3UQV1n6kXo7spL0qbQNmIDhmvv9qwiVnNNywMx8VxE8XBN9J6bJRdq2lQ5e60-&background=0xababab&format=png', 'AccountTier': 'Silver', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'http://dlassets.xboxlive.com/public/content/ppl/colors/00000.json', 'TenureLevel': 0, 'isSponsoredUser': False},
#                       {'id': 2533274811146636, 'hostId': 2533274811146636, 'Gamertag': 'DAVID DA HUT', 'GameDisplayName': 'DAVID DA HUT', 'AppDisplayName': 'DAVID DA HUT', 'Gamerscore': 10781, 'GameDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=rwljod2fPqLqGP3DBV9F_yK9iuxAt3_MH6tcOnQXTc9McDbLpJwByqiKdqLbG7.4ExxRk17SVTdgr34OmGORiew8dzu35l2q9rkmJ7c3nZQ-&background=0xababab&format=png', 'AppDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=rwljod2fPqLqGP3DBV9F_yK9iuxAt3_MH6tcOnQXTc9McDbLpJwByqiKdqLbG7.4ExxRk17SVTdgr34OmGORiew8dzu35l2q9rkmJ7c3nZQ-&background=0xababab&format=png', 'AccountTier': 'Silver', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'http://dlassets.xboxlive.com/public/content/ppl/colors/00000.json', 'TenureLevel': 0, 'isSponsoredUser': False},
#                       {'id': 2620397997482445, 'hostId': 2620397997482445, 'Gamertag': 'CLOBBIT', 'GameDisplayName': 'CLOBBIT', 'AppDisplayName': 'CLOBBIT', 'Gamerscore': 22242, 'GameDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=mHGRD8KXEf2sp2LC58XhBQKNl2IWRp.J.q8mSURKUUdlbzvMOlffvBfX5bAtNExgsm9QsaW_wB.Sel.y9rwpLbMdmG.e5Ejg.K52TTljeAA-&background=0xababab&format=png', 'AppDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=mHGRD8KXEf2sp2LC58XhBQKNl2IWRp.J.q8mSURKUUdlbzvMOlffvBfX5bAtNExgsm9QsaW_wB.Sel.y9rwpLbMdmG.e5Ejg.K52TTljeAA-&background=0xababab&format=png', 'AccountTier': 'Silver', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'http://dlassets.xboxlive.com/public/content/ppl/colors/00000.json', 'TenureLevel': 0, 'isSponsoredUser': False},
#                       {'id': 2533274809403780, 'hostId': 2533274809403780, 'Gamertag': 'Finalnickname', 'GameDisplayName': 'Finalnickname', 'AppDisplayName': 'Finalnickname', 'Gamerscore': 7550, 'GameDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=rwljod2fPqLqGP3DBV9F_yK9iuxAt3_MH6tcOnQXTc9HX.51AmQz_GzQjh2f2Jm4j0lNth5gUqRw7gmKndW2skOxDQkPx1Kfh.UfEWm7LyI-&background=0xababab&format=png', 'AppDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=rwljod2fPqLqGP3DBV9F_yK9iuxAt3_MH6tcOnQXTc9HX.51AmQz_GzQjh2f2Jm4j0lNth5gUqRw7gmKndW2skOxDQkPx1Kfh.UfEWm7LyI-&background=0xababab&format=png', 'AccountTier': 'Silver', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'http://dlassets.xboxlive.com/public/content/ppl/colors/00000.json', 'TenureLevel': 0, 'isSponsoredUser': False},
#                       {'id': 2609675141229278, 'hostId': 2609675141229278, 'Gamertag': 'Hextro', 'GameDisplayName': 'Hextro', 'AppDisplayName': 'Hextro', 'Gamerscore': 27904, 'GameDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=rwljod2fPqLqGP3DBV9F_yK9iuxAt3_MH6tcOnQXTc9dx8KzX4e2Qj5rzQAYmpZplDajY2MCh1qZLRKUCvYZAOXC6ZaFLj.nhXdT6mkyqyQ-&background=0xababab&format=png', 'AppDisplayPicRaw': 'http://images-eds.xboxlive.com/image?url=rwljod2fPqLqGP3DBV9F_yK9iuxAt3_MH6tcOnQXTc9dx8KzX4e2Qj5rzQAYmpZplDajY2MCh1qZLRKUCvYZAOXC6ZaFLj.nhXdT6mkyqyQ-&background=0xababab&format=png', 'AccountTier': 'Gold', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'https://dlassets-ssl.xboxlive.com/public/content/ppl/colors/00003.json', 'TenureLevel': 16, 'isSponsoredUser': False},
#                       {'id': 2533274828754124, 'hostId': 2533274828754124, 'Gamertag': 'JohnnyCisco52', 'GameDisplayName': 'JohnnyCisco52', 'AppDisplayName': 'JohnnyCisco52', 'Gamerscore': 24845, 'GameDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=z951ykn43p4FqWbbFvR2Ec.8vbDhj8G2Xe7JngaTToBrrCmIEEXHC9UNrdJ6P7KIoIeJ1sl4QgwrJRGcdRHOCrpvgKrMrK2S9HqLsMNJwyrlNUPwUSf9HFJJ.NwkURuH&format=png', 'AppDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=z951ykn43p4FqWbbFvR2Ec.8vbDhj8G2Xe7JngaTToBrrCmIEEXHC9UNrdJ6P7KIoIeJ1sl4QgwrJRGcdRHOCrpvgKrMrK2S9HqLsMNJwyrlNUPwUSf9HFJJ.NwkURuH&format=png', 'AccountTier': 'Silver', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'http://dlassets.xboxlive.com/public/content/ppl/colors/00012.json', 'TenureLevel': 0, 'isSponsoredUser': False},
#                       {'id': 2533274816780998, 'hostId': 2533274816780998, 'Gamertag': 'MULEHORN117', 'GameDisplayName': 'MULEHORN117', 'AppDisplayName': 'MULEHORN117', 'Gamerscore': 38430, 'GameDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=wHwbXKif8cus8csoZ03RW_ES.ojiJijNBGRVUbTnZKsoCCCkjlsEJrrMqDkYqs3MHgKrR5FQmYZyWljGgrHUZ6OzqCnZVtWMB3B9BuWrk_aWuSHbEs5OFH6ZIxyREdbddl_8TsxG._EgqJjmJhf9tvoRz4E0W0aD5ibD9YtRE5E-&format=png', 'AppDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=wHwbXKif8cus8csoZ03RW_ES.ojiJijNBGRVUbTnZKsoCCCkjlsEJrrMqDkYqs3MHgKrR5FQmYZyWljGgrHUZ6OzqCnZVtWMB3B9BuWrk_aWuSHbEs5OFH6ZIxyREdbddl_8TsxG._EgqJjmJhf9tvoRz4E0W0aD5ibD9YtRE5E-&format=png', 'AccountTier': 'Gold', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'https://dlassets-ssl.xboxlive.com/public/content/ppl/colors/00003.json', 'TenureLevel': 12, 'isSponsoredUser': False},
#                       {'id': 2692107098689038, 'hostId': 2692107098689038, 'Gamertag': 'CHEEZM0', 'GameDisplayName': 'CHEEZM0', 'AppDisplayName': 'CHEEZM0', 'Gamerscore': 36394, 'GameDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=wHwbXKif8cus8csoZ03RWwcxuUQ9WVT6xh5XaeeZD02wEfGZeuD.XMoGFVYkwHDq5YNQcVCbsAJ0tfUv0rLYtB2TiMJ9zJDsu5YGxJRT7RuUBb5a1vbNs4jHDww3Zcl_ztAylW3aW2EUbJB7.3PY8vjxqzdu4IzgcR4TnWMvei0-&format=png', 'AppDisplayPicRaw': 'https://images-eds-ssl.xboxlive.com/image?url=wHwbXKif8cus8csoZ03RWwcxuUQ9WVT6xh5XaeeZD02wEfGZeuD.XMoGFVYkwHDq5YNQcVCbsAJ0tfUv0rLYtB2TiMJ9zJDsu5YGxJRT7RuUBb5a1vbNs4jHDww3Zcl_ztAylW3aW2EUbJB7.3PY8vjxqzdu4IzgcR4TnWMvei0-&format=png', 'AccountTier': 'Gold', 'XboxOneRep': 'GoodPlayer', 'PreferredColor': 'http://dlassets.xboxlive.com/public/content/ppl/colors/00007.json', 'TenureLevel': 16, 'isSponsoredUser': False}]


if __name__ == "__main__":
    main()
