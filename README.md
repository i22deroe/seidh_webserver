# seidh 1.0 webserver
### First release of Seidh library
>En el antiguo idioma nórdico, seiðr (seidh), era un tipo de brujería o hechizo practicado en la edad de hierro escandinava con la finalidad de predecir el futuro. Esta práctica fue asociada a menudo con Odín, por su vasto conocimiento atemporal.

Las interacciones entre proteínas y péptidos representan una gran fracción de todos los procesos bioquímicos que tienen lugar en cualquier organismo vivo. Hoy en día, en pleno desarrollo de la medicina personalizada, el conocimiento sobre cómo se acoplan las proteínas y los péptidos resulta de vital importancia para el desarrollo de nuevos tratamientos y terapias encaminadas a la cura de enfermedades genéticas, oncológicas, autoinmunes y un largo etcétera.

La predicción de estructuras tridimensionales del complejo proteína-péptido (también proteína-proteína) es un sector muy concreto de la biología computacional y estructural. Implica un profundo conocimiento de las interacciones entre las moléculas implicadas, y cómo estas pueden afectar a las estructuras secundaria y terciaria de los complejos; además de un potente banco de recursos bioinformáticos para el manejo de esta información.

La librería Seidh implementa un algoritmo basado en el vuelo de Cuculus canorus (cuco común), un ave parásita que en época de puesta invade nidos de otros pájaros para depositar sus huevos. Este movimiento, que alterna movimientos cortos seguidos de vuelos más largos, resulta particularmente interesante para la predicción de estructuras.

La librería también incluye otros módulos auxiliares para llevar a cabo su cometido. Algunos de estos módulos son de recomendado acceso antes de la invocación de la función principal. Para ello, es recomendable leer detenidamente los requisitos de uso de Seidh y cómo pueden estos otros módulos ayudarte para obtener la estructura del péptido problema.

## Requisitos de Seidh
Seidh 1.0 está escrito para Python 2.7 y requiere los siguientes módulos de Python:
*	biopython 1.66 o superior
*	numpy 1.14.0 o superior
*	PeptideBuilder 1.0.3 o superior

## Requisitos de Seidh webserver
Esta implementación de Seidh requiere además los siguientes módulos:
*	flask
*	flask_sqlalchemy
*	celery

Además, Seidh webserver necesita la ejecución simultánea de un servidor redis, que actuará como broker de las tareas que suban los usuarios.

## Guía de uso

Para hacer funcionar el servidor, basta con ejecutar primero el servidor redis, seguido de celery y finalmente, la aplicación propiamente dicha (run.py). Es preciso configurar WSGI y Apache para su uso en producción.