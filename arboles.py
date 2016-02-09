class Nodo:
	def __init__(self, contenido=None, padre=None):
		self.contenido = contenido
		self.padre     = padre
		self.hijos     = []

	def __str__(self):
		return str(self.contenido)

	def addNode(self, contenido):
		self.hijos.append(Nodo(contenido, self))
