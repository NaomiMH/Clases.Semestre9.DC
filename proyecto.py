import ply.lex as lex
import ply.yacc as yacc
import copy

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
 
tokens = ['AND','OR','LE','LT','GE','GT','EQ','NE','EQUAL','LPAREN','RPAREN','LPAREN2','RPAREN2','PUNCOM','COMA','NINT','NFLOAT','SCHAR','SSTRING','SVAR'] + list(reserved.values())

literals = [ '+','-','*','/' ]

t_AND     = r'&'
t_OR      = r'\|'
t_LE      = r'<='
t_LT      = r'<'
t_GE      = r'>='
t_GT      = r'>'
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

# Estructura para variables temporales dentro de var
# {
# "nombre_de_funcion ##": {
#    "type": "tipo de variable",
#    "value": "valor de la variable"
#    },
# "contador sys": ##
# }

# Estructura
# {
# "nombre_de_funcion" : {
#    "type": "tipo de funcion"
#    "var": {
#         "nombre_de_variable":{...}
#    },
#    "param": {
#         "nombre_de_parametro":{...}
#    },
#    "run": [(...)]
#    }
# "active sys": "nombre de funcion"
# }
# ejemplo de llamada
# variables["nombre_de_funcion"]["var"]["nombre_de_variable"]["type"]
# inicializado con la funcion main
variables = {"main":{"type":"void","param":{},"run":[],"var":{"contador sys": 0}}}

# Tabla de match
# {
# "tipo1": {
#    "tipo2": {
#         "operando": "tipo de salida"
#         }
#    }
# }
# ejemplo de llamada
# tablaTipos["tipo1"]["tipo2"]["operador"]
tablaTipos = {}

tablaTipos["int"] = {"int": {}, "float": {}, "char": {}, "bool": {}}
tablaTipos["float"] = {"int": {}, "float": {}, "char": {}, "bool": {}}
tablaTipos["char"] = {"int": {}, "float": {}, "char": {}, "bool": {}}
tablaTipos["bool"] = {"int": {}, "float": {}, "char": {}, "bool": {}}

tablaTipos["int"]["int"]["+"] = "int"
tablaTipos["int"]["int"]["-"] = "int"
tablaTipos["int"]["int"]["*"] = "int"
tablaTipos["int"]["int"]["/"] = "float"
tablaTipos["int"]["int"]["=="] = "bool"
tablaTipos["int"]["int"]["!="] = "bool"
tablaTipos["int"]["int"]["<="] = "bool"
tablaTipos["int"]["int"][">="] = "bool"
tablaTipos["int"]["int"]["<"] = "bool"
tablaTipos["int"]["int"][">"] = "bool"
tablaTipos["int"]["int"]["&"] = "error"
tablaTipos["int"]["int"]["|"] = "error"

tablaTipos["int"]["float"]["+"] = "float"
tablaTipos["int"]["float"]["-"] = "float"
tablaTipos["int"]["float"]["*"] = "float"
tablaTipos["int"]["float"]["/"] = "float"
tablaTipos["int"]["float"]["=="] = "bool"
tablaTipos["int"]["float"]["!="] = "bool"
tablaTipos["int"]["float"]["<="] = "bool"
tablaTipos["int"]["float"][">="] = "bool"
tablaTipos["int"]["float"]["<"] = "bool"
tablaTipos["int"]["float"][">"] = "bool"
tablaTipos["int"]["float"]["&"] = "error"
tablaTipos["int"]["float"]["|"] = "error"

tablaTipos["int"]["char"]["+"] = "error"
tablaTipos["int"]["char"]["-"] = "error"
tablaTipos["int"]["char"]["*"] = "error"
tablaTipos["int"]["char"]["/"] = "error"
tablaTipos["int"]["char"]["=="] = "bool"
tablaTipos["int"]["char"]["!="] = "bool"
tablaTipos["int"]["char"]["<="] = "error"
tablaTipos["int"]["char"][">="] = "error"
tablaTipos["int"]["char"]["<"] = "error"
tablaTipos["int"]["char"][">"] = "error"
tablaTipos["int"]["char"]["&"] = "error"
tablaTipos["int"]["char"]["|"] = "error"

