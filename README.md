# Plataforma de Análisis de Video UADY

## Versión 0.1 ALPHA

### Acerca del proyecto
La plataforma de análisis de video (de aquí en adelante, PAVI) es una API que provee los siguientes servicios:

- Procesar videos con diferentes algoritmos.*
- Mantener una base de datos con metadatos de los videos y sus resultados.
- Obtener los resultados de los videos procesados anteriormente.

*Algoritmos soportados actualmente: 
- YOLOv3
- Pedestrian Tracker.

### Algunos pendientes:

- Tamaño de los JSON muy grande dependiendo la configuración usada.
- Probar el procesamiento con una menor resolución. Comparar rendimiento y presición.
- Probar integración multiplataforma. 
- Implementar sistema de autenticación para tenerlo en línea.
- Experimentar con códecs de video, los cuales influyen en el tamaño de los archivos.
