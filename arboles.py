
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
from classes import *
import textwrap
import sys

#global matrix

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

	def get_valor_left(self, tabla = None):
		
		if (isinstance(self.left, ArbolBin)):
			auxiliar = self.left
			auxizq = auxiliar.get_valor_left()
			auxder = auxiliar.get_valor_right()
			if tabla:
				resultado = auxiliar.evaluar(auxizq, auxiliar.op, auxder, tabla)
				return resultado
		elif (isinstance(self.left, ArbolUn)):
			return self.left.get_valor()
		elif (isinstance(self.left, Ident) or isinstance(self.left, Numero) or isinstance(self.left, Bool)):
			return self.left.get_valor()
		
		else:
			return self.left

	def get_valor_right(self, tabla = None):
		
		if (isinstance(self.right, ArbolBin)):
			auxiliar = self.right
			auxizq = auxiliar.get_valor_left()
			auxder = auxiliar.get_valor_right()
			if tabla:
				resultado = auxiliar.evaluar(auxizq, auxiliar.op, auxder, tabla)
				return resultado
		elif (isinstance(self.right, ArbolUn)):
			return self.right.get_valor()
		elif (isinstance(self.right, Ident) or isinstance(self.right, Numero) or isinstance(self.right, Bool)):
			return self.right.get_valor()

		else:
			return self.right

	def evaluar(self, izquierda, operador, derecha, tabla = None):

		if tabla:
			if (isinstance(izquierda, str)):
				#print("TENGO QUE TRANSFORMAR ESTO: ", izquierda)
				temporal = tabla.getSymbolData(izquierda)
				#print("temporal", temporal.value)
				izquierda = temporal.value

				#print("izquierda es ahora: ", izquierda)
			if (isinstance(derecha, str)):
				temporal = tabla.getSymbolData(derecha)
				derecha = temporal.value
		
		if (operador == '+'):
			resultado = izquierda + derecha
			resultado = int(resultado)

		elif (operador == '*'):
			resultado = izquierda * derecha
			resultado = int(resultado)

		elif (operador == '-'):
			resultado = izquierda - derecha
			resultado = int(resultado)

		elif (operador == '%'):
			if (derecha == 0):
				print("Error: No se puede dividir por cero (0).")
				sys.exit()
			else:
				resultado = izquierda % derecha
				resultado = int(resultado)

		elif (operador == '/'):
			if (derecha == 0):
				print("Error: No se puede dividir por cero (0).")
				sys.exit()
			else:	
				resultado = izquierda / derecha
				resultado = int(resultado)

		elif (operador == '/\\'):
			resultado = izquierda and derecha
			resultado = bool(resultado)

		elif (operador == '\\/'):
			resultado = izquierda or derecha
			resultado = bool(resultado)

		elif (operador == '>'):
			resultado = izquierda > derecha
			resultado = bool(resultado)

		elif (operador == '>='):
			resultado = izquierda >= derecha
			resultado = bool(resultado)
			
		elif (operador == '<'):
			resultado = izquierda < derecha
			resultado = bool(resultado)

		elif (operador == '<='):
			resultado = izquierda <= derecha
			resultado = bool(resultado)

		elif (operador == '/\='):
			resultado = izquierda != derecha
			resultado = bool(resultado)

		else:
			print("Error: Operacion " + str(operador) + " no definida.")
			sys.exit()

		return resultado

	def get_valor(self):
		print("LEFT: ",self.get_valor_right())
		print("RIGHT: ",self.get_valor_left())


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

	def evaluar(self):
		if (self.tipo == "ARITMETICA"):
			if (self.opsymbol == '-'):
				resultado = -1*self.operando.get_valor()
			else:
				print("DAFUQ?")
				sys.exit()
		elif(self.tipo == "BOOLEANA"):
			if (self.opsymbol == '~'):
				if (self.operando.get_valor() == 'True'):
					resultado = False
				elif (self.operando.get_valor() == 'False'):
					resultado = True
				else:
					print("BRODER LO ESTAS HACIENDO MAL", self.operando)
					sys.exit()
			else:
				print("DAFUQ?")
				sys.exit()

		print("RESULTADO de ARBOL UNARIO", resultado)
		return resultado

