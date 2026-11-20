import os
import json
import shutil
from typing import List, Optional
from fastapi import FastAPI, Form, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import init_db, get_db
from pdf_generator import generate_checklist_pdf, generate_photopanel_pdf

app = FastAPI(title="SGC Obra - Sistema de Gestión de Protocolos de Calidad")

BASE_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")
EXPORT_DIR = os.path.join(BASE_DIR, "data", "exports")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

init_db()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/api/protocols")
async def list_protocols():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM protocols ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/api/protocols/{protocol_id}")
async def get_protocol(protocol_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM protocols WHERE id = ?", (protocol_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Protocolo no encontrado")
    return dict(row)

@app.post("/api/protocols")
async def save_protocol(
    id: Optional[str] = Form(None),
    code: str = Form(...),
    contractor_header: str = Form("CONSORCIO LA MERCED"),
    header_title: str = Form("CONTROL DE CALIDAD"),
    partida_desc: str = Form("01.07.04.01, 01.07.04.02 y 01.07.04.03   CONCRETO f 'c=210 kg/cm2 P/ COLUMNAS, ENCOFRADO Y DESENCOFRADO P/ COLUMNAS Y ACERO DE REFUERZO fy=4200 kg/cm2"),
    project_name: str = Form(...),
    client: str = Form("GOBIERNO REGIONAL DE JUNIN"),
    contractor: str = Form("CONSORCIO LA MERCED"),
    sector: str = Form(...),
    subsector: str = Form(...),
    element_code: str = Form(...),
    ref_docs: str = Form(...),
    inspection_date: str = Form(...),
    status: str = Form("APROBADO"),
    observations: Optional[str] = Form(""),
    field_engineer: str = Form("RESIDENTE"),
    qa_qc_engineer: str = Form("ESPECIALISTA EN ESTRUCTURAS"),
    supervisor_engineer: str = Form("SUPERVISOR"),
    esp_supervisor: str = Form("ESPECIALISTA ESTRUCTURA"),
    firmas_contratista: str = Form("CONSORCIO LA MERCED"),
    firmas_supervision: str = Form("JOGAMA CONSULTORIA Y CONSTRUCCIONES GENERALES EIRL"),
    checklist_eval: str = Form("{}"),
    conc_params: str = Form("{}"),
    photo1_desc: str = Form("FOTO 1: ARMADURA DE ACERO Y ENCOFRADO DE COLUMNA"),
    photo2_desc: str = Form("FOTO 2: VERIFICACIÓN DE VERTICALIDAD Y APUNTALAMIENTO"),
    foto1: Optional[UploadFile] = File(None),
    foto2: Optional[UploadFile] = File(None)
):
    conn = get_db()
    cursor = conn.cursor()

    # Obtener fotos previas si es edición
    existing_photo1 = ""
    existing_photo2 = ""
    if id and id.strip() != "":
        cursor.execute("SELECT photos FROM protocols WHERE id = ?", (int(id),))
        row = cursor.fetchone()
        if row and row["photos"]:
            try:
                p_list = json.loads(row["photos"])
                if len(p_list) >= 1: existing_photo1 = p_list[0]
                if len(p_list) >= 2: existing_photo2 = p_list[1]
            except:
                pass

    final_photo1 = existing_photo1
    if foto1 and foto1.filename:
        filename1 = f"{code}_FOTO1_{foto1.filename}"
        filepath1 = os.path.join(UPLOAD_DIR, filename1)
        with open(filepath1, "wb") as buffer:
            shutil.copyfileobj(foto1.file, buffer)
        final_photo1 = filepath1

    final_photo2 = existing_photo2
    if foto2 and foto2.filename:
        filename2 = f"{code}_FOTO2_{foto2.filename}"
        filepath2 = os.path.join(UPLOAD_DIR, filename2)
        with open(filepath2, "wb") as buffer:
            shutil.copyfileobj(foto2.file, buffer)
        final_photo2 = filepath2

    all_photos = [p for p in [final_photo1, final_photo2] if p]

    if id and id.strip() != "":
        cursor.execute("""
            UPDATE protocols SET
                code = ?, contractor_header = ?, header_title = ?, partida_desc = ?,
                project_name = ?, client = ?, contractor = ?, sector = ?, subsector = ?,
                element_code = ?, ref_docs = ?, inspection_date = ?, status = ?, observations = ?,
                field_engineer = ?, qa_qc_engineer = ?, supervisor_engineer = ?, esp_supervisor = ?,
                firmas_contratista = ?, firmas_supervision = ?, checklist_eval = ?, conc_params = ?,
                photo1_desc = ?, photo2_desc = ?, photos = ?
            WHERE id = ?
        """, (
            code, contractor_header, header_title, partida_desc,
            project_name, client, contractor, sector, subsector,
            element_code, ref_docs, inspection_date, status, observations,
            field_engineer, qa_qc_engineer, supervisor_engineer, esp_supervisor,
            firmas_contratista, firmas_supervision, checklist_eval, conc_params,
            photo1_desc, photo2_desc, json.dumps(all_photos), int(id)
        ))
    else:
        cursor.execute("""
            INSERT INTO protocols (
                code, contractor_header, header_title, partida_desc, project_name,
                client, contractor, sector, subsector, element_code, ref_docs,
                inspection_date, status, observations, field_engineer, qa_qc_engineer,
                supervisor_engineer, esp_supervisor, firmas_contratista, firmas_supervision,
                checklist_eval, conc_params, photos, photo1_desc, photo2_desc
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            code, contractor_header, header_title, partida_desc, project_name,
            client, contractor, sector, subsector, element_code, ref_docs,
            inspection_date, status, observations, field_engineer, qa_qc_engineer,
            supervisor_engineer, esp_supervisor, firmas_contratista, firmas_supervision,
            checklist_eval, conc_params, json.dumps(all_photos), photo1_desc, photo2_desc
        ))

    conn.commit()
    conn.close()
    return {"status": "ok", "message": "Protocolo guardado con éxito."}

@app.delete("/api/protocols/{protocol_id}")
async def delete_protocol(protocol_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM protocols WHERE id = ?", (protocol_id,))
    conn.commit()
    conn.close()
    return {"status": "ok", "message": "Protocolo eliminado."}

@app.get("/api/protocols/{protocol_id}/checklist_pdf")
async def get_checklist_pdf(protocol_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM protocols WHERE id = ?", (protocol_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Protocolo no encontrado")

    protocol = dict(row)
    pdf_filename = f"Checklist_{protocol['code'].replace('/', '_')}.pdf"
    pdf_path = os.path.join(EXPORT_DIR, pdf_filename)
    generate_checklist_pdf(protocol, pdf_path)

    return FileResponse(pdf_path, media_type="application/pdf", filename=pdf_filename)

@app.get("/api/protocols/{protocol_id}/photopanel_pdf")
async def get_photopanel_pdf(protocol_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM protocols WHERE id = ?", (protocol_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Protocolo no encontrado")

    protocol = dict(row)
    pdf_filename = f"Panel_Fotos_{protocol['code'].replace('/', '_')}.pdf"
    pdf_path = os.path.join(EXPORT_DIR, pdf_filename)
    generate_photopanel_pdf(protocol, pdf_path)

    return FileResponse(pdf_path, media_type="application/pdf", filename=pdf_filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
