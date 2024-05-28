import pygame
from Enemy import Enemy


class EnemyFactory:
    def __init__(self, screenWidth):
        self.screenWidth = screenWidth
        self.startx = screenWidth
        self.starty = -240

    def create_enemies(self,row:int,col:int) -> tuple[list[list[Enemy]],list[Enemy]]:
        enemies=[]
        enemies_aux=[]
        enemies_list:list[Enemy]=[]

        for i in range(row):
            self.startx = (self.screenWidth - (col * 90 - 45)) // 2
            for j in range(col):
                enemies_aux.append(Enemy(self.startx, self.starty))
                self.startx+=90

            enemies.append(enemies_aux)
            enemies_list.extend(enemies_aux)
            enemies_aux=[]
            col-=1
            self.startx=0
            self.starty+=40
        return (enemies,enemies_list)
