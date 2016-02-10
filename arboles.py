class Expr: pass
class Instr: pass

class ArbolBin(Expr):
    def __init__(self,tipo=None,left,op,right):
        self.type = tipo
        self.left = left
        self.right = right
        self.op = op

class Numero(Expr):
    def __init__(self,value):
        self.type = "Numero"
        self.value = value

class ArbolInstr(Instr):
    def __init__(self,children=None, tipoInstruccion=None):
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.tipoInstruccion = tipoInstruccion

"""
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    p[0] = BinOp(p[1],p[2],p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Number(p[1])
    """