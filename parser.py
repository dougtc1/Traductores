# Yacc example

import ply.yacc as yacc
import re
from arboles import *
from lexBOT import *
global ASA

precedence = (
    ('left', 'TkMayor', 'TkMenor', 'TkMayorigual', 'TkMenorigual', 'TkIgual','TkNoigual'),
    ('left', 'TkSuma', 'TkResta'),
    ('left', 'TkMult', 'TkDiv', 'TkMod'),
    ('left', 'TkConjuncion', 'TkDisyuncion'),
    ('right', 'TkMenos', 'TkNegacion')
)

###############################################################################
################################ INSTRUCCIONES ################################
###############################################################################

# Gramatica libre de contexto 
ASA = ArbolInstr()
def p_estructura_Start(p):
    '''Start : TkCreate Declaraciones_lista TkExecute InstC_lista TkEnd
             | TkExecute InstC_lista TkEnd'''
    print("EN START")
    print("p[2] - Declaraciones_lista", p[2].children[1].children[0].children[0].children[0])
    print("\n")
    if (len(p) == 6):
        #ASA = ArbolInstr("Start", [p[1], p[2], p[3], p[4], p[5]])
        ASA.add_token("Start")
        ASA.add_children([p[1], p[2], p[3], p[4], p[5]])
        p[0] = ASA
    else:
        #ASA = ArbolInstr("Start", [p[1], p[2], p[3]])
        ASA.add_token("Start")
        ASA.add_children([p[1], p[2], p[3]])
        p[0] = ASA


def p_estructura_Declaraciones_lista(p):
    '''Declaraciones_lista : Declaraciones Declaraciones_lista
                           | Declaraciones'''
    print("EN Declaraciones_lista")
    print("p[0]",p[0])
    print("p[1]",p[1])
    print("\n")
    if (len(p) == 3):
        p[0] = ArbolInstr("Declaraciones_lista", [p[1], p[2]])
    else:
        p[0] = ArbolInstr("Declaraciones_lista", [p[1]])

def p_estructura_Declaraciones(p):
    '''Declaraciones : Type TkBot ID_list Comportamiento_lista TkEnd
                     | Type TkBot ID_list TkEnd'''
    print("EN Declaraciones")
    print("p[0]",p[0])
    print("p[1]",p[1])
    print("p[2]",p[2])
    print("\n")
    if (len(p) == 6):
        p[0] = ArbolInstr("Declaraciones", [p[1], p[2], p[3], p[4]])
    else:
        p[0] = ArbolInstr("Declaraciones", [p[1],p[2],p[3]])

def p_expresion_Type(p):
    '''Type : TkInt
            | TkBool
            | TkChar'''
    print("EN Type")
    print("p[0]",p[0])
    print("p[1]",p[1])
    print("\n")
    p[0] = ArbolInstr("Type", [p[1]])

def p_expresion_ID_list(p):
    '''ID_list : TkIdent TkComa ID_list
               | TkIdent'''
    print("EN ID_list")
    print("p[0]",p[0])
    print("p[1]",p[1])
    print("\n")
    if (len(p) == 4):
        p[0] = ArbolInstr("ID_list", [p[1], p[3]])
    else:
        p[0] = Ident(p[1])

def p_instruccion_Comportamiento_lista(p):
    '''Comportamiento_lista : Comportamiento Comportamiento_lista
                            | Comportamiento'''
    print("EN Comportamiento_lista")
    print("p[0]",p[0])
    print("p[1]",p[1])
    print("\n")
    if (len(p) == 3):
        p[0] = ArbolInstr("Comportamiento_lista", [p[1],p[2]])
    else:
        p[0] = ArbolInstr("Comportamiento_lista",[p[1]])

