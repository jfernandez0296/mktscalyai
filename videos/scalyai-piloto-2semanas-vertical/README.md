# Scaly AI · Las primeras 2 semanas de un piloto (vertical 9:16, diseño nuevo)

Versión vertical rehecha con el motor de los videos verticales (`build/spec.py` + `build/html.py`), reutilizando la locución original.
El render se guarda en `videos/scalyai-piloto-2semanas/renders/scalyai-piloto-2semanas-9x16.mp4` y reemplaza a la versión vertical anterior.

```bash
python3 build/audio.py && python3 build/html.py
npx --yes hyperframes@0.8.96 render -o ../scalyai-piloto-2semanas/renders/scalyai-piloto-2semanas-9x16.mp4
```
