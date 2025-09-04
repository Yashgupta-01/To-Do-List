document.addEventListener('DOMContentLoaded', function() {
    const dueDateInputs = document.querySelectorAll('input[type="date"]');
    dueDateInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            const value = e.target.value;
            if (value && !/^\d{4}-\d{2}-\d{2}$/.test(value)) {
                e.target.setCustomValidity('Please enter a date in YYYY-MM-DD format or leave empty.');
            } else {
                e.target.setCustomValidity('');
            }
        });
    });
});