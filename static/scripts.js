$(function() {
    $('#btnSignUp').click(function() {
 
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(xhr, ajaxOptions, thrownError){
                console.log(xhr.status);
                console.log(xhr.responseText);
                console.log(thrownError);
            }
        });
    });
});