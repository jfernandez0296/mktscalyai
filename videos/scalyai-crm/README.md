# Scaly AI · scalyai-crm (vertical 9:16)

Video vertical de 1080×1920 con voz (Gemini TTS, Charon), música, efectos y subtítulos. Identidad: `brand/scalyai/`.

- `build/spec.py`: guion visual (escenas y módulos gráficos: chat, cuadrícula, filas, flujo, embudo, indicadores, barras).
- `build/html.py`: motor común que convierte el spec en `index.html`. `build/lib.py`: base compartida.
- `audio/segmentos.json`: locución, una por escena. Todos los datos en pantalla son de ejemplo y están marcados "Ejemplo ilustrativo".

```bash
./audio/generar-segmentos-gemini.sh Charon "" gemini-3.1-flash-tts-preview   # sin STYLE
PLAN_ONLY=1 python3 build/audio.py && python3 build/html.py && python3 build/audio.py && python3 build/html.py
npx --yes hyperframes@0.8.96 check && npx --yes hyperframes@0.8.96 render -o renders/scalyai-crm-9x16.mp4
```
