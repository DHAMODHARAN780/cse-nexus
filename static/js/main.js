document.addEventListener('DOMContentLoaded', function () {
    // Image Slider Logic
    const slides = document.querySelectorAll('.hero-slider .slide');
    if (slides.length > 0) {
        let currentSlide = 0;
        let slideInterval;

        function showSlide(index) {
            slides[currentSlide].classList.remove('active');
            currentSlide = (index + slides.length) % slides.length;
            slides[currentSlide].classList.add('active');
        }

        function nextSlide() {
            showSlide(currentSlide + 1);
        }

        function startInterval() {
            stopInterval();
            slideInterval = setInterval(nextSlide, 5000);
        }

        function stopInterval() {
            if (slideInterval) clearInterval(slideInterval);
        }

        window.moveSlide = function (n) {
            showSlide(currentSlide + n);
            startInterval(); // Reset timer when manual move occurs
        };

        startInterval();
    }



    // PDF Viewer Modal Logic
    const viewerModal = document.getElementById('viewerModal');
    const viewerFrame = document.getElementById('viewerFrame');
    const modalTitle = document.getElementById('modalTitle');

    window.viewDocument = function (url, title) {
        if (!viewerModal || !viewerFrame) return;
        modalTitle.textContent = title;
        viewerFrame.src = url;
        viewerModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    // Detail Modal Logic (Announcements/Achievements)
    const detailModal = document.getElementById('detailModal');
    const detailTitle = document.getElementById('detailTitle');
    const detailText = document.getElementById('detailText');
    const detailMeta = document.getElementById('detailMeta');
    const detailMedia = document.getElementById('detailMedia');

    window.showDetails = function (data) {
        if (!detailModal) return;
        detailTitle.innerText = data.title;
        detailText.innerText = data.text;
        detailMeta.innerText = data.date;

        detailMedia.innerHTML = '';
        if (data.file) {
            const isImage = /\.(jpg|jpeg|png|gif)$/i.test(data.file);
            if (isImage) {
                detailMedia.innerHTML = `<img src="${data.file}" style="max-width: 100%; border-radius: 12px; border: 1px solid var(--border);">`;
            } else {
                detailMedia.innerHTML = `
                    <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 12px; display: flex; align-items: center; justify-content: space-between;">
                        <span><i class="fas fa-file-pdf"></i> Attached Document</span>
                        <button onclick="viewDocument('${data.file}', '${data.title}')" class="btn btn-primary">View Document</button>
                    </div>
                `;
            }
        }
        detailModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    // Global click handler for view buttons
    document.addEventListener('click', function (e) {
        // Document Viewers
        const viewBtn = e.target.closest('.btn-view');
        if (viewBtn) {
            e.preventDefault();
            const url = viewBtn.getAttribute('data-url');
            const title = viewBtn.getAttribute('data-title');
            window.viewDocument(url, title);
            return;
        }

        // Detail Viewers
        const detailBtn = e.target.closest('.btn-detail');
        if (detailBtn) {
            e.preventDefault();
            window.showDetails(detailBtn.dataset);
            return;
        }

        // Close Modals
        const closeBtn = e.target.closest('.close-modal');
        if (closeBtn) {
            const modal = closeBtn.closest('.modal-overlay');
            if (modal) {
                modal.classList.remove('active');
                if (modal.id === 'viewerModal') viewerFrame.src = '';
                document.body.style.overflow = 'auto';
            }
        }
    });

    // Close on overlay click
    document.querySelectorAll('.modal-overlay').forEach(modal => {
        modal.addEventListener('click', function (e) {
            if (e.target === modal) {
                modal.classList.remove('active');
                if (modal.id === 'viewerModal') viewerFrame.src = '';
                document.body.style.overflow = 'auto';
            }
        });
    });
});
