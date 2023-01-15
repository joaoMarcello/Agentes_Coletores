'''
	===========   ATIVIDADE DE INTELIGENCIA ARTIFICIAL :: AGENTES COLETORES   =================
		Simulacao de robos coletando lixo em um ambiente. Dois tipos de robos: os que coletam o lixo,
	e levam pra lixeira e os que levam o lixo da lixeira para o incinerador  ou recicladora,
	dependendo do tipo de lixo q coletou. O programa finaliza quando todos os lixos no ambiente
	foram coletados e descartados corretamente.

	Joao Marcello, 2020
'''
import os
import time

from utils import *
from agente import *

#=============================================================================================+
#                                      CONSTANTES                                             |
#=============================================================================================+

# quant. de linhas do espaco
LINES = 20

# quant. de colunas do espaco
COLUMNS = 20

# a quant. de lixo que sera gerado no ambiente (deve ser menor que LINES * COLUMNS - quant.de agentes - 4)
AMOUNT_TRASH = 40

# flag que informa se deseja mostrar a execucao do programa
SHOW_EXECUTION = True

# Se desejar mostrar a execucao com cores
SHOW_COLOR = True

# Se deseja visualizar o mapeamento do primeiro agente adicionado no ambiente
SHOW_FIRST_AGENT_MAPPING = True

# define o tempo de espera para atualizar cada passo do programa
DELAY = pow(2,-5)

#=============================================================================================+
#                                         FUNCOES                                             |
#=============================================================================================+
# insere um agente em uma lista, se nao existe nenhum agente na posicao informada 
def insertAgent(space, x, y, name, tipo, lista):
	ag = Agente(space, x, y, name, tipo)
	for g in lista:
		if comparePositions(ag.x, ag.y, g.x, g.y):
			return None

	r1 = Point(ag.x, ag.y).equals(ag.space.lixeira1) or Point(ag.x, ag.y).equals(ag.space.lixeira2)
	r2 = Point(ag.x, ag.y).equals(Point(0,19)) or Point(ag.x, ag.y).equals(Point(19,19))
	if r1 or r2:
		return None
	lista.append(ag)
	return ag

# para cada agente, checa qual acao este deve executar e altera o ambiente ao seu redor
def update(agentes):
	for ag in agentes:
		action = ag.select_action()
		action()
# informa de todos os agentes terminaram suas tarefas
def jobDone(agentes, space):
	for ag in agentes:
		if not space.finishedJob(ag):
			return False
	return True
#=============================================================================================+


#=============================================================================================+
#                                         MAIN                                                |
#=============================================================================================+
if __name__ == '__main__':
	# criando o espaco, especificando a quantidade de lixo desejada
	space = Space(amountTrash=AMOUNT_TRASH, lines=LINES, columns=COLUMNS)
	space.showFirstAgtMapping = SHOW_FIRST_AGENT_MAPPING

	

	# lista que contera todos os agentes q atuarao no espaco
	agentes = []

	''' Insira quantos agentes desejar no espaco, especificando a posicao da coluna e linha, o tipo do agente ('agente1' ou 'agente2')
		e o tipo da funcao ('reativo_simples', 'modelo', 'objetivo', 'utilidade') se for tipo 'agente1'. 
		Se for 'agente2' o tipo da funcao pode ser ('objetivo' ou 'utilidade').

		Pelo menos um agente do tipo 'agente1' deve estar no espaco senao
		ninguem coleta o lixo e o progama nao finaliza.
	#'''
	insertAgent(space, 0, 0, 'agente1', 'utilidade', agentes)
	insertAgent(space, 1, 0, 'agente1', 'objetivo', agentes)
	insertAgent(space, 10, 0, 'agente1', 'utilidade', agentes)
	insertAgent(space, 11, 0, 'agente1', 'objetivo', agentes)

	insertAgent(space, COLUMNS-1, 0, 'agente2', 'utilidade', agentes)
	insertAgent(space, COLUMNS-2, 0, 'agente2', 'objetivo', agentes)


    # tempo q durou a execucao do programa
	totalTime = 0.0

	# enquanto os agentes nao terminaram suas tarefas...
	while(not jobDone(agentes, space)): 

		start = time.time()

		update(agentes)

		if SHOW_EXECUTION:
			space.show(agentes, SHOW_COLOR)
		
			if DELAY > 0.:
				time.sleep(DELAY)

		start = time.time() - start
		totalTime = totalTime + start

	l = "+==================================================+"
	r = 'Tempo para conclusao: ' + '{:.3f}'.format(totalTime) + ' s.'
	print(l)
	print( "|", "{:^50}".format('CONCLUIDO!!!!'), "|", sep="" )
	print(l)
	print("|", "{:^50}".format(r), "|", sep="")
	print(l, "\n")

	
