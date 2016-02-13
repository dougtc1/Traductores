class Expr: pass
class Instr: pass

class ArbolBin(Expr):
    def __init__(self, left, op, right, tipo=None):
        self.type = tipo
        self.left = left
        self.right = right
        self.op = op
        
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
        print("token", self.token)
        print("tipoInstruccion", self.tipoInstruccion)

    def printPreorden(self):
        """print("en printPreorden")
        print(self.token)
        if (self.children == None):
            for hijo in self.children:
                hijo.printPreorden()
        else:
            print ("Voy a imprimir")
            self.imprimir()
            print("Ya imprimi")
        print("self.children", self.children)"""
        if (isinstance(child, Activate)):
            child.imprimir()
        elif(isinstance(child, Deactivate)):
            child.imprimir()
        elif(isinstance(child, Activate)):
            child.imprimir()
        else:
            print(type(child))

        if (self.children):
            for child in self.children:
                #if (len(child.children) == 0):
                #print("tipo", type(child))
                if (isinstance(child, ArbolInstr)):
                    child.printPreorden()
                else:
                    #print(child.value)
                    print("child", child)

class CondicionalIf(ArbolInstr):
    def __init__(self, token, children, condicion, instruccion1, instruccion2=None):
        ArbolInstr.__init__(self, token, children, "CONDICIONAL")
        self.condicion = condicion
        self.instruccion1 = instruccion1
        self.instruccion2 = instruccion2

class IteracionIndef(ArbolInstr):
    def __init__(self, token, children, condicion, instruccion):
        ArbolInstr.__init__(self, token, children, "ITERACION_INDEF")
        self.condicion = condicion
        self.instruccion = instruccion

class Activate(ArbolInstr):
    def __init__(self, token, children, id_list):
        ArbolInstr.__init__(self, token, children, "ACTIVACION")
        self.id_list = id_list

    def imprimir(self):
        ArbolInstr.imprimir(self)
        print(self.tipoInstruccion)
        for i in self.children:
            print('\t' "-var: ", i)

class Deactivate(ArbolInstr):
    def __init__(self, token, children, id_list):
        ArbolInstr.__init__(self, token, children, "DESACTIVACION")
        self.id_list = id_list

    def imprimir(self):
        ArbolInstr.imprimir(self)
        print(self.tipoInstruccion)
        for i in self.children:
            print('\t' "-var: ", i)

class Advance(ArbolInstr):
    def __init__(self, token, children, id_list):
        ArbolInstr.__init__(self, token, children, "AVANCE")
        self.id_list = id_list

    def imprimir(self):
        ArbolInstr.imprimir(self)
        print(self.tipoInstruccion)
        for i in self.children:
            print('\t' "-var: ", i)