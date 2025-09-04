from direct.showbase.ShowBase import ShowBase
from mapmanager import Mapmanager
from hero import Hero

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.map = Mapmanager()
        self.map.loadLand("land.txt")
        self.hero = Hero((10, 17, 2), self.map)
        self.setBackgroundColor(0.757, 0.996, 1)

game = Game()
game.run()