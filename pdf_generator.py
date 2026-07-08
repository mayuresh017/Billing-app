from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

from num2words import num2words

import os


def generate_pdf(
    bill_id,
    bill_no,
    customer,
    address,
    bill_date,
    discount,
    gst,
    items,
    grand_total
):

    os.makedirs("bills", exist_ok=True)

    filename = f"bills/Bill_{bill_id}.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=25,
        rightMargin=25,
        topMargin=25,
        bottomMargin=25
    )

    styles = getSampleStyleSheet()

    story=[]

    styles=getSampleStyleSheet()
    title_style=styles["Title"]
    title_style.alignment=TA_CENTER
    title_style.textColor=colors.HexColor("#1f4e79")

    # ====================================
    # COMPANY NAME
    # ====================================

    heading = styles["Heading1"]
    heading.alignment = TA_CENTER
    heading.textColor = colors.darkred

    story.append(
        Paragraph("<b>SHREE SAMARTH KRUPA</b>", heading)
    )

    sub = styles["Heading3"]
    sub.alignment = TA_CENTER

    story.append(
        Paragraph("Brick Manufacturer & Suppliers", sub)
    )

    body = styles["BodyText"]
    body.alignment = TA_CENTER

    story.append(
        Paragraph(
            "At. Injivali, Tal. Karjat, Dist. Raigad",
            body
        )
    )

    story.append(
        Paragraph(
            "Mob : 9822XXXXXX | 9870XXXXXX",
            body
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    # ====================================
    # CUSTOMER DETAILS
    # ====================================

    customer_data = [

        ["Bill No", bill_no, "Bill Date", bill_date],

        ["Customer", customer, "Address", address]

    ]

    customer_table = Table(
        customer_data,
        colWidths=[70,180,70,180]
    )

    customer_table.setStyle(TableStyle([

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#eeeeee")),
        ("BACKGROUND",(2,0),(2,-1),colors.HexColor("#eeeeee")),

        ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

        ("BOTTOMPADDING",(0,0),(-1,-1),8),

        ("VALIGN",(0,0),(-1,-1),"MIDDLE")

    ]))

    story.append(customer_table)

    story.append(Spacer(1,0.30*inch))

    # ====================================
    # ITEMS
    # ====================================

    data = [[

        "Sr",

        "Date",

        "Chalan",

        "Material",

        "Qty",

        "Rate",

        "Amount"

    ]]

    subtotal = 0

    for i,item in enumerate(items,start=1):

        subtotal += float(item["total"])

        data.append([

            str(i),

            item["itemDate"],

            item["chalan"],

            item["material"],

            str(item["qty"]),

            f"₹ {float(item['price']):,.2f}",

            f"₹ {float(item['total']):,.2f}"

        ])

    table = Table(
        data,
        colWidths=[35,70,70,150,45,60,75]
    )

    table.setStyle(TableStyle([

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,0),(-1,0),colors.darkred),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BOTTOMPADDING",(0,0),(-1,0),8),

        ("BACKGROUND",(0,1),(-1,-1),colors.white)

    ]))

    story.append(table)

    story.append(Spacer(1,0.35*inch))

    # ====================================
    # TOTALS
    # ====================================

    gst_amount = ((subtotal-discount)*gst)/100

    total_data=[

        ["Subtotal",f"₹ {subtotal:,.2f}"],

        ["Discount",f"₹ {discount:,.2f}"],

        [f"GST ({gst:.0f}%)",f"₹ {gst_amount:,.2f}"],

        ["Grand Total",f"₹ {grand_total:,.2f}"]

    ]

    total_table=Table(
        total_data,
        colWidths=[160,130],
        hAlign="RIGHT"
    )

    total_table.setStyle(TableStyle([

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),

        ("BACKGROUND",(0,3),(-1,3),colors.HexColor("#FFF2CC")),

        ("FONTNAME",(0,3),(-1,3),"Helvetica-Bold"),

        ("BOTTOMPADDING",(0,0),(-1,-1),8)

    ]))

    story.append(total_table)

    story.append(Spacer(1,0.35*inch))

    # ====================================
    # AMOUNT IN WORDS
    # ====================================

    try:

        words = num2words(
            int(round(grand_total)),
            lang="en_IN"
        ).title()

    except:

        words = num2words(
            int(round(grand_total))
        ).title()

    story.append(

        Paragraph(

            f"<b>Amount In Words :</b> {words} Rupees Only",

            styles["Normal"]

        )

    )

    story.append(Spacer(1,0.60*inch))

    # ====================================
    # SIGNATURE
    # ====================================

    sign = Table(
        [["Authorized Signature"]],
        colWidths=[180],
        hAlign="RIGHT"
    )

    sign.setStyle(TableStyle([

        ("LINEABOVE",(0,0),(-1,0),1,colors.black),

        ("TOPPADDING",(0,0),(-1,-1),10),

        ("ALIGN",(0,0),(-1,-1),"CENTER")

    ]))

    story.append(sign)

    story.append(Spacer(1,0.40*inch))

    # ====================================
    # FOOTER
    # ====================================

    footer = styles["Heading3"]

    footer.alignment = TA_CENTER

    footer.textColor = colors.darkgreen

    story.append(

        Paragraph(

            "Thank You! Visit Again",

            footer

        )

    )

    doc.build(story)

    return filename