class Numero(Expr):
	def __init__(self,value):
		self.tipo = "Numero"
		self.value = int(value)

	def get_valor(self):
		return self.value

class Bool(Expr):
	def __init__(self,value):
		self.tipo = "Bool"
		self.value = bool(value)

	def get_valor(self):
		return self.value

class Ident(Expr):
	def __init__(self,value):
		self.tipo = "Identificador"
		self.value = value

	def get_valor(self):
		return self.value		

class NewLine(Expr):
	def __init__(self, value):
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

	def ejecutar(self, tabla, matrix):
		#print("ESTOY EMPEZANDO EJECUTAR")

		#print("ESTA ES LA MATRIZ: ", matrix)

		if (self.token == 'Start'):
			
			#print("INICIAL")
			#print(self.children)
			self.children[1].ejecutar(tabla, matrix)

		elif(self.token == 'InstC_lista'):
			
			#print("INSTC_LISTA")
			#print(self.children[0].token)
			#print("HIJOS",self.children)
			for i in self.children:
				i.ejecutar(tabla, matrix)

		elif(self.token == 'InstrC'):
			#print("INSTRC")
			#print(self.children)

			if (isinstance(self, Activate)):
				#print("ACTIVATE")
				self.ejecutar(tabla, matrix)

			elif (isinstance(self, Deactivate)):
				#print("DEACTIVATE")
				self.ejecutar(tabla, matrix)

			elif (isinstance(self, Advance)):
				#print("ADVANCE")
				self.ejecutar(tabla, matrix)

			elif (isinstance(self.children[0], CondicionalIf)):
				#print("CONDICIONAL IF")
				#print(self.children[0])
				self.children[0].ejecutar(tabla,matrix)

			elif (isinstance(self.children[0], IteracionIndef)):
				#print("ITERACION INDEF")
				#print(self.children[0])
				self.children[0].ejecutar(tabla, matrix)

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

	def unirID_lista(self):

		lista=[]
		seguir = True

		while seguir:
			auxiliar = self.children[0]

			if (isinstance(auxiliar,str)):
				auxiliar = Ident(auxiliar)
				lista.append(auxiliar)

			elif (isinstance(auxiliar, Ident)):
				lista.append(auxiliar)

			else:
				print("Error: ID_LIST invalido.", auxiliar)
				sys.exit()

			if (len(self.children) > 1):
				self = self.children[1]
				if (isinstance(self, Ident)):
					lista.append(self)
					break
			else:
				seguir = False
		
		return lista


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


	def ejecutar(self, tabla, matrix):
		#print("\n")
		#print("EN EL EVALUAR DEL IF")
		#print("\n")
		#print("condicion", self.condicion)
		#print("\n")
		#print("self.instruccion1", self.instruccion1)
		#print("\n")
		#print("self.instruccion2", self.instruccion2)
		#print("\n")

		if (isinstance(self.condicion,ArbolBin)):
			izquierda = self.condicion.get_valor_left()
			operador = self.condicion.opsymbol
			derecha = self.condicion.get_valor_right()
			resultado = self.condicion.evaluar(izquierda, operador, derecha, tabla)

		elif (isinstance(self.condicion, ArbolUn)):
			resultado = self.condicion.evaluar()

		elif (isinstance(self.condicion, Bool)):
			resultado = self.condicion.get_valor()

		elif(isinstance(self.condicion, Ident)):
			tipo_ident = tabla.getSymbolData(self.condicion.get_valor())
			if (tipo_ident.tipo == "bool" and tipo_ident.estado == "activado"):
				resultado = tipo_ident.value
			else:
				if (tipo_ident.estado != "activado"):
					print("Error: El bot " + tipo_ident.nombre + " no se encuenta activado.")
					sys.exit()
				else:
					print("Error: El tipo del bot " + tipo_ident.nombre + " no es booleano.")
					sys.exit()

		else:
			print("Error: condicion no definida en el lenguaje bot.")
			sys.exit()


		if (resultado):
			#print("este es el resultado de la condicion del if: ",resultado)
			#print("\n")
			#print("VOY A EJECUTAR LA INSTRUCCION 1 DEL IF")
			self.instruccion1.ejecutar(tabla, matrix)
		else:
			if (self.instruccion2):
				#print("este es el resultado de la condicion del if: ",resultado)
				#print("\n")
				#print("VOY A EJECUTAR LA INSTRUCCION 2 DEL IF")
				self.instruccion2.ejecutar(tabla, matrix)


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


	def ejecutar(self, tabla, matrix):
		iterar = True
		while iterar:
			
			#print("\n")
			#print("EN EL EVALUAR DEL WHILE")
			#print("\n")
			#print("condicion", self.condicion)
			#print("\n")
			#print("self.instruccion", self.instruccion)
			#print("\n")
	
	
			if (isinstance(self.condicion,ArbolBin)):
				izquierda = self.condicion.get_valor_left()
				operador = self.condicion.opsymbol
				derecha = self.condicion.get_valor_right()
	
				if (not isinstance(izquierda, int)):
	
					if (izquierda == "me"):
						print("Error: Uso de palabra reservada me no definido en instrucciones de controlador.")
						sys.exit()
					else:
						#aux_bot = tabla.getSymbolData(bot)
						aux = tabla.getSymbolData(izquierda)
						izquierda = aux.value
	
				if (not isinstance(derecha, int)):
					if (derecha == "me"):
						print("Error: Uso de palabra reservada me no definido en instrucciones de controlador.")
						sys.exit()
					else:
						#aux_bot = tabla.getSymbolData(bot)
						aux = tabla.getSymbolData(derecha)
						derecha = aux.value
	
				resultado = self.condicion.evaluar(izquierda, operador, derecha, tabla)
	
			elif (isinstance(self.condicion, ArbolUn)):
				resultado = self.condicion.evaluar()
	
			elif (isinstance(self.condicion, Bool)):
				resultado = self.condicion.get_valor()
	
			elif(isinstance(self.condicion, Ident)):
				tipo_ident = tabla.getSymbolData(self.condicion.get_valor())
				if (tipo_ident.tipo == "bool" and tipo_ident.estado == "activado"):
					resultado = tipo_ident.value
				else:
					if (tipo_ident.estado != "activado"):
						print("Error: El bot " + tipo_ident.nombre + " no se encuenta activado.")
						sys.exit()
					else:
						print("Error: El tipo del bot " + tipo_ident.nombre + " no es booleano.")
						sys.exit()
	
			else:
				print("Error: condicion no definida en el lenguaje bot.")
				sys.exit()
	
			if (resultado):
				#print("este es el resultado de la condicion del WHILE: ",resultado)
				#print("\n")
				#print("VOY A EJECUTAR LA INSTRUCCION DEL WHILE")
				self.instruccion.ejecutar(tabla, matrix)
			else:
				iterar = False

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

	def ejecutar(self, tabla, matrix):

		#print("\n")
		#print("ESTOY EN EL EJECUTAR DE ACTIVATE")
		#print("ESTOS SON LOS IDENTIFICADRES QUE VOY A ACTIVAR")
		#print(self.id_list)

		if (isinstance(self.id_list[0], ArbolInstr)):
				#print("NOS VAMOS A unirID_lista: ", self.id_list[0])
				#print("\n")
				#print("LISTA DEFINITIVA DE self.id_list", self.id_list)
				#print("\n")

				self.id_list = self.id_list[0].unirID_lista()

		for i in self.id_list:
			#print("ESTE ES EL I QUE VOY A USAR: ", i)
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

					for x in bot.behaviors.behavs:
						#print("i",i)
						if (x == "activation"):
							aux = bot.behaviors.getBehavData(x)
							#print("nombre", aux.bot)
							aux.ejecutar(tabla, matrix)
							#print("aux",aux)
	
			else:
				print("Error: el bot " + bot.nombre + " ya se encuentra activado.")
				sys.exit()

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

	def ejecutar(self, tabla, matrix):

		#print("\n")
		#print("ESTOY EN EL EJECUTAR DE DEACTIVATE")
		#print("ESTOS SON LOS IDENTIFICADRES QUE VOY A DESACTIVAR")
		#print(self.id_list)



		if (isinstance(self.id_list[0], ArbolInstr)):
				#print("NOS VAMOS A unirID_lista: ", self.id_list[0])
				self.id_list = self.id_list[0].unirID_lista()
				#print("\n")
				#print("LISTA DEFINITIVA DE self.id_list", self.id_list)
				#print("\n")


		for i in self.id_list:
			#print("ESTE ES EL I QUE VOY A USAR: ", i)
			bot = tabla.getSymbolData(i.value)

			if (bot.estado == "activado"):
				bot.estado = "desactivado"

				if (bot.behaviors):

				
					for x in bot.behaviors.behavs:
						if (x == "deactivation"):
							aux = bot.behaviors.getBehavData(x)
							aux.ejecutar(tabla, matrix)
							#print(aux)

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

	def ejecutar(self, tabla, matrix):
		#print("\n")
		#print("EN EJECUTAR DE ADVANCE")
		#print("\n")
		#print("ESTOS SON LOS IDENTIFICADRES QUE VOY A AVANZAR")

		if (isinstance(self.id_list[0], ArbolInstr)):
				#print("NOS VAMOS A unirID_lista: ", self.id_list[0])
				self.id_list = self.id_list[0].unirID_lista()
				#print("\n")
				#print("LISTA DEFINITIVA DE self.id_list", self.id_list)
				#print("\n")

		for i in self.id_list:

			#print("ESTE ES EL I QUE VOY A USAR EN ADVANCE: ", i)
			bot = tabla.getSymbolData(i.value)

			if (bot.estado == "activado"):
				
				if (bot.behaviors):
					for x in bot.behaviors.behavs:

						#print("x de bot.behaviors.behavs: ",x)

						if(x == True):
							"""AQUI VA EL MANEJO DE LAS EXPRESIONES COMO COMPORTAMIENTOS, HAY QUE VER COMO SE HACE
							PERO ESTOY SERIA LO IDEAL DE LA EJECUCION, EL BETA ES COMO SE LLEGA A QUE LA X SE HAGA TRUE"""
							aux = bot.behaviors.getBehavData(x)
							#print("x de bot.behaviors.behavs: ",x)
							#print("aux_bot",aux.bot)
							aux.ejecutar(tabla, matrix)							

						elif (x == "default"):
							aux = bot.behaviors.getBehavData(x)
							#print("aux_bot",aux.bot)
							aux.ejecutar(tabla, matrix)
							break

			else:
				print("Error: el bot " + bot.nombre + " no se encuentra activado.")
				sys.exit()		

