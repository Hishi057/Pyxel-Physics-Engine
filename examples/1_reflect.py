import pyxphys 
import pyxel

class BallManager(pyxphys.GameObject):
    def __init__(self):
        super().__init__()
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.world.add_object(Ball())

class Ball(pyxphys.GameObject):
    color : int = 6 # ボールの色
    radius : int = 10 # ボールの半径

    def __init__(self):
        super().__init__()
        self.name = "ball"
        self.x = pyxel.rndi(0, 199)
        self.y = 100
        angle = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle) * 3 + 3
        self.vy = pyxel.rndi(0, 10) * -1
        self.add_collider(pyxphys.CircleCollider(self.radius))
    
    def update(self):
        if self.x < self.radius:
            self.x = self.radius
            self.vx *= -1
        if app.screen_x - self.radius < self.x:
            self.x = app.screen_x - self.radius
            self.vx *= -1

        limit_y = self.world.app.screen_y - self.radius # 床の位置
        if limit_y < self.y:
            overlap = self.y - limit_y #
            self.y = limit_y - overlap # 床にめり込んだ分だけ戻す
            self.vy *= -0.7

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)

# 初期設定
app = pyxphys.App(300,300)
world = pyxphys.World(gravity = 0.9)
app.add_world(world)

world.add_object(BallManager())
world.add_object(Ball())


app.run() # アプリを実行