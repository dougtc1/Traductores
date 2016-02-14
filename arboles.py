import textwrap

cantidadTabs = 0

class Expr: pass
class Instr: pass

class ArbolBin(Expr):
    def __init__(self, tipo, left, op, right):
        self.tipo  = tipo
        self.left  = left
        self.op    = op
        self.right = right

    def get_valor_left(self):
        return self.left.get_valor()
        
    def get_valor_right(self):
        return self.right.get_valor()

class ArbolUn(Expr):
    def __init__(self,tipo, operador,operando):
        self.tipo     = tipo
        self.operador = operador
        self.operando = operando

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

        if (self.children):
            for child in self.children:
                if (isinstance(child, Activate)):
                    print (textwrap.fill(child.tipoInstruccion, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
                    cantidadTabs    = auxCantidadTabs
                    cantidadTabs    += 1
                    auxCantidadTabs = cantidadTabs
                    lista = child.imprimir()
                    for i in lista:
                        print (textwrap.fill(i, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
                    cantidadTabs -= 1
                    auxCantidadTabs = cantidadTabs

                elif (isinstance(child, Deactivate)):
                    print (textwrap.fill(child.tipoInstruccion, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
                    cantidadTabs    = auxCantidadTabs
                    cantidadTabs    += 1
                    auxCantidadTabs = cantidadTabs
                    lista = child.imprimir()
                    for i in lista:
                        print (textwrap.fill(i, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
                    cantidadTabs -= 1
                    auxCantidadTabs = cantidadTabs

                elif (isinstance(child, Advance)):
                    print (textwrap.fill(child.tipoInstruccion, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
                    cantidadTabs    = auxCantidadTabs
                    cantidadTabs    += 1
                    auxCantidadTabs = cantidadTabs
                    lista = child.imprimir()
                    for i in lista:
                        print (textwrap.fill(i, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
                    cantidadTabs -= 1
                    auxCantidadTabs = cantidadTabs

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
                        if (child.token == 'InstC_lista' and len(child.children)>1):
                            print (textwrap.fill(child.tipoInstruccion, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
                            cantidadTabs += 1
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
            
            aux = "- expr: " + str(self.condicion.get_valor())
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

            aux = "- expr: " + str(self.condicion.get_valor())
            print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
            cantidadTabs -= 1

        elif (isinstance(self.condicion, Numero)):
            aux = "- guardia: " + str(self.condicion.tipo)
            print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
            cantidadTabs += 1

            aux = "- expr: " + str(self.condicion.get_valor())
            print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
            cantidadTabs -= 1

 
        print(textwrap.fill("- exito: ", initial_indent='\t'*cantidadTabs),end=" ")
        auxCantidadTabs = cantidadTabs
        cantidadTabs    = 0
        self.instruccion1.printPreorden()

        if (self.instruccion2):
            print(textwrap.fill("- fracaso: ", initial_indent='\t'*cantidadTabs),end=" ")
            auxCantidadTabs = cantidadTabs
            cantidadTabs    = 0
            self.instruccion2.printPreorden()
        else:
            pass

class IteracionIndef(ArbolInstr):
    def __init__(self, token, children, condicion, instruccion):
        ArbolInstr.__init__(self, token, children, "ITERACION_INDEF")
        self.condicion = condicion
        self.instruccion = instruccion

    def imprimir(self):

        global cantidadTabs
        global auxCantidadTabs
        
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

            aux = "- expr: " + str(self.condicion.get_valor())
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

            aux = "- expr: " + str(self.condicion.get_valor())
            print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
            cantidadTabs -= 1

        elif (isinstance(self.condicion, Numero)):
            aux = "- guardia: " + str(self.condicion.tipo)
            print (textwrap.fill(aux, initial_indent='\t'*cantidadTabs,subsequent_indent='\t'))
            cantidadTabs += 1

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