class Store(ArbolInstr):
	"""Clase arbol para accion de Robot Store"""
	def __init__(self, token, children, expr):
		ArbolInstr.__init__(self, token, children, "store")
		self.expr = expr

	def ejecutar(self, tabla, bot, matrix):
		#print("\n")
		#print("EN EJECUTAR DE STORE")
		#print(self.expr)
		#print(self.children)
		#print("\n")

		aux_bot = tabla.getSymbolData(bot)

		if (isinstance(self.expr, ArbolBin)):

			izquierda = self.expr.get_valor_left()
			operador = self.expr.opsymbol
			derecha = self.expr.get_valor_right()

			if (not isinstance(izquierda, int)):
				if (izquierda == "me"):

					izquierda = aux_bot.meVal

				elif (izquierda in tabla.tabla):
						
					tmp_boti = tabla.getSymbolData(izquierda)
		
					izquierda = tmp_boti.value 
					
				else:
					#aux_bot = tabla.getSymbolData(bot)
					aux = aux_bot.behaviors.getVarData(izquierda)
					izquierda = aux.value

			if (not isinstance(derecha, int)):
				if (derecha == "me"):
					derecha = aux_bot.meVal

				elif (derecha in tabla.tabla):
					# print("ADSADASD", tabla)
					# tabla.printTables()		

					tmp_botd = tabla.getSymbolData(derecha)
		
					derecha = tmp_botd.value

				else:
					#aux_bot = tabla.getSymbolData(bot)
					aux = aux_bot.behaviors.getVarData(derecha)
					derecha = aux.value

			#print("izquierda: ", izquierda)
			#print("derecha: ", derecha)
			#print("operador: ", operador)

			resultado = self.expr.evaluar(izquierda, operador, derecha, tabla)

			#print ("ESTE ES VALOR DEL EVALUAR: ", resultado)


		elif (isinstance(self.expr, ArbolUn)):
			
			if (self.expr.tipo == "ARITMETICA" or self.expr.tipo == "BOOLEANA"):
				resultado = self.expr.get_valor()
				
			else:
				print("Error: Tipo de bot " + aux_bot.nombre +" incompatible.")
				sys.exit()

		elif (isinstance(self.expr, Numero)):

			if (aux_bot.tipo == "int"):
				resultado = self.expr.get_valor()
			else:
				print("Error: Tipo de bot " + aux_bot.nombre +" incompatible.")
				sys.exit()

		elif (isinstance(self.expr, Bool)):
			if (aux_bot.tipo == "bool"):
				resultado = self.expr.get_valor()

			else:
				print("Error: Tipo de bot " + aux_bot.nombre +" incompatible.")
				sys.exit()

		elif (isinstance(self.expr, Ident)):
			ident = self.expr.get_valor()
			# Verifico que el identificador este declarado y obtengo su instancia en la tabla 

			if (ident in tabla.tabla):
				# Es identificador declarado y obtengo su instancia

				ident = tabla.getSymbolData(ident)

				if (aux_bot.tipo == ident.tipo):
					resultado = ident.value

				else:
					print("Error: Tipo de bot " + aux_bot.nombre +" incompatible.")
					sys.exit()

			else:
				if (len(ident) == 3):
					# Es un caracter
					resultado = ident

				else:
					print("Error: Identificador " + ident + "no declarado.")
					sys.exit()


		elif (isinstance(self.expr, NewLine)):
			resultado = self.expr.get_valor()

		elif (isinstance(self.expr, str)):
			print("SE ME OLVIDO HACER LO DEL CHAR")

		aux_bot.value = resultado

		aux_bot.meVal = resultado

		#print("RESULTADO STORE: ",resultado," para bot: ", aux_bot.nombre)

