/**
 * Quiz App - Frontend JavaScript
 */

// State
const state = {
    sessionId: null,
    questions: [],
    currentIndex: 0,
    selectedOption: null,
    selfEvaluation: null,
    nQuestions: 20,
    modo: 'mixto',
    ratioMcq: 0.7,
    selectedTemas: [],
    failedCardIds: [],
    timerSeconds: 0,
    timerInterval: null,
    questionStartTime: null
};

const MODE_LABELS = {
    mixto: 'Mixto',
    mcq: 'Respuesta múltiple',
    abierto: 'Respuesta abierta'
};

const TEMA_LABELS = {
    salud_mental: 'Salud Mental',
    urgencias: 'Urgencias',
    cirugia: 'Cirugía',
    mezclas: 'Mezclas'
};

const SUBTEMA_LABELS = {
    afectividad: 'afectividad',
    alucinaciones: 'alucinaciones',
    atencion: 'atención',
    calculo: 'cálculo',
    conciencia: 'conciencia',
    funciones_mentales: 'funciones mentales',
    inteligencia: 'inteligencia',
    juicio: 'juicio',
    lenguaje: 'lenguaje',
    memoria: 'memoria',
    orientacion: 'orientación',
    pensamiento: 'pensamiento',
    porte_actitud: 'porte y actitud',
    psicomotor: 'psicomotor',
    sensopercepcion: 'sensopercepción',
    'sueño': 'sueño'
};

function prettifyLabel(value) {
    return value.replace(/_/g, ' ');
}

function getTemaLabel(tema) {
    return TEMA_LABELS[tema] || prettifyLabel(tema);
}

function getSubtemaLabel(subtema) {
    return SUBTEMA_LABELS[subtema] || prettifyLabel(subtema);
}

function getModeLabel(mode) {
    return MODE_LABELS[mode] || prettifyLabel(mode);
}

// DOM Elements
const views = {
    config: document.getElementById('view-config'),
    question: document.getElementById('view-question'),
    feedback: document.getElementById('view-feedback'),
    summary: document.getElementById('view-summary'),
    history: document.getElementById('view-history')
};

// Initialize app
document.addEventListener('DOMContentLoaded', init);

function init() {
    loadTemas();
    setupEventListeners();
}

// ====== Setup ======

function setupEventListeners() {
    // Config view - button groups
    document.querySelectorAll('.config-section .button-group').forEach(group => {
        group.addEventListener('click', (e) => {
            if (e.target.classList.contains('btn-option')) {
                // Find which config section
                const section = e.target.closest('.config-section');
                const input = section.querySelector('input[type="hidden"]');

                // Toggle selection with animation
                section.querySelectorAll('.btn-option').forEach(btn => btn.classList.remove('selected'));
                e.target.classList.add('selected');

                if (input) {
                    input.value = e.target.dataset.value;

                    // Update state
                    if (input.id === 'n-questions') {
                        state.nQuestions = parseInt(e.target.dataset.value);
                    } else if (input.id === 'modo') {
                        state.modo = e.target.dataset.value;
                        // Show/hide ratio slider
                        document.getElementById('ratio-section').style.display =
                            state.modo === 'mixto' ? 'block' : 'none';
                    } else if (input.id === 'timer-seconds') {
                        state.timerSeconds = parseInt(e.target.dataset.value);
                    }
                }
            }
        });
    });

    // Ratio slider
    const ratioSlider = document.getElementById('ratio-mcq');
    ratioSlider.addEventListener('input', (e) => {
        state.ratioMcq = parseInt(e.target.value) / 100;
        document.getElementById('ratio-display').textContent = e.target.value + '%';
    });

    // Start button
    document.getElementById('btn-start').addEventListener('click', startQuiz);

    // History button
    document.getElementById('btn-history').addEventListener('click', showHistory);
    document.getElementById('btn-back-config').addEventListener('click', () => showView('config'));

    // Confirm/Show answer buttons
    document.getElementById('btn-confirm').addEventListener('click', confirmAnswer);
    document.getElementById('btn-show-answer').addEventListener('click', showAnswer);

    // Next button
    document.getElementById('btn-next').addEventListener('click', nextQuestion);

    // Self-evaluation buttons
    document.querySelectorAll('.btn-eval').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.btn-eval').forEach(b => b.classList.remove('selected'));
            e.target.classList.add('selected');
            state.selfEvaluation = e.target.dataset.value;
            document.getElementById('btn-next').style.display = 'block';
        });
    });

    // New quiz button
    document.getElementById('btn-new-quiz').addEventListener('click', () => {
        state.failedCardIds = [];
        showView('config');
    });

    // Back to config from summary
    document.getElementById('btn-back-summary').addEventListener('click', () => {
        showView('config');
    });
}

