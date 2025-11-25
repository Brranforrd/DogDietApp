
# backend/services/report_service.py - Selects appropriate report based on user selections of age-class and health issues.

def choose_report(status_dietRelat_preReg, breed):  # Function takes list of health statuses and breed name as inputs
    """
    Determines which report/recommendation to provide based on dog's health status.
    
    Args:
        status_dietRelat_preReg: List of diet-related health statuses (e.g., ['none'], ['puppy', 'allergy'])
        breed: Dog breed name (e.g., 'Labrador Retriever')
    
    Returns:
        String message indicating which type of report/recommendation to provide
    """
    # Normalize text (optional but helpful for beginners)
    status_dietRelat_preReg = [s.lower() for s in status_dietRelat_preReg]  # Convert all selections to lowercase for consistent comparison
    
    # Condition 1: Only none/puppy
    allowed = {"none", "puppy"}  # Define which selections count as "basic" (no special health concerns)
    if set(status_dietRelat_preReg).issubset(allowed):  # Check if ALL selections are only "none" and/or "puppy"
        report_name = "Report_basic_foodP1"  # Assign report name for tracking/logging
        return f"Info related to puppy or adult food for {breed}"  # Return basic nutrition report message
    
    # Condition 2: Any other health issues AT ALL
    report_name = "Report_enhanced_vet"  # Assign report name for special dietary needs - "Report... adjusted; targeted; advanced
    return f"Info related to health issues and/or pregnant female or senior"  # Return special health report message


# Example Use
# print(choose_report(["puppy"], "Labrador"))
# # → Info related to puppy or adult food for Labrador (Basic_NutritionReport)
# print(choose_report(["puppy", "pregnant"], "Husky"))
# # → Info related to health issues and/or pregnant female or senior (SpecialNeeds_HealthReport)
