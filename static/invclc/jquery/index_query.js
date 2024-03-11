$(document).ready(function(){
    $("#id_invoice_amount, #id_payment_amount").on("input", function () {
      var invoice_amount = parseFloat($("#id_invoice_amount").val()) || 0;
      var payment_amount = parseFloat($("#id_payment_amount").val()) || 0;
      $("#id_balance_amount").val(invoice_amount - payment_amount);
    });
});
