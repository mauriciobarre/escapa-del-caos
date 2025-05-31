import pygame
import random
import sys
import os
import time

class Juego:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.ancho = 600
        self.alto = 600
        self.ventana = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Escapa del Caos")
        self.clock = pygame.time.Clock()

        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.ROJO = (200, 0, 0)
        self.AZUL = (0, 0, 255)
        self.VERDE = (0, 200, 0)
        self.GRIS_CLARO = (180, 180, 180)

        # --- Cargar Sonidos y Música ---
        ruta_base = os.path.dirname(__file__)

        self.ruta_musica = os.path.join(ruta_base, 'musica_fondo.wav')
        self.ruta_musica_menu = os.path.join(ruta_base, 'musica_menu.wav')

        # NUEVOS: Cargar archivos de efectos de sonido
        self.sfx_impacto = self._cargar_sfx('impacto.wav', 0.5) # Volumen de 0.5
        self.sfx_powerup = self._cargar_sfx('powerup_recogido.wav', 0.7)
        self.sfx_game_over = self._cargar_sfx('game_over_sfx.wav', 0.8)
        self.sfx_level_up = self._cargar_sfx('level_up.wav', 0.6)
        self.sfx_button_click = self._cargar_sfx('button_click.wav', 0.5)


        # Cargar imágenes (sprites)
        self.imagen_jugador = self._cargar_imagen('player.png', (50, 50), alpha=True)
        self.imagen_enemigo = self._cargar_imagen('enemy.png', (50, 50), alpha=True)
        self.imagen_powerup = self._cargar_imagen('poweru.png', (30, 30), alpha=True)
        self.imagen_fondo = self._cargar_imagen('background.webp', (self.ancho, self.alto))
        
        self.imagen_pausa_btn = self._cargar_imagen('pause_icon.jpg', (40, 40), alpha=True)
        self.rect_boton_pausa = pygame.Rect(self.ancho - 50, 10, 40, 40)

        # Cargar mejor puntaje desde archivo
        try:
            with open("mejor_puntaje.txt", "r") as f:
                self.mejor_puntaje = int(f.read())
        except:
            self.mejor_puntaje = 0

        # --- Variables de estado del juego (ahora se reinician con resetear_juego) ---
        self.jugador = pygame.Rect(275, 500, 50, 50)
        self.vel_jugador = 6
        self.enemigos = []
        self.powerups = []
        self.vel_enemigo = 3
        self.puntos = 0
        self.vidas = 3
        self.nivel = 1
        self.MAX_ENEMIGOS = 10
        self.juego_activo = False
        self.tiempo_inicio_juego = 0
        self.pausado = False 

    # Función auxiliar para cargar imágenes y manejar errores
    def _cargar_imagen(self, nombre_archivo, escala, alpha=False):
        ruta_base = os.path.dirname(__file__)
        ruta_completa = os.path.join(ruta_base, nombre_archivo)
        imagen = None
        if os.path.exists(ruta_completa):
            try:
                imagen = pygame.image.load(ruta_completa)
                if alpha:
                    imagen = imagen.convert_alpha()
                else:
                    imagen = imagen.convert()
                imagen = pygame.transform.scale(imagen, escala)
            except pygame.error as e:
                print(f"Advertencia: No se pudo cargar '{nombre_archivo}'. Error: {e}")
                imagen = None
        else:
            print(f"Advertencia: No se encontró la imagen '{nombre_archivo}' en '{ruta_completa}'.")
        return imagen

    # NUEVA FUNCIÓN: Auxiliar para cargar efectos de sonido
    def _cargar_sfx(self, nombre_archivo, volumen=1.0):
        ruta_base = os.path.dirname(__file__)
        ruta_completa = os.path.join(ruta_base, nombre_archivo)
        sfx = None
        if os.path.exists(ruta_completa):
            try:
                sfx = pygame.mixer.Sound(ruta_completa)
                sfx.set_volume(volumen)
            except pygame.error as e:
                print(f"Advertencia: No se pudo cargar el SFX '{nombre_archivo}'. Error: {e}")
                sfx = None
        else:
            print(f"Advertencia: No se encontró el SFX '{nombre_archivo}' en '{ruta_completa}'.")
        return sfx

    def resetear_juego(self):
        self.jugador = pygame.Rect(275, 500, 50, 50)
        self.enemigos = []
        self.powerups = []
        self.puntos = 0
        self.vidas = 3
        self.nivel = 1
        self.vel_enemigo = 3
        self.juego_activo = False
        self.tiempo_inicio_juego = 0
        self.pausado = False 

    def mostrar_texto(self, texto, tam, color, x, y, bold=False):
        fuente = pygame.font.SysFont("Arial", tam, bold=bold)
        render = fuente.render(texto, True, color)
        rect = render.get_rect(center=(x, y))
        self.ventana.blit(render, rect)

    def dibujar_boton(self, texto, rect, color_normal, color_hover, mouse_pos):
        color = color_hover if rect.collidepoint(mouse_pos) else color_normal
        pygame.draw.rect(self.ventana, color, rect, border_radius=8)
        fuente = pygame.font.SysFont("Arial", 24, bold=True)
        texto_render = fuente.render(texto, True, self.BLANCO)
        texto_rect = texto_render.get_rect(center=rect.center)
        self.ventana.blit(texto_render, texto_rect)

    def crear_enemigo(self):
        x = random.randint(0, self.ancho - 50)
        self.enemigos.append(pygame.Rect(x, 0, 50, 50))

    def crear_powerup(self):
        if len(self.powerups) < 1:
            x = random.randint(0, self.ancho - 30)
            self.powerups.append(pygame.Rect(x, 0, 30, 30))

    def mover_elementos(self):
        for enemigo in self.enemigos[:]:
            enemigo.y += self.vel_enemigo
            if enemigo.y > self.alto:
                self.enemigos.remove(enemigo)
        for power in self.powerups[:]:
            power.y += 3
            if power.y > self.alto:
                self.powerups.remove(power)

    def detectar_colisiones(self):
        enemigos_a_eliminar = []
        for enemigo in self.enemigos:
            if self.jugador.colliderect(enemigo):
                enemigos_a_eliminar.append(enemigo)
                self.vidas -= 1
                if self.sfx_impacto: # NUEVO: Reproducir sonido de impacto
                    self.sfx_impacto.play()
        for enemigo in enemigos_a_eliminar:
            self.enemigos.remove(enemigo)
            self.crear_enemigo() 

        powerups_a_eliminar = []
        for power in self.powerups:
            if self.jugador.colliderect(power):
                powerups_a_eliminar.append(power)
                self.vidas = min(3, self.vidas + 1)
                self.puntos += 20
                if self.sfx_powerup: # NUEVO: Reproducir sonido de power-up
                    self.sfx_powerup.play()

        for power in powerups_a_eliminar:
            self.powerups.remove(power)


    def dibujar_elementos(self):
        if self.imagen_fondo:
            self.ventana.blit(self.imagen_fondo, (0, 0))
        else:
            self.ventana.fill(self.BLANCO)

        if self.imagen_jugador:
            self.ventana.blit(self.imagen_jugador, self.jugador)
        else:
            pygame.draw.rect(self.ventana, self.AZUL, self.jugador)

        if self.imagen_enemigo:
            for enemigo in self.enemigos:
                self.ventana.blit(self.imagen_enemigo, enemigo)
        else:
            for enemigo in self.enemigos:
                pygame.draw.rect(self.ventana, self.ROJO, enemigo)

        if self.imagen_powerup:
            for power in self.powerups:
                self.ventana.blit(self.imagen_powerup, power)
        else:
            for power in self.powerups:
                pygame.draw.rect(self.ventana, self.VERDE, power)
        
        if self.imagen_pausa_btn:
            self.ventana.blit(self.imagen_pausa_btn, self.rect_boton_pausa)
        else:
            pygame.draw.rect(self.ventana, self.GRIS_CLARO, self.rect_boton_pausa, border_radius=5)
            self.mostrar_texto("II", 28, self.NEGRO, self.rect_boton_pausa.centerx, self.rect_boton_pausa.centery, bold=True)


    def actualizar_dificultad(self):
        # Avanza de nivel cada 200 puntos
        if self.puntos > 0 and self.puntos % 200 == 0 and self.nivel == (self.puntos // 200):
            self.vel_enemigo += 1
            self.nivel += 1
            if self.sfx_level_up: # NUEVO: Reproducir sonido al subir de nivel
                self.sfx_level_up.play()

    def menu_inicio(self):
        self.resetear_juego()
        en_menu = True
        pygame.mixer.music.stop()

        if os.path.exists(self.ruta_musica_menu):
            pygame.mixer.music.load(self.ruta_musica_menu)
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)

        reloj = pygame.time.Clock()
        mostrar_texto_parpadeante = True
        tiempo_parpadeo = 0

        boton_jugar = pygame.Rect(self.ancho // 2 - 100, self.alto // 2 + 40, 200, 50)
        boton_salir = pygame.Rect(self.ancho // 2 - 100, self.alto // 2 + 110, 200, 50)

        while en_menu:
            reloj.tick(60)
            tiempo_parpadeo += 1
            if tiempo_parpadeo % 30 == 0:
                mostrar_texto_parpadeante = not mostrar_texto_parpadeante

            mouse = pygame.mouse.get_pos()
            click = False

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        if self.sfx_button_click: self.sfx_button_click.play() # NUEVO: Sonido al iniciar
                        en_menu = False
                        self.juego_activo = True
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.sfx_button_click: self.sfx_button_click.play() # NUEVO: Sonido al clic
                    click = True

            if self.imagen_fondo:
                self.ventana.blit(self.imagen_fondo, (0, 0))
            else:
                self.ventana.fill(self.NEGRO)

            self.mostrar_texto("ESCAPA DEL CAOS", 44, self.BLANCO, self.ancho // 2, self.alto // 2 - 100, bold=True)
            if mostrar_texto_parpadeante:
                self.mostrar_texto("Presiona ESPACIO o haz clic en JUGAR", 24, self.BLANCO, self.ancho // 2, self.alto // 2 - 30)

            self.dibujar_boton("JUGAR", boton_jugar, self.AZUL, (0, 150, 255), mouse)
            self.dibujar_boton("SALIR", boton_salir, self.ROJO, (255, 50, 50), mouse)

            if click:
                if boton_jugar.collidepoint(mouse):
                    en_menu = False
                    self.juego_activo = True
                if boton_salir.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

            self.mostrar_texto("← ↑ ↓ →   Mover", 18, self.BLANCO, 100, 480)
            self.mostrar_texto("P - Pausar/Reanudar", 18, self.BLANCO, 100, 505)
            self.mostrar_texto("ESC - Menú Pausa", 18, self.BLANCO, 100, 530)
            self.mostrar_texto("Clic en II para Pausa", 18, self.BLANCO, 100, 555)
            self.mostrar_texto(f"Record: {self.mejor_puntaje}", 20, self.BLANCO, self.ancho // 2, self.alto - 40)


            pygame.display.update()

        if self.juego_activo and os.path.exists(self.ruta_musica):
            pygame.mixer.music.load(self.ruta_musica)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            self.tiempo_inicio_juego = pygame.time.get_ticks()


    def pantalla_final(self, tiempo_jugado_segundos):
        if self.sfx_game_over: self.sfx_game_over.play() # NUEVO: Sonido de game over al entrar
        pygame.mixer.music.stop()

        if self.puntos > self.mejor_puntaje:
            self.mejor_puntaje = self.puntos
            try:
                with open("mejor_puntaje.txt", "w") as f:
                    f.write(str(self.mejor_puntaje))
            except IOError:
                print("Error: No se pudo guardar el mejor puntaje.")

        esperando = True
        
        boton_reintentar = pygame.Rect(self.ancho // 2 - 200, self.alto // 2 + 150, 120, 45)
        boton_menu = pygame.Rect(self.ancho // 2 - 60, self.alto // 2 + 150, 120, 45)
        boton_salir = pygame.Rect(self.ancho // 2 + 80, self.alto // 2 + 150, 120, 45)

        while esperando:
            mouse = pygame.mouse.get_pos()
            click = False

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.sfx_button_click: self.sfx_button_click.play() # NUEVO: Sonido al clic
                    click = True
            
            if self.imagen_fondo:
                self.ventana.blit(self.imagen_fondo, (0, 0))
            else:
                self.ventana.fill(self.NEGRO)

            marco_ancho = 450
            marco_alto = 280
            marco_x = self.ancho // 2 - marco_ancho // 2
            marco_y = self.alto // 2 - marco_alto // 2 - 80
            
            pygame.draw.rect(self.ventana, self.NEGRO, (marco_x, marco_y, marco_ancho, marco_alto), border_radius=15)
            pygame.draw.rect(self.ventana, self.BLANCO, (marco_x, marco_y, marco_ancho, marco_alto), 5, border_radius=15)
            pygame.draw.line(self.ventana, self.BLANCO, (marco_x + 20, marco_y + 80), (marco_x + marco_ancho - 20, marco_y + 80), 2)
            
            self.mostrar_texto("❌ GAME OVER ❌", 45, self.ROJO, self.ancho // 2, marco_y + 40, bold=True)
            self.mostrar_texto(f"Puntaje: {self.puntos}", 30, self.BLANCO, self.ancho // 2, marco_y + 110)
            self.mostrar_texto(f"Record: {self.mejor_puntaje}", 30, self.BLANCO, self.ancho // 2, marco_y + 150)
            self.mostrar_texto(f"Nivel alcanzado: {self.nivel}", 30, self.BLANCO, self.ancho // 2, marco_y + 190)
            
            minutos = tiempo_jugado_segundos // 60
            segundos = tiempo_jugado_segundos % 60
            self.mostrar_texto(f"Tiempo jugado: {minutos:02}:{segundos:02}", 30, self.BLANCO, self.ancho // 2, marco_y + 230)
            
            self.mostrar_texto("¡Sigue mejorando tus reflejos!", 22, self.VERDE, self.ancho // 2, marco_y + marco_alto + 20)

            self.dibujar_boton("REINTENTAR", boton_reintentar, (0, 100, 0), (0, 150, 0), mouse)
            self.dibujar_boton("MENÚ", boton_menu, (0, 0, 150), (0, 0, 200), mouse)
            self.dibujar_boton("SALIR", boton_salir, (150, 0, 0), (200, 0, 0), mouse)

            if click:
                if boton_reintentar.collidepoint(mouse):
                    return 'reintentar'
                elif boton_menu.collidepoint(mouse):
                    return 'menu'
                elif boton_salir.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def menu_pausa(self):
        pygame.mixer.music.pause()
        
        pausado = True
        
        boton_reanudar = pygame.Rect(self.ancho // 2 - 100, self.alto // 2 - 60, 200, 50)
        boton_menu_principal = pygame.Rect(self.ancho // 2 - 100, self.alto // 2 + 10, 200, 50)
        boton_salir_pausa = pygame.Rect(self.ancho // 2 - 100, self.alto // 2 + 80, 200, 50)

        while pausado:
            mouse = pygame.mouse.get_pos()
            click = False

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_p:
                        if self.sfx_button_click: self.sfx_button_click.play() # NUEVO: Sonido al reanudar
                        pygame.mixer.music.unpause()
                        return 'reanudar'
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.sfx_button_click: self.sfx_button_click.play() # NUEVO: Sonido al clic
                    click = True

            self.dibujar_elementos()
            s = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            self.ventana.blit(s, (0, 0))

            self.mostrar_texto("JUEGO EN PAUSA", 45, self.BLANCO, self.ancho // 2, self.alto // 2 - 120, bold=True)

            self.dibujar_boton("REANUDAR", boton_reanudar, (0, 100, 0), (0, 150, 0), mouse)
            self.dibujar_boton("MENÚ PRINCIPAL", boton_menu_principal, (0, 0, 150), (0, 0, 200), mouse)
            self.dibujar_boton("SALIR DEL JUEGO", boton_salir_pausa, (150, 0, 0), (200, 0, 0), mouse)

            if click:
                if boton_reanudar.collidepoint(mouse):
                    pygame.mixer.music.unpause()
                    return 'reanudar'
                elif boton_menu_principal.collidepoint(mouse):
                    pygame.mixer.music.stop()
                    return 'menu'
                elif boton_salir_pausa.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()
            self.clock.tick(60)


    def jugar(self):
        while True:
            self.menu_inicio()

            while self.juego_activo:
                self.clock.tick(60)
                mouse_pos = pygame.mouse.get_pos()

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        self.juego_activo = False
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_p:
                            self.pausado = not self.pausado
                            if self.pausado:
                                pygame.mixer.music.pause()
                            else:
                                pygame.mixer.music.unpause()
                        elif evento.key == pygame.K_ESCAPE:
                            self.pausado = True
                            accion_pausa = self.menu_pausa()
                            
                            if accion_pausa == 'reanudar':
                                self.pausado = False
                            elif accion_pausa == 'menu':
                                self.juego_activo = False
                                break
                            elif accion_pausa == 'salir':
                                pygame.quit()
                                sys.exit()
                    
                    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                        if self.rect_boton_pausa.collidepoint(mouse_pos) and not self.pausado:
                            if self.sfx_button_click: self.sfx_button_click.play() # NUEVO: Sonido al clic del botón de pausa
                            self.pausado = True
                            accion_pausa = self.menu_pausa()
                            
                            if accion_pausa == 'reanudar':
                                self.pausado = False
                            elif accion_pausa == 'menu':
                                self.juego_activo = False
                                break
                            elif accion_pausa == 'salir':
                                pygame.quit()
                                sys.exit()


                if not self.juego_activo:
                    break 
                
                if not self.pausado:
                    teclas = pygame.key.get_pressed()
                    if teclas[pygame.K_LEFT] and self.jugador.left > 0:
                        self.jugador.x -= self.vel_jugador
                    if teclas[pygame.K_RIGHT] and self.jugador.right < self.ancho:
                        self.jugador.x += self.vel_jugador
                    if teclas[pygame.K_UP] and self.jugador.top > 0:
                        self.jugador.y -= self.vel_jugador
                    if teclas[pygame.K_DOWN] and self.jugador.bottom < self.alto:
                        self.jugador.y += self.vel_jugador

                    if random.randint(1, 30) == 1 and len(self.enemigos) < self.MAX_ENEMIGOS:
                        self.crear_enemigo()
                    if random.randint(1, 500) == 1:
                        self.crear_powerup()

                    self.mover_elementos()
                    self.detectar_colisiones()
                    self.puntos += 1
                    self.actualizar_dificultad()

                self.dibujar_elementos() 
                self.mostrar_texto(f"Puntos: {self.puntos}", 22, self.BLANCO, 80, 20)
                self.mostrar_texto(f"Vidas: {self.vidas}", 22, self.BLANCO, 500, 20)
                self.mostrar_texto(f"Nivel: {self.nivel}", 22, self.BLANCO, 500, 50)
                self.mostrar_texto(f"Record: {self.mejor_puntaje}", 20, self.BLANCO, 500, 80)

                if self.pausado and self.juego_activo:
                    self.mostrar_texto("PAUSA", 60, self.BLANCO, self.ancho // 2, self.alto // 2, bold=True)
                    self.mostrar_texto("Presiona 'P' para continuar o 'ESC' para Opciones", 24, self.BLANCO, self.ancho // 2, self.alto // 2 + 50)


                pygame.display.update()

                if self.vidas <= 0:
                    self.juego_activo = False
                    break

            tiempo_jugado_segundos = 0
            if self.tiempo_inicio_juego > 0: 
                 tiempo_jugado_segundos = (pygame.time.get_ticks() - self.tiempo_inicio_juego) // 1000

            if not (pygame.event.peek(pygame.QUIT) and not self.juego_activo):
                accion_final = self.pantalla_final(tiempo_jugado_segundos)

                if accion_final == 'reintentar':
                    self.resetear_juego()
                    self.juego_activo = True
                    if os.path.exists(self.ruta_musica):
                        pygame.mixer.music.load(self.ruta_musica)
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                    self.tiempo_inicio_juego = pygame.time.get_ticks()
                elif accion_final == 'menu':
                    pass
                elif accion_final == 'salir':
                    break
            else:
                break

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    juego = Juego()
    juego.jugar()