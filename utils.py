import os
import numpy as np
import random
import platform

SO = platform.system()

NAME = {'vazio' : 0, 'organico' : 1, 'reciclavel' : 2, 'agente1':3, 'agente2':4, 'lixeira1':5, 'lixeira2':6, 'incinerador':7, 'recicladora':8}

def get_symbol(c):
	def switch(arg=0):
		s = {
			-1 : '-',
			0: ' ',  # espaco vazio
			1: 'o',  # lixo organico
			2: '*',  # lixo reciclavel
			3: '1',  # robo 1
			4: '2',  # robo 2
			5: 'X',  # lixeira 1
			6: 'Y',  # lixeira 2
			7: 'I',  # incinerador
			8: 'R'   # recicladora
		}
		return s[arg]
	return switch(c)

def comparePositions(x1, y1, x2, y2):
	return x1==x2 and y1==y2

class Point:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y= y

	def equals(self, p): return self.x == p.x and self.y == p.y

	def equals_x(self, p): return self.x == p.x

	def equals_y(self, p): return self.y == p.y


class Lixeira:
	def __init__(self,ident='lixeira1'):
		self.org = 0
		self.rec = 0
		if ident == 'lixeira1':
			self.x = 0
			self.y = 11
		else:
			self.x = 19
			self.y = 11

	def getTotal(self): return self.org + self.rec  

