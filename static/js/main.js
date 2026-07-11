/**
 * Quiz Application Frontend Core Logic
 * 
 * Handles:
 *  1. Precise Session-Based Countdown Timer (with auto-submit on expiry)
 *  2. Flash message auto-dismissal
 *  3. Interactive chart visualization placeholder drawing
 */

document.addEventListener('DOMContentLoaded', () => {
    initFlashDismissal();
    initQuizTimer();
    initDashboardChart();
});

/**
 * 1. Countdown Timer Logic
 */
function initQuizTimer() {
    const timerElement = document.getElementById('quiz-timer');
    if (!timerElement) return;

    const timeLimit = parseInt(timerElement.dataset.timeLimit, 10); // in seconds
    const startTimeISO = timerElement.dataset.startTime; // ISO timestamp
    const quizForm = document.getElementById('quiz-form');
    const timerProgress = document.getElementById('timer-progress-bar');

    if (!startTimeISO || !quizForm) return;

    const startTime = new Date(startTimeISO).getTime();

    function updateTimer() {
        const now = new Date().getTime();
        // Time elapsed in seconds
        const elapsed = Math.floor((now - startTime) / 1000);
        const remaining = timeLimit - elapsed;

        if (remaining <= 0) {
            clearInterval(timerInterval);
            timerElement.textContent = "00:00";
            timerElement.classList.add('text-danger', 'fw-bold');
            if (timerProgress) {
                timerProgress.style.width = '0%';
                timerProgress.classList.remove('bg-info');
                timerProgress.classList.add('bg-danger');
            }
            
            // Inject auto-submit action trigger and submit the form
            let actionInput = quizForm.querySelector('input[name="action"]');
            if (!actionInput) {
                actionInput = document.createElement('input');
                actionInput.type = 'hidden';
                actionInput.name = 'action';
                quizForm.appendChild(actionInput);
            }
            actionInput.value = 'submit';
            
            // Display alert and auto-submit
            alert("Time has expired! Your quiz is being submitted automatically.");
            quizForm.submit();
            return;
        }

        // Format MM:SS
        const minutes = Math.floor(remaining / 60);
        const seconds = remaining % 60;
        const displayMinutes = String(minutes).padStart(2, '0');
        const displaySeconds = String(seconds).padStart(2, '0');
        timerElement.textContent = `${displayMinutes}:${displaySeconds}`;

        // Update progress bar
        if (timerProgress) {
            const percentage = (remaining / timeLimit) * 100;
            timerProgress.style.width = `${percentage}%`;
            
            if (remaining < 30) {
                timerElement.classList.add('text-danger', 'blink-timer');
                timerProgress.classList.remove('bg-info', 'bg-warning');
                timerProgress.classList.add('bg-danger');
            } else if (remaining < 60) {
                timerProgress.classList.remove('bg-info');
                timerProgress.classList.add('bg-warning');
            }
        }
    }

    // Run first calculation immediately and set interval
    updateTimer();
    const timerInterval = setInterval(updateTimer, 1000);
}

/**
 * 2. Auto Dismiss Flash Alerts after 5 seconds
 */
function initFlashDismissal() {
    const alerts = document.querySelectorAll('#flash-container .alert');
    alerts.forEach(alertEl => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });
}

/**
 * 3. Render Canvas-Based Dashboard Statistics Chart
 * Using raw Canvas API to ensure self-contained, offline-compatible operation.
 */
function initDashboardChart() {
    const canvas = document.getElementById('attemptsChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Read chart data from dataset attributes
    const rawScores = canvas.dataset.scores || '';
    const scores = rawScores.split(',').map(s => parseFloat(s)).filter(s => !isNaN(s));

    if (scores.length === 0) {
        // Draw centered empty state message
        ctx.fillStyle = '#64748b';
        ctx.font = '14px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Take some quizzes to visualize your progress!', canvas.width / 2, canvas.height / 2);
        return;
    }

    // Chart parameters
    const padding = 40;
    const chartWidth = canvas.width - padding * 2;
    const chartHeight = canvas.height - padding * 2;
    const maxScore = 100;

    // Draw horizontal grid lines
    ctx.strokeStyle = '#f1f5f9';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
        const y = padding + (chartHeight * (4 - i)) / 4;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(canvas.width - padding, y);
        ctx.stroke();

        // Y-axis Labels
        ctx.fillStyle = '#94a3b8';
        ctx.font = '10px Inter, sans-serif';
        ctx.textAlign = 'right';
        ctx.fillText(`${i * 25}%`, padding - 8, y + 3);
    }

    // Plot line
    const xStep = scores.length > 1 ? chartWidth / (scores.length - 1) : chartWidth;
    
    // Draw area gradient
    const gradient = ctx.createLinearGradient(0, padding, 0, canvas.height - padding);
    gradient.addColorStop(0, 'rgba(59, 130, 246, 0.3)');
    gradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

    ctx.beginPath();
    scores.forEach((score, index) => {
        const x = padding + index * xStep;
        const y = canvas.height - padding - (score / maxScore) * chartHeight;
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    
    // Close area path for filling gradient
    if (scores.length > 0) {
        const lastX = padding + (scores.length - 1) * xStep;
        ctx.lineTo(lastX, canvas.height - padding);
        ctx.lineTo(padding, canvas.height - padding);
        ctx.closePath();
        ctx.fillStyle = gradient;
        ctx.fill();
    }

    // Draw line path
    ctx.beginPath();
    scores.forEach((score, index) => {
        const x = padding + index * xStep;
        const y = canvas.height - padding - (score / maxScore) * chartHeight;
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    ctx.strokeStyle = '#1e40af';
    ctx.lineWidth = 3;
    ctx.lineJoin = 'round';
    ctx.stroke();

    // Draw points & labels
    scores.forEach((score, index) => {
        const x = padding + index * xStep;
        const y = canvas.height - padding - (score / maxScore) * chartHeight;

        // Outer white glow circle
        ctx.beginPath();
        ctx.arc(x, y, 6, 0, Math.PI * 2);
        ctx.fillStyle = '#ffffff';
        ctx.fill();
        ctx.strokeStyle = '#1e40af';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Data point label
        ctx.fillStyle = '#0f172a';
        ctx.font = 'bold 10px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(`${score}%`, x, y - 10);

        // X-axis label
        ctx.fillStyle = '#94a3b8';
        ctx.font = '10px Inter, sans-serif';
        ctx.fillText(`Quiz ${index + 1}`, x, canvas.height - padding + 18);
    });
}
