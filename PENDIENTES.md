# Pendientes de la web

*Al 16 de septiembre de 2026*

## Material que falta de Maia

- [x] ~~Fotos del acordeón físico de Salto de Fe.~~ Entró una, recortada, en
      `Salto de Fe/acordeon/`. **Mejorable**: está sobre una sábana arrugada y con
      luz mezclada. Si se puede rehacer —fondo liso y oscuro, luz pareja, más de
      un ángulo— la sección gana bastante. `sumar_acordeon.py` toma lo que haya
      en esa carpeta.
- [ ] **Medios públicos: comitente, año y rol.** Es la única marca `[ falta ]`
      que queda en la web. Importa el rol: en Behance el proyecto figura como
      *Multiple Owners* y es el único donde la autoría no queda clara.
- [ ] **Colección de libros**: confirmar que sea sobre las obras completas de
      Samanta Schweblin. La bajada salió de leer la primera pieza, no de Behance,
      que para ese proyecto no tiene descripción.

## Decisiones abiertas

- [ ] **Mono o sans.** `index.html` está en Geist Mono, `index-sans.html` en
      Geist Sans. Si gana la sans hay que bajar los woff2 para no depender de
      Google Fonts.
- [ ] **Paneles del alfabeto**: son blancos y sobre el fondo negro se leen como
      bloques claros. Se dejaron así a propósito.
- [ ] **Orden de los proyectos** dentro de cada grupo.
- [ ] **Fascículos**: en Behance están las reseñas completas de Leila Guerriero,
      María Moreno y Juan Forn. Hoy la bajada solo las nombra.
- [ ] **Plaquette Perec**: la cita de *Pensar/Clasificar* está en Behance y no se
      usó. Puede ir como epígrafe.
- [ ] **Cátedra**: en Behance figura como "Ex-Manela". La web dice Ex-Manela.

## Técnico

- [ ] **El loop del acordeón** funciona fino solo publicado en el mismo dominio,
      donde se puede leer su scroll. En local cae a una recarga por tiempo.
      El arreglo de fondo es una línea en el repo `salto-de-fe`, para que loopee
      por sí mismo.
- [ ] **El GIF de cierre de Medios públicos** se estira de 600 a 1512 px y se ve
      blando. La única versión nítida que sirve Behance pesa 17,9 MB.
- [ ] **Publicar**: falta registrar la clave SSH, crear el repo `portfolio`
      público y prender Pages. Los commits ya están listos para pushear.

## Para el PDF de entrega

`index-claro.html` se mantiene en paralelo desde el mismo código: un PDF todo
negro es impracticable de imprimir.
