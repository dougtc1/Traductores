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
def symbolData:
	def __init__(self, tipo, value = None):
		self.tipo = tipo
		self.value = value

	"""Modifica el valor del simbolo"""
	def modifValue(self, value):
		self.value = value

	def modifType(self, tipo):
		self.tipo = tipo

# Estructura de datos correspondiente a la tabla de simbolos
# Esta corresponde a el diccionario en el que se contendran las
# declaraciones  
def symbolTable:
	def __init__(self, padre = None):
		self.tabla = {}
		self.padre = padre

	"""Verifica si el simbolo existe en la tabla de simbolos"""
	def symbolExists(self, symbol):
		if symbol in self.tabla:
			return True
		else:
			return False

	"""Crea un par en el diccionario con el nombre de la variable
	como clave y se le asigna solo el tipo"""
	def createTuple(self, symbol, tipo):
		self.tabla[symbol] = symbolData(tipo)		

	"""Verifica que una variable no exista en la tabla para agregarla"""
	def addSymbol(self, symbol, tipo):
		if (symbolExists(symbol) and self.getSymbolData(symbol).tipo == tipo):
			print("ERROR. VARIABLE YA DECLARADA")
			sys.exit()
		elif(symbolExists(symbol) and self.getSymbolData(symbol).tipo != tipo):
			self.getSymbolData(symbol).modifType(tipo)
		else:
			self.createTuple(symbol, tipo)

	"""Retorna el objeto que contiene la informacion de una variable 
	declarada"""
	def getSymbolData(self, symbol):
		if symbolExists(symbol):
			return self.tabla[symbol]

		return None

	"""Verifica que exista la variable en la tabla actual para agregar
	el valor correspondiente. De no existir, busca en la tabla padre"""
	def addValue(self, var, valor):
		if symbolExists(var):
			self.getSymbolData(var).modifValue(valor)
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
		if (self.symbolExists(symbol)):
			return self.getSymbolData(symbol).tipo
		return None