async function loadTemas() {
    try {
        const response = await fetch('/api/temas');
        const data = await response.json();

        const container = document.getElementById('temas-container');
        const temas = [...new Set(data.temas.map(t => t.tema))];

        container.innerHTML = temas.map(tema => `
            <label class="checkbox-item">
                <input type="checkbox" value="${tema}" checked>
                ${getTemaLabel(tema)}
            </label>
        `).join('');

        // Update state when checkboxes change
        container.addEventListener('change', () => {
            state.selectedTemas = Array.from(
                container.querySelectorAll('input:checked')
            ).map(cb => cb.value);
        });

        // Initialize state
        state.selectedTemas = temas;

    } catch (error) {
        console.error('Error loading temas:', error);
        document.getElementById('temas-container').innerHTML =
            '<div class="loading">Error al cargar los temas</div>';
    }
}

// ====== Views ======

function showView(name) {
    Object.values(views).forEach(v => v.classList.remove('active'));
    views[name].classList.add('active');

    // Stop timer when leaving question view
    if (name !== 'question') {
        stopTimer();
    }

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ====== Timer ======

function startTimer() {
    if (state.timerSeconds <= 0) return;

    const timerDisplay = document.getElementById('timer-display');
    const timerValue = document.getElementById('timer-value');

    timerDisplay.style.display = 'flex';
    timerDisplay.classList.remove('warning');

    let remaining = state.timerSeconds;
    timerValue.textContent = remaining;
    state.questionStartTime = Date.now();

    state.timerInterval = setInterval(() => {
        remaining--;
        timerValue.textContent = remaining;

        // Warning at 10 seconds
        if (remaining <= 10) {
            timerDisplay.classList.add('warning');
        }

        // Time's up
        if (remaining <= 0) {
            stopTimer();
            handleTimeUp();
        }
    }, 1000);
}

function stopTimer() {
    if (state.timerInterval) {
        clearInterval(state.timerInterval);
        state.timerInterval = null;
    }
    const timerDisplay = document.getElementById('timer-display');
    if (timerDisplay) {
        timerDisplay.style.display = 'none';
    }
}

function handleTimeUp() {
    const q = state.questions[state.currentIndex];

    if (q.formato === 'mcq') {
        // Auto-submit with no selection (incorrect)
        state.selectedOption = -1; // Invalid selection
        confirmAnswer();
    } else {
        // Show answer for open questions
        showAnswer();
    }
}

function getElapsedTime() {
    if (!state.questionStartTime) return null;
    return Math.round((Date.now() - state.questionStartTime) / 1000);
}

// ====== Quiz Flow ======

async function startQuiz() {
    const btn = document.getElementById('btn-start');
    btn.disabled = true;
    btn.textContent = 'Cargando...';

    const config = {
        n_questions: state.nQuestions,
        modo: state.modo,
        ratio_mcq: state.ratioMcq,
        temas: state.selectedTemas.length > 0 ? state.selectedTemas : null
    };

    try {
        const response = await fetch('/api/quiz/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || 'Error al iniciar el quiz');
            btn.disabled = false;
            btn.textContent = 'Comenzar quiz';
            return;
        }

        state.sessionId = data.session_id;
        state.questions = data.questions;
        state.currentIndex = 0;
        state.failedCardIds = [];

        document.getElementById('total-q').textContent = state.questions.length;

        showQuestion();
        showView('question');

    } catch (error) {
        console.error('Error starting quiz:', error);
        alert('Error de conexión');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Comenzar quiz';
    }
}

function showQuestion() {
    const q = state.questions[state.currentIndex];
    state.selectedOption = null;
    state.selfEvaluation = null;
    state.questionStartTime = Date.now();

    // Update progress
    document.getElementById('current-q').textContent = state.currentIndex + 1;
    const progress = ((state.currentIndex) / state.questions.length) * 100;
    document.getElementById('progress-fill').style.width = progress + '%';

    // Update question meta with styled badges
    const temaEl = document.getElementById('q-subtema');
    const formatoEl = document.getElementById('q-formato');

    temaEl.textContent = getTemaLabel(q.tema);
    formatoEl.textContent = q.formato === 'mcq' ? 'Respuesta múltiple' : 'Respuesta abierta';
    formatoEl.className = 'badge ' + (q.formato === 'mcq' ? 'mcq' : 'abierta');

    // Update question text
    document.getElementById('question-text').textContent = q.pregunta;

    // Show appropriate input
    const mcqContainer = document.getElementById('mcq-options');
    const openContainer = document.getElementById('open-answer');
    const btnConfirm = document.getElementById('btn-confirm');
    const btnShowAnswer = document.getElementById('btn-show-answer');

    if (q.formato === 'mcq') {
        mcqContainer.style.display = 'flex';
        openContainer.style.display = 'none';
        btnConfirm.style.display = 'block';
        btnShowAnswer.style.display = 'none';

        // Render options with animation delay
        mcqContainer.innerHTML = q.opciones.map((opt, i) => `
            <button class="option-btn" data-index="${i}" style="animation-delay: ${i * 0.1}s">${opt}</button>
        `).join('');

        // Option click handler
        mcqContainer.querySelectorAll('.option-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                mcqContainer.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
                e.target.classList.add('selected');
                state.selectedOption = parseInt(e.target.dataset.index);
            });
        });

    } else {
        mcqContainer.style.display = 'none';
        openContainer.style.display = 'block';
        btnConfirm.style.display = 'none';
        btnShowAnswer.style.display = 'block';

        document.getElementById('user-answer').value = '';
        document.getElementById('user-answer').focus();
    }

    // Start timer if configured
    startTimer();
}

