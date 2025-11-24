# backend/api_endpoint.py - Flask API endpoint to receive form data and trigger report selection

from flask import Flask, request, jsonify  # Import Flask framework and utilities
from flask_cors import CORS  # Import CORS to allow frontend to call backend from different origin
from Report_select import choose_report  # Import the report selection function

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes - allows frontend on different port to access this API

# Define POST endpoint at /api/submit-dog-info to receive form submissions
@app.route('/api/submit-dog-info', methods=['POST'])
def submit_dog_info():
    """
    Receives dog questionnaire data from frontend form,
    calls the report selection logic, and returns the appropriate report.
    """
    try:
        # Get JSON data from request body sent by frontend
        data = request.get_json()
        
        # Extract breed name from submitted data
        breed_name = data.get('breed_name_AKC')
        
        # Extract age (not used in report selection yet, but available for future use)
        age_years = data.get('age_years_preReg')
        
        # Extract diet-related health status array (list of selected checkboxes)
        status_list = data.get('status_dietRelat_preReg', [])
        
        # Validate that required fields are present
        if not breed_name:
            return jsonify({'error': 'Breed name is required'}), 400  # Return error if breed missing
        
        if not status_list:
            return jsonify({'error': 'Please select at least one diet-related status, such as "None apply"'}), 400
        
        # Call the report selection function from Report_select.py
        # Pass the status list and breed name to determine which report to use
        report_message = choose_report(status_list, breed_name)

# TODO: Insert data into database (questions_dog_initial3 table)        
    # TODO: Insert data into database (questions_dog_initial3 table)    
        # TODO: Insert data into database (questions_dog_initial3 table)
        # This is where you would add code to save the form data to your PostgreSQL database
        
        # Return success response with the selected report message
        return jsonify({
            'success': True,
            'message': 'Dog information submitted successfully!',
            'report': report_message,  # The report selection result
            'breed': breed_name,
            'age': age_years,
            'statuses': status_list
        }), 200  # HTTP 200 = success
        
    except Exception as e:
        # Catch any errors and return error response
        return jsonify({
            'success': False,
            'error': str(e)  # Return error message
        }), 500  # HTTP 500 = internal server error

# Main entry point - run the Flask server
if __name__ == '__main__':
    # Start Flask development server
    # host='0.0.0.0' makes it accessible from other devices on network
    # port=5000 is the default Flask port
    # debug=True enables auto-reload and detailed error messages
    app.run(host='0.0.0.0', port=5000, debug=True)
