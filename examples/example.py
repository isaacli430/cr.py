import cr_py

profile = cr_py.Profile("GYUGPLYL")
clan = cr_py.Clan("829L22L9")
arena = cr_py.Arena(4)
card = cr_py.Card("flying-machine")
print(profile.trophies.current)
print(clan.members)
print(arena.name)
print(card.img_url)
clan.update()
print(cr_py.members)