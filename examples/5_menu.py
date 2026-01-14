import pyxphys 
import pyxel

#
# タイトル画面
#
class TitleManager(pyxphys.GameObject):
    game : pyxphys.World
    def __init__(self):
        super().__init__(x=100, y=20)
        self.name = "background"
    
    def update(self):
        if pyxel.btn(pyxel.KEY_SPACE):
            app.clear_world()
            app.push_world("game")

class Background(pyxphys.GameObject):
    tile_size : int = 16
    time : int
    def __init__(self):
        super().__init__(x=100, y=20, z=0)
        self.name = "background"
        self.time = 0

    def update(self):
        self.time += 1

    def draw(self):
        for x in range(0,16):
            for y in range(0,16):
                if self.time % 30 <= 15:
                    pyxel.blt(x * self.tile_size,y * self.tile_size,0,
                                0,0,self.tile_size,self.tile_size,0)
                else:
                    pyxel.blt(x * self.tile_size,y * self.tile_size,0,
                                16,0,self.tile_size,self.tile_size,0)

class TitleLogo(pyxphys.GameObject):
    def __init__(self):
        super().__init__(x=100, y=20, z=1)
        self.name = "title logo"

    def draw(self):
        pyxel.blt(80,50, 0,
                  0,16,47,32, 0,
                  rotate=0, scale=2.0)

class Text(pyxphys.GameObject):
    time : int
    def __init__(self):
        super().__init__(x=75, y=150, z=1)
        self.name = "text"
        self.time = 0
    
    def update(self):
        self.time += 1

    def draw(self):
        if self.time % 30 <= 15:
            shadow_text(self.x, self.y, "PRESS ENTER")
            shadow_text(self.x, self.y + 12, "YAMASHITA YUI")
            shadow_line(self.x, self.y + 8, self.x + 50, self.y + 8)
        else:
            shadow_text(self.x, self.y +1, "PRESS ENTER")
            shadow_text(self.x, self.y + 13, "YAMASHITA YUI")
            shadow_line(self.x, self.y + 9, self.x + 50, self.y + 9)

def shadow_line(x1, y1, x2, y2):
    pyxel.line(x1, y1 + 1, x2, y2 +1, pyxel.COLOR_BLACK)
    pyxel.line(x1, y1, x2, y2, pyxel.COLOR_WHITE)

def shadow_text(x, y, str):
    o = [-1, 0, 1]
    for ox in o:
        for oy in o:
            pyxel.text(x+ox, y+oy, str, pyxel.COLOR_BLACK)
    pyxel.text(x, y, str, pyxel.COLOR_WHITE)

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

# アプリ本体
app = pyxphys.App(200,200)
app.load_resource("assets/5_resource.pyxres")

# title
title = pyxphys.World()
title.add_object(TitleManager())
title.add_object(Background())
title.add_object(TitleLogo())
title.add_object(Text())
app.regist_world(title, name = "title")

# game
game = pyxphys.World(gravity = 1.1)
game.add_object(Ball())
app.regist_world(game, name = "game")

app.run()