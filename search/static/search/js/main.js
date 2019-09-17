$( document ).ready(function() {
        console.log( "document loaded" );
        $( "#target" ).click(function() {
            console.log( "Handler for .click() called." );
            /* Le bouton du haut -> id : find_top
            Celui du millieux -> id : find_mid*/
        });
});

function connect() {
    // $("#button_connect").attr("disabled", true);
    $('#spinner').show( 600 );
    $('#spinner').hide(10250)
    // setTimeout(button_activate, 10000);
}

function button_activate() {
    $("#button_connect").attr("disabled", false);
}
/*
    if (document.getElementById('id_email')) {
        $(id_email).change(function () {
             var username = $('#id_email').val();
             $(id_wordpass).change(function () {
                var password = $(id_wordpass).val();

                $.ajax({
                    url: 'ajax/validate_connect/',
                    data: {
                    'username': username,
                    'password': password
                    },
                    dataType: 'json',
                    success: function (data) {
                    if (data.is_taken) {
                    console.log(data)

                        }
                    }
      });
    });
    });
*/
