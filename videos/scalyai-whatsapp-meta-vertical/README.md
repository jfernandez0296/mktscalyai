# Tutorial · Conecta WhatsApp Business a Meta desde Claude (90 s, 16:9)

1920×1080, 30 fps, 90,0 s, con voz (Gemini TTS, Charon, velocidad natural), música, efectos y subtítulos. Identidad: `brand/scalyai/`.

| Escena | Tiempo | Qué muestra |
|---|---|---|
| Gancho | 0–7,3 s | "Hazlo desde Claude": WhatsApp Business → API de Meta → Claude |
| Lo que necesitas | 7,3–18 s | Claude Code, Claude en Chrome, cuenta de Meta Business; "Tú apruebas cada paso" |
| Paso 1 | 18–31 s | Tú → Claude: crear la app de tipo negocio y agregar WhatsApp; Claude completa el formulario en Chrome |
| Paso 2 | 31–41 s | Claude agrega el número; tú le das el código SMS; Claude anota el ID |
| Paso 3 | 41–52 s | Claude crea el usuario del sistema y el token; tú lo guardas como variable de entorno |
| Paso 4 | 52–64,7 s | Claude Code escribe y publica el webhook con la API de Claude |
| Paso 5 | 64,7–74,5 s | Claude conecta el webhook en Meta y lo suscribe a `messages` |
| Prueba | 74,5–79,6 s | El agente responde en el chat |
| Cierre | 79,6–90 s | "¿Necesitas un agente de IA que responda en tu WhatsApp? Yo te ayudo a configurarlo." |

Las pantallas son recreaciones simplificadas (no capturas de Meta); los números e IDs son de ejemplo y lo dicen en pantalla.

## Regenerar
```bash
STYLE="Dilo en español latinoamericano neutro, con voz cálida, segura y cercana, ritmo claro de tutorial: " ./audio/generar-segmentos-gemini.sh Charon
cp audio/seg/*.wav audio/seg-orig/   # tomas originales
PLAN_ONLY=1 python3 build/audio.py && python3 build/html.py && python3 build/audio.py && python3 build/html.py
npx --yes hyperframes@0.8.96 check && npx --yes hyperframes@0.8.96 render -o renders/scalyai-whatsapp-meta.mp4
```