tablaTipos["int"]["bool"]["+"] = "error"
tablaTipos["int"]["bool"]["-"] = "error"
tablaTipos["int"]["bool"]["*"] = "error"
tablaTipos["int"]["bool"]["/"] = "error"
tablaTipos["int"]["bool"]["=="] = "bool"
tablaTipos["int"]["bool"]["!="] = "bool"
tablaTipos["int"]["bool"]["<="] = "error"
tablaTipos["int"]["bool"][">="] = "error"
tablaTipos["int"]["bool"]["<"] = "error"
tablaTipos["int"]["bool"][">"] = "error"
tablaTipos["int"]["bool"]["&"] = "error"
tablaTipos["int"]["bool"]["|"] = "error"

tablaTipos["float"]["int"]["+"] = "float"
tablaTipos["float"]["int"]["-"] = "float"
tablaTipos["float"]["int"]["*"] = "float"
tablaTipos["float"]["int"]["/"] = "float"
tablaTipos["float"]["int"]["=="] = "bool"
tablaTipos["float"]["int"]["!="] = "bool"
tablaTipos["float"]["int"]["<="] = "bool"
tablaTipos["float"]["int"][">="] = "bool"
tablaTipos["float"]["int"]["<"] = "bool"
tablaTipos["float"]["int"][">"] = "bool"
tablaTipos["float"]["int"]["&"] = "error"
tablaTipos["float"]["int"]["|"] = "error"

tablaTipos["float"]["float"]["+"] = "float"
tablaTipos["float"]["float"]["-"] = "float"
tablaTipos["float"]["float"]["*"] = "float"
tablaTipos["float"]["float"]["/"] = "float"
tablaTipos["float"]["float"]["=="] = "bool"
tablaTipos["float"]["float"]["!="] = "bool"
tablaTipos["float"]["float"]["<="] = "bool"
tablaTipos["float"]["float"][">="] = "bool"
tablaTipos["float"]["float"]["<"] = "bool"
tablaTipos["float"]["float"][">"] = "bool"
tablaTipos["float"]["float"]["&"] = "error"
tablaTipos["float"]["float"]["|"] = "error"

tablaTipos["float"]["char"]["+"] = "error"
tablaTipos["float"]["char"]["-"] = "error"
tablaTipos["float"]["char"]["*"] = "error"
tablaTipos["float"]["char"]["/"] = "error"
tablaTipos["float"]["char"]["=="] = "bool"
tablaTipos["float"]["char"]["!="] = "bool"
tablaTipos["float"]["char"]["<="] = "error"
tablaTipos["float"]["char"][">="] = "error"
tablaTipos["float"]["char"]["<"] = "error"
tablaTipos["float"]["char"][">"] = "error"
tablaTipos["float"]["char"]["&"] = "error"
tablaTipos["float"]["char"]["|"] = "error"

tablaTipos["float"]["bool"]["+"] = "error"
tablaTipos["float"]["bool"]["-"] = "error"
tablaTipos["float"]["bool"]["*"] = "error"
tablaTipos["float"]["bool"]["/"] = "error"
tablaTipos["float"]["bool"]["=="] = "bool"
tablaTipos["float"]["bool"]["!="] = "bool"
tablaTipos["float"]["bool"]["<="] = "error"
tablaTipos["float"]["bool"][">="] = "error"
tablaTipos["float"]["bool"]["<"] = "error"
tablaTipos["float"]["bool"][">"] = "error"
tablaTipos["float"]["bool"]["&"] = "error"
tablaTipos["float"]["bool"]["|"] = "error"

tablaTipos["char"]["int"]["+"] = "error"
tablaTipos["char"]["int"]["-"] = "error"
tablaTipos["char"]["int"]["*"] = "error"
tablaTipos["char"]["int"]["/"] = "error"
tablaTipos["char"]["int"]["=="] = "bool"
tablaTipos["char"]["int"]["!="] = "bool"
tablaTipos["char"]["int"]["<="] = "error"
tablaTipos["char"]["int"][">="] = "error"
tablaTipos["char"]["int"]["<"] = "error"
tablaTipos["char"]["int"][">"] = "error"
tablaTipos["char"]["int"]["&"] = "error"
tablaTipos["char"]["int"]["|"] = "error"

