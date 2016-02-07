class nodo:
	def __init__ (self,nodo=None,hijoIzq=None,hijoDer=None,tipo=None,padre=None):
		self.nodo=nodo
		self.hijoIzq=hijoIzq
		self.hijoDer=hijoDer
		self.tipo=tipo
		self.padre=padre


class tipolBooleano(nodo):
	def __init__ (self,nodo,hijoIzq,hijoDer,tipo="booleano",padre,resultado):
		nodo.__init__(self,nodo,hijoIzq,hijoDer,tipo,padre)
		self.resultado = resultado

class tipolAritmetico(nodo):
	def __init__ (self,nodo,hijoIzq,hijoDer,tipo="aritmetico",padre,resultado):
		nodo.__init__(self,nodo,hijoIzq,hijoDer,tipo,padre)
		self.resultado = resultado

class tipolRelacional(nodo):
	def __init__ (self,nodo,hijoIzq,hijoDer,tipo="relacional",padre,resultado):
		nodo.__init__(self,nodo,hijoIzq,hijoDer,tipo,padre)
		self.resultado = resultado