def p_instruccion_Comportamiento(p):
    'Comportamiento : TkOn Condicion TkDospuntos InstRobot_lista TkEnd'
    print("EN Comportamiento")
    print("p[0]", p[0])
    print("p[1]", p[1])
    print("p[2]", p[2])
    print("p[3]", p[3])
    print("p[4]", p[4])
    print("p[5]", p[5])
    print("\n")
# Parece innecesario
    if (len(p) == 6):
        p[0] = ArbolInstr("Comportamiento", [p[1], p[2], p[4]])

def p_instruccion_Condicion(p):
    '''Condicion : TkActivation
                 | TkDeactivation
                 | Expr
                 | TkDefault'''
    print("EN Condicion")
    print("p[0]",p[0])
    print("p[1]",p[1])
    print("\n")    
    p[0] = ArbolInstr("Condicion",[p[1]])

def p_instruccion_InstC_lista(p):
    '''InstC_lista : InstC InstC_lista
                   | InstC'''
    print("EN InstC_lista")
    print("p[0]",p[0])
    print("p[1]",p[1])
    print("\n")
    if (len(p) == 3):
        p[0] = ArbolInstr("InstC_lista",[p[1],p[2]],"SECUENCIACION")
    else:
        p[0] = ArbolInstr("InstC_lista",[p[1]])

def p_instruccion_InstC(p):
    '''InstC : TkActivate ID_list TkPunto
             | TkDeactivate ID_list TkPunto
             | TkAdvance ID_list TkPunto
             | InstrIf
             | InstrWhile
             | Start'''
    print("EN InstC")
    print("p[0]",p[0])
    print("p[1]",p[1])
    print("\n")
    if (p[1] == 'activate'):
        print("ASIGNANDO A ARBOL Activate #######################################################################################")
        print(p[2])
        p[0] = Activate("InstrC", None, [p[2]])
    elif (p[1] == 'deactivate'):
        print("ASIGNANDO A ARBOL Deactivate #####################################################################################")
        p[0] = Deactivate("InstrC", None, [p[2]])
    elif (p[1] == 'advance'):
        print("ASIGNANDO A ARBOL Advance ########################################################################################")
        print(p[2])
        p[0] = Advance("InstrC", None, [p[2]])
    else:
        p[0] = ArbolInstr("InstrC", [p[1]])

def p_instruccion_InstrIf(p):
    '''InstrIf : TkIf Expr TkDospuntos InstC_lista TkEnd 
               | TkIf Expr TkDospuntos InstC_lista TkElse TkDospuntos InstC_lista TkEnd'''
    print("EN InstrIf")
    print("p[0]",p[0])
    print("p[1]",p[1])
    print("p[2]",p[2])
    print("p[3]",p[3])
    print("p[4]",p[4])
    print("p[5]",p[5])
    print("\n")
    if (len(p) == 6):
        p[0] = CondicionalIf("InstrIf", [p[1], p[2], p[4]], p[2], p[4])
    else:
        p[0] = CondicionalIf("InstrIf", [p[1], p[2], p[4], p[5], p[7]], p[2], p[4], p[7])

def p_instruccion_InstrWhile(p):
    'InstrWhile : TkWhile Expr TkDospuntos InstC_lista TkEnd'
    print("EN InstrWhile")
    print("p[0]",p[0])
    print("p[1]",p[1])
    print("p[2]",p[2])
    print("p[3]",p[3])
    print("p[4]",p[4])
    print("p[5]",p[5])
    print("\n")
    p[0] = IteracionIndef("InstrWhile", [p[1], p[2], p[4]], p[2], p[4])

def p_instruccion_InstRobot_lista(p):
    '''InstRobot_lista : InstRobot InstRobot_lista
                       | InstRobot'''
    print("EN InstRobot_lista")
    print("p[0]",p[0])
    print("p[1]",p[1])
    print("\n")
    if(len(p) == 3):
        p[0] = ArbolInstr("InstRobot_lista",[p[1], p[2]])
    else:
        p[0] = ArbolInstr("InstRobot_lista",[p[1]])