async function confirmAnswer() {
    stopTimer();
    const q = state.questions[state.currentIndex];
    const timeSpent = getElapsedTime();

    if (q.formato === 'mcq' && state.selectedOption === null) {
        alert('Selecciona una opción');
        startTimer(); // Restart timer
        return;
    }

    const isCorrect = state.selectedOption === q.respuesta_correcta_index;

    // Record response
    await fetch('/api/quiz/answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: state.sessionId,
            card_id: q.card_id,
            formato: q.formato,
            user_answer: state.selectedOption >= 0 ? q.opciones[state.selectedOption] : '(sin respuesta)',
            correct: isCorrect,
            time_seconds: timeSpent
        })
    });

    // Track failed cards
    if (!isCorrect) {
        state.failedCardIds.push(q.card_id);
    }

    // Show feedback
    showFeedback(isCorrect, q);
}

function showAnswer() {
    stopTimer();
    const q = state.questions[state.currentIndex];
    showFeedback(null, q, true);
}

function showFeedback(isCorrect, question, isOpen = false) {
    const resultDiv = document.getElementById('feedback-result');
    const selfEvalDiv = document.getElementById('self-eval');
    const btnNext = document.getElementById('btn-next');

    // Reset self-eval buttons
    document.querySelectorAll('.btn-eval').forEach(b => b.classList.remove('selected'));

    if (isOpen) {
        // Open question - show self evaluation
        resultDiv.className = 'feedback-result pending';
        resultDiv.innerHTML = '📝 Evalúa tu respuesta';
        selfEvalDiv.style.display = 'block';
        btnNext.style.display = 'none';
    } else {
        // MCQ - show result with emoji
        if (isCorrect) {
            resultDiv.className = 'feedback-result correct';
            resultDiv.innerHTML = '✅ ¡Correcto!';
        } else {
            resultDiv.className = 'feedback-result incorrect';
            resultDiv.innerHTML = '❌ ¡Incorrecto!';
        }
        selfEvalDiv.style.display = 'none';
        btnNext.style.display = 'block';

        // Highlight options
        const options = document.querySelectorAll('.option-btn');
        options.forEach((btn, i) => {
            btn.classList.add('disabled');
            if (i === question.respuesta_correcta_index) {
                btn.classList.add('correct');
            } else if (i === state.selectedOption && !isCorrect) {
                btn.classList.add('incorrect');
            }
        });
    }

    // Show correct answer with HTML rendering
    document.getElementById('correct-answer-text').innerHTML = question.respuesta_correcta;

    // Show explanation if available
    const explanationSection = document.getElementById('explanation-section');
    const explanationText = document.getElementById('explanation-text');

    if (question.explicacion) {
        explanationText.textContent = question.explicacion;
        explanationSection.style.display = 'block';
    } else {
        explanationSection.style.display = 'none';
    }

    showView('feedback');
}