tablaTipos["char"]["float"]["+"] = "error"
tablaTipos["char"]["float"]["-"] = "error"
tablaTipos["char"]["float"]["*"] = "error"
tablaTipos["char"]["float"]["/"] = "error"
tablaTipos["char"]["float"]["=="] = "bool"
tablaTipos["char"]["float"]["!="] = "bool"
tablaTipos["char"]["float"]["<="] = "error"
tablaTipos["char"]["float"][">="] = "error"
tablaTipos["char"]["float"]["<"] = "error"
tablaTipos["char"]["float"][">"] = "error"
tablaTipos["char"]["float"]["&"] = "error"
tablaTipos["char"]["float"]["|"] = "error"

tablaTipos["char"]["char"]["+"] = "error"
tablaTipos["char"]["char"]["-"] = "error"
tablaTipos["char"]["char"]["*"] = "error"
tablaTipos["char"]["char"]["/"] = "error"
tablaTipos["char"]["char"]["=="] = "bool"
tablaTipos["char"]["char"]["!="] = "bool"
tablaTipos["char"]["char"]["<="] = "error"
tablaTipos["char"]["char"][">="] = "error"
tablaTipos["char"]["char"]["<"] = "error"
tablaTipos["char"]["char"][">"] = "error"
tablaTipos["char"]["char"]["&"] = "error"
tablaTipos["char"]["char"]["|"] = "error"

tablaTipos["char"]["bool"]["+"] = "error"
tablaTipos["char"]["bool"]["-"] = "error"
tablaTipos["char"]["bool"]["*"] = "error"
tablaTipos["char"]["bool"]["/"] = "error"
tablaTipos["char"]["bool"]["=="] = "bool"
tablaTipos["char"]["bool"]["!="] = "bool"
tablaTipos["char"]["bool"]["<="] = "error"
tablaTipos["char"]["bool"][">="] = "error"
tablaTipos["char"]["bool"]["<"] = "error"
tablaTipos["char"]["bool"][">"] = "error"
tablaTipos["char"]["bool"]["&"] = "error"
tablaTipos["char"]["bool"]["|"] = "error"

tablaTipos["bool"]["int"]["+"] = "error"
tablaTipos["bool"]["int"]["-"] = "error"
tablaTipos["bool"]["int"]["*"] = "error"
tablaTipos["bool"]["int"]["/"] = "error"
tablaTipos["bool"]["int"]["=="] = "bool"
tablaTipos["bool"]["int"]["!="] = "bool"
tablaTipos["bool"]["int"]["<="] = "error"
tablaTipos["bool"]["int"][">="] = "error"
tablaTipos["bool"]["int"]["<"] = "error"
tablaTipos["bool"]["int"][">"] = "error"
tablaTipos["bool"]["int"]["&"] = "error"
tablaTipos["bool"]["int"]["|"] = "error"

tablaTipos["bool"]["float"]["+"] = "error"
tablaTipos["bool"]["float"]["-"] = "error"
tablaTipos["bool"]["float"]["*"] = "error"
tablaTipos["bool"]["float"]["/"] = "error"
tablaTipos["bool"]["float"]["=="] = "bool"
tablaTipos["bool"]["float"]["!="] = "bool"
tablaTipos["bool"]["float"]["<="] = "error"
tablaTipos["bool"]["float"][">="] = "error"
tablaTipos["bool"]["float"]["<"] = "error"
tablaTipos["bool"]["float"][">"] = "error"
tablaTipos["bool"]["float"]["&"] = "error"
tablaTipos["bool"]["float"]["|"] = "error"

tablaTipos["bool"]["char"]["+"] = "error"
tablaTipos["bool"]["char"]["-"] = "error"
tablaTipos["bool"]["char"]["*"] = "error"
tablaTipos["bool"]["char"]["/"] = "error"
tablaTipos["bool"]["char"]["=="] = "bool"
tablaTipos["bool"]["char"]["!="] = "bool"
tablaTipos["bool"]["char"]["<="] = "error"
tablaTipos["bool"]["char"][">="] = "error"
tablaTipos["bool"]["char"]["<"] = "error"
tablaTipos["bool"]["char"][">"] = "error"
tablaTipos["bool"]["char"]["&"] = "error"
tablaTipos["bool"]["char"]["|"] = "error"

