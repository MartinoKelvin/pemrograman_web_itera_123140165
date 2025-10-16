let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

const form = document.getElementById('taskForm');
const taskList = document.getElementById('taskList');
const taskStats = document.getElementById('taskStats');
const filterStatus = document.getElementById('filterStatus');
const filterCourse = document.getElementById('filterCourse');
const emptyState = document.getElementById('emptyState');
const deleteModal = document.getElementById('deleteModal');
const cancelDelete = document.getElementById('cancelDelete');
const confirmDelete = document.getElementById('confirmDelete');

let taskToDelete = null;

function saveTasks() {
  localStorage.setItem('tasks', JSON.stringify(tasks));
}

function formatDate(dateString) {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('id-ID', options);
}

function isOverdue(deadline) {
  const today = new Date();
  const deadlineDate = new Date(deadline);
  return deadlineDate < today;
}

function getPriorityClass(priority) {
  switch(priority) {
    case 'high': return 'priority-high';
    case 'medium': return 'priority-medium';
    case 'low': return 'priority-low';
    default: return '';
  }
}

function getPriorityIcon(priority) {
  switch(priority) {
    case 'high': return '<i class="fas fa-exclamation-circle text-red-500"></i>';
    case 'medium': return '<i class="fas fa-exclamation-triangle text-yellow-500"></i>';
    case 'low': return '<i class="fas fa-info-circle text-green-500"></i>';
    default: return '';
  }
}

function renderTasks() {
  taskList.innerHTML = '';
  const filtered = tasks.filter(t => {
    const byStatus = filterStatus.value === 'all' || 
      (filterStatus.value === 'done' && t.done) || 
      (filterStatus.value === 'pending' && !t.done);
    const byCourse = t.course.toLowerCase().includes(filterCourse.value.toLowerCase());
    return byStatus && byCourse;
  });

  if (filtered.length === 0) {
    emptyState.classList.remove('hidden');
  } else {
    emptyState.classList.add('hidden');
    
    filtered.forEach((t, i) => {
      const div = document.createElement('div');
      div.className = `task-item bg-white border rounded-lg p-4 ${getPriorityClass(t.priority)} ${t.done ? 'opacity-75' : ''} fade-in`;
      
      const isOverdueFlag = !t.done && isOverdue(t.deadline);
      
      div.innerHTML = `
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1">
              ${getPriorityIcon(t.priority)}
              <p class="${t.done ? 'line-through text-gray-500' : 'font-semibold text-gray-800'}">${t.name}</p>
            </div>
            <div class="flex flex-wrap gap-2 text-sm text-gray-600">
              <span class="bg-indigo-100 text-indigo-800 px-2 py-1 rounded">${t.course}</span>
              <span class="${isOverdueFlag ? 'text-red-600 font-medium' : ''}">
                <i class="far fa-calendar-alt"></i> ${formatDate(t.deadline)}
                ${isOverdueFlag ? ' (Terlambat!)' : ''}
              </span>
              ${t.done ? '<span class="bg-green-100 text-green-800 px-2 py-1 rounded"><i class="fas fa-check-circle"></i> Selesai</span>' : ''}
            </div>
          </div>
          <div class="flex gap-2 ml-4">
            <button onclick="toggleTask(${tasks.indexOf(t)})" class="text-green-600 hover:text-green-800 transition p-2 rounded-full hover:bg-green-100" title="${t.done ? 'Tandai belum selesai' : 'Tandai selesai'}">
              <i class="fas ${t.done ? 'fa-undo' : 'fa-check'}"></i>
            </button>
            <button onclick="showDeleteModal(${tasks.indexOf(t)})" class="text-red-500 hover:text-red-700 transition p-2 rounded-full hover:bg-red-100" title="Hapus tugas">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
      `;
      taskList.appendChild(div);
    });
  }

  updateStats();
}

function updateStats() {
  const totalTasks = tasks.length;
  const doneTasks = tasks.filter(t => t.done).length;
  const pendingTasks = totalTasks - doneTasks;
  const overdueTasks = tasks.filter(t => !t.done && isOverdue(t.deadline)).length;
  
  taskStats.innerHTML = `
    <div class="bg-indigo-50 rounded-lg p-4 text-center">
      <div class="text-3xl font-bold text-indigo-600">${totalTasks}</div>
      <div class="text-gray-600">Total Tugas</div>
    </div>
    <div class="bg-green-50 rounded-lg p-4 text-center">
      <div class="text-3xl font-bold text-green-600">${doneTasks}</div>
      <div class="text-gray-600">Selesai</div>
    </div>
    <div class="bg-yellow-50 rounded-lg p-4 text-center">
      <div class="text-3xl font-bold text-yellow-600">${pendingTasks}</div>
      <div class="text-gray-600">Belum Selesai</div>
    </div>
    ${overdueTasks > 0 ? `
    <div class="bg-red-50 rounded-lg p-4 text-center">
      <div class="text-3xl font-bold text-red-600">${overdueTasks}</div>
      <div class="text-gray-600">Terlambat</div>
    </div>
    ` : ''}
  `;
}

form.addEventListener('submit', e => {
  e.preventDefault();
  const name = document.getElementById('taskName').value.trim();
  const course = document.getElementById('taskCourse').value.trim();
  const deadline = document.getElementById('taskDeadline').value;
  const priority = document.getElementById('taskPriority').value;

  if (!name || !course || !deadline) {
    showNotification('Semua field wajib diisi!', 'error');
    return;
  }

  tasks.push({ name, course, deadline, done: false, priority });
  saveTasks();
  renderTasks();
  form.reset();
  showNotification('Tugas berhasil ditambahkan!', 'success');
});

function toggleTask(index) {
  tasks[index].done = !tasks[index].done;
  saveTasks();
  renderTasks();
  showNotification(tasks[index].done ? 'Tugas ditandai selesai!' : 'Tugas ditandai belum selesai!', 'success');
}

function showDeleteModal(index) {
  taskToDelete = index;
  deleteModal.classList.remove('hidden');
}

function deleteTask() {
  if (taskToDelete !== null) {
    tasks.splice(taskToDelete, 1);
    saveTasks();
    renderTasks();
    deleteModal.classList.add('hidden');
    taskToDelete = null;
    showNotification('Tugas berhasil dihapus!', 'success');
  }
}

filterStatus.addEventListener('change', renderTasks);
filterCourse.addEventListener('input', renderTasks);

cancelDelete.addEventListener('click', () => {
  deleteModal.classList.add('hidden');
  taskToDelete = null;
});

confirmDelete.addEventListener('click', deleteTask);

deleteModal.addEventListener('click', (e) => {
  if (e.target === deleteModal) {
    deleteModal.classList.add('hidden');
    taskToDelete = null;
  }
});

function showNotification(message, type) {
  const notification = document.createElement('div');
  notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg text-white fade-in z-50 ${
    type === 'success' ? 'bg-green-500' : 'bg-red-500'
  }`;
  notification.innerHTML = `
    <div class="flex items-center gap-2">
      <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
      <span>${message}</span>
    </div>
  `;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.style.opacity = '0';
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 300);
  }, 3000);
}

document.getElementById('taskDeadline').min = new Date().toISOString().split('T')[0];

renderTasks();