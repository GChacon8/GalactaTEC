
class EnemyMovement:
    def __init__(self, inst_enemies, screenWidth, screenHeight, patron):
        self.inst_enemies = inst_enemies
        self.moving_rigth = True
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.Patter_X_Bools = [True,False,True,False,True,False]
        self.contador = 0
        self.changing = False
        self.patron = patron
        # print("el ancho es: ", self.screenWidth)
        # print("el alto es: ", self.screenHeight)

    def do_movement(self):
        self.pattern_2()
    #Patrón de vuelo que se mueven leteralmente hasta llegar al borde de la pantalla
    def pattern_1(self):
        if self.moving_rigth:
            for i in self.inst_enemies:
                for j in i:          
                    if j.get_x_coords() >= self.screenWidth-120 and j.is_alive():
                        self.moving_rigth = not self.moving_rigth 
                    j.move_rigth()
        else:
            for i in self.inst_enemies:
                for j in i:                
                    if j.get_x_coords() <= 80 and j.is_alive():
                        self.moving_rigth = not self.moving_rigth 
                    j.move_left()

    def pattern_2(self):   
        if self.moving_rigth:
            self.changing = False
            for i in range(0,6,2):
                self.pattern2_aux_R(i)
            for i in range(1,6,2):
                self.pattern2_aux_L(i)
        else:
            self.changing = False
            for i in range(0,6,2):
                self.pattern2_aux_L(i)
            for i in range(1,6,2):
                self.pattern2_aux_R(i)

    def pattern2_aux_R(self, fila):
        for i in self.inst_enemies[fila]:                
            if i.get_x_coords() >= self.screenWidth-120 and i.get_isAlive() and not self.changing:
                self.moving_rigth = not self.moving_rigth 
                self.changing = True
            i.move_rigth() 

    def pattern2_aux_L(self, fila):
        for i in self.inst_enemies[fila]:
            if i.get_x_coords() <= 80 and i.get_isAlive() and not self.changing:
                self.moving_rigth = not self.moving_rigth
                self.changing = True 
            i.move_left()  

    #cada fila se mueve lateralmente de forma independiente (es caótico)
    def pattern_X(self):
        self.contador = 0
        for i in self.Patter_X_Bools:
            if i:
                self.pattern_X_aux_R(self.contador)
            else:
                self.pattern_X_aux_L(self.contador)
            self.contador += 1

    
    def pattern_X_aux_R(self, fila):
        for i in self.inst_enemies[fila]:                
            if i.get_x_coords() >= self.screenWidth-120 and i.is_alive():
                self.Patter_X_Bools[fila] = not self.Patter_X_Bools[fila] 
            i.move_rigth() 

    def pattern_X_aux_L(self, fila):
        for i in self.inst_enemies[fila]:
            if i.get_x_coords() <= 80 and i.is_alive():
                self.Patter_X_Bools[fila] = not self.Patter_X_Bools[fila]
            i.move_left()  

#probar crear patron de invertir la piramide
#que todas bajen en conjunto