tablaTipos["bool"]["bool"]["+"] = "error"
tablaTipos["bool"]["bool"]["-"] = "error"
tablaTipos["bool"]["bool"]["*"] = "error"
tablaTipos["bool"]["bool"]["/"] = "error"
tablaTipos["bool"]["bool"]["=="] = "bool"
tablaTipos["bool"]["bool"]["!="] = "bool"
tablaTipos["bool"]["bool"]["<="] = "error"
tablaTipos["bool"]["bool"][">="] = "error"
tablaTipos["bool"]["bool"]["<"] = "error"
tablaTipos["bool"]["bool"][">"] = "error"
tablaTipos["bool"]["bool"]["&"] = "bool"
tablaTipos["bool"]["bool"]["|"] = "bool"

def buscaTipo(tipo):
     if type(tipo) == type(1):
          return "int"
     elif type(tipo) == type(1.0):
          return "float"
     elif tipo[0] == "'":
          return "char"
     elif tipo[0] == '"':
          return "str"
     elif (tipo == "true" or tipo == "false"):
          return "bool"
     elif variables["main"]["var"].get(tipo) != None:
          return variables["main"]["var"][tipo]["type"]
     elif variables["active sys"] != "main":
          if variables[variables["active sys"]]["var"].get(tipo) != None:
               return variables[variables["active sys"]]["var"][tipo]["type"]
          elif variables[variables["active sys"]]["param"].get(tipo) != None:
               return variables[variables["active sys"]]["param"][tipo]["type"]
     print("ERROR: Variable no encontrada")
     raise CalcError("Variable invalida")

def buscaVariable(temparam,tempvar,var):
     if variables["main"]["var"].get(var) != None:
          return variables["main"]["var"][var]
     elif variables["active sys"] != "main":
          if tempvar.get(var) != None:
               return tempvar[var]
          elif temparam.get(var) != None:
               return temparam[var]
     elif (type(var) == type(1) or type(var) == type(1.0) or var[0] == "'" or var[0] == '"' or var == "true" or var == "false"):
          return "constante"
     print("ERROR: Variable no encontrada")
     raise CalcError("Variable invalida")

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

# checar que las funciones que no son void, tengan un return

def op(op,opdo1,opdo2):
     if op == '*':
          return opdo1 * opdo2
     elif op == '/':
          return opdo1 / opdo2
     elif op == '-':
          return opdo1 - opdo2
     elif op == '+':
          return opdo1 + opdo2
     elif op == '==':
          return opdo1 == opdo2
     elif op == '<':
          return opdo1 < opdo2
     elif op == '>':
          return opdo1 > opdo2
     elif op == '<=':
          return opdo1 <= opdo2
     elif op == '>=':
          return opdo1 >= opdo2
     elif op == '!=':
          return opdo1 != opdo2
     elif op == '&':
          return opdo1 and opdo2
     elif op == '|':
          return opdo1 or opdo2
     else:
          print("ERROR: OP01")
          raise CalcError("Error en sistema")


