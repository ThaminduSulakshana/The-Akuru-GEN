document.addEventListener('DOMContentLoaded', function () {
    const audio = document.getElementById('audio');
    const playButton = document.getElementById('play-button');
    const pauseButton = document.getElementById('pause-button');
    const progressBar = document.getElementById('progress-bar');
    const currentTimeDisplay = document.getElementById('current-time');
    const totalTimeDisplay = document.getElementById('total-time');

            // Event listener for loaded metadata of audio
            audio.addEventListener('loadedmetadata', function () {
                const totalTime = formatTime(audio.duration);
                totalTimeDisplay.textContent = totalTime;
            });

            // Event listener for play button click
            playButton.addEventListener('click', function () {
                audio.play();
            });

            // Event listener for pause button click
            pauseButton.addEventListener('click', function () {
                audio.pause();
            });

            // Event listener for time update of audio
            audio.addEventListener('timeupdate', function () {
                const currentTime = formatTime(audio.currentTime);
                currentTimeDisplay.textContent = currentTime;

                const progress = (audio.currentTime / audio.duration) * 100;
                progressBar.style.width = progress + '%';
            });

            // Function to format time
            function formatTime(seconds) {
                const minutes = Math.floor(seconds / 60);
                const remainingSeconds = Math.floor(seconds % 60);
                return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
            }
    });
