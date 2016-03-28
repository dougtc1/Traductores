#!/usr/bin/python3
# Universidad Simon Bolivar 
#
# Traductores e interpretadores - CI3715
#
# Benjamin Amos. Carnet: 12-10240
# Douglas Torres. Carnet: 11-11027
#
# Proyecto 2
# Archivo que contiene la implementacion de la gramatica del lenguaje BOT.
# 
import ply.yacc as yacc
import re
from arboles import *
from lexBOT import *
global ASA

precedence = (
	('left', 'TkMayor', 'TkMenor', 'TkMayorigual', 'TkMenorigual', 'TkIgual','TkNoigual'),
	('left', 'TkSuma', 'TkResta'),
	('left', 'TkMult', 'TkDiv', 'TkMod'),
	('left', 'TkConjuncion', 'TkDisyuncion'),
	('right', 'TkMenos', 'TkNegacion')
)

###############################################################################
####################### GRAMATICA LIBRE DE CONTEXTO ###########################
###############################################################################

ASA = ArbolInstr()
def p_estructura_Start(p):
	'''Start : TkCreate Declaraciones_lista TkExecute InstC_lista TkEnd
			 | TkExecute InstC_lista TkEnd'''
	if (len(p) == 6):
		ASA.add_token("Start")
		ASA.add_children([p[2], p[4]])
		p[0] = ASA
	else:
		ASA.add_token("Start")
		ASA.add_children([p[2]])
		p[0] = ASA

def p_estructura_Declaraciones_lista(p):
	'''Declaraciones_lista : Declaraciones Declaraciones_lista
						   | Declaraciones'''
	if (len(p) == 3):
		p[0] = ArbolInstr("Declaraciones_lista", [p[1], p[2]])
	else:
		p[0] = ArbolInstr("Declaraciones_lista", [p[1]])

def p_estructura_Declaraciones(p):
	'''Declaraciones : Type TkBot ID_list Comportamiento_lista TkEnd
					 | Type TkBot ID_list TkEnd'''
	if (len(p) == 6):
		p[0] = ArbolInstr("Declaraciones", [p[1], p[3], p[4]])
	else:
		p[0] = ArbolInstr("Declaraciones", [p[1], p[3]])

def p_expresion_Type(p):
	'''Type : TkInt
			| TkBool
			| TkChar'''
	p[0] = ArbolInstr("Type", [p[1]])

def p_expresion_ID_list(p):
	'''ID_list : TkIdent TkComa ID_list
			   | TkIdent
			   | TkMe'''
	if (len(p) == 4):
		p[0] = ArbolInstr("ID_list", [p[1], p[3]])
	else:
		p[0] = Ident(p[1])

def p_instruccion_Comportamiento_lista(p):
	'''Comportamiento_lista : Comportamiento Comportamiento_lista
							| Comportamiento'''
	if (len(p) == 3):
		p[0] = ArbolInstr("Comportamiento_lista", [p[1],p[2]])
	else:
		p[0] = ArbolInstr("Comportamiento_lista",[p[1]])

def p_instruccion_Comportamiento(p):
	'Comportamiento : TkOn Condicion TkDospuntos InstRobot_lista TkEnd'
	if (len(p) == 6):
		p[0] = ArbolInstr("Comportamiento", [p[2], p[4]])

def p_instruccion_Condicion(p):
	'''Condicion : TkActivation
				 | TkDeactivation
				 | Expr
				 | TkDefault'''
	p[0] = ArbolInstr("Condicion",[p[1]])

def p_instruccion_InstC_lista(p):
	'''InstC_lista : InstC InstC_lista
				   | InstC'''
	if (len(p) == 3):
		p[0] = ArbolInstr("InstC_lista",[p[1],p[2]],"SECUENCIACION")
	else:
		p[0] = ArbolInstr("InstC_lista",[p[1]])

