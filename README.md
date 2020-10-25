# Clases.Semestre9.DC
Clase: Diseño de compiladores

## Informacion
Lenguaje: PLY y Python

## Avance 1
8 de octubre 2020

### Entrega
Archivo .py con el lexico y la sintaxis funcionando.

Checar el archivo GramaticaActual.

### Diferencias entre la GramaticaInicial y GramaticaActual
- Las funciones se inicializan con "module \<tipo de retorno> nombre_modulo" en lugar de "\<tipo de retorno> module nombre_modulo"

### Ejemplo de codigo de entrada

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

## Avance 2
14 de octubre 2020

### Entrega
Semántica básica

### Avance
- Las variables son guardadas por globales y funciones, las variables de funciones no pueden repetirse entre las variables globales

- Los parametros de funciones son guardados, los parametros de funciones no pueden repetirse entre las variables globales y las variables de funciones no pueden repetirse entre los parametros de dicha funcion

- Las funciones son guardadas con su variables y parametros correspondientes

- Las ecuaciones son transformadas en un arreglo de instrucciones en forma de cuadruplos

- Las asignaciones tienen todas sus instrucciones correspondientes

### Ejemplo de codigo de entrada

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

## Avance 3
24 de octubre 2020

### Entrega
Generación de código intermedio inicial

### Avance
- Se agregaron los tokens: '>=', '!=' y '<='

- Las variables del sistema ahora tienen un espacio entre el nombre y su numero. Esto ayuda a que el usuario no pueda por accidente crear una variable con el mismo nombre que una variable del sistema, ya que las variables del usuario son sin espacios.

- Se establecieron las estructuras que ira generando el programa en forma de cuadruplos.

- Todos los estatutos mandan su arreglo de instrucciones completo en el formato requerido.

- El arreglo de instrucciones del main es checado en busca de errores de semantica estatica.

- El arreglo de instrucciones de cada funcion es checado en busca de errores de semantica estatica.

- Se considero que el usuario puede no declarar variables.

### Diferencias entre la GramaticaInicial y GramaticaActual
- Se agrego la repeticion condicional While Do.

### Ejemplo de codigo de entrada

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
