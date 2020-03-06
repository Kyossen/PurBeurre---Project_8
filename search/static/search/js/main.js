/* It's a small function for to spawn print of the spinner */
function connect() {
    $('#spinner').show(600);
}

/* This condition is used to adjust the readability of the errors in the registration form */
if (document.getElementsByClassName('error')) {
    $(".error").toggleClass("result_error");
}

/* This condition is used to adjust the readability of the errors in the login form */
if (document.getElementById('error_login')) {
    $("#error_login").toggleClass("result_error");
}

/* These code line use js for change the input on page top */
document.getElementById('id_food');
{
    $('#id_food').toggleClass("color_find_base");
}

/* This method is use for change the error message if email is use */
if (document.getElementsByClassName('errorlist')) {
    const user = $('.error').text();
    if (user.indexOf('User') === 9) {
        $('div div div div div div div p').first().replaceWith(
            '<p id="result_error" class="result_error">'
            + 'Cette adresse email est déjà utilisée.' + '</p>');

    }
}

/* The function below record a click of the user
She records the click that selects a non-registered
    favorite food and will indicate it to the system to create the record */
$(document).on("click", "#check_saveFood", function () {
    var product = $(this).val();
    $(this).toggleClass('orange_back');
    console.log(product);

    $.ajax({
        url: '/search/favorites.html',
        data: {
            'product': product
        },
        dataType: 'json',
        success: function (data) {
            if (data['error_food']) {
                if (!document.getElementById("result_error")) {
                    $('#error_result').append('<p id="result_error" class="result_error">' + data['error_food'] + '</p>');
                }
            }
            if (data['success_save']) {
                if (!document.getElementById("result_success")) {
                    $('#error_result').append('<p id="result_success" class="result_success">' + data['success_save'] + '</p>');

                }
            }
        }
    });
});