def p_instruccion_InstC(p):
	'''InstC : TkActivate ID_list TkPunto
			 | TkDeactivate ID_list TkPunto
			 | TkAdvance ID_list TkPunto
			 | InstrIf
			 | InstrWhile
			 | Alcance'''
	if (p[1] == 'activate'):
		p[0] = Activate("InstrC", None, [p[2]])
	elif (p[1] == 'deactivate'):
		p[0] = Deactivate("InstrC", None, [p[2]])
	elif (p[1] == 'advance'):
		p[0] = Advance("InstrC", None, [p[2]])
	else:
		p[0] = ArbolInstr("InstrC", [p[1]])

def p_instruccion_Alcance(p):
	'''Alcance : TkCreate Declaraciones_lista TkExecute InstC_lista TkEnd
			   | TkExecute InstC_lista TkEnd'''
	if (len(p) == 6):
		p[0] = ArbolInstr("Alcance", [p[2], p[4]], "ALCANCE")
	else:
		p[0] = ArbolInstr("Alcance", [p[2]], "ALCANCE")


def p_instruccion_InstrIf(p):
	'''InstrIf : TkIf Expr TkDospuntos InstC_lista TkEnd 
			   | TkIf Expr TkDospuntos InstC_lista TkElse TkDospuntos InstC_lista TkEnd'''
	if (len(p) == 6):
		p[0] = CondicionalIf("InstrIf", [p[2], p[4]], p[2], p[4])
	else:
		p[0] = CondicionalIf("InstrIf", [p[2], p[4], p[7]], p[2], p[4], p[7])

def p_instruccion_InstrWhile(p):
	'InstrWhile : TkWhile Expr TkDospuntos InstC_lista TkEnd'
	p[0] = IteracionIndef("InstrWhile", [p[1], p[2], p[4]], p[2], p[4])

def p_instruccion_InstRobot_lista(p):
	'''InstRobot_lista : InstRobot InstRobot_lista
					   | InstRobot'''
	if(len(p) == 3):
		p[0] = ArbolInstr("InstRobot_lista",[p[1], p[2]])
	else:
		p[0] = ArbolInstr("InstRobot_lista",[p[1]])

def p_instruccion_InstRobot(p):
	'''InstRobot : TkStore Expr TkPunto 
				 | TkCollect TkPunto 
				 | TkCollect TkAs ID_list TkPunto 
				 | TkDrop Expr TkPunto 
				 | Direccion TkPunto
				 | Direccion Expr TkPunto
				 | TkRead TkPunto 
				 | TkRead TkAs ID_list TkPunto 
				 | TkSend TkPunto 
				 | TkReceive TkPunto'''
	# if (len(p) == 3):
	#     p[0] = ArbolInstr("InstRobot",[p[1]])
	# elif (len(p) == 4):
	#     p[0] = ArbolInstr("InstRobot",[p[1], p[2]])
	# elif (len(p) == 5):
	#     p[0] = ArbolInstr("InstRobot", [p[1], p[2], p[3]])
	
	if (p[1] == "store"):
		p[0] = Store("Store", [p[2]], p[2])
	elif (p[1] == "collect"):
		if (len(p) == 5):
			p[0] = Collect("Collect", [p[3]], p[3])
		else:
			p[0] = Collect("Collect", [p[1]])
	elif (p[1] == "drop"):
		p[0] = Drop("Drop", [p[2]], p[2])
	elif (p[1] == "up" or p[1] == "down" or p[1] == "left" or p[1] == "right"):
		if (len(p) == 4):
			p[0] = Direccion("Direccion", [p[1], p[2]], p[1], p[2])
		else:
			p[0] = Direccion("Direccion", [p[1]], p[1])
	elif (p[1] == "read"):
		if (len(p) == 5):
			p[0] = Read("read", [p[3]], p[3])
		else:
			p[0] = Read("read", [p[1]])
	elif (p[1] == "send"):
		p[0] = Send("send", [p[1]])
	elif (p[1] == "receive"):
		p[0] = Receive("receive")     

