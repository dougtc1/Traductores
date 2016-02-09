# Yacc example

import ply.yacc as yacc
from arboles import Nodo
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

def p_estructura_Start(p):
    '''Start : TkCreate Dec TkExecute InstC TkEnd
             | TkExecute InstC TkEnd'''
    p[0] = Nodo("S", None, [Nodo(p[1]), Nodo(p[2]), Nodo(p[3]), Nodo(p[4]), ])

def p_estructura_Declaraciones(p):
    ''''Declaraciones : Declaraciones Declaraciones
                      | Type TkBot ID_list Comportamiento TkEnd'''

def p_expresion_Type(p):
    '''Type : TkInt
            | TkBool
            | TkChar'''

def p_expresion_ID_list(p):
    '''ID_list : ID_list TkComa ID_list
               | TkIdent'''

def p_instruccion_Comportamiento(p):
    '''Comportamiento : Comportamiento Comportamiento
                      | TkOn Condicion TkDospuntos InstRobot TkEnd
                      | lambda'''

def p_instruccion_Condicion(p):
    '''Condicion : TkActivation
                 | TkDeactivation
                 | TkBool
                 | TkDefault'''

def p_instruccion_InstC(p):
    '''InstC : TkActivate ID_list
             | TkDeactivate ID_list
             | TkAdvance ID_list
             | TkIf ExprBooleana TkDospuntos InstC TkEnd
             | TkIf ExprBooleana TkDospuntos InstC TkElse InstC TkEnd
             | TkWhile ExprBooleana TkDospuntos InstC TkEnd
             | Start
             | InstC InstC'''

def p_instruccion_InstRobot(p):
    '''InstRobot : InstRobot InstRobot
                 | TkStore Expr TkPunto 
                 | TkCollect TkPunto 
                 | TkCollect TkAs ID_list TkPunto 
                 | TkDrop ExprAritmetica TkPunto 
                 | Dir TkPunto
                 | Dir ExprAritmetica TkPunto
                 | TkRead TkPunto 
                 | TkRead TkAs ID_list TkPunto 
                 | TkSend TkPunto 
                 | TkReceive TkPunto'''

def p_instruccion_Direccion(p):
    '''Direccion : TkUp
                 | TkDown
                 | TkLeft
                 | TkRight'''

def p_expresion_Expr(p):
    '''Expr : ExprAritmetica
            | ExprBooleana
            | ExprRelacional'''

def p_expresion_RangoRel(p):
    '''RangoRel : ExprAritmetica
                | ExprBooleana'''

def p_expresion_ExprAritmetica(p):
    '''ExprAritmetica : E TkSuma E
                      | E TkResta E
                      | E TkMult E
                      | E TkDiv E
                      | E TkMod E
                      | E'''

def p_expresion_AritParentizada(p):
    'E : (ExprAritmetica)'

def p_expresion_AritVariable(p):
    'E : TkIdent'

def p_expresion_Numerica(p):
    'E : TkNum'

def p_expresion_Negativa(p):
    'E : TkResta E %prec TkMenos'

def p_expresion_EtoArit(p):
    'E : ExprAritmetica'

def p_expresion_ExprBooleana(p):
    '''ExprBooleana : B TkConjuncion B
                    | B TkDisyuncion B
                    | B'''

def p_expresion_BoolParentizada(p):
    'B : (ExprBooleana)'

def p_expresion_BoolVariable(p):
    'B : TkIdent'

def p_expresion_Booleana(p):
    'B : TkBool'

def p_expresion_Negada(p):
    'B : TkNegacion B'

def p_expresion_BtoBool(p):
    'B : ExprBooleana'

def p_expresion_Relacional(p):
    '''ExprRelacional : RangoRel TkMayor RangoRel
                      | RangoRel TkMayorigual RangoRel
                      | RangoRel TkMenor RangoRel
                      | RangoRel TkMenorigual RangoRel
                      | RangoRel TkIgual RangoRel
                      | RangoRel TkNoigual RangoRel'''   ## DOUGLAS ME ILUMINE NOJODAAAAAAAAA ##################

# Parece que faltan 5 palabras que estan en la lista tokens de lexBOT.py y no estan en las palabras reservadas/simbolos reconocidos
