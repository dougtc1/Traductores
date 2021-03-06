#!/usr/bin/python3
# Universidad Simon Bolivar 
#
# Traductores e interpretadores - CI3715
#
# Benjamin Amos. Carnet: 12-10240
# Douglas Torres. Carnet: 11-11027
#
# Proyecto 2
# Archivo que contiene las estructuras de datos donde se guardan los tokens y errores.
from lexBOT import *
from arboles import *
import sys
global symTable

class Token: 
	def __init__(self, name=None, row=None, column=None, arg=None):
		"""Define un token
			
		Argumentos:
		name   -- Nombre del token en cuestion (default None)
		row    -- Numero de fila en la que se encuentra el token (default None)
		column -- Numero de columna en la que inicia el token (default None)
		arg    -- Argumento del token, si es Ident o Num (default None)
		"""
		self.name   = name
		self.row    = row
		self.column = column
		self.arg    = arg

class TokenList:
	def __init__(self, tokList=[], errList=[]):
		"""Define listas que almacenan token y errores
		
		Argumentos:
		tokList -- Lista de tokens (default [])
		errList -- Lista de errores (default [])
		"""
		self.tokList = tokList
		self.errList = errList

	def addTok(self, Token):
		"""Agrega un Token a la lista de tokens"""
		self.tokList.append(Token)

	def addErr(self, Err):
		"""Agrega un Error a la lista de errores"""
		self.errList.append(Err)

	def printTok(self):
		"""Imprime en pantalla el contenido de la lista de tokens"""
		for token in self.tokList:
			if (token.arg == None):
				# En el caso de que el token no sea TkIdent o TkCaracter
				if(self.tokList.index(token) == (len(self.tokList) - 1)):
					print(token.name + " " + str(token.row) + " " +\
					 str(token.column))
				else:
					print(token.name + " " + str(token.row) + " " +\
					 str(token.column) + ",", end=" ")
			else:
				# En caso de que el token sea TkIdent o TkCaracter
				if (token.name == 'TkIdent'):
					if(self.tokList.index(token) == (len(self.tokList) - 1)):
						print(token.name + '("' + str(token.arg) + '") ' +\
						 str(token.row) + " " + str(token.column))
					else:
						print(token.name + '("' + str(token.arg) + '") ' +\
						 str(token.row) + " " + str(token.column) + ",", end=" ")
				else:
					if (token.name == 'TkCaracter' or token.name == 'TkNum'):
						if(self.tokList.index(token) == (len(self.tokList) - 1)):
							print(token.name + '(' + str(token.arg) + ') ' +\
							 str(token.row) + " " + str(token.column))
						else:
							print(token.name + '(' + str(token.arg) + ') ' +\
							 str(token.row) + " " + str(token.column) + ",", end=" ")

	def printErr(self):
		"""Imprime en pantalla el contenido de la lista de errores"""
		for err in self.errList:
			print(err + '\n')

	def notErr(self):
		if (len(self.errList) == 0):
			return True
		else:
			return False
# Estructura de datos correspondiente a la tabla de simbolos
# Esta corresponde a una terna que contiene tipo de la variable
# y su valor. 
class symbolData:
	def __init__(self, tipo, value = None, meType = None, meVal = None):
		self.tipo   = tipo
		self.value  = value
		self.meType = meType
		self.meVal  = meVal 

	"""Modifica el valor del simbolo"""
	def modifValue(self, value):
		self.value = value

	def modifType(self, tipo):
		self.tipo = tipo

	def modifMeType(self, meType):
		self.meType = meType

	def modifMeVal(self, meVal):
		self.meVal = meVal
