import ply.lex as lex
import ply.yacc as yacc

class CalcError(Exception):
    def __init__(self, message):
        self.message = message

reserved = {
    'Program' : 'PROGRAM',
    'main' : 'MAIN',
    'var' : 'VAR',
    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'void' : 'VOID',
    'module' : 'MODULE',
    'return' : 'RETURN',
    'read' : 'READ',
    'write' : 'WRITE',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'do' : 'DO',
    'while' : 'WHILE',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'from' : 'FROM',
    'to' : 'TO',
    'Line' : 'LINE',
    'Point' : 'POINT',
    'Circle' : 'CIRCLE',
    'Arc' : 'ARC',
    'PenUp' : 'PENUP',
    'PenDown' : 'PENDOWN',
    'Color' : 'COLOR',
    'Size' : 'SIZE',
    'Clear' : 'CLEAR'
}
 
tokens = ['AND','OR','LT','LE','GT','GE','EQ','NE','EQUAL','LPAREN','RPAREN','LPAREN2','RPAREN2','PUNCOM','COMA','NINT','NFLOAT','SCHAR','SSTRING','SVAR'] + list(reserved.values())

literals = [ '+','-','*','/' ]

t_AND     = r'&'
t_OR      = r'\|'
t_LT      = r'<'
t_LE      = r'<='
t_GT      = r'>'
t_GE      = r'>='
t_EQ      = r'=='
t_NE      = r'!='
t_EQUAL   = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LPAREN2 = r'\{'
t_RPAREN2 = r'\}'
t_PUNCOM  = r';'
t_COMA    = r','

def t_NINT(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_NFLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)    
    return t

def t_SCHAR(t):
    r'\'.\''
    return t

def t_SSTRING(t):
    r'\".*\"'  
    return t

def t_SVAR(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value,'SVAR')    # Check for reserved words
    return t

t_ignore  = ' \t\n'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Estructura
# { "nombre de vairable": {
#    "type": "tipo de variable",
#    "value": "valor de la variable"
# }}
# ejemplo de llamada
# variablesGlobales["nombre de variable"]["type"]
variablesGlobales = {}
# Estructura
# { "nombre de funcion" : {
#    "type": "tipo de funcion"
#    "var": {
#         "nombre de variable":{...}},
#    "param": {
#         "nombre de parametro":{...}}
# }}
# ejemplo de llamada
# variablesFunciones["nombre de funcion"]["var"]["nombre de variable"]["type"]
variablesFunciones = {}
# Estructura
# { "variableSystema ##" : {
#    "type": "tipo de variable",
#    "value": "valor de la variable"},
#   "contador": ##
# }
# ejemplo de llamada
# variablesTemporales["variableSystema ##"]["type"]
variablesTemporales = {"contador": 0}
# Estructura
# (op, opdo1, opdo2, result)
# (=, var, null, result)
# (callr, func, param, result)
# (callf, func, param, null)
# (call, func, param, null)
# (goto, null, null, pos)
# (gotof, value, null, pos)
# (return, null, null, result)
# (write, null, null, result)
# (read, null, null, result)

def p_program(p):
     'program : programInicio decfuntemp programMain'
     print("Compile!!")

# Solo sirve para imprimir una vez variablesFunciones, recordar borrar.
def p_decfuntemp(p):
     'decfuntemp : decfun'
     pass

