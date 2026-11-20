import os
import json
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm

LOGO_PATH = os.path.join(os.path.dirname(__file__), "static", "logo_consorcio.png")

def get_base_styles():
    return {
        'title_main': ParagraphStyle('TM', fontName='Helvetica-Bold', fontSize=10.5, leading=12, alignment=1),
        'title_desc': ParagraphStyle('TD', fontName='Helvetica-Bold', fontSize=6.8, leading=8.0, alignment=1),
        'p_bold_center': ParagraphStyle('PBC', fontName='Helvetica-Bold', fontSize=5.0, leading=6.0, alignment=1),
        'p_center': ParagraphStyle('PC', fontName='Helvetica', fontSize=5.2, leading=6.2, alignment=1),
        'p_left': ParagraphStyle('PL', fontName='Helvetica', fontSize=4.6, leading=5.4),
        'p_left_bold': ParagraphStyle('PLB', fontName='Helvetica-Bold', fontSize=4.8, leading=5.6),
        'p_meta_lbl': ParagraphStyle('PML', fontName='Helvetica-Bold', fontSize=5.2, leading=6.2),
        'p_meta_val': ParagraphStyle('PMV', fontName='Helvetica', fontSize=5.0, leading=5.8),
    }

def build_header_and_meta(data: dict, st: dict):
    # Si existe el logo recortado, lo colocamos en la celda izquierda
    if os.path.exists(LOGO_PATH):
        try:
            logo_img = Image(LOGO_PATH, width=3.2*cm, height=1.35*cm)
            logo_cell = logo_img
        except:
            logo_cell = Paragraph(f"<b>{data.get('contractor_header', 'CONSORCIO<br/>LA MERCED')}</b>", st['title_main'])
    else:
        logo_cell = Paragraph(f"<b>{data.get('contractor_header', 'CONSORCIO<br/>LA MERCED')}</b>", st['title_main'])

    partida_default = "01.07.04.01, 01.07.04.02 y 01.07.04.03&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CONCRETO f 'c=210 kg/cm2 P/ COLUMNAS, ENCOFRADO Y DESENCOFRADO P/ COLUMNAS Y ACERO DE REFUERZO fy=4200 kg/cm2"
    partida_val = data.get('partida_desc') or partida_default

    header_data = [
        [
            logo_cell,
            Paragraph(f"<b>{data.get('header_title', 'CONTROL DE CALIDAD')}</b>", st['title_main'])
        ],
        [
            "",
            Paragraph(f"<b>{partida_val}</b>", st['title_desc'])
        ]
    ]
    t_header = Table(header_data, colWidths=[3.5*cm, 24.7*cm], rowHeights=[0.75*cm, 0.65*cm])
    t_header.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.0, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('SPAN', (0,0), (0,1)),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))

    # Metadatos idénticos al original
    obra_text = data.get('project_name', '')
    cliente_text = data.get('client', 'GOBIERNO REGIONAL DE JUNIN')
    estructura_text = data.get('sector', '')
    ubicacion_text = data.get('subsector', '')
    elemento_text = data.get('element_code', '')
    plano_text = data.get('ref_docs', '')
    fecha_text = data.get('inspection_date', '')
    reg_no = data.get('code', '')

    meta_data = [
        [
            Paragraph("<b>OBRA</b>", st['p_meta_lbl']), Paragraph(f": {obra_text}", st['p_meta_val']),
            Paragraph("<b>Registro Nº:</b>", st['p_meta_lbl']), Paragraph(reg_no, st['p_meta_val'])
        ],
        [
            Paragraph("<b>CLIENTE</b>", st['p_meta_lbl']), Paragraph(f": {cliente_text}", st['p_meta_val']),
            Paragraph("<b>Fecha:</b>", st['p_meta_lbl']), Paragraph(fecha_text, st['p_meta_val'])
        ],
        [
            Paragraph("<b>ESTRUCTURA</b>", st['p_meta_lbl']), Paragraph(f": {estructura_text}", st['p_meta_val']),
            Paragraph("<b>FECHA</b>", st['p_meta_lbl']), Paragraph(f": {fecha_text}", st['p_meta_val'])
        ],
        [
            Paragraph("<b>UBICACIÓN</b>", st['p_meta_lbl']), Paragraph(f": {ubicacion_text}", st['p_meta_val']),
            Paragraph("<b>ELEMENTO</b>", st['p_meta_lbl']), Paragraph(f": {elemento_text}", st['p_meta_val'])
        ],
        [
            Paragraph("<b>PLANO DE REFERENCIA</b>", st['p_meta_lbl']), Paragraph(f": {plano_text}", st['p_meta_val']),
            "", ""
        ]
    ]

    t_meta = Table(meta_data, colWidths=[3.5*cm, 16.5*cm, 2.5*cm, 5.7*cm], rowHeights=[0.38*cm, 0.32*cm, 0.32*cm, 0.32*cm, 0.32*cm])
    t_meta.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.0, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('SPAN', (1,4), (3,4)),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))

    return t_header, t_meta

