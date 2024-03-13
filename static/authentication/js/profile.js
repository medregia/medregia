$(document).ready(function() {
    $('#id_state').select2({
        placeholder: "Select a State",
        allowClear: true
    });
});

 $(document).ready(function() {
    $('#id_district').select2({
        placeholder: "Select a district",
        allowClear: true
    });
});

$(function() {
    $( "#button" ).click(function() {
      $( "#button" ).addClass( "onclic", 250, validate);
    });

    function validate() {
      setTimeout(function() {
        $( "#button" ).removeClass( "onclic" );
        $( "#button" ).addClass( "validate", 450, callback );
      }, 2250 );
    }
      function callback() {
        setTimeout(function() {
          $( "#button" ).removeClass( "validate" );
        }, 1250 );
      }
});