import pyxel
from typing import List
from .collision import Collider
import math

class GameObject:
    world : 'World'
    name : str
    is_alive : bool # 消去したければここをFalseにする
    x : float
    y : float
    vx : float
    vy : float
    mass : float
    tags : list[str]
    colliders : list[Collider]
    STILL_SHREHOLD : float

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
        self.mass = 1
        self.tags = []
        self.colliders = []
        self.STILL_SHREHOLD = 1 / 3

    def add_collider(self, collider : Collider):
        self.colliders.append(collider)
        collider.parent = self

    def add_force(self, F_x : float, F_y : float):
        self.ax = F_x / self.mass
        self.ay = F_y / self.mass

    def update(self):
        pass
    
    def draw(self):
        pass
    
    def on_collision(self, other):
        pass

    #
    # 物理的な反射の計算
    #
    def resolve_collision(self, other):

        # 1. 法線ベクトル（正規化)
        dx = other.x - self.x
        dy = other.y - self.y
        dist = math.sqrt(dx**2 + dy**2)

        if dist == 0: return  # 重なりすぎている場合はスキップ

        nx = dx / dist  # 法線ベクトルx (正規化済み)
        ny = dy / dist  # 法線ベクトルy (正規化済み)

        # 2. 相対速度の計算
        v_rel_x = other.vx - self.vx
        v_rel_y = other.vy - self.vy

        # 3. 相対速度の法線方向の成分
        v_normal_mag = v_rel_x * nx + v_rel_y * ny

        # 4. すでに離れようとしているならスキップ
        if v_normal_mag > 0:
            return

        # 5. 力積のスカラー量
        e = 1.0 
        inv_mass_sum = (1 / self.mass) + (1 / other.mass)
        j = -(1 + e) * v_normal_mag / inv_mass_sum

        # 6. 速度の更新
        self.vx -= (j / self.mass) * nx
        self.vy -= (j / self.mass) * ny
        other.vx += (j / other.mass) * nx
        other.vy += (j / other.mass) * ny