def p_programMain(p):
     'programMain : MAIN LPAREN RPAREN LPAREN2 estatutos RPAREN2'
     #print ("****** funcion **********")
     #nombre = p[1]
     #print(nombre)
     acciones = p[5]
     #print("definicion de globales")
     #print(variablesGlobales)
     #print("definicion de funcion antes")
     #print(variablesFunciones[nombre])
     #print("definicion de temporales antes")
     #print(variablesTemporales)
     print("--------------")
     print("acciones")
     contador = 1
     for a,b,c,d in acciones:
          print(contador, ":", a, "|", b, "|", c, "|", d)
          contador = contador + 1
          if (a == '+' or a == '-' or a == '*' or a == '/'):
               tb = ""
               tc = ""
               if type(b) == type(1):
                    tb = "int"
               elif type(b) == type(1.0):
                    tb = "float"
               else:
                    if variablesGlobales.get(b) != None:
                         tb = variablesGlobales[b]["type"]
                    elif variablesTemporales.get(b) != None:
                         tb = variablesTemporales[b]["type"]
                    else:
                         print("ERROR: Nombre de variable invalido")
                         raise CalcError("Variable invalida")
               if type(c) == type(1):
                    tc = "int"
               elif type(c) == type(1.0):
                    tc = "float"
               else:
                    if variablesGlobales.get(c) != None:
                         tc = variablesGlobales[c]["type"]
                    elif variablesTemporales.get(c) != None:
                         tc = variablesTemporales[c]["type"]
                    else:
                         print("ERROR: Nombre de variable invalido")
                         raise CalcError("Variable invalida")
               if ((tb == "int" or tb == "float") and (tc == "int" or tc == "float")):
                    if tb == tc:
                         if tb == "int":
                              variablesTemporales[d] = {"type": "int"}
                         else:
                              variablesTemporales[d] = {"type": "float"}
                    else:
                         variablesTemporales[d] = {"type": "float"}
               else:
                    print("ERROR: Tipo de variable erroneo en expresion")
                    raise CalcError("Expresion invalida")
               if a == '/':
                    variablesTemporales[d] = {"type": "float"}
          elif a == '=':
               tb = ""
               td = ""
               if type(b) == type(1):
                    tb = "int"
               elif type(b) == type(1.0):
                    tb = "float"
               elif variablesGlobales.get(b) != None:
                    tb = variablesGlobales[b]["type"]
               elif variablesTemporales.get(b) != None:
                    tb = variablesTemporales[b]["type"]
               elif b[0] == "'":
                    tb = "char"
               else:
                    print("ERROR: Nombre de variable invalido")
                    raise CalcError("Variable invalida")
               if variablesGlobales.get(d) != None:
                    td = variablesGlobales[d]["type"]
               elif variablesTemporales.get(d) != None:
                    td = variablesTemporales[d]["type"]
               else:
                    print("ERROR: Nombre de variable invalido")
                    raise CalcError("Variable invalida")
               if ((tb == "char" and td != "char") or (tb == "float" and td != "float") or (tb == "int" and (td != "int" and td != "float"))):
                    print(variablesTemporales)
                    print("ERROR: Tipo de variable erroneo en asignacion")
                    raise CalcError("Estatuto invalido")
          elif a == "return":
               print("ERROR: Return en main")
               raise CalcError("Estatuto invalido")
          elif a == "callr":
               if variablesFunciones.get(b) == None:
                    print("ERROR: Nombre de funcion invalido")
                    raise CalcError("Expresion invalida")
               variablesTemporales[d] = {"type": variablesFunciones[b]["type"]}
               if len(c) != len(variablesFunciones[b]["param"]):
                    print("ERROR: Cantidad de parametros en llamada con return invalido")
                    raise CalcError("Expresion invalida")
               cont = 0
               for param in variablesFunciones[b]["param"]:
                    tc = ""
                    if type(c[cont]) == type(1):
                         tc = "int"
                    elif type(c[cont]) == type(1.0):
                         tc = "float"
                    elif variablesGlobales.get(c[cont]) != None:
                         tc = variablesGlobales[c[cont]]["type"]
                    elif variablesTemporales.get(c[cont]) != None:
                         tc = variablesTemporales[c[cont]]["type"]
                    elif c[cont][0] == "'":
                         tc = "char"
                    else:
                         print("ERROR: Nombre de variable invalido")
                         raise CalcError("Variable invalida")
                    if variablesFunciones[b]["param"][param]["type"] != tc:
                         print("ERROR: Tipo de variable invalido en llamada con return")
                         raise CalcError("Expresion invalida")
                    cont = cont + 1
          elif a == 'callf':
               print("pendiente")
               # checar el tipo de parametro con el tipo que debe de recibir
               # definir mejor las funciones antes de continuar
          elif a == 'call':
               if variablesFunciones.get(b) == None:
                    print("ERROR: Nombre de funcion invalido")
                    raise CalcError("Estatuto invalido")
               if len(c) != len(variablesFunciones[b]["param"]):
                    print("ERROR: Cantidad de parametros en llamada invalido")
                    raise CalcError("Estatuto invalido")
               cont = 0
               for param in variablesFunciones[b]["param"]:
                    tc = ""
                    if type(c[cont]) == type(1):
                         tc = "int"
                    elif type(c[cont]) == type(1.0):
                         tc = "float"
                    elif variablesGlobales.get(c[cont]) != None:
                         tc = variablesGlobales[c[cont]]["type"]
                    elif variablesTemporales.get(c[cont]) != None:
                         tc = variablesTemporales[c[cont]]["type"]
                    elif c[cont][0] == "'":
                         tc = "char"
                    else:
                         print("ERROR: Nombre de variable invalido")
                         raise CalcError("Variable invalida")
                    if variablesFunciones[b]["param"][param]["type"] != tc:
                         print("ERROR: Tipo de variable invalido en llamada")
                         raise CalcError("Estatuto invalido")
                    cont = cont + 1
          elif (a == '==' or a == '&' or a == '|'):
               variablesTemporales[d] = {"type": "bool"}
          elif (a == '>' or a == '<' or a == '>=' or a == '<='):
               tb = ""
               tc = ""
               if (type(b) != type(1) and type(b) != type(1.0)):
                    if variablesGlobales.get(b) != None:
                         tb = variablesGlobales[b]["type"]
                    elif variablesTemporales.get(b) != None:
                         tb = variablesTemporales[b]["type"]
                    elif b[0] != "'":
                         print("ERROR: Nombre de variable invalido")
                         raise CalcError("Variable invalida")
                    if (tb != "int" and tb != "float"):
                         print("ERROR: Tipo de variable invalido en comparacion 1")
                         raise CalcError("Estatuto invalido")
               if (type(c) != type(1) and type(c) != type(1.0)):
                    if variablesGlobales.get(c) != None:
                         tc = variablesGlobales[c]["type"]
                    elif variablesTemporales.get(c) != None:
                         tc = variablesTemporales[c]["type"]
                    elif c[0] != "'":
                         print("ERROR: Nombre de variable invalido")
                         raise CalcError("Variable invalida")
                    if (tc != "int" and tc != "float"):
                         print("ERROR: Tipo de variable invalido en comparacion 2")
                         raise CalcError("Estatuto invalido")
               variablesTemporales[d] = {"type": "bool"}
          elif (a != 'write' and a != 'read' and a != 'goto' and a != 'gotof'):
               print("Pendiente, proximamente error")
     print("--------------")
     #print("definicion de temporales despues")
     #print(variablesTemporales)
     pass

