$(function () {
    $('.add-to-cart, .add-to-cart-plus').bind('click', function () {
        const film_id = $(this).attr('id').split("-").slice(-1)[0]
        $.getJSON($SCRIPT_ROOT + '/_add_to_cart',
            { film_id: film_id },
            function (data) { });

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
            function (data) { });
        const num = parseInt($('#cart-count-' + film_id).text())
        if (num > 0) {
            $('#cart-count-' + film_id).text(num - 1)
        }
        return false;
    });
});

$(function () {
    $('button#vaciar-carrito').bind('click', function () {
        $.getJSON($SCRIPT_ROOT + '/_vaciar_carrito',
            {},
            function (data) { });
        location.reload();
        return false;
    });

});

function displayMessage(message, error=false) {
    if(error){
        $('#message').css("background-color", "rgb(255, 160, 160)");
    }
    $('#message-container').show()
    $('#message').text(message)

    $('#message-container').animate({
        top: '50px'
    })
    setTimeout(function () {
        $('#message-container').animate({
            top: '-10px'
        })
        setTimeout(function () {
            $('#message-container').hide()
            if(error) {
                $('#message').css("background-color", "rgb(255, 255, 255)");
            }
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


/* Comprobar clave */

function muestra_seguridad_clave(clave, formulario) {
    seguridad = seguridad_clave(clave);
    formulario.seguridad.value = seguridad;
}

function comprobarClave() {
    clave1 = document.forms["formu"]["clave"].value;
    clave2 = document.forms["formu"]["clave-confirmar"].value;

    if (clave1 != clave2) {
        displayMessage('Las dos claves son distintas', error=true);
        return false;
    }
}

function seguridad_clave(clave) {
    seguridad = 0;
    if (clave.length != 0) {
        if (clave.length >= 4 && clave.length <= 5) {
            seguridad += 10;
        } else if (clave.length >= 6 && clave.length <= 8) {
            seguridad += 30;
        } else if (clave.length > 8) {
            seguridad += 40;
        }
    }

    numeros = "0123456789";

    for (i = 0; i < clave.length; i++) {
        letra = clave.charAt(i);
        if (numeros.indexOf(letra, 0) != -1) {
            seguridad += 20;
        }
        if (letra === letra.toUpperCase()) {
            seguridad += 20;
        }
        if (letra === letra.toLowerCase()) {
            seguridad += 10;
        }
    }

    especiales = "@#$%&/()="

    for (i = 0; i < clave.length; i++) {
        letra = clave.charAt(i);
        if (especiales.indexOf(letra, 0) != -1) {
            seguridad += 10;
        }
    }

    if (seguridad <= 100) {
        retorno = "debil";
    } else if (seguridad > 100 && seguridad <= 240) {
        retorno = "normal";
    } else {
        retorno = "fuerte";
    }

    return retorno;
}		

/* Set index movies colors */

window.onload = function setRandomColors() {
    const elements = document.getElementsByClassName('movie-container')
    for (const element of elements) {
        const num = parseFloat(element.id)
        element.style.backgroundColor = "hsl(" + 360 * ((num * 13) % 15) / 15 + ',' +
            (25 + 70 * ((num * 13) % 15) / 15) + '%,' +
            (85 + 10 * ((num * 13) % 15) / 15) + '%)'
    }
}