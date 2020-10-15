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
 
tokens = ['AND','OR','LT','GT','EQ','EQUAL','LPAREN','RPAREN','LPAREN2','RPAREN2','PUNCOM','COMA','NINT','NFLOAT','SCHAR','SSTRING','SVAR'] + list(reserved.values())

literals = [ '+','-','*','/' ]

t_AND     = r'&'
t_OR      = r'\|'
t_LT      = r'<'
t_GT      = r'>'
t_EQ      = r'=='
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
# variablesTemporales["variableSystema##"]["type"]
variablesTemporales = {"contador": 0}

def p_program(p):
     'program : programInicio decfuntemp programMain'
     print("Compile!!")

# Solo sirve para imprimir una vez variablesFunciones, recordar borrar.
def p_decfuntemp(p):
     'decfuntemp : decfun'
     print(variablesFunciones)
     pass

def p_programMain(p):
     'programMain : MAIN LPAREN RPAREN LPAREN2 estatutos RPAREN2'
     #acciones = p[5]
     pass

def p_programInicio(p):
     'programInicio : PROGRAM SVAR PUNCOM decvar'
     lista = p[4]
     for x in lista:
          variables = x[1]
          tipo = x[0]
          for var in variables:
               if (variablesGlobales.get(var)==None):
                    variablesGlobales[var]={"type":tipo}
               else:
                    print("ERROR: Nombre de variable global invalido")
                    raise CalcError("Variable repetida")
     print("Variables globales")
     print(variablesGlobales)
     pass

def p_decvar(p):
     'decvar : VAR tipo SVAR nomvar decvar2'
     temp=[p[3]]
     temp.extend(p[4])
     temp2=[[p[2],temp]]
     temp2.extend(p[5])
     p[0]=temp2
     pass

def p_decvar2(p):
     '''
     decvar2 : tipo SVAR nomvar decvar2
             | empty
     '''
     if p[1] == None:
          p[0]=[]
     else:
          temp=[p[2]]
          temp.extend(p[3])
          temp2=[[p[1],temp]]
          temp2.extend(p[4])
          p[0]=temp2
     pass

def p_nomvar(p):
     '''
     nomvar : COMA SVAR nomvar
            | PUNCOM
     '''
     if p[1] != ';':
          temp=[p[2]]
          temp.extend(p[3])
          p[0]=temp
     else:
          p[0]=[]
     pass

def p_tipo(p):
     '''
     tipo : INT
          | FLOAT
          | CHAR
     '''
     p[0]=p[1]

def p_decfun(p):
     'decfun : decfunCodigo decfun2'
     pass

def p_decfunCodigo(p):
     'decfunCodigo : decfunCodigoIni LPAREN2 estatutos RPAREN2'
     #nombre = p[1]
     #acciones = p[3]
     pass
     

def p_decfunCodigoIni(p):
     'decfunCodigoIni : MODULE funtipo SVAR LPAREN funpara RPAREN PUNCOM decvar'
     nombre = p[3]
     funtipo = p[2]
     listaParametros = p[5]
     listaVariables = p[8]
     if (variablesFunciones.get(nombre)==None):
          variablesFunciones[nombre]={}
          variablesFunciones[nombre]["type"]=funtipo
          variablesFunciones[nombre]["param"]={}
          for x in listaParametros:
               variable = x[1]
               tipo = x[0]
               if (variablesGlobales.get(variable)!=None):
                    print("ERROR: Nombre de variable de parametro invalido por variable global")
                    raise CalcError("Variable repetida")
               elif (variablesFunciones[nombre]["param"].get(variable)!=None):
                    print("ERROR: Nombre de variable de parametro invalido")
                    raise CalcError("Variable repetida")
               else:
                    variablesFunciones[nombre]["param"][variable]={"type":tipo}
          variablesFunciones[nombre]["var"]={}
          for x in listaVariables:
               variables = x[1]
               tipo = x[0]
               for var in variables:
                    if (variablesGlobales.get(var)!=None):
                         print("ERROR: Nombre de variable de funcion invalido por variable global")
                         raise CalcError("Variable repetida")
                    elif (variablesFunciones[nombre]["param"].get(var)!=None):
                         print("ERROR: Nombre de variable de funcion invalido por variable de parametro")
                         raise CalcError("Variable repetida")
                    elif (variablesFunciones[nombre]["var"].get(var)!=None):
                         print("ERROR: Nombre de variable de funcion invalido")
                         raise CalcError("Variable repetida")
                    else:
                         variablesFunciones[nombre]["var"][var]={"type":tipo}
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
     p[0]=p[1]
     pass

def p_funpara(p):
     '''
     funpara : tipo SVAR funpara2
             | empty
     '''
     if p[1] != None:
          temp = [[p[1],p[2]]]
          temp.extend(p[3])
          p[0]=temp
     else:
          p[0]=[]
     pass