def p_programInicio(p):
     'programInicio : PROGRAM SVAR PUNCOM decvar'
     lista = p[4]
     for x in lista:
          variables = x[1]
          tipo = x[0]
          for var in variables:
               if variablesGlobales.get(var) == None:
                    variablesGlobales[var] = {"type":tipo}
               else:
                    print("ERROR: Nombre de variable global invalido")
                    raise CalcError("Variable repetida")
     pass

def p_decvar(p):
     '''
     decvar : VAR tipo SVAR nomvar decvar2
            | empty
     '''
     if p[1] != None:
          temp = [p[3]]
          temp.extend(p[4])
          temp2 = [[p[2],temp]]
          temp2.extend(p[5])
          p[0] = temp2
     else:
          p[0] = []
     pass

def p_decvar2(p):
     '''
     decvar2 : tipo SVAR nomvar decvar2
             | empty
     '''
     if p[1] == None:
          p[0] = []
     else:
          temp = [p[2]]
          temp.extend(p[3])
          temp2 = [[p[1],temp]]
          temp2.extend(p[4])
          p[0] = temp2
     pass

def p_nomvar(p):
     '''
     nomvar : COMA SVAR nomvar
            | PUNCOM
     '''
     if p[1] != ';':
          temp = [p[2]]
          temp.extend(p[3])
          p[0] = temp
     else:
          p[0] = []
     pass

def p_tipo(p):
     '''
     tipo : INT
          | FLOAT
          | CHAR
     '''
     p[0] = p[1]

def p_decfun(p):
     'decfun : decfunCodigo decfun2'
     pass