# Esto es como un main de la construccion de la tabla. Me parecio
# demasiado trancado escribir todo lo que esto implica en el main
# aparte de que me estoy dando cuenta de que construyendo metodos se
# puede facilitar el trabajo
def tableBuildUp:
	def __init__(self, tree, table):
		self.tree = tree
		self.table = table

	"""Hay que probarla pero si sirve es super util. Recibe un nodo
	del tipo Dec_List y almacena en una lista todos los identificadores
	declarados"""
	def getID_list(self, ID_list, list = None):
		idlist = []

		if (len(ID_list.children) < 2):
			idlist.append(ID_list.children[0])
		else:
			idlist.append(ID_list.children[0])
			idChildList = ID_list.children[1]
			self.getID_list(idChildList, idlist)

		return idlist

	def checkExpressionOk(self, expr):
		# SI ARBOLBIN ES DE TIPO ARITMETICO
		if (expr.tipo == 'ARITMETICA'):
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
					if (self.table.getSymbolType(expr.right) == 'int'):
						return True
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Numero)):
					if (self.table.getSymbolType(expr.left) == 'int'):
						return True
				# SI AMBOS SON VARIABLES
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Ident)):
					if (self.table.getSymbolType(expr.right) == 'int' and\
						self.table.getSymbolType(expr.left) == 'int'):
						return True
				return False
			# LADO IZQUIERDO ARBOL Y DERECHO NO ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
				not isinstance(expr.right, ArbolBin)):
				if (expr.left.tipo == 'ARITMETICA'):
					# SI EL DERECHO ES NUMERO
					if (isinstance(expr.right, Numero)):
						comparationStatus = self.checkExpressionOk(expr.left)
						return comparationStatus
					# SI EL DERECHO ES VARIABLE
					if (isinstance(expr.right, Ident)):
						if (self.table.getSymbolType(expr.right) == 'int'):
							comparationStatus = self.checkExpressionOk(expr.left)
							return comparationStatus
				return False
			# LADO DERECHO ARBOL Y IZQUIERDO NO ARBOLBIN
			elif(isinstance(expr.right, ArbolBin) and 
				not isinstance(expr.left, ArbolBin)):
				if (expr.right.tipo == 'ARITMETICA'):
					# SI EL DERECHO ES NUMERO
					if (isinstance(expr.left, Numero)):
						comparationStatus = self.checkExpressionOk(expr.right)
						return comparationStatus
					# SI EL DERECHO ES VARIABLE
					if (isinstance(expr.left, Ident)):
						if (self.table.getSymbolType(expr.left) == 'int'):
							comparationStatus = self.checkExpressionOk(expr.right)
							return comparationStatus
				return False
			# AMBOS SON ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
			isinstance(expr.right, ArbolBin)):
				if(expr.left.tipo == expr.right.tipo):
					comparationStatus1 = self.checkExpressionOk(expr.left)
					comparationStatus2 = self.checkExpressionOk(expr.right)
					return comparationStatus1 == comparationStatus2
				return False

		# SI ARBOLBIN ES DE TIPO BOOLEANO
		elif (expr.tipo == 'BOOLEANA'):
			if (expr.tipo == 'BOOLEANA'):
			# LADO IZQUIERDO Y LADO DERECHO NO SON ARBOLBIN
			if (not isinstance(expr.left, ArbolBin) and 
				not isinstance(expr.right, ArbolBin)):
				# SI AMBOS SON NUMEROS
				if(isinstance(expr.left, Bool) and
					isinstance(expr.right, Bool)):
					return True
				# SI UNO ES NUMERO Y EL OTRO ES VARIABLE
				elif(isinstance(expr.left, Bool) and
					isinstance(expr.right, Ident)):
					if (self.table.getSymbolType(expr.right) == 'bool'):
						return True
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Bool)):
					if (self.table.getSymbolType(expr.left) == 'bool'):
						return True
				# SI AMBOS SON VARIABLES
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Ident)):
					if (self.table.getSymbolType(expr.right) == 'bool' and\
						self.table.getSymbolType(expr.left) == 'bool'):
						return True
				return False
			# LADO IZQUIERDO ARBOL Y DERECHO NO ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
				not isinstance(expr.right, ArbolBin)):
				if (expr.left.tipo == 'BOOLEANA'):
					# SI EL DERECHO ES NUMERO
					if (isinstance(expr.right, Bool)):
						comparationStatus = self.checkExpressionOk(expr.left)
						return comparationStatus
					# SI EL DERECHO ES VARIABLE
					if (isinstance(expr.right, Ident)):
						if (self.table.getSymbolType(expr.right) == 'bool'):
							comparationStatus = self.checkExpressionOk(expr.left)
							return comparationStatus
				return False
			# LADO DERECHO ARBOL Y IZQUIERDO NO ARBOLBIN
			elif(isinstance(expr.right, ArbolBin) and 
				not isinstance(expr.left, ArbolBin)):
				if (expr.right.tipo == 'BOOLEANA'):
					# SI EL DERECHO ES NUMERO
					if (isinstance(expr.left, Bool)):
						comparationStatus = self.checkExpressionOk(expr.right)
						return comparationStatus
					# SI EL DERECHO ES VARIABLE
					if (isinstance(expr.left, Ident)):
						if (self.table.getSymbolType(expr.left) == 'bool'):
							comparationStatus = self.checkExpressionOk(expr.right)
							return comparationStatus
				return False
			# AMBOS SON ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
			isinstance(expr.right, ArbolBin)):
				if(expr.left.tipo == expr.right.tipo):
					comparationStatus1 = self.checkExpressionOk(expr.left)
					comparationStatus2 = self.checkExpressionOk(expr.right)
					return comparationStatus1 == comparationStatus2
				return False

		# SI ARBOLBIN ES RELACIONAL
		elif (expr.tipo == 'RELACIONAL'):
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
					if (self.table.getSymbolType(expr.right) == 'int'):
						return True
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Numero)):
					if (self.table.getSymbolType(expr.left) == 'int'):
						return True
				elif(isinstance(expr.left, Bool) and
					isinstance(expr.right, Ident)):
					if (self.table.getSymbolType(expr.right) == 'bool'):
						return True
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Bool)):
					if (self.table.getSymbolType(expr.left) == 'int'):
						return True
				# SI AMBOS SON VARIABLES
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Ident)):
					if ((self.table.getSymbolType(expr.right) == 'int' and\
						self.table.getSymbolType(expr.left) == 'int') or\
					(self.table.getSymbolType(expr.right) == 'bool' and\
						self.table.getSymbolType(expr.left) == 'bool')):
						return True
				return False
			# LADO IZQUIERDO ARBOL Y DERECHO NO ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
				not isinstance(expr.right, ArbolBin)):
				if (expr.left.tipo == 'ARITMETICA'):
					# SI EL DERECHO ES NUMERO
					if (isinstance(expr.right, Numero)):
						comparationStatus = self.checkExpressionOk(expr.left)
						return comparationStatus
					# SI EL DERECHO ES VARIABLE
					if (isinstance(expr.right, Ident)):
						if (self.table.getSymbolType(expr.right) == 'int'):
							comparationStatus = self.checkExpressionOk(expr.left)
							return comparationStatus
				if (expr.left.tipo == 'BOOLEANA'):
					# SI EL DERECHO ES BOOL
					if (isinstance(expr.right, Bool)):
						comparationStatus = self.checkExpressionOk(expr.left)
						return comparationStatus
					# SI EL DERECHO ES VARIABLE
					if (isinstance(expr.right, Ident)):
						if (self.table.getSymbolType(expr.right) == 'bool'):
							comparationStatus = self.checkExpressionOk(expr.left)
							return comparationStatus
				return False
			# LADO DERECHO ARBOL Y IZQUIERDO NO ARBOLBIN
			elif(isinstance(expr.right, ArbolBin) and 
				not isinstance(expr.left, ArbolBin)):
				if (expr.right.tipo == 'ARITMETICA'):
					# SI EL IZQUIERDO ES NUMERO
					if (isinstance(expr.left, Numero)):
						comparationStatus = self.checkExpressionOk(expr.right)
						return comparationStatus
					# SI EL IZQUIERDO ES VARIABLE
					if (isinstance(expr.left, Ident)):
						if (self.table.getSymbolType(expr.left) == 'int'):
							comparationStatus = self.checkExpressionOk(expr.right)
							return comparationStatus
				if (expr.right.tipo == 'BOOLEANA'):
					# SI EL IZQUIERDO ES BOOL
					if (isinstance(expr.left, Bool)):
						comparationStatus = self.checkExpressionOk(expr.right)
						return comparationStatus
					# SI EL IZQUIERDO ES VARIABLE
					if (isinstance(expr.left, Ident)):
						if (self.table.getSymbolType(expr.left) == 'bool'):
							comparationStatus = self.checkExpressionOk(expr.right)
							return comparationStatus
				return False
			# AMBOS SON ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
			isinstance(expr.right, ArbolBin)):
				if(expr.left.tipo == expr.right.tipo):
					comparationStatus1 = self.checkExpressionOk(expr.left)
					comparationStatus2 = self.checkExpressionOk(expr.right)
					return comparationStatus1 == comparationStatus2
				return False

		if (isinstance(expr, ArbolUn)):
			# SI ES EL NEGATIVO DE UNA EXPRESION
			if (expr.opsymbol == '-'):
				if (isinstance(expr.operando, ArbolBin) or
					isinstance(expr.operando, ArbolUn)):
					# DEBE SER ARITMETICA
					if(expr.operando.tipo == 'ARITMETICA'):
						comparationStatus = self.checkExpressionOk(expr)
						return comparationStatus
				return False
			# SI ES EL NEGADO DE UNA EXPRESION
			elif (expr.opsymbol == '~'):
				if (isinstance(expr.operando, ArbolBin)):
					# SI ES ARBOLBIN DEBE SER BOOLEANA O RELACIONAL
					if(expr.operando.tipo == 'BOOLEANA' or
						expr.operando.tipo == 'RELACIONAL'):
						comparationStatus = self.checkExpressionOk(expr)
						return comparationStatus
				elif (isinstance(expr.operando, ArbolUn)):
					# SI ES ARBOLUN DEBE SER BOOLEANA
					if (expr.operando.tipo == 'BOOLEANA'):
						comparationStatus = self.checkExpressionOk(expr)
				return False

	def checkComp_list(self, Comp_list, checklist = None):
		comp1 = Comp_list.children[0]
		condition1 = comp1.children[0]
		checklist = [] 
		if (isinstance(condition1.children[0], ArbolBin) or
			isinstance(condition1.children[0], ArbolUn)):
			expr = condition1.children[0]
			checklist.append(self.checkExpressionOk(expr)

		if (len(Comp_list.children) > 1):
			self.checkComp_list(Comp_list.children[1], checklist)

		return checklist

	"""Aqui se llenara la tabla"""
	def fillTable(self):
		# Si es instrucciones..
		if (isinstance(self.tree, ArbolInstr)):
			# Vamos a buscar que sea declaraciones
			for child in self.tree.children:
				if (child.token == 'Declaraciones'):
					Type = child.children[0]
					idlist = child.children[1]
					for ID in self.getID_list(idlist):
						self.table.addSymbol(ID, Type)
					#Si tiene comportamiento especificado
					if child.children[2]:
						compStatus = self.checkComp_list(child.children[2])
						for stat in compStatus:
							if (stat == False):
								print("ERROR, UNA EXPRESION FUE INVALIDA")

				

