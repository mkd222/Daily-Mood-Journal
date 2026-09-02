

// Script only runs after HTML is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 3000);
    });

    // Form validation mood entry
    const moodForm = document.querySelector('#mood-form'); 
    if (moodForm) {
        moodForm.addEventListener('submit', function(e) {
            const moodSelect = document.querySelector('#mood');
            if (moodSelect?.value === '') {
                e.preventDefault();
                alert('Please select a mood before submitting.');
            }
        });
    }

    // Character counter for journal and gratitude entries
    const textareas = document.querySelectorAll('textarea[id="journal_entry"], textarea[id="content"]');
    textareas.forEach(textarea => {
        // Create counter after user starts typing
        const counter = document.createElement('small');
        counter.classList.add('char-counter', 'text-muted');
        textarea.parentNode.insertBefore(counter, textarea.nextSibling);
        
        // Update counter on input
        textarea.addEventListener('input', function() {
            const maxLength = 500;
            const remaining = maxLength - this.value.length;
            counter.textContent = `${remaining} characters remaining`;
            counter.classList.toggle('text-danger', remaining < 50);
        });
        
        
        counter.textContent = `500 characters remaining`;
    });

    
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', () => 
            navbarCollapse.classList.toggle('show')
        );

        document.addEventListener('click', ({target}) => {
            if (!navbarToggler.contains(target) && !navbarCollapse.contains(target)) {
                navbarCollapse.classList.remove('show');
            }
        });
    }
});