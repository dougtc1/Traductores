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