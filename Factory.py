import pygame
from Enemy import Enemy


class EnemyFactory:

    @staticmethod
    def create_enemies(row:int,col:int) -> tuple[list[list[Enemy]],list[Enemy]]:
        enemies=[]
        enemies_aux=[]
        enemies_list:list[Enemy]=[]

        startx=0
        starty=-240
        #(400-35) centro


        for i in range(row):
            startx = (row-col)*45 + 140
            for j in range(col):
                enemies_aux.append(Enemy(startx, starty))
                startx+=90

            enemies.append(enemies_aux)
            enemies_list.extend(enemies_aux)
            enemies_aux=[]
            col-=1
            startx=0
            starty+=40
        return (enemies,enemies_list)



    
"""
enemies=[]
       for i in range(row):
           enemies.append(Enemy(200))
           """