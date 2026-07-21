// Run the code after the page loads completely

window.onload = function() {

    // 1. Date Validation (Prevent picking past dates)
    const today = new Date().toISOString().split('T')[0];
    
    // Apply to search form
    const searchDateInput = document.querySelector('input[name="date"]');
    if (searchDateInput) {
        searchDateInput.setAttribute('min', today);
    }


    // Apply to all edit forms 
    const updateInputs = document.querySelectorAll('.future-date-only');
    for (let i = 0; i < updateInputs.length; i++) {
        updateInputs[i].setAttribute('min', today);
    }

    // 2. Time Validation Logic (Start time must be before End time)
    function setupTimeSync(startDropdown, endDropdown) {
        if (startDropdown && endDropdown) {
            
            // Using onchange 
            startDropdown.onchange = function() {
                const startIndex = this.selectedIndex;
                const endOptions = endDropdown.options;
                
                // Loop through end time options to disable past times
                for (let j = 0; j < endOptions.length; j++) {
                    if (j < startIndex) {
                        endOptions[j].disabled = true;
                        endOptions[j].style.display = 'none';
                    } else {
                        endOptions[j].disabled = false;
                        endOptions[j].style.display = 'block';
                    }
                }
                
                // Push end time forward if it conflicts
                if (endDropdown.selectedIndex < startIndex) {
                    endDropdown.selectedIndex = startIndex;
                }
            };
            
            // Trigger the change event manually on load to set initial state
            startDropdown.onchange();
        }
    }

    // Apply time logic to the Search Page
    const mainStart = document.getElementById('start_time_select');
    const mainEnd = document.getElementById('end_time_select');
    setupTimeSync(mainStart, mainEnd);

    // Apply time logic to the Dashboard Edit Forms
    const editForms = document.querySelectorAll('.edit-form');
    for (let k = 0; k < editForms.length; k++) {
        const editStart = editForms[k].querySelector('.edit-start');
        const editEnd = editForms[k].querySelector('.edit-end');
        setupTimeSync(editStart, editEnd);
    }

};


function savePreferenceAndRedirect(spaceType) {
    localStorage.setItem('selectedSpaceType', spaceType);
    window.location.href = "/rooms";
}