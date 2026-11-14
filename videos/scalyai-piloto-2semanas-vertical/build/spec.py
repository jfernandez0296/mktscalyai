TITLE = "Scaly AI — Las primeras 2 semanas de un piloto"
NOTE = "Calendario de ejemplo: cada piloto se ajusta a tu proceso."
LEG = [("occ", "Hecho"), ("block", "En curso"), ("free", "Por venir")]
def cal(done, now):
    return dict(type="grid", title="14 días", cols=7, legend=LEG, cells=[(str(d), "occ" if d in done else "free") for d in range(1, 15)],
                changes=[(d - 1, "block", 0.08 + 0.12 * i / max(1, len(now))) for i, d in enumerate(now)])
SCENES = [
 dict(seg="p1", kind="hook", eyebrow="Cómo trabajamos", title=["¿Qué pasa en las", "primeras <em>2 semanas</em>", "de un piloto?"], icon="calendar-check",
      orbit=[('target', '', 'Días 1–2'), ('link', 'c-crm', 'Días 3–5'), ('zap', 'c-erp', 'Semana 2'), ('chart-column', 'c-xls', 'Día 14')]),
 dict(seg="p2", kind="step", eyebrow="Días 1–2", title=["Elegimos", "<em>un proceso.</em>"], icon="target", lead="El que más tiempo le cuesta a tu equipo.", people=[0, 1],
      mods=[cal([], [1, 2]),
            dict(type="rows", rows=[dict(icon="message-circle", text="Conversamos 30 minutos", sub="Sobre tu operación", t1="Hecho"),
                                    dict(icon="target", cls="c-crm", text="Elegimos un solo proceso", sub="El que más tiempo cuesta", t1="Elegido")], span=(0.3, 0.95))]),
 dict(seg="p3", kind="step", eyebrow="Días 3–5", title=["Mapeamos y", "<em>conectamos.</em>"], icon="link", cls="c-crm", lead="Sobre las herramientas que ya usas.", people=[1],
      mods=[cal([1, 2], [3, 4, 5]),
            dict(type="rows", rows=[dict(icon="layers", cls="c-crm", text="Cómo funciona hoy", sub="Paso a paso", t1="Mapeado"),
                                    dict(icon="link", text="Tus herramientas", sub="WhatsApp · CRM · hojas · ERP", t1="Conectadas")], span=(0.3, 0.95))]),
 dict(seg="p4", kind="step", eyebrow="Semana 2", title=["Lo ponemos", "<em>a funcionar.</em>"], icon="zap", cls="c-erp", lead="Con casos reales de tu negocio.", people=[0, 2, 3],
      mods=[cal([1, 2, 3, 4, 5], [8, 9, 10, 11, 12, 13]),
            dict(type="rows", rows=[dict(icon="zap", cls="c-erp", text="Casos reales", sub="De tu negocio", t1="Funcionando"),
                                    dict(icon="users", cls="c-crm", text="Ajustes con tu equipo", sub="Hasta que encaje", t1="Ajustado")], span=(0.3, 0.95))]),
 dict(seg="p5", kind="step", eyebrow="Día 14", title=["El proceso", "<em>trabaja solo.</em>"], icon="chart-column", cls="c-xls", lead="Y empezamos a medir el retorno.", people=[0, 1],
      mods=[cal([1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13], [14]),
            dict(type="rows", rows=[dict(icon="circle-check", cls="c-xls", text="El proceso ya trabaja solo", sub="Sin trabajo manual", t1="Listo"),
                                    dict(icon="chart-column", text="ROI medible", sub="En 6 semanas", t0="Midiendo")], span=(0.2, 0.9))]),
 dict(seg="p5b", kind="step", eyebrow="Después", title=["Medimos y", "<em>tú decides.</em>"], icon="handshake", lead="Sin compromisos a ciegas.", people=[0, 2],
      mods=[dict(type="rows", title="Después del piloto", rows=[dict(icon="chart-column", cls="c-xls", text="Medimos el resultado", sub="Con datos reales", t1="Medido"),
                                    dict(icon="layers", cls="c-crm", text="¿Lo llevamos a otros procesos?", sub="La decisión es tuya", t0="Tú decides")])]),
 dict(seg="p6", kind="cta", title=["Empezamos con", "un piloto, no con", "<em>una apuesta.</em>"]),
]
