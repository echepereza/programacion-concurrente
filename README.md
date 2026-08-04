# Programación Concurrente — Guía de final (FIUBA)

Apunte-PWA para preparar el **final de Programación Concurrente**: teoría completa,
diagramas Mermaid interactivos, problemas clásicos y los **finales reales resueltos**.
Motor de UI adaptado (buscador, notas, resaltador, modo oscuro, offline) con contenido
y diseño propios; el armazón vive en `template.html` y el repo es **autocontenido**.

> **En vivo:** `https://TU-USUARIO.github.io/programacion-concurrente/`
> (reemplazá `TU-USUARIO` cuando lo publiques — ver [Publicar](#publicar-en-github-pages)).

---

## Índice

- [Qué incluye](#qué-incluye)
- [Contenido (21 capítulos + 3 anexos)](#contenido-21-capítulos--3-anexos)
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
  **toggle para ocultar todo el código** (estudio teórico), instalable y **offline** (service worker).

## Contenido (21 capítulos + 3 anexos)

| # | Capítulo | Temas |
| --- | --- | --- |
| 01 | Qué es la concurrencia | programa/proceso, atomicidad, interleaving, sincronización vs comunicación |
| 02 | Procesos, threads y estados | memoria compartida, stack/PC/registros, proceso vs thread vs async, estados |
| 03 | Rust: ownership y seguridad | ownership/borrow/move, RAII, `Box`/`Rc`/`Arc`, `Send`/`Sync` |
| 04 | Panorama de modelos | estado compartido, fork-join, canales, async, actores — **cuándo usar cada uno** |
| 05 | Fork-Join y paralelismo de datos | work stealing, Rayon, Crossbeam, MapReduce, Dremel, DAG |
| 06 | Vectorización, SIMD y GPU | SIMD (lanes, vertical/horizontal), SIMT/warps, CUDA, host↔device, WebGPU |
| 07 | Programación asincrónica | futures, `poll`, modelo piñata, `async`/`await`, executors, `Pin`, runtimes |
| 08 | Mensajes y canales | mpsc, sincrónica/asincrónica, direccionamiento, pipes/FIFO, colas, RPC |
| 09 | Modelo de actores | **Actix**, mailbox, ciclo de vida, Sync Arbiter, diseñar sistemas |
| 10 | Corrección: safety y liveness | **busy-wait / deadlock / race / starvation**, sección crítica, Coffman |
| 11 | Locks y RwLock | lock/unlock, Unix advisory, `RwLock`, guards RAII, poisoned locks, atómicos |
| 12 | Semáforos, barreras y monitores | `wait`/`signal`, barreras, monitores, **monitor vs semáforo**, spurious wakeup |
| 13 | Problemas clásicos | productor-consumidor, barbero, filósofos (+ Chandy-Misra), fumadores, lector-escritor |
| 14 | Redes de Petri | red ordinaria/general, disparo, grafo de alcance, **modelado**, arco inhibidor |
| 15 | Transacciones distribuidas y ACID | ACID, 2PC (+3PC/Sagas), 2PL, concurrencia optimista, timestamps |
| 16 | Deadlocks distribuidos | detección (centralizada/probe), prevención (wait-die/wound-wait) |
| 17 | Exclusión mutua y elección de líder | centralizado, Ricart-Agrawala, token ring, Bully, Ring |
| 18 | Sockets y cliente-servidor | TCP/UDP, iterativo/concurrente, syscalls, `TcpListener`/`TcpStream` |
| 19 | Ambientes distribuidos | entidad y capacidades, **acción/regla/comportamiento**, conocimiento |
| 20 | Redes y modelo OSI | capas, PDUs, servicio vs protocolo, tipos de servicio, TCP/IP |
| 21 | Testing de concurrencia | `#[cfg(test)]`, mockall, inyección de dependencias, **Loom** |
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

- **Imprimir / guardar PDF:** botón «PDF» dentro de la app (funciona igual en el apunte y en el repaso final).
- **Repaso final:** botón «Repaso final» de la barra lateral. Es otra página (`repaso-final.html`) con el **mismo armazón** (índice, notas, buscador, tema): intercambia el contenido por el resumen compacto para el final, igual que aprendizaje-automatico alterna entre su Apunte y su Resumen. Desde ahí, «Apunte» vuelve al apunte completo.

## Estructura del proyecto

```
programacion-concurrente/
├── index.html              # App PWA: apunte completo    ← GENERADO por build.py
├── repaso-final.html       # App PWA: repaso compacto (mismo shell) ← GENERADO
├── repaso-final.md         # Mirror del repaso en Markdown ← GENERADO
│
├── content/                # ← LA FUENTE DEL CONTENIDO (acá se edita)
│   ├── part-00-fundamentos.html          (caps. 01-03)
│   ├── part-01-modelos.html              (caps. 04-05)
│   ├── part-01b-vectorizacion.html       (cap.  06)
│   ├── part-01c-async.html               (cap.  07)
│   ├── part-02-mensajes.html             (cap.  08)
│   ├── part-02b-actores.html             (cap.  09)
│   ├── part-03-correccion-locks.html     (caps. 10-11)
│   ├── part-03b-semaforos-clasicos.html  (caps. 12-13)
│   ├── part-04-petri.html                (cap.  14)
│   ├── part-05-distribuidos.html         (caps. 15-17)
│   ├── part-05b-sockets-ambientes.html   (caps. 18-20)
│   ├── part-05c-testing.html             (cap.  21)
│   ├── part-06-anexos.html               (anexos A, B, C)
│   └── repaso-final.html                 (repaso compacto para el final)
├── toc.html                # Índice del apunte           ← FUENTE
├── toc-repaso.html         # Índice del repaso final      ← FUENTE
├── template.html           # Armazón (shell CSS/JS) con 5 placeholders ← FUENTE
├── build.py                # Rellena template.html con content/ + tocs (autocontenido)
│
├── sw.js                   # Service worker (offline)
├── manifest.webmanifest    # Manifiesto PWA
├── pwa-icon.svg            # Ícono
├── pwa-icon-maskable.svg   # Ícono maskable
├── .gitignore
└── README.md
```

> **Regla de oro:** `index.html`, `repaso-final.html` y `repaso-final.md` son
> **generados**. No los edites a mano: se pisan en el próximo `build.py`. Tocá siempre
> `content/*.html` y `toc.html`.
>
> El **Repaso final** (`content/repaso-final.html` → `repaso-final.html`) es el resumen
> compacto y orientado a finales: el mínimo teórico para aprobar, con bullets, tablas y
> definiciones. Es una página aparte con el mismo shell que el apunte (se navega con los
> botones «Repaso final» / «Apunte» de la barra lateral) y su fuente es independiente
> (no se concatena con los `part-*.html`).

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

3. `python build.py` y listo. El buscador, el índice y el `repaso-final.md` se actualizan solos.

### Qué hace `build.py`

Es un ensamblador en Python (sin dependencias) y **autocontenido**: el armazón vive en
`template.html` (CSS y JS del buscador, notas, resaltador, modo oscuro y service worker,
con la marca, la paleta, los estilos y los scripts ya horneados). `template.html` expone
cinco puntos de inyección — `<!--PAGE-TITLE-->`, `<!--DESCRIPTION-->`, `<!--TOC-->`,
`<!--NAV-LINK-->` y `<!--CONTENT-->` — y `build.py` solo los rellena (con `str.replace`,
sin regex ni marcadores heredados). En cada corrida:

1. Escapa los bloques `<pre data-code>` (a `<`/`>`/`&`) y concatena `content/part-*.html`.
2. Arma **dos páginas con el mismo shell**: `index.html` (apunte, índice `toc.html`, enlace →
   «Repaso final») y `repaso-final.html` (repaso compacto, índice propio `toc-repaso.html` con
   anclas in-page para que el buscador y la navegación funcionen dentro del repaso, enlace →
   «Apunte»). Cada sección del repaso es un `.chapter` con `id` y `data-title` (igual que el
   apunte), así el buscador la indexa. Genera también `repaso-final.md` (mirror Markdown).

> El build **no depende de ningún repo externo**: `template.html` es la plantilla y vive acá.
> Si querés tocar el armazón (estilos, scripts, paleta, marca), se edita `template.html`.

## Créditos

Contenido basado en los resúmenes, presentaciones, clases y exámenes de la cátedra de
**Programación Concurrente (FIUBA)**. El motor de la interfaz (buscador, notas, resaltador,
modo oscuro, PWA) está adaptado del apunte
[`aprendizaje-automatico`](https://github.com/flopeztancredi/aprendizaje-automatico).