def p_decfunCodigo(p):
     'decfunCodigo : decfunCodigoIni LPAREN2 estatutos RPAREN2'
     #print ("****** funcion **********")
     nombre = p[1]
     #print(nombre)
     acciones = p[3]
     #print("definicion de globales")
     #print(variablesGlobales)
     #print("definicion de funcion antes")
     #print(variablesFunciones[nombre])
     #print("definicion de temporales antes")
     #print(variablesTemporales)
     print("--------------")
     print("acciones")
     contador = 1
     for a,b,c,d in acciones:
          print(contador, ":", a, "|", b, "|", c, "|", d)
          contador = contador + 1
          if (a == '+' or a == '-' or a == '*' or a == '/'):
               tb = ""
               tc = ""
               if type(b) == type(1):
                    tb = "int"
               elif type(b) == type(1.0):
                    tb = "float"
               else:
                    if variablesGlobales.get(b) != None:
                         tb = variablesGlobales[b]["type"]
                    elif variablesFunciones[nombre]["param"].get(b) != None:
                         tb = variablesFunciones[nombre]["param"][b]["type"]
                    elif variablesFunciones[nombre]["var"].get(b) != None:
                         tb = variablesFunciones[nombre]["var"][b]["type"]
                    elif variablesTemporales.get(b) != None:
                         tb = variablesTemporales[b]["type"]
                    else:
                         print("ERROR: Nombre de variable invalido")
                         raise CalcError("Variable invalida")
               if type(c) == type(1):
                    tc = "int"
               elif type(c) == type(1.0):
                    tc = "float"
               else:
                    if variablesGlobales.get(c) != None:
                         tc = variablesGlobales[c]["type"]
                    elif variablesFunciones[nombre]["param"].get(c) != None:
                         tc = variablesFunciones[nombre]["param"][c]["type"]
                    elif variablesFunciones[nombre]["var"].get(c) != None:
                         tc = variablesFunciones[nombre]["var"][c]["type"]
                    elif variablesTemporales.get(c) != None:
                         tc = variablesTemporales[c]["type"]
                    else:
                         print("ERROR: Nombre de variable invalido")
                         raise CalcError("Variable invalida")
               if ((tb == "int" or tb == "float") and (tc == "int" or tc == "float")):
                    if tb == tc:
                         if tb == "int":
                              variablesTemporales[d] = {"type": "int"}
                         else:
                              variablesTemporales[d] = {"type": "float"}
                    else:
                         variablesTemporales[d] = {"type": "float"}
               else:
                    print("ERROR: Tipo de variable erroneo en expresion")
                    raise CalcError("Expresion invalida")
               if a == '/':
                    variablesTemporales[d] = {"type": "float"}
          elif a == '=':
               tb = ""
               td = ""
               if type(b) == type(1):
                    tb = "int"
               elif type(b) == type(1.0):
                    tb = "float"
               elif variablesGlobales.get(b) != None:
                    tb = variablesGlobales[b]["type"]
               elif variablesFunciones[nombre]["param"].get(b) != None:
                    tb = variablesFunciones[nombre]["param"][b]["type"]
               elif variablesFunciones[nombre]["var"].get(b) != None:
                    tb = variablesFunciones[nombre]["var"][b]["type"]
               elif variablesTemporales.get(b) != None:
                    tb = variablesTemporales[b]["type"]
               elif b[0] == "'":
                    tb = "char"
               else:
                    print("ERROR: Nombre de variable invalido")
                    raise CalcError("Variable invalida")
               if variablesGlobales.get(d) != None:
                    td = variablesGlobales[d]["type"]
               elif variablesFunciones[nombre]["param"].get(d) != None:
                    td = variablesFunciones[nombre]["param"][d]["type"]
               elif variablesFunciones[nombre]["var"].get(d) != None:
                    td = variablesFunciones[nombre]["var"][d]["type"]
               elif variablesTemporales.get(d) != None:
                    td = variablesTemporales[d]["type"]
               else:
                    print("ERROR: Nombre de variable invalido")
                    raise CalcError("Variable invalida")
               if ((tb == "char" and td != "char") or (tb == "float" and td != "float") or (tb == "int" and (td != "int" and td != "float"))):
                    print(variablesTemporales)
                    print("ERROR: Tipo de variable erroneo en asignacion")
                    raise CalcError("Estatuto invalido")
          elif a == "return":
               td = ""
               if type(d) == type(1):
                    td = "int"
               elif type(d) == type(1.0):
                    td = "float"
               elif variablesGlobales.get(d) != None:
                    td = variablesGlobales[d]["type"]
               elif variablesFunciones[nombre]["param"].get(d) != None:
                    td = variablesFunciones[nombre]["param"][d]["type"]
               elif variablesFunciones[nombre]["var"].get(d) != None:
                    td = variablesFunciones[nombre]["var"][d]["type"]
               elif variablesTemporales.get(d) != None:
                    td = variablesTemporales[d]["type"]
               elif b[0] == "'":
                    td = "char"
               else:
                    print("ERROR: Nombre de variable invalido")
                    raise CalcError("Variable invalida")
               if variablesFunciones[nombre]["type"] == "void":
                    print("ERROR: Return en funcion void")
                    raise CalcError("Estatuto invalido")
               elif ((td == "char" and variablesFunciones[nombre]["type"] != "char") or (td == "float" and variablesFunciones[nombre]["type"] != "float") or (td == "int" and (variablesFunciones[nombre]["type"] != "int" and variablesFunciones[nombre]["type"] != "float"))):
                    print("ERROR: Tipo de variable erroneo en return")
                    raise CalcError("Estatuto invalido")
          elif a == "callr":
               if variablesFunciones.get(b) == None:
                    print("ERROR: Nombre de funcion invalido")
                    raise CalcError("Expresion invalida")
               variablesTemporales[d] = {"type": variablesFunciones[b]["type"]}
               if len(c) != len(variablesFunciones[b]["param"]):
                    print("ERROR: Cantidad de parametros en llamada con return invalido")
                    raise CalcError("Expresion invalida")
               cont = 0
               for param in variablesFunciones[b]["param"]:
                    tc = ""
                    if type(c[cont]) == type(1):
                         tc = "int"
                    elif type(c[cont]) == type(1.0):
                         tc = "float"
                    elif variablesGlobales.get(c[cont]) != None:
                         tc = variablesGlobales[c[cont]]["type"]
                    elif variablesFunciones[nombre]["param"].get(c[cont]) != None:
                         tc = variablesFunciones[nombre]["param"][c[cont]]["type"]
                    elif variablesFunciones[nombre]["var"].get(c[cont]) != None:
                         tc = variablesFunciones[nombre]["var"][c[cont]]["type"]
                    elif variablesTemporales.get(c[cont]) != None:
                         tc = variablesTemporales[c[cont]]["type"]
                    elif c[cont][0] == "'":
                         tc = "char"
                    else:
                         print("ERROR: Nombre de variable invalido")
                         raise CalcError("Variable invalida")
                    if variablesFunciones[b]["param"][param]["type"] != tc:
                         print("ERROR: Tipo de variable invalido en llamada con return")
                         raise CalcError("Expresion invalida")
                    cont = cont + 1
          elif a == 'callf':
               print("pendiente")
               # checar el tipo de parametro con el tipo que debe de recibir
               # definir mejor las funciones antes de continuar
          elif a == 'call':
               if variablesFunciones.get(b) == None:
                    print("ERROR: Nombre de funcion invalido")
                    raise CalcError("Estatuto invalido")
               if len(c) != len(variablesFunciones[b]["param"]):
                    print("ERROR: Cantidad de parametros en llamada invalido")
                    raise CalcError("Estatuto invalido")
               cont = 0
               for param in variablesFunciones[b]["param"]:
                    tc = ""
                    if type(c[cont]) == type(1):
                         tc = "int"
                    elif type(c[cont]) == type(1.0):
                         tc = "float"
                    elif variablesGlobales.get(c[cont]) != None:
                         tc = variablesGlobales[c[cont]]["type"]
                    elif variablesFunciones[nombre]["param"].get(c[cont]) != None:
                         tc = variablesFunciones[nombre]["param"][c[cont]]["type"]
                    elif variablesFunciones[nombre]["var"].get(c[cont]) != None:
                         tc = variablesFunciones[nombre]["var"][c[cont]]["type"]
                    elif variablesTemporales.get(c[cont]) != None:
                         tc = variablesTemporales[c[cont]]["type"]
                    elif c[cont][0] == "'":
                         tc = "char"
                    else:
                         print("ERROR: Nombre de variable invalido")
                         raise CalcError("Variable invalida")
                    if variablesFunciones[b]["param"][param]["type"] != tc:
                         print("ERROR: Tipo de variable invalido en llamada")
                         raise CalcError("Estatuto invalido")
                    cont = cont + 1
          elif (a == '==' or a == '&' or a == '|'):
               variablesTemporales[d] = {"type": "bool"}
          elif (a == '>' or a == '<' or a == '>=' or a == '<='):
               tb = ""
               tc = ""
               if (type(b) != type(1) and type(b) != type(1.0)):
                    if variablesGlobales.get(b) != None:
                         tb = variablesGlobales[b]["type"]
                    elif variablesFunciones[nombre]["param"].get(b) != None:
                         tb = variablesFunciones[nombre]["param"][b]["type"]
                    elif variablesFunciones[nombre]["var"].get(b) != None:
                         tb = variablesFunciones[nombre]["var"][b]["type"]
                    elif variablesTemporales.get(b) != None:
                         tb = variablesTemporales[b]["type"]
                    elif b[0] != "'":
                         print("ERROR: Nombre de variable invalido")
                         raise CalcError("Variable invalida")
                    if (tb != "int" and tb != "float"):
                         print("ERROR: Tipo de variable invalido en comparacion 1")
                         raise CalcError("Estatuto invalido")
               if (type(c) != type(1) and type(c) != type(1.0)):
                    if variablesGlobales.get(c) != None:
                         tc = variablesGlobales[c]["type"]
                    elif variablesFunciones[nombre]["param"].get(c) != None:
                         tc = variablesFunciones[nombre]["param"][c]["type"]
                    elif variablesFunciones[nombre]["var"].get(c) != None:
                         tc = variablesFunciones[nombre]["var"][c]["type"]
                    elif variablesTemporales.get(c) != None:
                         tc = variablesTemporales[c]["type"]
                    elif c[0] != "'":
                         print("ERROR: Nombre de variable invalido")
                         raise CalcError("Variable invalida")
                    if (tc != "int" and tc != "float"):
                         print("ERROR: Tipo de variable invalido en comparacion 2")
                         raise CalcError("Estatuto invalido")
               variablesTemporales[d] = {"type": "bool"}
          elif (a != 'write' and a != 'read' and a != 'goto' and a != 'gotof'):
               print("Pendiente, proximamente error")
     print("--------------")
     #print("definicion de temporales despues")
     #print(variablesTemporales)
     pass
     