def p_instruccion_Direccion(p):
	'''Direccion : TkUp
				 | TkDown
				 | TkLeft
				 | TkRight'''
	#p[0] = ArbolInstr("Direccion", [p[1]])
	p[0] = p[1]

def p_expresion_Expr(p):
	''' Expr : Expr TkSuma Expr
			 | Expr TkResta Expr
			 | Expr TkMult Expr
			 | Expr TkDiv Expr
			 | Expr TkMod Expr
			 | Expr TkConjuncion Expr
			 | Expr TkDisyuncion Expr
			 | Expr TkIgual Expr
			 | Expr TkNoigual Expr
			 | Expr TkMayor Expr
			 | Expr TkMenor Expr
			 | Expr TkMayorigual Expr
			 | Expr TkMenorigual Expr
			 | TkQuote TkNewLine TkQuote
			 | TkParabre Expr TkParcierra
			 | TkResta Expr %prec TkMenos
			 | TkNegacion Expr
			 | TkNum
			 | TkIdent
			 | TkCaracter
			 | TkTrue
			 | TkFalse
			 | TkMe'''

	if (len(p) > 3):
		
		if (p[2] == '+'):
			p[0] = ArbolBin("ARITMETICA", p[1],"'Suma'", p[3], p[2])
		elif (p[2] == "-"):
			p[0] = ArbolBin("ARITMETICA", p[1], "'Resta'", p[3], p[2])
		elif (p[2] == "*"):
			p[0] = ArbolBin("ARITMETICA", p[1], "'Multiplicacion'",p[3], p[2])
		elif (p[2] == "/"):
			p[0] = ArbolBin("ARITMETICA", p[1], "'Division'",p[3], p[2])
		elif (p[2] == "%"):
			p[0] = ArbolBin("ARITMETICA", p[1], "'Modulo'", p[3], p[2])
		elif (p[2] == "/\\"):
			p[0] = ArbolBin("BOOLEANA", p[1], "'Conjuncion'", p[3], p[2])
		elif (p[2] == "\\/"):
			p[0] = ArbolBin("BOOLEANA", p[1], "'Disyuncion'", p[3], p[2])
		elif (p[2] == "="):
			p[0] = ArbolBin("RELACIONAL", p[1], "'Igualdad'", p[3], p[2])
		elif (p[2] == "/="):
			p[0] = ArbolBin("RELACIONAL", p[1], "'Desigualdad'", p[3], p[2])
		elif (p[2] == ">"):
			p[0] = ArbolBin("RELACIONAL", p[1], "'Mayor que'", p[3], p[2])
		elif (p[2] == "<"):
			p[0] = ArbolBin("RELACIONAL", p[1], "'Menor que'", p[3], p[2])
		elif (p[2] == ">="):
			p[0] = ArbolBin("RELACIONAL", p[1], "'Mayor igual que'", p[3], p[2])
		elif (p[2] == "<="):
			p[0] = ArbolBin("RELACIONAL", p[1], "'Menor igual que'", p[3], p[2])
		elif (p[1] == "(" and p[3] == ")"):
			p[0] = p[2]
		elif(p[2] == '\\n'):
			p[0] = NewLine(p[2])  
	else:
		if (p[1] == "-" and len(p) == 3):
			p[0] = ArbolUn("ARITMETICA", "Negativo", p[2], p[1])
		elif (p[1] == "~" and len(p) == 3):
			p[0] = ArbolUn("BOOLEANA", "Negacion", p[2], p[1])
		elif (len(p) == 2 and isinstance(p[1],int)):
			p[0] = Numero(p[1])
		elif (p[1] == 'True' or p[1] == 'False'):
			p[0] = Bool(p[1])
		elif (len(p) == 2 and isinstance(p[1],str)):
			p[0] = Ident(p[1])
	 

def p_error(p):
	if (not p):
		return
	print("Error de sintaxis en la entrada.\nError: '" + str(p.value) +\
	 "' ubicado en la fila {:d}, columna {:d}.".format(p.lineno,\
	  find_column(content, p)))
	sys.exit()

