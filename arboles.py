class Expr: pass
class Instr: pass

class ArbolBin(Expr):
    def __init__(self,left,op,right,tipo=None):
        self.left = left
        self.right = right
        self.op = op
        self.type = tipo

class ArbolUn(Expr):
    def __init__(self,operando,operador,tipo=None):
        self.operando = operando
        self.operador = operador
        self.type = tipo

class Numero(Expr):
    def __init__(self,value):
        self.type = "Numero"
        self.value = value

class Bool(Expr):
    def __init__(self,value):
        self.type = "Bool"
        self.value = value

class Ident(Expr):
    def __init__(self,value):
        self.type = "Identificador"
        self.value = value

class ArbolInstr(Instr):
    def __init__(self,children=None, tipoInstruccion=None):
        if (children):
            self.children = children
        else:
            self.children = [ ]
        self.tipoInstruccion = tipoInstruccion

    def recorrer_preorden(self):
        if (self.children == None):
            for hijo in self.children:
                hijo.recorrer_preorden()
        else:
            print ("Voy a imprimir")
            self.imprimir()
            print("Ya imprimi")

class CondicionalIf(ArbolInstr):
    def __init__(self, children, condicion, instruccion1, instruccion2=None):
        ArbolInstr.__init__(self, children, "CONDICIONAL")
        self.condicion = condicion
        self.instruccion1 = instruccion1
        self.instruccion2 = instruccion2

class IteracionIndef(ArbolInstr):
    def __init__(self, children, condicion, instruccion):
        ArbolInstr.__init__(self, children, "ITERACION_INDEF")
        self.condicion = condicion
        self.instruccion = instruccion

class Activate(ArbolInstr):
    def __init__(self, children, id_list):
        ArbolInstr.__init__(self, children, "ACTIVACION")
        self.id_list = id_list

    def imprimir(self):
        ArbolInstr.imprimir(self)
        print(self.tipoInstruccion)
        for i in self.children:
            print('\t' "-var: ", i)

class Deactivate(ArbolInstr):
    def __init__(self, children, id_list):
        ArbolInstr.__init__(self, children, "DESACTIVACION")
        self.id_list = id_list

    def imprimir(self):
        print(self.tipoInstruccion)
        for i in self.children:
            print('\t' "-var: ", i)

class Advance(ArbolInstr):
    def __init__(self, children, id_list):
        ArbolInstr.__init__(self, children, "AVANCE")
        self.id_list = id_list

    def imprimir(self):
        print(self.tipoInstruccion)
        for i in self.children:
            print('\t' "-var: ", i)