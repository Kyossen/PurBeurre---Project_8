function connect() {
/* Disable the button to ensure that the query is not repeated in a loop */
   $("#button_connect").attr("disabled", true);
   $('#loading').append('<p> Connexion en cours... </p>');
   $('#spinner').toggle();
    if (document.getElementById("loading")) {
            setTimeout(connect, 4000);
            $("#button_connect").attr("disabled", false);
          }
}
