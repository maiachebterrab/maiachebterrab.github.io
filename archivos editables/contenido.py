# -*- coding: utf-8 -*-
"""Los textos y el orden del portfolio. Lo leen build_web.py y build_pdf.py,
así que editar acá alcanza para que cambien la web y el PDF a la vez."""

PRESENTACION = ("Diseño identidades y universos visuales para artistas, proyectos "
                "culturales y productoras audiovisuales. Mi práctica cruza diseño, "
                "imagen, fotografía y cultura.")

GRUPOS = [("visuales",    "Proyectos visuales"),
          ("editoriales", "Proyectos editoriales"),
          ("identidad",   "Identidad institucional")]

# dibujo original  ->  imagen que lo reformula, en el orden que va en la página
PARES = [
    ("assets/00a-dibujos/04.jpg", "assets/00d-imagenes/01.jpg", "Mi casa"),
    ("assets/00a-dibujos/02.jpg", "assets/00d-imagenes/02.jpg", "Naturaleza emocional"),
    ("assets/00a-dibujos/05.jpg", "assets/00d-imagenes/03.jpg", "Familia unida"),
]

SECCIONES = [
 {"grupo": "visuales", "id": "bestiario", "num": "01", "titulo": "Bestiario",
  "nav": "Bestiario",
  "meta": "@ Destructores de Imágenes  ·  [2026]",
  "bajada": "Proyecto realizado en el marco de Destructores de Imágenes. Partiendo de los "
            "dibujos y la caligrafía de mi infancia con la idea de llevarlos a otros "
            "universos: reformular hoy, con otras técnicas, lo que dibujé de chica.",
  # El alfabeto de Bestiario quedó afuera: esa letra ya no existe (20/9/2026).
  "proyectos": [("@pares", "Imágenes", None)]},
 {"grupo": "visuales", "id": "salto-de-fe", "num": "02", "titulo": "Salto de Fe",
  "nav": "Salto de Fe",
  "meta": "@ Creadores de Imágenes  ·  [2026]",
  "bajada": "Proyecto creado en el marco del taller Creadores de Imágenes, a cargo de Julia "
            "Sbriller. Recopilación de fotografías propias sacadas en lo cotidiano. El nombre "
            "viene de algo que me sucede recurrentemente, el encuentro de mensajes oraculares "
            "en lo que me rodea.",
  "embed": "https://maiucheb-oss.github.io/salto-de-fe/",
  "proyectos": [("@embed", None, None)]},
 {"grupo": "visuales", "id": "corazon", "num": "08", "titulo": "Corazón",
  "nav": "Corazón",
  # Fotos de Descargas/AMORYCORAZONES (21/10/2026). Sin contexto ni año por ahora.
  "meta": "",
  "bajada": "Corazones y palabras de amor encontrados en la calle.",
  # Filas de distinto tamaño para darle ritmo. Cada lista es una fila; los
  # números son los de assets/09-corazon. Una foto sola va a todo el ancho.
  # Las palabras se reparten a lo largo: abre "A Ud. estaba esperando" y
  # cierra "Emociones".
  "filas": [["17"],                    # A Ud. estaba esperando
            ["11", "06", "04"],        # SI · Ojalá · carta
            ["22"],                    # Yo Tú Él
            ["01", "15"],              # corazones ByN · ramas
            ["07", "08"],              # hoja · neón en la ventana
            ["23", "05"],              # Amor / Roma · corazón pintado
            ["03", "10", "13"],        # zapatillas · persiana · SI en el piso
            ["27"],                    # enamorarse
            ["18", "19"],              # los gatos
            ["16", "14", "20"],        # corazón de neón · luces rojas · tronco
            ["26", "28"],              # Amor Escapes · ¿Y si?
            ["02", "09", "12", "24"],  # hojas · enredadera · tela · piedra
            ["21", "25"],              # sombra en el pasto · árboles
            ["29"]],                   # Emociones
  # la tapa es el cartel de AMOR (Untitled-3-09), no la primera foto
  "portada": "assets/09-corazon/23.jpg",
  "proyectos": [("09-corazon", None, None)]},
 {"grupo": "visuales", "id": "reached", "num": "09", "titulo": "You've Reached the End",
  "nav": "You've Reached the End",
  # Video en el canal de Nikolas Schneider (21/10/2026). Sin contexto ni año por ahora.
  "meta": "",
  "bajada": "<p>Me pasa algo muy raro desde chica, que tiene que ver con una vida que "
            "transcurre adentro de mis sueños. Los recuerdo con mucha lucidez y, de alguna "
            "manera, aunque la mayoría de ellos sean pesadillas, aprendí a disfrutarlos y a "
            "sentirlos cada vez más como una película que pasa adentro mío.</p>"
            "<p><i>You’ve reached the end</i> nació de esos sueños. A partir de las primeras "
            "imágenes creadas con inteligencia artificial, con Nico empezamos a crear prompts, "
            "jugando entre descripciones directas y frases sueltas que funcionaban como "
            "oráculos.</p>"
            "<p>Con distintas herramientas fuimos entrenando al modelo de imágenes hasta dar "
            "con una estética onírica, oscura y perturbadora que imitaba casi a la perfección "
            "su origen. Cada imagen alimentaba a la siguiente, hasta volverse escenas que "
            "parecían soñarse solas.</p>"
            "<p>De ahí surgieron los videos, que fueron dando espacio a este viaje entre lo "
            "irreal y lo real. Lo que vemos acá es apenas un portal.</p>",
  "embed": "https://www.youtube-nocookie.com/embed/JxvT7eyOc_M?rel=0",
  # tapa: Dorso Espiral.jpg (en la carpeta del proyecto), no el cuadro de YouTube
  "tapa": "10-reached",
  # el video es 4:3; con el 16:9 por defecto quedaban barras negras a los costados
  "proporcion": "4/3",
  "proyectos": [("@embed", None, None)]},
 {"grupo": "editoriales", "id": "fasciculos", "num": "03", "titulo": "Fascículos coleccionables", "nav": "Fascículos",
  "meta": "@ Cátedra Ex-Manela, FADU  ·  [2023]",
  "bajada": "Colección de fascículos coleccionables a partir de columnas y ensayos de "
            "Leila Guerriero, "
"María Moreno y Juan Forn.",
  "proyectos": [("02-fasciculos-coleccionables", None, None)]},
 {"grupo": "editoriales", "id": "libros", "num": "04", "titulo": "Colección de libros", "nav": "Colección de libros",
  "meta": "@ Cátedra Ex-Manela, FADU  ·  [2024]",
  "bajada": "Colección de libros para las obras completas de Samanta Schweblin.",
  "proyectos": [("05-coleccion-de-libros", None, None)]},
 {"grupo": "editoriales", "id": "perec", "num": "05", "titulo": "Plaquette Georges Perec", "nav": "Plaquette Perec",
  "meta": "@ Cátedra Ex-Manela, FADU  ·  [2023]",
  "bajada": "Plaquette a partir de un fragmento de <i>Pensar/Clasificar</i>, de Georges Perec.",
  "proyectos": [("06-plaquette-perec", None, None)]},
 {"grupo": "identidad", "id": "espacios", "num": "06", "titulo": "Especies de Espacios",
  "nav": "Especies de Espacios",
  "meta": "@ Tipografía, FADU  ·  [2021]",
  "bajada": "Identidad para una exposición de arte: sistema visual, piezas de comunicación "
            "y su aplicación en el espacio.",
  "proyectos": [("04-identidad-exposicion-arte", "Identidad para una exposición de arte", None)]},
 {"grupo": "identidad", "id": "medios", "num": "07",
  "titulo": "Diseño estratégico en medios públicos", "nav": "Medios públicos",
  "meta": "@ Diseño Gráfico, FADU  ·  [2023]",
  "bajada": "Estrategia de comunicación e identidad digital para TV Pública y Radio Nacional: "
            "teaser, campaña, piezas institucionales y sistema para redes.",
  "proyectos": [("01-medios-publicos", None, None)]},
]
