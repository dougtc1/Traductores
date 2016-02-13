class Expr: pass
class Instr: pass

class ArbolBin(Expr):
    def __init__(self, tipo, left, op, right):
        self.type = tipo
        self.left = left
        self.op = op
        self.right = right

    def get_valor_left(self):
        return self.left.get_valor()
        
    def get_valor_right(self):
        return self.right.get_valor()

class ArbolUn(Expr):
    def __init__(self,operando,operador,tipo=None):
        self.operando = operando
        self.operador = operador
        self.type = tipo

class Numero(Expr):
    def __init__(self,value):
        self.type = "Numero"
        self.value = value

    def get_valor(self):
        return self.value


class Bool(Expr):
    def __init__(self,value):
        self.type = "Bool"
        self.value = value

    def get_valor(self):
        return self.value

class Ident(Expr):
    def __init__(self,value):
        self.type = "Identificador"
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
        """print("token", self.token)
        print("tipoInstruccion", self.tipoInstruccion)"""
        pass

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
        
        if (self.children):
            for child in self.children:
                #if (len(child.children) == 0):
                #print("tipo", type(child))
                if (isinstance(child, Activate)):
                    child.imprimir()
                elif(isinstance(child, Deactivate)):
                    child.imprimir()
                elif(isinstance(child, Advance)):
                    child.imprimir()
                elif(isinstance(child, CondicionalIf)):
                    child.imprimir()
                elif(isinstance(child, IteracionIndef)):
                    child.imprimir()
                if (isinstance(child, ArbolInstr)):
                    child.printPreorden()
                else:
                    #print(child.value)
                    #print("child", child)
                    pass

class CondicionalIf(ArbolInstr):
    def __init__(self, token, children, condicion, instruccion1, instruccion2=None):
        ArbolInstr.__init__(self, token, children, "CONDICIONAL")
        self.condicion = condicion
        self.instruccion1 = instruccion1
        self.instruccion2 = instruccion2

    def imprimir(self):
        ArbolInstr.imprimir(self)
        print (self.tipoInstruccion)
        print('\t' "- guardia: ", self.token)
        print('\t' '\t' "- operacion: ", self.condicion.op)
        print('\t' '\t' "- operador izquierdo: ", self.condicion.get_valor_left())
        print('\t' '\t' "- operador derecho: ", self.condicion.get_valor_right())

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
        for i in self.id_list:
            print('\t' "-var: ", i.value)

class Deactivate(ArbolInstr):
    def __init__(self, token, children, id_list):
        ArbolInstr.__init__(self, token, children, "DESACTIVACION")
        self.id_list = id_list

    def imprimir(self):
        ArbolInstr.imprimir(self)
        print(self.tipoInstruccion)
        for i in self.id_list:
            print('\t' "-var: ", i.value)

class Advance(ArbolInstr):
    def __init__(self, token, children, id_list):
        ArbolInstr.__init__(self, token, children, "AVANCE")
        self.id_list = id_list

    def imprimir(self):
        ArbolInstr.imprimir(self)
        print(self.tipoInstruccion)
        for i in self.id_list:
            print('\t' "-var: ", i.value)