def call(function,param,var):
     contador = 0
     while contador < len(variables[function]["run"]):
          a = variables[function]["run"][contador][0]
          b = variables[function]["run"][contador][1]
          c = variables[function]["run"][contador][2]
          d = variables[function]["run"][contador][3]
          print(contador + 1, ":", a, "|", b, "|", c, "|", d)
          if a == "read":
               vard = buscaVariable(param,var,d)
               vard["value"] = read(vard["type"])
          elif (a == '*' or a == '/' or a == '-' or a == '+' or a == '==' or a == '>' or a == '<' or a == '<=' or a == '>=' or a == '!=' or a == '&' or a == '|'):
               varb = buscaVariable(param,var,b)
               if varb.get("value") == None:
                    print("ERROR: Variable no inicializada")
                    raise CalcError("Expresion invalida")
               varc = buscaVariable(param,var,c)
               if varc.get("value") == None:
                    print("ERROR: Variable no inicializada")
                    raise CalcError("Expresion invalida")
               vard = buscaVariable(param,var,d)
               vard["value"] = op(a,varb["value"],varc["value"])
          elif a == '=':
               varb = buscaVariable(param,var,b)
               if varb.get("value") == None:
                    print("ERROR: Variable no inicializada")
                    raise CalcError("Expresion invalida")
               vard = buscaVariable(param,var,d)
               vard["value"] = varb["value"]
          elif a == "callr" or a == "call":
               variables["active sys"] = b
               tparam = copy.deepcopy(variables[b]["param"])
               tcont = 0
               for x in tparam:
                    varc = buscaVariable(param,var,c[tcont])
                    print(varc)
                    if varc.get("value") == None:
                         print("ERROR: Variable no inicializada")
                         raise CalcError("Expresion invalida")
                    tparam[x]["value"] = varc["value"]
                    tcont = tcont + 1
               if a == "callr":
                    temp = call(b,tparam,copy.deepcopy(variables[b]["var"]))
                    variables["active sys"] = function
                    if temp == "Sys None":
                         print("ERROR: No llego a un return la funcion")
                         raise CalcError("Estatuto faltante")
                    else:
                         vard = buscaVariable(param,var,d)
                         vard["value"] = temp
               else:
                    call(b,tparam,copy.deepcopy(variables[b]["var"]))
                    variables["active sys"] = function
          elif a == "gotof":
               varb = buscaVariable(param,var,b)
               if varb["value"] == False:
                    contador = contador + d - 1
          elif a == "goto":
               contador = contador + d - 1
          elif a == "return":
               vard = buscaVariable(param,var,d)
               if vard.get("value") == None:
                    print("ERROR: Variable no inicializada")
                    raise CalcError("Expresion invalida")
               return vard["value"]
          elif a == "write":
               vard = buscaVariable(param,var,d)
               if vard.get("value") == None:
                    print("ERROR: Variable no inicializada")
                    raise CalcError("Expresion invalida")
               print(vard["value"])
          elif a != "callf":
               print("ERROR: CALL01")
               raise CalcError("Error en sistema")
          contador = contador + 1
     return "Sys None"

def read(tipo):
     if tipo == "int":
          return int(input())
     elif tipo == "float":
          return float(input())
     elif tipo == "char":
          inputTemp = str(input())
          if len(inputTemp) != 1:
               print("ERROR: Longitud de caracter mayor a 1")
               raise CalcError("Input invalido")
          return inputTemp
     print("ERROR: READ01")
     raise CalcError("Error en sistema")

def run():
     variables["active sys"] = "main"
     call("main",variables["main"]["param"],variables["main"]["var"])
     print("Run!!")

