document.addEventListener('DOMContentLoaded', function () {
    const preloader = document.getElementById('preloader');
    const progressBar = document.getElementById('loader-progress');

    let progress = 0;
    const interval = setInterval(function () {
        progress += Math.random() * 10;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
            document.body.classList.add('loaded');

            setTimeout(function () {
                if (preloader) {
                    preloader.style.display = 'none';
                }
            }, 500);
        }
        if (progressBar) {
            progressBar.style.width = progress + '%';
        }
    }, 200);
});
