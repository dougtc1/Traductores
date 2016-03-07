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
		self.value = str(value)

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

class Collect(ArbolInstr):
	"""Clase arbol para accion de Robot Collect"""
	def __init__(self, token, children, id_list = None):
		ArbolInstr.__init__(self, token, children, "collect")
		self.id_list = id_list

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
		