class Collect(ArbolInstr):
	"""Clase arbol para accion de Robot Collect"""
	def __init__(self, token, children, id_list = None):
		ArbolInstr.__init__(self, token, children, "collect")
		self.id_list = id_list

	def ejecutar(self, tabla, bot, matrix):
		#print("EN EJECUTAR DE COLLECT")
		#print("bot", bot)
		#print("id_list: ", self.id_list)
		#print("ESTA EN LA TABLA ", self.id_list.get_valor() in tabla.tabla)

		aux_bot = tabla.getSymbolData(bot)
		valueInMatrix = matrix.collectOf(aux_bot.posicion)
		# En caso de que tenga as, se verifica si no esta en la tabla interna,
		# se saca el nombre de dicho identificador y se busca para guardar su valor

		if ((self.id_list) and (self.id_list.get_valor() in aux_bot.behaviors.interna)):

			var = self.id_list.get_valor()
			#print(aux_bot.behaviors.interna)

			aux_bot.behaviors.modificarVarInterna(var, valueInMatrix)

		elif(isinstance(self.id_list, Ident)):
			if (self.id_list.get_valor() in tabla.tabla):
				aux_bot = tabla.getSymbolData(self.id_list.get_valor())

				aux_bot.value = valueInMatrix
				aux_bot.modifMeVal(valueInMatrix)
			

		elif (self.id_list in tabla.tabla):

			aux_bot = tabla.getSymbolData(self.id_list.get_valor())

			aux_bot.value = valueInMatrix
			aux_bot.modifMeVal(valueInMatrix)
			
		else:

			aux_bot.value = valueInMatrix
			aux_bot.modifMeVal(valueInMatrix)

		#print("RESULTADO COLLECT: ",aux_bot.value ," para bot: ", var or aux_bot.nombre)


