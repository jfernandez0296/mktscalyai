# Tutorial · Conecta WhatsApp Business a Meta con Claude (90 s, 16:9)

1920×1080, 30 fps, 90,0 s, con voz (Gemini TTS, Charon, acelerada ×1,06), música, efectos y subtítulos. Identidad: `brand/scalyai/`.

| Escena | Tiempo | Qué muestra |
|---|---|---|
| Gancho | 0–9,8 s | WhatsApp Business → API de Meta → Claude |
| Lo que necesitas | 9,8–19 s | Cuenta de Meta Business, número verificable, acceso a Claude |
| Paso 1 | 19–29 s | Crear app de tipo negocio en developers.facebook.com y agregar WhatsApp |
| Paso 2 | 29–40 s | Agregar y verificar el número, nombre visible, ID del número |
| Paso 3 | 40–51 s | Usuario del sistema y token permanente con permisos de WhatsApp |
| Paso 4 | 51–65,5 s | Claude escribe el webhook; claves en variables de entorno |
| Paso 5 | 65,5–75 s | URL de devolución de llamada, token de verificación, suscripción a `messages` |
| Prueba | 75–80 s | El agente responde en el chat |
| Cierre | 80–90 s | "¿Necesitas un agente de IA que responda en tu WhatsApp? Yo te ayudo a configurarlo." |

Las pantallas son recreaciones simplificadas (no capturas de Meta); los números e IDs son de ejemplo y lo dicen en pantalla.

## Regenerar
```bash
STYLE="Dilo en español latinoamericano neutro, con voz cálida, segura y cercana, ritmo claro de tutorial: " ./audio/generar-segmentos-gemini.sh Charon
for f in audio/seg-orig/*.wav; do ffmpeg -y -i $f -af atempo=1.06 audio/seg/$(basename $f); done
PLAN_ONLY=1 python3 build/audio.py && python3 build/html.py && python3 build/audio.py && python3 build/html.py
npx --yes hyperframes@0.8.96 check && npx --yes hyperframes@0.8.96 render -o renders/scalyai-whatsapp-meta.mp4
```
