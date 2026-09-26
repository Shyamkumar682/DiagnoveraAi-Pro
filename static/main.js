document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('symptomSearch');
    const symptomItems = document.querySelectorAll('.checkbox-wrapper');
    const selectedCountDisplay = document.getElementById('selectedCount');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const form = document.getElementById('diagnosisForm');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase().trim();
            symptomItems.forEach(item => {
                const text = item.querySelector('span').textContent.toLowerCase();
                if (text.includes(term)) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
    function updateSelectionState() {
        let count = 0;
        symptomItems.forEach(item => {
            const checkbox = item.querySelector('input[type="checkbox"]');
            if (checkbox.checked) {
                item.classList.add('active');
                count++;
            } else {
                item.classList.remove('active');
            }
        });
        if (selectedCountDisplay) {
            selectedCountDisplay.textContent = count;
        }
        if (analyzeBtn) {
            analyzeBtn.disabled = count === 0;
        }
    }
    symptomItems.forEach(item => {
        const checkbox = item.querySelector('input[type="checkbox"]');
        checkbox.addEventListener('change', updateSelectionState);
    });
    updateSelectionState();
    const cards = document.querySelectorAll('.glass-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `all 0.6s cubic-bezier(0.4, 0, 0.2, 1) ${index * 0.1}s`;
        requestAnimationFrame(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        });
    });
    const voiceBtn = document.getElementById('voiceBtn');
    if (voiceBtn) {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            voiceBtn.addEventListener('click', () => {
                voiceBtn.innerHTML = '<i data-lucide="radio"></i>';
                lucide.createIcons({root: voiceBtn});
                voiceBtn.style.background = '#ff4757'; 
                voiceBtn.style.boxShadow = '0 0 20px rgba(255, 71, 87, 0.6)';
                recognition.start();
            });
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript.toLowerCase();
                console.log("Speech recognized:", transcript);
                symptomItems.forEach(item => {
                    const checkbox = item.querySelector('input[type="checkbox"]');
                    const symptomName = item.querySelector('span').textContent.toLowerCase();
                    const words = symptomName.split(' ');
                    let matched = false;
                    for (let w of words) {
                        if (w.length > 3 && transcript.includes(w)) {
                            matched = true; break;
                        }
                    }
                    if (transcript.includes(symptomName)) matched = true;
                    if (matched && !checkbox.checked) {
                        checkbox.checked = true;
                        checkbox.dispatchEvent(new Event('change'));
                        item.style.transform = 'scale(1.05)';
                        setTimeout(() => item.style.transform = '', 300);
                    }
                });
            };
            const resetVoiceBtn = () => {
                voiceBtn.innerHTML = '<i data-lucide="mic"></i>';
                lucide.createIcons({root: voiceBtn});
                voiceBtn.style.background = '';
                voiceBtn.style.boxShadow = '';
            };
            recognition.onerror = resetVoiceBtn;
            recognition.onend = resetVoiceBtn;
        } else {
            voiceBtn.style.display = 'none';
        }
    }
});
