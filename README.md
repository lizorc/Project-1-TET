# Base de datos distribuida simple

## Abstract 

Varios desarrollos actuales requieren de un sistema distribuido que permita el almacenamiento de datos de forma eficiente para obtener, con baja latencia, información y realizar tareas internas de forma eficiente por lo que partiremos de la premisa ¿qué es una base de datos distribuida NoSQL y como se manejan los sistemas key-value? para poder brindar información y clarificar cómo podemos adaptar este tipo de sistemas a desarrollos en la actualidad, y mucho más importante, bases teóricas de cómo podemos desarrollar un sistema distribuído key-value.

## Descripción breve

Tenemos un conjunto de nodos, los cuales almacenarán registros de una aplicación cliente en el formato key-value. Siendo el objetivo diseñar e implementar un sistema que permita almacenar datos distribudios en los nodos por parte de los cliente. 

En una implementación simple, el cliente sera el que contacta el ServerFrontend, el cual recibe el requerimiento CRUD para determinar que ServerData procesara dicho requerimiento. Por otro lado, los ServerData deben cooperar, coordinar y ejecutar las acciones del CRUD entre si oara garantizar rendimiento, confiabilidad, tolerancia a fallos, entre otros.

Retos y soluciones a los que se debe enfrentar son:
- Almacenamiento distribuido de datos (Recuperación Distribuida o Centralizada)
- Replicación 
- Particionamiento
- Tolerancia a fallos
- Escalabilidad
- WORM vs WMRM
- Cliente/Servidor vs P2P vs hibrido C/S-P2P
- Transacciones, Bloque u Objetos

Requisimientos a cumplir:
- Analizar, diseñar e implementar una base de datos distribuida NoSQL simple a nivel key-value
- Esta base de datos recibirá las peticiones CRUD de los clientes a través de una API Sockets o HTTP
- Determinar los protocolos de comunicación Cliente-ServerFrontend, ServerFrontend-ServerData y ServerData-ServerData sobre protocolos TCP/UDP con sockets o con protocolos HTTP

## Propuesta de diseño

![Blank diagram](https://user-images.githubusercontent.com/79216103/159069363-a69a28ab-245e-43b0-98a0-a0c4f9dfad23.png)


## Participantes
- Julian Ramirez Giraldo
- Liz Oriana Rodrigues Cruz 
