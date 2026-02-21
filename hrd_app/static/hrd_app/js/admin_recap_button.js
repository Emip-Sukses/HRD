(function () {
    function injectButton() {
        const contentHeader = document.querySelector('.content-header .container-fluid .row');

        if (document.getElementById('custom-recap-btn')) return;

        if (window.location.pathname.includes('/hrd_app/attendance/') && contentHeader) {
            const col = contentHeader.querySelector('.col-sm-6:last-child');
            if (col) {
                const recapBtn = document.createElement('a');
                recapBtn.id = 'custom-recap-btn';
                recapBtn.href = '/rekap/';
                // Menggunakan btn-warning (kuning) agar kontras tinggi dengan teks gelap
                recapBtn.className = 'btn btn-sm btn-warning float-right mr-2';
                recapBtn.innerHTML = '<i class="fas fa-file-invoice me-1"></i> Lihat Rekap Harian';
                // Paksa warna teks hitam agar sangat jelas terlihat
                recapBtn.style.cssText = 'border-radius: 8px; padding: 5px 15px; font-weight: 700; margin-right: 10px; color: #000 !important; border: 2px solid #000;';

                col.prepend(recapBtn);
            }
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectButton);
    } else {
        injectButton();
    }

    setInterval(injectButton, 2000);
})();
