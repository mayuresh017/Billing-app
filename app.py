from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from pdf_generator import generate_pdf
import sqlite3
import os
import database

app = Flask(__name__)

DATABASE = "database/billing.db"


# ==========================
# DATABASE CONNECTION
# ==========================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================
# HOME
# ==========================

@app.route("/")
def home():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(id) FROM bills")
    last_id = cursor.fetchone()[0]

    conn.close()

    if last_id:
        bill_no = f"INV-{last_id+1:04d}"
    else:
        bill_no = "INV-0001"

    return render_template(
        "index.html",
        bill_no=bill_no
    )


# ==========================
# SAVE BILL
# ==========================

@app.route("/save_bill", methods=["POST"])
def save_bill():

    try:

        data = request.get_json()

        customer = data["customer"]
        address = data["address"]
        bill_no = data["billNo"]
        bill_date = data["billDate"]

        discount = float(data["discount"])
        gst = float(data["gst"])
        grand_total = float(data["grandTotal"])

        items = data["items"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO bills(

            bill_no,
            customer_name,
            customer_address,
            bill_date,
            discount,
            gst,
            grand_total

        )

        VALUES(?,?,?,?,?,?,?)

        """,(

            bill_no,
            customer,
            address,
            bill_date,
            discount,
            gst,
            grand_total

        ))

        bill_id = cursor.lastrowid

        for item in items:

            cursor.execute("""

            INSERT INTO bill_items(

                bill_id,
                item_date,
                chalan_no,
                material,
                quantity,
                price,
                total

            )

            VALUES(?,?,?,?,?,?,?)

            """,(

                bill_id,
                item["itemDate"],
                item["chalan"],
                item["material"],
                item["qty"],
                item["price"],
                item["total"]

            ))

        conn.commit()
        conn.close()

        generate_pdf(

            bill_id=bill_id,
            bill_no=bill_no,
            customer=customer,
            address=address,
            bill_date=bill_date,
            discount=discount,
            gst=gst,
            items=items,
            grand_total=grand_total

        )

        return jsonify({

            "success":True,
            "message":"Bill Saved Successfully",
            "bill_id":bill_id,
            "pdf":f"/download_pdf/{bill_id}"

        })

    except Exception as e:

        return jsonify({

            "success":False,
            "message":str(e)

        })


# ==========================
# DOWNLOAD PDF
# ==========================

@app.route("/download_pdf/<int:bill_id>")
def download_pdf(bill_id):

    pdf = f"bills/Bill_{bill_id}.pdf"

    if os.path.exists(pdf):
        return send_file(pdf, as_attachment=True)

    return "PDF Not Found",404


# ==========================
# BILL HISTORY
# ==========================

@app.route("/history")
def history():

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM bills

    ORDER BY id DESC

    """)

    bills = cursor.fetchall()

    conn.close()

    return render_template(

        "history.html",

        bills=bills

    )


# ==========================
# BILL DETAILS
# ==========================

@app.route("/bill/<int:bill_id>")
def bill_details(bill_id):

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM bills WHERE id=?",

        (bill_id,)

    )

    bill = cursor.fetchone()

    cursor.execute(

        "SELECT * FROM bill_items WHERE bill_id=?",

        (bill_id,)

    )

    items = cursor.fetchall()

    conn.close()

    return render_template(

        "bill_details.html",

        bill=bill,

        items=items

    )


# ==========================
# DELETE BILL
# ==========================

@app.route("/delete_bill/<int:bill_id>")
def delete_bill(bill_id):

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM bill_items WHERE bill_id=?",

        (bill_id,)

    )

    cursor.execute(

        "DELETE FROM bills WHERE id=?",

        (bill_id,)

    )

    conn.commit()

    conn.close()

    pdf = f"bills/Bill_{bill_id}.pdf"

    if os.path.exists(pdf):
        os.remove(pdf)

    return jsonify({

        "success":True,

        "message":"Bill Deleted Successfully"

    })


# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM bills")
    total_bills = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(grand_total) FROM bills")
    total_sales = cursor.fetchone()[0]

    if total_sales is None:
        total_sales = 0

    cursor.execute("""

    SELECT COUNT(DISTINCT customer_name)

    FROM bills

    """)

    customers = cursor.fetchone()[0]

    conn.close()

    return render_template(

        "dashboard.html",

        total_bills=total_bills,

        total_sales=total_sales,

        customers=customers

    )


# ==========================
# SEARCH BILL
# ==========================

@app.route("/search")
def search():

    keyword = request.args.get("q","")

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM bills

    WHERE

    customer_name LIKE ?

    OR bill_no LIKE ?

    ORDER BY id DESC

    """,

    (

        f"%{keyword}%",

        f"%{keyword}%"

    ))

    bills = cursor.fetchall()

    conn.close()

    return render_template(

        "history.html",

        bills=bills

    )


# ==========================
# RUN
# ==========================

if __name__=="__main__":

    app.run(debug=True)