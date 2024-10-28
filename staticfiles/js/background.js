document.addEventListener('DOMContentLoaded', function() {
    const backgrounds = [
        '/static/videos/background.mp4',
        '/static/videos/background2.mp4',
        '/static/videos/background3.mp4',
        '/static/videos/background4.mp4'
    ];
    
    let currentBackgroundIndex = parseInt(localStorage.getItem('currentBackgroundIndex')) || 0;

    function changeBackground(direction) {
        currentBackgroundIndex = (currentBackgroundIndex + direction + backgrounds.length) % backgrounds.length;
        const video = document.getElementById('myVideo');
        video.src = backgrounds[currentBackgroundIndex];
        video.load();
        localStorage.setItem('currentBackgroundIndex', currentBackgroundIndex);
    }

    document.getElementById('prevBackground').addEventListener('click', () => changeBackground(-1));
    document.getElementById('nextBackground').addEventListener('click', () => changeBackground(1));

    const video = document.getElementById('myVideo');
    video.src = backgrounds[currentBackgroundIndex];
    video.load();

    video.addEventListener('loadedmetadata', function() {
        video.play();
    });
});