async function nextQuestion() {
    const q = state.questions[state.currentIndex];
    const timeSpent = getElapsedTime();

    // For open questions, record with self evaluation
    if (q.formato === 'abierto' && state.selfEvaluation) {
        const isCorrect = state.selfEvaluation === 'sabia';

        await fetch('/api/quiz/answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: state.sessionId,
                card_id: q.card_id,
                formato: q.formato,
                user_answer: document.getElementById('user-answer').value,
                correct: isCorrect,
                self_evaluation: state.selfEvaluation,
                time_seconds: timeSpent
            })
        });

        if (!isCorrect) {
            state.failedCardIds.push(q.card_id);
        }
    }

    state.currentIndex++;

    if (state.currentIndex >= state.questions.length) {
        // Quiz finished
        await endQuiz();
    } else {
        showQuestion();
        showView('question');
    }
}

async function endQuiz() {
    try {
        const response = await fetch('/api/quiz/end', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: state.sessionId })
        });

        const summary = await response.json();
        showSummary(summary);

    } catch (error) {
        console.error('Error ending quiz:', error);
    }
}

function showSummary(summary) {
    // Score
    const percent = Math.round((summary.n_correct / summary.n_questions) * 100);
    const scoreEl = document.getElementById('final-score');
    const emojiEl = document.getElementById('score-emoji');

    scoreEl.textContent = percent + '%';
    document.getElementById('correct-count').textContent = summary.n_correct;
    document.getElementById('total-count').textContent = summary.n_questions;

    // Set score color class and emoji based on performance
    scoreEl.className = 'score-big';
    if (percent >= 90) {
        scoreEl.classList.add('excellent');
        emojiEl.textContent = '🎉';
        // Trigger confetti for excellent scores
        setTimeout(() => createConfetti(), 300);
    } else if (percent >= 70) {
        scoreEl.classList.add('good');
        emojiEl.textContent = '👍';
    } else if (percent >= 50) {
        scoreEl.classList.add('needs-work');
        emojiEl.textContent = '💪';
    } else {
        scoreEl.classList.add('poor');
        emojiEl.textContent = '📚';
    }

    // By formato
    const byFormato = document.getElementById('by-formato');
    byFormato.innerHTML = Object.entries(summary.by_formato)
        .filter(([_, data]) => data.total > 0)
        .map(([formato, data]) => {
            const pct = Math.round((data.correct / data.total) * 100);
            const cls = pct >= 70 ? 'good' : pct >= 50 ? 'medium' : 'bad';
            return `
                <div class="summary-row">
                <span class="label">${formato === 'mcq' ? 'Respuesta múltiple' : 'Respuesta abierta'}</span>
                    <span class="value ${cls}">${data.correct}/${data.total} (${pct}%)</span>
                </div>
            `;
        }).join('');

    // By tema
    const byTema = document.getElementById('by-subtema');
    byTema.innerHTML = Object.entries(summary.by_tema || summary.by_subtema)
        .sort((a, b) => (a[1].correct / a[1].total) - (b[1].correct / b[1].total))
        .map(([tema, data]) => {
            const pct = Math.round((data.correct / data.total) * 100);
            const cls = pct >= 70 ? 'good' : pct >= 50 ? 'medium' : 'bad';
            return `
                <div class="summary-row">
                    <span class="label">${getTemaLabel(tema)}</span>
                    <span class="value ${cls}">${data.correct}/${data.total} (${pct}%)</span>
                </div>
            `;
        }).join('');

    // Failed cards
    const failedSection = document.getElementById('failed-section');
    const failedCardsDiv = document.getElementById('failed-cards');

    if (summary.failed_cards && summary.failed_cards.length > 0) {
        failedSection.style.display = 'block';
        failedCardsDiv.innerHTML = summary.failed_cards.map(card => `
            <div class="failed-card-item">
                <div class="q">${card.pregunta}</div>
                <div class="a">${card.respuesta_correcta}</div>
            </div>
        `).join('');
    } else {
        failedSection.style.display = 'none';
    }

    showView('summary');
}

