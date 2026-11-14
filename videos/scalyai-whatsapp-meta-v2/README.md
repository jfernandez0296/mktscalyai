# Scaly AI · Conecta WhatsApp Business a Meta desde Claude (vertical 9:16, diseño nuevo)

Versión vertical rehecha con el motor de los videos verticales (`build/spec.py` + `build/html.py`), reutilizando la locución original.
El render se guarda en `videos/scalyai-whatsapp-meta-vertical/renders/scalyai-whatsapp-meta-vertical.mp4` y reemplaza a la versión vertical anterior.

```bash
python3 build/audio.py && python3 build/html.py
npx --yes hyperframes@0.8.96 render -o ../scalyai-whatsapp-meta-vertical/renders/scalyai-whatsapp-meta-vertical.mp4
```