def build_firmas_table(data: dict, st: dict):
    status = data.get('status', 'APROBADO')
    aprob_text = "APROBADO ( X )          DESAPROBADO (   )" if status == 'APROBADO' else "APROBADO (   )          DESAPROBADO ( X )"

    contratista_label = data.get('firmas_contratista', 'CONSORCIO LA MERCED')
    supervision_label = data.get('firmas_supervision', 'JOGAMA CONSULTORIA Y CONSTRUCCIONES GENERALES EIRL')

    residente_nom = data.get('field_engineer', 'RESIDENTE')
    esp_est_nom = data.get('qa_qc_engineer', 'ESPECIALISTA EN ESTRUCTURAS')
    supervisor_nom = data.get('supervisor_engineer', 'SUPERVISOR')
    esp_sup_nom = data.get('esp_supervisor', 'ESPECIALISTA ESTRUCTURA')

    t_firmas = Table([
        [
            Paragraph(f"<b>APROBACIÓN PREVIA AL VACIADO:</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{aprob_text}", st['p_meta_lbl']),
            ""
        ],
        [
            Paragraph(f"<b>{contratista_label}</b>", st['p_bold_center']),
            Paragraph(f"<b>{supervision_label}</b>", st['p_bold_center'])
        ],
        [
            Table([
                [
                    Paragraph(f"<br/><br/><br/>____________________________________<br/><b>{residente_nom}</b>", st['p_bold_center']),
                    Paragraph(f"<br/><br/><br/>____________________________________<br/><b>{esp_est_nom}</b>", st['p_bold_center'])
                ]
            ], colWidths=[7.05*cm, 7.05*cm]),
            Table([
                [
                    Paragraph(f"<br/><br/><br/>____________________________________<br/><b>{supervisor_nom}</b>", st['p_bold_center']),
                    Paragraph(f"<br/><br/><br/>____________________________________<br/><b>{esp_sup_nom}</b>", st['p_bold_center'])
                ]
            ], colWidths=[7.05*cm, 7.05*cm])
        ]
    ], colWidths=[14.1*cm, 14.1*cm], rowHeights=[0.38*cm, 0.32*cm, 1.8*cm])

    t_firmas.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.0, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('SPAN', (0,0), (1,0)),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    return t_firmas

