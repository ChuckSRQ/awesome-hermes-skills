---
name: p5js
description: "Production pipeline for interactive and generative visual art using p5.js. Creates browser-based sketches, generative art, data visualizations, interactive experiences, 3D scenes, audio-reactive visuals, and motion graphics — exported as HTML, PNG, GIF, MP4, or SVG. Covers: 2D/3D rendering, noise and particle systems, flow fields, shaders (GLSL), pixel manipulation, kinetic typography, WebGL scenes, audio analysis, mouse/keyboard interaction, and headless high-res export. Use when users request: p5.js sketches, creative coding, generative art, interactive visualizations, canvas animations, browser-based visual art, data viz, shader effects, or any p5.js project."
version: 1.0.0
metadata:
  hermes:
    tags: [creative-coding, generative-art, p5js, canvas, interactive, visualization, webgl, shaders, animation]
    related_skills: [ascii-video, manim-video, excalidraw]
---

# p5.js Production Pipeline

## Creative Standard

This is visual art rendered in the browser. The canvas is the medium; the algorithm is the brush.

**Before writing a single line of code**, articulate the creative concept. What does this piece communicate? What makes the viewer stop scrolling? What separates this from a code tutorial example? The user's prompt is a starting point — interpret it with creative ambition.

**First-render excellence is non-negotiable.** The output must be visually striking on first load. If it looks like a p5.js tutorial exercise, a default configuration, or "AI-generated creative coding," it is wrong. Rethink before shipping.

---

## DaVinci Design Foundation

Before choosing colors, typography, or composition for any project, read this section. These principles apply to ALL visual output — generative art, diagrams, animations, web designs, and creative coding.

### The #1 Rule: Restraint Signals Quality

**Luxury = what you remove, not what you add.**

The single most important difference between amateur and professional visual output:
- Amateurs: more colors, more effects, more detail, more everything
- Professionals: fewer things, each chosen with more care

Every element you add dilutes the impact of every other element. A palette of 3 colors used consistently beats 10 colors used randomly. A single animation done beautifully beats five animations done mediocrely.

**Rule of thumb:** If you can't explain why each element is there, remove it.

### Color Theory Basics

**Build palettes intentionally, not arbitrarily.**

A good palette has:
- **1 dominant hue** (60-70% of visual space) — the mood setter
- **1 secondary hue** (20-30%) — supports the dominant, not competing
- **1 accent** (5-10%) — the pop that draws attention to what matters

**Never use more than one saturated color at full intensity.** Saturated colors fight each other. Muted tones create harmony.

**Color temperature matters.** Warm colors (reds, oranges, yellows) feel intimate, energetic, organic. Cool colors (blues, teals, purples) feel distant, calm, technical. Mixing warm and cool in one piece creates tension — use it intentionally.

