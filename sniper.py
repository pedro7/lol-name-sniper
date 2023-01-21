from checker import Checker
from connector import Client, Store
from datetime import datetime
from time import sleep


class _Sniper:
    def __init__(self):
        self._client = Client()
        self._store = Store()
        self._body = {
            'summonerName': None,
            'accountId': self._client.call('GET', '/lol-login/v1/session').json()['accountId'],
            'items': [
                {
                        'inventoryType': 'SUMMONER_CUSTOMIZATION',
                        'itemId': 1,
                        'ipCost': 13900,
                        'rpCost': None,
                        'quantity': 1
                }
            ]
        }

    def _change_name(self):
        return self._store.call('POST', '/summonerNameChange/purchase', self._body)


class Caitlyn(_Sniper):
    def __init__(self, key=None):
        super().__init__()
        self._key = key

    def snipe_name(self, name):
        self._body['summonerName'] = name
        checker = Checker(self._get_server(), self._key)
        name_availability = checker.get_name_availability(name)
        sleep((name_availability - datetime.now()).total_seconds() - 0.4)
        for i in range(5):
            if self._change_name().status_code == 200:
                return True
            sleep(0.1)
        return False

    def _get_server(self):
        return self._client.call('GET', '/riotclient/get_region_locale').json()['region']


class Aphelios(_Sniper):
    def __init__(self):
        super().__init__()

    def snipe_name(self, names):
        while True:
            for name in names:
                if self._check_name_availability(name):
                    self._body['summonerName'] = name
                    return self._change_name()

    def _check_name_availability(self, name):
        return self._client.call('GET', f'/lol-summoner/v1/check-name-availability/{name}').json()
