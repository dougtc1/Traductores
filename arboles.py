
#!/usr/bin/python3
# Universidad Simon Bolivar 
#
# Traductores e interpretadores - CI3715
#
# Benjamin Amos. Carnet: 12-10240
# Douglas Torres. Carnet: 11-11027
#
# Proyecto 2
# Archivo que contiene las estructuras de datos de arboles utilizadas.
import textwrap
from classes import *
import sys

cantidadTabs = 0
auxCantidadTabs = 0

class Expr: pass
class Instr: pass

class ArbolBin(Expr):
	def __init__(self, tipo, left, op, right, opsymbol):
		self.tipo     = tipo
		self.left     = left
		self.op       = op
		self.right    = right
		self.opsymbol = opsymbol

	def get_valor_left(self):
		
		if (isinstance(self.left, ArbolBin)):
			auxiliar = self.left
			auxiliar.get_valor_left()
			auxiliar.get_valor_right()
		elif (isinstance(self.left, ArbolUn)):
			return self.left.get_valor()
		elif (isinstance(self.left, Ident) or isinstance(self.left, Numero) or isinstance(self.left, Bool)):
			return self.left.get_valor()
			
	def get_valor_right(self):
		
		if (isinstance(self.right, ArbolBin)):
			auxiliar = self.right
			auxiliar.get_valor_left()
			auxiliar.get_valor_right()
		elif (isinstance(self.right, ArbolUn)):
			return self.right.get_valor()
		elif (isinstance(self.right, Ident) or isinstance(self.right, Numero) or isinstance(self.right, Bool)):
			return self.right.get_valor()

	def evaluar(self, izquierda, operador, derecha):
		
		if (operador == '+'):
			resultado = izquierda + derecha

		elif (operador == '*'):
			resultado = izquierda * derecha

		elif (operador == '-'):
			resultado = izquierda - derecha

		elif (operador == '%'):
			if (derecha == 0):
				print("Error: No se puede dividir por cero (0).")
				sys.exit()
			else:
				resultado = izquierda % derecha

		elif (operador == '/'):
			if (derecha == 0):
				print("Error: No se puede dividir por cero (0).")
				sys.exit()
			else:	
				resultado = izquierda / derecha

		elif (operador == '/\\'):
			resultado = izquierda and derecha

		elif (operador == '\\/'):
			resultado = izquierda or derecha

		else:
			print("Error: Operacion " + str(operador) + " no definida.")
			sys.exit()

		return resultado


class ArbolUn(Expr):
	def __init__(self,tipo, operador,operando, opsymbol):
		self.tipo     = tipo
		self.operador = operador
		self.operando = operando
		self.opsymbol = opsymbol

	def imprimir(self):
		return (self.operador + self.operando)

	def get_valor(self):
		return self.operando.get_valor()

class Numero(Expr):
	def __init__(self,value):
		self.tipo = "Numero"
		self.value = value

	def get_valor(self):
		return self.value

class Bool(Expr):
	def __init__(self,value):
		self.tipo = "Bool"
		self.value = value

	def get_valor(self):
		return self.value

class Ident(Expr):
	def __init__(self,value):
		self.tipo = "Identificador"
		self.value = value

	def get_valor(self):
		return self.value

