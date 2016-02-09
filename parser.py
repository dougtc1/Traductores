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

######################## OPERACIONES ARITMETICAS ##############################
def p_exp_suma(p):
    'E : E TkSuma T'
    p[0] = p[1] + p[3]
 
def p_exp_resta(p):
    'E : E TkResta T'
    p[0] = p[1] - p[3]

def p_exp_mod(p):
    'E : E TkMod T'
    p[0] = p[1] % p[3]    

def p_exp_t(p):
    'E : T'
    p[0] = p[1]

def p_t_mult(p):
    'T : T TkMult F'
    p[0] = p[1] * p[3]

def p_t_div(p):
    'T : T TkDiv F'
    p[0] = p[1] / p[3]

def p_t_f(p):
    'T : F'
    p[0] = p[1]

def p_f_num(p):
    'F : TkNum'
    p[0] = p[1]

def p_f_exp(p):
    'F : TkParabre E TkParcierra'
    p[0] = p[2]

# Creo que no necesitamos el %prec porque tenemos un token especifico para el op unario

def p_exp_menos(p):
    'E : TkResta E %prec TkMenos'
    p[0] = -p[2]

###############################################################################
########################### OPERACIONES BOOLEANAS #############################
def p_exp_conj(p):
    'E : E TkConjuncion B'
    p[0] = p[1] and p[3]

def p_exp_disy(p):
    'E : E TkDisyuncion B'
    p[0] = p[1] or p[3]

def p_exp_neg(p):
    'E : TkNegacion E'
    p[0] = not p[2]

def p_exp_b(p):
    'E : B'
    p[0] = p[1]

def p_b_bool(p):
    'B : TkBool'
    p[0] = p[1]

def p_b_exp(p):
    'B  : TkParabre E TkParcierra'
    p[0] = p[2]

###############################################################################
########################## OPERACIONES RELACIONALES ###########################
def p_exp_mayor(p):
    '''E : E TkMayor T
         | E TkMayor B'''
    p[0] = p[1] > p[3]

def p_exp_mayorigual(p):
    '''E : E TkMayorigual T
         | E TkMayorigual B'''
    p[0] = p[1] >= p[3]

def p_exp_menor(p):
    '''E : E TkMenor T
         | E TkMenor B'''
    p[0] = p[1] < p[3]

def p_exp_menorigual(p):
    '''E : E TkMenorigual T
         | E TkMenorigual B'''
    p[0] = p[1] <= p[3]

def p_exp_igual(p):
    '''E : E TkIgual T
         | E TkIgual B'''
    p[0] = (p[1] = p[3])

def p_exp_noigual(p):
    '''E : E TkNoigual T
         | E TkNoigual B'''
    p[0] = (p[1] != p[3])

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

# Gramatica libre de contexto

def p_E_Start(p):
    '''Start : TkCreate Dec TkExecute InstC TkEnd
             | TkExecute InstC_list TkEnd'''

def p_E_Dec(p):
    '''Dec : Type TkBot ID_list TkEnd
           | Type TkBot ID_list Comportamiento TkEnd'''

def p_E_Type(p):
    '''Type : TkInt
            | TkBool
            | TkChar'''

def p_E_ID_list(p):
    '''ID_list : ID_list, ID_list
               | TkIdent'''

def p_E_Comportamiento(p):
    '''Comportamiento : TkOn Condicion TkDospuntos InstRobot_list TkEnd
                      | TkPass''' #Creo que hay que agregar una instruccion vacia (TkPass) para que esto tenga sentido

def p_E_Condicion(p):
    '''Condicion : TkActivation
                 | TkDeactivation
                 | TkBool
                 | default''' #Debe ser Tkdefault o esto es algo cuyo comportamiento implementamos despues?

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
    '''InstRobot_list : TkStore E TkPunto InstRobot_list
                      | TkStore TkMe E TkPunto InstRobot_list
                      | TkCollect TkPunto InstRobot_list
                      | TkCollect TkAs ID_list TkPunto InstRobot_list
                      | TkDrop E TkPunto InstRobot_list
                      | TkDrop TkMe TkPunto InstRobot_list
                      | TkUp TkPunto InstRobot_list
                      | TkDown TkPunto InstRobot_list 
                      | TkLeft TkPunto InstRobot_list
                      | TkRight TkPunto InstRobot_list
                      | TkUp E TkPunto InstRobot_list
                      | TkDown E TkPunto InstRobot_list
                      | TkLeft E TkPunto InstRobot_list
                      | TkRight E TkPunto InstRobot_list
                      | TkRead TkPunto InstRobot_list
                      | TkRead TkAs ID_list TkPunto InstRobot_list
                      | TkSend TkPunto InstRobot_list
                      | TkReceive TkPunto InstRobot_list'''

# Parece que faltan 5 palabras que estan en la lista tokens de lexBOT.py y no estan en las palabras reservadas/simbolos reconocidos
