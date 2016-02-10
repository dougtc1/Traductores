# Yacc example

import ply.yacc as yacc
from arboles import Nodo
# Get the token map from the lexer.  This is required.
from lexBOT import tokens

import re

precedence = (
    ('left', 'TkMayor', 'TkMenor', 'TkMayorigual', 'TkMenorigual', 'TkIgual','TkNoigual'),
    ('left', 'TkSuma', 'TkResta'),
    ('left', 'TkMult', 'TkDiv', 'TkMod'),
    ('left', 'TkConjuncion', 'TkDisyuncion'),
    ('right', 'TkMenos', 'TkNegacion')
)

###############################################################################
################################ INSTRUCCIONES ################################
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

ASA = ArbolInst()

def p_lambda(p):
    'lambda :'
    pass

def p_estructura_Start(p):
    '''Start : TkCreate Dec TkExecute InstC TkEnd
             | TkExecute InstC TkEnd'''
    if (len(p) == 6):
        p[0] = ASA([p[1], p[2], p[3], p[4], p[5]])
    else:
        p[0] = ASA([p[1], p[2], p[3]])

def p_estructura_Declaraciones(p):
    ''''Declaraciones : Declaraciones Declaraciones
                      | Type TkBot ID_list Comportamiento TkEnd'''
    if (len(p) == 3):
        p[0] = ArbolInst([p[1], p[2]])
    else:
        p[0] = ArbolInst([p[1], p[2], p[3], p[4], p[5]])

def p_expresion_Type(p):
    '''Type : TkInt
            | TkBool
            | TkChar'''
    p[0] = ArbolInst(p[1])

def p_expresion_ID_list(p):
    '''ID_list : ID_list TkComa ID_list
               | TkIdent'''
    if (len(p) == 4):
        p[0] = ArbolInst([p[1], p[2], p[3]])
    else:
        p[0] = ArbolInst(p[1])

def p_instruccion_Comportamiento(p):
    '''Comportamiento : Comportamiento Comportamiento
                      | TkOn Condicion TkDospuntos InstRobot TkEnd
                      | lambda'''
    if (len(p) == 3):
        p[0] = ArbolInst([p[1], p[2]])
    elif (len(p) == 6):
        p[0] = Comportamiento(p[2], p[4]) # ESTO ES NUEVO, funciona como el del while
    else:
        pass

def p_instruccion_Condicion(p):
    '''Condicion : TkActivation
                 | TkDeactivation
                 | ExprBooleana
                 | TkDefault'''
    p[0] = ArbolInst(p[1])

def p_instruccion_InstC(p):
    '''InstC : TkActivate ID_list TkPunto
             | TkDeactivate ID_list TkPunto
             | TkAdvance ID_list TkPunto
             | InstrIf
             | InstrWhile
             | Start
             | InstC InstC'''

    if (p[1] == 'TkActivate'):
        p[0] = ArbolInst(p[1], p[2], p[3], "ACTIVACION")
    elif (p[1] == 'TkDeactivate'):
        p[0] = ArbolInst(p[1], p[2], p[3], "DESACTIVACION")
    elif (p[1] == 'TkAdvance'):
        p[0] = ArbolInst(p[1], p[2], p[3], "AVANCE")
    elif (len(p) == 3): # No hay peo porque en los otros casos que el len es igual a 2 son casos que ya deberian de haber entrado
        p[0] = ArbolInst(p[1], p[2], "SECUENCIACION")
    else:
        p[0] = ArbolInst(p[1])


def p_instruccion_InstrIf(p):
    '''InstrIf : TkIf Expr TkDospuntos InstC TkEnd 
               | TkIf Expr TkDospuntos InstC TkElse TkDospuntos InstC end'''
    if (len(p) == 6):
        p[0] = CondicionalIf(p[2], p[4], "CONDICIONAL")
    else:
        p[0] = CondicionalIf(p[2], p[4], p[7], "CONDICIONAL")

def p_instruccion_InstrWhile(p):
    'InstrWhile : TkWhile Expr TkDospuntos InstC TkEnd'
    p[0] = IteracionIndef(p[2], p[4], "REPETICION_INDET")

def p_instruccion_InstRobot(p):
    '''InstRobot : InstRobot InstRobot
                 | TkStore Expr TkPunto 
                 | TkCollect TkPunto 
                 | TkCollect TkAs ID_list TkPunto 
                 | TkDrop Expr TkPunto 
                 | Direccion TkPunto
                 | Direccion Expr TkPunto
                 | TkRead TkPunto 
                 | TkRead TkAs ID_list TkPunto 
                 | TkSend TkPunto 
                 | TkReceive TkPunto'''
    if (len(p) == 3):
        p[0] = ArbolInst([p[1], p[2]])
    elif (len(p) == 4):
        p[0] = ArbolInst([p[1], p[2], p[3]])
    elif (len(p) == 5):
        p[0] = ArbolInst([p[1], p[2], p[3], p[4]])

def p_instruccion_Direccion(p):
    '''Direccion : TkUp
                 | TkDown
                 | TkLeft
                 | TkRight'''
    p[0] = ArbolInst(p[1])

# Correccion Monascal 

##################################################################################################

