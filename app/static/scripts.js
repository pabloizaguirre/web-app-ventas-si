
/* Carrito */

$(function () {
    $('.add-to-cart-plus').bind('click', function () {
        const prod_id = $(this).attr('id').split("-").slice(-1)[0]
        $.getJSON($SCRIPT_ROOT + '/_add_to_cart',
            { prod_id: prod_id },
            function (data) {location.reload()});
        
        return false;
    });
});

$(function () {
    $('.add-to-cart').bind('click', function () {
        const prod_id = $('#descripcion-productos option:selected').val()
        $.getJSON($SCRIPT_ROOT + '/_add_to_cart',
            { prod_id: prod_id },
            function (data) { });
            
        displayMessage('Añadido al carrito')
        return false;
    });
});

$(function () {
    $('.remove-from-cart').bind('click', function () {
        const prod_id = $(this).attr('id').split("-").slice(-1)[0]
        $.getJSON($SCRIPT_ROOT + '/_remove_from_cart',
            { prod_id: prod_id },
            function (data) { 
                location.reload();
            });
        
        return false;
    });
});

$(function () {
    $('button.vaciar-carrito').bind('click', function () {
        $.getJSON($SCRIPT_ROOT + '/_vaciar_carrito',
            {},
            function (data) {location.reload();});
        return false;
    });

});

/* Finalizar compra */

$(function () {
    $('button#finalizar-compra').bind('click', function () {
        $.getJSON($SCRIPT_ROOT + '/_finalizar_compra',
            {},
            function (data) {
                if (data.usuario == 0) {
                    window.location.href = data.url
                } else if (data.suficiente_saldo == 0) {
                    displayMessage("No tienes suficiente saldo", error = true)
                } else {
                    $.getJSON($SCRIPT_ROOT + '/_vaciar_carrito',
                        {},
                        function (data) { }
                    );
                    window.location.href = data.url
                }
            });
        return false;
    });

});

function actualizarSaldo() {
    $.getJSON($SCRIPT_ROOT + '/_get_saldo', {}, function (data) {
        $("#saldo-side").text('Saldo: ' + data.result + "€");
    });
}

function displayMessage(message, error = false) {
    if (error) {
        $('#message').css("background-color", "rgb(255, 160, 160)");
    }
    $('#message-container').show()
    $('#message').text(message)

    $('#message-container').animate({
        top: '60px'
    })
    setTimeout(function () {
        $('#message-container').animate({
            top: '-10px'
        })
        setTimeout(function () {
            $('#message-container').hide()
            if (error) {
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

/* Enviar valoracion estrellas */

$(function () {
    $('input.star').on('change', function () {
        valoracion = $(this).attr('id').split("-").slice(-1)[0]
        $.getJSON($SCRIPT_ROOT + '/_introducir_valoracion', {
            valoracion: valoracion,
            film_id: window.location.pathname.split('/').slice(-1)[0]
        }, function (data) {
            if (data.usuario == 0) {
                displayMessage('Es necesario iniciar sesión para valorar películas', error = true);
                return false;
            }
            if (data.valorada) {
                displayMessage('Ya has valorado esta pelicula', error = true);
                return false;
            }
        });
        message = 'Introducida valoracion de ' + valoracion + ' estrella'
        if (valoracion > '1') {
            message += 's'
        }
        displayMessage(message)
        return false;
    });
});


/* Comprobar clave */

function muestra_seguridad_clave(clave, formulario) {
    seguridad = seguridad_clave(clave);
    formulario.seguridad.value = seguridad;
    if(seguridad=='Débil'){
        $("#medidor-fortaleza").css('color', 'rgb(233, 60, 70)')
    } else if(seguridad=='Normal'){
        $("#medidor-fortaleza").css('color', 'rgb(240	165	59	)')
    } else {
        $("#medidor-fortaleza").css('color', 'rgb(111, 201, 90)')
    }
}

function comprobarClave() {
    clave1 = document.forms["formu"]["clave"].value;
    clave2 = document.forms["formu"]["clave-confirmar"].value;

    if (clave1 != clave2) {
        displayMessage('Las dos claves son distintas', error = true);
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
        retorno = "Débil";
    } else if (seguridad > 100 && seguridad <= 240) {
        retorno = "Normal";
    } else {
        retorno = "Fuerte";
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