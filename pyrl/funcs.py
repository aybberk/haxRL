import scipy
import matplotlib.pyplot as plt
from Border import Border
from VerticalBorder import VerticalBorder
from HorizontalBorder import HorizontalBorder
from Disc import Disc
from Collision import Collision
from DHBCollision import DHBCollision
from DVBCollision import DVBCollision
from KickCollision import KickCollision
from DDCollision import DDCollision
from Way import Way
from Vector import Vector
from Kicker import Kicker
from Ball import Ball


def preprocess_state(state):
    assert len(state.shape) == 3
    cropped = state.mean(axis=2, keepdims=True)[40:-20]
    normalized = cropped / 255
    return scipy.misc.imresize(normalized[:,:,0], [84, 84])


def show(image):
    plt.imshow(image)
    plt.show()
    

def get_collision(body1, body2):
    #Returns collision of corresponding type with body1 and body2, if any. 
    #else returns undefined 
    if body1 == body2:
        return
    
    body1_in_body2_mask = isinstance(body1, body2.collision_mask)
    body2_in_body1_mask = isinstance(body2, body1.collision_mask)
    
    if not body1_in_body2_mask or not body2_in_body1_mask:
        return
    
    if isinstance(body1, Border) and isinstance(body2, Disc):
        # Disc-Border is allowed, Border-Disc is not.
        return Collision.get_collision(body2, body1)
    
    if isinstance(body1, Disc) and isinstance(body2, HorizontalBorder):
        ##Disc-HB collision
        if body2.center.x + body2.length / 2 > body1.center.x and body2.center.x - body2.length / 2 < body1.center.x:
            if body1.center.y - body2.center.y < body1.radius and body2.extends_to == Way.up:
                return DHBCollision(body1, body2)
            elif body2.center.y - body1.center.y < body1.radius and body2.extends_to == Way.down:
                return DHBCollision(body1, body2)
    
    
 
    elif isinstance(body1, Disc) and isinstance(body2, HorizontalBorder):
        if body2.center.x + body2.length / 2 > body1.center.x and body2.center.x - body2.length / 2 < body1.center.x:
            if body1.center.y - body2.center.y < body1.radius and body2.extends_to == Way.up:
                return DHBCollision(body1, body2)
            if body2.center.y - body1.center.y < body1.radius and body2.extends_to == Way.down:
                return DHBCollision(body1, body2)
            
    elif isinstance(body1, Disc) and isinstance(body2, VerticalBorder):
        if body2.center.y + body2.length / 2 > body1.center.y and body2.center.y - body2.length / 2 < body1.center.y:#
            if body1.center.x - body2.center.x < body1.radius and body2.extendsTo == Way.left:
                return DVBCollision(body1, body2)
            elif body2.center.x - body1.center.x < body1.radius and body2.extendsTo == Way.right:
                return DVBCollision(body1, body2)
                      


    elif isinstance(body1, Disc) and isinstance(body2, VerticalBorder):
        if body2.center.y + body2.length / 2 > body1.center.y and body2.center.y - body2.length / 2 < body1.center.y:
            if body1.center.x - body2.center.x < body1.radius and body2.extendsTo == Way.left:
                return DVBCollision(body1, body2)
            elif body2.center.x - body1.center.x < body1.radius and body2.extendsTo == Way.right:
                return DVBCollision(body1, body2)
            
    elif isinstance(body1, Disc) and isinstance(body2, Disc):
        if Vector.sub(body1.center, body2.center).magnitude() <= body1.radius + body2.radius:
            return DDCollision(body1, body2)

    elif isinstance(body1, Kicker) and isinstance(body2, Ball):
        return Collision.get_collision(body2, body1)


    elif isinstance(body1, Ball) and isinstance(body2, Kicker):
        if Vector.sub(body1.center, body2.center).magnitude() <= body1.radius + body2.radius:
            return KickCollision(body1, body2)
