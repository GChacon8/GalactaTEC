import random
class EnemyMovement:
    def __init__(self, inst_enemies, screenWidth, screenHeight, patron):
        self.inst_enemies = inst_enemies
        self.moving_rigth = True
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        print("EL TAMAÑO DE LA PANTALLA ES:", self.screenWidth, "x", self.screenHeight)
        self.Patter_X_Bools = [True,False,True,False,True,False]
        self.contador = 0
        self.changing = True
        self.patron = patron

        self.enemigo_random = None #Para patron 3
        self.y_coord_inicial = 0
        self.goingdown = True

        

        # print("el ancho es: ", self.screenWidth)
        # print("el alto es: ", self.screenHeight)

    def do_movement(self):
        if self.patron == 1:
            self.pattern_1()
        elif self.patron == 2:
            self.pattern_2()
        elif self.patron == 3:
            self.pattern_3()
        elif self.patron == 4:
            self.pattern_4()
        elif self.patron == 5:
            self.pattern_5()
        else:
            print("Patron indefinido")
            self.pattern_1

        
    #Patrón de vuelo que se mueven leteralmente hasta llegar al borde de la pantalla
    def pattern_1(self):
        if self.moving_rigth:
            for i in self.inst_enemies:
                for j in i:          
                    if j.get_x_coords() >= self.screenWidth-40 and j.is_alive():  #cambiar por funcion de carlos de si estan vivos
                        self.moving_rigth = not self.moving_rigth                  #Y eliminar la funcion creada en enemy
                    j.move_rigth(4)
        else:
            for i in self.inst_enemies:
                for j in i:                
                    if j.get_x_coords() <= 0 and j.is_alive():
                        self.moving_rigth = not self.moving_rigth 
                    j.move_left(4)

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
            if i.get_x_coords() >= self.screenWidth-40 and i.get_isAlive() and not self.changing:
                self.moving_rigth = not self.moving_rigth 
                self.changing = True
            i.move_rigth(4) 

    def pattern2_aux_L(self, fila):
        for i in self.inst_enemies[fila]:
            if i.get_x_coords() <= 0 and i.get_isAlive() and not self.changing:
                self.moving_rigth = not self.moving_rigth
                self.changing = True 
            i.move_left(4)  

    def pattern_3(self):        
        #self.pattern_1()  #Se puede seleccionar el patrón 1 o 2 para que vaya movimiento
        if self.contador == 0:
            try:
                enemigos = [j for i in self.inst_enemies for j in i if j.is_alive()]
                self.enemigo_random = random.choice(enemigos)
                self.y_coord_inicial = self.enemigo_random.get_y_coords()
                self.goingdown = True
                self.contador = 1 #cambiar el contador para que salga de esta condicin
            except:
                # print("No hay enemigos vivos")
                pass
    
        elif self.enemigo_random.get_y_coords() < self.screenHeight-100 and self.goingdown:
            self.enemigo_random.move_down(10)
        
        elif self.enemigo_random.get_y_coords() > self.y_coord_inicial and not self.goingdown:
            self.enemigo_random.move_up(10)

        elif self.enemigo_random.get_y_coords() >= self.screenHeight-100:
            self.goingdown = False
        else:
            self.contador = random.randint(0, 149)
            self.pattern_2()
            
    def pattern_4(self):
        pass

    def pattern_5(self):
        pass

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

