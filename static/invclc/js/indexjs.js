// function editbtn(){
//     alert("I am an alert box!");
//   }

//   function editInvoice(invoiceId) {
//           // You can implement an AJAX request to fetch the invoice data
//           // and populate the form fields for editing
//           // For simplicity, let's assume you have a URL for fetching invoice data
//           var eidtbtnurl = "{% url 'update' %}?pk=" + invoiceId;

//           // Assuming you are using jQuery for AJAX
//           $.get(eidtbtnurl, function (data) {
//               // Populate the form fields with the fetched data
//               $("#phname_id_").val(data.pharmacy_name);
//               $("#ivncno_id_").val(data.invoice_number);
//               $("#ivncdt_id_").val(data.invoice_date);
//               $("#invcamt_id_").val(data.invoice_amount);
//               $("#blnc_id_").val(data.balance_amount);
//               $("#due_id_").val(data.payment_amount);

//               // Change the form action to handle editing
//               $("form").attr("action", "{% url 'edit' %}?id=" + invoiceId);
//           });
//       }


// document.addEventListener("DOMContentLoaded", (event) => {
//   let tablinks = document.querySelectorAll(".tablinks");
//   let tabcontent = document.querySelectorAll(".tabcontent");

//   for (let i = 0; i < tabcontent.length; i++) {
//     tabcontent[i].style.display = "none";
//   }

//   tabcontent[0].style.display = "block";

//   for (let i = 0; i < tablinks.length; i++) {
//     tablinks[i].addEventListener("click", function () {
//       let tabName = this.getAttribute("data-tabs");

//       for (let i = 0; i < tabcontent.length; i++) {
//         tabcontent[i].style.display = "none";
//       }

//       if (tabName === "current_updates") {
//         document.getElementById("current").style.display = "block";
//       } else if (tabName === "payment_details") {
//         document.getElementById("payment").style.display = "block";
//       }
//     });
//   }
// });

