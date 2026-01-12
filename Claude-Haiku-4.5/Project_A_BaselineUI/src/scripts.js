// Baseline UI JavaScript - Minimal functionality
document.addEventListener('DOMContentLoaded', function() {
    // Basic task card interactions
    const taskCards = document.querySelectorAll('.task-card');
    const addTaskBtn = document.querySelector('.header-actions .btn-primary');
    
    // Add click logging for testing purposes
    taskCards.forEach(card => {
        card.addEventListener('click', function(e) {
            if (!e.target.closest('.task-actions')) {
                console.log('Task card clicked:', card.querySelector('.task-title').textContent);
            }
        });
    });
    
    // Button click handlers
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-sm')) {
            const action = e.target.textContent.toLowerCase();
            const taskCard = e.target.closest('.task-card');
            const taskTitle = taskCard.querySelector('.task-title').textContent;
            
            console.log(`${action} clicked for task: ${taskTitle}`);
            
            if (action === 'delete') {
                if (confirm(`Are you sure you want to delete "${taskTitle}"?`)) {
                    taskCard.style.opacity = '0.5';
                    setTimeout(() => {
                        taskCard.remove();
                    }, 300);
                }
            }
        }
    });
    
    // Add task functionality
    if (addTaskBtn) {
        addTaskBtn.addEventListener('click', function() {
            console.log('Add task clicked');
            alert('Add task functionality would open a modal or form');
        });
    }
    
    // Filter functionality
    const filterBtn = document.querySelector('.btn-secondary');
    if (filterBtn) {
        filterBtn.addEventListener('click', function() {
            console.log('Filter clicked');
            alert('Filter functionality would show/hide tasks based on criteria');
        });
    }
    
    // Progress bar animations
    const progressBars = document.querySelectorAll('.progress-fill');
    setTimeout(() => {
        progressBars.forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = width;
            }, 100);
        });
    }, 500);
});