def p_decfunCodigoIni(p):
     'decfunCodigoIni : MODULE funtipo SVAR LPAREN funpara RPAREN PUNCOM decvar'
     nombre = p[3]
     funtipo = p[2]
     listaParametros = p[5]
     listaVariables = p[8]
     if variablesFunciones.get(nombre) == None:
          variablesFunciones[nombre] = {}
          variablesFunciones[nombre]["type"] = funtipo
          variablesFunciones[nombre]["param"] = {}
          for x in listaParametros:
               variable = x[1]
               tipo = x[0]
               if variablesGlobales.get(variable) != None:
                    print("ERROR: Nombre de variable de parametro invalido por variable global")
                    raise CalcError("Variable repetida")
               elif variablesFunciones[nombre]["param"].get(variable) != None:
                    print("ERROR: Nombre de variable de parametro invalido")
                    raise CalcError("Variable repetida")
               else:
                    variablesFunciones[nombre]["param"][variable] = {"type":tipo}
          variablesFunciones[nombre]["var"] = {}
          for x in listaVariables:
               variables = x[1]
               tipo = x[0]
               for var in variables:
                    if variablesGlobales.get(var) != None:
                         print("ERROR: Nombre de variable de funcion invalido por variable global")
                         raise CalcError("Variable repetida")
                    elif variablesFunciones[nombre]["param"].get(var) != None:
                         print("ERROR: Nombre de variable de funcion invalido por variable de parametro")
                         raise CalcError("Variable repetida")
                    elif variablesFunciones[nombre]["var"].get(var) != None:
                         print("ERROR: Nombre de variable de funcion invalido")
                         raise CalcError("Variable repetida")
                    else:
                         variablesFunciones[nombre]["var"][var] = {"type":tipo}
     else:
          print("ERROR: Nombre de funcion invalido")
          raise CalcError("Funcion repetida")
     p[0] = nombre
     pass

def p_decfun2(p):
     '''
     decfun2 : decfun
             | empty
     '''
     pass

def p_funtipo(p):
     '''
     funtipo : tipo
             | VOID
     '''
     p[0] = p[1]
     pass

