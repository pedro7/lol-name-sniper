from checker import Checker
from connector import Client, Store
from datetime import datetime
from time import sleep

class _Sniper:
    def __init__(self):
        self._client = Client()
        self._store = Store()
        self._body = \
        {
            'summonerName': None,
            'accountId': self._get_account_id(),
            'items': [{'inventoryType': 'SUMMONER_CUSTOMIZATION', 'itemId': 1, 'ipCost': 13900, 'rpCost': None, 'quantity': 1}]
        }

    def _get_account_id(self):
        return self._client.call('GET', '/lol-login/v1/session').json()['accountId']

    def _change_name(self):
        return self._store.call('POST', '/summonerNameChange/purchase', self._body)

class Caitlyn(_Sniper):
    def __init__(self, key, name):
        super().__init__()
        self._key = key
        self._body['summonerName'] = name

    def snipe(self):
        checker = Checker(self._key, self._get_server())
        name_availability_datetime = checker.get_name_availability_datetime(self._body['summonerName'])
        print(f'Sleeping for {name_availability_datetime - datetime.now()}, until {name_availability_datetime}')
        sleep((name_availability_datetime - datetime.now()).total_seconds() - 0.4)
        for i in range(1, 6):
            print(f'Try {i} of 5', datetime.now())
            if self._change_name().status_code == 200:
                print('Success', datetime.now())
                return True
            sleep(0.1)
        return False

    def _get_server(self):
        return self._client.call('GET', '/riotclient/get_region_locale').json()['region']

class Aphelios(_Sniper):
    def __init__(self, names):
        super().__init__()
        self._names = names

    def snipe(self):
        while True:
            for name in self._names:
                if self._check_name_availability(name):
                    self._body['summonerName'] = name
                    return self._change_name()

    def _check_name_availability(self, name):
        return self._client.call('GET', f'/lol-summoner/v1/check-name-availability/{name}').json()