import ply.lex as lex
import ply.yacc as yacc

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

def p_program(p):
     'program : PROGRAM SVAR PUNCOM decvar decfun MAIN LPAREN RPAREN LPAREN2 estatutos RPAREN2'
     print("Compile!!")

def p_decvar(p):
     'decvar : VAR tipo SVAR nomvar decvar2'
     pass

def p_decvar2(p):
     '''
     decvar2 : tipo SVAR nomvar decvar2
             | empty
     '''
     pass

def p_nomvar(p):
     '''
     nomvar : COMA SVAR nomvar
            | PUNCOM
     '''
     pass

def p_tipo(p):
     '''
     tipo : INT
          | FLOAT
          | CHAR
     '''
     pass

def p_decfun(p):
     'decfun : MODULE funtipo SVAR LPAREN funpara RPAREN PUNCOM decvar LPAREN2 estatutos RPAREN2 decfun2'
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
     pass

def p_funpara(p):
     '''
     funpara : tipo SVAR funpara2
             | empty
     '''
     pass

def p_funpara2(p):
     '''
     funpara2 : COMA tipo SVAR funpara2
              | empty
     '''
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
     pass

def p_asignacion(p):
     'asignacion : SVAR EQUAL asitipos PUNCOM'
     pass

def p_asitipos(p):
     '''
     asitipos : expr
              | SCHAR
     '''
     pass

def p_expr(p):
     '''
     expr : expr1 '+' expr
          | expr1 '-' expr
          | expr1
     '''
     pass

def p_expr1(p):
     '''
     expr1 : expr2 '*' expr1
           | expr2 '/' expr1
           | expr2
     '''
     pass

def p_expr2(p):
     '''
     expr2 : LPAREN expr RPAREN
           | term
     '''
     pass

def p_term(p):
     '''
     term : SVAR posfun
          | NINT
          | NFLOAT
     '''
     pass

def p_posfun(p):
     '''
     posfun : LPAREN parametros RPAREN
            | empty
     '''
     pass

def p_parametros(p):
     '''
     parametros : asitipos parametros2
                | empty
     '''
     pass

def p_parametros2(p):
     '''
     parametros2 : COMA asitipos parametros2
                 | empty
     '''
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
     'condicional : WHILE LPAREN expresion RPAREN DO LPAREN2 estatutos RPAREN2'
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

module int fact (int j);
var
    int i;
{
    i = j + (p - j * 2 + j);
    if(j == 1) then
        {return(j);}
    else
        {return(j * fact(j - 1));}
}

module void pinta (int y);
var
    int x;
{
    x = 1;
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
    read(p);
    j = p * 2;
    Point(0, 0);
    i = fact(p);
    from i = 0 to 9 do
        {pinta(i * j);}
    while (i < 10) do
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
log = logging.getLogger()
yacc.parse(data, debug=log)