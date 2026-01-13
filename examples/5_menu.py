import pyxphys 
import pyxel

# アプリ本体
app = pyxphys.App(200,200)
app.load_resource("assets/5_resource.pyxres")

#
# タイトル画面
#
class TitleManager(pyxphys.GameObject):
    game : pyxphys.World
    def __init__(self, game : pyxphys.World):
        super().__init__(x=100, y=20)
        self.name = "background"
        self.game = game
    
    def update(self):
        if pyxel.btn(pyxel.KEY_SPACE):
            app.worlds = []
            app.add_world(game)

class Background(pyxphys.GameObject):
    tile_size : int = 16
    def __init__(self):
        super().__init__(x=100, y=20)
        self.name = "background"

    def draw(self):
        for x in range(0,16):
            for y in range(0,16):
                pyxel.blt(x * self.tile_size,y * self.tile_size,0,
                  0,0,self.tile_size,self.tile_size,0)

class TitleLogo(pyxphys.GameObject):
    def __init__(self):
        super().__init__(x=100, y=20)
        self.name = "title logo"

    def draw(self):
        pyxel.blt(80,50, 0,
                  0,16,47,32, 0,
                  rotate=0, scale=2.0)

class Text_PressEnter(pyxphys.GameObject):
    def __init__(self):
        super().__init__(x=100, y=20)
        self.name = "text press enter"

    def draw(self):
        pyxel.text(75, 150, "PRESS ENTER", pyxel.COLOR_WHITE)

#
# ゲーム部分
#

class Ball(pyxphys.GameObject):
    color : int = 6 # ボールの色
    radius : int = 10 # ボールの半径

    def __init__(self):
        super().__init__(x=100, y=20)
        self.name = "ball"
        self.vx = 0
        self.vy = -4
        self.add_collider(pyxphys.CircleCollider(self.radius))
    
    def update(self):
        if self.y > 190:
            self.vy *= -0.9
            self.y = 190

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)


#
# 最終的な処理
#

# game
game = pyxphys.World(gravity = 1.1)
game.add_object(Ball())

# title
title = pyxphys.World()
title.add_object(TitleManager(game))
title.add_object(Background())
title.add_object(TitleLogo())
title.add_object(Text_PressEnter())

app.add_world(title)
app.run()