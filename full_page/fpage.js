const mode = document.getElementById('mode_icon');

mode.addEventListener('click', () => {
    const form = document.getElementById('container');

    if(mode.classList.contains('fa-sun')) {
        mode.classList.remove('fa-sun');
        mode.classList.add('fa-moon');

        form.classList.add('dark');
        return ;
    }
    
    mode.classList.remove('fa-moon');
    mode.classList.add('fa-sun');

    form.classList.remove('dark');
});