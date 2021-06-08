'use strict';

const menuHidden = document.querySelector('#menu_hidden');
const menuButton = document.querySelector('.toggle');
const switchButtons = document.querySelectorAll('.relay_switch');

console.log(switchButtons);

menuButton.addEventListener('click', function (e) {
    e.preventDefault();

    if (!menuHidden.classList.contains('active')) {
        menuHidden.classList.add('active');
        menuHidden.style.height = 'auto';
        const height = menuHidden.clientHeight + 'px';
        menuHidden.style.height = '0px';

        setTimeout(function () {
            menuHidden.style.height = height;
            menuButton.setAttribute('name', 'close-outline');
        }, 0); // A blank setTimeout moves the code within to the end of the pipeline after rendering.
    } else {
        menuHidden.style.height = '0px';
        menuButton.setAttribute('name', 'menu-outline');

        menuHidden.addEventListener(
            'transitionend',
            () => menuHidden.classList.remove('active'),
            { once: true }
        );
    }
});

fetch('/status')
    .then(function (response) {
        return response.json(); // Goes to Python probably
    })
    .then(function (text) {
        console.log('GET response text:');
        console.log(text);
        // console.log(text.gpio_pin_14);
        document.getElementById('gpio_pin_14').checked = text.gpio_pin_14;
        document.getElementById('gpio_pin_15').checked = text.gpio_pin_15;
        document.getElementById('gpio_pin_18').checked = text.gpio_pin_18;
        document.getElementById('gpio_pin_23').checked = text.gpio_pin_23;
    });

switchButtons.forEach(function (button) {
    button.addEventListener('click', function (e) {
        // e.preventDefault();

        fetch('/status', {
            headers: {
                'content-type': 'application/json',
            },
            method: 'POST',
            body: JSON.stringify({
                state: this.checked,
                gpio: this.getAttribute('id'),
                name: this.getAttribute('name'),
            }),
        })
            .then(function (response) {
                return response.text();
            })
            .then(function (text) {
                console.log('POST response');
                console.log(text);
            });
    });
});
