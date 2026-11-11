# Scaly AI · "¿Qué pasa en las primeras 2 semanas de un piloto?" (1:01)

Dos formatos desde el mismo generador: `FMT=h` → 1920×1080 (`renders/scalyai-piloto-2semanas-16x9.mp4`), `FMT=v` → 1080×1920 (`renders/scalyai-piloto-2semanas-9x16.mp4`). Voz Gemini TTS (gemini-3.1-flash-tts-preview, Charon). Base común en `build/lib.py`.

Escenas: gancho con calendario de 14 días → calendario que se ilumina por etapas (días 1–2, 3–5, semana 2, día 14) con una tarjeta por etapa → CTA "Empezamos con un piloto, no con una apuesta".

El reparto por días es un **calendario de ejemplo** (lo dice en pantalla); lo real es: piloto de 2 semanas, un proceso, conectar herramientas, ROI medible en 6 semanas.

```bash
./audio/generar-segmentos-gemini.sh Charon "" gemini-3.1-flash-tts-preview
PLAN_ONLY=1 python3 build/audio.py && FMT=h python3 build/html.py && python3 build/audio.py
FMT=h python3 build/html.py && npx --yes hyperframes@0.8.96 render -o renders/scalyai-piloto-2semanas-16x9.mp4
FMT=v python3 build/html.py && npx --yes hyperframes@0.8.96 render -o renders/scalyai-piloto-2semanas-9x16.mp4
```
