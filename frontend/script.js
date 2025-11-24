// Frontend form handlers for DogDietApp

const form = document.getElementById('dogQuestionnaireForm');
// Add event listener for form submission (only if the form exists on the page)
if (form) {
    form.addEventListener('submit', async function (event) {
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
            // Send POST request to backend API endpoint
            const response = await fetch('/api/submit-dog-info', {
                method: 'POST', // HTTP POST method
                // Check if request was successful
                if (response.ok) {
                    const result = await response.json(); // Parse JSON response
                } else {
                    // Handle error response
                    const error = await response.json();
            } catch (error) {
                // Handle network or other errors
                console.error('Error submitting form:', error);


// Only attach handler if the admin form exists on the page
if (adminForm) {
    adminForm.addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData(adminForm);
    const searchField = formData.get('search_field'); // Get which field to search by
    const searchValue = formData.get('search_value'); // Get the search value

    // Build update data object - only include non-empty fields
    const updateData = {};
    for (let [key, value] of formData.entries()) {
            // Skip search fields and empty values
            if (key !== 'search_field' && key !== 'search_value' && value !== '') {
                updateData[key] = value; // Add non-empty field to update object
        // Check if there's anything to update
        if (Object.keys(updateData).length === 0) {
            alert('Please fill in at least one field to update.');
        try {
            // Send PATCH request to backend API endpoint
            // URL includes search field and value as query parameters
            if (response.ok) {
                const result = await response.json(); // Parse JSON response
                alert('Success! Breed information updated.'); // Show success message
            } else {
                const error = await response.json();
                alert('Error: ' + (error.error || 'Update failed')); // Show error message
            console.error('Error updating breed:', error);
            alert('Failed to update breed information. Please try again.');
        }
    });
}
const form = document.getElementById('dogQuestionnaireForm');
        
        // Add event listener for form submission
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

        // Admin form submission handler
        const adminForm = document.getElementById('adminUpdateForm');
        
        adminForm.addEventListener('submit', async function(event) {
            event.preventDefault(); // Prevent default form submission
            
            const formData = new FormData(adminForm);
            const searchField = formData.get('search_field'); // Get which field to search by
            const searchValue = formData.get('search_value'); // Get the search value
            
            // Build update data object - only include non-empty fields
            const updateData = {};
            for (let [key, value] of formData.entries()) {
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

                // Admin form submission handler
                const adminForm = document.getElementById('adminUpdateForm');

                // Only attach handler if the admin form exists on the page
                if (adminForm) {
                    adminForm.addEventListener('submit', async function(event) {
                        event.preventDefault(); // Prevent default form submission

                        const formData = new FormData(adminForm);
                        const searchField = formData.get('search_field'); // Get which field to search by
                        const searchValue = formData.get('search_value'); // Get the search value

                        // Build update data object - only include non-empty fields
                        const updateData = {};
                        for (let [key, value] of formData.entries()) {
                            // Skip search fields and empty values
                            if (key !== 'search_field' && key !== 'search_value' && value !== '') {
                                updateData[key] = value; // Add non-empty field to update object
                            }
                        }

                        // Check if there's anything to update
                        if (Object.keys(updateData).length === 0) {
                            alert('Please fill in at least one field to update.');
                            return;
                        }

                        try {
                            // Send PATCH request to backend API endpoint
                            // URL includes search field and value as query parameters
                            const response = await fetch(`/api/breed/${searchField}/${encodeURIComponent(searchValue)}`, {
                                method: 'PATCH', // HTTP PATCH method for partial updates
                                headers: {
                                    'Content-Type': 'application/json' // Sending JSON data
                                },
                                body: JSON.stringify(updateData) // Convert update data to JSON
                            });

                            if (response.ok) {
                                const result = await response.json(); // Parse JSON response
                                alert('Success! Breed information updated.'); // Show success message
                                adminForm.reset(); // Clear the form after successful update
                            } else {
                                const error = await response.json();
                                alert('Error: ' + (error.error || 'Update failed')); // Show error message
                            }
                        } catch (error) {
                            console.error('Error updating breed:', error);
                            alert('Failed to update breed information. Please try again.');
                        }
                    });
                }