def p_program(p):
     'program : programInicio decvar decfuntemp programMain'
     for funcion in variables:
          if funcion != "active sys":
               print("*** ", funcion)
               variables["active sys"] = funcion
               contador = 1
               for a,b,c,d in variables[funcion]["run"]:
                    print(contador, ":", a, "|", b, "|", c, "|", d)
                    contador = contador + 1
                    if (a == '+' or a == '-' or a == '*' or a == '/' or a == '==' or a == '!=' or a == '<=' or a == '>=' or a == '<' or a == '>' or a == '&' or a == '|'):
                         tb = buscaTipo(b)
                         tc = buscaTipo(c)
                         if tablaTipos[tb][tc][a] == "error":
                              print("ERROR: Tipos de valores invalidos")
                              raise CalcError("Expresion invalida")
                         variables[variables["active sys"]]["var"][d] = {"type": tablaTipos[tb][tc][a]}
                    elif a == "gotof":
                         if buscaTipo(b) != "bool":
                              print("ERROR: Error en compilacion")
                              raise CalcError("Expresion invalida")
                    elif a == "=":
                         tb = buscaTipo(b)
                         td = buscaTipo(d)
                         if (tb != td and (tb == "int" and td != "float")):
                              print("ERROR: Tipo de variable invalido en asignacion")
                              raise CalcError("Estatuto invalido")
                    elif a == "return":
                         if variables[variables["active sys"]]["type"] == "void":
                              print("ERROR: Return en funcion void")
                              raise CalcError("Estatuto invalido")
                         elif variables[variables["active sys"]]["type"] != buscaTipo(d):
                              print("ERROR: Tipo de return invalido")
                              raise CalcError("Estatuto invalido")
                    elif a == "callr":
                         if variables.get(b) == None:
                              print("ERROR: Llamada a funcion invalida")
                              raise CalcError("Estatuto invalido")
                         if variables[b]["type"] == "void":
                              print("ERROR: Llamada con return a funcion void")
                              raise CalcError("Estatuto invalido")
                         else:
                              variables[variables["active sys"]]["var"][d] = {"type": variables[b]["type"]}
                         if len(variables[b]["param"]) != len(c):
                              print("ERROR: Cantidad de parametros invalido")
                              raise CalcError("Estatuto invalido")
                         cont = 0
                         for param in variables[b]["param"]:
                              tc = buscaTipo(c[cont])
                              if (variables[b]["param"][param]["type"] != tc and (variables[b]["param"][param]["type"] == "int" and tc != "float")):
                                   print("ERROR: Tipo de parametro esperado invalido en return")
                                   raise CalcError("Estatuto invalido")
                              cont = cont + 1
                    elif a == "call":
                         if variables.get(b) == None:
                              print("ERROR: Llamada a funcion invalida")
                              raise CalcError("Estatuto invalido")
                         if variables[b]["type"] != "void":
                              print("ERROR: Llamada a funcion con return en llamada void")
                              raise CalcError("Estatuto invalido")
                         elif b == "main":
                              print("ERROR: Llamada a main")
                              raise CalcError("Estatuto invalido")
                         if len(variables[b]["param"]) != len(c):
                              print("ERROR: Cantidad de parametros invalido")
                              raise CalcError("Estatuto invalido")
                         cont = 0
                         for param in variables[b]["param"]:
                              tc = buscaTipo(c[cont])
                              if (variables[b]["param"][param]["type"] != tc and (variables[b]["param"][param]["type"] == "int" and tc != "float")):
                                   print("ERROR: Tipo de parametro esperado invalido en return")
                                   raise CalcError("Estatuto invalido")
                              cont = cont + 1
                    elif a == "read" or a == "write":
                         buscaTipo(d)
                    elif (a != "callf" and a != "goto"):
                         print("ERROR: PROGRAM01")
                         raise CalcError("Error en sistema")
     print("Compile!!")
     run()

def p_decfuntemp(p):
     'decfuntemp : decfunCodigo decfuntemp'
     pass

def p_decfuntemp02(p):
     'decfuntemp : empty'
     pass

def p_programMain(p):
     'programMain : programMainIni LPAREN2 estatutos RPAREN2'
     variables["main"]["run"] = p[3]
     pass

def p_programMainIni(p):
     'programMainIni : MAIN LPAREN RPAREN'
     variables["active sys"] = "main"
     pass

def p_programInicio(p):
     'programInicio : PROGRAM SVAR PUNCOM'
     variables["active sys"] = "main"
     pass

def p_decvar(p):
     '''
     decvar : VAR decvar2
            | empty
     '''
     pass

def p_decvar2(p):
     '''
     decvar2 : tipo SVAR nomvar decvar2
             | empty
     '''
     if p[1] != None:
          temp = [p[2]]
          temp.extend(p[3])
          for x in temp:
               if variables["main"]["var"].get(x) != None:
                    print("ERROR: Nombre de variable repetido, variable global declarada")
                    raise CalcError("Variable repetida")
               if variables["active sys"] != "main":
                    if variables[variables["active sys"]]["param"].get(x) != None:
                         print("ERROR: Nombre de variable repetido, parametro de funcion declarada")
                         raise CalcError("Variable repetida")
                    if variables[variables["active sys"]]["var"].get(x) != None:
                         print("ERROR: Nombre de variable repetido, variable de funcion declarada")
                         raise CalcError("Variable repetida")
               variables[variables["active sys"]]["var"][x] = {"type": p[1]}
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

