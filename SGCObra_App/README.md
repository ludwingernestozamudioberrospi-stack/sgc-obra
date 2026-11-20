# SGC Obra - Sistema de Gestión y Liberación de Protocolos de Calidad

## 📋 Descripción del Aporte para la Empresa
Aplicación desarrollada a la medida de la obra **"Construcción de Infraestructura Educativa en la I.E. José Carlos Mariátegui"**, basada en los protocolos reales de la empresa (**Consorcio C&C**).

### 🎯 Problemas que Resuelve:
1. **Reemplazo de archivos Excel pesados (de más de 50 MB):** Evita la lentitud, errores de fórmulas y riesgo de pérdida de información.
2. **Registro Ágil en Campo (Tablet / Móvil / Laptop):** Permite registrar la liberación de elementos estructurales (Columnas, Placas, Losas Aligeradas, Zapatas, Vigas) con checklists estandarizados y fotos in situ.
3. **Generación Instantánea de PDF Oficial:** Genera en 1 segundo el protocolo formal listo para firma del Residente, Especialista QA/QC y Supervisión, con cabeceras institucionales, tolerancias y panel fotográfico.
4. **Dashboard y Trazabilidad:** Muestra el conteo de elementos Aprobados, Observados y Pendientes por Módulo (Módulo 01, 02, 04, XI, Cerco Perimétrico, Cisterna).

---

## 🚀 Cómo Iniciar la Aplicación

1. **Opción Rápida:** Haz doble clic en el archivo [`run_app.bat`](file:///C:/Users/LUDWING/.gemini/antigravity/scratch/SGCObra_App/run_app.bat).
2. **Opción por Consola:**
   ```bash
   cd "C:\Users\LUDWING\.gemini\antigravity\scratch\SGCObra_App"
   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```
3. Abre tu navegador web en: **`http://127.0.0.1:8000`**

---

## 🗂️ Estructura del Proyecto

* [`main.py`](file:///C:/Users/LUDWING/.gemini/antigravity/scratch/SGCObra_App/main.py): Backend con FastAPI, endpoints de CRUD y exportación.
* [`database.py`](file:///C:/Users/LUDWING/.gemini/antigravity/scratch/SGCObra_App/database.py): Base de datos SQLite y datos iniciales de los módulos de la obra.
* [`pdf_generator.py`](file:///C:/Users/LUDWING/.gemini/antigravity/scratch/SGCObra_App/pdf_generator.py): Motor ReportLab que emite el PDF oficial del consorcio con formato estandarizado.
* [`templates/index.html`](file:///C:/Users/LUDWING/.gemini/antigravity/scratch/SGCObra_App/templates/index.html): Interfaz moderna y responsiva con TailwindCSS y FontAwesome.
* `data/`: Almacena la base de datos `calidad_obra.db`, las fotos subidas y los PDFs generados.
