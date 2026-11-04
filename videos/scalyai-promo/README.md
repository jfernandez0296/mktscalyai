# Scaly AI · promo 60 s (16:9)

Video promocional de 60,0 s en 1920×1080 a 30 fps, en español, con locución, música y efectos. Usa la identidad de `brand/scalyai/` (Guía de diseño v1).

## Escenas
| # | Tiempo | Escena | Voz |
|---|---|---|---|
| A | 0–6 s | Noche (azul medianoche): 11:40 p. m., un cliente escribe por WhatsApp, "Sin respuesta" sube hasta 8 h | "Son las once y cuarenta de la noche…" |
| B | 6–13 s | "De día, todo a mano.": cuatro tareas pendientes + "12 h a la semana" | "De día, tu equipo copia pedidos a Excel…" |
| C | 13–20 s | Marca: las barras del logo crecen en secuencia y aparece el hero "Construimos software e IA a la medida de tu negocio." | "Esto es Scaly AI…" |
| D | 20–27,5 s | "Responde en segundos.": celular con el asistente, recibo "Pedido #1042 registrado en tu CRM" y ficha CRM | "Un asistente con IA responde en WhatsApp…" |
| E | 27,5–35 s | "Automatizamos lo repetitivo.": CRM, WhatsApp, hojas de cálculo y ERP conectados; las tareas pasan a "Automático" | "Conectamos tu CRM…" |
| F | 35–41 s | "Ponemos tus datos a trabajar." (oscura): 1.240 pedidos, 18 h, 24/7 y gráfico manual vs. automatizado | "Y ponemos tus datos a trabajar…" |
| G | 41–49,5 s | "Empezamos con un piloto.": 01 proceso · 02 en 2 semanas · 03 ROI medible en 6 semanas | "Empezamos con un piloto…" |
| H | 49,5–60 s | Cierre (oscuro): logo, lema, botón "Conversemos de tu próximo piloto →", "30 minutos · sin tarjeta · sin compromiso", scalyai.dev | "Conversemos de tu próximo piloto…" |

Transiciones: las tres barras del logo cruzan la pantalla (A→B, C→D, E→F, G→H), fundido (B→C) y cortina lateral (D→E, F→G). Movimiento según la guía: fundido + desplazamiento corto, sin rebotes ni giros.

**Datos ilustrativos** (marcados en pantalla): el caso de las 11:40 p. m., el pedido #1042, 12 h, 1.240 pedidos, 18 h y el gráfico. **Reales** (web): lema, integraciones, 2 semanas, ROI medible en 6 semanas y el CTA.

## Regenerar
```bash
cd videos/scalyai-promo
STYLE="Dilo en español latinoamericano neutro, con voz cálida, segura y cercana, ritmo ágil de anuncio: " ./audio/generar-segmentos-gemini.sh Charon   # voz (Gemini TTS)
PLAN_ONLY=1 python3 build/audio.py && python3 build/html.py   # tiempos → eventos
python3 build/audio.py && python3 build/html.py               # música + efectos → index.html
npx --yes hyperframes@0.8.96 check
npx --yes hyperframes@0.8.96 render -o renders/scalyai-promo.mp4
```
El texto de la locución vive en `audio/segmentos.json`; las escenas en `build/html.py` y los estilos en `build/style.css`.
