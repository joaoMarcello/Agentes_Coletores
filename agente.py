#===============================================================================================================+
#                           IMPLEMENTACAO DA CLASSE AGENTE                                                      |
#===============================================================================================================+
from utils import *

class Agente:
	# mapMode: modo como vai mapear os lugares visitados no historico. Se 0, so mapeia o local onde esta pisando, senao mapeia os vizinhos tmb
    def __init__(self, space, x=0, y=0, name='agente1', tipo='objetivo', mapMode=1):
        self.content = space.get_value(x, y)    # o que tem no espaco atual
        space.change(x, y, NAME[name])
        self.name = name
        self.x = x
        self.y = y
        self.initialPosition = Point(self.x, self.y)
        self.tipo = tipo

        self.select_action = self.action_objetivo

        if self.name == 'agente1':
	        if self.tipo == 'modelo': self.select_action = self.action_modelo
	        if self.tipo == 'utilidade': self.select_action = self.action_utilidade
	        if self.tipo == 'reativo_simples': self.select_action = self.action_simple
        else:
        	self.select_action = self.action_ag2_objetivo
        	if self.tipo == 'utilidade': self.select_action = self.action_ag2_utilidade

        self.state = 0			# serve para manter o controle sobre o q o agente esta fazendo
        self.lastState = 0		# serve para guardar o ultimo estado do agente

        self.getAlwaysTheClosiestTrash = False
        self.ignoreTrashInWay = False
        self.selectClosiestFromList = False
        self.takeInciReciPosGetTrash = False

        self.actualAction = self.noop  # serve p/ manter o controle sobre a atual acao de movimento do agente
        self.lastAction = self.noop    # serve p/ guardar a ultima acao de movimento do agente

        self.bag = 0       # aqui armazenara algum lixo
        self.listLixoOrg = []   # lista com os pontos onde tem lixo organico
        self.listLixoRec = []   # lista com os pontos onde tem lixo reciclavel
        self.space = space
        self.spaceCopy = Space(0, self.space.m, self.space.n)  # aqui salva os lugares por onde jah passou. Pode ser resetado a qualquer hora
        self.get_neighbor()   # pegando o conteudo dos vizinhos
        self.mapMode = mapMode # informa como o agente mapeara o espaco. se 1 mapeia posicao atual e vizinhos. senao, so o ponto atual
        #self.mapSpace()


    def get_neighbor(self):
        if self.y-1 >= 0: self.up = self.space.get_value(self.x, self.y-1)
        else: self.up = -1 

        if self.y+1 < self.space.m: self.down = self.space.get_value(self.x, self.y+1)
        else: self.down = -1

       	if self.x-1 >= 0: self.left = self.space.get_value(self.x-1, self.y)
        else: self.left = -1 

        if self.x+1 < self.space.n: self.right = self.space.get_value(self.x+1, self.y)
        else: self.right = -1 


    def insertPoint(self, point, lista ):
        def checkExists(p, points):
            for pp in points:
                if pp.equals(p):
                    return True
            return False

        if not checkExists(point, lista):
            lista.append(point)
            return True
        return False

    def insertNeighborTrash(self):
    	if self.up == NAME['organico']: self.insertPoint(Point(self.x, self.y-1), self.listLixoOrg)
    	else:
    		if self.up == NAME['reciclavel']: self.insertPoint(Point(self.x, self.y-1), self.listLixoRec)#'''

    	if self.down == NAME['organico']: self.insertPoint(Point(self.x, self.y+1), self.listLixoOrg)
    	else:
    		if self.down == NAME['reciclavel']: self.insertPoint(Point(self.x, self.y+1), self.listLixoRec)#'''

    	if self.left == NAME['organico']: self.insertPoint(Point(self.x-1, self.y), self.listLixoOrg)
    	else:
    		if self.left == NAME['reciclavel']: self.insertPoint(Point(self.x-1, self.y), self.listLixoRec)#'''

    	if self.right == NAME['organico']: self.insertPoint(Point(self.x+1, self.y), self.listLixoOrg)
    	else:
    		if self.right == NAME['reciclavel']: self.insertPoint(Point(self.x+1, self.y), self.listLixoRec)#'''

    def mapSpace(self):
    	self.spaceCopy.change(self.x, self.y, -1)
    	if self.mapMode != 0: 
            if self.up != -1: self.spaceCopy.change(self.x, self.y-1, -1)
            if self.down != -1: self.spaceCopy.change(self.x, self.y+1, -1)
            if self.left != -1: self.spaceCopy.change(self.x-1, self.y, -1)
            if self.right != -1: self.spaceCopy.change(self.x+1, self.y, -1)

    def move_up(self):
        # se tem espaco disponivel em cima e nao estiver ocupado por outro robo, lixeiras, recicladora ou incinerador 
        if self.y - 1 >= 0 and self.space.check_can_move(self.x, self.y-1):
            self.space.change(self.x, self.y, self.content)
            self.y = self.y - 1
            self.content = self.space.get_value(self.x, self.y)

            self.get_neighbor()
            self.insertNeighborTrash()

            self.mapSpace()

            self.space.change(self.x, self.y, NAME[self.name])

            return True
        return False

    def move_down(self):
        # se tem espaco disponivel em cima e nao estiver ocupado por outro robo, lixeiras, recicladora ou incinerador 
        if self.y + 1 < self.space.m and self.space.check_can_move(self.x, self.y+1):
            self.space.change(self.x, self.y, self.content)
            self.y = self.y + 1
            self.content = self.space.get_value(self.x, self.y)

            self.get_neighbor()
            self.insertNeighborTrash()

            self.mapSpace()

            self.space.change(self.x, self.y, NAME[self.name])
            return True
        return False

    def move_left(self):
        # se tem espaco disponivel na esquerda e nao estiver ocupado por outro robo, lixeiras, recicladora ou incinerador 
        if self.x - 1 >= 0 and self.space.check_can_move(self.x-1, self.y):
            self.space.change(self.x, self.y, self.content)
            self.x = self.x - 1
            self.content = self.space.get_value(self.x, self.y)

            self.get_neighbor()
            self.insertNeighborTrash()

            self.mapSpace()

            self.space.change(self.x, self.y, NAME[self.name])
            return True
        return False

    def move_right(self):
        # se tem espaco disponivel na direita e nao estiver ocupado por outro robo, lixeiras, recicladora ou incinerador 
        if self.x + 1 < self.space.n and self.space.check_can_move(self.x+1, self.y):  
            self.space.change(self.x, self.y, self.content) # o espaco antigo volta a ser o q era
            self.x = self.x + 1
            self.content = self.space.get_value(self.x, self.y)

            self.get_neighbor()
            self.insertNeighborTrash()
            
            self.mapSpace()

            self.space.change(self.x, self.y, NAME[self.name])
            return True
        return False

    def noop(self):
    	return

    def getTrashInGround(self):
    	if self.bag == 0 and (self.content == NAME['organico'] or self.content == NAME['reciclavel']):
    		self.space.mat[self.y][self.x] = NAME[self.name]
    		self.bag = self.content

    		p = Point(self.x, self.y)
    		self.removePoint(p, self.listLixoOrg if self.content == NAME['organico'] else self.listLixoRec)

    		self.content = 0
    		return True
    	return False

    def getTrashInTrash(self):
    	if self.bag == 0:
    		if (self.content == NAME['lixeira1'] and self.space.lixeira1.rec > 0) or (self.content == NAME['lixeira2'] and self.space.lixeira2.rec > 0):
    			c1 = self.takeInciReciPosGetTrash and self.content == NAME['lixeira1'] and self.space.lixeira1.org > 0
    			qualPegar = NAME['reciclavel'] if not c1 else NAME['organico']

    			self.space.getTrash(self.content, qualPegar)
    			self.bag = qualPegar
    			return True
    		if (self.content == NAME['lixeira1'] and self.space.lixeira1.org > 0) or (self.content == NAME['lixeira2'] and self.space.lixeira2.org > 0):
    			self.space.getTrash(self.content, NAME['organico'])
    			self.bag = NAME['organico']
    			return True
    	return False

    def dumpIntoTrash(self):
    	if self.bag != 0:  # o robo esta segurando algum lixo
    		if (self.bag == NAME['reciclavel'] or self.bag == NAME['organico']) and (self.content == NAME['lixeira2'] or self.content == NAME['lixeira1']):	    		
    			r = self.space.dumpTrash(self.content, self.bag)
	    		if r: self.bag = 0
	    		return r
    	return False

    def dumpIntoRecicler(self):
    	if self.bag != 0:
    		if self.bag == NAME['reciclavel'] and self.content == NAME['recicladora']:
    			self.bag = 0
    			self.space.trashCount = self.space.trashCount - 1
    			return True
    	return False

    def dumpIntoIncinerator(self):
    	if self.bag != 0:
    		if self.bag == NAME['organico'] and self.content == NAME['incinerador']:
    			self.bag = 0
    			self.space.trashCount = self.space.trashCount - 1
    			return True
    	return False


    def isHoldingTrash(self): return self.content == NAME['organico'] or self.content == NAME['reciclavel']


    def getTrash(self):
    	if self.name == 'agente1':
    		return self.getTrashInGround()
    	else:
    		return self.getTrashInTrash()

    def dumpTrash(self):
    	if self.name == 'agente1':
    		return self.dumpIntoTrash()
    	else:
    		return self.dumpIntoIncinerator() or self.dumpIntoRecicler()

    def distance(self, x, y):
    	d = abs(self.x-x) + abs(self.y-y)
    	return d

    def removePoint(self, point, lista):
    	for c, p in enumerate(lista):
    		if p.equals(point):
    			del lista[c]
    			return True

    	return False

    def closiestPoint(self, lista):
    	d = 1000000000
    	point = False
    	index = 0
    	for num, p in enumerate(lista):
    		if self.distance(p.x, p.y) < d:
    			d = self.distance(p.x, p.y)
    			point = p
    			index = num
    	return point, index

    
    def getRandomMove(self, exceto=None):
    	def switch_move(arg=0):
    		if arg == 1: return self.move_right
    		if arg == 2: return self.move_left
    		if arg == 3: return self.move_up
    		return self.move_down

    	def execao_to_int(arg):
    		if arg is not None:
    			if arg == 'right': arg=1
    			else:
    				if arg == 'left': arg=2
    				else:
    					if arg == 'up' : arg=3
    					else:
    						arg=4
    		return arg

    	exceto = execao_to_int(exceto)
    	r = random.randint(1, 5)
    	if exceto is not None and r == exceto: r = (r + 1) % 4
    	return switch_move(r)

    def goToPosition(self):
        if not self.objective: return self.getRandomMove()

        x = self.objective.x
        y = self.objective.y

        self.get_neighbor()

        if self.x < x:
            if self.spaceIsOccupied(self.right): 
            	return self.getRandomMove() 
            return self.move_right
        if self.x > x:
            if self.spaceIsOccupied(self.left): 
            	return self.getRandomMove()
            return self.move_left
        if self.y < y:
            if self.spaceIsOccupied(self.down): 
            	return self.getRandomMove() 
            return self.move_down
        if self.y > y:
            if self.spaceIsOccupied(self.up):
            	return self.getRandomMove()
            return self.move_up
        
        return self.noop

    def spaceIsOccupied(self, content):
    	return content == -1 or (content == NAME['agente1'] or content==NAME['agente2'])

    def isLandingInTrash(self): return self.content == NAME['organico'] or self.content == NAME['reciclavel']

    def actualLineIsComplete(self):
    	for i in range(self.spaceCopy.n):
    		if self.spaceCopy.mat[self.y][i] == 0:
    			return False

    		if self.up != -1 and self.spaceCopy.mat[self.y-1][i] == 0:
    			return False
    	return True

    def bottomSpaceIsComplete(self):
    	for i in range(self.space.lixeira1.y, self.space.m):
    		for k in range(self.space.n):
    			if self.spaceCopy.mat[i][k] == 0:
    				return False
    	return True

    def getNextLixoOrg(self, closiest=False):
    	if len(self.listLixoOrg) != 0:
    		if not closiest:
    			return self.listLixoOrg[0], 0
    		else:
    			p, index = self.closiestPoint(self.listLixoOrg)
    			return p, index
    	return None, None

    def getNextLixoRec(self, closiest=False):
    	if len(self.listLixoRec) != 0:
    		if not closiest:
    			return self.listLixoRec[0], 0
    		else:
    			p, index = self.closiestPoint(self.listLixoRec)
    			return p, index
    	return None, None

    def selectNextTrash(self):

    	r = False
    	if self.getAlwaysTheClosiestTrash:
    		r, index = self.closiestPoint(self.listLixoRec + self.listLixoOrg)
    		index = index % (len(self.listLixoRec)+1)
    		if r:
    			self.state = states['goingGetTrash']
    			self.objective = r
    		return r, index


    	# checando se sabe a posicao de algum lixo reciclavel
    	r, index = self.getNextLixoRec(self.selectClosiestFromList)
    	if r:
    		self.state = states['goingGetTrash']
    		self.objective = r

    	# se nao sabe a posicao de lixo reciclavel, checa se sabe a posicao de algum lixo organico
    	if not r:
       		r, index = self.getNextLixoOrg(self.selectClosiestFromList)
        	if r:
        		self.state = states['goingGetTrash']
        		self.objective = r

    	return r, index


    # varre o espaco indo na horizontal, chega ao final da linha, avanca pra proxima linha, percorre a linha, avanca pra proxima e assim
    # por diante, sempre mapeando onde tem lixo (quando encontra ele leva pra lixeira mais proxima). quando chega no final e nao sabe onde tem algum lixo, 
    # volta pra posicao inicial e percorre o espaco novamente. se percorreu todos os espacos e nao tem mais lixo, volta pra posicao inicial.
    def movement1(self):
    	if self.name == 'agente1' and self.space.clearTaskRobot1():
    		self.objective = self.initialPosition
    		return self.goToPosition()

    	if self.bag == 0: # se esta vazio
    		self.lastState = self.state

    		self.objective = None

    		r, index = self.selectNextTrash()

    		# se setou como objetivo procurar um lixo mas chegando no local nao ha lixo nenhum
	    	if r and comparePositions(self.objective.x, self.objective.y, self.x, self.y) and not self.isLandingInTrash():
	    		self.removePoint(self.objective, self.listLixoRec)
	    		self.removePoint(self.objective, self.listLixoOrg)
	    		self.state = 0
	    		return self.noop

    		if self.ignoreTrashInWay:
    			if r:
    				if comparePositions(self.x, self.y, self.objective.x, self.objective.y):
    					self.state = 0
    					return self.getTrash
    		else:
    			# checa se estah em um espaco com lixo, se sim, pega e vai para a lixeira
		    	if self.isLandingInTrash():
	    			# nao ignora o lixo no caminho, ou seja, se estava indo a algum lugar mas encontrou
	    		    # algum lixo, recolhe e o leva pra lixeira. 
	    			self.state = 0
	    			return self.getTrash


	    	if self.state == states['goingGetTrash']:
	    		return self.goToPosition()
	    		
	    	if self.state == states['dump'] and self.bottomSpaceIsComplete():
	    		self.state = states['goInicialPos']

	    	# =============== nao tem nenhum lixo q ja conheca a posicao, entao se movimenta ======================================
	    	if self.state == states['goInicialPos']:
	    		self.objective = Point(0,0)
	    		if comparePositions(self.objective.x, self.objective.y, self.x, self.y):
	    			self.state = 0
	    	else:
		    	if self.state != states['goStartLine']:
		    		self.state = states['goFinalLine']
		    	if self.x >= self.space.n-1 or self.right == NAME['agente2']:
		    		self.state = states['avanceLine']

		    	if self.state == states['avanceLine']:
		    		if self.spaceIsOccupied(self.down) or self.lastState == self.state:
		    			self.state = states['goStartLine']

		    	if self.state == states['goFinalLine']:
		    		self.objective = Point(self.space.n-1, self.y)

		    	if self.state == states['avanceLine']:
		    		self.objective = Point(self.x, self.y + 1)

		    	if self.state == states['goStartLine']:
		    		self.objective = Point(0, self.y)
		    		if comparePositions(self.objective.x, self.objective.y, self.x, self.y):
	    				self.state = states['avanceLine']
	    				self.objective = Point(self.x, self.y + 1)

    		if self.y == self.space.m-1 and self.actualLineIsComplete():
    				self.state = states['goInicialPos']
    				self.objective = Point(0,0)


	    	if self.objective is not None:
    			return self.goToPosition()
    		else:
    			return self.noop


    	else:  # esta com lixo

    		disl1 = self.distance(self.space.lixeira1.x, self.space.lixeira1.y)	
    		disl2 = self.distance(self.space.lixeira2.x, self.space.lixeira2.y)
    		closiest_lix = self.space.lixeira1 if disl1 <= disl2 else self.space.lixeira2

    		self.objective = Point(closiest_lix.x, closiest_lix.y)
    		action = self.goToPosition()
    		
    		if not comparePositions(self.x, self.y, self.objective.x, self.objective.y):
    			self.state = states['goingToTrash']
    			return action
    		else:
    			self.state = states['dump']
    			return self.dumpTrash

    # mesmo movimento de 1 mas avanca pra proxima linha quando a atual ja foi completamente verificada
    def movement2(self):
    	action = self.movement1()

    	if (self.state == states['goFinalLine'] or self.state == states['goStartLine']) and self.actualLineIsComplete():
    		self.state = states['avanceLine']
    		self.objective = Point(self.x, self.y+1)
    		return self.goToPosition()

    	'''if self.state == states['goInicialPos'] and action == self.move_up and self.actualLineIsComplete() and self.y < self.space.lixeira1.y:
    		self.state = states['avanceLine']
    		self.objective = Point(self.x, self.y+1)
    		return self.goToPosition()#'''

    	return action

    # o movimento do agente2: vai para a lixeira mais proxima, pega o lixo, se tiver, dando prioridade para os reciclaveis.
    # vai para o incinerador ou recicladora dependendo do tipo de lixo e repete o ciclo. quando todos os lixos ja foram depositados
    # na recicladora ou incinerador, o agente2 volta pra posicao inicial.
    def movement3(self):
    	if self.space.clearTaskRobot2():
    		self.objective = self.initialPosition
    		return self.goToPosition()

    	if self.bag == 0:
    		self.objective = None

    		if self.state == 0:
    			disl1 = self.distance(self.space.lixeira1.x, self.space.lixeira1.y)
    			disl2 = self.distance(self.space.lixeira2.x, self.space.lixeira2.y)
    			self.state = states['goToL1'] if disl1 <= disl2 else states['goToL2']

    		if self.state == states['goToL2']:
    			self.objective = Point(self.space.lixeira2.x, self.space.lixeira2.y)

    		if self.state == states['goToL1']:
    			self.objective = Point(self.space.lixeira1.x, self.space.lixeira1.y)

    		if self.state == states['goToL1'] or self.state == states['goToL2']:
    			if comparePositions(self.x, self.y, self.objective.x, self.objective.y):
    				c1 = self.state == states['goToL1'] and self.space.lixeira1.getTotal() > 0
    				c2 = not c1 and self.state == states['goToL2'] and self.space.lixeira2.getTotal() > 0
    				if c1 or c2:
    					return self.getTrash
    				else:
    					self.state = states['goToL1'] if comparePositions(self.x, self.y, self.space.lixeira2.x, self.space.lixeira2.y) else states['goToL2'] 
    					return self.noop
    				'''self.waitingCount = self.waitingCount + 1
    				if self.waitingCount <= 1:
    					return self.getTrash
    				else:
    					self.waitingCount = 0
    					self.objective = None
    					self.state = states['goToL1'] if self.state == states['goToL2'] else states['goToL2']
    					return self.noop#'''


    		if self.objective is not None:
    			return self.goToPosition()
    		else:
    			return self.noop()

    	else:
    		self.objective = None
    		if self.bag == NAME['reciclavel']:
    			self.objective = Point(self.space.recicladora.x,self.space.recicladora.y)
    		else:
    			self.objective = Point(self.space.incinerador.x, self.space.recicladora.y)


    		if comparePositions(self.x, self.y, self.objective.x, self.objective.y):
    			self.state = 0
    			#self.waitingCount = 0
    			return self.dumpTrash

    		if self.objective is not None:
    			return self.goToPosition()
    		else:
    			return self.noop()


    def isTrash(self, value):
    	return value == NAME['organico'] or value == NAME['reciclavel']

    # se move aleatoriamente. se encontra qualquer lixo, no espaco atual recolhe o lixo e vai para a lixeira mais proxima.
    # se na vizinhanca tem algum lixo, ele vai para aquele lugar, recolhe o lixo e leva para a lixeira mais proxima
    def movement4(self):
    	if self.name == 'agente1' and self.space.clearTaskRobot1():
    		self.objective = self.initialPosition
    		return self.goToPosition()

    	if self.bag == 0:
    		self.objective = None

    		if self.isLandingInTrash():
    			self.state = 0
    			return self.getTrash

    		r1 = self.up != -1 and self.isTrash( self.space.get_value(self.x, self.y-1) )
    		r2 = self.down != -1 and self.isTrash(self.space.get_value(self.x, self.y+1))
    		r3 = self.left != -1 and self.isTrash(self.space.get_value(self.x-1, self.y))
    		r4 = self.right != -1 and self.isTrash(self.space.get_value(self.x+1, self.y))

    		if r1 or r2 or r3 or r4:
    			if r1: return self.move_up
    			if r2: return self.move_down
    			if r3: return self.move_left
    			return self.move_right

    		return self.getRandomMove()
    	else:
    		self.objective = None
    		disl1 = self.distance(self.space.lixeira1.x, self.space.lixeira1.y)	
    		disl2 = self.distance(self.space.lixeira2.x, self.space.lixeira2.y)
    		closiest_lix = self.space.lixeira1 if disl1 <= disl2 else self.space.lixeira2

    		self.objective = Point(closiest_lix.x, closiest_lix.y)
    		action = self.goToPosition()
    		
    		if not comparePositions(self.x, self.y, self.objective.x, self.objective.y):
    			return action
    		else:
    			return self.dumpTrash

    def action_simple(self):
    	self.lastAction = self.actualAction
    	self.actualAction = self.movement4()
    	return self.actualAction

    '''	agente 1 baseado em modelo: mapeia as posicoes q jah passou e os lixos q encontrou na sua posicao atual e vizinhancas. Move linha a linha, 
    	horizontalmente. Passa para a proxima linha quando chega no final ou no comeco da linha atual. Se chega no final do espaco, volta 
    	pra primeira posicao do espaco realizando o mesmo movimento de percorrer a linha horizontalmente (se ainda nao mapeou todo o espaco).

    	Nao verifica se a linha atual do espaco ja foi completamente mapeada, por isso caso ele esteja em uma linha repetida, vai percorre-la inteira
    	novamente  :-(

    	Sempre q encontra algum lixo no caminho, ele pega e leva pra lixeira mais proxima. se ele sabe o local de algum lixo, ele vai atras desse lixo,
    	mas se encontrar algum outro lixo no caminho seja de qualquer tipo, ele pega e leva pra lixeira. Dos lixos q sabe a posicao, sempre vai atras
    	do mais proximo lixo reciclavel seguido do mais proximo lixo organico caso nao saiba a posicao de mais nenhum reciclavel.

    	Se mapeou todo o espaco e nao tem mais lixo, volta pra posicao inicial '''
    def action_modelo(self):
    	self.lastAction = self.actualAction
    	self.actualAction = self.movement1()
    	return self.actualAction

    '''	agente 1 baseado em objetivo: mapeia as posicoes q jah passou e os lixos q encontrou na sua posicao atual e vizinhancas. Move linha a linha, 
    	horizontalmente. Passa para a proxima linha quando chega no final ou no comeco da linha atual. Se chega no final do espaco, volta 
    	pra primeira posicao do espaco realizando o mesmo movimento de percorrer a linha horizontalmente (se ainda nao mapeou todo o espaco).

    	Sempre verifica se a linha q esta percorrendo e a anterior(para impedir espacos em brancos nao mapeados) ja foi completamente mapeada.
    	Se sim, avanca pra proxima linha.

    	O objetivo do modelo eh coletar cada lixo o mais rapido possivel. A partir do seu mapeamento, ele consegue selecionar o ponto q deve ir
    	para recolher algum lixo, dando preferencia pros reciclaveis. Se nao sabe a posicao de nenhum lixo, ele faz o movimento descrito anteriormente
    	(linha a linha, horizontalmente).

    	Sempre q encontra algum lixo no caminho (nao importa o tipo), ele pega e leva pra lixeira mais proxima (ignorando o q estava buscando).
    	Resumo: se ele sabe o local de algum lixo, ele vai atras desse lixo, mas se encontrar algum outro lixo no caminho seja de qualquer tipo,
    	ele pega e leva pra lixeira.

    	Se mapeou todo o espaco e nao tem mais lixo, volta pra posicao inicial '''
    def action_objetivo(self):
    	self.getAlwaysTheClosiestTrash = True
    	self.lastAction = self.actualAction
    	self.actualAction = self.movement2()
    	return self.actualAction

    '''	agente 1 baseado em utilidade: mapeia as posicoes q jah passou e os lixos q encontrou na sua posicao atual e vizinhancas. Move linha a linha, 
    	horizontalmente. Passa para a proxima linha quando chega no final ou no comeco da linha atual. Se chega no final do espaco, volta 
    	pra primeira posicao do espaco realizando o mesmo movimento de percorrer a linha horizontalmente (se ainda nao mapeou todo o espaco).

    	Sempre verifica se a linha q esta percorrendo e a anterior(para impedir espacos em brancos nao mapeados) ja foi completamente mapeada.
    	Se sim, avanca pra proxima linha.

    	O objetivo do agente baseado em utilidade eh recolher cada lixo dando prioridade maxima aos reciclaveis. A partir do seu mapeamento, ele consegue selecionar o ponto q deve ir
    	para recolher algum lixo, dando preferencia pros reciclaveis. Se nao sabe a posicao de nenhum lixo, ele faz o movimento descrito anteriormente
    	(linha a linha, horizontalmente).

    	Se estava buscando algum um lixo e passar em cima de algum outro lixo no caminho, ele pega e leva pra lixeira se for reciclavel. Senao apenas
    	ignora (mas mapeia sua posicao pra buscar depois XD ).

    	Se mapeou todo o espaco e nao tem mais lixo, volta pra posicao inicial '''
    def action_utilidade(self):
    	self.selectClosiestFromList = True
    	self.ignoreTrashInWay = True
    	self.lastAction = self.actualAction
    	self.actualAction = self.movement2()
    	return self.actualAction

    def action_ag2_utilidade(self):
    	self.actualAction = self.lastAction
    	self.actualAction = self.movement3()
    	return self.actualAction

    def action_ag2_objetivo(self):
    	self.takeInciReciPosGetTrash = True
    	self.actualAction = self.lastAction
    	self.actualAction = self.movement3()
    	return self.actualAction    	




states = {
'goingGetTrash':1, 'dumpTrash' : 2, 'goingToTrash' : 3, 'goFinalLine' : 4, 'goStartLine' : 5, 'avanceLine' : 6,
'goInicialPos' : 7, 'dump' : 8, 'waiting_l1' : 9, 'waiting_l2' : 10, 'goToIncinerator':11, 'goToReciclator' : 12, 'goToL1':13, 'goToL2':14,
'finished':15}