def generate_checklist_pdf(protocol: dict, output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        rightMargin=7*mm,
        leftMargin=7*mm,
        topMargin=6*mm,
        bottomMargin=6*mm
    )
    st = get_base_styles()
    story = []

    t_header, t_meta = build_header_and_meta(protocol, st)
    story.append(t_header)
    story.append(t_meta)

    # 1. PARTE IZQUIERDA: 4 TABLAS
    checklist_eval = protocol.get('checklist_eval')
    if isinstance(checklist_eval, str):
        try:
            checklist_eval = json.loads(checklist_eval)
        except:
            checklist_eval = {}
    if not isinstance(checklist_eval, dict):
        checklist_eval = {}

    def make_section_table(title, items, key_prefix):
        rows = [[
            Paragraph(f"<b>{title}</b>", st['p_left_bold']),
            Paragraph("<b>SI</b>", st['p_bold_center']),
            Paragraph("<b>NO</b>", st['p_bold_center']),
            Paragraph("<b>NA</b>", st['p_bold_center'])
        ]]
        for idx, it in enumerate(items, 1):
            val = checklist_eval.get(f"{key_prefix}_{idx}", "SI")
            si_mark = "X" if val == "SI" else ""
            no_mark = "X" if val == "NO" else ""
            na_mark = "X" if val == "NA" else ""
            rows.append([
                Paragraph(f"{idx}. {it}", st['p_left']),
                Paragraph(si_mark, st['p_center']),
                Paragraph(no_mark, st['p_center']),
                Paragraph(na_mark, st['p_center'])
            ])
        t = Table(rows, colWidths=[5.5*cm, 0.5*cm, 0.5*cm, 0.5*cm], rowHeights=[0.35*cm] + [0.38*cm]*len(items))
        t.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.7, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.4, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (1,1), (-1,-1), 'CENTER'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 1),
            ('RIGHTPADDING', (0,0), (-1,-1), 1),
        ]))
        return t

    from checklist_catalog import CHECKLIST_CATALOG

    # Determinar el tipo de elemento para cargar los ítems correspondientes
    el_code_upper = str(protocol.get('element_code', '')).upper()
    sec_upper = str(protocol.get('sector', '')).upper()
    sub_upper = str(protocol.get('subsector', '')).upper()
    partida_upper = str(protocol.get('partida_desc', '')).upper()
    full_context = f"{el_code_upper} {sec_upper} {sub_upper} {partida_upper}"

    catalog_key = "COLUMNAS"
    if any(k in full_context for k in ['ZAPATA', 'CIMENTACI', 'EXCAVACI', 'SOLADO']):
        catalog_key = "ZAPATAS"
    elif any(k in full_context for k in ['CISTERNA', 'MURO', 'CONTENCI', 'TANQUE', 'WATERSTOP']):
        catalog_key = "MUROS"
    elif any(k in full_context for k in ['SOBRECIMIENTO', 'CERCO']):
        catalog_key = "SOBRECIMIENTOS"
    elif any(k in full_context for k in ['LOSA', 'ALIGERAD', 'TECHO', 'LADRILLO', 'VIGUETA']):
        catalog_key = "LOSAS"

    active_cat = CHECKLIST_CATALOG.get(catalog_key, CHECKLIST_CATALOG["COLUMNAS"])

    enc_items = active_cat["items1"]
    acero_items = active_cat["items2"]
    conc_items = active_cat["items3"]
    inst_items = active_cat["items4"]

    t_enc = make_section_table(active_cat["title1"], enc_items, "enc")
    t_acero = make_section_table(active_cat["title2"], acero_items, "ace")
    t_conc = make_section_table(active_cat["title3"], conc_items, "con")
    t_inst = make_section_table(active_cat["title4"], inst_items, "ins")

    grid_left = Table([
        [Paragraph("<b>1. INSPECCIÓN PREVIA AL VACIADO</b>", st['p_left_bold']), ""],
        [t_enc, t_acero],
        [t_conc, t_inst]
    ], colWidths=[7.05*cm, 7.05*cm])
    grid_left.setStyle(TableStyle([
        ('SPAN', (0,0), (1,0)),
        ('BOX', (0,0), (-1,-1), 1.0, colors.black),
        ('LINEBELOW', (0,0), (1,0), 0.7, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))

    # 2. PARTE DERECHA: CONCRETO Y PROBETAS
    conc_params = protocol.get('conc_params')
    if isinstance(conc_params, str):
        try:
            conc_params = json.loads(conc_params)
        except:
            conc_params = {}
    if not isinstance(conc_params, dict):
        conc_params = {}

    fc_val = conc_params.get('fc', '210')
    vol_val = conc_params.get('volumen', '')
    slump_val = conc_params.get('slump', '5"-6"')
    t_conc_obra = "X" if conc_params.get('tipo_concreto') == 'OBRA' else ""
    t_conc_pre = "X" if conc_params.get('tipo_concreto') == 'PREMEZCLADO' else ""
    t_coloc_dir = "X" if conc_params.get('tipo_colocacion') == 'DIRECTO' else ""
    t_coloc_bom = "X" if conc_params.get('tipo_colocacion') == 'BOMBA' else ""
    t_acab_cara = "X" if conc_params.get('tipo_acabado') == 'CARAVISTA' else ""
    t_acab_frot = "X" if conc_params.get('tipo_acabado') == 'FROTACHADO' else ""

    p_conc_lbl = ParagraphStyle('PCL', fontName='Helvetica', fontSize=4.8, leading=5.6)
    p_conc_val = ParagraphStyle('PCV', fontName='Helvetica-Bold', fontSize=5.0, leading=5.8, alignment=1)

    # Cuadrito con casillas idéntico
    t_conc_header = [
        [
            Paragraph("FECHA:", p_conc_lbl), Paragraph(protocol.get('inspection_date', ''), p_conc_val), "",
            Paragraph("TIPO DE CONCRETO :", p_conc_lbl), Paragraph("HECHO EN OBRA", p_conc_lbl), Paragraph(t_conc_obra, p_conc_val), Paragraph("PREMEZCLADO", p_conc_lbl), Paragraph(t_conc_pre, p_conc_val)
        ],
        [
            Paragraph("f'c DISEÑO:", p_conc_lbl), Paragraph(fc_val, p_conc_val), Paragraph("kg/cm²", p_conc_lbl),
            Paragraph("TIPO DE COLOCACIÓN :", p_conc_lbl), Paragraph("DIRECTO", p_conc_lbl), Paragraph(t_coloc_dir, p_conc_val), Paragraph("CON BOMBA", p_conc_lbl), Paragraph(t_coloc_bom, p_conc_val)
        ],
        [
            Paragraph("VOLUMEN", p_conc_lbl), Paragraph(f"{vol_val} m³", p_conc_val), "",
            Paragraph("TIPO DE ACABADO :", p_conc_lbl), Paragraph("CARAVISTA", p_conc_lbl), Paragraph(t_acab_cara, p_conc_val), Paragraph("FROTACHADO", p_conc_lbl), Paragraph(t_acab_frot, p_conc_val)
        ],
        [
            Paragraph("SLUMP", p_conc_lbl), Paragraph(slump_val, p_conc_val), Paragraph('"', p_conc_lbl),
            "", "", "", "", ""
        ]
    ]
    t_conc_top = Table(t_conc_header, colWidths=[1.8*cm, 1.4*cm, 1.1*cm, 2.7*cm, 2.4*cm, 0.5*cm, 2.5*cm, 0.5*cm], rowHeights=[0.4*cm]*4)
    t_conc_top.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (4,0), (4,0), 0.5, colors.black),
        ('BOX', (6,0), (6,0), 0.5, colors.black),
        ('BOX', (4,1), (4,1), 0.5, colors.black),
        ('BOX', (6,1), (6,1), 0.5, colors.black),
        ('BOX', (4,2), (4,2), 0.5, colors.black),
        ('BOX', (6,2), (6,2), 0.5, colors.black),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 1),
    ]))

    # Remisiones con tamaño exacto en una sola línea
    truck_header = [
        [
            Paragraph("Guia de Remisión", st['p_bold_center']),
            Paragraph("VOLUMEN", st['p_bold_center']),
            Paragraph("SALIDA<br/>PLANTA", st['p_bold_center']),
            Paragraph("LLEGADA<br/>OBRA", st['p_bold_center']),
            Paragraph("HORA<br/>INICIO", st['p_bold_center']),
            Paragraph("HORA<br/>FIN", st['p_bold_center']),
            Paragraph("SLUMP<br/>(\")", st['p_bold_center']),
            Paragraph("TEMP.<br/>AMBIENTE", st['p_bold_center']),
            Paragraph("TEMP.<br/>CONCRETO", st['p_bold_center']),
            Paragraph("NÚMERO<br/>PROBETAS", st['p_bold_center']),
            Paragraph("CÓDIGO DE<br/>PROBETAS", st['p_bold_center'])
        ]
    ]
    remisiones = conc_params.get('remisiones', [])
    for idx in range(8):
        if idx < len(remisiones):
            r = remisiones[idx]
            truck_header.append([
                Paragraph(r.get('guia', ''), st['p_center']),
                Paragraph(str(r.get('vol', '')), st['p_center']),
                Paragraph(r.get('salida', ''), st['p_center']),
                Paragraph(r.get('llegada', ''), st['p_center']),
                Paragraph(r.get('inicio', ''), st['p_center']),
                Paragraph(r.get('fin', ''), st['p_center']),
                Paragraph(r.get('slump', ''), st['p_center']),
                Paragraph(r.get('temp_amb', ''), st['p_center']),
                Paragraph(r.get('temp_conc', ''), st['p_center']),
                Paragraph(str(r.get('prob', '')), st['p_center']),
                Paragraph(r.get('cod_prob', ''), st['p_center'])
            ])
        else:
            truck_header.append(["", "", "", "", "", "", "", "", "", "", ""])

    t_trucks = Table(
        truck_header,
        colWidths=[2.1*cm, 1.1*cm, 1.05*cm, 1.05*cm, 1.0*cm, 1.0*cm, 0.9*cm, 1.4*cm, 1.4*cm, 1.25*cm, 1.65*cm],
        rowHeights=[0.6*cm] + [0.44*cm]*8
    )
    t_trucks.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.8, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    obs_content = protocol.get('observations', 'Conforme con planos estructurales.')
    t_right_panel = Table([
        [Paragraph("<b>2. COLOCACIÓN DE CONCRETO</b>", st['p_left_bold'])],
        [t_conc_top],
        [t_trucks],
        [Paragraph(f"<b>3. COMENTARIOS:</b> {obs_content}", st['p_left_bold'])]
    ], colWidths=[13.9*cm])
    t_right_panel.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.0, colors.black),
        ('LINEBELOW', (0,0), (0,0), 0.7, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (0,0), (-1,-1), 1),
        ('RIGHTPADDING', (0,0), (-1,-1), 1),
    ]))

    t_main_body = Table([[grid_left, t_right_panel]], colWidths=[14.2*cm, 14.0*cm])
    t_main_body.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_main_body)

    t_firmas = build_firmas_table(protocol, st)
    story.append(t_firmas)

    doc.build(story)
    return output_path

