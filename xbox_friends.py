import requests
import serial
import time

x_auth = '6670f76a5481bf8de6dce36b92020b9e8c3da340'  # api authentication key
headers = {'X-AUTH': x_auth}
api_prefix = 'https://xapi.us/v2'

def test_arduino():
    ser = serial.Serial('/dev/cu.usbmodem14401', 9600)  # open arduino port
    print(ser.name)
    time.sleep(3)  # arduino resets when init connection via python

    msg1 = 'abcdefgh'
    msg2 = '0123456789123456'
    msg3 = 'lmnop'
    lst = [msg1, msg2, msg3]

    TERM = '\r\n'

    for msg in lst:
        ser.write(msg.encode())  # variable to bytes rather than b'some message'
        chars_sent = len(msg)

        exp_response_bytes = len(str(chars_sent)) + len(TERM)
        response_b = ser.read(exp_response_bytes)  # arduino println terms with '\r\n'
        print(response_b)
        print(int(response_b) == int(chars_sent))  # int cast drops TERM

    ser.close()


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


def append_presence_json(friends_json):
    for d in friends_json:
        xuid = d['id']
        gamertag = d['Gamertag']
        presence_json = get_presence_json(xuid)
        d['status'] = presence_json['state']
    return friends_json

if __name__ == "__main__":
    # main()
    test_arduino()