def p_instruccion_InstRobot(p):
    '''InstRobot : TkStore Expr TkPunto 
                 | TkCollect TkPunto 
                 | TkCollect TkAs ID_list TkPunto 
                 | TkDrop Expr TkPunto 
                 | Direccion TkPunto
                 | Direccion Expr TkPunto
                 | TkRead TkPunto 
                 | TkRead TkAs ID_list TkPunto 
                 | TkSend TkPunto 
                 | TkReceive TkPunto'''
    print("EN InstRobot")
    print("p[0]",p[0])
    print("p[1]",p[1])
    print("\n")
    if (len(p) == 3):
        p[0] = ArbolInstr("InstRobot",[p[1]])
    elif (len(p) == 4):
        p[0] = ArbolInstr("InstRobot",[p[1], p[2]])
    elif (len(p) == 5):
        p[0] = ArbolInstr("InstRobot", [p[1], p[2], p[3]])

def p_instruccion_Direccion(p):
    '''Direccion : TkUp
                 | TkDown
                 | TkLeft
                 | TkRight'''
    print("EN Direccion")
    print("p[0]",p[0])
    print("p[1]",p[1])
    print("\n")
    p[0] = ArbolInstr("Direccion", [p[1]])

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
             | TkCaracter
             | TkTrue
             | TkFalse
             | TkMe'''
    print("EN EXPR")
    print("P", p)
    print("P[0]", p[0])
    print("P[1]", p[1])
    print("\n")
#    print("EXPR P[2]", p[2])

    if (len(p) > 3):
        
        if (p[2] == '+'):
            p[0] = ArbolBin("Aritmetica", p[1],"'Suma'", p[3])
        elif (p[2] == "-"):
            p[0] = ArbolBin("Aritmetica", p[1], "'Resta'", p[3])
        elif (p[2] == "*"):
            p[0] = ArbolBin("Aritmetica", p[1], "'Multiplicacion'",p[3])
        elif (p[2] == "/"):
            p[0] = ArbolBin("Aritmetica", p[1], "'Division'",p[3])
        elif (p[2] == "%"):
            p[0] = ArbolBin("Aritmetica", p[1], "'Modulo'", p[3])
        elif (p[2] == "/\\"):
            p[0] = ArbolBin("Booleano", p[1], "'Conjuncion'", p[3])
        elif (p[2] == "\\/"):
            p[0] = ArbolBin("Booleano", p[1], "'Disyuncion'", p[3])
        elif (p[2] == "="):
            p[0] = ArbolBin("Relacional", p[1], "'Igualdad'", p[3])
        elif (p[2] == "/\="):
            p[0] = ArbolBin("Relacional", p[1], "'Desigualdad'", p[3])
        elif (p[2] == ">"):
            p[0] = ArbolBin("Relacional", p[1], "'Mayor que'", p[3])
        elif (p[2] == "<"):
            p[0] = ArbolBin("Relacional", p[1], "'Menor que'", p[3])
        elif (p[2] == ">="):
            p[0] = ArbolBin("Relacional", p[1], "'Mayor igual que'", p[3])
        elif (p[2] == "<="):
            p[0] = ArbolBin("Relacional", p[1], "'Menor igual que'", p[3])
        elif (p[1] == "(" and p[3] == ")"):
            p[0] = p[2]
    
    else:

        if (p[1] == "-" and len(p) == 3):
            p[0] = -p[2]
        elif (p[1] == "~" and len(p) == 3):
            p[0] = ArbolUn("Booleana", p[2], p[1])
        elif (len(p) == 2 and isinstance(p[1],int)):
            p[0] = Numero(p[1])
        elif (len(p) == 2 and isinstance(p[1],str)):
            p[0] = Ident(p[1])
        elif (p[1] == 'True' or p[1] == 'False'):
            p[0] = Bool(p[1])

def p_error(p):
   print("Error de sintaxis en la entrada") 

###############################################################################
