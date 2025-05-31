# Escapa del Caos

¡Bienvenido a "Escapa del Caos"! Un vibrante juego de esquivar obstáculos desarrollado completamente con la librería Pygame en Python. Este proyecto ha sido diseñado para ofrecer una experiencia de juego sencilla pero adictiva, donde tus reflejos y habilidad para anticipar movimientos enemigos son clave para la supervivencia.

Tu objetivo principal es simple: **esquivar una implacable lluvia de enemigos que descienden desde la parte superior de la pantalla**, sobreviviendo el mayor tiempo posible para acumular la puntuación más alta. En tu travesía, podrás recoger valiosos power-ups que te proporcionarán una ventaja vital.

## 🚀 Cómo Jugar

Para poner en marcha "Escapa del Caos", asegúrate de tener Python 3.x y Pygame instalados en tu sistema.

1.  **Ejecutar el juego:** Navega a la carpeta donde se encuentran todos los archivos del juego (incluyendo `zmain.py`, imágenes y sonidos) en tu terminal o línea de comandos. Luego, ejecuta el siguiente comando:
    ```bash
    python zmain.py
    ```

## 📦 Nota Importante sobre el Archivo ZIP

Para mayor comodidad o como respaldo, todos los archivos de este proyecto también están disponibles en un único archivo comprimido: `mi_juego_pygame.zip`. Si lo descargas, asegúrate de descomprimirlo para acceder a todos los componentes del juego (código, imágenes, sonidos) y poder ejecutar `zmain.py`.

## 🕹️ Controles

* **Flechas del teclado (↑ ↓ ← →):** Mover al jugador.
* **P (tecla):** Pausar/Reanudar el juego.
* **ESC (tecla):** Desde el juego, presiona 'ESC' para abrir el menú de pausa completo con opciones adicionales.
* **Clic en el icono de engranaje (⚙️):** Ubicado en la esquina superior derecha durante el juego. Al hacer clic, también abrirá el menú de pausa.
* **Clic de ratón / ESPACIO:** Utiliza el clic del ratón o la tecla ESPACIO para seleccionar opciones en los menús de Inicio, Pausa y Game Over.

## ✨ Características Principales

### **Mecánicas de Juego**

* **Jugabilidad de Esquivar:** El núcleo del juego se centra en mover a tu jugador para evitar colisiones con enemigos que caen aleatoriamente desde la parte superior.
* **Sistema de Puntuación y Récords:** Gana puntos por cada momento que sobrevives y establece tu mejor puntuación personal. Tu récord se registra y se guarda localmente en el archivo `mejor_puntaje.txt`, animándote a superar tus propios límites.
* **Manejo de Vidas:** Comienzas con 3 vidas. Cada colisión con un enemigo te resta una vida. El juego finaliza al perder todas tus vidas.
* **Power-ups de Vida:** Ocasionalmente, aparecerán power-ups de vida (representados por un sprite específico) que, al ser recogidos, te otorgan una vida adicional (con un máximo de 3 vidas).
* **Dificultad Dinámica:** La velocidad de los enemigos y la frecuencia con que aparecen aumentan progresivamente a medida que tu puntaje alcanza ciertos umbrales, elevando el nivel del juego y manteniendo el desafío constante.

### **Estructura de Menús y Estados**

El juego cuenta con un sistema robusto de manejo de estados y menús para una experiencia de usuario fluida:

* **Menú de Inicio:** La primera pantalla que el jugador ve. Permite comenzar una nueva partida, revisar los controles y ver el récord actual.
* **Menú de Pausa:** Accesible durante el juego. Ofrece opciones para reanudar la partida, regresar al menú principal o salir del juego. La música de fondo se pausa/reanuda con este menú.
* **Pantalla de Game Over:** Se activa al perder todas las vidas. Muestra el puntaje final, el récord, el nivel alcanzado y el tiempo jugado, junto con opciones para reintentar la partida, volver al menú principal o salir.

### **Inmersión y Feedback**

* **Efectos de Sonido (SFX):** Implementados estratégicamente para proporcionar retroalimentación auditiva clara y satisfactoria:
    * Sonido de impacto al colisionar con enemigos.
    * Sonido de recolección al obtener power-ups.
    * Sonido distintivo al subir de nivel.
    * Sonido de "Game Over" para indicar el fin de la partida.
    * Sonidos de clic para interacciones con botones en los menús.
* **Música de Fondo:** Acompaña la experiencia de juego, con una melodía diferente para el menú de inicio y para la fase de juego activa.
* **Gráficos Sencillos:** Utiliza sprites básicos para el jugador, enemigos y power-ups, así como una imagen de fondo para establecer la atmósfera espacial.

## 🛠️ Estructura del Código y Tecnologías

El juego está desarrollado bajo un enfoque modular, encapsulado en una clase principal `Juego` que maneja todos los aspectos de la aplicación:

* **Clase `Juego`:** Contiene el bucle principal del juego, la inicialización de Pygame, la carga de assets, la gestión de estados (inicio, juego activo, pausa, game over) y todas las funciones lógicas del juego (movimiento, colisiones, renderizado, etc.).
* **Funciones Auxiliares:** Métodos privados y públicos para cargar recursos (`_cargar_imagen`, `_cargar_sfx`), dibujar texto y botones, gestionar la lógica de juego (`mover_elementos`, `detectar_colisiones`, `actualizar_dificultad`), y manejar los flujos de los menús (`menu_inicio`, `menu_pausa`, `pantalla_final`).

**Tecnologías Utilizadas:**

* **Python 3.x:** Lenguaje de programación principal.
* **Pygame:** Librería fundamental para el desarrollo de gráficos y sonido.

## 💡 Desafíos y Aprendizajes

Durante el desarrollo de "Escapa del Caos", se abordaron varios desafíos importantes:

* **Manejo de Estados del Juego:** Implementar una lógica robusta para transicionar entre el menú de inicio, el juego activo, el estado de pausa y la pantalla de fin de juego. Esto fue crucial para una experiencia de usuario fluida.
* **Gestión de Recursos (Assets):** Asegurar que las imágenes y los archivos de sonido se cargaran correctamente y que el juego pudiera funcionar incluso si algún archivo faltaba, gracias a las funciones de carga con manejo de errores.
* **Integración de Sonido:** Coordinar los efectos de sonido con eventos específicos del juego (colisiones, power-ups) y gestionar la música de fondo (reproducción, pausa, stop) para mejorar la inmersión.
* **Persistencia de Datos:** Implementar la lectura y escritura del mejor puntaje en un archivo de texto (`mejor_puntaje.txt`) para mantener un récord entre sesiones de juego.

## 🤝 Autor

* **Mauricio Alejandro Barreto Arenas**