def p_expresion_Expr(p):
    ''' Expr : Expr TkSuma Expr
             | Expr TkResta Expr
             | Expr TkMult Expr
             | Expr TkDiv Expr
             | Expr TkMod Expr
             | Expr TkConjuncion Expr
             | Expr TkDisyuncion Expr
             | Expr TkIgual Expr
             | Expr TkNoigual Expr
             | Expr TkMayor Expr
             | Expr TkMenor Expr
             | Expr TkMayorigual Expr
             | Expr TkMenorigual Expr
             | TkParabre Expr TkParcierra
             | TkResta Expr %prec TkMenos
             | TkNegacion Expr
             | TkNum
             | TkIdent
             | TkBool'''

    if (p[2] == "+"):
        p[0] = ArbolBin("Aritmetica",p[0], p[1], p[3])
    elif (p[2] == "-"):
        p[0] = ArbolBin("Aritmetica",p[0], p[1], p[3])
    elif (p[2] == "*"):
        p[0] = ArbolBin("Aritmetica",p[0], p[1], p[3])
    elif (p[2] == "/"):
        p[0] = ArbolBin("Aritmetica",p[0], p[1], p[3])
    elif (p[2] == "%"):
        p[0] = ArbolBin("Aritmetica",p[0], p[1], p[3])
    elif (p[2] == "/\\"):
        p[0] = ArbolBin("Booleano",p[0], p[1], p[3])
    elif (p[2] == "\\/"):
        p[0] = ArbolBin("Booleano",p[0], p[1], p[3])
    elif (p[2] == "="):
        p[0] = ArbolBin("Relacional",p[0], p[1], p[3])
    elif (p[2] == "/\="):
        p[0] = ArbolBin("Relacional",p[0], p[1], p[3])
    elif (p[2] == ">"):
        p[0] = ArbolBin("Relacional",p[0], p[1], p[3])
    elif (p[2] == "<"):
        p[0] = ArbolBin("Relacional",p[0], p[1], p[3])
    elif (p[2] == ">="):
        p[0] = ArbolBin("Relacional",p[0], p[1], p[3])
    elif (p[2] == "<="):
        p[0] = ArbolBin("Relacional",p[0], p[1], p[3])
    elif (p[1] == "(" and p[3] == ")"):
        p[0] = p[2]
    elif (p[1] == "-" and len(p) == 3):
        p[0] = -p[2]
    elif (p[1] == "~" and len(p) == 3):
        p[0] = ArbolUn("Booleana", p[2], p[1])
    elif (len(p) == 2 and int(p[1])):
        p[0] = Numero(p[1])
    elif (len(p) == 2 and re.search(([a-zA-Z][a-zA-Z0-9_]*),p[1])):
        p[0] = Ident(p[1])
    elif (p[1] == 'True' or p[1] == 'False'):
        p[0] = Bool(p[1])


##################################################################################################

# En Stand-By

"""
def p_expresion_Expr(p):
    '''Expr : ExprAritmetica
            | ExprBooleana
            | ExprRelacional'''
    p[0] = ArbolInst(p[1])

def p_expresion_RangoRel(p):
    '''RangoRel : ExprAritmetica
                | ExprBooleana'''
    p[0] = ArbolInst(p[1])

def p_expresion_ExprAritmetica(p):
    '''ExprAritmetica : E TkSuma E
                      | E TkResta E
                      | E TkMult E
                      | E TkDiv E
                      | E TkMod E
                      | E'''
    if (len(p) == 4):
        p[0] = ArbolBin("Aritmetica", p[1], p[3], p[2])
    else:
        p[0] = p[1]

def p_expresion_AritParentizada(p):
    'E : TkParabre ExprAritmetica TkParcierra'
    p[0] = p[2]

def p_expresion_AritVariable(p):
    'E : TkIdent'
    p[0] = Ident(p[1])

def p_expresion_Numerica(p):
    'E : TkNum'
    p[0] = Numero(p[1])

def p_expresion_Negativa(p):
    'E : TkResta E %prec TkMenos'
    p[0] = Numero(-p[1])
    
def p_expresion_EtoArit(p):
    'E : ExprAritmetica'
    p[0] = p[1]

def p_expresion_ExprBooleana(p):
    '''ExprBooleana : B TkConjuncion B
                    | B TkDisyuncion B
                    | ExprRelacional
                    | B'''
    if (len(p) == 4):
        p[0] = ArbolBin("Booleano", p[1], p[3], p[2])
    else:
        p[0] = p[1]

def p_expresion_BoolParentizada(p):
    'B : TkParabre ExprBooleana TkParcierra'
    p[0] = p[2]

def p_expresion_BoolVariable(p):
    'B : TkIdent'
    p[0] = Ident(p[1])

def p_expresion_Booleana(p):
    'B : TkBool'
    p[0] = Bool(p[1])

def p_expresion_Negada(p):
    'B : TkNegacion B'
    p[0] = ArbolUn("Booleana", p[2], p[1])

def p_expresion_BtoBool(p):
    'B : ExprBooleana'
    p[0] = p[1]

def p_expresion_Relacional(p):
    '''ExprRelacional : RangoRel TkMayor RangoRel
                      | RangoRel TkMayorigual RangoRel
                      | RangoRel TkMenor RangoRel
                      | RangoRel TkMenorigual RangoRel
                      | RangoRel TkIgual RangoRel
                      | RangoRel TkNoigual RangoRel'''   
    p[0] = ArbolBin("Relacional", p[1], p[3], p[2])

# Parece que faltan 5 palabras que estan en la lista tokens de lexBOT.py y no estan en las palabras reservadas/simbolos reconocidos

"""