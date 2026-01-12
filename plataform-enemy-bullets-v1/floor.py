class Floor:
    def __init__(self, level):
        self.level = level
        self.enemies = []
        self.platforms = []

    def update(self):
        for enemy in self.enemies:
            enemy.update()

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