def generate_photopanel_pdf(protocol: dict, output_path: str):
    from PIL import Image as PILImage
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        rightMargin=7*mm,
        leftMargin=7*mm,
        topMargin=6*mm,
        bottomMargin=6*mm
    )
    st = get_base_styles()
    story = []

    photo_proto = dict(protocol)
    photo_proto['header_title'] = "CONTROL DE CALIDAD - PANEL DE FOTOGRAFÍAS"
    t_header, t_meta = build_header_and_meta(photo_proto, st)
    story.append(t_header)
    story.append(t_meta)

    # Rutas explícitas de foto 1 y foto 2
    photo1_path = protocol.get('photo1_path')
    photo2_path = protocol.get('photo2_path')

    # Fallback a lista photos si no están explícitas
    if not photo1_path or not photo2_path:
        photos = []
        if isinstance(protocol.get('photos'), str):
            try:
                photos = json.loads(protocol['photos'])
            except:
                photos = []
        elif isinstance(protocol.get('photos'), list):
            photos = protocol['photos']
        
        if not photo1_path and len(photos) >= 1:
            photo1_path = photos[0]
        if not photo2_path and len(photos) >= 2:
            photo2_path = photos[1]

    desc1 = protocol.get('photo1_desc', 'FOTO 1: ARMADURA DE ACERO Y ENCOFRADO DE COLUMNA')
    desc2 = protocol.get('photo2_desc', 'FOTO 2: VERIFICACIÓN DE VERTICALIDAD Y APUNTALAMIENTO')

    # Caja máxima para cada foto dentro de su mitad: ancho max 13.5cm, alto max 11.2cm
    max_w_cm = 13.5
    max_h_cm = 11.2

    def create_photo_cell(p_path, p_desc):
        if p_path and os.path.exists(p_path):
            try:
                pil_im = PILImage.open(p_path)
                iw, ih = pil_im.size
                aspect = iw / ih
                box_aspect = max_w_cm / max_h_cm
                if aspect > box_aspect:
                    calc_w = max_w_cm
                    calc_h = max_w_cm / aspect
                else:
                    calc_h = max_h_cm
                    calc_w = max_h_cm * aspect
                
                img_obj = Image(p_path, width=calc_w*cm, height=calc_h*cm)
                cell_table = Table(
                    [
                        [img_obj],
                        [Paragraph(f"<b>{p_desc}</b>", st['p_bold_center'])]
                    ],
                    colWidths=[13.9*cm],
                    rowHeights=[11.6*cm, 0.8*cm]
                )
                cell_table.setStyle(TableStyle([
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('VALIGN', (0,0), (0,0), 'MIDDLE'),
                    ('VALIGN', (0,1), (0,1), 'MIDDLE'),
                    ('TOPPADDING', (0,0), (-1,-1), 0),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                ]))
                return cell_table
            except Exception as e:
                pass
        
        # Celda vacía centrada
        cell_empty = Table(
            [[Paragraph(f"<b>{p_desc}</b><br/><font size=5 color=gray>(Registro fotográfico obligatorio)</font>", st['p_bold_center'])]],
            colWidths=[13.9*cm],
            rowHeights=[12.4*cm]
        )
        cell_empty.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        return cell_empty

    cell1 = create_photo_cell(photo1_path, desc1)
    cell2 = create_photo_cell(photo2_path, desc2)

    photo_box = Table([[cell1, cell2]], colWidths=[14.1*cm, 14.1*cm], rowHeights=[12.6*cm])
    photo_box.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.0, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(photo_box)

    t_firmas = build_firmas_table(protocol, st)
    story.append(t_firmas)

    doc.build(story)
    return output_path
