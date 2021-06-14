'use strict';

const menuHidden = document.querySelector('#menu_hidden');
const menuButton = document.querySelector('.toggle');
const switchButtons = document.querySelectorAll('.relay_switch');
const sendLog = document.querySelector('#send_log');
const fishLens = document.querySelector('#fishlens');
const overlay = document.querySelector('.overlay');
const mainModal = document.querySelector('.main_modal');
const mainModalClose = document.querySelector('.main_modal_close');

const changeLabel = function (currentSwitch) {
    currentSwitch.previousElementSibling.innerHTML = '';
    currentSwitch.checked
        ? currentSwitch.previousElementSibling.classList.add('neon')
        : currentSwitch.previousElementSibling.classList.remove('neon');
    currentSwitch.previousElementSibling.insertAdjacentHTML(
        'afterbegin',
        `${currentSwitch
            .getAttribute('name')
            .replace(/(\d+)/g, '<sub>$1</sub>')}&nbsp;is&nbsp;switched&nbsp;${
            currentSwitch.checked ? 'on' : 'off'
        }`
    );
};

const openSendLogModal = function () {
    mainModal.classList.remove('hidden');
    overlay.classList.remove('hidden');
};

const closeSendLogModal = function () {
    mainModal.classList.add('hidden');
    overlay.classList.add('hidden');
};

mainModalClose.addEventListener('click', closeSendLogModal);
overlay.addEventListener('click', closeSendLogModal);

sendLog.addEventListener('click', function (e) {
    fetch('/email', {
        headers: {
            'content-type': 'application/json',
        },
        method: 'POST',
        body: 'lorem ipsum',
    }).then(function (response) {
        if (response.status == 200) {
            openSendLogModal();
        } else {
            alert('Something went wrong, please try again later.');
        }
    });
});

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
        // console.log('GET response text:');
        // console.log(text);
        for (const [gpio, status] of Object.entries(text)) {
            if (status) {
                const element = document.getElementById(`${gpio}`);
                element.checked = status;
                changeLabel(element);
            }
        }
    });

switchButtons.forEach(function (button) {
    button.addEventListener('click', function (e) {
        changeLabel(this);
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

fishLens.addEventListener('click', function (e) {
    fetch('/fishlens', {
        headers: {
            'content-type': 'application/json',
        },
        method: 'POST',
        body: 'lorem ipsum',
    })
        .then(function (response) {
            return response.text();
        })
        .then(function (text) {
            console.log('POST response');
            console.log(text);
        });
    // location.reload();
    // Make dynamic using AJAX in later stage
});
