# Scaly AI · "Excel, CRM y ERP conectados" (~41 s)

Dos formatos desde el mismo generador: `FMT=h` → 1920×1080 (`renders/scalyai-integraciones-16x9.mp4`), `FMT=v` → 1080×1920 (`renders/scalyai-integraciones-9x16.mp4`). Voz Gemini TTS (gemini-3.8-flash-tts, Charon), música, efectos y subtítulos. Identidad: `brand/scalyai/`. La base común está en `build/lib.py`.

Escenas: el mismo pedido copiado tres veces (Excel, CRM, ERP) → tiempo y errores (#1042 → #1024) → "Un solo flujo" (WhatsApp, CRM, hojas de cálculo, ERP) → el pedido llega por WhatsApp y se registra en el CRM → la hoja se actualiza y el ERP descuenta stock → "Menos copiar y pegar. Más vender." → CTA.

Ilustrativo y marcado en pantalla: el pedido #1042, las 12 h, la hoja y el stock.

```bash
./audio/generar-segmentos-gemini.sh Charon "" gemini-3.8-flash-tts   # sin STYLE: este modelo lo lee en voz alta
PLAN_ONLY=1 python3 build/audio.py && FMT=h python3 build/html.py && python3 build/audio.py
FMT=h python3 build/html.py && npx --yes hyperframes@0.8.96 render -o renders/scalyai-integraciones-16x9.mp4
FMT=v python3 build/html.py && npx --yes hyperframes@0.8.96 render -o renders/scalyai-integraciones-9x16.mp4
```
