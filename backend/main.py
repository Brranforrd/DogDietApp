# backend/main.py - Flask API endpoint to receive form data and trigger report selection

from flask import Flask, request, jsonify  # Import Flask framework and utilities
from flask_cors import CORS  # Import CORS to allow frontend to call backend from different origin
from Report_select import choose_report  # Import the report selection function

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes - allows frontend on different port to access this API


# ==================== GET ROUTES - Retrieve Data ====================

@app.route('/api/breeds', methods=['GET'])
def get_all_breeds():
    """
    GET endpoint to retrieve all breeds from database.
    Returns list of all breeds in breeds_AKC_Rsrch_FoodV1 table.
    """
    try:
        # TODO: Connect to database and fetch all breeds
        # Example query: SELECT * FROM breeds_AKC_Rsrch_FoodV1
        
        # Placeholder response - replace with actual database query
        return jsonify({
            'success': True,
            'message': 'Retrieved all breeds',
            'breeds': []  # Will contain list of breed objects from database
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/breed/<search_field>/<search_value>', methods=['GET'])
def get_breed(search_field, search_value):
    """
    GET endpoint to retrieve a specific breed by breed_name_AKC or dogapi_id.
    URL parameters:
        search_field: either 'breed_name_AKC' or 'dogapi_id'
        search_value: the actual breed name or ID to search for
    """
    try:
        # Validate search field
        if search_field not in ['breed_name_AKC', 'dogapi_id']:
            return jsonify({'error': 'Invalid search field. Use breed_name_AKC or dogapi_id'}), 400
        
        # TODO: Connect to database and fetch specific breed
        # Example query: SELECT * FROM breeds_AKC_Rsrch_FoodV1 WHERE {search_field} = {search_value}
        
        # Placeholder response - replace with actual database query
        return jsonify({
            'success': True,
            'message': f'Retrieved breed by {search_field}',
            'breed': {}  # Will contain breed object from database
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== POST ROUTES - Create New Data ====================

@app.route('/api/submit-dog-info', methods=['POST'])
def submit_dog_info():
    """
    POST endpoint - Receives dog questionnaire data from frontend form,
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
        # This is where you would add code to save the form data to your PostgreSQL database
        # Example: INSERT INTO questions_dog_initial3 (breed_name_AKC, age_years_preReg, status_dietRelat_preReg) VALUES (...)
        
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


@app.route('/api/breed', methods=['POST'])
def create_breed():
    """
    POST endpoint to create a new breed record in breeds_AKC_Rsrch_FoodV1 table.
    Requires all necessary breed information in request body.
    """
    try:
        data = request.get_json()  # Get JSON data from request
        
        # Validate required field
        if not data.get('breed_name_AKC'):
            return jsonify({'error': 'breed_name_AKC is required'}), 400
        
        # TODO: Insert new breed into database
        # Example: INSERT INTO breeds_AKC_Rsrch_FoodV1 (...) VALUES (...)
        
        return jsonify({
            'success': True,
            'message': 'Breed created successfully',
            'breed': data.get('breed_name_AKC')
        }), 201  # HTTP 201 = created
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== PATCH ROUTES - Partial Update ====================

@app.route('/api/breed/<search_field>/<search_value>', methods=['PATCH'])
def update_breed_partial(search_field, search_value):
    """
    PATCH endpoint for partial updates to breed information.
    Only updates fields that are provided in request body.
    URL parameters:
        search_field: either 'breed_name_AKC' or 'dogapi_id'
        search_value: the actual breed name or ID to search for
    """
    try:
        # Validate search field
        if search_field not in ['breed_name_AKC', 'dogapi_id']:
            return jsonify({'error': 'Invalid search field. Use breed_name_AKC or dogapi_id'}), 400
        
        data = request.get_json()  # Get update data from request body
        
        # Check if there's data to update
        if not data:
            return jsonify({'error': 'No update data provided'}), 400
        
        # TODO: Update breed in database - only update provided fields
        # Example: UPDATE breeds_AKC_Rsrch_FoodV1 SET field1=value1, field2=value2 WHERE {search_field} = {search_value}
        
        # Build list of fields being updated (for response message)
        updated_fields = list(data.keys())
        
        return jsonify({
            'success': True,
            'message': f'Breed updated successfully via {search_field}',
            'updated_fields': updated_fields,
            'search_value': search_value
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== PUT ROUTES - Full Update/Replace ====================

@app.route('/api/breed/<search_field>/<search_value>', methods=['PUT'])
def update_breed_full(search_field, search_value):
    """
    PUT endpoint for full replacement of breed information.
    Requires all fields to be provided - replaces entire record.
    URL parameters:
        search_field: either 'breed_name_AKC' or 'dogapi_id'
        search_value: the actual breed name or ID to search for
    """
    try:
        # Validate search field
        if search_field not in ['breed_name_AKC', 'dogapi_id']:
            return jsonify({'error': 'Invalid search field. Use breed_name_AKC or dogapi_id'}), 400
        
        data = request.get_json()  # Get full breed data from request body
        
        # Validate that required fields are present for full update
        required_fields = ['breed_name_AKC', 'breed_group_AKC', 'breed_size_categ_AKC']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields for PUT: {", ".join(missing_fields)}'
            }), 400
        
        # TODO: Replace breed record in database with new data
        # Example: UPDATE breeds_AKC_Rsrch_FoodV1 SET (all fields) WHERE {search_field} = {search_value}
        
        return jsonify({
            'success': True,
            'message': f'Breed fully replaced successfully via {search_field}',
            'search_value': search_value
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== DELETE ROUTE (Optional) ====================

@app.route('/api/breed/<search_field>/<search_value>', methods=['DELETE'])
def delete_breed(search_field, search_value):
    """
    DELETE endpoint to remove a breed from the database.
    URL parameters:
        search_field: either 'breed_name_AKC' or 'dogapi_id'
        search_value: the actual breed name or ID to delete
    """
    try:
        # Validate search field
        if search_field not in ['breed_name_AKC', 'dogapi_id']:
            return jsonify({'error': 'Invalid search field. Use breed_name_AKC or dogapi_id'}), 400
        
        # TODO: Delete breed from database
        # Example: DELETE FROM breeds_AKC_Rsrch_FoodV1 WHERE {search_field} = {search_value}
        
        return jsonify({
            'success': True,
            'message': f'Breed deleted successfully',
            'deleted': search_value
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Server Entry Point ====================

# Main entry point - run the Flask server
if __name__ == '__main__':
    # Start Flask development server
    # host='0.0.0.0' makes it accessible from other devices on network
    # port=5000 is the default Flask port
    # debug=True enables auto-reload and detailed error messages
    app.run(host='0.0.0.0', port=5000, debug=True)
