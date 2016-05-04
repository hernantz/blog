Title: Batalla naval
Status: draft

Armar listados
--------------
1) Tener un listado de puntos para cada barco donde hay que disparar
2) Para obtener esos puntos dividir la grilla en grillas menores de n x n, donde n es el tamanio del barco
3) Para cada grilla, agregar los puntos de la diagonal (superior izquierdo a inferior derecho) a los listados de puntos a disparar para cada barco de ese tamanio
4) Crear un listado vacio para almacenar los puntos a donde no disparar (lleno de aciertos y fallos)
5) Ir a modo busqueda


Modo busqueda
-------------
1) Obtener el primer punto del listado del barco mas grande disponible y disparar 
2) Ir al procediento analizar resultado


Procedimiento analizar resultado
--------------------------------
1) En caso de acertar ir a modo ataque, en caso de hundir ir a procedimiento de hundir, y en caso de fallar ir a procedimiento de fallar


Procedimiento fallar
--------------------
1) Borrar ese elemento de todos los listados de barcos
2) Agregar ese punto al listado de no disparar
3) Ir al modo busqueda


Procedimiento hundir
--------------------
1) Obtener todos los puntos del barco y sus aledanios y borrarlos de todos los otros listados 
2) Agregar esos puntos (del barco y sus aledanios) al listado de no disparar
3) Borrar el listado correspondiente a este barco
4) Ir al modo busqueda


Modo ataque
-----------
1) Obtener los puntos arriba, abajo, derecho e izquierdo del punto acertado 
2) Remover de ese listado los puntos que ya se encuentran en el listado de no disparar
3) De los puntos restantes elegir uno indistinto y disparar
4) Ir al procedimiento analizar resultado
