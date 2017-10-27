"""
Copyright (c) 2017 kwugfighter

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json, requests

class Profile:

    def __init__(self, tag: str):
        self.tag = tag
        json = requests.get("http://api.cr-api.com/profile/{}".format(self.tag)).json()
        if "error" in json:
            self.data = None
        else:
            self.data = json

    @property
    def update(self):
        json = requests.get("http://api.cr-api.com/profile/{}".format(self.tag)).json()
        if "error" in json:
            self.data = None
        else:
            self.data = json

    @property
    def exists(self):
        if self.data == None:
            return False
        return True

    class Cycles:

        def __init__(self, data):
            self.chest_pos = data['chestCycle']['chest_position']
            self.smc_pos = data['chestCycle']['superMagicalPos']
            self.leg_pos = data['chestCycle']['legendaryPos']
            self.epic_pos = data['chestCycle']['epicPos']
            self.leg_shop = data['shopOffers']['legendary']
            self.epic_shop = data['shopOffers']['epic']
            self.arena_shop = data['shopOffers']['arena']

    class XP:

        def __init__(self, data):
            self.current = data['experience']['xp']
            self.required = data['experience']['xpRequiredForLevelUp']
            self.remaining = data['experience']['xpToLevelUp']

    class Trophies:

        def __init__(self, data):
            self.current = data['trophies']
            self.record = data['stats']['maxTrophies']
            self.legendary = data['legendaryTrophies']

    class Cards:

        def __init__(self, data):
            self.found = data['stats']['cardsFound']
            self.tournament = data['stats']['tournamentCardsWon']
            self.favorite = Constants().card[self.data['stats']['favoriteCard']]
            self.challenge = data['stats']['challengeCardsWon']

    class Games:

        def __init__(self, data):
            self.total = data['games']['total']
            self.tournament = data['games']['tournamentGames']
            self.wins = data['games']['wins']
            self.losses = data['games']['losses']
            self.draws = data['games']['draws']
            self.three_crowns = data['stats']['threeCrownWins']
            if data['games']['currentWinStreak'] < 0:
                self.win_streak = 0
            else:
                self.win_streak = data['games']['currentWinStreak']

    class Seasons:

        def __init__(self, data):
            self.number = data['seasonNumber']
            self.highest = data['seasonHighest']
            self.finish = data['seasonEnding']
            self.global_ranking = data['seasonEndGlobalRank']

    @property
    def cycles(self):
        if not self.exists:
            return None
        return self.Cycles(self.data)

    @property
    def xp(self):
        if not self.exists:
            return None
        return self.XP(self.data)

    @property
    def trophies(self):
        if not self.exists:
            return None
        return self.Trophies(self.data)

    @property
    def cards(self):
        if not self.exists:
            return None
        return self.Cards(self.data)

    @property
    def games(self):
        if not self.exists:
            return None
        return self.Games(self.data)

    @property
    def seasons(self):
        if not self.exists:
            return None
        return [self.Season(season) for season in self.data['previousSeasons']]

    @property
    def name(self):
        if not self.exists:
            return None
        return self.data['name']

    @property
    def arena(self):
        if not self.exists:
            return None
        return Constants().arena[self.data['arena']['arenaID']]

    @property
    def name_changed(self):
        if not self.exists:
            return None
        return self.data['nameChanged']

    @property
    def global_rank(self):
        if not self.exists:
            return None
        return self.data['globalRank']

    @property
    def clan(self):
        if not self.exists:
            return None
        return Clan(self.data['clan']['tag']) or None

    @property
    def clan_chest_contrib(self):
        if not self.exists:
            return None
        try:
            return [x['clanChestCrowns'] for x in self.clan.members if x.name==self.name][0]
        except:
            return None

    @property
    def level(self):
        if not self.exists:
            return None
        return self.data['experience']['level']

    @property
    def account_age(self):
        if not self.exists:
            return None
        return self.data['stats']['accountAgeInDays']

    @property
    def total_donations(self):
        if not self.exists:
            return None
        return self.data['stats']['totalDonations']

    @property
    def challenge_record(self):
        if not self.exists:
            return None
        return self.data['stats']['challengeMaxWins']

    @property
    def deck(self):
        if not self.exists:
            return None
        deck = []
        for card in self.data['currentDeck']:
            deck.append((Constants().card[card['key']], card['level']))
        return deck

class Clan:

    def __init__(self, tag: str):
        self.tag = tag
        data = requests.get("http://api.cr-api.com/clan/{}".format(self.tag)).json()
        if "error" in data:
            self.data = None
        else:
            self.data = data

    @property
    def exists(self):
        if self.data == None:
            return False
        return True

    def update(self):
        data = requests.get("http://api.cr-api.com/clan/{}".format(self.tag)).json()
        if "error" in data:
            self.data = None
        else:
            self.data = data

    class ClanChest:

        def __init__(self, data):
            self.data = data
            self.required = data['clanChest']['clanChestCrownsRequired']
            self.crowns = data['clanChest']['clanChestCrowns']
            self.finished_percent = data['clanChest']['clanChestCrownsPercent']*100
            self.contributions = [(i['name'], i['clanChestCrowns']) for i in self.data['members']]

    class Trophies:

        def __init__(self, data):
            self.data = data
            self.current = data['score']
            self.requirement = data['requiredScore']
            self.players = [(i['name'], i['trophies']) for i in self.data['members']]

    @property
    def clanchest(self):
        if not self.exists:
            return None
        return self.ClanChest(self.data)

    @property
    def trophies(self):
        if not self.exists:
            return None
        return self.Trophies(self.data)

    @property
    def members(self):
        if not self.exists:
            return None
        return [(x['name'], x['tag']) for x in self.data['members']]

    @property
    def name(self):
        if not self.exists:
            return None
        return self.data['name']

    @property
    def badge_url(self):
        if not self.exists:
            return None
        return "api.cr-api.com/{0}".format(self.data['badge']['url'])

    @property
    def type(self):
        if not self.exists:
            return None
        return self.data['typeName']

    @property
    def member_count(self):
        if not self.exists:
            return None
        return self.data['memberCount']

    @property
    def donations(self):
        if not self.exists:
            return None
        return self.data['donations']

    @property
    def rank(self):
        if self.data['currentRank'] == 0 or not self.exists:
            return None
        return self.data['currentRank']

    @property
    def description(self):
        if not self.exists:
            return None
        return self.data['description']

    @property
    def region(self):
        if not self.exists:
            return None
        return self.data['region']['name']



class Profiles:

    def __init__(self, *tags: str):
        self.profiles = [Profile(tag) for tag in tags]

class Clans:

    def __init__(self, *tags: str):
        self.clans = [Clan(tag) for tag in tags]

class Constants:

    def __init__(self):
        self.data = requests.get("http://api.cr-api.com/constants").json()
        self.badges = self.data['badges']
        self.chest_cycle = self.data['chestCycle']
        countries = []
        for country in self.data['countryCodes']:
            if country['isCountry'] == "false":
                countries.append({"is_country": False, "name": country['name']})
        self.countries = countries

    class Arena:

        def __init__(self, data):
            self.arena = data['arena']
            self.name = data['name']
            self.trophies_required = data['trophyLimit']
            self.id = data['arenaID']
            self.img_url = "http://api.cr-api.com/arena/{}.png".format(self.arena.replace(" ", "").lower())

    class Card:

        def __init__(self, data):
            self.key = data['key']
            self.name = data['name']
            self.elixir = data['elixir']
            self.type = data['type']
            self.rarity = data['rarity']
            self.arena_found = data['arena']
            self.description = data['description']
            self.card_id = data['card_id']
            self.decklink = data['decklink']
            self.img_url = "https://raw.githubusercontent.com/cr-api/cr-api-assets/master/card/{}.png".format(self.key)

    class Alliance:

        def __init__(self, data):
            self.roles = data['roles']
            self.types = data['types']

    class Rarity:

        def __init__(self, data):
            self.name = data['name']
            self.donate_capacity = data['donate_capacity']
            self.donate_reward = data['donate_reward']
            self.donate_xp = data['donate_xp']
            self.gold_equivelant = data['gold_conversion_value']
            self.level_count = data['level_count']
            self.upgrade_cost = data['upgrade_cost']
            self.upgrade_xp = data['upgrade_exp']
            self.upgrade_cards = data['upgrade_material_count']

    @property
    def arena(self):
        return [self.Arena(arena) for arena in self.data['arenas']]

    @property
    def card(self):
        cards = {}
        for card in self.data['cards']:
            cards[card['key']] = self.Card(card)
        return cards

    @property
    def alliance(self):
        return self.Alliance(self.data['alliance'])

    @property
    def rarity(self):
        rarities = {}
        for rarity in self.data['rarities']:
            rarities[rarity['name']] = self.Raritiy(rarity)
        return rarities
