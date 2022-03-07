'use strict';

// FOR MENUS
const menuHidden = document.querySelector('#hidden_menu_panel');
const menuButton = document.querySelector('.toggle');

// FOR BUTTONS
const switchButtons = document.querySelectorAll('.relay_switch');
const scheduleButtons = document.querySelectorAll('.schedule_switch');
const cleanAq = document.querySelector('#clean_aq');
const sendLog = document.querySelector('#send_log');
const alarmMode = document.querySelector('#alarm_mode');
const yesClean = document.querySelector('#yes_clean');
const noClean = document.querySelector('#no_clean');
const arrowLeft = document.querySelector('.js--arrow_btn_left');
const arrowRight = document.querySelector('.js--arrow_btn_right');
const fishLensPhoto = document.querySelector('#fishlens_photo');

// FOR OVERLAYS
const overlayLog = document.querySelector('.overlay_log');
const overlayClean = document.querySelector('.overlay_clean');
const overlayLens = document.querySelector('.overlay_lens');
const fishLens = document.querySelector('#fishlens');
const spinner = document.querySelector('#spinner');
const logMessage = document.querySelector('#log_message');
const spinner_2 = document.querySelector('#spinner_2');
const logMessage_2 = document.querySelector('#log_message_2');

// FOR LEDS
const alarmRed = document.querySelector('.alarm_red');
const alarmBlue = document.querySelector('.alarm_blue');

// FOR SLIDER
const scheduleSlider = document.querySelector('.js--schedule_slider');
const scheduleSlides = document.querySelectorAll('.js--schedule_slide');


// Initiate Socket //////////////

const socket = io.connect('http://82.72.121.59:9000');

socket.on('connect', function () {
    socket.send(
        '####### The browser has succesfully connected with Gyllcare...'
    );
    socket.on('message', function (msg) {
        console.log(msg);
    });
});

socket.on('alarm', function (msg) {
    alarmBlue.classList.remove('hidden');
});


// Initiate App /////////////////

const init = {
    retrieveStatus() {
        fetch('/status')
            .then(function (response) {
                console.log(response);
                return response.json();
            })
            .then(function (data) {
                console.log(data);
                if (data.gpio_pin_16) alarmRed.classList.remove('hidden');
                if (data.gpio_pin_20) alarmBlue.classList.remove('hidden');
                for (const [gpio, status] of Object.entries(data)) {
                    if (
                        gpio != 'gpio_pin_16' &&
                        gpio != 'gpio_pin_20' &&
                        status
                    ) {
                        const element = document.getElementById(`${gpio}`);
                        element.checked = status;
                        changeLabel(element);
                    }
                }
            });
    },
};

init.retrieveStatus();


// Label control ////////////////

const changeLabel = function (currentSwitch) {
    if (currentSwitch.id[0] == 'g') {
        currentSwitch.previousElementSibling.innerHTML = '';
        currentSwitch.checked
            ? currentSwitch.previousElementSibling.classList.add('neon')
            : currentSwitch.previousElementSibling.classList.remove('neon');
        currentSwitch.previousElementSibling.insertAdjacentHTML(
            'afterbegin',
            `${currentSwitch
                .getAttribute('name')
                .replace(
                    /(\d+)/g,
                    '<sub>$1</sub>'
                )}&nbsp;is&nbsp;switched&nbsp;${
                currentSwitch.checked ? 'on' : 'off'
            }`
        );
    } else {
        const [select_on, select_off] =
            currentSwitch.parentElement.parentElement.nextElementSibling.querySelectorAll(
                'select'
            );
        console.log(select_on);
        currentSwitch.checked
            ? (select_on.removeAttribute('disabled'),
              (select_on.style.backgroundColor = '#2d3436'),
              select_off.removeAttribute('disabled'),
              (select_off.style.backgroundColor = '#2d3436'))
            : (select_on.setAttribute('disabled', true),
              (select_on.style.backgroundColor = '#55efc4'),
              select_off.setAttribute('disabled', true),
              (select_off.style.backgroundColor = '#55efc4'));
    }
};

const removeSpinnerMenuPanel = function () {
    spinner.classList.add('hidden');
    logMessage.classList.add('hidden');
    overlayLog.classList.add('hidden');
};

const removeSpinnerPhotoPanel = function () {
    spinner_2.classList.add('hidden');
    logMessage_2.classList.add('hidden');
    overlayLens.classList.add('hidden');
};


// Clean Aquarium ///////////////

cleanAq.addEventListener('click', function (e) {
    overlayClean.classList.remove('hidden');
});

yesClean.addEventListener('click', function (e) {
    fetch('/shutdown', {
        method: 'POST',
    });
});

noClean.addEventListener('click', function (e) {
    overlayClean.classList.add('hidden');
});


// Send log /////////////////////

sendLog.addEventListener('click', function (e) {
    spinner.classList.remove('hidden');
    logMessage.classList.remove('hidden');
    overlayLog.classList.remove('hidden');
    fetch('/email', {
        method: 'POST',
    })
        .then(function (response) {
            if (response.status == 200) {
                removeSpinnerMenuPanel();
            } else {
                alert('Something went wrong, please check the logs.');
            }
        })
        .finally(function () {
            console.log('log send.');
        });
});


// Toggle alarm /////////////////

alarmMode.addEventListener('click', function (e) {
    fetch('/alarm_mode', {
        method: 'POST',
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (text) {
            console.log(text);
            if (text) {
                alarmRed.classList.remove('hidden');
            } else {
                alarmRed.classList.add('hidden');
                alarmBlue.classList.add('hidden');
            }
        });
});


// Hidden menu slider ///////////

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
        }, 0);
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


// Switch buttons ///////////////

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
                name: this.getAttribute('name'),
            }),
        })
            .then(function (response) {
                return response.text();
            })
            .then(function (text) {});
    });
});


// Schedule buttons /////////////

scheduleButtons.forEach(function (button) {
    button.addEventListener('click', function (e) {
        changeLabel(this);
        fetch('/status', {
            headers: {
                'content-type': 'application/json',
            },
            method: 'POST',
            body: JSON.stringify({
                name: this.getAttribute('name'),
            }),
        })
            .then(function (response) {
                return response.text();
            })
            .then(function (text) {});
    });
});


// Capture image ////////////////

fishLens.addEventListener('click', function (e) {
    spinner_2.classList.remove('hidden');
    logMessage_2.classList.remove('hidden');
    overlayLens.classList.remove('hidden');
    fetch('/fishlens', {
        method: 'POST',
    })
        .then(function (response) {
            if (response.status == 200) {
                console.log('Message received');
                const timestamp = new Date().getTime();
                fishLensPhoto.src =
                    '/static/Resources/img/fishlens.jpg?t=' + timestamp;
            } else {
                alert('Something went wrong, please check the logs.');
            }
        })
        .finally(function () {
            removeSpinnerPhotoPanel();
        });
});


// Schedule slider //////////////

let curSlide = 0;
const maxSlide = scheduleSlides.length;

const goToSlide = function (slide) {
    scheduleSlides.forEach(
        (s, i) => (s.style.transform = `translateX(${110 * (i - slide)}%)`)
    );
};

const nextSlide = function () {
    if (curSlide === maxSlide - 1) {
        curSlide = 0;
    } else {
        curSlide++;
    }
    goToSlide(curSlide);
};

const prevSlide = function () {
    if (curSlide === 0) {
        curSlide = maxSlide - 1;
    } else {
        curSlide--;
    }
    goToSlide(curSlide);
};

arrowRight.addEventListener('click', nextSlide);
arrowLeft.addEventListener('click', prevSlide);

goToSlide(0);
