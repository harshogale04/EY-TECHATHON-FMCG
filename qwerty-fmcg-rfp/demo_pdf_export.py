import json
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register fonts that support rupee symbol (fallback to standard if not available)
try:
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
    FONT_NAME = 'DejaVuSans'
    FONT_NAME_BOLD = 'DejaVuSans-Bold'
except:
    # Fallback to standard fonts if DejaVu not available
    FONT_NAME = 'Helvetica'
    FONT_NAME_BOLD = 'Helvetica-Bold'

# Load RFP data
with open("rfp_response.json", "r") as f:
    rfp_data = json.load(f)

# PDF Setup with better margins
doc = SimpleDocTemplate(
    "NHAI_proposal.pdf", 
    pagesize=A4,
    rightMargin=25*mm, 
    leftMargin=25*mm,
    topMargin=25*mm, 
    bottomMargin=25*mm
)

styles = getSampleStyleSheet()
story = []

# ============= CUSTOM STYLES =============
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],
    fontSize=24,
    leading=30,
    spaceAfter=6,
    textColor=colors.HexColor('#1a3a52'),
    alignment=TA_CENTER,
    fontName=FONT_NAME_BOLD
)

subtitle_style = ParagraphStyle(
    'Subtitle',
    parent=styles['Normal'],
    fontSize=16,
    leading=20,
    spaceAfter=20,
    textColor=colors.HexColor('#2c5f7f'),
    alignment=TA_CENTER,
    fontName=FONT_NAME_BOLD
)

section_header_style = ParagraphStyle(
    'SectionHeader',
    parent=styles['Heading2'],
    fontSize=14,
    leading=18,
    spaceAfter=12,
    spaceBefore=20,
    textColor=colors.HexColor('#1a3a52'),
    fontName=FONT_NAME_BOLD,
    borderWidth=1,
    borderColor=colors.HexColor('#2c5f7f'),
    borderPadding=8,
    backColor=colors.HexColor('#e8f1f7')
)

footer_style = ParagraphStyle(
    'Footer',
    parent=styles['Normal'],
    fontSize=9,
    textColor=colors.grey,
    alignment=TA_CENTER,
    spaceAfter=0
)

# Helper function to format currency (using Rs. instead of ₹ for compatibility)
def format_currency(amount):
    return f"Rs. {int(amount):,}"

# ============= DOCUMENT HEADER =============
title = Paragraph("RFP PROPOSAL", title_style)
story.append(title)

subtitle = Paragraph("NH-44 Four Laning Project", subtitle_style)
story.append(subtitle)
story.append(Spacer(1, 10))

# ============= CLIENT INFO BOX =============
# NO <b> TAGS - Using TableStyle instead
client_info = [
    ['Client', rfp_data['client_name']],
    ['Project ID', rfp_data['rfp_id']],
    ['Due Date', rfp_data['due_date']],
    ['Strategic Fit Score', f'{rfp_data["strategic_fit_score"]}%']
]

client_table = Table(client_info, colWidths=[2.3*inch, 4*inch])
client_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#e8f1f7')),
    ('BACKGROUND', (1,0), (1,-1), colors.white),
    ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#1a3a52')),
    ('ALIGN', (0,0), (0,-1), 'LEFT'),
    ('ALIGN', (1,0), (1,-1), 'LEFT'),
    ('FONTNAME', (0,0), (0,-1), FONT_NAME_BOLD),  # Bold for labels
    ('FONTNAME', (1,0), (1,-1), FONT_NAME),       # Regular for values
    ('FONTSIZE', (0,0), (-1,-1), 11),
    ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#2c5f7f')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8)
]))
story.append(client_table)
story.append(Spacer(1, 25))

# ============= PROJECT SUMMARY BOX =============
story.append(Paragraph("PROJECT SUMMARY", section_header_style))

pricing = rfp_data["pricing_summary"]
summary_data = [
    ['Project Value', format_currency(pricing["grand_total"])],
    ['Material Cost', format_currency(pricing["material_cost"])],
    ['Testing Cost', format_currency(pricing["test_cost"])],
    ['Status', 'AI Generated - Ready for Review']
]

summary_table = Table(summary_data, colWidths=[2.3*inch, 4*inch])
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f5f9fc')),
    ('BACKGROUND', (1,0), (1,-1), colors.white),
    ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#333333')),
    ('ALIGN', (0,0), (0,-1), 'LEFT'),
    ('ALIGN', (1,0), (1,-1), 'RIGHT'),
    ('FONTNAME', (0,0), (0,-1), FONT_NAME_BOLD),
    ('FONTNAME', (1,0), (1,-1), FONT_NAME),
    ('FONTSIZE', (0,0), (-1,-1), 11),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c5d9e8')),
    ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#2c5f7f')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8)
]))
story.append(summary_table)
story.append(Spacer(1, 25))

# ============= BILL OF MATERIALS =============
story.append(Paragraph("BILL OF MATERIALS & PRICING", section_header_style))