class ArbolInstr(Instr):
	def __init__(self, token=None, children=None, tipoInstruccion=None):
		self.token = token
		if children:
			self.children = children
		else:
			self.children = [ ]
		self.tipoInstruccion = tipoInstruccion

	def add_token(self, token):
		self.token = token

	def add_children(self, children):
		self.children = children

	def add_tipoInstruccion(self, tipoInstruccion):
		self.tipoInstruccion = tipoInstruccion

	def imprimir(self):
		pass

	def printPreorden(self):
		global cantidadTabs
		global auxCantidadTabs
		global guardaTabs

		if (self.children):
			if (len(self.children) > 1 and str(self.tipoInstruccion) == 'SECUENCIACION' ):

				print (textwrap.fill(self.tipoInstruccion, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
				cantidadTabs = auxCantidadTabs
				cantidadTabs += 1
				auxCantidadTabs = cantidadTabs

			for child in self.children:

				if (isinstance(child, Activate)):
					print (textwrap.fill(child.tipoInstruccion, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
					cantidadTabs    = auxCantidadTabs
					cantidadTabs    += 1
					lista = child.imprimir()
					for i in lista:
						print (textwrap.fill(i, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
					cantidadTabs -= 1

				elif (isinstance(child, Deactivate)):
					print (textwrap.fill(child.tipoInstruccion, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
					cantidadTabs    = auxCantidadTabs
					cantidadTabs    += 1
					lista = child.imprimir()
					for i in lista:
						print (textwrap.fill(i, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
					cantidadTabs -= 1


				elif (isinstance(child, Advance)):
					print (textwrap.fill(child.tipoInstruccion, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
					cantidadTabs    = auxCantidadTabs
					cantidadTabs    += 1
					lista = child.imprimir()
					for i in lista:
						print (textwrap.fill(i, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
					cantidadTabs -= 1

				elif(isinstance(child, CondicionalIf)):
					child.imprimir()
				elif(isinstance(child, IteracionIndef)):
					child.imprimir()
				elif(isinstance(child, Ident)):
					return child.get_valor()
				elif(isinstance(child, Bool)):
					return child.get_valor()
				elif(isinstance(child, Numero)):
					return child.get_valor()
				elif(isinstance(child, ArbolUn)):
					return child.imprimir()
				else:
					if (isinstance(child, ArbolInstr)):
						if (child.tipoInstruccion == "ALCANCE"):

							print (textwrap.fill(child.tipoInstruccion, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
							cantidadTabs    += 1
							auxCantidadTabs = cantidadTabs
						child.printPreorden()

	def ejecutar(self, tabla):

		print("ESTOY EMPEZANDO EJECUTAR")

		if (self.token == 'Start'):
			
			print("INICIAL")
			print(self.children)
			self.children[1].ejecutar(tabla)

		elif(self.token == 'InstC_lista'):
			
			print("INSTC_LISTA")
			print(self.children[0].token)
			for i in self.children:
				i.ejecutar(tabla)

		elif(self.token == 'InstrC'):
			print("INSTRC")
			print(self.children)

			if (isinstance(self.children[0], CondicionalIf)):
				print("CONDICIONAL IF")
				print(self.children[0])

			elif (isinstance(self.children[0], IteracionIndef)):
				print("ITERACION INDEF")
				print(self.children[0])


		elif(isinstance(self, Activate)):
			
			print("ACTIVATE")
			print(self.id_list)
			self.ejecutar(tabla)


		"""
		print("Tabla de simbolos")
		print("\n")
		tabla.printTables()
		tablaComportamientos = tabla.behav
		print("\n")
		print("Tablas de Comportamientos asociada a la tabla de simbolos")
		print("\n")
		#print(tablaComportamientos)
		for i in tablaComportamientos:
			#print("ESTA ES I: ",i)
			#print("i.behavs: ", i.behavs)
			i.printTable()

		print("\n")
		"""
class CondicionalIf(ArbolInstr):
	def __init__(self, token, children, condicion, instruccion1, instruccion2=None):
		ArbolInstr.__init__(self, token, children, "CONDICIONAL")
		self.condicion    = condicion
		self.instruccion1 = instruccion1
		self.instruccion2 = instruccion2

	def imprimir(self):
		global cantidadTabs
		global auxCantidadTabs
		guardaTabs = 0

		print (textwrap.fill(self.tipoInstruccion, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
		cantidadTabs = auxCantidadTabs
		cantidadTabs += 1
		auxCantidadTabs = cantidadTabs

		if (isinstance(self.condicion, ArbolBin)):

			while ((auxCantidadTabs - cantidadTabs) > 1):
				auxCantidadTabs -= 1

			cantidadTabs = auxCantidadTabs

			aux = "- guardia: " + str(self.condicion.tipo)
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs += 1
			
			aux = "- operacion: " + str(self.condicion.op)
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			
			aux = "- operador izquierdo: " + str(self.condicion.get_valor_left())
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			
			aux = "- operador derecho: " + str(self.condicion.get_valor_right())
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs))
			cantidadTabs -= 1

		elif (isinstance(self.condicion, Bool)):

			while ((auxCantidadTabs - cantidadTabs) > 1):
				auxCantidadTabs -= 1

			cantidadTabs = auxCantidadTabs

			aux = "- guardia: " + str(self.condicion.tipo)
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs += 1
			
			aux = "- var: " + str(self.condicion.get_valor())
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs -= 1

		elif (isinstance(self.condicion, ArbolUn)):

			while ((auxCantidadTabs - cantidadTabs) > 1):
				auxCantidadTabs -= 1

			cantidadTabs = auxCantidadTabs

			aux = "- guardia: " + str(self.condicion.tipo)
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs += 1

			aux = "- operacion: " + str(self.condicion.operador)
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			
			aux = "- operando: " + str(self.condicion.get_valor())
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs -= 1 

		elif (isinstance(self.condicion, Ident)):

			while ((auxCantidadTabs - cantidadTabs) > 1):
				auxCantidadTabs -= 1

			cantidadTabs = auxCantidadTabs

			aux = "- guardia: " + str(self.condicion.tipo)
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs += 1

			aux = "- var: " + str(self.condicion.get_valor())
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs -= 1

		elif (isinstance(self.condicion, Numero)):

			while ((auxCantidadTabs - cantidadTabs) > 1):
				auxCantidadTabs -= 1

			cantidadTabs = auxCantidadTabs

			aux = "- guardia: " + str(self.condicion.tipo)
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs += 1

			aux = "- expresion: " + str(self.condicion.get_valor())
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs -= 1

		auxCantidadTabs = cantidadTabs

		while ((auxCantidadTabs - cantidadTabs) > 1):
				auxCantidadTabs -= 1

		cantidadTabs = auxCantidadTabs

		print(textwrap.fill("- exito: ", initial_indent='\t'*cantidadTabs),end=" ")
		auxCantidadTabs = cantidadTabs
		cantidadTabs    = 0
		guardaTabs = auxCantidadTabs

		self.instruccion1.printPreorden()

		auxCantidadTabs = guardaTabs

		if (self.instruccion2):

			cantidadTabs = auxCantidadTabs

			print(textwrap.fill("- fracaso: ", initial_indent='\t'*cantidadTabs),end=" ")
			auxCantidadTabs = cantidadTabs
			cantidadTabs    = 0
			self.instruccion2.printPreorden()

class IteracionIndef(ArbolInstr):
	def __init__(self, token, children, condicion, instruccion):
		ArbolInstr.__init__(self, token, children, "ITERACION_INDEF")
		self.condicion = condicion
		self.instruccion = instruccion

	def imprimir(self):

		global cantidadTabs
		global auxCantidadTabs
		global guardaTabs
		
		print (textwrap.fill(self.tipoInstruccion, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
		cantidadTabs = auxCantidadTabs
		cantidadTabs += 1

		if (isinstance(self.condicion, ArbolBin)):

			aux = "- guardia: " + str(self.condicion.tipo)
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs += 1

			aux = "- operacion: " + str(self.condicion.op)
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))

			aux = "- operador izquierdo: " + str(self.condicion.get_valor_left())
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))

			aux = "- operador derecho: " + str(self.condicion.get_valor_right())
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs))
			cantidadTabs -= 1

		elif (isinstance(self.condicion, Bool)):
			aux = "- guardia: " + str(self.condicion.tipo)
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs += 1

			aux = "- var: " + str(self.condicion.get_valor())
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs -= 1

		elif (isinstance(self.condicion, ArbolUn)):
			aux = "- guardia: " + str(self.condicion.tipo)
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs += 1

			aux = "- operacion: " + str(self.condicion.operador)
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			
			aux = "- operando: " + str(self.condicion.get_valor())
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs -= 1 

		elif (isinstance(self.condicion, Ident)):
			aux = "- guardia: " + str(self.condicion.tipo)
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs += 1

			aux = "- var: " + str(self.condicion.get_valor())
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs -= 1

		elif (isinstance(self.condicion, Numero)):
			aux = "- guardia: " + str(self.condicion.tipo)
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))

			aux = "- expr: " + str(self.condicion.get_valor())
			print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
			cantidadTabs -= 1

		print(textwrap.fill("- exito: ", initial_indent='\t'*cantidadTabs),end=" ")
		auxCantidadTabs = cantidadTabs
		cantidadTabs    = 0
		
		self.instruccion.printPreorden()

class Activate(ArbolInstr):
	def __init__(self, token, children, id_list):
		ArbolInstr.__init__(self, token, children, "ACTIVACION")
		self.id_list = id_list

	def imprimir(self):
		lista=[]
		for x in self.id_list:
			if (isinstance(x, ArbolInstr)):
				lista.append(x.printPreorden())
			else:
				lista.append("- var: " + str(x.value))
		return lista

	def ejecutar(self, tabla):

		print("\n")
		print("ESTOY EN EL EJECUTAR DE ACTIVATE")

		print("ESTOS SON LOS IDENTIFICADRES QUE VOY A ACTIVAR")
		print(self.id_list)

		for i in self.id_list:
			bot = tabla.getSymbolData(i.value)

			#print(bot.nombre)
			#print(bot.tipo)
			#print(bot.value)
			#print(bot.meType)
			#print(bot.meVal)
			#print(bot.posicion)
			#print(bot.estado)
			#print(bot.behaviors)
			
			if (bot.estado == "desactivado"):
				bot.estado = "activado"

				if (bot.behaviors):
					bot.behaviors.printTable()
				
					for i in bot.behaviors.behavs:
						print("i",i)

						if (i == "activation"):
							aux = bot.behaviors.getBehavData(i)
							print("aux",aux)
							aux.ejecutar(tabla)

			else:
				print("Error: el bot " + bot.nombre + " ya se encuentra activado.")
				sys.exit()
				i.activarBot("activado",tabla)


		print("\n")


class Deactivate(ArbolInstr):
	def __init__(self, token, children, id_list):
		ArbolInstr.__init__(self, token, children, "DESACTIVACION")
		self.id_list = id_list

	def imprimir(self):
		lista=[]
		for x in self.id_list:
			if (isinstance(x, ArbolInstr)):
				lista.append(x.printPreorden())
			else:
				lista.append("- var: " + str(x.value))
		return lista

	def ejecutar(self, tabla):

		print("\n")
		print("ESTOY EN EL EJECUTAR DE DEACTIVATE")

		print("ESTOS SON LOS IDENTIFICADRES QUE VOY A DESACTIVAR")
		print(self.id_list)

		for i in self.id_list:
			bot = tabla.getSymbolData(i.value)

			if (bot.estado == "activado"):
				bot.estado = "desactivado"

				if (bot.behaviors):
					bot.behaviors.printTable()
				
					for i in bot.behaviors.behavs:
						aux = bot.behaviors.getBehavData(i)
						print(aux)
						aux.ejecutar(tabla)

			else:
				print("Error: el bot " + bot.nombre + " ya se encuentra desactivado.")
				sys.exit()		



class Advance(ArbolInstr):
	def __init__(self, token, children, id_list):
		ArbolInstr.__init__(self, token, children, "AVANCE")
		self.id_list = id_list

	def imprimir(self):
		lista=[]
		for x in self.id_list:
			if (isinstance(x, ArbolInstr)):
				for i in x.children:
					if (isinstance(i, ArbolInstr)):
						lista.append("- var: " + str(i.printPreorden()))
					elif (isinstance(i, Ident) or isinstance(i, Bool) or\
					isinstance(i, Numero)):
						lista.append("- var: " + str(i.get_valor()))
					else:
						lista.append("- var: " + str(i))
			else:
				lista.append("- var: " + str(x.value))

		return lista

class Store(ArbolInstr):
	"""Clase arbol para accion de Robot Store"""
	def __init__(self, token, children, expr):
		ArbolInstr.__init__(self, token, children, "store")
		self.expr = expr

	def ejecutar(self, tabla, bot):
		print("\n")
		print("EN EJECUTAR DE STORE")
		print(self.expr)
		print("\n")

		if (isinstance(self.expr, ArbolBin)):

			izquierda = self.expr.get_valor_left()
			operador = self.expr.opsymbol
			derecha = self.expr.get_valor_right()

			if (not isinstance(izquierda, int)):
				aux_bot = tabla.getSymbolData(bot)
				aux = aux_bot.behaviors.getVarData(izquierda)
				izquierda = aux.value

			if (not isinstance(derecha, int)):
				aux_bot = tabla.getSymbolData(bot)
				aux = aux_bot.behaviors.getVarData(derecha)
				derecha = aux.value

			print("izquierda: ", izquierda)
			print("derecha: ", derecha)
			print("operador: ", operador)

			resultado = self.expr.evaluar(izquierda, operador, derecha)

			print ("ESTE ES VALOR DEL EVALUAR: ", resultado)


		elif (isinstance(self.expr, ArbolUn)):
			unario = self.expr.get_valor()
			aux_bot = tabla.getSymbolData(bot)

			if (self.expr.tipo == "ARITMETICA"):
				print("SOY INT UNARIO")
				aux_bot.value = unario
				aux_bot.meVal = unario
			elif (self.expr.tipo == "BOOLEANA"):
				print("SOY BOOL UNARIO")
				aux_bot.value = unario
				aux_bot.meVal = unario

			else:
				print("Error: Tipo de bot " + aux_bot.nombre +" incompatible.")
				sys.exit()

		elif (isinstance(self.expr, Numero)):
			num = self.expr.get_valor()
			aux_bot = tabla.getSymbolData(bot)

			if (aux_bot.tipo == "int"):
				print("SOY INT")
				aux_bot.value = num
				aux_bot.meVal = num

			else:
				print("Error: Tipo de bot " + aux_bot.nombre +" incompatible.")
				sys.exit()

		elif (isinstance(self.expr, Bool)):
			boolean = self.expr.get_valor()
			aux_bot = tabla.getSymbolData(bot)

			if (aux_bot.tipo == "bool"):
				print("SOY BOOL")
				aux_bot.value = boolean
				aux_bot.meVal = boolean

			else:
				print("Error: Tipo de bot " + aux_bot.nombre +" incompatible.")
				sys.exit()

		elif (isinstance(self.expr, Ident)):
			ident = self.expr.get_valor()
			# Verifico que el identificador este declarado y obtengo su instancia en la tabla 
			ident = tabla.getSymbolData(ident)
			aux_bot = tabla.getSymbolData(bot)

			if (aux_bot.tipo == ident.tipo):
				print("SOY IDENT")
				aux_bot.value = ident.value
				aux_bot.meVal = ident.meVal

			else:
				print("Error: Tipo de bot " + aux_bot.nombre +" incompatible.")
				sys.exit()

class Collect(ArbolInstr):
	"""Clase arbol para accion de Robot Collect"""
	def __init__(self, token, children, id_list = None):
		ArbolInstr.__init__(self, token, children, "collect")
		self.id_list = id_list

	def ejecutar(self, tabla, bot):
		print("EN EJECUTAR DE COLLECT")
		print(bot)
		print("id_list: ",self.id_list.get_valor())

		""" Falta implementar matriz, mientras el valor siempre va a ser 1 """
		valorMatriz = 1

		aux_bot = tabla.getSymbolData(bot)


		# En caso de que tenga as, se saca el nombre de dicho identificador y se busca para guardar su valor

		if (self.id_list):
			var = self.id_list.get_valor()
			print(aux_bot.behaviors.interna)

			aux_bot.behaviors.modificarVarInterna(var, valorMatriz)
			
		else:

			aux_bot.value = valorMatriz
			aux_bot.modifMeVal(valorMatriz)

class Drop(ArbolInstr):
	"""Clase arbol para accion de Robot Drop"""
	def __init__(self, token, children, expr):
		ArbolInstr.__init__(self, token, children, "drop")
		self.expr = expr

class Direccion(ArbolInstr):
	"""Clase arbol para accion de Robot Direccion"""
	def __init__(self, token, children, direccion, expr = None):
		ArbolInstr.__init__(self, token, children, "direccion")
		self.direccion = direccion
		self.expr = expr
		
class Read(ArbolInstr):
	"""Clase arbol para accion de Robot Read"""
	def __init__(self, token, children, id_list = None):
		ArbolInstr.__init__(self, token, children, "read")
		self.id_list = id_list

class Send(ArbolInstr):
	"""Clase arbol para accion de Robot Send"""
	def __init__(self, token, children):
		ArbolInstr.__init__(self, token, children, "send")
		
class Receive(ArbolInstr):
	"""Clase arbol para accion de Robot Receive"""
	def __init__(self, token, children):
		ArbolInstr.__init__(self, token, children, "receive")