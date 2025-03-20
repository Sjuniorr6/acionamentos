from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.colors import Color, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import os

# Definindo a cor amarela clara
light_yellow = Color(1, 1, 0.8)

def generate_pdf(instance):
    def format_datetime(value):
        if isinstance(value, datetime):
            return value.strftime("%d/%m/%Y %H:%M")
        return value or "Não Informado"

    # Caminho absoluto do logotipo
    logo_path = os.path.join('static', 'logo-golden.png')

    # Verifique se o logotipo existe
    if not os.path.exists(logo_path):
        raise FileNotFoundError(f"Logotipo não encontrado no caminho: {logo_path}")

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=36,
        leftMargin=36,
        rightMargin=36,
        bottomMargin=36
    )
    elements = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenteredTitle', alignment=1, fontSize=14, spaceAfter=10))
    styles.add(ParagraphStyle(name='SectionTitle', alignment=0, fontSize=12, spaceAfter=5, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='BodyTextWithWrap', alignment=0, fontSize=10, spaceAfter=10, wordWrap='CJK'))

    # Adicione o logotipo
    try:
        logo = Image(logo_path, width=70, height=70)
        elements.append(logo)
    except Exception as e:
        elements.append(Paragraph(f"Erro ao carregar o logotipo: {e}", styles['BodyText']))

    elements.append(Spacer(1, 15))

    # Título e protocolo
    elements.append(Paragraph(f"Protocolo: {instance.protocolo or 'Não Informado'}", styles['CenteredTitle']))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("Relatório de Acionamento", styles['CenteredTitle']))

    # Informações Gerais
    general_info = [
        [Paragraph("<b>Cliente:</b>", styles['BodyText']), instance.cliente or "Não Informado",
         Paragraph("<b>Prestador:</b>", styles['BodyText']), getattr(instance.prestador, 'nome', "Não Informado")],
        [Paragraph("<b>Data/Hora Inicial:</b>", styles['BodyText']), format_datetime(instance.data_hora_inicial),
         Paragraph("<b>Data/Hora Final:</b>", styles['BodyText']), format_datetime(instance.data_hora_final)],
        [Paragraph("<b>SLA:</b>", styles['BodyText']), instance.sla or "Não Informado",
         Paragraph("<b>Previsão de Chegada:</b>", styles['BodyText']), format_datetime(instance.previsa_chegada)],
    ]

    # Tabela de Informações Gerais
    general_table = Table(general_info, colWidths=[100, 150, 100, 150])
    general_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (0, 2), light_yellow),
        ('BACKGROUND', (2, 0), (2, 2), light_yellow),
    ]))
    elements.append(general_table)
    elements.append(Spacer(1, 15))

    # Informações do Veículo
    vehicle_info = [
        [Paragraph("<b>Placa:</b>", styles['BodyText']), instance.placas1 or "Não Informado",
         Paragraph("<b>Modelo:</b>", styles['BodyText']), instance.modelo or "Não Informado"],
        [Paragraph("<b>Ano:</b>", styles['BodyText']), instance.ano or "Não Informado",
         Paragraph("<b>Cor:</b>", styles['BodyText']), instance.cor or "Não Informado"],
        [Paragraph("<b>KM Inicial:</b>", styles['BodyText']), instance.km_inicial or "Não Informado",
         Paragraph("<b>KM Final:</b>", styles['BodyText']), instance.km_final or "Não Informado"],
        [Paragraph("<b>KM Total:</b>", styles['BodyText']), instance.km_total or "Não Informado",
         Paragraph("<b>KM Excedente:</b>", styles['BodyText']), instance.km_excedente or "Não Informado"],
    ]

    # Tabela de Informações do Veículo
    vehicle_table = Table(vehicle_info, colWidths=[100, 150, 100, 150])
    vehicle_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (0, 3), light_yellow),
        ('BACKGROUND', (2, 0), (2, 3), light_yellow),
    ]))
    elements.append(vehicle_table)
    elements.append(Spacer(1, 15))

    # Campo de Descrição (fora da tabela)
    elements.append(Paragraph("<b>Descrição:</b>", styles['BodyText']))
    description_paragraph = Paragraph(instance.descricao or "Não Informado", styles['BodyTextWithWrap'])
    elements.append(description_paragraph)
    elements.append(Spacer(1, 15))

    # Imagens em formato de 3 por linha
    elements.append(Paragraph("Imagens do Acionamento :", styles['CenteredTitle']))
    image_fields = [
        'imagem1', 'imagem2', 'imagem3', 'imagem4', 'imagem5', 'imagem6',
        'imagem7', 'imagem8', 'imagem9', 'imagem10', 'imagem11', 'imagem12',
        'imagem13', 'imagem14'
    ]

    # Lista para consolidar todas as linhas de imagens
    consolidated_image_rows = []

    # Processar imagens em grupos de 3
    image_row = []
    for field_name in image_fields:
        image_field = getattr(instance, field_name)
        if image_field and hasattr(image_field, 'path') and os.path.exists(image_field.path):
            try:
                img = Image(image_field.path, width=150, height=150, hAlign='CENTER')  # Ajuste o tamanho proporcionalmente
                image_row.append(img)
                if len(image_row) == 3:  # Quando atingir 3 imagens, adicionar a linha à tabela
                    consolidated_image_rows.append(image_row)
                    image_row = []
            except Exception as e:
                elements.append(Paragraph(f"Erro ao carregar a imagem {field_name}: {e}", styles['BodyText']))

    # Adicionar qualquer linha incompleta que tenha menos de 3 imagens
    if image_row:
        consolidated_image_rows.append(image_row)

    # Adicionar tabela consolidada com todas as linhas
    if consolidated_image_rows:
        for row in consolidated_image_rows:
            while len(row) < 3:
                row.append("")
            image_table = Table([row], colWidths=[180, 180, 180])  # Largura de cada coluna
            image_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, black),
                ('BOX', (0, 0), (-1, -1), 0.5, black),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(image_table)
            elements.append(Spacer(1, 20))
    else:
        elements.append(Paragraph("Nenhuma imagem anexada.", styles['BodyText']))

    # Construir o PDF com o rodapé fixado ao final da página
    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data

def add_footer(canvas, doc):
    """
    Adiciona o rodapé ao final da página.
    """
    footer_text = "www.grupogoldensat.com.br - Rua Haiti,129 - Parque das Nações - Santo André CEP:09280-390"
    canvas.saveState()
    canvas.setFont("Helvetica", 9)

    # Obtém a posição do rodapé
    page_width, page_height = letter
    text_width = canvas.stringWidth(footer_text, "Helvetica", 9)
    x_position = (page_width - text_width) / 2
    y_position = 30  # Define o rodapé ao final da página

    # Desenha o texto
    canvas.drawString(x_position, y_position, footer_text)
    canvas.restoreState()