def p_decfunCodigo(p):
     'decfunCodigo : decfunCodigoIni LPAREN funpara RPAREN PUNCOM decvar LPAREN2 estatutos RPAREN2'
     variables[variables["active sys"]]["run"] = p[8]
     pass
     

def p_decfunCodigoIni(p):
     'decfunCodigoIni : MODULE funtipo SVAR'
     nombre = p[3]
     funtipo = p[2]
     if variables.get(nombre) != None:
          print("ERROR: Nombre de funcion invalido")
          raise CalcError("funcion repetida")
     variables[nombre] = {}
     variables[nombre]["type"] = funtipo
     variables[nombre]["param"] = {}
     variables[nombre]["run"] = []
     variables[nombre]["var"] = {}
     variables[nombre]["var"]["contador sys"] = 0
     variables["active sys"] = nombre
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
          temp = [(p[1], p[2])]
          temp.extend(p[3])
          for tipo, param in temp:
               if variables["main"]["var"].get(param) != None:
                    print("ERROR: Nombre de parametro invalido")
                    raise CalcError("Variable repetida")
               if variables[variables["active sys"]]["param"].get(param) != None:
                    print("ERROR: Nombre de parametro invalido")
                    raise CalcError("Variable repetida")
               variables[variables["active sys"]]["param"][param] = {"type": tipo}
     pass

def p_funpara2(p):
     '''
     funpara2 : COMA tipo SVAR funpara2
              | empty
     '''
     if p[1] != None:
          temp = [(p[2], p[3])]
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
     # print("***** BANDERA ******")
     # print(p[1])
     # print("********************")

     temp = []
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
     variables[variables["active sys"]]["var"]["contador sys"] = variables[variables["active sys"]]["var"]["contador sys"] + 1
     varTemp = variables["active sys"] + " " + str(variables[variables["active sys"]]["var"]["contador sys"])
     variables[variables["active sys"]]["var"][varTemp] = {"type": "char","value": p[1][1]}
     p[0] = (varTemp,"char")
     pass

def p_expr(p):
     'expr : exprCode'
     pila = []
     final = []
     for x in p[1]:
          if ( x == '+' or x == '-' or x == '*' or x == '/'):
               y = pila.pop()
               z = pila.pop()
               variables[variables["active sys"]]["var"]["contador sys"] = variables[variables["active sys"]]["var"]["contador sys"] + 1
               varTemp = variables["active sys"] + " " + str(variables[variables["active sys"]]["var"]["contador sys"])
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
                    variables[variables["active sys"]]["var"]["contador sys"] = variables[variables["active sys"]]["var"]["contador sys"] + 1
                    varTemp = variables["active sys"] + " " + str(variables[variables["active sys"]]["var"]["contador sys"])
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
     'exprCode : expr1 exprCodeT'
     temp = p[1]
     temp.extend(p[2])
     p[0] = temp
     pass

def p_exprCode02(p):
     '''
     exprCodeT : '+' expr1 exprCodeT
               | '-' expr1 exprCodeT
     '''
     temp = []
     temp.extend(p[2])
     temp.append(p[1])
     temp.extend(p[3])
     p[0] = temp
     pass

def p_exprCode03(p):
     'exprCodeT : empty'
     p[0] = []
     pass

def p_expr1(p):
     'expr1 : expr2 expr1T'
     temp = p[1]
     temp.extend(p[2])
     p[0] = temp
     pass

def p_expr12(p):
     '''
     expr1T : '*' expr2 expr1T
            | '/' expr2 expr1T
     '''
     temp = []
     temp.extend(p[2])
     temp.append(p[1])
     temp.extend(p[3])
     p[0] = temp
     pass

def p_expr13(p):
     'expr1T : empty'
     p[0] = []
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
     'term : NINT'
     variables[variables["active sys"]]["var"]["contador sys"] = variables[variables["active sys"]]["var"]["contador sys"] + 1
     varTemp = variables["active sys"] + " " + str(variables[variables["active sys"]]["var"]["contador sys"])
     variables[variables["active sys"]]["var"][varTemp] = {"type": "int","value": p[1]}
     p[0] = varTemp
     pass

