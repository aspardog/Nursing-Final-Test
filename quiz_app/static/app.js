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
    selectedSubtemas: [],
    failedCardIds: [],
    timerSeconds: 0,
    timerInterval: null,
    questionStartTime: null
};

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

                // Toggle selection
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

    // Retry failed button
    document.getElementById('btn-retry-failed').addEventListener('click', retryFailed);
}

async function loadTemas() {
    try {
        const response = await fetch('/api/temas');
        const data = await response.json();

        const container = document.getElementById('temas-container');
        const subtemas = [...new Set(data.temas.map(t => t.subtema))];

        container.innerHTML = subtemas.map(subtema => `
            <label class="checkbox-item">
                <input type="checkbox" value="${subtema}" checked>
                ${subtema.replace(/_/g, ' ')}
            </label>
        `).join('');

        // Update state when checkboxes change
        container.addEventListener('change', () => {
            state.selectedSubtemas = Array.from(
                container.querySelectorAll('input:checked')
            ).map(cb => cb.value);
        });

        // Initialize state
        state.selectedSubtemas = subtemas;

    } catch (error) {
        console.error('Error loading temas:', error);
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
}

// ====== Timer ======

function startTimer() {
    if (state.timerSeconds <= 0) return;

    const timerDisplay = document.getElementById('timer-display');
    const timerValue = document.getElementById('timer-value');

    timerDisplay.style.display = 'block';
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
    const config = {
        n_questions: state.nQuestions,
        modo: state.modo,
        ratio_mcq: state.ratioMcq,
        subtemas: state.selectedSubtemas.length > 0 ? state.selectedSubtemas : null
    };

    try {
        const response = await fetch('/api/quiz/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || 'Error starting quiz');
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
        alert('Error de conexion');
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

    // Update question meta
    document.getElementById('q-subtema').textContent = q.subtema.replace(/_/g, ' ');
    document.getElementById('q-formato').textContent = q.formato === 'mcq' ? 'Opcion Multiple' : 'Abierta';

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

        // Render options
        mcqContainer.innerHTML = q.opciones.map((opt, i) => `
            <button class="option-btn" data-index="${i}">${opt}</button>
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
    }

    // Start timer if configured
    startTimer();
}

async function confirmAnswer() {
    stopTimer();
    const q = state.questions[state.currentIndex];
    const timeSpent = getElapsedTime();

    if (q.formato === 'mcq' && state.selectedOption === null) {
        alert('Selecciona una opcion');
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
        resultDiv.textContent = 'Evalua tu respuesta';
        selfEvalDiv.style.display = 'block';
        btnNext.style.display = 'none';
    } else {
        // MCQ - show result
        resultDiv.className = 'feedback-result ' + (isCorrect ? 'correct' : 'incorrect');
        resultDiv.textContent = isCorrect ? 'Correcto!' : 'Incorrecto';
        selfEvalDiv.style.display = 'none';
        btnNext.style.display = 'block';

        // Highlight options
        const options = document.querySelectorAll('.option-btn');
        options.forEach((btn, i) => {
            if (i === question.respuesta_correcta_index) {
                btn.classList.add('correct');
            } else if (i === state.selectedOption && !isCorrect) {
                btn.classList.add('incorrect');
            }
        });
    }

    // Show correct answer with HTML rendering
    document.getElementById('correct-answer-text').innerHTML = question.respuesta_correcta;

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
    document.getElementById('final-score').textContent = percent + '%';
    document.getElementById('correct-count').textContent = summary.n_correct;
    document.getElementById('total-count').textContent = summary.n_questions;

    // By formato
    const byFormato = document.getElementById('by-formato');
    byFormato.innerHTML = Object.entries(summary.by_formato)
        .filter(([_, data]) => data.total > 0)
        .map(([formato, data]) => {
            const pct = Math.round((data.correct / data.total) * 100);
            const cls = pct >= 70 ? 'good' : pct >= 50 ? '' : 'bad';
            return `
                <div class="summary-row">
                    <span class="label">${formato === 'mcq' ? 'Opcion Multiple' : 'Abierta'}</span>
                    <span class="value ${cls}">${data.correct}/${data.total} (${pct}%)</span>
                </div>
            `;
        }).join('');

    // By subtema
    const bySubtema = document.getElementById('by-subtema');
    bySubtema.innerHTML = Object.entries(summary.by_subtema)
        .sort((a, b) => (a[1].correct / a[1].total) - (b[1].correct / b[1].total))
        .map(([subtema, data]) => {
            const pct = Math.round((data.correct / data.total) * 100);
            const cls = pct >= 70 ? 'good' : pct >= 50 ? '' : 'bad';
            return `
                <div class="summary-row">
                    <span class="label">${subtema.replace(/_/g, ' ')}</span>
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

async function retryFailed() {
    alert('Funcion en desarrollo. Por ahora, las tarjetas falladas se muestran arriba para repaso.');
}

// ====== History ======

async function showHistory() {
    try {
        const response = await fetch('/api/history?limit=20');
        const data = await response.json();

        const historyList = document.getElementById('history-list');

        if (data.sessions.length === 0) {
            historyList.innerHTML = '<div class="history-empty">No hay sesiones anteriores</div>';
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
                    <div class="history-item" data-session-id="${session.session_id}">
                        <div class="history-item-header">
                            <span class="history-date">${dateStr}</span>
                            <span class="history-score ${scoreClass}">${session.score_percent}%</span>
                        </div>
                        <div class="history-details">
                            <span>${session.n_correct}/${session.n_questions} correctas</span>
                            <span>${session.modo}</span>
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

        showView('history');

    } catch (error) {
        console.error('Error loading history:', error);
        alert('Error cargando historial');
    }
}
