// Improved UI JavaScript - Enhanced functionality with accessibility
document.addEventListener('DOMContentLoaded', function() {
    // Enhanced task card interactions with keyboard support
    const taskCards = document.querySelectorAll('.task-card');
    const addTaskBtn = document.querySelector('.header-actions .btn-primary');
    
    // Add enhanced click and keyboard logging for testing purposes
    taskCards.forEach((card, index) => {
        card.addEventListener('click', function(e) {
            if (!e.target.closest('.task-actions')) {
                console.log('Task card clicked:', card.querySelector('.task-title').textContent);
                // Focus management for accessibility
                card.focus();
            }
        });
        
        // Keyboard navigation support
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                console.log('Task card activated via keyboard:', card.querySelector('.task-title').textContent);
                // Could open task details or edit mode
            }
            
            // Arrow key navigation
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                const nextCard = taskCards[index + 1];
                if (nextCard) {
                    nextCard.focus();
                }
            }
            
            if (e.key === 'ArrowUp') {
                e.preventDefault();
                const prevCard = taskCards[index - 1];
                if (prevCard) {
                    prevCard.focus();
                }
            }
        });
    });
    
    // Enhanced button click handlers with improved feedback
    document.addEventListener('click', function(e) {
        if (e.target.closest('.btn-sm')) {
            const button = e.target.closest('.btn-sm');
            const action = button.textContent.trim().toLowerCase();
            const taskCard = button.closest('.task-card');
            const taskTitle = taskCard.querySelector('.task-title').textContent;
            
            console.log(`${action} clicked for task: ${taskTitle}`);
            
            // Add visual feedback
            button.style.transform = 'scale(0.95)';
            setTimeout(() => {
                button.style.transform = '';
            }, 150);
            
            if (action.includes('delete')) {
                if (confirm(`Are you sure you want to delete "${taskTitle}"?`)) {
                    // Enhanced deletion animation
                    taskCard.style.transform = 'translateX(-100%)';
                    taskCard.style.opacity = '0';
                    taskCard.setAttribute('aria-hidden', 'true');
                    
                    setTimeout(() => {
                        taskCard.remove();
                        // Announce to screen readers
                        announceToScreenReader(`Task "${taskTitle}" has been deleted`);
                    }, 300);
                }
            } else if (action.includes('edit')) {
                // Focus on the task card for edit mode
                taskCard.focus();
                announceToScreenReader(`Editing task: ${taskTitle}`);
            }
        }
    });
    
    // Enhanced add task functionality
    if (addTaskBtn) {
        addTaskBtn.addEventListener('click', function() {
            console.log('Add task clicked');
            announceToScreenReader('Opening add task form');
            // In a real app, this would open a modal or navigate to a form
            alert('Add task functionality would open an accessible modal or form');
        });
    }
    
    // Enhanced filter functionality
    const filterBtn = document.querySelector('.btn-secondary');
    if (filterBtn) {
        filterBtn.addEventListener('click', function() {
            console.log('Filter clicked');
            announceToScreenReader('Opening filter options');
            // In a real app, this would show filter controls
            alert('Filter functionality would show accessible filter controls');
        });
    }
    
    // Enhanced progress bar animations with accessibility considerations
    const progressBars = document.querySelectorAll('.progress-fill');
    setTimeout(() => {
        progressBars.forEach(bar => {
            const width = bar.style.width;
            const progressBar = bar.closest('.progress-bar');
            const ariaValueNow = progressBar.getAttribute('aria-valuenow');
            
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = width;
                // Announce progress to screen readers if significant
                if (parseInt(ariaValueNow) >= 75) {
                    setTimeout(() => {
                        announceToScreenReader(`Task nearly complete at ${ariaValueNow}%`);
                    }, 1000);
                }
            }, 100);
        });
    }, 500);
    
    // Utility function to announce to screen readers
    function announceToScreenReader(message) {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.style.position = 'absolute';
        announcement.style.left = '-10000px';
        announcement.style.width = '1px';
        announcement.style.height = '1px';
        announcement.style.overflow = 'hidden';
        document.body.appendChild(announcement);
        
        announcement.textContent = message;
        
        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    }
    
    // Enhanced keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Global shortcuts
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 'n':
                    e.preventDefault();
                    addTaskBtn.click();
                    break;
                case 'f':
                    e.preventDefault();
                    filterBtn.click();
                    break;
            }
        }
        
        // Escape to clear focus
        if (e.key === 'Escape') {
            document.activeElement.blur();
        }
    });
    
    // Enhanced hover effects for better affordance
    const interactiveElements = document.querySelectorAll('button, .task-card');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            if (this.classList.contains('task-card')) {
                console.log('Task card hovered:', this.querySelector('.task-title').textContent);
            }
        });
    });
    
    // Initialize ARIA live regions for dynamic content
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.id = 'live-announcements';
    liveRegion.style.position = 'absolute';
    liveRegion.style.left = '-10000px';
    document.body.appendChild(liveRegion);
    
    // Announce initial page load
    setTimeout(() => {
        announceToScreenReader(`Task list loaded with ${taskCards.length} tasks`);
    }, 1000);
});