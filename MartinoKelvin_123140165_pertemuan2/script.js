
class DashboardManager {
    constructor() {
        this.tasks = [];
        this.notes = [];
        this.schedules = [];
        this.editingId = null;
        this.editingType = null;
        this.init();
    }

    // Arrow Function: Initialize dashboard
    init = () => {
        this.loadFromStorage();
        this.setupEventListeners();
        this.updateDateTime();
        this.renderAllItems();
        setInterval(this.updateDateTime, 1000);
    };

    // Arrow Function: Setup all event listeners
    setupEventListeners = () => {
        // Tab navigation
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });

        // Task events
        document.getElementById('add-task-btn').addEventListener('click', () => this.toggleTaskForm());
        document.getElementById('task-form').addEventListener('submit', (e) => this.handleTaskSubmit(e));
        document.getElementById('cancel-task-btn').addEventListener('click', () => this.toggleTaskForm());

        // Note events
        document.getElementById('add-note-btn').addEventListener('click', () => this.toggleNoteForm());
        document.getElementById('note-form').addEventListener('submit', (e) => this.handleNoteSubmit(e));
        document.getElementById('cancel-note-btn').addEventListener('click', () => this.toggleNoteForm());

        // Schedule events
        document.getElementById('add-schedule-btn').addEventListener('click', () => this.toggleScheduleForm());
        document.getElementById('schedule-form').addEventListener('submit', (e) => this.handleScheduleSubmit(e));
        document.getElementById('cancel-schedule-btn').addEventListener('click', () => this.toggleScheduleForm());

        // Weather events
        document.getElementById('refresh-weather-btn').addEventListener('click', () => this.fetchWeather());

        // Modal events
        document.querySelector('.close').addEventListener('click', () => this.closeModal());
        document.getElementById('close-modal-btn').addEventListener('click', () => this.closeModal());
        document.getElementById('edit-form').addEventListener('submit', (e) => this.handleEditSubmit(e));
    };

    // Arrow Function: Update date and time
    updateDateTime = () => {
        const now = new Date();
        const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        const timeOptions = { hour: '2-digit', minute: '2-digit', second: '2-digit' };
        
        document.getElementById('current-date').textContent = now.toLocaleDateString('id-ID', dateOptions);
        document.getElementById('current-time').textContent = now.toLocaleTimeString('id-ID', timeOptions);
    };

    // Arrow Function: Switch tabs
    switchTab = (tabName) => {
        document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        
        document.getElementById(tabName).classList.add('active');
        event.target.classList.add('active');

        // Fetch weather when switching to weather tab
        if (tabName === 'weather' && this.tasks.length === 0) {
            this.fetchWeather();
        }
    };

    // ============================================
    // TASK MANAGEMENT
    // ============================================

    toggleTaskForm = () => {
        document.getElementById('task-form').classList.toggle('hidden');
        if (!document.getElementById('task-form').classList.contains('hidden')) {
            document.getElementById('task-input').focus();
        }
    };

    handleTaskSubmit = (e) => {
        e.preventDefault();
        const input = document.getElementById('task-input');
        const priority = document.getElementById('task-priority').value;

        if (input.value.trim()) {
            const task = {
                id: Date.now(),
                title: input.value,
                priority,
                completed: false,
                createdAt: new Date().toISOString()
            };

            this.tasks.push(task);
            this.saveToStorage();
            this.renderTasks();
            input.value = '';
            this.toggleTaskForm();
        }
    };

    renderTasks = () => {
        const tasksList = document.getElementById('tasks-list');
        
        if (this.tasks.length === 0) {
            tasksList.innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">Tidak ada tugas. Tambahkan tugas baru!</p>';
            return;
        }

        // Template literal untuk rendering tasks
        tasksList.innerHTML = this.tasks.map(task => `
            <div class="item ${task.completed ? 'completed' : ''}">
                <div class="item-header">
                    <div style="flex: 1;">
                        <input type="checkbox" class="item-checkbox" ${task.completed ? 'checked' : ''} 
                               onchange="dashboard.toggleTaskComplete(${task.id})">
                        <span class="item-title" style="margin-left: 0.5rem;">${this.escapeHtml(task.title)}</span>
                    </div>
                </div>
                <div class="item-meta">
                    <span class="badge badge-${task.priority}">${this.getPriorityLabel(task.priority)}</span>
                    <span style="color: #999; font-size: 0.85rem;">${this.formatDate(task.createdAt)}</span>
                </div>
                <div class="item-actions">
                    <button class="btn btn-primary btn-small" onclick="dashboard.editTask(${task.id})">Edit</button>
                    <button class="btn btn-danger btn-small" onclick="dashboard.deleteTask(${task.id})">Hapus</button>
                </div>
            </div>
        `).join('');
    };

    toggleTaskComplete = (id) => {
        const task = this.tasks.find(t => t.id === id);
        if (task) {
            task.completed = !task.completed;
            this.saveToStorage();
            this.renderTasks();
        }
    };

    editTask = (id) => {
        const task = this.tasks.find(t => t.id === id);
        if (task) {
            this.editingId = id;
            this.editingType = 'task';
            document.getElementById('modal-title').textContent = 'Edit Tugas';
            document.getElementById('modal-body').innerHTML = `
                <div class="form-group">
                    <label>Judul Tugas</label>
                    <input type="text" id="edit-task-title" value="${this.escapeHtml(task.title)}" required>
                </div>
                <div class="form-group">
                    <label>Prioritas</label>
                    <select id="edit-task-priority">
                        <option value="low" ${task.priority === 'low' ? 'selected' : ''}>Prioritas Rendah</option>
                        <option value="medium" ${task.priority === 'medium' ? 'selected' : ''}>Prioritas Sedang</option>
                        <option value="high" ${task.priority === 'high' ? 'selected' : ''}>Prioritas Tinggi</option>
                    </select>
                </div>
            `;
            document.getElementById('edit-modal').classList.remove('hidden');
        }
    };

    deleteTask = (id) => {
        if (confirm('Apakah Anda yakin ingin menghapus tugas ini?')) {
            this.tasks = this.tasks.filter(t => t.id !== id);
            this.saveToStorage();
            this.renderTasks();
        }
    };

    // ============================================
    // NOTE MANAGEMENT
    // ============================================

    toggleNoteForm = () => {
        document.getElementById('note-form').classList.toggle('hidden');
        if (!document.getElementById('note-form').classList.contains('hidden')) {
            document.getElementById('note-title').focus();
        }
    };

    handleNoteSubmit = (e) => {
        e.preventDefault();
        const title = document.getElementById('note-title').value;
        const content = document.getElementById('note-content').value;

        if (title.trim() && content.trim()) {
            const note = {
                id: Date.now(),
                title,
                content,
                createdAt: new Date().toISOString()
            };

            this.notes.push(note);
            this.saveToStorage();
            this.renderNotes();
            document.getElementById('note-title').value = '';
            document.getElementById('note-content').value = '';
            this.toggleNoteForm();
        }
    };

    renderNotes = () => {
        const notesList = document.getElementById('notes-list');
        
        if (this.notes.length === 0) {
            notesList.innerHTML = '<p style="text-align: center; color: #999; padding: 2rem; grid-column: 1/-1;">Tidak ada catatan. Tambahkan catatan baru!</p>';
            return;
        }

        // Template literal untuk rendering notes
        notesList.innerHTML = this.notes.map(note => `
            <div class="item">
                <div class="item-header">
                    <div>
                        <div class="item-title">${this.escapeHtml(note.title)}</div>
                        <div style="color: #999; font-size: 0.85rem; margin-top: 0.25rem;">${this.formatDate(note.createdAt)}</div>
                    </div>
                </div>
                <div class="item-content">${this.escapeHtml(note.content)}</div>
                <div class="item-actions">
                    <button class="btn btn-primary btn-small" onclick="dashboard.editNote(${note.id})">Edit</button>
                    <button class="btn btn-danger btn-small" onclick="dashboard.deleteNote(${note.id})">Hapus</button>
                </div>
            </div>
        `).join('');
    };

    editNote = (id) => {
        const note = this.notes.find(n => n.id === id);
        if (note) {
            this.editingId = id;
            this.editingType = 'note';
            document.getElementById('modal-title').textContent = 'Edit Catatan';
            document.getElementById('modal-body').innerHTML = `
                <div class="form-group">
                    <label>Judul</label>
                    <input type="text" id="edit-note-title" value="${this.escapeHtml(note.title)}" required>
                </div>
                <div class="form-group">
                    <label>Isi Catatan</label>
                    <textarea id="edit-note-content" rows="4" required>${this.escapeHtml(note.content)}</textarea>
                </div>
            `;
            document.getElementById('edit-modal').classList.remove('hidden');
        }
    };

    deleteNote = (id) => {
        if (confirm('Apakah Anda yakin ingin menghapus catatan ini?')) {
            this.notes = this.notes.filter(n => n.id !== id);
            this.saveToStorage();
            this.renderNotes();
        }
    };

    // ============================================
    // SCHEDULE MANAGEMENT
    // ============================================

    toggleScheduleForm = () => {
        document.getElementById('schedule-form').classList.toggle('hidden');
        if (!document.getElementById('schedule-form').classList.contains('hidden')) {
            document.getElementById('schedule-title').focus();
        }
    };

    handleScheduleSubmit = (e) => {
        e.preventDefault();
        const title = document.getElementById('schedule-title').value;
        const date = document.getElementById('schedule-date').value;
        const time = document.getElementById('schedule-time').value;
        const description = document.getElementById('schedule-description').value;

        if (title.trim() && date && time) {
            const schedule = {
                id: Date.now(),
                title,
                date,
                time,
                description,
                createdAt: new Date().toISOString()
            };

            this.schedules.push(schedule);
            this.saveToStorage();
            this.renderSchedules();
            document.getElementById('schedule-title').value = '';
            document.getElementById('schedule-date').value = '';
            document.getElementById('schedule-time').value = '';
            document.getElementById('schedule-description').value = '';
            this.toggleScheduleForm();
        }
    };

    renderSchedules = () => {
        const scheduleList = document.getElementById('schedule-list');
        
        if (this.schedules.length === 0) {
            scheduleList.innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">Tidak ada jadwal. Tambahkan jadwal baru!</p>';
            return;
        }

        // Sort schedules by date and time
        const sorted = [...this.schedules].sort((a, b) => {
            const dateA = new Date(`${a.date}T${a.time}`);
            const dateB = new Date(`${b.date}T${b.time}`);
            return dateA - dateB;
        });

        // Template literal untuk rendering schedules
        scheduleList.innerHTML = sorted.map(schedule => `
            <div class="item">
                <div class="item-header">
                    <div>
                        <div class="item-title">${this.escapeHtml(schedule.title)}</div>
                    </div>
                </div>
                <div class="item-meta">
                    <span style="background: #dbeafe; color: #1e40af; padding: 0.25rem 0.75rem; border-radius: 0.375rem; font-size: 0.85rem;">
                        📅 ${this.formatDateDisplay(schedule.date)} - ${schedule.time}
                    </span>
                </div>
                ${schedule.description ? `<div class="item-content">${this.escapeHtml(schedule.description)}</div>` : ''}
                <div class="item-actions">
                    <button class="btn btn-primary btn-small" onclick="dashboard.editSchedule(${schedule.id})">Edit</button>
                    <button class="btn btn-danger btn-small" onclick="dashboard.deleteSchedule(${schedule.id})">Hapus</button>
                </div>
            </div>
        `).join('');
    };

    editSchedule = (id) => {
        const schedule = this.schedules.find(s => s.id === id);
        if (schedule) {
            this.editingId = id;
            this.editingType = 'schedule';
            document.getElementById('modal-title').textContent = 'Edit Jadwal';
            document.getElementById('modal-body').innerHTML = `
                <div class="form-group">
                    <label>Judul</label>
                    <input type="text" id="edit-schedule-title" value="${this.escapeHtml(schedule.title)}" required>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Tanggal</label>
                        <input type="date" id="edit-schedule-date" value="${schedule.date}" required>
                    </div>
                    <div class="form-group">
                        <label>Waktu</label>
                        <input type="time" id="edit-schedule-time" value="${schedule.time}" required>
                    </div>
                </div>
                <div class="form-group">
                    <label>Deskripsi</label>
                    <textarea id="edit-schedule-description" rows="3">${this.escapeHtml(schedule.description)}</textarea>
                </div>
            `;
            document.getElementById('edit-modal').classList.remove('hidden');
        }
    };

    deleteSchedule = (id) => {
        if (confirm('Apakah Anda yakin ingin menghapus jadwal ini?')) {
            this.schedules = this.schedules.filter(s => s.id !== id);
            this.saveToStorage();
            this.renderSchedules();
        }
    };

    // ============================================
    // WEATHER MANAGEMENT (Async/Await)
    // ============================================

    fetchWeather = async () => {
        const container = document.getElementById('weather-container');
        container.innerHTML = '<div class="loading">Memuat data cuaca...</div>';

        try {
            // Minta current_weather + hourly relative humidity agar dapat menampilkan kelembaban
            const url = 'https://api.open-meteo.com/v1/forecast?latitude=-6.2088&longitude=106.8456&current_weather=true&hourly=relativehumidity_2m&timezone=Asia/Jakarta';
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error('Gagal mengambil data cuaca');
            }

            const data = await response.json();
            const current = data.current_weather; // current_weather tersedia saat current_weather=true

            // Cari kelembaban pada jam saat ini (zona waktu Asia/Jakarta)
            let humidityDisplay = 'Tidak tersedia';
            if (data.hourly && Array.isArray(data.hourly.time) && Array.isArray(data.hourly.relativehumidity_2m)) {
                // Dapatkan waktu sekarang di zona Asia/Jakarta dalam format YYYY-MM-DDTHH:00
                const nowJakarta = new Date().toLocaleString('sv', { timeZone: 'Asia/Jakarta' }); // "YYYY-MM-DD HH:MM:SS"
                const [datePart, timePart] = nowJakarta.split(' ');
                const hour = timePart.split(':')[0].padStart(2, '0');
                const currentHourKey = `${datePart}T${hour}:00`;
                const idx = data.hourly.time.indexOf(currentHourKey);
                if (idx !== -1) {
                    const rh = data.hourly.relativehumidity_2m[idx];
                    if (typeof rh === 'number') {
                        humidityDisplay = `${rh}%`;
                    }
                }
            }

            // Pastikan field yang digunakan ada, tampilkan fallback jika tidak ada
            const temp = current && typeof current.temperature === 'number' ? Math.round(current.temperature) + '°C' : 'N/A';
            const weatherCode = current && (typeof current.weathercode !== 'undefined' ? current.weathercode : null);
            const wind = current && typeof current.windspeed === 'number' ? current.windspeed + ' km/h' : 'N/A';

            container.innerHTML = `
                <div class="weather-card">
                    <div style="font-size: 3rem;">🌡️</div>
                    <div class="weather-temp">${temp}</div>
                    <div class="weather-description">${this.getWeatherDescription(weatherCode)}</div>
                    <div class="weather-details">
                        <div class="weather-detail">
                            <div class="weather-detail-label">Kelembaban</div>
                            <div class="weather-detail-value">${humidityDisplay}</div>
                        </div>
                        <div class="weather-detail">
                            <div class="weather-detail-label">Kecepatan Angin</div>
                            <div class="weather-detail-value">${wind}</div>
                        </div>
                    </div>
                </div>
            `;
        } catch (error) {
            container.innerHTML = `<div class="error">⚠️ ${error.message}</div>`;
        }
    };

    getWeatherDescription = (code) => {
        const descriptions = {
            0: 'Cerah',
            1: 'Sebagian Berawan',
            2: 'Berawan',
            3: 'Mendung',
            45: 'Berkabut',
            48: 'Berkabut Beku',
            51: 'Gerimis Ringan',
            53: 'Gerimis Sedang',
            55: 'Gerimis Lebat',
            61: 'Hujan Ringan',
            63: 'Hujan Sedang',
            65: 'Hujan Lebat',
            71: 'Salju Ringan',
            73: 'Salju Sedang',
            75: 'Salju Lebat',
            80: 'Hujan Rintik Ringan',
            81: 'Hujan Rintik Sedang',
            82: 'Hujan Rintik Lebat',
            85: 'Salju Rintik Ringan',
            86: 'Salju Rintik Lebat',
            95: 'Badai Petir'
        };
        return descriptions[code] || 'Tidak Diketahui';
    };

    // ============================================
    // MODAL MANAGEMENT
    // ============================================

    handleEditSubmit = (e) => {
        e.preventDefault();

        if (this.editingType === 'task') {
            const task = this.tasks.find(t => t.id === this.editingId);
            if (task) {
                task.title = document.getElementById('edit-task-title').value;
                task.priority = document.getElementById('edit-task-priority').value;
                this.saveToStorage();
                this.renderTasks();
            }
        } else if (this.editingType === 'note') {
            const note = this.notes.find(n => n.id === this.editingId);
            if (note) {
                note.title = document.getElementById('edit-note-title').value;
                note.content = document.getElementById('edit-note-content').value;
                this.saveToStorage();
                this.renderNotes();
            }
        } else if (this.editingType === 'schedule') {
            const schedule = this.schedules.find(s => s.id === this.editingId);
            if (schedule) {
                schedule.title = document.getElementById('edit-schedule-title').value;
                schedule.date = document.getElementById('edit-schedule-date').value;
                schedule.time = document.getElementById('edit-schedule-time').value;
                schedule.description = document.getElementById('edit-schedule-description').value;
                this.saveToStorage();
                this.renderSchedules();
            }
        }

        this.closeModal();
    };

    closeModal = () => {
        document.getElementById('edit-modal').classList.add('hidden');
        this.editingId = null;
        this.editingType = null;
    };

    // ============================================
    // STORAGE MANAGEMENT
    // ============================================

    saveToStorage = () => {
        const data = {
            tasks: this.tasks,
            notes: this.notes,
            schedules: this.schedules
        };
        localStorage.setItem('dashboardData', JSON.stringify(data));
    };

    loadFromStorage = () => {
        const data = localStorage.getItem('dashboardData');
        if (data) {
            const parsed = JSON.parse(data);
            this.tasks = parsed.tasks || [];
            this.notes = parsed.notes || [];
            this.schedules = parsed.schedules || [];
        }
    };

    // ============================================
    // UTILITY FUNCTIONS
    // ============================================

    renderAllItems = () => {
        this.renderTasks();
        this.renderNotes();
        this.renderSchedules();
    };

    getPriorityLabel = (priority) => {
        const labels = {
            low: '🟢 Rendah',
            medium: '🟡 Sedang',
            high: '🔴 Tinggi'
        };
        return labels[priority] || priority;
    };

    formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('id-ID', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    formatDateDisplay = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('id-ID', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric'
        });
    };

    escapeHtml = (text) => {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    };
}

// ============================================
// INITIALIZE DASHBOARD
// ============================================

const dashboard = new DashboardManager();