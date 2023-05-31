import networkx as nx
import random

def crea_grafo_unidireccional(n,m):
    """
    Crea grafo con todas las rutas posibles
    (tipo cuadrilla), que es representado
    como un diccionario.
    
    Parametros:
        n (Entero):cantidad de valores del grafo de alto
        m (Entero):cantidad de valores del grafo de ancho
    
    Retorna:
        Grafo(Diccionario):almacena todos los nodos con todas
        las conexiones posibles de nuestro laberinto
    """
    grafo = nx.DiGraph()
    #Agregar nodos
    for i in range(n):
        for j in range(m):
            grafo.add_node((i+1, j+1))
    #Agrega aristas horizontales
    for i in range(n):
        for j in range(m-1):
            grafo.add_edge((i+1, j+1), (i+1, j+2))
    #Agregar aristas verticales
    for i in range(n-1):
        for j in range(m):
            grafo.add_edge((i+1, j+1), (i+2, j+1))
    #Crea las conexiones de vuelta
    #Agrega aristas horizontales
    for i in range(n):
        for j in range(m-1):
            grafo.add_edge((i+1, j+2), (i+1, j+1))    
    #Agregar aristas verticales
    for i in range(n-1):
        for j in range(m):
            grafo.add_edge((i+2, j+1), (i+1, j+1))
    return grafo

def inicio_ruta(n, m):
    """
    Toma un valor al azar en el borde del grafo nxm
    
    Parametros:
        n (entero):cantidad de valores del grafo de alto
        m (entero):cantidad de valores del grafo de ancho
    
    Retorna:
        inicio(entero): una coordenada de dos puntos(x,y)
        que representa el inicio del laberinto
    """
    x = random.randint(1,n)
    if x==1:
        y = random.randint(2,m)
    elif(1<x and x<n):
        l=[1,m]
        y = random.choice(l)
    elif x==n:
        y = random.randint(1,m-1)
    #print("nodo inicial:", end=" ")
    #print(x,y)
    return x,y
    
def final_ruta(inicio,n, m):
    """
    Toma un valor al azar en el borde del
    grafo nxm, excluyendo el valor del
    nodo inicial, se encarga de crear una
    salida rompio el borde donde termine
    la ruta.
    
    Parametros:
        inicio (Entero coordenadas):dos valores (x,y)
            que representan al nodo inicial
        n (Entero):cantidad de valores del grafo de alto
        m (Entero):cantidad de valores del grafo de ancho
    
    Retorna:
        final (Entero):dos valores de coordenadas para
            el final del laberinto
        pared (String): retorna la direccion de la ultima ruta
            para generar la salida del borde del laberinto
    """
    x1,y1 = inicio
    x = random.randint(1,n)
    pared=str("")
    while x==x1:
        x = random.randint(1,n)
    y=y1
    while y==y1:
        if x==1:
            y = random.randint(2,m)
        elif(1<x and x<n):
            l=[1,m]
            y = random.choice(l)
        elif x==n:
            y = random.randint(1,m-1)
            
    if y==1:
        pared="izquierda"
    elif y==m:
        pared="derecha"
    if x==1:
        pared="arriba"
    elif x==n:
        pared="abajo"
        
    final=(x,y)  
    return final,pared
def dfs(node,node_final,visitados,grafo):
    """
    Esta función implementa un algoritmo
    de búsqueda en profundidad
    (Depth-First Search).
    (DFS) es un algoritmo de búsqueda no
    informada que se utiliza para recorrer
    o buscar elementos en un grafo.
    La idea principal detrás del DFS es
    explorar tan profundamente como sea
    posible en un camino antes de retroceder.
    
    Parametros:
        node(Entero coordenada):Es el nodo actual en el que se encuentra
            el algoritmo de búsqueda en cada iteración.
        node_final(Entero coordenada):Es el nodo objetivo que se desea encontrar.
        visitados(Lista):Es una lista que almacena los nodos
            visitados durante la ejecución del algoritmo.
        grafo(Diccionario):Es el grafo representado como un diccionario,
            que nos muestra todos los nodos y posibles conexiones
        
    Retorna:
        visitados(Lista):lista de visitados que usaremos como ruta en el laberinto
    """
    visitados.append(node)
    #print("nodo base:", end=" ")
    #print(node)
    for vecinos in grafo[node]:
        if vecinos not in visitados:
            if vecinos!=node_final:
                dfs(vecinos,node_final, visitados, grafo)
            else:
                visitados.append(vecinos)
                break
            return visitados
def GrafoaMatriz(n,m,lista,pared):
    """
    Su Función es tomar la lista que tiene la ruta, y
    representarla de manera grafica con una matriz.
    
    Parametros:
        n (tipo entero):cantidad de valores del grafo de alto
        m (tipo entero):cantidad de valores del grafo de ancho
        lista (lista): lista que almacena la ruta por la que 
        pasa el laberinto.
        pared (string):Almacena la ultima direccion de salida
        para crear la salida del borde. 

    Retorna:
        matriz(matriz): retorna la matriz que representa la ruta
        de la lista visitados.
        indice(entero): numero de valor de largo de la ruta
    """
    matriz = []
    for i in range((2*n)+1):
        matriz.append([])
        for j in range((2*m)+1):
            matriz[i].append("x")
    for a in range(len(lista)):
        x, y = lista[a]
        indice=a
        matriz[(2*x)-1][(2*y)-1]="{}".format(" ")
        if a+1<len(lista):
            x1,y1 = lista[a+1]
            if x==x1:
                if y-y1==1:#izquierda
                    matriz[(2*x)-1][(2*y)-2]=' '
                elif y-y1==-1:#derecha
                    matriz[(2*x)-1][(2*y)]=' '
            if y==y1:
                if x-x1==1:#arriba
                    matriz[(2*x)-2][(2*y)-1]=' '
                elif x-x1==-1:#abajo
                    matriz[(2*x)][(2*y)-1]=' '
        if a==0:
            matriz[(2*x)-1][(2*y)-1]="p"
        if a+1==len(lista):
            if pared=="arriba":
                matriz[(2*x)-2][(2*y)-1]=' '
            if pared=="abajo":
                matriz[(2*x)][(2*y)-1]=' '
            if pared=="izquierda":
                matriz[(2*x)-1][(2*y)-2]=' '
            if pared=="derecha":
                matriz[(2*x)-1][(2*y)]=' '
    return matriz,indice

def imprime_matriz(matriz):
    """
    Se encarga de imprimir la matriz en la terminal
    
    Parametros:
        matriz(matriz)=matriz que representa al laberinto
    """ 
    for lista in matriz:
        print("[", end=" ")
        for elemento in lista:
            print(elemento, end=" ")
        print("]")
        
#Programa Principal
n=10
m=5
grafo=crea_grafo_unidireccional(n,m)
inicio=inicio_ruta(n,m)
final,pared=final_ruta(inicio,n,m)
lista=[]
lista=dfs(inicio,final,lista,grafo)
matriz,i=GrafoaMatriz(n,m,lista,pared)
while i<((n*m)-1):
    inicio=inicio_ruta(n,m)
    final,pared=final_ruta(inicio,n,m)
    lista=[]
    lista=dfs(inicio,final,lista,grafo)
    matriz,i=GrafoaMatriz(n,m,lista,pared)
imprime_matriz(matriz)
