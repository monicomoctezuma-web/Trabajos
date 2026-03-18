# ============================================================
#   SISTEMA EXPERTO - DIAGNÓSTICO DE ESTILO DE APRENDIZAJE
#   Con manejo de incertidumbre (Factores de Certeza)
# ============================================================

# ─────────────────────────────────────────────────────────────
# COMPONENTE 1: CLASE PRINCIPAL DEL SISTEMA EXPERTO
# ─────────────────────────────────────────────────────────────
class SistemaExpertoAprendizaje:
    def __init__(self):
        # BASE DE HECHOS: almacena las respuestas ingresadas por el usuario
        self.hechos = {}

        # BASE DE CONOCIMIENTOS: lista de reglas de producción
        self.reglas = []

        # MEMORIA DE TRABAJO: guarda conclusiones derivadas con su certeza
        self.conclusiones = {}

        # TRAZA DE INFERENCIA: registro del camino seguido por el motor
        self.traza = []

    # ─────────────────────────────────────────────────────────
    # COMPONENTE 2: BASE DE CONOCIMIENTOS (reglas de producción)
    # 12 reglas con factor de certeza (0.0 – 1.0)
    # 2 niveles de inferencia (encadenamiento hacia adelante)
    # ─────────────────────────────────────────────────────────
    def definir_reglas(self):
        """
        Cada regla tiene:
          id        → identificador único
          premisas  → lista de (hecho/conclusión, valor_esperado)
          conclusion→ nombre del hecho derivado
          certeza   → confianza de la regla (0.0 a 1.0)
          encadenada→ True si alguna premisa es conclusión de otra regla
        """

        # ── NIVEL 1: reglas que usan solo respuestas directas ──────────────

        # Regla 1: Prefiere diagramas + apuntes con colores → Tendencia Visual
        self.reglas.append({
            'id': 1,
            'premisas': [('prefiere_diagramas', True), ('apuntes_colores', True)],
            'conclusion': 'Tendencia_Visual',
            'certeza': 0.90,
            'encadenada': False
        })

        # Regla 2: Dificultad sin imágenes + recuerda caras → Tendencia Visual reforzada
        self.reglas.append({
            'id': 2,
            'premisas': [('dificil_sin_imagenes', True), ('recuerda_caras', True)],
            'conclusion': 'Tendencia_Visual',
            'certeza': 0.85,
            'encadenada': False
        })

        # Regla 3: Prefiere explicación oral + recuerda conversaciones → Tendencia Auditiva
        self.reglas.append({
            'id': 3,
            'premisas': [('prefiere_explicacion_oral', True), ('recuerda_conversaciones', True)],
            'conclusion': 'Tendencia_Auditiva',
            'certeza': 0.90,
            'encadenada': False
        })

        # Regla 4: Lee en voz alta + se distrae con ruido → Tendencia Auditiva reforzada
        self.reglas.append({
            'id': 4,
            'premisas': [('lee_en_voz_alta', True), ('se_distrae_con_ruido', True)],
            'conclusion': 'Tendencia_Auditiva',
            'certeza': 0.80,
            'encadenada': False
        })

        # Regla 5: Aprende haciendo + difícil estar quieto → Tendencia Kinestésica
        self.reglas.append({
            'id': 5,
            'premisas': [('aprende_haciendo', True), ('dificil_estar_quieto', True)],
            'conclusion': 'Tendencia_Kinestesica',
            'certeza': 0.90,
            'encadenada': False
        })

        # Regla 6: Prefiere experimentos + recuerda experiencias → Tendencia Kinestésica reforzada
        self.reglas.append({
            'id': 6,
            'premisas': [('prefiere_experimentos', True), ('recuerda_experiencias', True)],
            'conclusion': 'Tendencia_Kinestesica',
            'certeza': 0.85,
            'encadenada': False
        })

        # ── NIVEL 2: reglas encadenadas (usan conclusiones de nivel 1) ───

        # Regla 7: Tendencia Visual + organiza en tablas → Estilo Visual Confirmado
        self.reglas.append({
            'id': 7,
            'premisas': [('Tendencia_Visual', True), ('organiza_en_tablas', True)],
            'conclusion': 'Estilo_Visual',
            'certeza': 0.92,
            'encadenada': True   # usa conclusión de Reglas 1 o 2
        })

        # Regla 8: Tendencia Auditiva + estudia con audio → Estilo Auditivo Confirmado
        self.reglas.append({
            'id': 8,
            'premisas': [('Tendencia_Auditiva', True), ('estudia_con_audio', True)],
            'conclusion': 'Estilo_Auditivo',
            'certeza': 0.92,
            'encadenada': True   # usa conclusión de Reglas 3 o 4
        })

        # Regla 9: Tendencia Kinestésica + aprende en campo → Estilo Kinestésico Confirmado
        self.reglas.append({
            'id': 9,
            'premisas': [('Tendencia_Kinestesica', True), ('aprende_en_campo', True)],
            'conclusion': 'Estilo_Kinestesico',
            'certeza': 0.92,
            'encadenada': True   # usa conclusión de Reglas 5 o 6
        })

        # Regla 10: Tendencia Visual + Tendencia Auditiva → Estilo Mixto Visual-Auditivo
        self.reglas.append({
            'id': 10,
            'premisas': [('Tendencia_Visual', True), ('Tendencia_Auditiva', True)],
            'conclusion': 'Estilo_Mixto_Visual_Auditivo',
            'certeza': 0.78,
            'encadenada': True
        })

        # Regla 11: Tendencia Visual + Tendencia Kinestésica → Estilo Mixto Visual-Kinestésico
        self.reglas.append({
            'id': 11,
            'premisas': [('Tendencia_Visual', True), ('Tendencia_Kinestesica', True)],
            'conclusion': 'Estilo_Mixto_Visual_Kinestesico',
            'certeza': 0.78,
            'encadenada': True
        })

        # Regla 12: Tendencia Auditiva + Tendencia Kinestésica → Estilo Mixto Auditivo-Kinestésico
        self.reglas.append({
            'id': 12,
            'premisas': [('Tendencia_Auditiva', True), ('Tendencia_Kinestesica', True)],
            'conclusion': 'Estilo_Mixto_Auditivo_Kinestesico',
            'certeza': 0.78,
            'encadenada': True
        })

    # ─────────────────────────────────────────────────────────
    # COMPONENTE 3: INTERFAZ DE USUARIO / ADQUISICIÓN DE HECHOS
    # Recoge las respuestas del usuario (Sí / No / N/A)
    # ─────────────────────────────────────────────────────────
    def obtener_respuestas(self):
        preguntas = [
            ('prefiere_diagramas',        'Prefiere aprender con diagramas, mapas o esquemas'),
            ('apuntes_colores',           'Toma apuntes usando colores, subrayados o dibujos'),
            ('dificil_sin_imagenes',      'Le cuesta entender textos sin imágenes o gráficos'),
            ('recuerda_caras',            'Recuerda mejor las caras que los nombres'),
            ('prefiere_explicacion_oral', 'Prefiere que le expliquen las cosas de viva voz'),
            ('recuerda_conversaciones',   'Recuerda con facilidad lo que se habló en clase'),
            ('lee_en_voz_alta',           'Acostumbra leer en voz alta para entender mejor'),
            ('se_distrae_con_ruido',      'El ruido del ambiente le distrae al estudiar'),
            ('aprende_haciendo',          'Aprende mejor practicando o haciendo con las manos'),
            ('dificil_estar_quieto',      'Le cuesta estar mucho tiempo sentado sin moverse'),
            ('prefiere_experimentos',     'Prefiere aprender con experimentos o actividades prácticas'),
            ('recuerda_experiencias',     'Recuerda mejor lo que vivió o hizo que lo que leyó'),
            ('organiza_en_tablas',        'Organiza su información en tablas, listas o cuadros'),
            ('estudia_con_audio',         'Estudia escuchando música, podcasts o grabaciones'),
            ('aprende_en_campo',          'Aprende mejor en laboratorios o salidas fuera del aula'),
        ]

        print("\n" + "=" * 60)
        print("   SISTEMA EXPERTO - ESTILO DE APRENDIZAJE")
        print("   Responda: s = Sí  |  n = No  |  Enter = N/A")
        print("=" * 60)

        for clave, descripcion in preguntas:
            while True:
                resp = input(f"  {descripcion}: ").strip().lower()
                if resp in ('s', 'si', 'sí'):
                    self.hechos[clave] = True
                    break
                elif resp in ('n', 'no'):
                    self.hechos[clave] = False
                    break
                elif resp == '':
                    # N/A: no se incluye en la base de hechos
                    break
                else:
                    print("    → Ingrese 's', 'n' o deje en blanco (N/A)")

    # ─────────────────────────────────────────────────────────
    # COMPONENTE 4: CÁLCULO DE CERTEZA
    # Fórmula: certeza_final = certeza_regla × promedio_premisas
    # Para encadenamiento: multiplica además la certeza de la premisa previa
    # ─────────────────────────────────────────────────────────
    def calcular_certeza(self, regla, premisas_ok, total_premisas):
        """Certeza base = certeza_regla × (premisas cumplidas / total)"""
        certeza_base = regla['certeza'] * (premisas_ok / total_premisas)

        # Si la regla usa conclusiones encadenadas, propaga la certeza previa
        if regla['encadenada']:
            for premisa, valor in regla['premisas']:
                if premisa in self.conclusiones:
                    certeza_previa = self.conclusiones[premisa]['certeza']
                    certeza_base = certeza_base * certeza_previa
                    break   # solo se considera la primera premisa encadenada

        return round(certeza_base, 4)

    # ─────────────────────────────────────────────────────────
    # COMPONENTE 5: MOTOR DE INFERENCIA (encadenamiento hacia adelante)
    # Evalúa las reglas en múltiples pasadas hasta que no haya cambios
    # ─────────────────────────────────────────────────────────
    def motor_inferencia(self):
        cambio = True
        while cambio:
            cambio = False
            for regla in self.reglas:
                base = {**self.hechos, **{k: True for k in self.conclusiones}}

                premisas_cumplidas = 0
                todas_disponibles = True

                for premisa, valor_esperado in regla['premisas']:
                    if premisa in base:
                        if base[premisa] == valor_esperado:
                            premisas_cumplidas += 1
                    else:
                        todas_disponibles = False

                # La regla se activa si TODAS las premisas disponibles coinciden
                if todas_disponibles and premisas_cumplidas == len(regla['premisas']):
                    certeza = self.calcular_certeza(
                        regla, premisas_cumplidas, len(regla['premisas'])
                    )
                    conclusion = regla['conclusion']
                    # Guardar o actualizar con la certeza más alta
                    if conclusion not in self.conclusiones or \
                       certeza > self.conclusiones[conclusion]['certeza']:
                        self.conclusiones[conclusion] = {
                            'certeza': certeza,
                            'regla_id': regla['id'],
                            'encadenada': regla['encadenada']
                        }
                        self.traza.append({
                            'conclusion': conclusion,
                            'regla': regla,
                            'certeza': certeza
                        })
                        cambio = True   # nueva conclusión → otra pasada

    # ─────────────────────────────────────────────────────────
    # COMPONENTE 6: MÓDULO DE EXPLICACIÓN / TRAZABILIDAD
    # Muestra respuestas, conclusiones y el camino de inferencia
    # ─────────────────────────────────────────────────────────
    def mostrar_explicacion(self):
        RECOMENDACIONES = {
            'Estilo_Visual':
                'Usa mapas mentales, diagramas y esquemas con colores. '
                'Estudia con videos e infografías.',
            'Estilo_Auditivo':
                'Graba explicaciones y escúchalas. Estudia en voz alta '
                'y participa en debates o grupos de estudio.',
            'Estilo_Kinestesico':
                'Aprende haciendo: prácticas, laboratorios y proyectos. '
                'Toma descansos activos y usa tarjetas físicas.',
            'Estilo_Mixto_Visual_Auditivo':
                'Combina diagramas con explicaciones grabadas. '
                'Los videos educativos son ideales para ti.',
            'Estilo_Mixto_Visual_Kinestesico':
                'Aprende haciendo y acompáñalo con esquemas visuales. '
                'Las simulaciones interactivas son perfectas.',
            'Estilo_Mixto_Auditivo_Kinestesico':
                'Aprende con actividades prácticas y explicaciones orales. '
                'Escucha instrucciones y ponlas en práctica de inmediato.',
            'Tendencia_Visual':
                'Tienes inclinación visual. Usa más imágenes y diagramas al estudiar.',
            'Tendencia_Auditiva':
                'Tienes inclinación auditiva. Escucha más contenido educativo.',
            'Tendencia_Kinestesica':
                'Tienes inclinación kinestésica. Busca actividades prácticas para aprender.',
        }

        nombres = {
            'prefiere_diagramas':        'Prefiere diagramas/esquemas',
            'apuntes_colores':           'Apuntes con colores',
            'dificil_sin_imagenes':      'Dificultad sin imágenes',
            'recuerda_caras':            'Recuerda caras',
            'prefiere_explicacion_oral': 'Prefiere explicación oral',
            'recuerda_conversaciones':   'Recuerda conversaciones',
            'lee_en_voz_alta':           'Lee en voz alta',
            'se_distrae_con_ruido':      'Se distrae con ruido',
            'aprende_haciendo':          'Aprende haciendo',
            'dificil_estar_quieto':      'Difícil estar quieto',
            'prefiere_experimentos':     'Prefiere experimentos',
            'recuerda_experiencias':     'Recuerda experiencias',
            'organiza_en_tablas':        'Organiza en tablas/listas',
            'estudia_con_audio':         'Estudia con audio',
            'aprende_en_campo':          'Aprende en campo/laboratorio',
        }

        print("\n" + "=" * 60)
        print("   — RESPUESTAS INGRESADAS —")
        print("=" * 60)
        for clave, etiqueta in nombres.items():
            if clave in self.hechos:
                valor = "SÍ" if self.hechos[clave] else "NO"
            else:
                valor = "N/A"
            print(f"  ✓ {etiqueta}: {valor}")

        print("\n" + "=" * 60)
        print("   — CONCLUSIONES —")
        print("=" * 60)

        if not self.conclusiones:
            print("  No se pudo determinar un estilo de aprendizaje.")
        else:
            # Priorizar estilos confirmados (nivel 2) sobre tendencias (nivel 1)
            estilos = {k: v for k, v in self.conclusiones.items() if k.startswith('Estilo_')}
            mostrar = estilos if estilos else self.conclusiones

            mejor = max(mostrar, key=lambda k: mostrar[k]['certeza'])
            for i, (nombre, datos) in enumerate(
                    sorted(mostrar.items(),
                           key=lambda x: x[1]['certeza'], reverse=True), 1):
                marca = " ← ESTILO DOMINANTE" if nombre == mejor else ""
                print(f"  {i}. {nombre.replace('_', ' ')} "
                      f"({datos['certeza']*100:.0f}% confianza){marca}")

        print("\n" + "=" * 60)
        print("   — TRAZABILIDAD DE INFERENCIA —")
        print("=" * 60)
        for entrada in self.traza:
            r = entrada['regla']
            c = entrada['certeza']
            print(f"\n  Conclusión: {entrada['conclusion']}")
            print(f"    → Regla #{r['id']} activada (certeza base: {r['certeza']})")
            premisas_str = ', '.join(
                f"{p}={'TRUE' if v else 'FALSE'}" for p, v in r['premisas']
            )
            print(f"    → Premisas: {premisas_str}")
            if r['encadenada']:
                for premisa, _ in r['premisas']:
                    if premisa in self.conclusiones:
                        cert_prev = self.conclusiones[premisa]['certeza']
                        print(f"    → [ENCADENAMIENTO] Usa conclusión '{premisa}' "
                              f"(certeza previa: {cert_prev})")
                        print(f"    → Cálculo: {r['certeza']} × {cert_prev} = "
                              f"{c:.4f} ({c*100:.0f}%)")
                        break
            else:
                print(f"    → Cálculo: {r['certeza']} × 1.0 = {c:.4f} ({c*100:.0f}%)")

        print("\n" + "=" * 60)
        if self.conclusiones:
            estilos = {k: v for k, v in self.conclusiones.items() if k.startswith('Estilo_')}
            mostrar = estilos if estilos else self.conclusiones
            mejor_nombre = max(mostrar, key=lambda k: mostrar[k]['certeza'])
            rec = RECOMENDACIONES.get(mejor_nombre, "Sigue explorando distintas técnicas de estudio.")
            print(f"  RECOMENDACIÓN: {rec}")
        print("=" * 60 + "\n")


# ─────────────────────────────────────────────────────────────
# PROGRAMA PRINCIPAL
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    se = SistemaExpertoAprendizaje()   # Inicializar SE
    se.definir_reglas()                 # Cargar base de conocimientos
    se.obtener_respuestas()             # Adquirir hechos del usuario
    se.motor_inferencia()               # Aplicar reglas (encadenamiento)
    se.mostrar_explicacion()            # Mostrar resultados y trazabilidad