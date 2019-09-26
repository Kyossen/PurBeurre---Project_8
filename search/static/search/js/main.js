/* It's a small function for to spawn print of the spinner */

function connect() {
    $('#spinner').show( 600 );
}


/* 
The function below record a click of the user
She records the click that selects a non-registered favorite food and will indicate it to the system to create the record
The advantage of going through this function is to stay on the page and to be able to record other foods simultaneously thanks to Ajax 
*/

$( document ).ready(function() {
    $(check_saveFood).click(function() {
        var product = $( this ).val();
        console.log(product)
        console.log('True');

          $.ajax({
            url: '/search/favorites.html',
            data: {
              'product': product
            },
            dataType: 'json',
            success: function (data) {
              if (data.error_food) {
                $('#error_result').append('<p>' + data.error_food + '</p>');
              }
              if (data.success_save) {
                $('#error_result').append('<p>' + data.success_save + '</p>');
              }
            }
          });
      })
});

