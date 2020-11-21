class Pokemon:
    def __init__(self, name, hp, atk, df, spa, spd, spe, ability, moves):
        self.name = name
        self.ability = ability
        self.stats = [hp, atk, df, spa, spd, spe]
        self.moves = moves
        self.status = 'healthy'

    def __init__(self, name):
        self.name = name
        self.ability = ""
        self.stats = [250, 250, 250, 250, 250, 250]
        self.moves = []
        self.status = 'healthy'