def p_funpara(p):
     '''
     funpara : tipo SVAR funpara2
             | empty
     '''
     if p[1] != None:
          temp = [[p[1], p[2]]]
          temp.extend(p[3])
          p[0] = temp
     else:
          p[0] = []
     pass

def p_funpara2(p):
     '''
     funpara2 : COMA tipo SVAR funpara2
              | empty
     '''
     if p[1] != None:
          temp = [[p[2], p[3]]]
          temp.extend(p[4])
          p[0] = temp
     else:
          p[0] = []
     pass

def p_estatutos(p):
     '''
     estatutos : asignacion estatutos
               | llamada estatutos
               | lectura estatutos
               | escritura estatutos
               | desicion estatutos
               | repeticion estatutos
               | funespecial estatutos
     '''
     #print("***** BANDERA ******")
     #print(p[1])
     #print("********************")

     # ya que algunas instrucciones siguen regresando vacio
     temp = []
     if p[1] != None:
          temp.extend(p[1])
     temp.extend(p[2])
     p[0] = temp
     pass

def p_estatutos02(p):
     '''
     estatutos : retorno
               | empty
     '''
     #print("***** BANDERA ******")
     #print(p[1])
     #print("********************")
     if p[1] != None:
          p[0] = p[1]
     else:
          p[0] = []
     pass

def p_asignacion(p):
     'asignacion : SVAR EQUAL asitipos PUNCOM'
     final = []
     if p[3][1] == "expr":
          if p[3][0][0][0] != None:
               final.extend(p[3][0])
          final.append( ('=', p[3][0][len(p[3][0])-1][3], None, p[1]) )
     else:
          final.append( ('=', p[3][0], None, p[1]) )
     p[0] = final
     pass

def p_asitipos(p):
     'asitipos : expr'
     p[0] = (p[1],"expr")
     pass

def p_asitipos02(p):
     'asitipos : SCHAR'
     p[0] = (p[1],"char")
     pass

def p_expr(p):
     'expr : exprCode'
     pila = []
     final = []
     for x in p[1]:
          if (x == '*' or x == '/' or x == '+' or x == '-'):
               y = pila.pop()
               z = pila.pop()
               variablesTemporales["contador"] = variablesTemporales["contador"] + 1
               varTemp = "variableSystema " + str(variablesTemporales["contador"])
               temp2 = (x,z,y,varTemp)
               pila.append(varTemp)
               final.append(temp2)
          elif type(x) != type(1):
               if x[0] == "Sys funcion":
                    parametros = []
                    temp2 = []
                    for para,tipo in x[2]:
                         if tipo == "char":
                              parametros.append(para)
                         else:
                              if para[0][0] == None:
                                   parametros.append(para[0][3])
                              else:
                                   parametros.append(para[len(para)-1][3])
                                   temp2.extend(para)
                    variablesTemporales["contador"] = variablesTemporales["contador"] + 1
                    varTemp = "variableSystema " + str(variablesTemporales["contador"])
                    temp2.append(("callr",x[1],parametros,varTemp))
                    pila.append(varTemp)
                    final.extend(temp2)
               else:
                    pila.append(x)
          else:
               pila.append(x)
     if final == []:
          final = [(None,None,None,p[1][0])]
     p[0] = final
     pass

def p_exprCode(p):
     '''
     exprCode : expr1 '+' exprCode
              | expr1 '-' exprCode
     '''
     temp = p[1]
     temp.extend(p[3])
     temp.append(p[2])
     p[0] = temp
     pass

def p_expr02(p):
     'exprCode : expr1'
     p[0] = p[1]
     pass

def p_expr1(p):
     '''
     expr1 : expr2 '*' expr1
           | expr2 '/' expr1
     '''
     temp = p[1]
     temp.extend(p[3])
     temp.append(p[2])
     p[0] = temp
     pass

def p_expr12(p):
     'expr1 : expr2'
     p[0] = p[1]
     pass

def p_expr2(p):
     '''
     expr2 : LPAREN exprCode RPAREN
           | term
     '''
     if p[1] != '(':
          p[0] = [p[1]]
     else:
          p[0] = p[2]
     pass

def p_term(p):
     '''
     term : NINT
          | NFLOAT
     '''
     p[0] = p[1]
     pass

def p_term02(p):
     'term : SVAR posfun'
     if p[2] == []:
          p[0] = p[1]
     else:
          p[0] = ("Sys funcion",p[1], p[2])
     pass

def p_posfun(p):
     '''
     posfun : LPAREN parametros RPAREN
            | empty
     '''
     if p[1] != None:
          p[0] = p[2]
     else:
          p[0] = []
     pass

def p_parametros(p):
     '''
     parametros : asitipos parametros2
                | empty
     '''
     if p[1] != None:
          temp = [p[1]]
          temp.extend(p[2])
          p[0] = temp
     else:
          p[0] = []
     pass

def p_parametros2(p):
     '''
     parametros2 : COMA asitipos parametros2
                 | empty
     '''
     if p[1] != None:
          temp = [p[2]]
          temp.extend(p[3])
          p[0] = temp
     else:
          p[0] = []
     pass