def p_funpara2(p):
     '''
     funpara2 : COMA tipo SVAR funpara2
              | empty
     '''
     if p[1] != None:
          temp = [[p[2],p[3]]]
          temp.extend(p[4])
          p[0]=temp
     else:
          p[0]=[]
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
               | retorno
               | empty
     '''
     #print("***** BANDERA ******")
     #print(p[1])
     #print("********************")
     pass

def p_asignacion(p):
     'asignacion : SVAR EQUAL asitipos PUNCOM'
     final = []
     if p[3][1] == "expr":
          if p[3][0][0] != None:
               final.extend(p[3][0])
          final.append( ('=', p[3][0][len(p[3][0])-1][3], None, p[1]) )
     else:
          final.append( ('=', p[3][0], None, p[1]) )
     p[0] = final
     pass

def p_asitipos(p):
     'asitipos : expr'
     p[0]=(p[1],"expr")
     pass

def p_asitipos02(p):
     'asitipos : SCHAR'
     p[0]=(p[1][1],"char")
     pass

# falta comprobar si son ints o floats para saber el tipo de la variable temporal
# y despues crear la variable temporal
# checar el tipo del return de la funcion
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
     temp=p[1]
     temp.extend(p[3])
     temp.append(p[2])
     p[0]=temp
     pass

def p_expr02(p):
     'exprCode : expr1'
     p[0]=p[1]
     pass

def p_expr1(p):
     '''
     expr1 : expr2 '*' expr1
           | expr2 '/' expr1
     '''
     temp=p[1]
     temp.extend(p[3])
     temp.append(p[2])
     p[0]=temp
     pass

def p_expr12(p):
     'expr1 : expr2'
     p[0]=p[1]
     pass

def p_expr2(p):
     '''
     expr2 : LPAREN exprCode RPAREN
           | term
     '''
     if p[1] != '(':
          p[0]=[p[1]]
     else:
          p[0]=p[2]
     pass

def p_term(p):
     '''
     term : NINT
          | NFLOAT
     '''
     p[0] = p[1]
     pass

# Si posfun no es vacio, hay que checar que los parametros sean los correctos.
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
          p[0]=temp
     else:
          p[0]=[]
     pass

def p_parametros2(p):
     '''
     parametros2 : COMA asitipos parametros2
                 | empty
     '''
     if p[1] != None:
          temp = [p[2]]
          temp.extend(p[3])
          p[0]=temp
     else:
          p[0]=[]
     pass

def p_llamada(p):
     'llamada : SVAR LPAREN parametros RPAREN PUNCOM'
     pass

def p_retorno(p):
     'retorno : RETURN LPAREN asitipos RPAREN PUNCOM'
     pass

def p_lectura(p):
     'lectura : READ LPAREN SVAR lectura2 RPAREN PUNCOM'
     pass

def p_lectura2(p):
     '''
     lectura2 : COMA SVAR lectura2
              | empty
     '''
     pass

def p_escritura(p):
     'escritura : WRITE LPAREN escritura2 escritura3 RPAREN PUNCOM'
     pass

def p_escritura2(p):
     '''
     escritura2 : SSTRING
                | asitipos
     '''
     pass

def p_escritura3(p):
     '''
     escritura3 : COMA escritura2
                | empty
     '''
     pass

def p_desicion(p):
     'desicion : IF LPAREN expresion RPAREN THEN LPAREN2 estatutos RPAREN2 desicion2'
     pass

def p_desicion2(p):
     '''
     desicion2 : ELSE LPAREN2 estatutos RPAREN2
               | empty
     '''
     pass

def p_repeticion(p):
     '''
     repeticion : condicional
                | nocondicional
     '''
     pass

def p_condicional(p):
     'condicional : DO LPAREN expresion RPAREN WHILE LPAREN2 estatutos RPAREN2'
     pass

def p_expresion(p):
     'expresion : comp1 expresion2'
     pass

def p_expresion2(p):
     '''
     expresion2 : comp2 comp1 expresion2
                | empty
     '''
     pass

def p_comp2(p):
     '''
     comp2 : AND
           | OR
     '''
     pass

def p_comp1(p):
     'comp1 : comp comp3 comp'
     pass

def p_comp3(p):
     '''
     comp3 : EQ
           | GT
           | LT
     '''
     pass

def p_comp(p):
     '''
     comp : TRUE
          | FALSE
          | expr
     '''
     pass

def p_nocondicional(p):
     'nocondicional : FROM SVAR EQUAL NINT TO NINT DO LPAREN2 estatutos RPAREN2'
     pass

def p_empty(p):
     'empty :'
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

module int fact (int j2, char f);
var
    int i2;
{
    i = j + (p - j * 2 + j);
    valor = 'm';
    if(j == 1) then
        {return(j);}
    else
        {return(j * fact(j - 1, 'c'));}
}

module void pinta (int y);
var
    int x;
{
    x = 1;
    do (x < 11) while
        {
            Circle(y + x * 5);
            Color(x + 10);
            Size(10 - x);
            x = x + 1;
        }
}

main()
{
    read(p);
    j = p * 2;
    Point(0, 0);
    i = fact(p);
    from i = 0 to 9 do
        {pinta(i * j);}
    do (i < 10) while
    {
        write("Hello World", fact(i));
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
