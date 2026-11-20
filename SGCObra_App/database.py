import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "calidad_obra.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS protocols (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE,
        contractor_header TEXT DEFAULT 'CONSORCIO LA MERCED',
        header_title TEXT DEFAULT 'CONTROL DE CALIDAD',
        partida_desc TEXT DEFAULT '01.07.04.01, 01.07.04.02 y 01.07.04.03   CONCRETO f ''c=210 kg/cm2 P/ COLUMNAS, ENCOFRADO Y DESENCOFRADO P/ COLUMNAS Y ACERO DE REFUERZO fy=4200 kg/cm2',
        project_name TEXT,
        client TEXT DEFAULT 'GOBIERNO REGIONAL DE JUNIN',
        contractor TEXT DEFAULT 'CONSORCIO LA MERCED',
        sector TEXT,            -- ESRUCTURA / MODULO
        subsector TEXT,         -- UBICACION
        element_code TEXT,      -- ELEMENTO (C-01, C-02)
        ref_docs TEXT,          -- PLANO DE REFERENCIA
        inspection_date TEXT,
        status TEXT DEFAULT 'APROBADO',
        observations TEXT,
        field_engineer TEXT DEFAULT 'RESIDENTE',
        qa_qc_engineer TEXT DEFAULT 'ESPECIALISTA EN ESTRUCTURAS',
        supervisor_engineer TEXT DEFAULT 'SUPERVISOR',
        esp_supervisor TEXT DEFAULT 'ESPECIALISTA ESTRUCTURA',
        firmas_contratista TEXT DEFAULT 'CONSORCIO LA MERCED',
        firmas_supervision TEXT DEFAULT 'JOGAMA CONSULTORIA Y CONSTRUCCIONES GENERALES EIRL',
        checklist_eval TEXT,    -- JSON con el estado individual de cada uno de los 44 items (SI/NO/NA)
        conc_params TEXT,       -- JSON con f'c, volumen, slump, tipo concreto, tipo colocacion, acabado y remisiones
        photos TEXT,            -- JSON con las rutas de las fotos
        photo1_desc TEXT DEFAULT 'FOTO 1: ARMADURA DE ACERO Y ENCOFRADO DE COLUMNA',
        photo2_desc TEXT DEFAULT 'FOTO 2: VERIFICACIÓN DE VERTICALIDAD Y APUNTALAMIENTO',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

    # Si la tabla ya existe con columnas viejas, alterarla si es necesario
    existing_cols = [c[1] for c in cursor.execute("PRAGMA table_info(protocols)").fetchall()]
    needed_cols = [
        ("contractor_header", "TEXT DEFAULT 'CONSORCIO LA MERCED'"),
        ("header_title", "TEXT DEFAULT 'CONTROL DE CALIDAD'"),
        ("partida_desc", "TEXT DEFAULT '01.07.04.01, 01.07.04.02 y 01.07.04.03   CONCRETO f ''c=210 kg/cm2 P/ COLUMNAS, ENCOFRADO Y DESENCOFRADO P/ COLUMNAS Y ACERO DE REFUERZO fy=4200 kg/cm2'"),
        ("client", "TEXT DEFAULT 'GOBIERNO REGIONAL DE JUNIN'"),
        ("esp_supervisor", "TEXT DEFAULT 'ESPECIALISTA ESTRUCTURA'"),
        ("firmas_contratista", "TEXT DEFAULT 'CONSORCIO LA MERCED'"),
        ("firmas_supervision", "TEXT DEFAULT 'JOGAMA CONSULTORIA Y CONSTRUCCIONES GENERALES EIRL'"),
        ("checklist_eval", "TEXT"),
        ("conc_params", "TEXT"),
        ("photo1_desc", "TEXT DEFAULT 'FOTO 1: ARMADURA DE ACERO Y ENCOFRADO DE COLUMNA'"),
        ("photo2_desc", "TEXT DEFAULT 'FOTO 2: VERIFICACIÓN DE VERTICALIDAD Y APUNTALAMIENTO'")
    ]
    for col_name, col_type in needed_cols:
        if col_name not in existing_cols:
            cursor.execute(f"ALTER TABLE protocols ADD COLUMN {col_name} {col_type}")
    conn.commit()

    # Seed data acorde a la plantilla oficial de la obra
    cursor.execute("SELECT COUNT(*) FROM protocols")
    count = cursor.fetchone()[0]
    if count == 0:
        # Evaluacion por defecto: todo cumple SI
        default_eval = {}
        for i in range(1, 13):
            default_eval[f"enc_{i}"] = "SI"
            default_eval[f"ace_{i}"] = "SI"
        for i in range(1, 9):
            default_eval[f"con_{i}"] = "SI"
            default_eval[f"ins_{i}"] = "NA" if i > 3 else "SI"

        default_conc = {
            "fc": "210",
            "volumen": "4.5",
            "slump": "5\"-6\"",
            "tipo_concreto": "PREMEZCLADO",
            "tipo_colocacion": "BOMBA",
            "tipo_acabado": "CARAVISTA",
            "remisiones": [
                {
                    "guia": "GR-002491",
                    "vol": "4.5",
                    "salida": "09:15",
                    "llegada": "09:45",
                    "inicio": "09:55",
                    "fin": "10:30",
                    "slump": "5.5",
                    "temp_amb": "24°C",
                    "temp_conc": "22°C",
                    "prob": "6",
                    "cod_prob": "C-01/C-02 (A-F)"
                }
            ]
        }

        seed_rows = [
            (
                "REG-MOD02-COL-001",
                "CONSORCIO LA MERCED",
                "CONTROL DE CALIDAD",
                "01.07.04.01, 01.07.04.02 y 01.07.04.03   CONCRETO f 'c=210 kg/cm2 P/ COLUMNAS, ENCOFRADO Y DESENCOFRADO P/ COLUMNAS Y ACERO DE REFUERZO fy=4200 kg/cm2",
                "MEJORAIENTO Y AMPLIACIÓN DE LOS SERVICIOS EDUCATIVOS DE LA I.E POLITÉCNICO SELVA CENTRAL, DISTRITO DE CHANCHAMAYO - PROVINCIA DE CHANCHAMAYO - DEPARTAMENTO DE JUNIN , CON CUI Nº2499579.",
                "GOBIERNO REGIONAL DE JUNIN",
                "CONSORCIO LA MERCED",
                "MODULO 2 PISO 3",
                "COLUMNAS EJE 2 Y 5",
                "COLUMNA PL-1",
                "ESTRUCTURAS MODULO II (E-14)",
                "2026-10-20",
                "APROBADO",
                "Elemento estructural conforme a planos. Liberado para vaciado de concreto f'c=210 kg/cm2.",
                "ING. RESIDENTE DE OBRA",
                "ING. ESPECIALISTA EN ESTRUCTURAS",
                "ING. SUPERVISOR DE OBRA",
                "ING. ESPECIALISTA ESTRUCTURA (SUPERVISIÓN)",
                "CONSORCIO LA MERCED",
                "JOGAMA CONSULTORIA Y CONSTRUCCIONES GENERALES EIRL",
                json.dumps(default_eval),
                json.dumps(default_conc),
                json.dumps([]),
                "FOTO 1: ARMADURA DE ACERO Y ENCOFRADO DE COLUMNA PL-1",
                "FOTO 2: VERIFICACIÓN DE VERTICALIDAD Y APUNTALAMIENTO"
            ),
            (
                "REG-MOD03-COL-002",
                "CONSORCIO LA MERCED",
                "CONTROL DE CALIDAD",
                "01.07.04.01, 01.07.04.02 y 01.07.04.03   CONCRETO f 'c=210 kg/cm2 P/ COLUMNAS, ENCOFRADO Y DESENCOFRADO P/ COLUMNAS Y ACERO DE REFUERZO fy=4200 kg/cm2",
                "MEJORAIENTO Y AMPLIACIÓN DE LOS SERVICIOS EDUCATIVOS DE LA I.E POLITÉCNICO SELVA CENTRAL, DISTRITO DE CHANCHAMAYO - PROVINCIA DE CHANCHAMAYO - DEPARTAMENTO DE JUNIN , CON CUI Nº2499579.",
                "GOBIERNO REGIONAL DE JUNIN",
                "CONSORCIO LA MERCED",
                "MODULO 3 TERCER PISO EJE 5-8",
                "COLUMNAS (C-02,C-01)",
                "COLUMNAS (C-02,C-01)",
                "ESTRUCTURAS MODULO III E-28",
                "2026-08-12",
                "APROBADO",
                "Liberado para vaciado de concreto premezclado.",
                "ING. RESIDENTE DE OBRA",
                "ING. ESPECIALISTA EN ESTRUCTURAS",
                "ING. SUPERVISOR DE OBRA",
                "ING. ESPECIALISTA ESTRUCTURA (SUPERVISIÓN)",
                "CONSORCIO LA MERCED",
                "JOGAMA CONSULTORIA Y CONSTRUCCIONES GENERALES EIRL",
                json.dumps(default_eval),
                json.dumps(default_conc),
                json.dumps([]),
                "FOTO 1: ARMADURA DE ACERO EN COLUMNAS C-01 Y C-02",
                "FOTO 2: ENCOFRADO HERMÉTICO Y PLOMADA"
            )
        ]
        cursor.executemany("""
        INSERT INTO protocols (
            code, contractor_header, header_title, partida_desc, project_name,
            client, contractor, sector, subsector, element_code, ref_docs,
            inspection_date, status, observations, field_engineer, qa_qc_engineer,
            supervisor_engineer, esp_supervisor, firmas_contratista, firmas_supervision,
            checklist_eval, conc_params, photos, photo1_desc, photo2_desc
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, seed_rows)
        conn.commit()

    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database checked and updated.")
