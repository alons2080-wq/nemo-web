document.addEventListener('DOMContentLoaded', () => {
    const themeBtn = document.getElementById('theme-switch');
    const body = document.body;
    const icon = themeBtn.querySelector('i');

    // MODO CLARO/OSCURO
    if (localStorage.getItem('theme') === 'light') {
        body.classList.add('light-mode');
        icon.classList.replace('fa-moon', 'fa-sun');
    }

    themeBtn.addEventListener('click', () => {
        body.classList.toggle('light-mode');
        const isLight = body.classList.contains('light-mode');
        icon.classList.replace(isLight ? 'fa-moon' : 'fa-sun', isLight ? 'fa-sun' : 'fa-moon');
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
    });

    // TWITCH REAL TIME
    const player = new Twitch.Player("twitch-embed-hidden", {
        channel: "nemo_704",
        width: 10, height: 10, muted: true
    });

    player.addEventListener(Twitch.Player.ONLINE, () => {
        document.getElementById('live-status').classList.remove('hidden');
    });

    player.addEventListener(Twitch.Player.OFFLINE, () => {
        document.getElementById('live-status').classList.add('hidden');
    });
});