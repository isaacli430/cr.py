import cr_py

profile = cr_py.Profile("GYUGPLYL")
constants = cr_py.Constants()
print(profile.trophies.current)
print(constants.card['knight'].name)
print(profile.deck[0][0].name)