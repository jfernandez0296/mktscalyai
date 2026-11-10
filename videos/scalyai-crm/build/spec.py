TITLE = "Scaly AI — Cómo se opera un CRM"
NOTE = "Ejemplo ilustrativo"
SCENES = [
 dict(seg="s1", kind="hook", eyebrow="CRM · Ventas", title=["¿Cómo se opera", "<em>un CRM?</em>"], icon="users", cls="c-crm",
      orbit=[("wa", ""), ("globe", "c-xls"), ("phone", "c-erp"), ("handshake", "")]),
 dict(seg="s2", kind="step", eyebrow="Contactos", title=["Cada contacto,", "<em>registrado solo.</em>"], icon="users", cls="c-crm", lead="Llegue por donde llegue, entra como oportunidad.",
      mods=[dict(type="rows", title="Entradas de hoy", rows=[dict(icon="wa", text="WhatsApp", sub="María · consulta por precios", t0="Nuevo", t1="Oportunidad"),
                                    dict(icon="globe", cls="c-xls", text="Formulario web", sub="Carlos · pide una demo", t0="Nuevo", t1="Oportunidad"),
                                    dict(icon="phone", cls="c-erp", text="Llamada", sub="Lucía · quiere cotización", t0="Nuevo", t1="Oportunidad")])]),
 dict(seg="s3", kind="step", eyebrow="Etapas", title=["La oportunidad", "<em>avanza por etapas.</em>"], icon="trending-up", lead="Siempre sabes en qué va cada cliente.",
      mods=[dict(type="pipe", title="Embudo de ventas", cols=[("Nuevo", "#2F4560"), ("Conversación", "#1F4FBF"), ("Propuesta", "#B5651D"), ("Ganado", "#1D6F42")], person=2, deal="María", amount="S/ 3.200", at=[0.38, 0.6, 0.82])]),
 dict(seg="s4", kind="step", eyebrow="Seguimiento", title=["Te recuerda", "<em>a quién llamar hoy.</em>"], icon="bell", cls="c-erp", lead="Ningún cliente se enfría.",
      mods=[dict(type="rows", title="Tareas de hoy", rows=[dict(person=2, text="María", sub="Enviar la propuesta", t0="10:00 a. m.", t1="Hecho"),
                                    dict(person=3, text="Carlos", sub="Llamar para la demo", t0="12:30 p. m.", t1="Hecho"),
                                    dict(person=1, text="Lucía", sub="Hacer seguimiento", t0="4:00 p. m.")])]),
 dict(seg="s5", kind="step", eyebrow="Pronóstico", title=["Cuánto vas a vender,", "<em>con datos.</em>"], icon="chart-column", cls="c-xls", lead="Tu pronóstico del mes, siempre actualizado.",
      mods=[dict(type="kpis", ring=dict(pct=68, label="de la meta"), stats=[dict(pre="S/ ", value=32400, label="pronóstico del mes"), dict(value=18, label="oportunidades abiertas")]),
            dict(type="bars", title="Oportunidades por etapa", bars=[("Nuevo", 8), ("Conversación", 5), ("Propuesta", 3), ("Ganado", 2)], colors={0: "#2F4560", 1: "#1F4FBF", 2: "#B5651D", 3: "#1D6F42"})]),
 dict(seg="s6", kind="cta", title=["¿Quieres un CRM", "hecho para", "<em>tu negocio?</em>"]),
]