def p_term02(p):
     'term : NFLOAT'
     variables[variables["active sys"]]["var"]["contador sys"] = variables[variables["active sys"]]["var"]["contador sys"] + 1
     varTemp = variables["active sys"] + " " + str(variables[variables["active sys"]]["var"]["contador sys"])
     variables[variables["active sys"]]["var"][varTemp] = {"type": "int","value": p[1]}
     p[0] = varTemp
     pass

def p_term01(p):
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
     'escritura2 : SSTRING'
     variables[variables["active sys"]]["var"]["contador sys"] = variables[variables["active sys"]]["var"]["contador sys"] + 1
     varTemp = variables["active sys"] + " " + str(variables[variables["active sys"]]["var"]["contador sys"])
     variables[variables["active sys"]]["var"][varTemp] = {"type": "string","value": p[1].replace('"', '')}
     p[0] = [([(None, None, None, varTemp)], 'expr')]
     pass

def p_escritura22(p):
     'escritura2 : asitipos'
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
     temp = []
     temp2 = p[1]
     if p[1][0][0] != None:
          temp.extend(p[1])
     if p[2] != None:
          for x, y in p[2]:
               if y[0][0] != None:
                    temp.extend(y)
               variables[variables["active sys"]]["var"]["contador sys"] = variables[variables["active sys"]]["var"]["contador sys"] + 1
               varTemp = variables["active sys"] + " " + str(variables[variables["active sys"]]["var"]["contador sys"])
               temp.append((x, temp2[len(temp2)-1][3], y[len(y)-1][3], varTemp))
               temp2 = temp
     p[0] = temp
     pass

def p_expresion2(p):
     '''
     expresion2 : comp2 comp1 expresion2
                | empty
     '''
     if p[1] != None:
          temp = [(p[1],p[2])]
          temp.extend(p[3])
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
     variables[variables["active sys"]]["var"]["contador sys"] = variables[variables["active sys"]]["var"]["contador sys"] + 1
     varTemp = variables["active sys"] + " " + str(variables[variables["active sys"]]["var"]["contador sys"])
     temp.append((p[2], last1, last2,varTemp))
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
     'nocondicional : FROM SVAR EQUAL expr TO expr DO LPAREN2 estatutos RPAREN2'
     temp = []
     if p[4][0][0] != None:
          temp.extend(p[4])
     temp.append(("=", p[4][len(p[4])-1][3], None, p[2]))
     if p[6][0][0] != None:
          temp.extend(p[6])
     variables[variables["active sys"]]["var"]["contador sys"] = variables[variables["active sys"]]["var"]["contador sys"] + 1
     varTemp = variables["active sys"] + " " + str(variables[variables["active sys"]]["var"]["contador sys"])
     temp.append(("<=", p[2], p[6][len(p[6])-1][3], varTemp))
     temp.append(("gotof", varTemp, None, len(p[9]) + 4))
     temp.extend(p[9])
     variables[variables["active sys"]]["var"]["contador sys"] = variables[variables["active sys"]]["var"]["contador sys"] + 1
     varTemp = variables["active sys"] + " " + str(variables[variables["active sys"]]["var"]["contador sys"])
     variables[variables["active sys"]]["var"]["contador sys"] = variables[variables["active sys"]]["var"]["contador sys"] + 1
     varTemp2 = variables["active sys"] + " " + str(variables[variables["active sys"]]["var"]["contador sys"])
     variables[variables["active sys"]]["var"][varTemp2] = {"type": "int", "value": 1}
     temp.append(("+", p[2], varTemp2, varTemp))
     temp.append(("=", varTemp, None, p[2]))
     temp.append(("goto", None, None, -(len(p[9]) + len(p[6]) + 4)))
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
    int i, j, p, q;
    float valor;
    char exam;

module int fact (int j2, char f);
var
    int i2;
{
    i2 = j2 + (j2 * 2);
    if(j2 == 1) then
        {return(j2);}
    else
        {return(j2 * fact(j2 - 1, 'c'));}
    return(9);
}

module void pinta (int y);
var
    int x;
    float m;
{
    x = 10;
    m = 1 / 2;
    write(x,m+1,"q");
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
    exam = 'm';
    Point(0, 0);
    i = fact(p, 'f');
    from i = 0 + 3 to 9 - 1 do
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
