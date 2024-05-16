
class EnemyMovement:
    def __init__(self, inst_enemies, screenWidth, screenHeight):
        self.inst_enemies = inst_enemies
        self.moving_rigth = True
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        # print("el ancho es: ", self.screenWidth)
        # print("el alto es: ", self.screenHeight)

    def pattern_1(self):
        # print(self.inst_enemies[0][0].get_x_coords())
        for i in self.inst_enemies:
            for j in i:
                #print(self.inst_enemies)
                reference_enemy = self.inst_enemies[5][0].get_x_coords()   
                # print(referenkce_enemy)         
                if self.moving_rigth:
                    if reference_enemy<=(self.screenWidth-315):
                        j.move_rigth()
                    else:
                        self.moving_rigth = False

                else:
                    if reference_enemy>=285:  #cambiar coords para cumplir con ancho de pantalla
                        j.move_left()
                    else:
                        self.moving_rigth = True
                        break
                        