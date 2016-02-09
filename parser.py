# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexBOT import tokens

precedence = (
    ('left', 'TkMayor', 'TkMenor', 'TkMayorigual', 'TkMenorigual', 'TkIgual','TkNoigual'),
    ('left', 'TkSuma', 'TkResta'),
    ('left', 'TkMult', 'TkDiv', 'TkMod'),
    ('left', 'TkConjuncion', 'TkDisyuncion'),
    ('right', 'TkMenos', 'TkNegacion')
)

###############################################################################
################################ INSTRUCCIONES ################################

def p_exp_activate(p):
    'E : TkActivate ID'
    p[]

# Error rule for syntax errors
def p_error(p):
    print("Error de sintaxis en la entrada")

# Build the parser
parser = yacc.yacc()

#############################################33

# Estructura ejemplo arbol 

class Expresion:
    pass

class Bin_Expresion(Expresion):
    def __init__(self,exp_izq,operador,exp_der):
        self.tipo = "Bin_Expresion"
        self.exp_izq = exp_izq
        self.exp_der = exp_der
        self.operador = operador

class Numero(Expresion):
    def __init__(self,valor):
        self.tipo = "numero"
        self.valor = valor

class Booleano(Expresion):
    def __init__(self,valor):
        self.tipo = "booleano"
        self.valor = valor

class Relacional(Expresion):
    def __init__(self,valor):
        self.tipo = "relacional"
        self.valor = valor

def p_E_numero(p):
    '''E : TkNum
         | E TkSuma E
         | E TkResta E
         | E TkMult E
         | E TkDiv E
         | E TkMod E
         | TkMenos E'''
    p[0] = Numero(p[0])

def p_E_booleano(p):
    '''E : TkBool
         | E TkIgual E
         | E TkNoigual E
         | E TkConjuncion E
         | E TkDisyuncion E
         | TkNegacion E'''
    p[0] = Booleano(p[0])

def p_E_relacional(p):
    '''E : E TkIgual E
         | E TkNoigual E
         | E TkMenorigual E
         | E TkMayorigual E
         | E TkMenor E
         | E TkMayor E'''
    p[0] = Relacional(p[0])

"""
###
### Betancourt, estas funcionalidades las tenemos que hacer pero para otra entrega, cierto?
###

name = {}

def p_statement_assign(p):
    '''E : E TkStore E
         | E TkStore T
         | E TkStore F'''
    names[p[1]] = t[3]
"""

# Gramatica libre de contexto #################################################
def p_lambda(p):
    'lambda :'
    pass

def p_E_Start(p):
    '''Start : TkCreate Dec TkExecute InstC TkEnd
             | TkExecute InstC TkEnd'''

def p_E_Dec(p):
    'Dec : Type TkBot ID_list Comportamiento TkEnd'

def p_E_Type(p):
    '''Type : TkInt
            | TkBool
            | TkChar'''

def p_E_ID_list(p):
    '''ID_list : ID_list, ID_list
               | TkIdent'''

def p_E_Comportamiento(p):
    '''Comportamiento : TkOn Condicion TkDospuntos InstRobot_list TkEnd
                      | Comportamiento Comportamiento
                      | lambda'''

def p_E_Condicion(p):
    '''Condicion : TkActivation
                 | TkDeactivation
                 | TkBool
                 | TkDefault''' #Debe ser Tkdefault o esto es algo cuyo comportamiento implementamos despues?

def p_E_InstC(p):
    '''InstC : TkActivate ID_list
             | TkDeactivate ID_list
             | TkAdvance ID_list
             | TkIf TkBool TkDospuntos InstC TkEnd
             | TkIf TkBool TkDospuntos InstC TkElse InstC TkEnd
             | TkWhile TkBool TkDospuntos InstC TkEnd
             | Start
             | InstC InstC'''

def p_E_InstRobot_list(p):
    '''InstRobot_list : InstRobot_list InstRobot_list
                      | TkStore Expr TkPunto 
                      | TkCollect TkPunto 
                      | TkCollect TkAs ID_list TkPunto 
                      | TkDrop E TkPunto 
                      | Dir TkPunto
                      | Dir Expr TkPunto
                      | TkRead TkPunto 
                      | TkRead TkAs ID_list TkPunto 
                      | TkSend TkPunto 
                      | TkReceive TkPunto'''

def p_E_Dir(p):
    '''Dir : TkUp
           | TkDown
           | TkLeft
           | TkRight'''

def p_E_Expr(p):
    '''Expr : AritBinexpr
            | AritUnexpr
            | BoolBinexpr
            | BoolUnexpr
            | TkParabre Expr TkParcierra
            | TkNum
            | TkBool
            | TkMe'''

def p_E_AritBinexpr(p):
    '''Binexpr : Expr TkSuma Expr
               | Expr TkResta Expr
               | Expr TkMult Expr
               | Expr TkDiv Expr
               | Expr TkMod Expr
               | Expr TkMayor Expr
               | Expr TkMayorigual Expr
               | Expr TkMenor Expr
               | Expr TkMenorigual Expr
               | Expr TkIgual Expr
               | Expr TkNoigual Expr'''

def p_E_BoolBinexpr(p):
    '''BoolBinexpr : Expr TkConjuncion Expr
                   | Expr TkDisyuncion Expr
                   | Expr TkMayor Expr
                   | Expr TkMayorigual Expr
                   | Expr TkMenor Expr
                   | Expr TkMenorigual Expr
                   | Expr TkIgual Expr
                   | Expr TkNoigual Expr'''

def p_E_AritUnexpr(p):
    'Unexpr : TkResta Expr %prec TkMenos'

def p_E_BoolUnexpr(p):
    'BoolUnexpr : TkNegacion Expr'
    
# Parece que faltan 5 palabras que estan en la lista tokens de lexBOT.py y no estan en las palabras reservadas/simbolos reconocidos
