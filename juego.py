import numpy as np
import cv2
import random
import time

#############################################
#   Universidad Técnica Particular de Loja  #
#############################################
# Professor:                                #
# Rodrigo Barba        lrbarba@utpl.edu.ec  #
#############################################
# Students:                                 #
# Freddy Jiménez      ffjimenez1@utpl.edu.ec#
# Enrique Cueva       fecueva3@utpl.edu.ec  #
#############################################

class Ball:

	def __init__(self, img, x, y):
		self.img = img
		self.shape = img.shape
		self.x = x
		self.y = y
		self.cont = 0

class Player:

	def __init__(self, color):
		self.color = color
		self.nballs = 0

#convierte el fondo blanco de la imagen a negro
def setWhiteToBlack(ball):
	for c in range(0,2):
		for y in range(0,ball.shape[0]):
			for x in range(0,ball.shape[1]):
				if(ball[y,x,c]>=250):
					ball[y,x,c] = 0

#dibuja una pelota en el frame capturado por la camara
def drawBall(ball):

	x_offset = ball.x
	y_offset = ball.y

	if ball.cont >= -1 and ball.cont <= 0:
		x_offset = x_offset + 1
		y_offset = y_offset + 1
		ball.cont = ball.cont + 1
	elif ball.cont <= 1 and ball.cont >0:
		x_offset = x_offset - 1
		y_offset = y_offset - 1
		ball.cont = ball.cont - 1

	for c in range(0,2):
		frameflip[y_offset:y_offset+ball.shape[0], x_offset:x_offset+ball.shape[1], c] = ball.img[:,:,c] * (ball.img[:,:,c]/255.0) +  frameflip[y_offset:y_offset+ball.shape[0], x_offset:x_offset+ball.shape[1], c] * (1.0 - ball.img[:,:,c]/255.0)

#Verifica si el obetjo de color que se esta detectando esta sobre alguna pelota 
def isOnBall(cx, cy):
	i=0
	for b in balls:
		h,w,_ = b.shape
		if (cx >= b.x and cx<= b.x+w) and (cy >= b.y and cy<= b.y+h):
			return True, b, i	
		i = i+1
	return False, 0, 0

#remover del frameflip una pelota
def deleteBall(b,index):
	h,w,_ = b.shape
	frameflip[b.y:h, b.x:w] = frameflipcpy[b.y:h, b.x:w]
	balls.pop(index)

#retorna la posicion del objeto color verde   
def detectGreenColor():
	return getColorPos(frameflip.copy(), lower_green, upper_green, (0,255,0))


	
#detecta un objeto de un determinado color, dibuja un circulo sobre el y retorna la posicion
def getColorPos(framecp, lowerColor, upperColor, color):
	hsv = cv2.cvtColor(framecp, cv2.COLOR_BGR2HSV)  # Convertimos imagen a HSV
   	
    # Aqui mostramos la imagen en blanco o negro segun el rango de colores.
	mask = cv2.inRange(hsv, lowerColor, upperColor)
    # Limpiamos la imagen de imperfecciones con los filtros erode y dilate
	mask = cv2.erode(mask, None, iterations=6)
	mask = cv2.dilate(mask, None, iterations=6)

    # Localizamos la posicion del objeto
	M = cv2.moments(mask)
	if M['m00'] > 50000:
		cx = int(M['m10'] / M['m00'])
		cy = int(M['m01'] / M['m00'])
		# Mostramos un circulo azul en la posicion en la que se encuentra el objeto
		cv2.circle(frameflip, (cx, cy), 20, color, 2)
		return True, cx, cy

	return False, 0, 0

def addBalls():
	n = random.choice(nb)
	for i in range(n):
		# se crean posiciones aleatorias para ubicar las pelotas en el frameflip
		h,w,_ = ball.shape
		x = random.randint(5, frameflip.shape[1]-w-5)
		y = random.randint(5+h, frameflip.shape[0]-h-5)
		balls.append(Ball(ball, x, y))

