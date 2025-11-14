async function loadTasks() {
  try {
    const response = await fetch('../data/tasks.json');
    const tasks = await response.json();
    renderTasks(tasks);
  } catch (error) {
    console.error('Failed to load tasks', error);
  }
}

function renderTasks(tasks) {
  const board = document.getElementById('task-board');
  board.innerHTML = '';

  tasks.forEach((task) => {
    const card = document.createElement('article');
    card.className = 'task-card';

    const icon = document.createElement('div');
    icon.className = 'task-icon';
    icon.textContent = task.icon;

    const title = document.createElement('h2');
    title.className = 'task-title';
    title.textContent = task.title;

    const meta = document.createElement('div');
    meta.className = 'task-meta';
    meta.textContent = `${task.status} • Owner: ${task.assignee} • Due ${task.due_date}`;

    const summary = document.createElement('p');
    summary.className = 'task-summary';
    summary.textContent = task.summary;

    const tags = document.createElement('div');
    tags.className = 'tag-list';
    task.tags.forEach((tag) => {
      const chip = document.createElement('span');
      chip.textContent = tag.toUpperCase();
      tags.appendChild(chip);
    });

    const actions = document.createElement('div');
    actions.className = 'task-actions';
    ['Open', 'Edit', 'Escalate'].forEach((label, idx) => {
      const button = document.createElement('button');
      button.textContent = label.toUpperCase();
      button.classList.add(idx === 0 ? 'btn-primary' : 'btn-secondary');
      actions.appendChild(button);
    });

    card.appendChild(icon);
    card.appendChild(title);
    card.appendChild(meta);
    card.appendChild(summary);
    card.appendChild(tags);
    card.appendChild(actions);

    board.appendChild(card);
  });
}

loadTasks();
