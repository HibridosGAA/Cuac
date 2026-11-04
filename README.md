# Sistema Autónomo V2 (Red Neuronal)

Versión mejorada y elegante del sistema autónomo, diseñada para Render.

## Cambios en esta versión
- **Diseño Elegante y Profesional:** Tonos oscuros con acentos en amarillo suave pastel. Sin emojis.
- **Robot NVIDIA-Style:** La interfaz de la IA ahora presenta un robot recreado con CSS Art, inspirado en el diseño adjunto (cabeza tipo lente, pico/mordaza amarilla, torso lila/oscuro). Anima el ojo y la boca al procesar y hablar.
- **Sistema de Usuarios:** Pantalla de Login inicial. Al ingresar un nombre, entras a la IA y se crea un registro de tus chats en la base de datos y se muestran en la barra lateral izquierda.
- **Navegación Intuitiva:** El logo de la barra lateral redirige a la página principal `/`.
- **Protección con Contraseña:** Las secciones de `Historial Global` y `Panel de Control` están protegidas. Al intentar entrar, pedirá la clave de administrador (`cuac123`).
- **Historial Global Enriquecido:** La tabla de datos ahora muestra Fecha y Hora exacta, Nombre de Usuario, quién emitió el mensaje, el mensaje y la fase evolutiva.
- **Fix del Panel de Control:** El interruptor ahora actualiza el estado interno de la IA correctamente y apaga visualmente al robot (filtro de escala de grises).

## Despliegue en Render
Mismos pasos: Github -> Render -> Web Service (Python, `pip install -r requirements.txt`, `gunicorn app:app`).
