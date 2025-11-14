const STATUS_TOKENS = {
  "Blocked": { label: "Blocked", icon: "⏸", color: "#c62828" },
  "In Progress": { label: "In progress", icon: "⏳", color: "#1565c0" },
  "Ready for Review": { label: "Ready for review", icon: "👀", color: "#2e7d32" }
};

async function bootstrap() {
  const board = document.getElementById('task-board');
  const template = document.getElementById('task-card-template');
  try {
    const response = await fetch('../data/tasks.json');
    const tasks = await response.json();
    tasks.forEach((task) => {
      const card = template.content.cloneNode(true);
      const article = card.querySelector('.task-card');
      const icon = card.querySelector('.task-icon');
      const status = STATUS_TOKENS[task.status] || { icon: '•', label: task.status, color: '#607d8b' };
      icon.textContent = status.icon || task.icon;
      icon.style.color = status.color;

      card.querySelector('.task-status').textContent = status.label;
      const titleEl = card.querySelector('.task-title');
      titleEl.textContent = task.title;
      titleEl.id = `task-title-${task.id}`;

      const summary = card.querySelector('.task-summary');
      summary.textContent = task.summary;
      summary.setAttribute('aria-describedby', titleEl.id);

      const metaList = card.querySelector('.meta-list');
      metaList.innerHTML = '';
      const details = [
        `Owner: ${task.assignee}`,
        `Due ${task.due_date}`,
        ...task.tags
      ];
      details.forEach((text) => {
        const item = document.createElement('li');
        item.textContent = text;
        metaList.appendChild(item);
      });

      const actions = card.querySelector('.task-actions');
      actions.innerHTML = '';
      const actionMap = [
        { label: 'Open task', kind: 'primary' },
        { label: 'Add note', kind: 'secondary' },
        { label: 'Reassign', kind: 'secondary' }
      ];
      actionMap.forEach(({ label, kind }) => {
        const btn = document.createElement('button');
        btn.className = `btn ${kind}`;
        btn.classList.add(kind === 'primary' ? 'btn-primary' : 'btn-secondary');
        btn.type = 'button';
        btn.textContent = label;
        btn.setAttribute('aria-label', `${label} for ${task.title}`);
        btn.addEventListener('focus', () => article.classList.add('focus'));
        btn.addEventListener('blur', () => article.classList.remove('focus'));
        actions.appendChild(btn);
      });

      board.appendChild(card);
    });
  } catch (error) {
    const alert = document.createElement('p');
    alert.setAttribute('role', 'status');
    alert.textContent = 'Unable to load tasks right now.';
    board.appendChild(alert);
    console.error(error);
  }
}

bootstrap();