# NO <b> TAGS in data - formatting handled by TableStyle
bom_data = [
    ['Product Description', 'SKU', 'Qty', 'Rate', 'Total', 'Match'],
    ['1.1kV Cable 240mm²', 'CABLE-1.1KV-240CU-AL', '1000 m', 'Rs. 450/m', format_currency(450000), '90%'],
    ['0.6kV Cable 185mm²', 'CABLE-0.6KV-185CU-AL', '500 m', 'Rs. 320/m', format_currency(160000), '90%'],
    ['0.4kV Cable 50mm²', 'CABLE-0.4KV-50CU-AL', '2000 m', 'Rs. 95/m', format_currency(190000), '90%']
]

# Calculate subtotals
material_total = int(pricing["material_cost"])
test_total = int(pricing["test_cost"])
grand_total = int(pricing["grand_total"])

# Add subtotal rows (NO <b> TAGS)
bom_data.append(['', '', '', 'Material Subtotal', format_currency(material_total), ''])
bom_data.append(['', '', '', 'Testing & QA', format_currency(test_total), ''])
bom_data.append(['', '', '', 'GRAND TOTAL', format_currency(grand_total), ''])

bom_table = Table(bom_data, colWidths=[1.6*inch, 1.5*inch, 0.7*inch, 1*inch, 1.2*inch, 0.7*inch])
bom_table.setStyle(TableStyle([
    # Header row
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3a52')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), FONT_NAME_BOLD),
    ('FONTSIZE', (0,0), (-1,0), 10),
    ('ALIGN', (0,0), (0,0), 'LEFT'),      # Product Description - LEFT
    ('ALIGN', (1,0), (1,0), 'LEFT'),      # SKU - LEFT
    ('ALIGN', (2,0), (2,0), 'CENTER'),    # Qty - CENTER
    ('ALIGN', (3,0), (3,0), 'RIGHT'),     # Rate - RIGHT
    ('ALIGN', (4,0), (4,0), 'RIGHT'),     # Total - RIGHT
    ('ALIGN', (5,0), (5,0), 'CENTER'),    # Match - CENTER
    
    # Data rows (items)
    ('BACKGROUND', (0,1), (-1,3), colors.white),
    ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor('#333333')),
    ('FONTNAME', (0,1), (-1,3), FONT_NAME),
    ('FONTSIZE', (0,1), (-1,3), 9),
    ('ALIGN', (0,1), (0,3), 'LEFT'),      # Product - LEFT
    ('ALIGN', (1,1), (1,3), 'LEFT'),      # SKU - LEFT
    ('ALIGN', (2,1), (2,3), 'CENTER'),    # Qty - CENTER
    ('ALIGN', (3,1), (3,3), 'RIGHT'),     # Rate - RIGHT
    ('ALIGN', (4,1), (4,3), 'RIGHT'),     # Total - RIGHT
    ('ALIGN', (5,1), (5,3), 'CENTER'),    # Match - CENTER
    ('WORDWRAP', (0,0), (-1,-1), True),   # Enable word wrap
    
    # Subtotal rows (make bold through style)
    ('BACKGROUND', (0,4), (-1,5), colors.HexColor('#f5f9fc')),
    ('FONTNAME', (3,4), (4,5), FONT_NAME_BOLD),
    ('FONTSIZE', (0,4), (-1,5), 9),
    ('ALIGN', (3,4), (3,5), 'RIGHT'),     # Label - RIGHT
    ('ALIGN', (4,4), (4,5), 'RIGHT'),     # Amount - RIGHT
    
    # Grand total row (larger and bolder)
    ('BACKGROUND', (0,6), (-1,6), colors.HexColor('#e8f1f7')),
    ('FONTNAME', (3,6), (4,6), FONT_NAME_BOLD),
    ('FONTSIZE', (3,6), (4,6), 11),
    ('ALIGN', (3,6), (3,6), 'RIGHT'),     # Label - RIGHT
    ('ALIGN', (4,6), (4,6), 'RIGHT'),     # Amount - RIGHT
    
    # Grid and borders
    ('GRID', (0,0), (-1,3), 0.5, colors.HexColor('#c5d9e8')),
    ('GRID', (0,4), (-1,6), 0.5, colors.HexColor('#c5d9e8')),
    ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#2c5f7f')),
    ('LINEABOVE', (0,4), (-1,4), 1.5, colors.HexColor('#2c5f7f')),
    ('LINEABOVE', (0,6), (-1,6), 2, colors.HexColor('#1a3a52')),
    
    # Padding - reduced for SKU column
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (0,-1), 8),    # Product column
    ('LEFTPADDING', (1,0), (1,-1), 6),    # SKU column - less padding
    ('LEFTPADDING', (2,0), (-1,-1), 8),   # Other columns
    ('RIGHTPADDING', (0,0), (0,-1), 8),   
    ('RIGHTPADDING', (1,0), (1,-1), 4),   # SKU column - less padding
    ('RIGHTPADDING', (2,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8)
]))

story.append(bom_table)
story.append(Spacer(1, 30))


# ============= BUILD PDF =============
doc.build(story)
print("=" * 60)
print("✅ Professional NHAI_proposal.pdf generated successfully!")
print("=" * 60)
print("📄 High-quality PDF ready for review and submission")
print("💡 Key improvements:")
print("   - Removed all <b> tags (using TableStyle for formatting)")
print("   - Fixed currency display (using 'Rs.' for compatibility)")
print("   - Professional color scheme and typography")
print("   - Proper table alignment and spacing")
print("=" * 60)