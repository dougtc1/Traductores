#!/usr/bin/python3
# Universidad Simon Bolivar 
#
# Traductores e interpretadores - CI3715
#
# Benjamin Amos. Carnet: 12-10240
# Douglas Torres. Carnet: 11-11027
#
# Proyecto 1
# Archivo que contiene las reglas a usar por el analizador lexográfico.
from classes import *
import sys

# CREACION DE LAS LISTAS DE TOKEN Y ERRORES, APERTURA DE ARCHIVO
global globalList
global content
global symTable
global behavTable

with open(sys.argv[1], 'r') as content_file:
	content = 	content_file.read()
content_file.close()

globalList = TokenList()

#=================================#
#		SECCION DEL LEXER         # 
#=================================#

# Nombres que van a tener los tokens de las palabras reservadas 
tokens = (
	'TkNum', 'TkCaracter', 'TkComa', 'TkPunto', 'TkDospuntos',
	'TkParabre', 'TkParcierra', 'TkSuma', 'TkResta', 'TkMult',
	'TkDiv', 'TkMod', 'TkConjuncion', 'TkDisyuncion',
	'TkNegacion', 'TkMenor', 'TkMenorigual', 'TkMayor',
	'TkMayorigual', 'TkIgual', 'TkComentario', 'TkIdent',
	'TkTab', 'TkQuote', 'TkNoigual', 'TkCreate', 'TkWhile',
	'TkIf', 'TkBool', 'TkInt', 'TkChar', 'TkExecute',
	'TkEnd', 'TkStore', 'TkReceive', 'TkOn', 'TkActivate',
	'TkActivation', 'TkAdvance', 'TkDeactivate',
	'TkDeactivation', 'TkElse', 'TkDefault', 'TkSend',
	'TkCollect', 'TkAs', 'TkDrop', 'TkLeft', 'TkRight',
	'TkUp', 'TkDown', 'TkRead', 'TkTrue', 'TkFalse',
	'TkBot', 'TkMe'
	)

# Lista de palabras reservadas que pertenecen al lenguaje BOT
reserved = {
	"create": 		"TkCreate",
	"while": 		"TkWhile",
	"if": 			"TkIf",
	"bool": 		"TkBool",
	"int": 			"TkInt",
	"char": 		"TkChar",
	"execute": 		"TkExecute",
	"end": 			"TkEnd",
	"store": 		"TkStore",
	"receive": 		"TkReceive",
	"on": 			"TkOn",
	"activate": 	"TkActivate",
	"activation": 	"TkActivation",
	"advance": 		"TkAdvance",
	"deactivate": 	"TkDeactivate",
	"deactivation": "TkDeactivation",
	"else": 		"TkElse",
	"default": 		"TkDefault",
	"send": 		"TkSend",
	"collect": 		"TkCollect",
	"as": 			"TkAs",
	"drop": 		"TkDrop",
	"left": 		"TkLeft",
	"right": 		"TkRight",
	"up": 			"TkUp",
	"down": 		"TkDown",
	"read": 		"TkRead",
	"true": 		"TkTrue",
	"false": 		"TkFalse",
	"bot": 			"TkBot",
	"me": 			"TkMe"
}

#----------------------------------------------------------------#
#						REGLAS PARA TOKENS 						 #
#----------------------------------------------------------------#
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_COMMENT(t):
	r'(\$\-([^\-]|(\-)+[^\$])*[\n]*\-\$)|((\$\$).*)'
	for commentContent in t.value:
		for word in commentContent:
			if (word == '\n'):
				t.lexer.lineno += 1
	t.lexer.lineno += 1
	t.lexer.skip(1)

# Definicion de regla que marca como error un numero seguido de un caracter no numérico
def t_ignoreBadId(t):
	r'\d+[a-zA-Z0-9_]+[a-zA-Z_]+'
	globalList.errList.append("Error: Caracter inesperado "+ '"' +\
	 t.value[0] + '"' + " en la fila " + str(t.lineno) +", columna " +\
	  str(find_column(content, t)))
	t.lexer.skip(1)

def t_TkNum(t):
	r'\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Numero invalido o demasiado grande %d", t.value)
		t.value = 0
	return t

def t_TkIdent(t):
	r'[a-zA-Z][a-zA-Z0-9_]*'
	t.type = reserved.get(t.value,'TkIdent')
	return t

def t_TkCaracter(t):
	r'\'.\''
	t.type = reserved.get(t.value,'TkCaracter')
	return t

def t_error(t):
	globalList.errList.append("Error: Caracter inesperado "+ '"' +\
	 t.value[0] + '"' + " en la fila " + str(t.lineno) +", columna " +\
	  str(find_column(content, t)))
	t.lexer.skip(1)

# SIMBOLOS RECONOCIDOS POR EL LEXER
t_TkComa       = r'\,'
t_TkPunto      = r'\.'
t_TkDospuntos  = r':'
t_TkParabre    = r'\('
t_TkParcierra  = r'\)'
t_TkSuma       = r'\+'
t_TkResta      = r'\-'
t_TkMult       = r'\*'
t_TkDiv        = r'/'
t_TkMod        = r'%'
t_TkConjuncion = r'/\\'
t_TkDisyuncion = r'\\/'
t_TkNegacion   = r'\~'
t_TkMenor      = r'\<'
t_TkMenorigual = r'\<\='
t_TkMayor      = r'\>'
t_TkMayorigual = r'\>\='
t_TkNoigual    = r'/\='
t_TkIgual      = r'\='
t_TkQuote      = r'\''

# LOS ESPACIOS, TABS Y SALTOS DE LINEA SON IGNORADOS
t_ignore = '[ \t]' 

import ply.lex as lex
lexer = lex.lex()

def find_column(input, tok):
		"""
		Permite determinar la columna en la que se
		ubica un determinado token
		Tomado de la documentacion de ply
	 	http://www.dabeaz.com/ply/ply.html#ply_nn9
		"""
		last_cr = input.rfind('\n',1, tok.lexpos)
		if last_cr < 0:
			last_cr = -1
		column = (tok.lexpos - last_cr) 
		return column