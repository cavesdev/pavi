# Plataforma de Análisis de Video UADY

## Versión 0.1 ALPHA

### Acerca del proyecto
La plataforma de análisis de video tiene las siguientes funciones:

- Procesar videos con diferentes algoritmos.*
- Visualizar datos obtenidos de los videos.
- Mantener una base de datos con metadatos de los videos y sus resultados.

*Algoritmos soportados actualmente: YOLOv3, OpenVINO Pedestrian Tracker.

### PENDIENTES:
- Evitar Docker y utilizar OpenVINO instalado de manera local, ya que la imagen de Docker ocupa mucho espacio y la
instalación de OpenVINO provee la biblioteca de OpenCV con el Inference Engine de Intel, lo que acelera el procesamiento
en equipos sin GPU. Ya se encuentra código para esto solamente que no está implementado aún. (Véase *scripts/openvino*)
- Integrar OpenCV compilado con librerías CUDA. El OpenCV que se instala mediante Python no incluye funcionalidad para
utilizar GPU.
- Mejor integración multiplataforma. 
- Refactorizar el código de Python, sin tener tantas llamadas a diferentes scripts en app.py. (¿Funciones? ¿Módulos?)
- Mejor manejo de las credenciales de la base de datos.
- Implementar sistema de autenticación para tenerlo en línea.
- Determinar cómo se guardarán los archivos de video. (¿Almacenamiento en línea? ¿Servidor local? 
¿Sólo guardar los recientes?)
- Manejo de videos en el UI. (procesados vs original)
- Mostrar progreso del procesamiento en el UI web.