def p_llamada(p):
     'llamada : SVAR LPAREN parametros RPAREN PUNCOM'
     parametros = []
     parametros = []
     final = []
     for x in p[3]:
          if x[1] == "char":
               parametros.append(x[0])
          else:
               if x[0][0][0] == None:
                    parametros.append(x[0][0][3])
               else:
                    parametros.append(x[0][len(x[0])-1][3])
                    final.extend(x[0])
     final.append(("call",p[1],parametros,None))
     p[0] = final
     pass

def p_retorno(p):
     'retorno : RETURN LPAREN asitipos RPAREN PUNCOM'
     final = []
     if p[3][1] == "expr":
          if p[3][0][0][0] == None:
               final.append(("return", None, None, p[3][0][0][3]))
          else:
               final.extend(p[3][0])
               final.append(("return", None, None, p[3][0][len(p[3][0])-1][3]))
     else:
          final.append(("return",None,None,p[3][0]))
     p[0] = final
     pass

def p_lectura(p):
     'lectura : READ LPAREN SVAR lectura2 RPAREN PUNCOM'
     temp = [("read", None, None, p[3])]
     for x in p[4]:
          temp.append(("read", None, None, x))
     p[0] = temp
     pass

def p_lectura2(p):
     '''
     lectura2 : COMA SVAR lectura2
              | empty
     '''
     if p[1] != None:
          temp = [p[2]]
          temp.extend(p[3])
          p[0] = temp
     else:
          p[0] = []
     pass

def p_escritura(p):
     'escritura : WRITE LPAREN escritura2 escritura3 RPAREN PUNCOM'
     temp = p[3]
     temp.extend(p[4])
     final = []
     for x in temp:
          if x[0] == '"':
               final.append(("write", None, None, x))
          else:
               if x[1] == "char":
                    final.append(("write", None, None, x[0]))
               else:
                    if x[0][0][0] == None:
                         final.append(("write", None, None, x[0][0][3]))
                    else:
                         final.extend(x[0])
                         final.append(("write", None, None, x[0][len(x[0])-1][3]))
     p[0] = final
     pass

def p_escritura2(p):
     '''
     escritura2 : SSTRING
                | asitipos
     '''
     p[0] = [p[1]]
     pass

def p_escritura3(p):
     '''
     escritura3 : COMA escritura2 escritura3
                | empty
     '''
     if p[1] != None:
          temp = []
          temp.extend(p[2])
          temp.extend(p[3])
          p[0] = temp
     else:
          p[0] = []
     pass

def p_desicion(p):
     'desicion : IF LPAREN expresion RPAREN THEN LPAREN2 estatutos RPAREN2 desicion2'
     temp = []
     #print("decision")
     temp.extend(p[3])
     if p[9] == None:
          temp.append(("gotof", p[3][len(p[3])-1][3], None, len(p[7])+1))
     else:
          temp.append(("gotof", p[3][len(p[3])-1][3], None, len(p[7])+2))
     temp.extend(p[7])
     if p[9] != None:
          temp.append(("goto", None, None, len(p[9])))
          temp.extend(p[9])
     p[0] = temp
     pass

def p_desicion2(p):
     '''
     desicion2 : ELSE LPAREN2 estatutos RPAREN2
               | empty
     '''
     if p[1] != None:
          p[0] = p[3]
     pass

def p_repeticion(p):
     '''
     repeticion : condicional
                | nocondicional
     '''
     p[0] = p[1]
     pass

def p_condicional(p):
     'condicional : DO LPAREN2 estatutos RPAREN2 WHILE LPAREN expresion RPAREN'
     temp = []
     temp.extend(p[3])
     temp.extend(p[7])
     temp.append(("gotof", p[7][len(p[7])-1][3], None, 2))
     temp.append(("goto", None, None, -(len(p[3]) + len(p[7]) + 1)))
     p[0] = temp
     pass

def p_condicional02(p):
     'condicional : WHILE LPAREN expresion RPAREN DO LPAREN2 estatutos RPAREN2'
     temp = []
     temp.extend(p[3])
     temp.append(("gotof", p[3][len(p[3])-1][3], None, len(p[3]) + len(p[7]) + 1))
     temp.extend(p[7])
     temp.append(("goto", None, None, -(len(p[3]) + len(p[7]) + 1)))
     p[0] = temp
     pass

def p_expresion(p):
     'expresion : comp1 expresion2'
     #print("expresion")
     #print(p[1])
     #print(p[2])
     temp = []
     temp2 = p[1]
     if p[1][0][0] != None:
          temp.extend(p[1])
     if p[2] != None:
          for x, y in p[2]:
               if y[0][0] != None:
                    temp.extend(y)
               variablesTemporales["contador"] = variablesTemporales["contador"] + 1
               varTemp = "variableSystema " + str(variablesTemporales["contador"])
               temp.append((x, temp2[len(temp2)-1][3], y[len(y)-1][3], varTemp))
               temp2 = temp
     #print("final")
     #print(temp)
     p[0] = temp
     pass

