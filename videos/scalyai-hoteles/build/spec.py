TITLE = "Scaly AI — Cómo automatizar un hotel"
NOTE = "Ejemplo ilustrativo"
SCENES = [
 dict(seg="s1", kind="hook", eyebrow="Hoteles · Automatización", title=["¿Tienes un hotel?", "Así podría trabajar,", "<em>casi solo.</em>"], icon="building-2",
      orbit=[("wa", ""), ("bed-double", "c-crm"), ("calendar-check", "c-xls"), ("sparkles", "c-erp")]),
 dict(seg="s2", kind="step", eyebrow="Reservas", title=["Responde y reserva,", "<em>a cualquier hora.</em>"], icon="wa", lead="Un asistente con IA atiende por WhatsApp y confirma la reserva.",
      mods=[dict(type="chat", person=2, name="Huésped", time="12:04 a. m.", msg="Hola, ¿tienen habitación doble para este sábado?", reply="Sí, tenemos una doble disponible. ¿La reservo a tu nombre?", done="Reserva confirmada · Hab. 204")]),
 dict(seg="s3", kind="step", eyebrow="Canales", title=["La reserva entra sola", "<em>al sistema.</em>"], icon="calendar-check", cls="c-xls", lead="La habitación queda bloqueada en todos tus canales.",
      mods=[dict(type="grid", title="Habitaciones · sábado", cols=4, cells=[("201", "occ"), ("202", "free"), ("203", "occ"), ("204", "free"), ("205", "free"), ("206", "occ"), ("207", "free"), ("208", "occ")],
                 changes=[(3, "block", 0.3)], legend=[("free", "Libre"), ("occ", "Ocupada"), ("block", "Reservada")]),
            dict(type="rows", span=(0.45, 0.95), rows=[dict(icon="globe", cls="c-crm", text="Web del hotel", sub="Hab. 204 · sábado", t0="Disponible", t1="Bloqueada"),
                                    dict(icon="handshake", cls="c-erp", text="Agencias en línea", sub="Hab. 204 · sábado", t0="Disponible", t1="Bloqueada")])]),
 dict(seg="s4", kind="step", eyebrow="Estadía", title=["Check-in digital.", "<em>Limpieza avisada.</em>"], icon="key-round", cls="c-erp", lead="Cada área recibe su aviso en el momento justo.", people=[0, 1],
      mods=[dict(type="rows", rows=[dict(icon="key-round", cls="c-crm", text="Check-in digital", sub="Antes de llegar", t0="Pendiente", t1="Enviado"),
                                    dict(icon="door-open", text="Huésped en su habitación", sub="Hab. 204", t0="Pendiente", t1="Listo"),
                                    dict(icon="receipt", cls="c-xls", text="Check-out y comprobante", sub="Al salir", t0="Pendiente", t1="Emitido"),
                                    dict(icon="sparkles", cls="c-erp", text="Aviso a limpieza", sub="Al instante", t0="Pendiente", t1="Avisado")])]),
 dict(seg="s5", kind="step", eyebrow="Indicadores", title=["Tu hotel,", "<em>en números.</em>"], icon="chart-column", cls="c-xls", lead="Ocupación e ingresos del día, sin armar reportes.",
      mods=[dict(type="kpis", ring=dict(pct=82, label="ocupación"), stats=[dict(pre="S/ ", value=6480, label="ingresos de hoy"), dict(value=14, label="check-ins de hoy")]),
            dict(type="bars", title="Ocupación de la semana", bars=[("L", 55), ("M", 60), ("M", 58), ("J", 70), ("V", 88), ("S", 96), ("D", 82)], colors={5: "#1D6F42"})]),
 dict(seg="s6", kind="cta", title=["¿Quieres automatizar", "<em>tu hotel?</em>"]),
]