**The accent rule:** Gold (#C9A84C or similar warm yellow-brass) works as an accent on both dark AND light backgrounds. Navy (#0A1628) works as an authority color. Muted sage green works with warm neutrals. When in doubt, gold or brass as accent never looks cheap.

**Avoid at all costs:**
- Bright primary colors (red, blue, green) as dominant hues
- Random hex codes chosen because they "looked ok"
- More than 2-3 distinct hues in one piece

### Typography Intuition

**Pair one serif with one sans-serif, or use one family at multiple weights.**

- Headlines: Playfair Display, Cormorant, Libre Baskerville (editorial serif)
- Body/UI: Inter, DM Sans, Source Sans (clean geometric sans)
- Never mix more than 2 font families in one piece

**Type scale hierarchy (minimum):**
- Display: 48-72px (titles, hero text)
- Heading: 24-36px (section titles)
- Body: 16-18px (paragraphs, descriptions)
- Caption: 12-14px (labels, fine print)

**White space is not empty space.** It gives the eye a place to rest and signals that the content is curated, not crammed.

### Visual Anti-Patterns (The "AI-Generated" Tell)

These scream "made by AI with no design judgment":

1. **Rainbow palettes** — using many saturated colors that weren't deliberately chosen
2. **Gradient backgrounds on everything** — gradients as a substitute for not knowing how to create depth
3. **Default p5.js colorMode(RGB, 255)** — RGB at max values creates harsh, unmixed colors
4. **No dominant color** — equal visual weight everywhere means nothing stands out
5. **Flat white or pure black backgrounds** — always add subtle texture, gradient, or tint
6. **Random-feeling positions** — elements without deliberate spacing or grid
7. **Too many fonts** — more than 2 font families feels chaotic
8. **Generic "creative coding" look** — white background, primary colors, basic shapes

### What Makes a Piece Feel "Chosen, Not Generated"

A viewer should feel that a human with taste made deliberate choices:
- Colors feel like they belong to a specific world (ocean at dusk, desert heat, midnight code)
- Shapes have personality (not just circles and squares — modified, layered, textured)
- Motion has intention (not everything moves at the same speed or direction)
- Details reward close inspection (a texture, a shadow, a layering that isn't obvious at first glance)
- The overall piece could be described in one evocative phrase: "the feeling of sand between your toes at golden hour" not "a particle system with noise"

### Reference Vocabulary

Learn to think in these dimensions:
- **Temperature:** warm vs. cool vs. neutral
- **Saturation:** vivid vs. muted vs. neutral gray
- **Value:** light vs. dark vs. mid-tone
- **Contrast:** high (dramatic) vs. low (subtle, calm)
- **Density:** sparse (breathable) vs. rich (layered, intense)
- **Texture:** smooth vs. grainy vs. geometric vs. organic
- **Motion quality:** smooth/eased vs. mechanical/stepped vs. organic/noise-driven

When you receive a creative request, map it to these dimensions BEFORE choosing colors and shapes.

---

## Creative Standard (Continued)

**Go beyond the reference vocabulary.** The noise functions, particle systems, color palettes, and shader effects in the references are a starting vocabulary. For every project, combine, layer, and invent. The catalog is a palette of paints — you write the painting.

**Be proactively creative.** If the user asks for "a particle system," deliver a particle system with emergent flocking behavior, trailing ghost echoes, palette-shifted depth fog, and a background noise field that breathes. Include at least one visual detail the user didn't ask for but will appreciate.

**Dense, layered, considered.** Every frame should reward viewing. Never flat white backgrounds. Always compositional hierarchy. Always intentional color. Always micro-detail that only appears on close inspection.

**Cohesive aesthetic over feature count.** All elements must serve a unified visual language — shared color temperature, consistent stroke weight vocabulary, harmonious motion speeds. A sketch with ten unrelated effects is worse than one with three that belong together.

## Modes

| Mode | Input | Output | Reference |
|------|-------|--------|-----------|
| **Generative art** | Seed / parameters | Procedural visual composition (still or animated) | `references/visual-effects.md` |
| **Data visualization** | Dataset / API | Interactive charts, graphs, custom data displays | `references/interaction.md` |
| **Interactive experience** | None (user drives) | Mouse/keyboard/touch-driven sketch | `references/interaction.md` |
| **Animation / motion graphics** | Timeline / storyboard | Timed sequences, kinetic typography, transitions | `references/animation.md` |
| **3D scene** | Concept description | WebGL geometry, lighting, camera, materials | `references/webgl-and-3d.md` |
| **Image processing** | Image file(s) | Pixel manipulation, filters, mosaic, pointillism | `references/visual-effects.md` § Pixel Manipulation |
| **Audio-reactive** | Audio file / mic | Sound-driven generative visuals | `references/interaction.md` § Audio Input |

## Stack

Single self-contained HTML file per project. No build step required.

| Layer | Tool | Purpose |
|-------|------|---------|
| Core | p5.js 1.11.3 (CDN) | Canvas rendering, math, transforms, event handling |
| 3D | p5.js WebGL mode | 3D geometry, camera, lighting, GLSL shaders |
| Audio | p5.sound.js (CDN) | FFT analysis, amplitude, mic input, oscillators |
| Export | Built-in `saveCanvas()` / `saveGif()` / `saveFrames()` | PNG, GIF, frame sequence output |
| Capture | CCapture.js (optional) | Deterministic framerate video capture (WebM, GIF) |
| Headless | Puppeteer + Node.js (optional) | Automated high-res rendering, MP4 via ffmpeg |
| SVG | p5.js-svg 1.6.0 (optional) | Vector output for print — requires p5.js 1.x |
| Natural media | p5.brush (optional) | Watercolor, charcoal, pen — requires p5.js 2.x + WEBGL |
| Texture | p5.grain (optional) | Film grain, texture overlays |
| Fonts | Google Fonts / `loadFont()` | Custom typography via OTF/TTF/WOFF2 |

### Version Note

**p5.js 1.x** (1.11.3) is the default — stable, well-documented, broadest library compatibility. Use this unless a project requires 2.x features.

**p5.js 2.x** (2.2+) adds: `async setup()` replacing `preload()`, OKLCH/OKLAB color modes, `splineVertex()`, shader `.modify()` API, variable fonts, `textToContours()`, pointer events. Required for p5.brush. See `references/core-api.md` § p5.js 2.0.

## Pipeline

Every project follows the same 6-stage path:

```
CONCEPT → DESIGN → CODE → PREVIEW → EXPORT → VERIFY
```

1. **CONCEPT** — Articulate the creative vision: mood, color world, motion vocabulary, what makes this unique
2. **DESIGN** — Choose mode, canvas size, interaction model, color system, export format. Map concept to technical decisions
3. **CODE** — Write single HTML file with inline p5.js. Structure: globals → `preload()` → `setup()` → `draw()` → helpers → classes → event handlers
4. **PREVIEW** — Open in browser, verify visual quality. Test at target resolution. Check performance
5. **EXPORT** — Capture output: `saveCanvas()` for PNG, `saveGif()` for GIF, `saveFrames()` + ffmpeg for MP4, Puppeteer for headless batch
6. **VERIFY** — Does the output match the concept? Is it visually striking at the intended display size? Would you frame it?

## Creative Direction

### Aesthetic Dimensions

| Dimension | Options | Reference |
|-----------|---------|-----------|
| **Color system** | HSB/HSL, RGB, named palettes, procedural harmony, gradient interpolation | `references/color-systems.md` |
| **Noise vocabulary** | Perlin noise, simplex, fractal (octaved), domain warping, curl noise | `references/visual-effects.md` § Noise |
| **Particle systems** | Physics-based, flocking, trail-drawing, attractor-driven, flow-field following | `references/visual-effects.md` § Particles |
| **Shape language** | Geometric primitives, custom vertices, bezier curves, SVG paths | `references/shapes-and-geometry.md` |
| **Motion style** | Eased, spring-based, noise-driven, physics sim, lerped, stepped | `references/animation.md` |
| **Typography** | System fonts, loaded OTF, `textToPoints()` particle text, kinetic | `references/typography.md` |
| **Shader effects** | GLSL fragment/vertex, filter shaders, post-processing, feedback loops | `references/webgl-and-3d.md` § Shaders |
| **Composition** | Grid, radial, golden ratio, rule of thirds, organic scatter, tiled | `references/core-api.md` § Composition |
| **Interaction model** | Mouse follow, click spawn, drag, keyboard state, scroll-driven, mic input | `references/interaction.md` |
| **Blend modes** | `BLEND`, `ADD`, `MULTIPLY`, `SCREEN`, `DIFFERENCE`, `EXCLUSION`, `OVERLAY` | `references/color-systems.md` § Blend Modes |
| **Layering** | `createGraphics()` offscreen buffers, alpha compositing, masking | `references/core-api.md` § Offscreen Buffers |
| **Texture** | Perlin surface, stippling, hatching, halftone, pixel sorting | `references/visual-effects.md` § Texture Generation |

### Per-Project Variation Rules

Never use default configurations. For every project:
- **Custom color palette** — never raw `fill(255, 0, 0)`. Always a designed palette with 3-7 colors
- **Custom stroke weight vocabulary** — thin accents (0.5), medium structure (1-2), bold emphasis (3-5)
- **Background treatment** — never plain `background(0)` or `background(255)`. Always textured, gradient, or layered
- **Motion variety** — different speeds for different elements. Primary at 1x, secondary at 0.3x, ambient at 0.1x
- **At least one invented element** — a custom particle behavior, a novel noise application, a unique interaction response

### Project-Specific Invention

For every project, invent at least one of:
- A custom color palette matching the mood (not a preset)
- A novel noise field combination (e.g., curl noise + domain warp + feedback)
- A unique particle behavior (custom forces, custom trails, custom spawning)
- An interaction mechanic the user didn't request but that elevates the piece
- A compositional technique that creates visual hierarchy

### Parameter Design Philosophy

Parameters should emerge from the algorithm, not from a generic menu. Ask: "What properties of *this* system should be tunable?"

**Good parameters** expose the algorithm's character:
- **Quantities** — how many particles, branches, cells (controls density)
- **Scales** — noise frequency, element size, spacing (controls texture)
- **Rates** — speed, growth rate, decay (controls energy)
- **Thresholds** — when does behavior change? (controls drama)
- **Ratios** — proportions, balance between forces (controls harmony)

**Bad parameters** are generic controls unrelated to the algorithm:
- "color1", "color2", "size" — meaningless without context
- Toggle switches for unrelated effects
- Parameters that only change cosmetics, not behavior

Every parameter should change how the algorithm *thinks*, not just how it *looks*. A "turbulence" parameter that changes noise octaves is good. A "particle size" slider that only changes `ellipse()` radius is shallow.

## Workflow

### Step 1: Creative Vision

Before any code, articulate:

- **Mood / atmosphere**: What should the viewer feel? Contemplative? Energized? Unsettled? Playful?
- **Visual story**: What happens over time (or on interaction)? Build? Decay? Transform? Oscillate?
- **Color world**: Warm/cool? Monochrome? Complementary? What's the dominant hue? The accent?
- **Shape language**: Organic curves? Sharp geometry? Dots? Lines? Mixed?
- **Motion vocabulary**: Slow drift? Explosive burst? Breathing pulse? Mechanical precision?
- **What makes THIS different**: What is the one thing that makes this sketch unique?

Map the user's prompt to aesthetic choices. "Relaxing generative background" demands different everything from "glitch data visualization."

### Step 2: Technical Design

- **Mode** — which of the 7 modes from the table above
- **Canvas size** — landscape 1920x1080, portrait 1080x1920, square 1080x1080, or responsive `windowWidth/windowHeight`
- **Renderer** — `P2D` (default) or `WEBGL` (for 3D, shaders, advanced blend modes)
- **Frame rate** — 60fps (interactive), 30fps (ambient animation), or `noLoop()` (static generative)
- **Export target** — browser display, PNG still, GIF loop, MP4 video, SVG vector
- **Interaction model** — passive (no input), mouse-driven, keyboard-driven, audio-reactive, scroll-driven
- **Viewer UI** — for interactive generative art, start from `templates/viewer.html` which provides seed navigation, parameter sliders, and download. For simple sketches or video export, use bare HTML

### Step 3: Code the Sketch

For **interactive generative art** (seed exploration, parameter tuning): start from `templates/viewer.html`. Read the template first, keep the fixed sections (seed nav, actions), replace the algorithm and parameter controls. This gives the user seed prev/next/random/jump, parameter sliders with live update, and PNG download — all wired up.

For **animations, video export, or simple sketches**: use bare HTML:

Single HTML file. Structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Project Name</title>
  <script>p5.disableFriendlyErrors = true;</script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.11.3/p5.min.js"></script>
  <!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.11.3/addons/p5.sound.min.js"></script> -->
  <!-- <script src="https://unpkg.com/p5.js-svg@1.6.0"></script> -->  <!-- SVG export -->
  <!-- <script src="https://cdn.jsdelivr.net/npm/ccapture.js-npmfixed/build/CCapture.all.min.js"></script> -->  <!-- video capture -->
  <style>
    html, body { margin: 0; padding: 0; overflow: hidden; }
    canvas { display: block; }
  </style>
</head>
<body>
<script>
// === Configuration ===
const CONFIG = {
  seed: 42,
  // ... project-specific params
};

// === Color Palette ===
const PALETTE = {
  bg: '#0a0a0f',
  primary: '#e8d5b7',
  // ...
};

// === Global State ===
let particles = [];

// === Preload (fonts, images, data) ===
function preload() {
  // font = loadFont('...');
}

// === Setup ===
function setup() {
  createCanvas(1920, 1080);
  randomSeed(CONFIG.seed);
  noiseSeed(CONFIG.seed);
  colorMode(HSB, 360, 100, 100, 100);
  // Initialize state...
}

// === Draw Loop ===
function draw() {
  // Render frame...
}

// === Helper Functions ===
// ...

// === Classes ===
class Particle {
  // ...
}

// === Event Handlers ===
function mousePressed() { /* ... */ }
function keyPressed() { /* ... */ }
function windowResized() { resizeCanvas(windowWidth, windowHeight); }
</script>
</body>
</html>
```

Key implementation patterns:
- **Seeded randomness**: Always `randomSeed()` + `noiseSeed()` for reproducibility
- **Color mode**: Use `colorMode(HSB, 360, 100, 100, 100)` for intuitive color control
- **State separation**: CONFIG for parameters, PALETTE for colors, globals for mutable state
- **Class-based entities**: Particles, agents, shapes as classes with `update()` + `display()` methods
- **Offscreen buffers**: `createGraphics()` for layered composition, trails, masks

### Step 4: Preview & Iterate

- Open HTML file directly in browser — no server needed for basic sketches
- For `loadImage()`/`loadFont()` from local files: use `scripts/serve.sh` or `python3 -m http.server`
- Chrome DevTools Performance tab to verify 60fps
- Test at target export resolution, not just the window size
- Adjust parameters until the visual matches the concept from Step 1

### Step 5: Export

| Format | Method | Command |
|--------|--------|---------|
| **PNG** | `saveCanvas('output', 'png')` in `keyPressed()` | Press 's' to save |
| **High-res PNG** | Puppeteer headless capture | `node scripts/export-frames.js sketch.html --width 3840 --height 2160 --frames 1` |
| **GIF** | `saveGif('output', 5)` — captures N seconds | Press 'g' to save |
| **Frame sequence** | `saveFrames('frame', 'png', 10, 30)` — 10s at 30fps | Then `ffmpeg -i frame-%04d.png -c:v libx264 output.mp4` |
| **MP4** | Puppeteer frame capture + ffmpeg | `bash scripts/render.sh sketch.html output.mp4 --duration 30 --fps 30` |
| **SVG** | `createCanvas(w, h, SVG)` with p5.js-svg | `save('output.svg')` |

### Step 6: Quality Verification

- **Does it match the vision?** Compare output to the creative concept. If it looks generic, go back to Step 1
- **Resolution check**: Is it sharp at the target display size? No aliasing artifacts?
- **Performance check**: Does it hold 60fps in browser? (30fps minimum for animations)
- **Color check**: Do the colors work together? Test on both light and dark monitors
- **Edge cases**: What happens at canvas edges? On resize? After running for 10 minutes?

## Critical Implementation Notes

### Performance — Disable FES First

The Friendly Error System (FES) adds up to 10x overhead. Disable it in every production sketch:

```javascript
p5.disableFriendlyErrors = true;  // BEFORE setup()

function setup() {
  pixelDensity(1);  // prevent 2x-4x overdraw on retina
  createCanvas(1920, 1080);
}
```

In hot loops (particles, pixel ops), use `Math.*` instead of p5 wrappers — measurably faster:

```javascript
// In draw() or update() hot paths:
let a = Math.sin(t);          // not sin(t)
let r = Math.sqrt(dx*dx+dy*dy); // not dist() — or better: skip sqrt, compare magSq
let v = Math.random();        // not random() — when seed not needed
let m = Math.min(a, b);       // not min(a, b)
```

Never `console.log()` inside `draw()`. Never manipulate DOM in `draw()`. See `references/troubleshooting.md` § Performance.

### Seeded Randomness — Always

Every generative sketch must be reproducible. Same seed, same output.

```javascript
function setup() {
  randomSeed(CONFIG.seed);
  noiseSeed(CONFIG.seed);
  // All random() and noise() calls now deterministic
}
```

Never use `Math.random()` for generative content — only for performance-critical non-visual code. Always `random()` for visual elements. If you need a random seed: `CONFIG.seed = floor(random(99999))`.

### Generative Art Platform Support (fxhash / Art Blocks)

For generative art platforms, replace p5's PRNG with the platform's deterministic random:

```javascript
// fxhash convention
const SEED = $fx.hash;              // unique per mint
const rng = $fx.rand;               // deterministic PRNG
$fx.features({ palette: 'warm', complexity: 'high' });

// In setup():
randomSeed(SEED);   // for p5's noise()
noiseSeed(SEED);

// Replace random() with rng() for platform determinism
let x = rng() * width;  // instead of random(width)
```

See `references/export-pipeline.md` § Platform Export.

### Color Mode — Use HSB

HSB (Hue, Saturation, Brightness) is dramatically easier to work with than RGB for generative art:

```javascript
colorMode(HSB, 360, 100, 100, 100);
// Now: fill(hue, sat, bri, alpha)
// Rotate hue: fill((baseHue + offset) % 360, 80, 90)
// Desaturate: fill(hue, sat * 0.3, bri)
// Darken: fill(hue, sat, bri * 0.5)
```

Never hardcode raw RGB values. Define a palette object, derive variations procedurally. See `references/color-systems.md`.

### Noise — Multi-Octave, Not Raw

Raw `noise(x, y)` looks like smooth blobs. Layer octaves for natural texture:

```javascript
function fbm(x, y, octaves = 4) {
  let val = 0, amp = 1, freq = 1, sum = 0;
  for (let i = 0; i < octaves; i++) {
    val += noise(x * freq, y * freq) * amp;
    sum += amp;
    amp *= 0.5;
    freq *= 2;
  }
  return val / sum;
}
```

For flowing organic forms, use **domain warping**: feed noise output back as noise input coordinates. See `references/visual-effects.md`.

### createGraphics() for Layers — Not Optional

Flat single-pass rendering looks flat. Use offscreen buffers for composition:

```javascript
let bgLayer, fgLayer, trailLayer;
function setup() {
  createCanvas(1920, 1080);
  bgLayer = createGraphics(width, height);
  fgLayer = createGraphics(width, height);
  trailLayer = createGraphics(width, height);
}
function draw() {
  renderBackground(bgLayer);
  renderTrails(trailLayer);   // persistent, fading
  renderForeground(fgLayer);  // cleared each frame
  image(bgLayer, 0, 0);
  image(trailLayer, 0, 0);
  image(fgLayer, 0, 0);
}
```

### Performance — Vectorize Where Possible

p5.js draw calls are expensive. For thousands of particles:

```javascript
// SLOW: individual shapes
for (let p of particles) {
  ellipse(p.x, p.y, p.size);
}

// FAST: single shape with beginShape()
beginShape(POINTS);
for (let p of particles) {
  vertex(p.x, p.y);
}
endShape();

// FASTEST: pixel buffer for massive counts
loadPixels();
for (let p of particles) {
  let idx = 4 * (floor(p.y) * width + floor(p.x));
  pixels[idx] = r; pixels[idx+1] = g; pixels[idx+2] = b; pixels[idx+3] = 255;
}
updatePixels();
```

See `references/troubleshooting.md` § Performance.

### Instance Mode for Multiple Sketches

Global mode pollutes `window`. For production, use instance mode:

```javascript
const sketch = (p) => {
  p.setup = function() {
    p.createCanvas(800, 800);
  };
  p.draw = function() {
    p.background(0);
    p.ellipse(p.mouseX, p.mouseY, 50);
  };
};
new p5(sketch, 'canvas-container');
```

Required when embedding multiple sketches on one page or integrating with frameworks.

### WebGL Mode Gotchas

- `createCanvas(w, h, WEBGL)` — origin is center, not top-left
- Y-axis is inverted (positive Y goes up in WEBGL, down in P2D)
- `translate(-width/2, -height/2)` to get P2D-like coordinates
- `push()`/`pop()` around every transform — matrix stack overflows silently
- `texture()` before `rect()`/`plane()` — not after
- Custom shaders: `createShader(vert, frag)` — test on multiple browsers

### Export — Key Bindings Convention

Every sketch should include these in `keyPressed()`:

```javascript
function keyPressed() {
  if (key === 's' || key === 'S') saveCanvas('output', 'png');
  if (key === 'g' || key === 'G') saveGif('output', 5);
  if (key === 'r' || key === 'R') { randomSeed(millis()); noiseSeed(millis()); }
  if (key === ' ') CONFIG.paused = !CONFIG.paused;
}
```

### Headless Video Export — Use noLoop()

For headless rendering via Puppeteer, the sketch **must** use `noLoop()` in setup. Without it, p5's draw loop runs freely while screenshots are slow — the sketch races ahead and you get skipped/duplicate frames.

```javascript
function setup() {
  createCanvas(1920, 1080);
  pixelDensity(1);
  noLoop();                    // capture script controls frame advance
  window._p5Ready = true;      // signal readiness to capture script
}
```

The bundled `scripts/export-frames.js` detects `_p5Ready` and calls `redraw()` once per capture for exact 1:1 frame correspondence. See `references/export-pipeline.md` § Deterministic Capture.

For multi-scene videos, use the per-clip architecture: one HTML per scene, render independently, stitch with `ffmpeg -f concat`. See `references/export-pipeline.md` § Per-Clip Architecture.

### Agent Workflow

When building p5.js sketches:

1. **Write the HTML file** — single self-contained file, all code inline
2. **Open in browser** — `open sketch.html` (macOS) or `xdg-open sketch.html` (Linux)
3. **Local assets** (fonts, images) require a server: `python3 -m http.server 8080` in the project directory, then open `http://localhost:8080/sketch.html`
4. **Export PNG/GIF** — add `keyPressed()` shortcuts as shown above, tell the user which key to press
5. **Headless export** — `node scripts/export-frames.js sketch.html --frames 300` for automated frame capture (sketch must use `noLoop()` + `_p5Ready`)
6. **MP4 rendering** — `bash scripts/render.sh sketch.html output.mp4 --duration 30`
7. **Iterative refinement** — edit the HTML file, user refreshes browser to see changes
8. **Load references on demand** — use `skill_view(name="p5js", file_path="references/...")` to load specific reference files as needed during implementation

## Performance Targets

| Metric | Target |
|--------|--------|
| Frame rate (interactive) | 60fps sustained |
| Frame rate (animated export) | 30fps minimum |
| Particle count (P2D shapes) | 5,000-10,000 at 60fps |
| Particle count (pixel buffer) | 50,000-100,000 at 60fps |
| Canvas resolution | Up to 3840x2160 (export), 1920x1080 (interactive) |
| File size (HTML) | < 100KB (excluding CDN libraries) |
| Load time | < 2s to first frame |

## References

| File | Contents |
|------|----------|
| `references/core-api.md` | Canvas setup, coordinate system, draw loop, `push()`/`pop()`, offscreen buffers, composition patterns, `pixelDensity()`, responsive design |
| `references/shapes-and-geometry.md` | 2D primitives, `beginShape()`/`endShape()`, Bezier/Catmull-Rom curves, `vertex()` systems, custom shapes, `p5.Vector`, signed distance fields, SVG path conversion |
| `references/visual-effects.md` | Noise (Perlin, fractal, domain warp, curl), flow fields, particle systems (physics, flocking, trails), pixel manipulation, texture generation (stipple, hatch, halftone), feedback loops, reaction-diffusion |
| `references/animation.md` | Frame-based animation, easing functions, `lerp()`/`map()`, spring physics, state machines, timeline sequencing, `millis()`-based timing, transition patterns |
| `references/typography.md` | `text()`, `loadFont()`, `textToPoints()`, kinetic typography, text masks, font metrics, responsive text sizing |
| `references/color-systems.md` | `colorMode()`, HSB/HSL/RGB, `lerpColor()`, `paletteLerp()`, procedural palettes, color harmony, `blendMode()`, gradient rendering, curated palette library |
| `references/webgl-and-3d.md` | WEBGL renderer, 3D primitives, camera, lighting, materials, custom geometry, GLSL shaders (`createShader()`, `createFilterShader()`), framebuffers, post-processing |
| `references/interaction.md` | Mouse events, keyboard state, touch input, DOM elements, `createSlider()`/`createButton()`, audio input (p5.sound FFT/amplitude), scroll-driven animation, responsive events |
| `references/export-pipeline.md` | `saveCanvas()`, `saveGif()`, `saveFrames()`, deterministic headless capture, ffmpeg frame-to-video, CCapture.js, SVG export, per-clip architecture, platform export (fxhash), video gotchas |
| `references/troubleshooting.md` | Performance profiling, per-pixel budgets, common mistakes, browser compatibility, WebGL debugging, font loading issues, pixel density traps, memory leaks, CORS |
| `templates/viewer.html` | Interactive viewer template: seed navigation (prev/next/random/jump), parameter sliders, download PNG, responsive canvas. Start from this for explorable generative art |

---

## Creative Divergence (use only when user requests experimental/creative/unique output)

If the user asks for creative, experimental, surprising, or unconventional output, select the strategy that best fits and reason through its steps BEFORE generating code.

- **Conceptual Blending** — when the user names two things to combine or wants hybrid aesthetics
- **SCAMPER** — when the user wants a twist on a known generative art pattern
- **Distance Association** — when the user gives a single concept and wants exploration ("make something about time")

### Conceptual Blending
1. Name two distinct visual systems (e.g., particle physics + handwriting)
2. Map correspondences (particles = ink drops, forces = pen pressure, fields = letterforms)
3. Blend selectively — keep mappings that produce interesting emergent visuals
4. Code the blend as a unified system, not two systems side-by-side

### SCAMPER Transformation
Take a known generative pattern (flow field, particle system, L-system, cellular automata) and systematically transform it:
- **Substitute**: replace circles with text characters, lines with gradients
- **Combine**: merge two patterns (flow field + voronoi)
- **Adapt**: apply a 2D pattern to a 3D projection
- **Modify**: exaggerate scale, warp the coordinate space
- **Purpose**: use a physics sim for typography, a sorting algorithm for color
- **Eliminate**: remove the grid, remove color, remove symmetry
- **Reverse**: run the simulation backward, invert the parameter space

### Distance Association
1. Anchor on the user's concept (e.g., "loneliness")
2. Generate associations at three distances:
   - Close (obvious): empty room, single figure, silence
   - Medium (interesting): one fish in a school swimming the wrong way, a phone with no notifications, the gap between subway cars
   - Far (abstract): prime numbers, asymptotic curves, the color of 3am
3. Develop the medium-distance associations — they're specific enough to visualize but unexpected enough to be interesting
