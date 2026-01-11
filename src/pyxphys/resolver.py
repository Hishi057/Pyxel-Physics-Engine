import math
from .utils import clamp
import math
from .utils import clamp
from .constants import CombineMode

# ---------------------------------------------------------
# 反発係数関連
# ---------------------------------------------------------

# 2つのColliderから最終的な反発係数を取得
def get_restitution(c1 , c2):
    r1 = c1.restitution
    r2 = c2.restitution

    if c1.restitution_priority > c2.restitution_priority:
        c = c1
    if c1.restitution_priority < c2.restitution_priority:
        c = c2
    
    if c1.restitution_priority != c2.restitution_priority:
        if c.restitution_combine_mode == CombineMode.MAX:
            return max_restitution(r1, r2)
        if c.restitution_combine_mode == CombineMode.MIN:
            return min_restitution(r1, r2)
        if c.restitution_combine_mode == CombineMode.AVERAGE:
            return average_restitution(r1, r2)
        if c.restitution_combine_mode == CombineMode.MULTIPLY:
            return multiply_restitution(r1, r2)
    else:
        mode_1 = c1.restitution_combine_mode
        mode_2 = c2.restitution_combine_mode
        if mode_1 == CombineMode.MAX or mode_2 == CombineMode.MAX:
            return max_restitution(r1, r2)
        if mode_1 == CombineMode.MULTIPLY or mode_2 == CombineMode.MULTIPLY:
            return multiply_restitution(r1, r2)
        if mode_1 == CombineMode.MIN or mode_2 == CombineMode.MIN:
            return min_restitution(r1, r2)
        if mode_1 == CombineMode.AVERAGE or mode_2 == CombineMode.AVERAGE:
            return average_restitution(r1, r2)
    return 0.2

def max_restitution(restitution1, restitution2):
    return max(restitution1, restitution2)

def min_restitution(restitution1, restitution2):
    return min(restitution1, restitution2)

def average_restitution(restitution1, restitution2):
    return (restitution1 + restitution2)/2

def multiply_restitution(restitution1, restitution2):
    return restitution1 * restitution2



# ---------------------------------------------------------
# 共通処理: 物理的な処理
# ---------------------------------------------------------
def apply_collision_response(body_a, body_b, nx, ny, depth, e):
    """
    衝突した2つの物体に対して、位置修正と速度更新を行う
    body_a: 法線ベクトルの始点側の物体 (位置・速度がマイナス方向に補正される)
    body_b: 法線ベクトルの終点側の物体 (位置・速度がプラス方向に補正される)
    nx, ny: 正規化された法線ベクトル (body_a -> body_b の向き)
    depth:  めり込み量 (正の値)
    """
    if depth <= 0:
        return

    # 1. 位置修正
    percent = 0.4 # 補正強度
    correction_x = nx * depth * percent
    correction_y = ny * depth * percent

    if not body_a.IS_FREEZE_POSITION:
        body_a.x -= correction_x
        body_a.y -= correction_y
    if not body_b.IS_FREEZE_POSITION:
        body_b.x += correction_x
        body_b.y += correction_y

    # 2. 速度の更新
    
    # 相対速度
    v_rel_x = body_b.vx - body_a.vx
    v_rel_y = body_b.vy - body_a.vy

    # 相対速度の法線方向成分
    v_normal_mag = v_rel_x * nx + v_rel_y * ny

    # すでに離れようとしているならスキップ
    if v_normal_mag > 0:
        return

    # 逆質量の計算
    inv_m1 = 1.0 / body_a.mass if body_a.mass != float('inf') else 0.0
    inv_m2 = 1.0 / body_b.mass if body_b.mass != float('inf') else 0.0
    inv_mass_sum = inv_m1 + inv_m2

    if inv_mass_sum == 0:
        return

    # 撃力 のスカラー量
    j = -(1 + e) * v_normal_mag / inv_mass_sum

    # 速度ベクトルに撃力を適用
    impulse_x = j * nx
    impulse_y = j * ny

    body_a.vx -= impulse_x * inv_m1
    body_a.vy -= impulse_y * inv_m1
    body_b.vx += impulse_x * inv_m2
    body_b.vy += impulse_y * inv_m2


# ---------------------------------------------------------
# 形状ごとの衝突判定
# ---------------------------------------------------------

# circle, circle
def resolve_circle_circle(circle1, circle2):
    dx = circle2.center_x - circle1.center_x
    dy = circle2.center_y - circle1.center_y
    dist = math.sqrt(dx**2 + dy**2)
    
    nx : float
    ny : float
    depth : float

    if dist == 0:
        nx, ny = 0, -1
        depth = circle1.radius + circle2.radius
    else:
        nx = dx / dist
        ny = dy / dist
        depth = (circle1.radius + circle2.radius) - dist

    e = get_restitution(circle1, circle2)
    apply_collision_response(circle1.parent, circle2.parent, nx, ny, depth, e)


# circle, box
def resolve_box_circle(box, circle):
    # box上の「円の中心に最も近い点」を特定
    closest_x = clamp(circle.center_x, box.center_x - box.width/2, box.center_x + box.width/2)
    closest_y = clamp(circle.center_y, box.center_y - box.height/2, box.center_y + box.height/2)

    # 法線と距離の計算
    dx = closest_x - circle.center_x
    dy = closest_y - circle.center_y
    dist = math.sqrt(dx**2 + dy**2)

    nx : float
    ny : float
    depth : float

    if dist == 0:
        nx, ny = 0, -1
        depth = circle.radius
    else:
        nx = dx / dist
        ny = dy / dist
        depth = circle.radius - dist

    e = get_restitution(box, circle)
    apply_collision_response(circle.parent, box.parent, nx, ny, depth, e)

# box, box
def resolve_box_box(box1, box2):
    dx = box2.center_x - box1.center_x
    dy = box2.center_y - box1.center_y
    overlap_x = (box1.width + box2.width) / 2 - abs(dx)
    overlap_y = (box1.height + box2.height) / 2 - abs(dy)
    
    # 重なりが小さい方の軸を衝突軸とする
    if overlap_x < overlap_y:
        # X軸方向の衝突
        nx = 1.0 if dx > 0 else -1.0
        ny = 0.0
        depth = overlap_x
    else:
        # Y軸方向の衝突
        nx = 0.0
        ny = 1.0 if dy > 0 else -1.0
        depth = overlap_y
    
    e = get_restitution(box1, box2)
    apply_collision_response(box1.parent, box2.parent, nx, ny, depth, e)