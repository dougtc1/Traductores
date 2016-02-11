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
        self.type = tipo
        self.operando = operando
        self.operador = operador

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

class ArbolInstr(Expr):
    def __init__(self, token=None, children=None, tipoInstruccion=None):
        self.token = token
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.tipoInstruccion = tipoInstruccion

    def printPreorden(self):
        for child in self.children:
            if (len(child.children) == 0):
                if (type(child) == 'ArbolInstr'):
                    print(child.token)
                else:
                    print(child.value)

            if (child.children):
                child.printPreorden()


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