class Drop(ArbolInstr):
	"""Clase arbol para accion de Robot Drop"""
	def __init__(self, token, children, expr):
		ArbolInstr.__init__(self, token, children, "drop")
		self.expr = expr

	def ejecutar(self, tabla, bot, matrix):
		#print("\n")
		#print("EN EJECUTAR DE DROP")
		#print("bot", bot)
		#print("self.expr: ",self.expr.get_valor())
		#print("\n")

		aux_bot = tabla.getSymbolData(bot)

		if (isinstance(self.expr, ArbolBin)):

			izquierda = self.expr.get_valor_left()
			operador = self.expr.opsymbol
			derecha = self.expr.get_valor_right()

			if (not isinstance(izquierda, int)):
				if (izquierda == "me"):

					izquierda = aux_bot.meVal

				elif (izquierda in tabla.tabla):
						
					tmp_boti = tabla.getSymbolData(izquierda)
		
					izquierda = tmp_boti.value 
					
				else:
					#aux_bot = tabla.getSymbolData(bot)
					aux = aux_bot.behaviors.getVarData(izquierda)
					izquierda = aux.value

			if (not isinstance(derecha, int)):
				if (derecha == "me"):
					derecha = aux_bot.meVal

				elif (derecha in tabla.tabla):
					# print("ADSADASD", tabla)
					# tabla.printTables()		

					tmp_botd = tabla.getSymbolData(derecha)
		
					derecha = tmp_botd.value

				else:
					#aux_bot = tabla.getSymbolData(bot)
					aux = aux_bot.behaviors.getVarData(derecha)
					derecha = aux.value

			expr = self.expr.evaluar(izquierda, operador, derecha, tabla)

		elif(isinstance(self.expr, ArbolUn)):
			expr = self.expr.evaluar()

		else:
			expr = self.expr.get_valor()

		if (expr == 'me'):

			expr = aux_bot.meVal

		#print("ANTES DE EXPLOTAR: ", expr)		
		matrix.dropIn(aux_bot.posicion, expr)

		#print("QUIERO VERIFICAR EL READ, TERMINO EL PROGRAMA AQUI")
		#sys.exit()