# Estructura de datos correspondiente a la tabla de simbolos
# Esta corresponde a el diccionario en el que se contendran las
# declaraciones  
class symbolTable:
	def __init__(self, padre = None, hijo = None):
		self.tabla = {}
		self.padre = padre
		self.hijo = hijo
		self.behav = None

	"""Verifica si el simbolo existe en la tabla de simbolos"""
	def symbolExistsForDec(self, symbol):
		if (symbol in self.tabla):
			return True 
		else:
			return False

	def symbolExists(self, symbol):
		if (symbol in self.tabla):
			return True
		elif (self.padre):
			return self.padre.symbolExists(symbol)
		else:
			return False

	"""Crea un par en el diccionario con el nombre de la variable
	como clave y se le asigna solo el tipo"""
	def createTuple(self, symbol, tipo):
		self.tabla[symbol] = symbolData(tipo)
		self.tabla[symbol].modifMeType(tipo)	

	"""Verifica que una variable no exista en la tabla para agregarla"""
	def addSymbol(self, symbol, tipo):
		if (self.symbolExistsForDec(symbol)):
			print("Error: Idenficador " + symbol + ", de tipo: " +\
			self.getSymbolType(symbol) + " ya ha sido declarada.")
			sys.exit()
		else:
			self.createTuple(symbol, tipo)

	"""Retorna el objeto que contiene la informacion de una variable 
	declarada"""
	def getSymbolData(self, symbol):
		if self.symbolExists(symbol):
			return self.tabla[symbol]
		elif (not symbolExists(symbol) and self.padre):
			self.padre.getSymbolData(symbol)
		else:
			print("Error: Idenficador " + symbol + " no declarado")
			sys.exit()

	"""Verifica que exista la variable en la tabla actual para agregar
	el valor correspondiente. De no existir, busca en la tabla padre"""
	def addValue(self, var, valor):
		if symbolExists(var):
			self.getSymbolData(var).modifValue(valor)
			self.getSymbolData(var).modifMeVal(valor)
		elif(self.padre):
			self.padre.addValue()

		print("ERROR, VARIABLE NO DECLARADA")
		sys.exit()

	"""Compara los tipos de un simbolo con otro existente en el diccionario"""
	def compareTypes(self, symbol, symbolType):
		if (getSymbolData(symbol).tipo == symbolType):
			return True
		else:
			return False

	def getSymbolType(self, symbol):
		if (isinstance(symbol, Ident)):
			symbol = symbol.get_valor()
		if (self.symbolExists(symbol)):
			return self.getSymbolData(symbol).tipo
		else:
			print("Error: Idenficador " + str(symbol) + " no definido")
			sys.exit()
		return None

	def addFather(self, padre):
		self.padre = padre

	def addSonNode(self, hijo):
		self.hijo = hijo

	def addBehav(self, behav):
		self.behav = behav

	def printTables(self):
		for keys in self.tabla:
			print("Clave: "+ keys + " Tipo: " + self.tabla[keys].tipo)
		if self.hijo:
			self.hijo.printTables() 

class RobotBehav:
	def __init__(self, bot, instr_list = []):
		self.bot       = bot
		self.inst_list = instr_list

	def addInstr(self, instr):
		self.inst_list.append(instr)

class behavTable:
	def __init__(self, tabAssoc):
		self.behavs   = {}
		self.tabAssoc = tabAssoc
	
	def behavExists(self, behav):	
		if behav in self.behavs:
			return True
		else:
			return False
	
	def createTuple(self, behav, bot):
		self.behavs[behav] = RobotBehav(bot)
	
	def getBehavData(self, behav):
		if self.behavs.behavExists(behav):
			return self.behavs.get(behav)
		else:
			return None

	def addBehav(self, bot, behav):
		if (behav not in self.behavs):
			self.createTuple(behav, bot)
		else:
			print("Error: comportamiento " + behav + " definido mas de una vez para " + bot)
			sys.exit()	
