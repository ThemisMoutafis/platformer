from enum import Enum 

class HeroState(Enum):
    WALK = 1
    RUN = 2
    JUMP = 3
    IDLE = 4
    HURT = 5
    DEFEND = 6
    DEATH = 7
    ATTACK = 8
    HEAVYATK = 9
    LIGHTATK = 10