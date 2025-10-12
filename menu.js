document.addEventListener('DOMContentLoaded', function() {
    var menuBtn = document.getElementById('menuBtn');
    var dropdownMenu = document.getElementById('dropdownMenu');

    if (menuBtn && dropdownMenu) {
        menuBtn.onclick = function(event) {
            event.stopPropagation();
            dropdownMenu.style.display = (dropdownMenu.style.display === 'block') ? 'none' : 'block';
        };

        document.addEventListener('click', function(event) {
            if (!dropdownMenu.contains(event.target) && event.target !== menuBtn) {
                dropdownMenu.style.display = 'none';
            }
        });
    }
});

