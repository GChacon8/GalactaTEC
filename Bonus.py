import enum

import pygame

from Observer import Collidable

class BonusType(enum.Enum):
    CHASING_BULLET = "Chasing Bullet"
    EXPANDING_BULLET = "Expanding Bullet"
    DOUBLE_POINTS = "Double Points"
    SHIELD = "Shield"
    EXTRA_LIFE = "Extra Life"


class Bonus(Collidable):

    WIDTH = 40

    def __init__(self, posx: int, posy: int, bonus_type: BonusType):
        super().__init__()
        self.image = pygame.image.load( "Images/" + 
                                        bonus_type.value
                                            .lower()
                                            .replace(" ", "_") +
                                        ".png"
                                      )
        self.image = pygame.transform.smoothscale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.type = bonus_type
        self.active = True

    def update(self):
        # Mover el bonus hacia abajo en la pantalla
        self.rect.y += 5
        if self.rect.y > 600:  # Suponiendo que el límite inferior es 600
            self.active = False

    def on_collision(self, other):
        if isinstance(other, Ship):
            print(f"Bonus {self.type.value} collected!")
            self.active = False
            # Aquí se podrían implementar efectos adicionales
    
    def draw(self, screen: pygame.Surface):
        if self.active:
            screen.blit(self.image, self.rect)

    def desactive(self):
        self.active = False
