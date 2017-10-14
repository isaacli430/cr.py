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
        return "http://api.cr-api.com/arena/{0}.png".format(self.number.replace(" ", "").lower())

class Profile:

    def __init__(self, **tag: str):
        self.tag = tag

    @property
    def data(self):
        with urllib.request.urlopen("http://api.cr-api.com/profile/{0}".format(self.tag)) as url:
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
    def win_streak(self):
        if self.data['games']['currentWinStreak'] < 0:
            return 0
        else:
            return self.data['games']['currentWinStreak']

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
    def arena_offer(self):
        return self.data['shopOffers']['arena']

    @property
    def deck(self)
        deck = []
        for card in self.data['currentDeck']:
            card_name = card.name.replace("_", "-")
            if card_name == "x-bow":
                deck.append((Card(key="bow"), card.level))
            else:
                deck.append((Card(key=card_name), card.level))
        return deck

class Clan:

    def __init__(self, **tag: str):
        self.tag = tag

    @property
    def data(self):
        with urllib.request.urlopen("http://api.cr-api.com/clan/{0}".format(self.tag)) as url:
            return json.loads(url.read().decode())

    @property
    def members(self):
        return [Profile(tag=x['tag']) for x in self.data['members']]

    @property
    def name(self):
        return self.data['name']

    @property
    def badge_url(self):
        return "api.cr-api.com/{0}".format(self.data['badge']['url'])

    @property
    def type(self):
        return self.data['typeName']

    @property
    def member_count(self):
        return self.data['memberCount']

    @property
    def trophies(self):
        return self.data['score']

    @property
    def required_trophies(self):
        return self.data['requiredScore']

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

    @property
    def clan_chest_trophies(self):
        return self.data['clanChest']['clanChestCrowns']

    @property
    def cc_finished_percent(self):
        return self.data['clanChest']['clanChestCrownsPercent']*100

class Card:

    def __init__(self, **key: str):
        self.key = key

    @property
    def data(self):
        with urllib.request.urlopen("https://raw.githubusercontent.com/smlbiobot/cr-api-data/master/dst/cards.json") as url:
            data = json.loads(url.read().decode())
        for test_card in data:
            if self.key == test_card['key']:
                return test_card
        return None

    @property
    def exists(self):
        if self.data == None:
            return False
        return True

    @property
    def name(self):
        if self.data == None:
            return None
        return self.data['name']

    @property
    def elixir(self):
        if self.data == None:
            return None
        return self.data['elixir']

    @property
    def type(self):
        if self.data == None:
            return None
        return self.data['type']

    @property
    def rarity(self):
        if self.data == None:
            return None
        return self.data['rarity']

    @property
    def arena_found(self):
        if self.data == None:
            return None
        return self.data['arena']

    @property
    def description(self):
        if self.data == None:
            return None
        return self.data['description']

    @property
    def card_id(self):
        if self.data == None:
            return None
        return self.data['decklink']

    @property
    def img_url(self):
        if self.data == None:
            return None
        return "https://raw.githubusercontent.com/cr-api/cr-api-assets/master/card/{0}.png".format(self.key)
