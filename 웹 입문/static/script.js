window.addEventListener('DOMContentLoaded', () => {
    const textElement = document.getElementById('moving');

    if (textElement) {
        textElement.classList.add('auto-moving');

        textElement.addEventListener('mouseenter', () => {
            textElement.classList.remove('auto-moving');
        });

        textElement.addEventListener('mouseleave', () => {
            textElement.classList.add('auto-moving');
        });
    }
});
const btn = document.getElementById('fly-btn');

btn.addEventListener('mouseover', () => {
    const randomX = Math.random() * (window.innerWidth - btn.offsetWidth);
    const randomY = Math.random() * (window.innerHeight - btn.offsetHeight);

    btn.style.left = randomX + 'px';
    btn.style.top = randomY + 'px';
});

btn.addEventListener('click', () => {
    btn.textContent = "힛";
    btn.style.transition = "transform 1s cubic-bezier(0.25, 1, 0.5, 1), opacity 1s";
    
    btn.style.transform = "translateY(-1000px) rotate(360deg) scale(0.1)";
    btn.style.opacity = "0";

    setTimeout(() => {
        btn.style.transition = "all 0.2s ease-out";
        btn.style.transform = "translateY(0) rotate(0) scale(1)";
        btn.style.opacity = "1";
        btn.textContent = "히히";
        
        btn.style.left = (window.innerWidth / 2 - btn.offsetWidth / 2) + 'px';
        btn.style.top = (window.innerHeight / 2 - btn.offsetHeight / 2) + 'px';
    }, 2500);
});