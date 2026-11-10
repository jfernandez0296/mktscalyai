TITLE = "Scaly AI — Cómo sería operar un ERP"
NOTE = "Ejemplo ilustrativo"
SCENES = [
 dict(seg="s1", kind="hook", eyebrow="ERP · Operación", title=["¿Cómo sería operar", "tu empresa", "<em>con un ERP?</em>"], icon="boxes", cls="c-erp",
      orbit=[("shopping-cart", "c-crm"), ("package", ""), ("receipt", "c-xls"), ("wallet", "c-erp")]),
 dict(seg="s2", kind="step", eyebrow="Ventas", title=["Registras la venta.", "<em>El stock se descuenta.</em>"], icon="shopping-cart", cls="c-crm", lead="Una sola acción actualiza todo.",
      mods=[dict(type="flow", chip="Venta #2051", tiles=[dict(icon="shopping-cart", cls="c-crm", label="Venta"), dict(icon="package", label="Stock"), dict(icon="receipt", cls="c-xls", label="Factura")]),
            dict(type="grid", title="Stock · Polo básico", cols=6, cells=[("", "occ")] * 12, changes=[(11, "free", 0.62), (10, "free", 0.74)], legend=[("occ", "En stock"), ("free", "Vendido")])]),
 dict(seg="s3", kind="step", eyebrow="Compras", title=["Stock bajo.", "<em>Orden de compra lista.</em>"], icon="truck", cls="c-erp", lead="El ERP repone antes de que te quedes sin producto.",
      mods=[dict(type="rows", title="Reposición", rows=[dict(icon="package", cls="c-erp", text="Polo básico · M", sub="Quedan 4 · mínimo 10", t0="Bajo mínimo", t1="Orden creada"),
                                    dict(icon="clipboard-list", cls="c-crm", text="Orden de compra OC-118", sub="Proveedor asignado", t0="Borrador", t1="Enviada"),
                                    dict(icon="truck", text="Entrega del proveedor", sub="Llega en 3 días", t0="Sin fecha", t1="Programada")])]),
 dict(seg="s4", kind="step", eyebrow="Finanzas", title=["Factura emitida.", "<em>Cobranza programada.</em>"], icon="receipt", cls="c-xls", lead="Sin perseguir pagos a mano.", people=[1],
      mods=[dict(type="rows", rows=[dict(icon="receipt", cls="c-xls", text="Factura F001-2051", sub="S/ 1.240", t0="Pendiente", t1="Emitida"),
                                    dict(icon="bell", cls="c-erp", text="Recordatorio de pago", sub="3 días antes del vencimiento", t0="Sin programar", t1="Programado"),
                                    dict(icon="banknote", text="Pago recibido", sub="Conciliado en caja", t0="Pendiente", t1="Conciliado")])]),
 dict(seg="s5", kind="step", eyebrow="Un solo lugar", title=["Todas las áreas,", "<em>los mismos números.</em>"], icon="chart-column", lead="Ventas, inventario y caja, siempre al día.", people=[0, 1, 3],
      mods=[dict(type="kpis", ring=dict(pct=74, label="meta del mes"), stats=[dict(pre="S/ ", value=48200, label="ventas del mes"), dict(value=312, label="productos en stock")]),
            dict(type="bars", title="Ventas por semana", bars=[("Sem. 1", 60), ("Sem. 2", 72), ("Sem. 3", 68), ("Sem. 4", 90)], colors={3: "#1D6F42"})]),
 dict(seg="s6", kind="cta", title=["¿Tu empresa necesita", "un ERP", "<em>a su medida?</em>"]),
]
