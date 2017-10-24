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

class Arena:

    def __init__(self, arena_id: int):
        self.arena_id = arena_id
        data = requests.get("http://api.cr-api.com/constants").json()
        found_arena = False
        for test_arena in data['arenas']:
            if self.arena_id == test_arena['arenaID']:
                self.data = test_arena
                found_arena = True
        if not found_arena:
            self.data = None

    @property
    def exists(self):
        if self.data == None:
            return False
        return True

    @property
    def number(self):
        if not self.exists:
            return None
        return self.data['arena']

    @property
    def name(self):
        if not self.exists:
            return None
        return self.data['name']

    @property
    def trophies_required(self):
        if not self.exists:
            return None
        return self.data['trophyLimit']

    @property
    def img_url(self):
        if not self.exists:
            return None
        return "http://api.cr-api.com/arena/{}.png".format(self.number.replace(" ", "").lower())

class Profile:

    def __init__(self, tag: str):
        self.tag = tag
        json = requests.get("http://api.cr-api.com/profile/{}".format(self.tag)).json()
        if "error" in json:
            self.data = None
        self.data = json

    @property
    def update(self):
        json = requests.get("http://api.cr-api.com/profile/{}".format(self.tag)).json()
        if "error" in json:
            self.data = None
        self.data = json

    @property
    def exists(self):
        if self.data == None:
            return False
        return True

    class Cycles:

        def __init__(self, data):
            self.data = data

        @property
        def chest_pos(self):
            return self.data['chestCycle']['chest_position']

        @property
        def smc_pos(self):
            return self.data['chestCycle']['superMagicalPos']

        @property
        def leg_pos(self):
            return self.data['chestCycle']['legendaryPos']

        @property
        def epic_pos(self):
            return self.data['chestCycle']['epicPos']

        @property
        def leg_shop(self):
            return self.data['shopOffers']['legendary']

        @property
        def epic_shop(self):
            return self.data['shopOffers']['epic']

        @property
        def arena_shop(self):
            return self.data['shopOffers']['arena']

    class XP:

        def __init__(self, data):
            self.data = data

        @property
        def current(self):
            return self.data['experience']['xp']

        @property
        def required(self):
            return self.data['experience']['xpRequiredForLevelUp']

        @property
        def remaining(self):
            return self.data['experience']['xpToLevelUp']

    class Trophies:

        def __init__(self, data):
            self.data = data

        @property
        def current(self):
            return self.data['trophies']

        @property
        def record(self):
            return self.data['stats']['maxTrophies']

        @property
        def legendary(self):
            return self.data['legendaryTrophies']

    class Cards:

        def __init__(self, data):
            self.data = data

        @property
        def found(self):
            return self.data['stats']['cardsFound']

        @property
        def tournament(self):
            return self.data['stats']['tournamentCardsWon']

        @property
        def favorite(self):
            return Card(key=self.data['stats']['favoriteCard'])

        @property
        def challenge(self):
            return self.data['stats']['challengeCardsWon']

    class Games:

        def __init__(self, data):
            self.data = data

        @property
        def total_games(self):
            return self.data['games']['total']

        @property
        def tournament_games(self):
            return self.data['games']['tournamentGames']

        @property
        def wins(self):
            return self.data['games']['wins']

        @property
        def losses(self):
            return self.data['games']['losses']

        @property
        def draws(self):
            return self.data['games']['draws']

        @property
        def three_crowns(self):
            return self.data['stats']['threeCrownWins']

        @property
        def win_streak(self):
            if self.data['games']['currentWinStreak'] < 0:
                return 0
            else:
                return self.data['games']['currentWinStreak']

    class Seasons:

        def __init__(self, data, number):
            self.data = data

        @property
        def number(self):
            return self.data['seasonNumber']

        @property
        def highest(self):
            return self.data['seasonHighest']

        @property
        def finish(self):
            return self.data['seasonHighest']

        @property
        def global_ranking(self):
            return self.data['seasonEndGlobalRank']

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
        return Arena(arena_id=self.data['arena']['arenaID'])

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
            deck.append((Card(card.key), card.level))
        return deck

class Clan:

    def __init__(self, tag: str):
        self.tag = tag
        data = requests.get("http://api.cr-api.com/clan/{}".format(self.tag)).json()
        if "error" in data:
            self.data = None
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
        self.data = data

    class ClanChest:

        def __init__(self, data):
            self.data = data

        @property
        def required(self):
            return self.data['clanChest']['clanChestCrownsRequired']

        @property
        def crowns(self):
            return self.data['clanChest']['clanChestCrowns']

        @property
        def finished_percent(self):
            return self.data['clanChest']['clanChestCrownsPercent']*100

        @property
        def contributions(self):
            return [(i['name'], i['clanChestCrowns']) for i in self.data['members']]

    class Trophies:

        def __init__(self, data):
            self.data = data

        @property
        def current(self):
            return self.data['score']

        @property
        def requirement(self):
            return self.data['requiredScore']

        @property
        def players(self):
            return [(i['name'], i['trophies']) for i in self.data['members']]

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
        return [Profile(x['tag']) for x in self.data['members']]

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
        return self.data['donations']

    @property
    def rank(self):
        if self.data['currentRank'] == 0:
            return None
        return self.data['currentRank']

    @property
    def description(self):
        return self.data['description']

    @property
    def region(self):
        return self.data['region']['name']



class Card:

    def __init__(self, key):
        self.key = key
        data = requests.get("https://api.cr-api.com/constants").json()
        card_found = False
        for test_card in data['cards']:
            if self.key == test_card['key']:
                self.data = test_card
                card_found = True
        if not card_found:
            self.data = None

    @property
    def exists(self):
        if self.data == None:
            return False
        return True

    @property
    def name(self):
        if not self.exists:
            return None
        return self.data['name']

    @property
    def elixir(self):
        if not self.exists:
            return None
        return self.data['elixir']

    @property
    def type(self):
        if not self.exists:
            return None
        return self.data['type']

    @property
    def rarity(self):
        if not self.exists:
            return None
        return self.data['rarity']

    @property
    def arena_found(self):
        if not self.exists:
            return None
        return self.data['arena']

    @property
    def description(self):
        if not self.exists:
            return None
        return self.data['description']

    @property
    def card_id(self):
        if not self.exists:
            return None
        return self.data['decklink']

    @property
    def img_url(self):
        if not self.exists:
            return None
        return "https://raw.githubusercontent.com/cr-api/cr-api-assets/master/card/{}.png".format(self.key)

class Profiles:

    def __init__(self, *tags: str):
        self.profiles = [Profile(tag) for tag in tags]

class Clans:

    def __init__(self, *tags: str):
        self.clans = [Clan(tag) for tag in tags]