import pyxphys 
import pyxel

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

# 初期設定
app = pyxphys.App(200,200) # アプリ本体
world = pyxphys.World(gravity = 0.9) # 世界のルールを決める
app.regist_world("game", world) # 作った世界を倉庫に名前をつけて登録
app.push_world("game") # 倉庫からアプリ画面に世界を表示する

world.add_object(Ball()) # "world"という世界にBallオブジェクトを追加

app.run() # アプリを実行