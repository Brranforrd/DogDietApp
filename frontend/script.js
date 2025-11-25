// Frontend form handlers for DogDietApp

const form = document.getElementById('dogQuestionnaireForm');

// Add event listener for form submission (only if the form exists on the page)
if (form) {
    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent default form submission (page reload)
        
        // Collect form data
        const formData = new FormData(form);
        
        // Get all checked status values (since multiple checkboxes allowed)
        const statusValues = formData.getAll('status_dietRelat_preReg');
        
        // Build data object to send to backend
        const dogData = {
            breed_name_AKC: formData.get('breed_name_AKC'), // Get breed name
            age_years_preReg: parseFloat(formData.get('age_years_preReg')), // Convert age to number
            status_dietRelat_preReg: statusValues // Array of selected statuses
        };
        
        try {
            // Send POST request to backend API endpoint
            const response = await fetch('/api/submit-dog-info', {
                method: 'POST', // HTTP POST method
                headers: {
                    'Content-Type': 'application/json' // Sending JSON data
                },
                body: JSON.stringify(dogData) // Convert data object to JSON string
            });
            
            // Check if request was successful
            if (response.ok) {
                const result = await response.json(); // Parse JSON response
                alert('Success! ' + result.message); // Show success message to user
                // Optionally display the report or redirect to report page
                console.log('Report:', result.report); // Log report to console
            } else {
                // Handle error response
                const error = await response.json();
                alert('Error: ' + error.message); // Show error to user
            }
        } catch (error) {
            // Handle network or other errors
            console.error('Error submitting form:', error);
            alert('Failed to submit form. Please try again.');
        }
    });
}