class Space:
	def __init__(self, amountTrash=40, lines=20, columns=20):
		self.m = lines  # quant. linhas
		self.n = columns # quant.colunas

		self.amountTrash = amountTrash
		if self.amountTrash > (self.m * self.n - 4): self.amountTrash = self.m * self.n - 4

		self.trashCount = self.amountTrash
		self.trashCollected = 0
		self.lixeira1 = Lixeira()
		self.lixeira2 = Lixeira('lixeira2')
		self.incinerador = Point(0,self.m-1)
		self.recicladora = Point(self.n-1, self.m-1)
		self.showFirstAgtMapping = False
		self.clear()
		self.generate_trash()

	def clear(self):
		self.lixeira1 = Lixeira()
		self.lixeira2 = Lixeira('lixeira2')
		self.lixeira2.x = self.n-1
		self.mat = np.zeros((self.m,self.n), dtype=np.int32)
		self.mat[self.lixeira1.y][self.lixeira1.x] = NAME['lixeira1']    # lixeira 1
		self.mat[self.lixeira2.y][self.lixeira2.x] = NAME['lixeira2']   # lixeira 2
		self.mat[self.incinerador.y][self.incinerador.x] = NAME['incinerador']    # incinerador
		self.mat[self.recicladora.y][self.recicladora.x] = NAME['recicladora']   # recicladora

	def checkExceptionsTrashPositions(self, value, agentes=None):
		'''if agentes != None:
			for ag in agentes:
				if value == (self.n*ag.y + ag.x):
					return True#'''

		#if (value == self.n*11) or (value == self.n*11+19) or (value == self.n*19) or (value == self.n*19+19):
		r1 = (value == self.n*self.lixeira1.y + self.lixeira1.x)
		r2 = (value == self.n*self.lixeira2.y+self.lixeira2.x)
		r3 = (value == self.n*self.recicladora.y+self.recicladora.x)
		r4 = (value == self.n*self.incinerador.y+self.incinerador.x)
		return r1 or r2 or r3 or r4

	def generate_trash(self, agentes=None):
		if self.amountTrash <= 0:
			return False

		amount = self.amountTrash
		#temp = [i for i in range(self.m * self.n) if i != 0 and i != 19 and i != self.n*11 and i != self.n*11+19 and i != self.n*19 and i != self.n*19+19]
		temp = [i for i in range(self.m * self.n) if not self.checkExceptionsTrashPositions(i, agentes) ]
		random.shuffle(temp)

		for i in temp[:amount]:
			x = i % self.n
			y = i//(self.n)
			value = random.randint(0,1)
			if value == 0: self.mat[y][x] = NAME['organico']
			else: self.mat[y][x] = NAME['reciclavel']
		return True

	def finishedJob(self, ag):
		if ag.name == 'agente1': 
			return self.trashCollected >= self.amountTrash #and comparePositions(ag.x, ag.y, ag.initialPosition.x, ag.initialPosition.y)
		return self.trashCount <= 0 #and comparePositions(ag.x, ag.y, ag.initialPosition.x, ag.initialPosition.y)


	def dumpTrash(self, lixeira, lixo):
		if lixeira == NAME['lixeira1']:
			if lixo == NAME['organico']:
				self.lixeira1.org = self.lixeira1.org + 1
			else:
				self.lixeira1.rec = self.lixeira1.rec + 1

			self.trashCollected = self.trashCollected + 1
			return True
		else:
			if lixo == NAME['organico']:
				self.lixeira2.org = self.lixeira2.org + 1
			else:
				self.lixeira2.rec = self.lixeira2.rec + 1

			self.trashCollected = self.trashCollected + 1
			return True
		return False

	def getTrash(self, lixeira, lixo):
		if lixeira == NAME['lixeira1']:
			if lixo == NAME['organico']:
				if self.lixeira1.org > 0: self.lixeira1.org = self.lixeira1.org - 1
			else:
				if self.lixeira1.rec > 0: self.lixeira1.rec = self.lixeira1.rec - 1
			return True
		else:
			if lixo == NAME['organico']:
				if self.lixeira2.org > 0: self.lixeira2.org = self.lixeira2.org - 1
			else:
				if self.lixeira2.rec: self.lixeira2.rec = self.lixeira2.rec - 1
			return True
		return False

	def clearTaskRobot1(self):
		return self.trashCollected >= self.amountTrash

	def clearTaskRobot2(self):
		return self.trashCount <= 0

	def change(self, x, y, value):
		self.mat[y][x] = value

	def get_value(self, x, y):
		return self.mat[y][x]

	def check_can_move(self, x, y):
		return self.mat[y][x] <= NAME['reciclavel'] or self.mat[y][x] >= NAME['lixeira1']

	# usada para debug
	def countAll(self, agentes):
		c = 0
		for i in range(self.m):
			for j in range(self.n):
				obj = self.mat[i][j]
				if obj == NAME['reciclavel'] or obj == NAME['organico']:
					c = c + 1

		for ag in agentes:
			if ag.bag != 0:
				c = c + 1
			if ag.content == NAME['reciclavel'] or ag.content == NAME['organico']:
				c = c + 1
		return c + self.lixeira1.getTotal() + self.lixeira2.getTotal()

	def getColor(self, value, x, y, showColor=True):
		if not showColor:
			return ''
		if value == NAME['agente1']:
			if comparePositions(self.lixeira1.x, self.lixeira1.y, x, y) or comparePositions(self.lixeira2.x, self.lixeira2.y, x, y): return'\x1b[0;31;43m'
			if comparePositions(self.recicladora.x, self.recicladora.y, x, y): return '\x1b[0;31;44m'
			if comparePositions(self.incinerador.x, self.incinerador.y, x, y): return '\x1b[0;31;47m'
			return '\x1b[0;31;40m'

		if value == NAME['agente2']:
			if comparePositions(self.lixeira1.x, self.lixeira1.y, x, y) or comparePositions(self.lixeira2.x, self.lixeira2.y, x, y): return '\x1b[0;32;43m'
			if comparePositions(self.recicladora.x, self.recicladora.y, x, y): return'\x1b[0;32;44m'
			if comparePositions(self.incinerador.x, self.incinerador.y, x, y): return'\x1b[0;32;47m'
			return '\x1b[0;32;40m'

		if value == NAME['organico']:
			return ''
		if value == NAME['reciclavel']:
			return '\x1b[0;34;40m'

		if value == NAME['lixeira1'] or value == NAME['lixeira2']:
			return '\x1b[0;30;43m' 
		if value == NAME['recicladora']:
			return '\x1b[0;30;44m'
		if value == NAME['incinerador']:
			return '\x1b[0;30;47m'

		return ''

	def show(self, agentes=None, color=True):
		os.system('cls' if SO =='Windows' else 'clear')

		print(' +', end='')
		[print('=', end='') for i in range(self.n)]
		print('+', end='')

		for i in range(self.m):
			print('\n |', end='')
			for j in range(self.n):
				c = self.getColor(self.mat[i][j], j, i, color)

				if c: print(c + get_symbol(self.mat[i][j]) + '\x1b[0m', end='' )
				else: print(get_symbol(self.mat[i][j]), end='')

			print('|      ', end='')#'''
			if self.showFirstAgtMapping and not agentes[0].tipo == 'reativo_simples':
				for j in range(self.n):
					print(get_symbol(agentes[0].spaceCopy.mat[i][j]), end='')

		print('\n +', end='')
		[print('=', end='') for i in range(self.n)]
		print('+', end='\n')

		print('\n LIXEIRA ', ' ORG ', ' REC ')
		print('{:^9}'.format('1'), '{:^5}'.format(self.lixeira1.org), '{:^5}'.format(self.lixeira1.rec))
		print('{:^9}'.format('2'), '{:^5}'.format(self.lixeira2.org), '{:^5}'.format(self.lixeira2.rec))

		print('\n - Falta descartar ', self.trashCount, '/', self.amountTrash, '. ', '\n - Total coletado: ', self.trashCollected, '/',self.amountTrash, sep='')

		#print('All:', self.countAll(agentes))

		'''if agentes:
			for c, ag in enumerate(agentes):
				if ag.name == 'agente2': continue
				print('\nstate: ', c+1, '-', ag.state, ' content: ', ag.content, ' bag: ', ag.bag, ' x:', ag.x, ' y:', ag.y )
				if ag.objective: print('    obj_x:', ag.objective.x, '  obj_y:', ag.objective.y)
			else: print()#'''


		#self.show_agente(ag1)