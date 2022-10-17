$(function () {
    $('.add-to-cart, .add-to-cart-plus').bind('click', function () {
        const film_id = $(this).attr('id').split("-").slice(-1)[0]
        $.getJSON($SCRIPT_ROOT + '/_add_to_cart',
            { film_id: film_id },
            function (data) {});
        
        if ($(this).attr('class').split(' ')[0] == 'add-to-cart-plus') {
            const num = $('#cart-count-' + film_id).text()
            $('#cart-count-' + film_id).text(parseInt(num) + 1)
        }
        else {
            displayMessage('Añadido al carrito')
        }
        return false;
    });
});

$(function () {
    $('.remove-from-cart').bind('click', function () {
        const film_id = $(this).attr('id').split("-").slice(-1)[0]
        $.getJSON($SCRIPT_ROOT + '/_remove_from_cart',
            { film_id: film_id },
            function (data) {});
        const num = parseInt($('#cart-count-' + film_id).text())
        if(num > 0) {
            $('#cart-count-' + film_id).text(num - 1)
        }
        return false;
    });
});

$(function () {
    $('button#vaciar-carrito').bind('click', function () {
        $.getJSON($SCRIPT_ROOT + '/_vaciar_carrito',
            {},
            function (data) {});
        location.reload();
        return false;
    });
    
});

function displayMessage(message) {
    $('#message-container').show()
    $('#message').text(message)
    
    $('#message-container').animate({
        top: '50px'
    })
    setTimeout(function() {
        $('#message-container').animate({
            top: '-10px'
        })
        setTimeout(function() {
            $('#message-container').hide()
        }, 1000);
    }, 3000);
}

function updateUserCount() {

    $.getJSON($SCRIPT_ROOT + '/_return_random_number', {}, function (data) {
        $("#user-count").text('User Count: ' + data.result);
    });

    setTimeout(updateUserCount, 3000);
}

$(function () {
    updateUserCount();
});

/* $(function () {
    $('input.star').bind('click', function () {
        $.getJSON($SCRIPT_ROOT + '/_introducir_valoracion', {
            valoracion: $(this).attr('id').split("-").slice(-1)[0]
        }, function (data) {
        });
        return false;
    });
}); */