#!/usr/bin/python3
# Universidad Simon Bolivar 
#
# Traductores e interpretadores - CI3715
#
# Benjamin Amos. Carnet: 12-10240
# Douglas Torres. Carnet: 11-11027
#
# Proyecto 2
# Archivo que contiene el programa principal.

from lexBOT import *
from classes import *

# Primera iteracion, se detectan los posibles errores
lexer.input(content)
while (True):
	tok = lexer.token()
	if (not tok):
		break

# Si se encuentran errores, se imprimen y se finaliza el programa
if (not globalList.notErr()):
	globalList.printErr()
	sys.exit()
  
# Segunda iteracion que solo se realiza en caso de que no se encuentren errores.
# Aqui se detectan los tokens y son almacenados en la estructura de datos
lexer.lineno = 1
lexer.input(content)
while (True):
	tok = lexer.token()
	if (not tok):
		break
	if (tok.type == 'TkIdent' or tok.type == 'TkNum' or\
	 tok.type == 'TkCaracter'):
		globalList.tokList.append(Token(tok.type, tok.lineno,\
		 find_column(content, tok), tok.value))
	else:
		globalList.tokList.append(Token(tok.type, tok.lineno,\
		 find_column(content, tok)))

# IMPRESION DE LOS TOKENS
#globalList.printTok()

######### ETAPA 2 ################

from parser import *
lexer.lineno = 1

# Construccion del parser, del AST e impresion de las instrucciones
parser = yacc.yacc()
parser.parse(content)
symTable = symbolTable()
construccion = tableBuildUp(ASA)
construccion.fillTable(symTable)
#symTable.printTables()

# Se crea la matriz y se pasa al ejecutar
matrix = botMatrix()

ASA.ejecutar(symTable, matrix)
#print("corrio :)")
#ASA.printPreorden()
print("\n")