def p_expresion2(p):
     '''
     expresion2 : comp2 comp1 expresion2
                | empty
     '''
     if p[1] != None:
          #print("expresion2")
          #print(p[1])
          #print(p[2])
          #print(p[3])
          temp = [(p[1],p[2])]
          temp.extend(p[3])
          #print("final")
          #print(temp)
          p[0] = temp
     else:
          p[0] = []
     pass

def p_comp2(p):
     '''
     comp2 : AND
           | OR
     '''
     p[0] = p[1]
     pass

def p_comp1(p):
     'comp1 : asitipos comp3 asitipos'
     #print("comp1")
     #print(p[1])
     #print(p[3])
     temp = []
     last1 = ""
     last2 = ""
     if p[1][1] == "expr":
          if p[1][0][0][0] != None:
               temp.extend(p[1][0])
          last1 = p[1][0][len(p[1][0])-1][3]
     else:
          last1 = p[1][0]
     if p[3][1] == "expr":
          if p[3][0][0][0] != None:
               temp.extend(p[3][0])
          last2 = p[3][0][len(p[3][0])-1][3]
     else:
          last2 = p[3][0]
     variablesTemporales["contador"] = variablesTemporales["contador"] + 1
     varTemp = "variableSystema " + str(variablesTemporales["contador"])
     temp.append((p[2], last1, last2,varTemp))
     #print("final")
     #print(temp)
     p[0] = temp
     pass

def p_comp12(p):
     '''
     comp1 : TRUE
           | FALSE
     '''
     p[0] = [(None, None, None, p[1])]
     pass

def p_comp3(p):
     '''
     comp3 : EQ
           | GT
           | GE
           | LT
           | LE
           | NE
     '''
     p[0] = p[1]
     pass

def p_nocondicional(p):
     'nocondicional : FROM SVAR EQUAL NINT TO NINT DO LPAREN2 estatutos RPAREN2'
     temp = []
     temp.append(("=", p[4], None, p[2]))
     variablesTemporales["contador"] = variablesTemporales["contador"] + 1
     varTemp = "variableSystema " + str(variablesTemporales["contador"])
     temp.append(("<=", p[2], p[6], varTemp))
     temp.append(("gotof", varTemp, None, len(p[9]) + 4))
     temp.extend(p[9])
     variablesTemporales["contador"] = variablesTemporales["contador"] + 1
     varTemp = "variableSystema " + str(variablesTemporales["contador"])
     temp.append(("+", p[2], 1, varTemp))
     temp.append(("=", varTemp, None, p[2]))
     temp.append(("goto", None, None, -(len(p[9]) + 4)))
     p[0] = temp
     pass

def p_funespecial(p):
     '''
     funespecial : LINE LPAREN expr RPAREN PUNCOM
                 | POINT LPAREN expr COMA expr RPAREN PUNCOM
                 | CIRCLE LPAREN expr RPAREN PUNCOM
                 | ARC LPAREN expr RPAREN PUNCOM
                 | PENUP LPAREN RPAREN PUNCOM
                 | PENDOWN LPAREN RPAREN PUNCOM
                 | COLOR LPAREN expr RPAREN PUNCOM
                 | SIZE LPAREN expr RPAREN PUNCOM
                 | CLEAR LPAREN RPAREN PUNCOM
     '''
     temp = []
     param = []
     if (p[1] != "Clear" and p[1] != "PenDown" and p[1] != "PenUp"):
          if p[3][0][0] == None:
               param.append(p[3][0][3])
          else:
               temp.extend(p[3])
               param.append(p[3][len(p[3])-1][3])
          if p[1] == "Point":
               if p[5][0][0] == None:
                    param.append(p[5][0][3])
               else:
                    temp.extend(p[5])
                    param.append(p[5][len(p[5])-1][3])
     temp.append(("callf",p[1],param,None))
     p[0] = temp
     pass

def p_empty(p):
     'empty :'
     pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
yacc.yacc(debug=True)

data = '''
Program MeMySelf;
var
    int i, j, p;
    float valor;
    char exam;

module int fact (int j2, char f);
var
    int i2;
{
    i = j + (p - j * 2 + j);
    exam = 'm';
    if(j == 1 + 2 & j == 'm') then
        {if(true | false) then
          {if(true & false | true) then
          {return(j);}}}
    else
        {return(j * fact(j - 1, 'c'));}
    return(9);
}

module void pinta (int y);
var
    int x;
    float m;
{
    x = 10;
    write(x,m+1,"q");
    read(y);
    pinta(9);
    m = 1 / 2;
    while (x < 11) do
        {
            Circle(y + x * 5);
            Color(x + 10);
            Size(10 - x);
            x = x + 1;
        }
}

main()
{
    read(p,q);
    j = p * 2;
    Point(0, 0);
    i = fact(p, 'f');
    from i = 0 to 9 do
        {pinta(i * j);}
    while (i < 10) do
    {
        write("Hello World", fact(i,exam) + 1, 'l');
        i = i + 1;
    }
}
'''

# Give the lexer some input
lexer.input(data)

# Set up a logging object
import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
try:
     log = logging.getLogger()
     yacc.parse(data, debug=log)
except CalcError:
    print()
