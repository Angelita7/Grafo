import pygame
import sys
import math
import time

pygame.init()

#imagen = pygame.image.load("pic.png")

pantalla_juego = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Imagen en PyGame - By Parzibyte")

FPS_CLOCK= pygame.time.Clock()


color_blanco = (255, 255, 255)
color = (255,0,0) 
azul = 0,0,255
mouse_pos=(0,0)
nodos=[]
aristas=[]
cantidadCirculos=-1

#----------------------------------------------------------------------------
#crear la clase nodo
class Nodo: 
    def __init__(self,posicion,numero):
        self.posicion = posicion
        self.numeracion = numero
        self.colorNodo = (255,0,0)

    def newcolor(self):
        self.colorNodo=(0,255,0)

    def dibujar(self,pantalla):
        pygame.draw.circle(pantalla, self.colorNodo, self.posicion, 30)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text =font.render(str(self.numeracion), True, (0, 255, 0), (0, 0, 128))
        textRect = text.get_rect()
        textRect.center = (self.posicion[0], self.posicion[1])
        pantalla.blit(text, textRect)


#---------------------------------------------------------------------------
#Creando la clase arista
class Arista:
    def __init__(self, inicio, fin):
        self.circulo1=inicio
        self.circulo2=fin
        
    def dibujar(self):
        pygame.draw.line(pantalla_juego, color,(self.circulo1.posicion[0],self.circulo1.posicion[1]),(self.circulo2.posicion[0],self.circulo2.posicion[1]))

#---------------------------------------------------------------------------
#Creando la clase boton
myFont = pygame.font.SysFont("Calibri", 40)


class Boton():
    def __init__(self,trabajo,ubicacion):
        self.tamano = pygame.Rect(ubicacion)
        self.activar = trabajo
        
    def pintar_boton(self,screen, palabra):
        pygame.draw.rect(screen, (70,189,34), self.tamano, 0)
        texto = myFont.render(palabra, True, (255,255,255)) 
        screen.blit(texto, (self.tamano.x+(self.tamano.width-texto.get_width())/2,
                            self.tamano.y+(self.tamano.height-texto.get_height())/2))

#----------------------------------------------------------------------------
#Creando la clase Recorrido

class Recorrido():
    def __init__(self):
        self.recorrido=[]
        self.animacion=[]
    
    def anadirNodo(self,posicion):
        n=[]
        for i in range(posicion+1):
            n.append(0)
        for j in self.recorrido:
            j.append(0)
        self.recorrido.append(n)
    
    def anadirAnimacion(self,posicion,nodo):
        n=[]
        for i in range(posicion+1):
            n.append(0)
        for j in self.animacion:
            j.append(nodo)
        self.animacion.append(n)

    def mostrar(self):
        fila=0
        columna=0
        for i in self.recorrido:
            print(i,'\n')
            fila+=1
            columna+=1
                    
        
    def anadirArista(self,circulosPresionados):
        self.recorrido[circulosPresionados[0].numeracion][circulosPresionados[1].numeracion]=1
        self.recorrido[circulosPresionados[1].numeracion][circulosPresionados[0].numeracion]=1
        
#----------------------------------------------------------------------------

ubicacionBoton1=10,100,150,50
ubicacionBoton2=10,200,150,50
ubicacionBoton3=10,300,150,50

botonNodo = Boton(False, ubicacionBoton1)
botonArista = Boton(False,ubicacionBoton2)
botonCamino = Boton(False,ubicacionBoton3)

circulosPresionados = []
nuevoRecorrido = Recorrido()
contador=0 
while True:
    

    for event in pygame.event.get():
     
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_button = pygame.mouse.get_pressed(num_buttons=3)
            if botonNodo.tamano.collidepoint(pygame.mouse.get_pos()):
                botonNodo.activar=True
                botonArista.activar=False
                botonCamino.activar=False
                print('activo el nodo')
            if botonArista.tamano.collidepoint(pygame.mouse.get_pos()):
                botonNodo.activar=False
                botonArista.activar=True
                botonCamino.activar=False
                print('activo la arista')

            if botonCamino.tamano.collidepoint(pygame.mouse.get_pos()):
                botonNodo.activar=False
                botonArista.activar=False
                botonCamino.activar=True
                print('activo el camino')
                print(nuevoRecorrido.mostrar())
                print(nodos)

            
                '''for nodo in nodos: 
                    nodo.newcolor()
                    time.sleep(0.5)'''

  
            if  (700 > mouse_pos[0] > 180) and (420 > mouse_pos[1] > 20) and (mouse_button[2]) : 
                if  botonNodo.activar:
                    cantidadCirculos+=1
                    newNodo= Nodo(mouse_pos,cantidadCirculos)
                    nodos.append(newNodo)
                    nuevoRecorrido.anadirNodo(cantidadCirculos)
                    nuevoRecorrido.anadirAnimacion(cantidadCirculos,newNodo)
                 
                elif botonArista.activar:
                    for i in nodos:
                        x1,y1 = mouse_pos[0],mouse_pos[1]
                        x2,y2 = i.posicion[0], i.posicion[1]
                        distance =math.hypot(x1 - x2, y1 - y2)
                        if distance <= 30:
                                circulosPresionados.append(i)
                elif botonCamino.activar:
                    nuevoRecorrido.mostrar()
            elif (700 > mouse_pos[0] > 180) and (420 > mouse_pos[1] > 20) and (mouse_button[1]):
                for i in nodos:
                    x1,y1 = mouse_pos[0],mouse_pos[1]
                    x2,y2 = i.posicion[0], i.posicion[1]
                    distance =math.hypot(x1 - x2, y1 - y2)
                    if distance <= 30:
                            for j in aristas:
                                if j.circulo1==i or j.circulo2==i:
                                    aristas.remove(j)
                            nodos.remove(i)
     
                
                
    
    
    # Actualizamos la pantalla
    pantalla_juego.fill(color_blanco)
    pygame.draw.rect(pantalla_juego, color, pygame.Rect(180, 20, 600, 450),  2)
    if len(circulosPresionados)==2:
        newArista=Arista(circulosPresionados[0],circulosPresionados[1])
        aristas.append(newArista)
        nuevoRecorrido.anadirArista(circulosPresionados)
        

        circulosPresionados = []


    for i in nodos:
        i.dibujar(pantalla_juego)
    for i in aristas:
        i.dibujar()
    
    
    if botonCamino.activar:
        print(contador)
        if (contador < len(nodos)):
            nodos[contador].newcolor()
        print("uno")
        print("dos")
        time.sleep(2)
        contador+=1
        
        
        #print(nuevoRecorrido.animacion)
        #print(nuevoRecorrido.recorrido)
        #print('presionado')
        print("final")
        '''for i in range(len(nuevoRecorrido.animacion)):
            for j in range(len(nuevoRecorrido.animacion[i])):
                if nuevoRecorrido.recorrido[i][j] ==1 and nuevoRecorrido.recorrido[j][i] ==1:
                    print(nuevoRecorrido.animacion[i][j])'''
           
    if (contador>len(nodos) and botonCamino.activar):
            print("if")
            botonCamino.activar=False   

    botonNodo.pintar_boton(pantalla_juego, "Nodo")
    botonArista.pintar_boton(pantalla_juego, "Arista" )
    botonCamino.pintar_boton(pantalla_juego, "Camino" )
    pygame.display.update()