// ====== Confetti Animation ======

function createConfetti() {
    const colors = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];
    const container = document.body;

    for (let i = 0; i < 50; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.top = Math.random() * 50 + 50 + 'vh';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.width = Math.random() * 10 + 5 + 'px';
            confetti.style.height = confetti.style.width;
            confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
            container.appendChild(confetti);

            setTimeout(() => confetti.remove(), 1000);
        }, i * 30);
    }
}

// ====== History ======

async function showHistory() {
    const historyList = document.getElementById('history-list');
    historyList.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <span>Cargando historial...</span>
        </div>
    `;

    showView('history');

    try {
        const response = await fetch('/api/history?limit=20');
        const data = await response.json();

        if (data.sessions.length === 0) {
            historyList.innerHTML = `
                <div class="history-empty">
                    <p>No hay sesiones anteriores</p>
                    <p style="font-size: 0.9rem; margin-top: 0.5rem;">Completa tu primer quiz para ver tu historial aquí</p>
                </div>
            `;
        } else {
            historyList.innerHTML = data.sessions.map(session => {
                const date = new Date(session.started_at);
                const dateStr = date.toLocaleDateString('es-ES', {
                    day: 'numeric',
                    month: 'short',
                    hour: '2-digit',
                    minute: '2-digit'
                });

                const scoreClass = session.score_percent >= 70 ? 'good' :
                                   session.score_percent >= 50 ? 'medium' : 'bad';

                return `
                    <div class="history-item ${scoreClass}" data-session-id="${session.session_id}">
                        <div class="history-item-header">
                            <span class="history-date">${dateStr}</span>
                            <span class="history-score ${scoreClass}">${session.score_percent}%</span>
                        </div>
                        <div class="history-details">
                            <span>${session.n_correct}/${session.n_questions} correctas</span>
                            <span>${getModeLabel(session.modo)}</span>
                        </div>
                    </div>
                `;
            }).join('');

            // Click handler to view session details
            historyList.querySelectorAll('.history-item').forEach(item => {
                item.addEventListener('click', async () => {
                    const sessionId = item.dataset.sessionId;
                    const response = await fetch(`/api/quiz/${sessionId}/summary`);
                    const summary = await response.json();
                    showSummary(summary);
                });
            });
        }

    } catch (error) {
        console.error('Error loading history:', error);
        historyList.innerHTML = `
            <div class="history-empty">
                <p>Error al cargar el historial</p>
            </div>
        `;
    }
}
