# Plataforma de Análisis de Video UADY

## Versión 0.1 ALPHA

### Acerca del proyecto
La plataforma de análisis de video tiene las siguientes funciones:

- Procesar videos con diferentes algoritmos.*
- Visualizar datos obtenidos de los videos.
- Mantener una base de datos con metadatos de los videos y sus resultados.

*Algoritmos soportados actualmente: YOLOv3, OpenVINO Pedestrian Tracker.

### PENDIENTES:

#### Importante 
- Renderizado dinámico de la gráfica.
- Evitar Docker y utilizar OpenVINO instalado de manera local, ya que la imagen de Docker ocupa mucho espacio y la
instalación de OpenVINO provee la biblioteca de OpenCV con el Inference Engine de Intel, lo que acelera el procesamiento
en equipos sin GPU. Ya se encuentra código para esto solamente que no está implementado aún. (Véase *scripts/openvino*)
- Integrar OpenCV compilado con librerías CUDA. El OpenCV que se instala mediante Python no incluye funcionalidad para
utilizar GPU.
- **EN CURSO** - Refactorizar el código de Python y JS, sin tener tantas llamadas a diferentes scripts en app.py. (¿Funciones? ¿Módulos?)
ARQUITECTURA.
- Tamaño de los JSON muy grande dependiendo la configuración usada.

#### Puede esperar
- Probar el procesamiento con una menor resolución. Comparar rendimiento y presición.
- Mejor integración multiplataforma. 
- **LISTO** - Mejor manejo de las credenciales de la base de datos.
- Implementar sistema de autenticación para tenerlo en línea.
- Determinar cómo se guardarán los archivos de video. (¿Almacenamiento en línea? ¿Servidor local? 
¿Sólo guardar los recientes?)
- Cambiar códecs de entrada y salida de video. Actualmente los videos de salida ocupan mucho más espacio del original
(3 a 5 veces más)
- Manejo de videos en el UI. (procesados vs original)
- Mejorar conversión de los videos del NVR, ya que la conversión actual quita algunos metadatos del video original.
- Renderizar las cajas de detección de objetos al momento sobre el video original.

#### Detalles
- Renderizado inmediato de la gráfica, sin tener que hacerle clic
- Mostrar progreso del procesamiento en el UI web.
- Botones para ir cambiando entre los archivos de video procesados.

### Otras tareas

1. Parametrizar desde la web app los datos necesarios del json en la configuración de cada algoritmo. Estos datos deben mostrarse al usuario de acuerdo al algoritmo.
2. En la gráfica, sería conveniente una comparación del algoritmo (ejecutándose cada uno por separado o juntos quizás), mostrando cuál es el algoritmo que detectó mejor los objetos (claro está solo objetos comunes detectables por cada algoritmo)
3. Verificar que una gráfica muestre correctamente los datos obtenidos de MongoDB, usando REACT
4. Usando la historia de usuario crear el Mock UI en figma y enviarlo al PO.
5. Verificar que las tablas de la interfaz estén sincronizados con los valores obtenidos de MongoDB, usando REACT
6. El título de la webapp cambiarlo, me parece que dice solamente el nombre de un algoritmo.
7. Agrega logo facultad o logo Uady
8. Hacer un análisis de los atributos necesarios de la BD de tal manera que sean más flexible, fácil y adecuada las consultas.
9. Fecha y hora de captura del video.
10. La división de vídeos largos en vídeos cortos para mayor facilidad de manipulación.
11. La posibilidad de manejar otro formato de vídeo más ligero.
12. Estimar el escalamiento del tamaño de la BD de acuerdo a los videos
13. Exportar datos a CSV controlado por frames (o segundos)
14. Hacer uniforme la medida usada en la interfaz ya sea frame o segundos
15. Hacer explícita la acción de cargar un video y procesarlo contra ver los resultados de un video ya procesado. Diseño de la interfaz con React.
16. Agregar el dato CameraID y ProcessingDate en los documentos
17. Registrar en la BD de Mongo, datos de las trayectorias de los objetos identificados.
18. Definir historias de usuario para la página web de PAVI (JR)

