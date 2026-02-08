import math

def calc_distance(index_tip, thumb_tip):
    return math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)

def calc_distance_regular (index_tip, thumb_tip):
    return math.hypot(index_tip, thumb_tip)
