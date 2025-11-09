"""
AbilityPath Programs Database
This simulates the 15+ programs that AbilityPath offers.
In production, this would be stored in a real database (PostgreSQL, etc.)
"""

PROGRAMS = [
    {
        "id": "early_intervention",
        "name": "Early Intervention Services",
        "description": "Support for infants and toddlers (0-3 years) with developmental delays",
        "age_range": [0, 3],
        "eligibility_criteria": {
            "developmental_delay": True,
            "requires_mobility_support": None,  # None means not required
            "requires_behavioral_support": None,
        },
        "benefits": [
            "Speech therapy",
            "Occupational therapy",
            "Developmental assessments",
            "Family support services"
        ]
    },
    {
        "id": "preschool_program",
        "name": "Inclusive Preschool Program",
        "description": "Educational program for children ages 3-5 with developmental needs",
        "age_range": [3, 5],
        "eligibility_criteria": {
            "developmental_delay": True,
            "requires_social_skills_support": True,
        },
        "benefits": [
            "Inclusive classroom environment",
            "Individualized education plans",
            "Social skills development",
            "Peer interaction opportunities"
        ]
    },
    {
        "id": "school_age_support",
        "name": "School-Age Support Services",
        "description": "After-school and weekend programs for children 6-17",
        "age_range": [6, 17],
        "eligibility_criteria": {
            "requires_behavioral_support": True,
        },
        "benefits": [
            "Social recreation activities",
            "Behavioral support",
            "Homework help",
            "Community integration"
        ]
    },
    {
        "id": "transition_services",
        "name": "Transition to Adulthood Services",
        "description": "Support for young adults transitioning from school to adult services",
        "age_range": [18, 22],
        "eligibility_criteria": {
            "recently_graduated": True,
        },
        "benefits": [
            "Job skills training",
            "Independent living skills",
            "Career exploration",
            "Adult service navigation"
        ]
    },
    {
        "id": "adult_day_program",
        "name": "Adult Day Program",
        "description": "Daytime activities and support for adults with developmental disabilities",
        "age_range": [22, 120],
        "eligibility_criteria": {
            "needs_daytime_support": True,
            "can_participate_in_groups": True,
        },
        "benefits": [
            "Structured daily activities",
            "Social engagement",
            "Community outings",
            "Skills development"
        ]
    },
    {
        "id": "vocational_training",
        "name": "Vocational Training & Employment Services",
        "description": "Job training and placement services for adults",
        "age_range": [18, 120],
        "eligibility_criteria": {
            "seeking_employment": True,
            "can_work_with_support": True,
        },
        "benefits": [
            "Job skills training",
            "Resume building",
            "Interview preparation",
            "Job placement assistance",
            "On-site job coaching"
        ]
    },
    {
        "id": "supported_living",
        "name": "Supported Independent Living",
        "description": "Support for adults living independently in the community",
        "age_range": [22, 120],
        "eligibility_criteria": {
            "lives_independently": True,
            "needs_ongoing_support": True,
        },
        "benefits": [
            "Life skills training",
            "Budgeting support",
            "Healthcare coordination",
            "24/7 emergency support"
        ]
    },
    {
        "id": "behavioral_services",
        "name": "Intensive Behavioral Support Services",
        "description": "Specialized support for individuals with challenging behaviors",
        "age_range": [3, 120],
        "eligibility_criteria": {
            "has_challenging_behaviors": True,
            "needs_intensive_support": True,
        },
        "benefits": [
            "Behavior assessment",
            "Individualized behavior plans",
            "One-on-one support",
            "Family training"
        ]
    },
    {
        "id": "respite_care",
        "name": "Respite Care Services",
        "description": "Temporary relief care for family caregivers",
        "age_range": [0, 120],
        "eligibility_criteria": {
            "has_family_caregiver": True,
        },
        "benefits": [
            "In-home respite care",
            "Weekend programs",
            "Emergency backup care",
            "Caregiver support"
        ]
    },
    {
        "id": "social_recreation",
        "name": "Social Recreation Programs",
        "description": "Evening and weekend social activities for all ages",
        "age_range": [6, 120],
        "eligibility_criteria": {
            "seeks_social_activities": True,
        },
        "benefits": [
            "Sports and fitness activities",
            "Arts and crafts",
            "Community outings",
            "Social clubs"
        ]
    }
]


def get_all_programs():
    """Return all available programs"""
    return PROGRAMS


def filter_programs_by_criteria(age, user_needs):
    """
    Filter programs based on age and user needs
    
    Args:
        age: User's age in years
        user_needs: Dictionary of user needs/characteristics
        
    Returns:
        List of matching programs with match scores
    """
    matching_programs = []
    
    for program in PROGRAMS:
        # Check age eligibility
        if not (program["age_range"][0] <= age <= program["age_range"][1]):
            continue
        
        # Check eligibility criteria
        criteria = program["eligibility_criteria"]
        match_score = 0
        total_criteria = 0
        criteria_met = []
        criteria_not_met = []
        
        for criterion, required_value in criteria.items():
            if required_value is None:  # Optional criterion
                continue
                
            total_criteria += 1
            user_value = user_needs.get(criterion, False)
            
            if required_value == user_value:
                match_score += 1
                criteria_met.append(criterion)
            else:
                criteria_not_met.append(criterion)
        
        # Calculate match percentage
        if total_criteria > 0:
            match_percentage = (match_score / total_criteria) * 100
        else:
            match_percentage = 100  # No specific criteria, so it's a match
        
        # Include programs with at least 60% match
        if match_percentage >= 60:
            matching_programs.append({
                "program": program,
                "match_percentage": match_percentage,
                "criteria_met": criteria_met,
                "criteria_not_met": criteria_not_met
            })
    
    # Sort by match percentage (highest first)
    matching_programs.sort(key=lambda x: x["match_percentage"], reverse=True)
    
    return matching_programs


def format_program_recommendations(matches):
    """
    Format program matches into a readable string
    """
    if not matches:
        return "Based on the information provided, I couldn't find a perfect match. However, let me connect you with our intake team who can do a comprehensive assessment."
    
    result = f"Great news! I found {len(matches)} program(s) that could be a good fit:\n\n"
    
    for i, match in enumerate(matches[:3], 1):  # Show top 3
        program = match["program"]
        percentage = match["match_percentage"]
        
        result += f"{i}. **{program['name']}** ({percentage:.0f}% match)\n"
        result += f"   {program['description']}\n"
        result += f"   Age range: {program['age_range'][0]}-{program['age_range'][1]} years\n"
        result += f"   Benefits:\n"
        for benefit in program['benefits'][:3]:
            result += f"   • {benefit}\n"
        result += "\n"
    
    return result
