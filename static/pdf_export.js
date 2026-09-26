document.addEventListener('DOMContentLoaded', () => {
    const downloadBtn = document.getElementById('downloadPdfBtn');
    if(downloadBtn) {
        const dateElement = document.getElementById('report-date');
        if(dateElement) {
            const today = new Date();
            dateElement.textContent = today.toLocaleDateString() + ' ' + today.toLocaleTimeString();
        }
        downloadBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const element = document.getElementById('clinical-report');
            const opt = {
                margin:       0,
                filename:     'MediAI_Diagnostic_Report.pdf',
                image:        { type: 'jpeg', quality: 0.98 },
                html2canvas:  { scale: 2, useCORS: true, logging: false },
                jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' },
                pagebreak:    { mode: 'avoid-all' }
            };
            const originalHtml = downloadBtn.innerHTML;
            downloadBtn.innerHTML = '<i data-lucide="loader" class="lucide-spin"></i> Generating...';
            setTimeout(() => {
                html2pdf().set(opt).from(element.outerHTML).save().then(() => {
                    downloadBtn.innerHTML = originalHtml;
                    if(window.lucide) {
                        lucide.createIcons();
                    }
                }).catch(err => {
                    console.error("PDF Generation error:", err);
                    downloadBtn.innerHTML = originalHtml;
                    if(window.lucide) {
                        lucide.createIcons();
                    }
                    alert("An error occurred while generating the PDF.");
                });
            }, 100);
        });
    }
});