# Esto es como un main de la construccion de la tabla. Me parecio
# demasiado trancado escribir todo lo que esto implica en el main
# aparte de que me estoy dando cuenta de que construyendo metodos se
# puede facilitar el trabajo
class tableBuildUp:
	def __init__(self, tree):
		self.tree = tree

	"""Hay que probarla pero si sirve es super util. Recibe un nodo
	del tipo Dec_List y almacena en una lista todos los identificadores
	declarados"""
	def getID_list(self, ID_list, idlist = None):
		if (not idlist):
			idlist = []
		if (isinstance(ID_list, Ident)):
			idlist.append(ID_list.value)
		elif (isinstance(ID_list, list)):
			self.getID_list(ID_list[0])	
		elif (len(ID_list.children) < 2):
			idlist.append(ID_list.children[0])
		else:
			idlist.append(ID_list.children[0])
			idChildList = ID_list.children[1]
			if (isinstance(idChildList, Ident)):
				idlist.append(idChildList.value)
			else:
				self.getID_list(idChildList, idlist)

		return idlist

	def checkExpressionOk(self, table, expr, ver_condicion = None):
		# SI ARBOLBIN ES DE TIPO ARITMETICO
		if (isinstance(expr, ArbolBin) and expr.tipo == 'ARITMETICA'):
			# LADO IZQUIERDO Y LADO DERECHO NO SON ARBOLBIN
			if (not isinstance(expr.left, ArbolBin) and 
				not isinstance(expr.right, ArbolBin)):
				# SI AMBOS SON NUMEROS
				if(isinstance(expr.left, Numero) and
					isinstance(expr.right, Numero)):
					return True
				# SI UNO ES NUMERO Y EL OTRO ES VARIABLE
				elif(isinstance(expr.left, Numero) and
					isinstance(expr.right, Ident)):
					if (table.getSymbolType(expr.right) == 'int'):
						return True
					else:
						print("Error: tipos incompatibles para '" + expr.left.value +\
						"' de tipo " + table.getSymbolType(expr.left.value) + " y '" +\
						expr.right.value + "' de tipo " +\
						table.getSymbolType(expr.right.value) + " con operacion de " +\
						expr.op)
						sys.exit()
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Numero)):
					if (table.getSymbolType(expr.left) == 'int'):
						return True
					else:
						print("Error: tipos incompatibles para '" + expr.left.value +\
						"' de tipo " + table.getSymbolType(expr.left.value) + " y '" +\
						expr.right.value + "' de tipo " +\
						table.getSymbolType(expr.right.value) + " con operacion de " +\
						str(expr.op))
						sys.exit()
				# SI AMBOS SON VARIABLES
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Ident)):
					if (table.getSymbolType(expr.right) == 'int' and\
						table.getSymbolType(expr.left) == 'int'):
						return True
					else:
						print("Error: tipos incompatibles para '" + expr.left.value +\
						"' de tipo " + table.getSymbolType(expr.left.value)+ " y '" + expr.right.value +\
						"' de tipo " + table.getSymbolType(expr.right.value) + " con operacion de " + str(expr.op))
						sys.exit()
				else:
					print("Error: tipos incompatibles para '" + expr.left.value +\
					"' de tipo " + table.getSymbolType(expr.left.value)+ " y '" + expr.right.value +\
					"' de tipo " + table.getSymbolType(expr.right.value) + " con operacion de " + str(expr.op))
					sys.exit()
			# LADO IZQUIERDO ARBOL Y DERECHO NO ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
				not isinstance(expr.right, ArbolBin)):
				if (expr.left.tipo == 'ARITMETICA'):
					# SI EL DERECHO ES NUMERO
					if (isinstance(expr.right, Numero)):
						return True
					# SI EL DERECHO ES VARIABLE
					elif (isinstance(expr.right, Ident)):
						if (table.getSymbolType(expr.right) == 'int'):
							return True
						else:
							print("Error: tipos incompatibles para expresion de tipo " + expr.left.tipo +\
							" y '" + expr.right.value + "' de tipo " + table.getSymbolType(expr.right.value) +\
							" con operacion de " + str(expr.op))
							sys.exit()
					else:
						print("Error: tipos incompatibles para expresion de tipo " + expr.left.tipo +\
						" y '" +	expr.right.value + "' con operacion de " + str(expr.op))
						sys.exit()	
				else:
					print("Error: tipos incompatibles para expresion de tipo " + expr.left.tipo +\
					" y '" + expr.right.value + "' de tipo " + table.getSymbolType(expr.right.value) +\
					" con operacion de " + str(expr.op))
					sys.exit()
			# LADO DERECHO ARBOL Y IZQUIERDO NO ARBOLBIN
			elif(isinstance(expr.right, ArbolBin) and 
				not isinstance(expr.left, ArbolBin)):
				if (expr.right.tipo == 'ARITMETICA'):
					# SI EL IZQUIERDO ES NUMERO
					if (isinstance(expr.left, Numero)):
						return True
					# SI EL IZQUIERDO ES VARIABLE
					elif (isinstance(expr.left, Ident)):
						if (table.getSymbolType(expr.left) == 'int'):
							return True
						else:
							print("Error: tipos incompatibles para '" + expr.left.value +\
							"' de tipo " + table.getSymbolType(expr.left.value) + " y expresion " +\
							str(expr.right.tipo) + " con operacion de " + str(expr.op))
							sys.exit()
					else:
						print("Error: tipos incompatibles para '" + expr.left.value +\
						"' de tipo " + table.getSymbolType(expr.left.value) + " y expresion " +\
						str(expr.right.tipo) + " con operacion de " + str(expr.op))
						sys.exit()
				else:
					print("Error: tipos incompatibles para '" + expr.left.value +\
					"' de tipo " + table.getSymbolType(expr.left.value) + " y expresion " +\
					str(expr.right.tipo) + " con operacion de " + str(expr.op))
					sys.exit()
			# AMBOS SON ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
			isinstance(expr.right, ArbolBin)):
				if(expr.left.tipo == expr.right.tipo):
					self.checkMeExists(expr.left)
					self.checkExpressionOk(table, expr.left)
					self.checkMeExists(expr.right)
					self.checkExpressionOk(table, expr.right)
					return True
				else:
					print("Error: tipos incompatibles para expresion " + str(expr.left.tipo) +\
					" y expresion " + str(expr.right.tipo) + " con operacion de " + str(expr.op))
					sys.exit()

		# SI ARBOLBIN ES DE TIPO BOOLEANO
		elif (isinstance(expr, ArbolBin) and expr.tipo == 'BOOLEANA'):
			# LADO IZQUIERDO Y LADO DERECHO NO SON ARBOLBIN
			if (not isinstance(expr.left, ArbolBin) and 
				not isinstance(expr.right, ArbolBin)):
				# SI AMBOS SON BOOL
				if(isinstance(expr.left, Bool) and
					isinstance(expr.right, Bool)):
					return True
				# SI UNO ES BOOL Y EL OTRO ES VARIABLE
				elif(isinstance(expr.left, Bool) and
					isinstance(expr.right, Ident)):
					if (table.getSymbolType(expr.right) == 'bool'):
						return True
					else:
						print("Error: tipos incompatibles para '" + expr.left.value +\
						"' de tipo " + table.getSymbolType(expr.left.value) + " y '" +\
						expr.right.value + "' de tipo " +\
						table.getSymbolType(expr.right.value) + " con operacion de " +\
						expr.op)
						sys.exit()
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Bool)):
					if (table.getSymbolType(expr.left) == 'bool'):
						return True
					else:
						print("Error: tipos incompatibles para '" + expr.left.value +\
						"' de tipo " + table.getSymbolType(expr.left.value) + " y '" +\
						expr.right.value + "' de tipo " +\
						table.getSymbolType(expr.right.value) + " con operacion de " +\
						str(expr.op))
						sys.exit()
				# SI AMBOS SON VARIABLES
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Ident)):
					if (table.getSymbolType(expr.right) == 'bool' and\
						table.getSymbolType(expr.left) == 'bool'):
						return True
					else:
						print("Error: tipos incompatibles para '" + expr.left.value +\
						"' de tipo " + table.getSymbolType(expr.left.value)+ " y '" + expr.right.value +\
						"' de tipo " + table.getSymbolType(expr.right.value) + " con operacion de " + str(expr.op))
						sys.exit()
				else:
					print("Error: tipos incompatibles para '" + expr.left.value +\
					"' de tipo " + table.getSymbolType(expr.left.value)+ " y '" + expr.right.value +\
					"' de tipo " + table.getSymbolType(expr.right.value) + " con operacion de " + str(expr.op))
					sys.exit()
			# LADO IZQUIERDO ARBOL Y DERECHO NO ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
				not isinstance(expr.right, ArbolBin)):
				if (expr.left.tipo == 'BOOLEANA'):
					# SI EL DERECHO ES BOOL
					if (isinstance(expr.right, Bool)):
						return True
					# SI EL DERECHO ES VARIABLE
					elif (isinstance(expr.right, Ident)):
						if (table.getSymbolType(expr.right) == 'bool'):
							return True
						else:
							print("Error: tipos incompatibles para expresion de tipo " + expr.left.tipo +\
							" y '" + expr.right.value + "' de tipo " + table.getSymbolType(expr.right.value) +\
							" con operacion de " + str(expr.op))
							sys.exit()
					else:
						print("Error: tipos incompatibles para expresion de tipo " + expr.left.tipo +\
						" y '" +	expr.right.value + "' con operacion de " + str(expr.op))
						sys.exit()	
				else:
					print("Error: tipos incompatibles para expresion de tipo " + expr.left.tipo +\
					" y '" + expr.right.value + "' de tipo " + table.getSymbolType(expr.right.value) +\
					" con operacion de " + str(expr.op))
					sys.exit()
			# LADO DERECHO ARBOL Y IZQUIERDO NO ARBOLBIN
			elif(isinstance(expr.right, ArbolBin) and 
				not isinstance(expr.left, ArbolBin)):
				if (expr.right.tipo == 'BOOLEANA'):
					# SI EL DERECHO ES BOOL
					if (isinstance(expr.left, Bool)):
						return True
					# SI EL DERECHO ES VARIABLE
					elif (isinstance(expr.left, Ident)):
						if (table.getSymbolType(expr.left) == 'bool'):
							return True
						else:
							print("Error: tipos incompatibles para '" + expr.left.value +\
							"' de tipo " + table.getSymbolType(expr.left.value) + " y expresion " +\
							str(expr.right.tipo) + " con operacion de " + str(expr.op))
							sys.exit()
					else:
						print("Error: tipos incompatibles para '" + expr.left.value +\
						"' de tipo " + table.getSymbolType(expr.left.value) + " y expresion " +\
						str(expr.right.tipo) + " con operacion de " + str(expr.op))
						sys.exit()
				else:
					print("Error: tipos incompatibles para '" + expr.left.value +\
					"' de tipo " + table.getSymbolType(expr.left.value) + " y expresion " +\
					str(expr.right.tipo) + " con operacion de " + str(expr.op))
					sys.exit()
			# AMBOS SON ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
			isinstance(expr.right, ArbolBin)):
				if(expr.left.tipo == expr.right.tipo):
					self.checkMeExists(expr.left)
					self.checkExpressionOk(table, expr.left)
					self.checkMeExists(expr.right)
					self.checkExpressionOk(table, expr.right)
					return True
				print("Error: tipos incompatibles para expresion " +\
				str(expr.left.tipo) + " y expresion " + str(expr.right.tipo) +\
				" con operacion de " + str(expr.op))
				sys.exit()

		# SI ARBOLBIN ES RELACIONAL
		elif (isinstance(expr, ArbolBin) and expr.tipo == 'RELACIONAL'):
			# LADO IZQUIERDO Y LADO DERECHO NO SON ARBOLBIN
			if (not isinstance(expr.left, ArbolBin) and 
				not isinstance(expr.right, ArbolBin)):
				# SI AMBOS SON NUMEROS O BOOL
				if(isinstance(expr.left, Numero) and
					isinstance(expr.right, Numero)):
					return True
				elif(isinstance(expr.left, Bool) and
					isinstance(expr.right, Bool)):
					return True
				# SI UNO ES NUMERO O BOOL Y EL OTRO ES VARIABLE
				elif(isinstance(expr.left, Numero) and
					isinstance(expr.right, Ident)):
					if (table.getSymbolType(expr.right) == 'int'):
						return True
					else:
						print("Error: tipos incompatibles para '" + expr.left.value +\
						"' de tipo " + table.getSymbolType(expr.left.value) + " y '" +\
						expr.right.value + "' de tipo " +\
						table.getSymbolType(expr.right.value) + " con operacion de " +\
						expr.op)
						sys.exit()
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Numero)):
					if (table.getSymbolType(expr.left) == 'int'):
						return True
					else:
						print("Error: tipos incompatibles para '" + expr.left.value +\
						"' de tipo " + table.getSymbolType(expr.left.value) + " y '" +\
						expr.right.value + "' de tipo " +\
						table.getSymbolType(expr.right.value) + " con operacion de " +\
						expr.op)
						sys.exit()
				elif(isinstance(expr.left, Bool) and
					isinstance(expr.right, Ident)):
					if (table.getSymbolType(expr.right) == 'bool'):
						return True
					else:
						print("Error: tipos incompatibles para '" + expr.left.value +\
						"' de tipo " + table.getSymbolType(expr.left.value) + " y '" +\
						expr.right.value + "' de tipo " +\
						table.getSymbolType(expr.right.value) + " con operacion de " +\
						expr.op)
						sys.exit()
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Bool)):
					if (table.getSymbolType(expr.left) == 'int'):
						return True
					else:
						print("Error: tipos incompatibles para '" + expr.left.value +\
						"' de tipo " + table.getSymbolType(expr.left.value) + " y '" +\
						expr.right.value + "' de tipo " +\
						table.getSymbolType(expr.right.value) + " con operacion de " +\
						expr.op)
						sys.exit()
				# SI AMBOS SON VARIABLES
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Ident)):
					if ((table.getSymbolType(expr.right) == 'int' and\
						table.getSymbolType(expr.left) == 'int') or\
					(table.getSymbolType(expr.right) == 'bool' and\
						table.getSymbolType(expr.left) == 'bool')):
						return True
					elif (not table.symbolExists(expr.left)):
						print("Error: Identificador " + str(expr.left.get_valor()) + " no definido")
						sys.exit()
					elif (not table.symbolExists(expr.right)):
						print("Error: Identificador " + str(expr.right.get_valor()) + " no definido")
						sys.exit()
					else:
						print("Error: tipos incompatibles para '" + expr.left.value +\
						"' de tipo " + table.getSymbolType(expr.left.value)+ " y '" + expr.right.value +\
						"' de tipo " + table.getSymbolType(expr.right.value) + " con operacion de " + str(expr.op))
						sys.exit()
				else:		
					print("Error: tipos incompatibles para '" + expr.left.value +\
					"' de tipo " + table.getSymbolType(expr.left.value)+ " y '" + expr.right.value +\
					"' de tipo " + table.getSymbolType(expr.right.value) + " con operacion de " + str(expr.op))
					sys.exit()
			# LADO IZQUIERDO ARBOL Y DERECHO NO ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
				not isinstance(expr.right, ArbolBin)):
				if (expr.left.tipo == 'ARITMETICA'):
					# SI EL DERECHO ES NUMERO
					if (isinstance(expr.right, Numero)):
						return True
					# SI EL DERECHO ES VARIABLE
					elif (isinstance(expr.right, Ident)):
						if (table.getSymbolType(expr.right) == 'int'):
							return True
						else:
							print("Error: tipos incompatibles para expresion de tipo " + expr.left.tipo +\
							" y '" + expr.right.value + "' de tipo " + table.getSymbolType(expr.right.value) +\
							" con operacion de " + str(expr.op))
							sys.exit()
					else:
						print("Error: tipos incompatibles para expresion de tipo " + expr.left.tipo +\
						" y '" + expr.right.value + "' de tipo " + table.getSymbolType(expr.right.value) +\
						" con operacion de " + str(expr.op))
						sys.exit()
				if (expr.left.tipo == 'BOOLEANA'):
					# SI EL DERECHO ES BOOL
					if (isinstance(expr.right, Bool)):
						return True
					# SI EL DERECHO ES VARIABLE
					elif (isinstance(expr.right, Ident)):
						if (table.getSymbolType(expr.right) == 'bool'):
							return True
						else:
							print("Error: tipos incompatibles para expresion de tipo " + expr.left.tipo +\
							" y '" + expr.right.value + "' de tipo " + table.getSymbolType(expr.right.value) +\
							" con operacion de " + str(expr.op))
							sys.exit()
					else:
						print("Error: tipos incompatibles para expresion de tipo " + expr.left.tipo +\
						" y '" + expr.right.value + "' de tipo " + table.getSymbolType(expr.right.value) +\
						" con operacion de " + str(expr.op))
						sys.exit()
			# LADO DERECHO ARBOL Y IZQUIERDO NO ARBOLBIN
			elif(isinstance(expr.right, ArbolBin) and 
				not isinstance(expr.left, ArbolBin)):
				if (expr.right.tipo == 'ARITMETICA'):
					# SI EL IZQUIERDO ES NUMERO
					if (isinstance(expr.left, Numero)):
						return True
					# SI EL IZQUIERDO ES VARIABLE
					elif (isinstance(expr.left, Ident)):
						if (table.getSymbolType(expr.left) == 'int'):
							return True
						else:
							print("Error: tipos incompatibles para '" + expr.left.value +\
							"' de tipo " + table.getSymbolType(expr.left.value) + " y expresion " +\
							str(expr.right.tipo) + " con operacion de " + str(expr.op))
							sys.exit()
					else:
						print("Error: tipos incompatibles para '" + expr.left.value +\
						"' de tipo " + table.getSymbolType(expr.left.value) + " y expresion " +\
						str(expr.right.tipo) + " con operacion de " + str(expr.op))
						sys.exit()
				elif (expr.right.tipo == 'BOOLEANA'):
					# SI EL IZQUIERDO ES BOOL
					if (isinstance(expr.left, Bool)):
						return True
					# SI EL IZQUIERDO ES VARIABLE
					elif (isinstance(expr.left, Ident)):
						if (table.getSymbolType(expr.left) == 'bool'):
							return True
						else:
							print("Error: tipos incompatibles para '" + expr.left.value +\
							"' de tipo " + table.getSymbolType(expr.left.value) + " y expresion " +\
							str(expr.right.tipo) + " con operacion de " + str(expr.op))
							sys.exit()
					else:
						print("Error: tipos incompatibles para '" + expr.left.value +\
						"' de tipo " + table.getSymbolType(expr.left.value) + " y expresion " +\
						str(expr.right.tipo) + " con operacion de " + str(expr.op))
						sys.exit()
			# AMBOS SON ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
			isinstance(expr.right, ArbolBin)):
				if(expr.left.tipo == expr.right.tipo):
					self.checkMeExists(expr.left)
					self.checkExpressionOk(table, expr.left)
					self.checkMeExists(expr.right)
					self.checkExpressionOk(table, expr.right)
					return True
				else:
					print("Error: tipos incompatibles para expresion " + str(expr.left.tipo) +\
					 " y expresion " + str(expr.right.tipo) + " con operacion de " + str(expr.op))
					sys.exit()	
			else:
				print("Error: tipos incompatibles para expresion " + str(expr.left.tipo) +\
				 " y expresion " + str(expr.right.tipo) + " con operacion de " + str(expr.op))
				sys.exit()

		if (isinstance(expr, ArbolUn)):
			# SI ES EL NEGATIVO DE UNA EXPRESION
			if (expr.opsymbol == '-'):

				if (isinstance(expr.operando, ArbolBin) or
					isinstance(expr.operando, ArbolUn) or isinstance(expr.operando,Numero)):
					# DEBE SER ARITMETICA
					if(expr.operando.tipo == 'Numero' and not ver_condicion):
						return True
					elif (ver_condicion):
						print("Error: no se aceptan numeros como condiciones.")
						sys.exit()
					else:
						print("Error: tipo incompatible para operacion de '-' y expresion " +\
						str(expr.operando.tipo) + " con operacion de " + str(expr.operando))
						sys.exit()
				else:
					print("Error: tipo incompatible para operacion de '-' y expresion " +\
					str(expr.operando.tipo) + " con operacion de " + str(expr.operando))	
					sys.exit()
			# SI ES EL NEGADO DE UNA EXPRESION
			elif (expr.opsymbol == '~'):
				if (isinstance(expr.operando, ArbolBin)):
					# SI ES ARBOLBIN DEBE SER BOOLEANA O RELACIONAL
					if(expr.operando.tipo == 'BOOLEANA' or
						expr.operando.tipo == 'RELACIONAL'):
						return True
					else:
						print("Error: tipo incompatible para operacion de '~' y expresion " +\
						str(expr.operando.tipo) + " con operacion de " + str(expr.operando))
						sys.exit()
				elif (isinstance(expr.operando, ArbolUn) or isinstance(expr.operando, Ident)):
					# SI ES ARBOLUN DEBE SER BOOLEANA
					if (not table.symbolExists(expr.operando)):
						print("Error: variable " + str(expr.operando.get_valor()) + " no definida.")
						sys.exit()
					if (expr.operando.tipo == 'BOOLEANA'):
						self.checkExpressionOk(table, expr)
						return True

					else:
						print("Error: tipo incompatible para operacion de '~' y expresion " +\
						str(expr.operando.tipo) + " con operacion de " + str(expr.operando))
						sys.exit()
				else:
					print("Error: tipos incompatibles para '~' y expresion " +\
					str(expr.operando.tipo) + " con operacion de " + str(expr.operando))
					sys.exit()

		elif (isinstance(expr, Ident)):
			if (not table.symbolExists(expr.value)):
				print("Error: Identificador '" + str(expr.get_valor()) + "' no definido")
				sys.exit()

	def checkMeExists(self, expr):
		if (isinstance(expr, ArbolBin)):
			if(isinstance(expr.left, Ident) and not isinstance(expr.right, Ident)):
				if (isinstance(expr.right, Numero) or isinstance(expr.right, Bool)):
					if (expr.left.get_valor() == 'me'):
						print("Error: 'me' no esta definido para su uso en " +\
						"instrucciones de controlador.")
						sys.exit()
				elif(isinstance(expr.right, ArbolBin)):
					if (expr.left.get_valor() == 'me'):
						print("Error: 'me' no esta definido para su uso en " +\
						"instrucciones de controlador.")
						sys.exit()
					self.checkMeExists(expr.right)

			elif(isinstance(expr.right, Ident) and not isinstance(expr.left, Ident)):
				if (isinstance(expr.left, Numero) or isinstance(expr.left, Bool)):
					if (expr.right.get_valor() == 'me'):
						print("Error: 'me' no esta definido para su uso en " +\
						"instrucciones de controlador.")
						sys.exit()
				elif(isinstance(expr.left, ArbolBin)):
					if (expr.right.get_valor() == 'me'):
						print("Error: 'me' no esta definido para su uso en " +\
						 "instrucciones de controlador.")
						sys.exit()
					self.checkMeExists(left.right)
			elif(isinstance(expr.right, Ident) and isinstance(expr.left, Ident)):
				if (expr.left.get_valor() == 'me' or expr.right.get_valor() == 'me'):
					print("Error: 'me' no esta definido para su uso en " +\
					"instrucciones de controlador.")
					sys.exit()
			elif (isinstance(expr.left, ArbolBin) and isinstance(expr.right, Ident)):
				if(expr.right.get_valor() == 'me'):
					print("Error: 'me' no esta definido para su uso en " +\
					"instrucciones de controlador.")
					sys.exit()
				self.checkMeExists(expr.left)
			elif(isinstance(expr.right, ArbolBin) and isinstance(expr.left, Ident)):
				if (expr.left.get_valor() == 'me'):
					print("Error: 'me' no esta definido para su uso en " +\
					"instrucciones de controlador.")
					sys.exit()
				self.checkMeExists(expr.right)
			elif(isinstance(expr.right, ArbolBin) and isinstance(expr.left, ArbolBin)):
				self.checkMeExists(expr.left)
				self.checkMeExists(expr.right)
		
		elif(isinstance(expr, ArbolUn)):
			if (expr.get_valor() == 'me'):
				print("Error: 'me' no esta definido para su uso en " +\
					"instrucciones de controlador.")
				sys.exit()
		
		elif(isinstance(expr, Ident)):
			if (expr.get_valor() == 'me'):
				print("Error: 'me' no esta definido para su uso en " +\
					"instrucciones de controlador.")
				sys.exit()

	def checkExprNotInTable(self, table, expr):
		if isinstance(expr, ArbolBin):
			if(isinstance(expr.left, Ident)):
				if expr.left.value in table.tabla:
					print("Error: ", expr.left.value, " no puede ser usado en instrucciones de robot")
			if (isinstance(expr.right, Ident)):
				if expr.right.value in table.tabla:
					print("Error: ", expr.right.value, " no puede ser usado en instrucciones de robot")
			if (isinstance(expr.left, ArbolBin)):
				self.checkExprNotInTable(table, expr.left)
			if (isinstance(expr.right, ArbolBin)):
				self.checkExprNotInTable(table, expr.right)
		elif isinstance(expr, ArbolUn):
			if (isinstance(expr.operando, ArbolBin)):
				self.checkExprNotInTable(expr.operando)
			if (isinstance(expr.operando, Ident)):
				if expr.operando.value in table.tabla:
					print("Error: ", expr.operando.value, " no puede ser usado en instrucciones de robot")

	def checkInstRobot_List(self, table, instr_list, Type):
		inst1 = instr_list.children[0]

		if isinstance(inst1, Store):
			self.checkExprNotInTable(table, inst1.expr)
			self.checkExpressionOk(table, inst1.expr)
		elif isinstance(inst1,Collect):
			if inst1.id_list:
				idList = self.getID_list(inst1.id_list)
				for ID in idList:
					if ID in table.tabla:
						print("Uso de bot ", ID, " prohibido en instrucciones de robot.")
						sys.exit()
					else:
						table.addSymbol(ID, Type)
		elif isinstance(inst1, Drop):
			self.checkExpressionOk(table, expr)
			self.checkExprNotInTable(table, expr)
		elif isinstance(inst1, Direccion):
			self.checkExpressionOk(table, expr)
			self.checkExprNotInTable(table, expr)
		elif(isinstance(inst1, Read)):
			if inst1.id_list:
				idList = self.getID_list(inst1.id_list)
				for ID in idList:
					if ID in table.tabla:
						print("Uso de bot ", ID, " prohibido en instrucciones de robot.")
						sys.exit()
					else:
						table.addSymbol(ID, Type)

	def checkComp_list(self, table, comp_list, idlist, Type, behavTab = None):
		comp = comp_list.children[0]
		condition = comp.children[0]

		if (isinstance(condition.children[0], ArbolBin) or
			isinstance(condition.children[0], ArbolUn)):
			expr = condition.children[0]
			self.checkMeExists(expr)
			self.checkExpressionOk(table, expr)
			if (len(comp_list.children) > 1):
				self.checkComp_list(table, comp_list.children[1])

		elif (isinstance(condition.children[0], Ident)):
			idnt = condition.children[0]

			self.checkMeExists(idnt)
			self.checkExpressionOk(table,idnt)

		elif(condition.children[0] == 'activation' or
			condition.children[0] == 'deactivation' or
			condition.children[0] == 'default' ):
			if (condition.children[0] == 'default' and
				len(comp_list.children) > 1):
				print("Error: comportamiento 'default' definido antes de otros comportamientos.")
				sys.exit()

			if not behavTab:
				behavTab = behavTable(table)

			for ID in idlist:
				behavTab.addBehav(ID, condition.children[0])

			instRobot = comp.children[1]
			self.checkInstRobot_List(table, instRobot, Type)
			
			if (len(comp_list.children) > 1):
				self.checkComp_list(table, comp_list.children[1], idlist, Type, behavTab)
			


	def checkInstC_list(self, table, inst_list):
		instc = inst_list.children[0]
		if (instc.tipoInstruccion == None):
			if (instc.children[0]):
				instc = instc.children[0]

		if (instc.tipoInstruccion == 'ACTIVACION' or
			instc.tipoInstruccion == 'DESACTIVACION' or
			instc.tipoInstruccion == 'AVANCE'):
			id_list = self.getID_list(instc.id_list[0])

			for ID in id_list:
				if table.padre:
					print(table.padre.tabla)

				if (ID == 'me'):
					print("Error, uso de la palabra 'me' fuera de una instruccion de robot.")
					sys.exit()
				elif (not table.symbolExists(ID)):
					print("Error: Idenficador " + str(ID) +" no declarado")
					sys.exit()

			if (len(inst_list.children) > 1):
				inst_list1 = inst_list.children[1]
				self.checkInstC_list(table, inst_list1)

		elif (instc.tipoInstruccion == 'CONDICIONAL'):
			condition = instc.condicion
			self.checkMeExists(condition)
			self.checkExpressionOk(table, condition)

			inst1 = instc.instruccion1
			self.checkInstC_list(table, inst1)

			if (instc.instruccion2):
				inst2 = instc.instruccion2
				self.checkInstC_list(table, inst2)

			if (len(inst_list.children) > 1):
				inst_list1 = inst_list.children[1]
				self.checkInstC_list(table, inst_list1)

		elif (instc.tipoInstruccion == 'ITERACION_INDEF'):
			condition = instc.condicion
			self.checkMeExists(condition)
			self.checkExpressionOk(table, condition)

			instr = instc.instruccion
			self.checkInstC_list(table, instr)

			if (len(inst_list.children) > 1):
				inst_list1 = inst_list.children[1]
				self.checkInstC_list(table, inst_list1)

		elif (instc.tipoInstruccion == "ALCANCE"):
			childTable = symbolTable()
			table.addSonNode(childTable)
			childTable.addFather(table)
			self.fillTable(childTable, instc)

			if (len(inst_list.children) > 1):
				inst_list1 = inst_list.children[1]
				self.checkInstC_list(table, inst_list1)
		else:
			return

	def declist_check(self, table, dec_list):
		#print("YA ESTOY POR ASIGNAR TYPE")
		Type = dec_list.children[0].children[0].children[0]
		#print(Type)
		idlist = dec_list.children[0].children[1]
		for ID in self.getID_list(idlist):
			table.addSymbol(ID, Type)
		idlist = self.getID_list(idlist)
		if (len(dec_list.children[0].children) > 2):
			self.checkComp_list(table, dec_list.children[0].children[2], idlist, Type)
		if(len(dec_list.children) > 1):
			self.declist_check(table, dec_list.children[1])


	"""Aqui se llenara la tabla"""
	def fillTable(self, table, arbol = None):
		if arbol:
			self.tree = arbol
		# Si es instrucciones..
		if (isinstance(self.tree, ArbolInstr)):
			# Vamos a buscar que sea declaraciones
			for child in self.tree.children:
				if (child.token == 'Declaraciones_lista'):
					self.declist_check(table, child)
					#Si tiene comportamiento especificado
				elif (child.token == 'InstC_lista'):
					self.checkInstC_list(table, child)
				elif (child.token == 'Alcance'): 
					self.fillTable(table, child)			

