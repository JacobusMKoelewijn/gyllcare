'use strict';

const mousePointer = document.querySelectorAll('.mouse_pointer');
const menuHidden = document.querySelector('#menu_hidden');
const menuButton = document.querySelector('.toggle');
const switchButtons = document.querySelectorAll('.relay_switch');
const sendLog = document.querySelector('#send_log');
const fishLens = document.querySelector('#fishlens');

const overlay = document.querySelector('.overlay');
const spinner = document.querySelector('#spinner');
const logMessage = document.querySelector('#log_message');

const mainModal = document.querySelector('.main_modal');
const mainModalClose = document.querySelector('.main_modal_close');

const alarmMode = document.querySelector('#alarm_mode');
const alarm = document.querySelector('.alarm');
const alarmBlue = document.querySelector('.alarm_blue');

// const socket = io.connect('http://127.0.0.1:5000');
const socket = io.connect('http://82.72.121.59:9000');

socket.on('connect', function () {
    socket.send('####### The browser has succesfully connected with Gyllcare...');
    console.log('####### Greetings from Gyllcare...');
    socket.on('message', function (msg) {
        console.log(msg);
    });
});

socket.on('alarm', function (msg) {
    console.log('Something triggered the alarm');
    // setTimeout()
    setInterval(function () {
        console.log('testing');
        alarmBlue.classList.remove('hidden');
    }, 1000);
    setInterval(function () {
        alarmBlue.classList.add('hidden');
    }, 2000);
});

const init = {
    retrieveStatus() {
        fetch('/status')
            .then(function (response) {
                console.log(response);
                return response.json();
            })
            .then(function (data) {
                // console.log(data);
                if (data.gpio_pin_16) alarm.classList.remove('hidden');
                for (const [gpio, status] of Object.entries(data)) {
                    if (gpio != 'gpio_pin_16' && status) {
                        const element = document.getElementById(`${gpio}`);
                        element.checked = status;
                        changeLabel(element);
                    }
                }
            });
    },

    // setButtons() {
    //     button.forEach(function (btn) {
    //         btn.classList.add('mouse_pointer');
    //     });
    // },
};

init.retrieveStatus();
// init.setButtons();

const changeLabel = function (currentSwitch) {
    // console.log(currentSwitch);
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
    spinner.classList.add('hidden');
    logMessage.classList.add('hidden');
    overlay.classList.add('hidden');
    // mainModal.classList.remove('hidden');
    // overlay.classList.remove('hidden');
};

// const closeSendLogModal = function () {
//     mainModal.classList.add('hidden');
// };

// mainModalClose.addEventListener('click', closeSendLogModal);
// overlay.addEventListener('click', closeSendLogModal);

sendLog.addEventListener('click', function (e) {
    // document.body.style.cursor = 'wait';
    // mousePointer.forEach(function (btn) {
    // btn.classList.remove('mouse_pointer');
    // });
    spinner.classList.remove('hidden');
    logMessage.classList.remove('hidden');
    overlay.classList.remove('hidden');
    fetch('/email', {
        method: 'POST',
    })
        .then(function (response) {
            console.log(response);
            console.log(response.status);

            if (response.status == 200) {
                openSendLogModal();
            } else {
                alert('Something went wrong, please try again later.');
            }
        })
        .finally(function () {
            // document.body.style.cursor = 'auto';
            // mousePointer.forEach(function (btn) {
            // btn.classList.add('mouse_pointer');
        });
});

alarmMode.addEventListener('click', function (e) {
    fetch('/alarm_mode', {
        method: 'POST',
        // body: 'request_1',
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (text) {
            console.log(text);
            if (text) {
                alarm.classList.remove('hidden');
            } else {
                alarm.classList.add('hidden');
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

switchButtons.forEach(function (button) {
    button.addEventListener('click', function (e) {
        changeLabel(this);
        console.log(this);
        fetch('/status', {
            headers: {
                'content-type': 'application/json',
            },
            method: 'POST',
            body: JSON.stringify({
                // state: this.checked,
                // gpio: this.getAttribute('id'),
                name: this.getAttribute('name'),
            }),
        })
            .then(function (response) {
                return response.text();
            })
            .then(function (text) {
                // console.log('POST response');
                // console.log(text);
            });
    });
});

fishLens.addEventListener('click', function (e) {
    fetch('/fishlens', {
        // headers: {
        //     'content-type': 'application/json',
        // },
        method: 'POST',
        // body: 'lorem ipsum',
    })
        .then(function (response) {
            return response.text();
        })
        .then(function (text) {
            // console.log('POST response');
            // console.log(text);
        });
    // location.reload();
    // Make dynamic using AJAX in later stage
});
