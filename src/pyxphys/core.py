import pyxel #pyxel というライブラリをインポート
import math
from typing import List

class App:
    screen_x : int
    screen_y : int
    worlds : list[World]

    def __init__(self,screen_x,screen_y):
        self.screen_x = screen_x
        self.screen_y = screen_y
        pyxel.init(screen_x, screen_y)
        self.worlds = []
    
    def add_world(self, world : World):
        self.worlds.append(world)
    
    def run(self):
        pyxel.run(self.update, self.draw)
    
    def update(self):
        for w in self.worlds: 
            w.update_physics()
            
    def draw(self):
        pyxel.cls(7)
        for w in self.worlds:
            for o in w.objects:
                o.draw()

class World:
    objects : list[GameObject]
    gravity : float
    def __init__(self, gravity : float = 0):
        self.objects = []
        self.gravity = gravity

    def update_physics(self):
        # オブジェクトを削除する処理
        new_objects = []
        for o in self.objects:
            if o.is_alive:
                new_objects.append(o)
        self.objects = new_objects

        # 物理演算
        for o in self.objects:
            o.vx += o.ax
            o.vy += o.ay + self.gravity
            o.x += o.vx
            o.y += o.vy
            o.update()
        
        # 衝突の処理 
        for o1 in self.objects:
            for o2 in self.objects:
                o1.collide(o2)

    def add_object(self, object : GameObject):
        self.objects.append(object)

class GameObject:
    name : str
    is_alive : bool # 消去したければここをFalseにする
    x : float
    y : float
    vx : float
    vy : float
    tags : list[str]

    def __init__(self, 
                 name : str = "",
                 x : float = 0,
                 y : float = 0,
                 vx : float = 0,
                 vy : float = 0,
                 ax : float = 0,
                 ay : float = 0,
                 ):

        # 変数の設定
        self.is_alive = True
        self.name = name
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.tags = []
        return self

    def update(self):
        pass
    
    def draw(self):
        pass
    
    def collide(self, target):
        pass