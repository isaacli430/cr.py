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
        return "http://api.cr-api.com/arena/{}.png".format(self.number.replace(" ", "").lower())

class Profile:

    def __init__(self, **tag: str):
        self.tag = tag

    @property
    def data(self):
        with urllib.request.urlopen("http://api.cr-api.com/profile/{}".format(self.tag)) as url:
            return json.loads(url.read().decode())

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
        return self.data['legendaryTrophies']

    @property
    def name_changed(self):
        return self.data['nameChanged']

    @property
    def global_rank(self):
        return self.data['globalRank']

    @property
    def clan(self):
        return Clan(tag=self.data['clan']['tag']) or None

    @property
    def clan_chest_contrib(self):
        try:
            return [x['clanChestCrowns'] for x in self.clan.members if x.name==self.name][0]
        except:
            return None

    @property
    def level(self):
        return self.data['experience']['level']

    @property
    def current_xp(self):
        return self.data['experience']['xp']

    @property
    def xp_required(self):
        return self.data['experience']['xpRequiredForLevelUp']

    @property
    def xp_remaining(self):
        return self.data['experience']['xpToLevelUp']

    @property
    def account_age(self):
        return self.data['stats']['accountAgeInDays']

    @property
    def tourney_cards_won(self):
        return self.data['stats']['tournamentCardsWon']

    @property
    def pb(self):
        return self.data['stats']['maxTrophies']

    @property
    def three_crowns(self):
        return self.data['stats']['threeCrownWins']

    @property
    def cards_found(self):
        return self.data['stats']['cardsFound']

    @property
    def fav_card(self):
        return self.data['stats']['favoriteCard']

    @property
    def total_donations(self):
        return self.data['stats']['totalDonations']

    @property
    def challenge_wins(self):
        return self.data['stats']['challengeMaxWins']

    @property
    def challenge_cards(self):
        return self.data['stats']['challengeCardsWon']

    @property
    def total_games(self):
        return self.data['games']['total']

    @property
    def tournament_games(self):
        return self.data['games']['tournamentGames']

class Clan:

    def __init__(self, **tag: str):
        self.tag = tag

    @property
    def data(self):
        with urllib.request.urlopen("http://api.cr-api.com/clan/{}".format(self.tag)) as url:
            return json.loads(url.read().decode())

    @property
    def members(self):
        return [Profile(tag=x['tag']) for x in self.data['members']]

