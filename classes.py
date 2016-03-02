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
		if (self.symbolExists(symbol)):
			print("ERROR, VARIABLE YA DECLARADA")
			sys.exit()
		else:
			self.createTuple(symbol, tipo)

	"""Retorna el objeto que contiene la informacion de una variable 
	declarada"""
	def getSymbolData(self, symbol):
		if symbolExists(symbol):
			return self.tabla[symbol]
		elif (not symbolExists(symbol) and self.padre):
			self.padre.getSymbolData(symbol)
		else:
			print("VARIABLE NO DECLARADA, ERROR")
			sys.exit()

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
	def __init__(self, tree):
		self.tree = tree

	"""Hay que probarla pero si sirve es super util. Recibe un nodo
	del tipo Dec_List y almacena en una lista todos los identificadores
	declarados"""
	def getID_list(self, ID_list, idlist = None):
		if (not idlist):
			idlist = []

		if (len(ID_list.children) < 2):
			idlist.append(ID_list.children[0])
		else:
			idlist.append(ID_list.children[0])
			idChildList = ID_list.children[1]
			self.getID_list(idChildList, idlist)

		return idlist

	def checkExpressionOk(self, table, expr):
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
						print("ERROR, tipos incompatibles para " + expr.left +\
						" y " + expr.right)
						sys.exit()
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Numero)):
					if (table.getSymbolType(expr.left) == 'int'):
						return True
					else:
						print("ERROR, tipos incompatibles para " + expr.left +\
						" y " + expr.right)
						sys.exit()
				# SI AMBOS SON VARIABLES
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Ident)):
					if (table.getSymbolType(expr.right) == 'int' and\
						table.getSymbolType(expr.left) == 'int'):
						return True
					else:
						print("ERROR, tipos incompatibles para " + expr.left +\
						" y " + expr.right)
						sys.exit()
				else:
					print("ERROR, tipos incompatibles para " + expr.left +\
					 " y " + expr.right)
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
							print("ERROR, tipos incompatibles para " + expr.left +\
							" y " + expr.right)
							sys.exit()
					else:
						print("ERROR, tipos incompatibles para " + expr.left.tipo + " y " +\
						expr.right)
						sys.exit()	
				else:
					print("ERROR, tipos incompatibles para " + expr.left.tipo + " y " +\
					expr.right)
					sys.exit()
			# LADO DERECHO ARBOL Y IZQUIERDO NO ARBOLBIN
			elif(isinstance(expr.right, ArbolBin) and 
				not isinstance(expr.left, ArbolBin)):
				if (expr.right.tipo == 'ARITMETICA'):
					# SI EL DERECHO ES NUMERO
					if (isinstance(expr.left, Numero)):
						return True
					# SI EL DERECHO ES VARIABLE
					elif (isinstance(expr.left, Ident)):
						if (table.getSymbolType(expr.left) == 'int'):
							return True
						else:
							print("ERROR, tipos incompatibles para " + expr.left +\
							" y " + expr.right)
							sys.exit()
					else:
						print("ERROR, tipos incompatibles para " + expr.left.tipo + " y " +\
						expr.right)
						sys.exit()
				else:
					print("ERROR, tipos incompatibles para " + expr.left + " y " +\
					expr.right.tipo)
					sys.exit()
			# AMBOS SON ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
			isinstance(expr.right, ArbolBin)):
				if(expr.left.tipo == expr.right.tipo):
					self.checkExpressionOk(expr.left)
					self.checkExpressionOk(expr.right)
					return True
				else:
					print("ERROR, tipos incompatibles para " + expr.left. + " y " +\
					expr.right.tipo)
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
						print("ERROR, tipos incompatibles para " + expr.left +\
						" y " + expr.right)
						sys.exit()
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Bool)):
					if (table.getSymbolType(expr.left) == 'bool'):
						return True
					else:
						print("ERROR, tipos incompatibles para " + expr.left +\
						" y " + expr.right)
						sys.exit()
				# SI AMBOS SON VARIABLES
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Ident)):
					if (table.getSymbolType(expr.right) == 'bool' and\
						table.getSymbolType(expr.left) == 'bool'):
						return True
					else:
						print("ERROR, tipos incompatibles para " + expr.left +\
						" y " + expr.right)
						sys.exit()
				else:
					print("ERROR, tipos incompatibles para " + expr.left + " y " +\
					expr.right)
					sys.exit()
			# LADO IZQUIERDO ARBOL Y DERECHO NO ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
				not isinstance(expr.right, ArbolBin)):
				if (expr.left.tipo == 'BOOLEANA'):
					# SI EL DERECHO ES BOOL
					if (isinstance(expr.right, Bool)):
						return True
					else:
						print("ERROR, tipos incompatibles para " + expr.left +\
						" y " + expr.right)
						sys.exit()
					# SI EL DERECHO ES VARIABLE
					if (isinstance(expr.right, Ident)):
						if (table.getSymbolType(expr.right) == 'bool'):
							return True
						else:
							print("ERROR, tipos incompatibles para " + expr.left +\
							" y " + expr.right)
							sys.exit()
				print("ERROR, tipos incompatibles para " + expr.left.tipo + " y " +\
				expr.right)
				sys.exit()
			# LADO DERECHO ARBOL Y IZQUIERDO NO ARBOLBIN
			elif(isinstance(expr.right, ArbolBin) and 
				not isinstance(expr.left, ArbolBin)):
				if (expr.right.tipo == 'BOOLEANA'):
					# SI EL DERECHO ES BOOL
					if (isinstance(expr.left, Bool)):
						return True
					else:
						print("ERROR, tipos incompatibles para " + expr.left +\
						" y " + expr.right)
						sys.exit()
					# SI EL DERECHO ES VARIABLE
					if (isinstance(expr.left, Ident)):
						if (table.getSymbolType(expr.left) == 'bool'):
							return True
						else:
							print("ERROR, tipos incompatibles para " + expr.left +\
							" y " + expr.right)
							sys.exit()
				print("ERROR, tipos incompatibles para " + expr.left + " y " +\
				expr.right.tipo)
				sys.exit()
			# AMBOS SON ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
			isinstance(expr.right, ArbolBin)):
				if(expr.left.tipo == expr.right.tipo):
					self.checkExpressionOk(expr.left)
					self.checkExpressionOk(expr.right)
					return True
				print("ERROR, tipos incompatibles para " + expr.left.tipo + " y " +\
				expr.right.tipo)
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
						print("ERROR, tipos incompatibles para " + expr.left +\
											 " y " + expr.right)
											sys.exit()
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Numero)):
					if (table.getSymbolType(expr.left) == 'int'):
						return True
					else:
						print("ERROR, tipos incompatibles para " + expr.left +\
											 " y " + expr.right)
											sys.exit()
				elif(isinstance(expr.left, Bool) and
					isinstance(expr.right, Ident)):
					if (table.getSymbolType(expr.right) == 'bool'):
						return True
					else:
						print("ERROR, tipos incompatibles para " + expr.left +\
											 " y " + expr.right)
											sys.exit()
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Bool)):
					if (table.getSymbolType(expr.left) == 'int'):
						return True
					else:
						print("ERROR, tipos incompatibles para " + expr.left +\
											 " y " + expr.right)
											sys.exit()
				# SI AMBOS SON VARIABLES
				elif(isinstance(expr.left, Ident) and
					isinstance(expr.right, Ident)):
					if ((table.getSymbolType(expr.right) == 'int' and\
						table.getSymbolType(expr.left) == 'int') or\
					(table.getSymbolType(expr.right) == 'bool' and\
						table.getSymbolType(expr.left) == 'bool')):
						return True
				print("ERROR, tipos incompatibles para " + expr.left + " y " +\
				expr.right)
				sys.exit()
			# LADO IZQUIERDO ARBOL Y DERECHO NO ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
				not isinstance(expr.right, ArbolBin)):
				if (expr.left.tipo == 'ARITMETICA'):
					# SI EL DERECHO ES NUMERO
					if (isinstance(expr.right, Numero)):
						return True
					else:
						print("ERROR, tipos incompatibles para " + expr.left +\
											 " y " + expr.right)
											sys.exit()
					# SI EL DERECHO ES VARIABLE
					if (isinstance(expr.right, Ident)):
						if (table.getSymbolType(expr.right) == 'int'):
							return True
						else:
							print("ERROR, tipos incompatibles para " + expr.left +\
												 " y " + expr.right)
												sys.exit()
				if (expr.left.tipo == 'BOOLEANA'):
					# SI EL DERECHO ES BOOL
					if (isinstance(expr.right, Bool)):
						return True
					else:
						print("ERROR, tipos incompatibles para " + expr.left +\
											 " y " + expr.right)
											sys.exit()
					# SI EL DERECHO ES VARIABLE
					if (isinstance(expr.right, Ident)):
						if (table.getSymbolType(expr.right) == 'bool'):
							return True
						else:
							print("ERROR, tipos incompatibles para " + expr.left +\
												 " y " + expr.right)
												sys.exit()
				print("ERROR, tipos incompatibles para " + expr.left.tipo + " y " +\
				expr.right)
				sys.exit()
			# LADO DERECHO ARBOL Y IZQUIERDO NO ARBOLBIN
			elif(isinstance(expr.right, ArbolBin) and 
				not isinstance(expr.left, ArbolBin)):
				if (expr.right.tipo == 'ARITMETICA'):
					# SI EL IZQUIERDO ES NUMERO
					if (isinstance(expr.left, Numero)):
						return True
					else:
						print("ERROR, tipos incompatibles para " + expr.left +\
											 " y " + expr.right)
											sys.exit()
					# SI EL IZQUIERDO ES VARIABLE
					if (isinstance(expr.left, Ident)):
						if (table.getSymbolType(expr.left) == 'int'):
							return True
						else:
							print("ERROR, tipos incompatibles para " + expr.left +\
												 " y " + expr.right)
												sys.exit()
				if (expr.right.tipo == 'BOOLEANA'):
					# SI EL IZQUIERDO ES BOOL
					if (isinstance(expr.left, Bool)):
						return True
					else:
						print("ERROR, tipos incompatibles para " + expr.left +\
											 " y " + expr.right)
											sys.exit()
					# SI EL IZQUIERDO ES VARIABLE
					if (isinstance(expr.left, Ident)):
						if (table.getSymbolType(expr.left) == 'bool'):
							return True
						else:
							print("ERROR, tipos incompatibles para " + expr.left +\
												 " y " + expr.right)
												sys.exit()
				print("ERROR, tipos incompatibles para " + expr.left + " y " +\
				expr.right.tipo)
				sys.exit()
			# AMBOS SON ARBOLBIN
			elif(isinstance(expr.left, ArbolBin) and 
			isinstance(expr.right, ArbolBin)):
				if(expr.left.tipo == expr.right.tipo):
					self.checkExpressionOk(expr.left)
					self.checkExpressionOk(expr.right)
					return True
				print("ERROR, tipos incompatibles para " + expr.left.tipo + " y " +\
				expr.right.tipo)
				sys.exit()

		if (isinstance(expr, ArbolUn)):
			# SI ES EL NEGATIVO DE UNA EXPRESION
			if (expr.opsymbol == '-'):
				if (isinstance(expr.operando, ArbolBin) or
					isinstance(expr.operando, ArbolUn)):
					# DEBE SER ARITMETICA
					if(expr.operando.tipo == 'ARITMETICA'):
						return True
				print("ERROR, tipo incompatible para operacion '-' y " +\
					expr.operando.tipo)
				sys.exit()
			# SI ES EL NEGADO DE UNA EXPRESION
			elif (expr.opsymbol == '~'):
				if (isinstance(expr.operando, ArbolBin)):
					# SI ES ARBOLBIN DEBE SER BOOLEANA O RELACIONAL
					if(expr.operando.tipo == 'BOOLEANA' or
						expr.operando.tipo == 'RELACIONAL'):
						return True
				elif (isinstance(expr.operando, ArbolUn)):
					# SI ES ARBOLUN DEBE SER BOOLEANA
					if (expr.operando.tipo == 'BOOLEANA'):
						self.checkExpressionOk(expr)
						return True
				print("ERROR, tipos incompatibles para '~' y " +\
				expr.operando.tipo)
				sys.exit()

	def checkComp_list(self, comp_list):
		comp = comp_list.children[0]
		condition = comp.children[0]
		if (isinstance(condition.children[0], ArbolBin) or
			isinstance(condition.children[0], ArbolUn)):
			expr = condition.children[0]
			self.checkExpressionOk(expr)

		if (len(comp_list.children) > 1):
			self.checkComp_list(comp_list.children[1])

	def checkInstC_list(self, table, inst_list):
		instc = inst_list.children[0]
		if (instc.tipoInstruccion == 'ACTIVACION' or
			instc.tipoInstruccion == 'DESACTIVACION' or
			instc.tipoInstruccion == 'AVANCE'):
			id_list = self.getID_list(instc.id_list)

			for ID in id_list:
				if (not table.symbolExists(ID)):
					print("ERROR, VARIABLE NO DECLARADA")
					sys.exit()
				elif (ID == 'me'):
					print("ERROR, USO DE LA PALABRA RESERVADA ME FUERA DE UN COMPORTAMINENTO")
					sys.exit()

			if (len(instc.children) > 1):
				inst_list1 = inst_list.children[1]
				self.checkInstC_list(inst_list1)

		elif (instc.tipoInstruccion == 'CONDICIONAL'):
			condition = instc.condicion
			self.checkExpressionOk(condition)

			inst1 = instc.instruccion1
			self.checkInstC_list(inst1)

			if (instc.instruccion2):
				inst2 = instc.instruccion2
				self.checkInstC_list(inst2)

		elif (instc.tipoInstruccion == 'ITERACION_INDEF'):
			condition = inst.condicion
			self.checkExpressionOk(condition)

			instr = instc.instruccion
			self.checkInstC_list(instr)

		elif (instc.children[0].tipoInstruccion == "ALCANCE"):
			childTable = symbolTable(table)
			self.fillTable(childTable)

	"""Aqui se llenara la tabla"""
	def fillTable(self, table):
		# Si es instrucciones..
		if (isinstance(self.tree, ArbolInstr)):
			# Vamos a buscar que sea declaraciones
			for child in self.tree.children:
				if (child.token == 'Declaraciones'):
					Type = child.children[0]
					idlist = child.children[1]
					for ID in self.getID_list(idlist):
						table.addSymbol(ID, Type)
					#Si tiene comportamiento especificado
					if child.children[2]:
						self.checkComp_list(child.children[2])
				elif (child.token == 'InstC_lista'):
					self.checkInstC_list(child)