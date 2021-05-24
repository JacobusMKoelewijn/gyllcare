$(document).ready(function() {
    
    $.get('/status', function(data) {
        if (data.gpio_14_status == "on") {
            $('#gpio_pin_14').prop('checked', true).change()
        }
        if (data.gpio_15_status == "on") {
            $('#gpio_pin_15').prop('checked', true).change()
        }
        if (data.gpio_18_status == "on") {
            $('#gpio_pin_18').prop('checked', true).change()
        }
        if (data.gpio_23_status == "on") {
            $('#gpio_pin_23').prop('checked', true).change()
        }
    });
    
    $('.relay_switch').click(function() {
        $.post('/status', { state: $(this).prop('checked'), gpio: $(this).attr("id"), name: $(this).attr("name") });
        setTimeout(Reload, 3000);
    });

    $('.log_file').click(function() {
        $.post('/email', { key:"confirmed" });
    });

    function Reload() {
        location.reload()
    }

});