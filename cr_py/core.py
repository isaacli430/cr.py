import json, urllib.request

class Arena:

    def __init__(self, **arena_id: int):
        self.arena_id = arena_id

    @property
    def data(self):
        with urllib.request.urlopen("http://api.cr-api.com/constants") as url:
            data = json.loads(url.read().decode())
            return data['arenas'][self.arena_id-1]

    @property
    def number(self):
        return self.data['arena']

    @property
    def name(self):
        return self.data['name']

    @property
    def trophies_required(self):
        return self.data['trophyLimit']

    @property
    def img_url(self):
        return "http://api.cr-api.com/arena/{}".format(self.number.replace(" ", "").lower())

class Profile:

    def __init__(self, **tag: str):
        self.tag = tag

    @property
    def data(self):
        with urllib.request.urlopen("http://api.cr-api.com/profile/{}".format(self.tag)) as url:
            data = json.loads(url.read().decode())
        return data

    @property
    def name(self):
        return self.data['name']

    @property
    def trophies(self):
        return self.data['trophies']

    @property
    def arena(self):
        return Arena(arena_id=self.data['arena']['arenaID'])

    @property
    def legend_trophies(self):
        pass

    @property
    def name_changed(self):
        pass

    @property
    def global_rank(self):
        pass

class Clan:

    def __init__(self, **tag: str):
        self.tag = tag

