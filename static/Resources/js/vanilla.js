'use strict';

const menuBar = document.getElementById('menu_bar');

document.getElementById('toggle').addEventListener('click', function (e) {
    e.preventDefault();

    if (!menuBar.classList.contains('active')) {
        menuBar.classList.add('active');
        menuBar.style.height = 'auto';

        const height = menuBar.clientHeight + 'px';

        menuBar.style.height = '0px';
        setTimeout(function () {
            menuBar.style.height = height;
        }, 0);
    } else {
        menuBar.style.height = '0px';

        menuBar.addEventListener(
            'transitionend',
            function () {
                menuBar.classList.remove('active');
            },
            {
                once: true,
            }
        );
    }
});
