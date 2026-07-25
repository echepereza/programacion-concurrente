# Programación Concurrente — Guía de final (FIUBA)

Apunte-PWA para preparar el final: teoría completa, diagramas Mermaid interactivos,
problemas clásicos y los **finales reales resueltos**. Misma arquitectura que el repo
`aprendizaje-automatico` (buscador, notas, resaltador, modo oscuro, offline).

## Cómo usarla

- **Leer rápido:** doble clic en `index.html` (abre en el navegador). Los diagramas
  Mermaid se cargan por CDN, así que en la primera apertura necesitás internet.
- **Full PWA (instalar + offline + service worker):** hay que *servirla*, porque los
  service workers no corren sobre `file://`. Desde esta carpeta:

  ```bash
  python -m http.server 8000
  # abrir http://localhost:8000/
  ```

- **Imprimir / PDF:** `resumen.html` (o botón «PDF» en la app).

## Estructura

| Archivo | Qué es |
| --- | --- |
| `index.html` | La app completa (generada). **No editar a mano.** |
| `resumen.html` / `resumen.md` | Versión imprimible / mirror Markdown (generados). |
| `content/part-*.html` | **La fuente del contenido.** Acá se escribe/edita. |
| `toc.html` | Índice de la barra lateral. |
| `build.py` | Ensambla `index.html` + `resumen.html` + `resumen.md`. |
| `sw.js`, `manifest.webmanifest`, `pwa-icon*.svg` | Plomería de la PWA. |

## Rebuild

Editás un `content/part-*.html` (o `toc.html`) y regenerás todo:

```bash
python build.py
```

`build.py` reutiliza el shell probado de `../aprendizaje-automatico/index.html`
(todo su CSS/JS) y le inyecta el contenido, el índice y la marca. Los bloques de código
van como `<pre data-code="rust">…</pre>` (se escapan solos) y los diagramas como
`<div class="mermaid">…</div>` (evitá el carácter `<` literal adentro).

## Contenido (18 capítulos + 3 anexos)

1. Fundamentos · 2. Threads y procesos · 3. Rust: ownership/Send/Sync
4. Modelos (elegir modelo) · 5. Fork-Join · 6. Async · 7. Mensajes y actores
8. Corrección (safety/liveness) · 9. Locks · 10. Semáforos/monitores · 11. Problemas clásicos
12. Redes de Petri · 13. Transacciones/ACID · 14. Deadlocks distribuidos
15. Exclusión mutua y líder · 16. Sockets · 17. Ambientes distribuidos · 18. Redes/OSI
· A. Finales resueltos · B. Banco de ejercicios · C. Glosario