class Direccion(ArbolInstr):
	"""Clase arbol para accion de Robot Direccion"""
	def __init__(self, token, children, direccion, expr = None):
		ArbolInstr.__init__(self, token, children, "direccion")
		self.direccion = direccion
		self.expr = expr

	def ejecutar(self, tabla, bot, matrix):
		#print("EN EJECUTAR DE DIRECCION")
		#print("bot", bot)
		#print("self.expr: ",self.expr)
		#print("self.direccion: ", self.direccion)
		botToMove = tabla.getSymbolData(bot)

		if self.expr:
			if (isinstance(self.expr, ArbolBin) or isinstance(self.expr, ArbolUn)):
				expr = self.expr.evaluar()
			else:
				expr = self.expr.get_valor()
			botToMove.moverse(self.direccion, expr)
		else:
			botToMove.moverse(self.direccion)	

		
class Read(ArbolInstr):
	"""Clase arbol para accion de Robot Read"""
	def __init__(self, token, children, id_list = None):
		ArbolInstr.__init__(self, token, children, "read")
		self.id_list = id_list

	def ejecutar(self, tabla, bot, matrix):
		#print("EN EJECUTAR DE READ")
		#print("bot", bot)
		#print("self.id_list: ",self.id_list)


		aux_bot = tabla.getSymbolData(bot)
		#print("aux_bot.tipo", aux_bot.tipo)

		# En caso de que tenga as, se saca el nombre de dicho identificador y se busca para guardar su valor

		if (self.id_list):
			var = self.id_list.get_valor()
			if var:
				if (aux_bot.tipo == "int"):
					valorEntrada = int(input("Introduzca la entrada para el bot " + aux_bot.nombre + " de tipo " + aux_bot.tipo + ": "))
				elif (aux_bot.tipo == "char"):
					valorEntrada = input("Introduzca la entrada para el bot " + aux_bot.nombre + " de tipo " + aux_bot.tipo + ": ")
					if (len(valorEntrada) > 1):
						print("Error: El bot " + aux_bot.nombre + " solo acepta un caracter al ser del tipo char.")
						sys.exit()
				elif (aux_bot.tipo == 'bool'):
					valorEntrada = bool(input("Introduzca la entrada para el bot " + aux_bot.nombre + " de tipo " + aux_bot.tipo + ": "))

				#print("TYPE DE valorEntrada", type(valorEntrada))
				if (not var in aux_bot.behaviors.interna):
					aux_bot.behaviors.createVarInterna(var, valorEntrada)
				else:
					aux_bot.behaviors.modificarVarInterna(var, valorEntrada)
				#print("RESULTADO READ: ",valorEntrada ," para variable: ", var)
			
		else:
			if (aux_bot.tipo == "int"):
				aux_bot.value = int(input("Introduzca la entrada para el bot " + aux_bot.nombre + " de tipo " + aux_bot.tipo + ": "))
			elif (aux_bot.tipo == "char"):
				aux_bot.value = input("Introduzca la entrada para el bot " + aux_bot.nombre + " de tipo " + aux_bot.tipo + ": ")
				if (len(valorEntrada) > 1):
					print("Error: El bot " + aux_bot.nombre + " solo acepta un caracter al ser del tipo char.")
					sys.exit()
			elif (aux_bot.tipo == 'bool'):
				aux_bot.value = bool(input("Introduzca la entrada para el bot " + aux_bot.nombre + " de tipo " + aux_bot.tipo + ": "))

			#print("TYPE DE aux_bot.value", type(aux_bot.value))

			aux_bot.modifMeVal(aux_bot.value)
		#print("RESULTADO READ: ",aux_bot.value ," para bot: ", aux_bot.nombre)


class Send(ArbolInstr):
	"""Clase arbol para accion de Robot Send"""
	def __init__(self, token, children):
		ArbolInstr.__init__(self, token, children, "send")

	def ejecutar(self, tabla, bot, matrix):
		#print("EN EJECUTAR DE SEND")
		#print("bot", bot)

		aux_bot = tabla.getSymbolData(bot)

		if (aux_bot.value == '\\n'):
			print("\n")

		else:
			print(aux_bot.value,end=" ")
			#print("RESULTADO SEND: ",aux_bot.value, " para bot: ", aux_bot.nombre)




"""NO SE USA, SE VA A USAR READ COMO UNICA INSTRUCCION, HAY QUE BORRARLA AQUI Y EN EL PARSER """		
class Receive(ArbolInstr):
	"""Clase arbol para accion de Robot Receive"""
	def __init__(self, token, children):
		ArbolInstr.__init__(self, token, children, "receive")