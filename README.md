# Programación Concurrente — Guía de final (FIUBA)

Apunte-PWA para preparar el **final de Programación Concurrente**: teoría completa,
diagramas Mermaid interactivos, problemas clásicos y los **finales reales resueltos**.
Mismo motor que el repo `aprendizaje-automatico` (buscador, notas, resaltador, modo
oscuro, offline) con contenido y diseño propios.

> **En vivo:** `https://TU-USUARIO.github.io/programacion-concurrente/`
> (reemplazá `TU-USUARIO` cuando lo publiques — ver [Publicar](#publicar-en-github-pages)).

---

## Índice

- [Qué incluye](#qué-incluye)
- [Contenido (19 capítulos + 3 anexos)](#contenido-19-capítulos--3-anexos)
- [Cómo usarla](#cómo-usarla)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Cómo hacer cambios](#cómo-hacer-cambios)
  - [Flujo básico](#flujo-básico)
  - [Vocabulario de marcado](#vocabulario-de-marcado)
  - [Agregar un capítulo nuevo](#agregar-un-capítulo-nuevo)
  - [Qué hace `build.py`](#qué-hace-buildpy)
- [Publicar en GitHub Pages](#publicar-en-github-pages)
- [Créditos](#créditos)

---

## Qué incluye

- **Apunte completo** de toda la materia, mapeado desde los resúmenes de cátedra,
  enriquecido con los resúmenes de las 21 clases y con las presentaciones teórica/práctica.
- **Diagramas Mermaid** interactivos, varios replicados de las diapositivas de cátedra:
  interleaving, ciclo de vida de actores, Redes de Petri (con **grafo de alcance** y
  notación `p1..p6`), DAG de MapReduce, fan-out async, 2PC, deadlocks/probe, Bully y Ring.
- **Código Rust** real por tema (Arc/Mutex, RwLock, canales mpsc, Actix, sockets…).
- **Callouts «En el final»** al cierre de cada capítulo: cómo cae exactamente el tema.
- **Anexo de finales resueltos** (16/07/2026 y 09/07/2026) + un diseño de sistema completo.
- **Banco de ejercicios** de parciales resueltos y un **glosario**.
- **PWA:** buscador, notas en Markdown (se guardan solas), resaltador, modo claro/oscuro,
  instalable y con funcionamiento **offline** (service worker).

## Contenido (19 capítulos + 3 anexos)

| # | Capítulo | Temas |
| --- | --- | --- |
| 01 | Qué es la concurrencia | programa/proceso, atomicidad, interleaving, sincronización vs comunicación |
| 02 | Procesos, threads y estados | memoria compartida, stack/PC/registros, proceso vs thread vs async, estados |
| 03 | Rust: ownership y seguridad | ownership/borrow/move, RAII, `Box`/`Rc`/`Arc`, `Send`/`Sync` |
| 04 | Panorama de modelos | estado compartido, fork-join, canales, async, actores — **cuándo usar cada uno** |
| 05 | Fork-Join y paralelismo de datos | work stealing, Rayon, Crossbeam, MapReduce, SIMD, CUDA |
| 06 | Programación asincrónica | futures, `poll`, modelo piñata, `async`/`await`, executors, `Pin`, runtimes |
| 07 | Mensajes, canales y actores | mpsc, pipes/FIFO, RPC, modelo de actores, **Actix** y ciclo de vida |
| 08 | Corrección: safety y liveness | **busy-wait / deadlock / race / starvation**, sección crítica, Coffman |
| 09 | Locks y RwLock | lock/unlock, Unix advisory, `RwLock`, guards RAII, poisoned locks |
| 10 | Semáforos, barreras y monitores | `wait`/`signal`, barreras, monitores, **monitor vs semáforo**, spurious wakeup |
| 11 | Problemas clásicos | productor-consumidor, barbero, filósofos, fumadores, lector-escritor |
| 12 | Redes de Petri | red ordinaria/general, disparo, **modelado** (asientos, buffer acotado, mutex) |
| 13 | Transacciones distribuidas y ACID | ACID, 2PC, 2PL, concurrencia optimista, timestamps |
| 14 | Deadlocks distribuidos | detección (centralizada/probe), prevención (wait-die/wound-wait) |
| 15 | Exclusión mutua y elección de líder | centralizado, Ricart-Agrawala, token ring, Bully, Ring |
| 16 | Sockets y cliente-servidor | TCP/UDP, iterativo/concurrente, syscalls, `TcpListener`/`TcpStream` |
| 17 | Ambientes distribuidos | entidad y capacidades, **acción/regla/comportamiento**, conocimiento |
| 18 | Redes y modelo OSI | capas, servicio vs protocolo, tipos de servicio, TCP/IP |
| 19 | Testing de concurrencia | `#[cfg(test)]`, mockall, inyección de dependencias, **Loom** |
| A | Finales resueltos | los 2 finales reales resueltos + diseño de sistema (venta online) |
| B | Banco de ejercicios | parciales resueltos (busy-wait, modelos, Petri, actores, V/F) |
| C | Glosario | definiciones breves de todos los términos |

## Cómo usarla

- **Leer rápido:** doble clic en `index.html`. Los diagramas se bajan por CDN, así que
  la primera vez necesitás internet.
- **Full PWA (instalar + offline + service worker):** hay que *servirla*, porque los
  service workers no corren sobre `file://`:

  ```bash
  python -m http.server 8000
  # abrir http://localhost:8000/
  ```

- **Imprimir / guardar PDF:** `resumen.html` (o el botón «PDF» dentro de la app).

## Estructura del proyecto

```
programacion-concurrente/
├── index.html              # App PWA completa            ← GENERADO por build.py
├── resumen.html            # Versión imprimible          ← GENERADO
├── resumen.md              # Mirror en Markdown          ← GENERADO
├── resumen-analitico.html  # Redirección a resumen.html
│
├── content/                # ← LA FUENTE DEL CONTENIDO (acá se edita)
│   ├── part-00-fundamentos.html          (caps. 01-03)
│   ├── part-01-modelos.html              (caps. 04-06)
│   ├── part-02-mensajes.html             (cap.  07)
│   ├── part-03-correccion-locks.html     (caps. 08-09)
│   ├── part-03b-semaforos-clasicos.html  (caps. 10-11)
│   ├── part-04-petri.html                (cap.  12)
│   ├── part-05-distribuidos.html         (caps. 13-15)
│   ├── part-05b-sockets-ambientes.html   (caps. 16-18)
│   ├── part-05c-testing.html             (cap.  19)
│   └── part-06-anexos.html               (anexos A, B, C)
├── toc.html                # Índice de la barra lateral  ← FUENTE
├── build.py                # Ensambla index/resumen desde content/ + toc.html
│
├── sw.js                   # Service worker (offline)
├── manifest.webmanifest    # Manifiesto PWA
├── pwa-icon.svg            # Ícono
├── pwa-icon-maskable.svg   # Ícono maskable
├── .gitignore
└── README.md
```

> **Regla de oro:** `index.html`, `resumen.html` y `resumen.md` son **generados**. No los
> edites a mano: se pisan en el próximo `build.py`. Tocá siempre `content/*.html` y `toc.html`.

## Cómo hacer cambios

### Flujo básico

1. Editás un archivo de `content/part-*.html` (o `toc.html`).
2. Regenerás todo:

   ```bash
   python build.py
   ```

3. Verificás en el navegador (`python -m http.server 8000`).
4. Commiteás y publicás:

   ```bash
   git add .
   git commit -m "Descripción del cambio"
   git push
   ```

   GitHub Pages se redepliega solo en ~1 minuto.

### Vocabulario de marcado

El contenido usa clases del shell (ya estilizadas en claro y oscuro). Bloques disponibles:

```html
<!-- Estructura de un capítulo -->
<section class="chapter" id="mi-id" data-title="palabras clave para el buscador">
  <div class="chapter-head">
    <div class="chapter-number">NN</div>
    <div><h2>Título del capítulo</h2></div>
  </div>

  <h3>Subtítulo</h3>
  <p>Texto normal con <strong>negrita</strong>, <em>cursiva</em> y <code>código inline</code>.</p>

  <ul class="study-list"><li>Ítem de lista de estudio</li></ul>

  <!-- Tabla (siempre envuelta en .table-wrap para scroll horizontal) -->
  <div class="table-wrap"><table>
    <thead><tr><th>Col</th></tr></thead>
    <tbody><tr><td>Dato</td></tr></tbody>
  </table></div>

  <!-- Cajas de color -->
  <div class="callout">nota</div>
  <div class="callout warning">atención</div>
  <div class="callout danger">error frecuente</div>
  <div class="callout blue">dato extra</div>

  <!-- Dos cajas lado a lado -->
  <div class="cmp two"><div class="callout">A</div><div class="callout blue">B</div></div>

  <!-- Etiquetas -->
  <span class="tag">Rust</span> <span class="tag warm">warm</span>
  <span class="tag blue">blue</span> <span class="tag red">red</span>

  <!-- Desplegable -->
  <details><summary>Título</summary><p>Contenido oculto</p></details>

  <!-- Código: usar SIEMPRE data-code (se escapan < > & solos) -->
  <pre data-code="rust">
fn main() {
    let x: Arc<Mutex<i32>> = Arc::new(Mutex::new(0)); // los < > no rompen nada
}
  </pre>

  <!-- Diagrama Mermaid (NO uses el carácter "<" literal adentro) -->
  <figure class="diagram">
    <div class="mermaid">
flowchart LR
    A --> B
    </div>
    <figcaption>Explicación del diagrama.</figcaption>
  </figure>

  <!-- Cierre "cómo cae en el final" -->
  <p class="exam-answer"><strong>En el final:</strong> ...</p>
</section>
```

**Dos reglas que importan:**

- **Código →** siempre `<pre data-code="rust">…</pre>`. `build.py` escapa `<`, `>`, `&` por
  vos, así que podés pegar Rust con genéricos (`Arc<Mutex<T>>`) sin romper el HTML.
- **Diagramas →** `<div class="mermaid">…</div>` con sintaxis Mermaid. Evitá el carácter
  `<` literal (los `-->`, `->>`, `>=` están bien porque no usan `<`).

### Agregar un capítulo nuevo

1. Escribí la `<section class="chapter" id="nuevo-id" data-title="...">…</section>` dentro
   del `content/part-*.html` que corresponda (o creá uno nuevo `part-XX-...html`; el orden
   lo da el nombre del archivo alfabéticamente).
2. Agregá el link en `toc.html`:

   ```html
   <a href="#nuevo-id"><span>NN</span>Título en el índice</a>
   ```

3. `python build.py` y listo. El buscador, el índice y `resumen.md` se actualizan solos.

### Qué hace `build.py`

Es un ensamblador en Python (sin dependencias). En cada corrida:

1. Toma el **shell probado** de `../aprendizaje-automatico/index.html` (todo su CSS y JS:
   buscador, notas, resaltador, modo oscuro, service worker).
2. Le **reemplaza** la paleta de colores, la marca, el índice (`toc.html`) y el contenido
   (concatena `content/part-*.html` en orden).
3. **Escapa** los bloques `<pre data-code>` e **inyecta** Mermaid.
4. Genera además `resumen.html` (standalone imprimible) y `resumen.md` (mirror Markdown).

> Para *rebuildear* necesitás la carpeta hermana `aprendizaje-automatico` (es la plantilla).
> El `index.html` ya generado **no** la necesita: es autocontenido y se publica solo.

## Créditos

Contenido basado en los resúmenes, presentaciones, clases y exámenes de la cátedra de
**Programación Concurrente (FIUBA)**. El motor de la interfaz (buscador, notas, resaltador,
modo oscuro, PWA) está adaptado del apunte
[`aprendizaje-automatico`](https://github.com/flopeztancredi/aprendizaje-automatico).
