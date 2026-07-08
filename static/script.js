let items = [];
let serial = 1;
let grandTotal = 0;

// Generate Bill Number
document.getElementById("billNo").value =
`INV-${new Date().getFullYear()}${String(new Date().getMonth()+1).padStart(2,"0")}${String(new Date().getDate()).padStart(2,"0")}-${Math.floor(Math.random()*9000+1000)}`;

// Set Today's Date
document.getElementById("billDate").value =
new Date().toISOString().split("T")[0];

document.getElementById("itemDate").value =
new Date().toISOString().split("T")[0];

const addBtn = document.getElementById("addBtn");
const clearBtn = document.getElementById("clearBtn");
const saveBtn = document.getElementById("saveBtn");

const billTable = document.getElementById("billTable");

function numberToWords(num){

    return num.toLocaleString("en-IN") + " Rupees Only";

}

function updateTotals(){

    let subtotal = 0;

    items.forEach(item=>{

        subtotal += item.total;

    });

    let discount = Number(document.getElementById("discount").value || 0);

    let gstPercent = Number(document.getElementById("gst").value || 0);

    let amountAfterDiscount = subtotal - discount;

    if(amountAfterDiscount < 0)
        amountAfterDiscount = 0;

    let gstAmount = amountAfterDiscount * gstPercent / 100;

    grandTotal = amountAfterDiscount + gstAmount;

    document.getElementById("subtotal").innerText = subtotal.toFixed(2);

    document.getElementById("discountValue").innerText = discount.toFixed(2);

    document.getElementById("gstValue").innerText = gstAmount.toFixed(2);

    document.getElementById("grandTotal").innerText = grandTotal.toFixed(2);

    document.getElementById("amountWords").value =
    numberToWords(grandTotal.toFixed(2));

}

// Add Item
addBtn.addEventListener("click",function(){

    let itemDate = document.getElementById("itemDate").value;

    let chalan = document.getElementById("chalan").value.trim();

    let material = document.getElementById("material").value.trim();

    let qty = Number(document.getElementById("qty").value);

    let price = Number(document.getElementById("price").value);

    if(material==="" || qty<=0 || price<=0){

        alert("Please enter all item details.");

        return;

    }

    let total = qty * price;

    const item={

        itemDate,

        chalan,

        material,

        qty,

        price,

        total

    };

    items.push(item);

    let row=document.createElement("tr");

    row.innerHTML=`

        <td>${serial++}</td>

        <td>${itemDate}</td>

        <td>${chalan}</td>

        <td>${material}</td>

        <td>${qty}</td>

        <td>₹${price}</td>

        <td>₹${total.toFixed(2)}</td>

        <td>

            <button class="deleteBtn">

                Delete

            </button>

        </td>

    `;

    billTable.appendChild(row);

    updateTotals();

    row.querySelector(".deleteBtn").addEventListener("click",function(){

        const index = items.indexOf(item);

        if(index>-1){

            items.splice(index,1);

        }

        row.remove();

        updateTotals();

    });

    document.getElementById("chalan").value="";

    document.getElementById("material").value="";

    document.getElementById("qty").value="";

    document.getElementById("price").value="";

});

// Discount
document.getElementById("discount")
.addEventListener("input",updateTotals);

// GST
document.getElementById("gst")
.addEventListener("change",updateTotals);

// Clear
clearBtn.addEventListener("click",function(){

    billTable.innerHTML="";

    items=[];

    serial=1;

    document.getElementById("customer").value="";

    document.getElementById("address").value="";

    document.getElementById("discount").value=0;

    document.getElementById("gst").value=0;

    document.getElementById("billNo").value =
    `INV-${new Date().getFullYear()}${String(new Date().getMonth()+1).padStart(2,"0")}${String(new Date().getDate()).padStart(2,"0")}-${Math.floor(Math.random()*9000+1000)}`;

    updateTotals();

});

// Save Bill
saveBtn.addEventListener("click",function(){

    let customer =
    document.getElementById("customer").value.trim();

    let address =
    document.getElementById("address").value.trim();

    let billNo =
    document.getElementById("billNo").value;

    let billDate =
    document.getElementById("billDate").value;

    if(customer==="" || address===""){

        alert("Enter customer details.");

        return;

    }

    if(items.length===0){

        alert("Please add at least one item.");

        return;

    }

    fetch("/save_bill",{

        method:"POST",

        headers:{

            "Content-Type":"application/json"

        },

        body:JSON.stringify({

            customer,

            address,

            billNo,

            billDate,

            discount:Number(document.getElementById("discount").value),

            gst:Number(document.getElementById("gst").value),

            grandTotal,

            items

        })

    })

    .then(response=>response.json())

    .then(data=>{

        alert(data.message);

        window.location.href=data.pdf;

        clearBtn.click();

    })

    .catch(error=>{

        console.log(error);

        alert("Error Saving Bill");

    });

});

updateTotals();