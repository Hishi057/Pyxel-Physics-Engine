import pyxel
from typing import List
from .engine import GameObject
from .collision import check_collision
import math

class World:
    app : 'App'
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
        sub_step = 10
        dt = 1 / sub_step
        for o in self.objects:
            for i in range(sub_step):
                o.vx += o.ax * dt
                o.vy += (o.ay + self.gravity) * dt
                if math.fabs(o.vx / dt) < o.STILL_SHREHOLD:
                    o.vx = 0
                if math.fabs(o.vy / dt) < o.STILL_SHREHOLD:
                    o.vy = 0
                o.x += o.vx * dt
                o.y += o.vy *dt
            o.update()
        
        #
        # 衝突判定 
        #
        all_colliders = []
        for o in self.objects:
            all_colliders.extend(o.colliders)
        
        for c1 in all_colliders:
            for c2 in all_colliders:
                if c1.parent != c2.parent and check_collision(c1, c2):
                    # 物理的な挙動の計算
                    if (not c1.is_trigger) and (not c2.is_trigger):
                        c1.parent.resolve_collision(c2.parent)
                    # ユーザー設定の衝突時の処理
                    c1.parent.on_collision(c2.parent)


    def draw(self):
        pyxel.cls(7)
        for o in self.objects:
            o.draw()

    def add_object(self, object : GameObject):
        self.objects.append(object)
        object.world = self