#muestra los puntajes al finalizar el juego
def showGameOver(player):
	font = cv2.FONT_HERSHEY_SIMPLEX
	color = (255,255,255)
	pos = (0,0)
	h,w,_ = frame.shape
	p1 = ""
	p2 = ""
	if player.color == "verde":
		pos = (50, h-130)
		text = "Pelotas atrapadas J1: " + str(player.nballs)
	
		
	cv2.putText(final,text,pos, font, 2,color,2,cv2.LINE_AA)

def showNumOfBalls(player):
	font = cv2.FONT_HERSHEY_SIMPLEX
	color = (255,255,255)
	pos = (0,0)
	h,w,_ = frame.shape
	text = ""
	if player.color == "verde":
		color = (0,255,0)
		pos = (50, h-50)
		text = "Jugador1: " + str(player.nballs)
	

	cv2.putText(frameflip,text,pos, font, 2,color,2,cv2.LINE_AA)

def showTime(restante):
	font = cv2.FONT_HERSHEY_SIMPLEX
	color = (255,0,0)
	pos = (20,60)
	text = "Segundos restantes: " + str(int(restante))
	cv2.putText(frameflip, text, pos, font, 2, color, 2, cv2.LINE_AA)

def showTime1(restante):
	font = cv2.FONT_HERSHEY_SIMPLEX
	color = (0,0,0)
	pos = (600,150)
	text = "Puntaje a vencer: " + str(int(restante))
	cv2.putText(frameflip, text, pos, font, 2, color, 2, cv2.LINE_AA)

	
nb = [1,1,1,1,2,2,2,3,3]

#rango de colores para la deteccion
lower_green = np.array([49,100,54])
upper_green = np.array([90,255,183])
lower_red = np.array([160,100,100])
upper_red = np.array([190,255,255])


cap = cv2.VideoCapture(0)
ball = cv2.imread('imagenes/pelota.jpg')
setWhiteToBlack(ball)

p1 = Player('verde')

balls = []
start = True
point_t = random.randint(25,60)
start_t = time.time()
total_t = 0
duracion = 60
while total_t <=duracion :
	#capturar frame por frame
	ret, frame, = cap.read()
	frame = cv2.resize(frame, (0,0), fx=2, fy=2)
	frameflip = cv2.flip(frame.copy(),1)
	frameflipcpy = frameflip.copy()

	if start:
		addBalls()
		start = False
	
	detectedc1, cxg, cyg = detectGreenColor()
	#detectedc2, cxr, cyr = detectRedColor()
	#detectedc2, cxr, cyr = detectBlueColor()

	if detectedc1:
		isOn,b,i = isOnBall(cxg, cyg)
		if isOn:
			deleteBall(b, i)
			p1.nballs = p1.nballs + 1
			if len(balls)<=5:
				addBalls()
	

	for b in balls: #se dibujan las pelotas caputradas
		drawBall(b)

	if cv2.waitKey(1) & 0xFF == ord('q'):  # Indicamos que al pulsar "q" el programa se cierre
		break

	showNumOfBalls(p1) #se muestran los balones dibujados
	
	total_t = time.time()-start_t
	showTime(duracion-total_t) #se muestra el tiempo restante

	showTime1(point_t) #se muestra el puntaje a vencer
	p = point_t
	
	#mostrar el frameflip resultante
	cv2.namedWindow("frameflip", cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty("frameflip",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
	cv2.imshow('frameflip', frameflip)
	
#cargar las imagenes finales del juego
final = cv2.imread('imagenes/game-over.jpg')
end = cv2.imread('imagenes/ganador.jpg')

cap.release()
cv2.destroyAllWindows()

cv2.namedWindow("final", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("final",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
showGameOver(p1)

#condicional
if p1.nballs < p:
        cv2.imshow('final', final) #si el puntaje del jugador es menor o igual al punteje a vencer

if p < p1.nballs:
        cv2.imshow('final', end) #si el puntaje del jugador es mayor o igual al punteje a vencer

cv2.waitKey(0)
cv2.destroyAllWindows()

print "Balones atrapados Jugador1: "+ str(p1.nballs)

print "Tiempo transcurrido: " + str(int(total_t)) + " seg"



