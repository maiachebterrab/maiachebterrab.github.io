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
