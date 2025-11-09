# INSTRUCTIONS: Copy this ENTIRE file content and paste it into programs_database.py
# This adds the missing matching functions to your converted programs database

# NOTE: Keep your PROGRAMS = [...] list at the top, then add these functions below it

def filter_programs_by_criteria(user_profile):
    """
    Filter and score programs based on user profile criteria.
    
    Args:
        user_profile (dict): Dictionary containing:
            - age (int): User's age
            - diagnosis (str): Primary diagnosis
            - location (str): County or city
            - interests (list): List of interest areas
            - support_needs (dict): Support requirements
    
    Returns:
        list: Recommended programs with match scores
    """
    recommendations = []
    
    age = user_profile.get('age')
    diagnosis = user_profile.get('diagnosis', '').lower()
    location = user_profile.get('location', '').lower()
    interests = user_profile.get('interests', [])
    
    for program in PROGRAMS:
        # Step 1: AGE FILTER (Hard requirement)
        age_range = program.get('age_range', {})
        min_age = age_range.get('min_age')
        max_age = age_range.get('max_age')
        
        # Check if age falls within range
        if min_age is not None and age < min_age:
            continue  # Skip this program
        if max_age is not None and age > max_age:
            continue  # Skip this program
        
        # Step 2: CALCULATE MATCH SCORE
        match_score = 0
        total_criteria = 0
        criteria_details = []
        
        # 2a. DIAGNOSIS MATCH
        diagnosis_accepted = program.get('diagnosis_accepted', [])
        if diagnosis_accepted:
            total_criteria += 1
            diagnosis_match = False
            
            for accepted_dx in diagnosis_accepted:
                if accepted_dx.lower() in diagnosis or diagnosis in accepted_dx.lower():
                    diagnosis_match = True
                    break
            
            if diagnosis_match:
                match_score += 1
                criteria_details.append("✓ Diagnosis matches")
            else:
                criteria_details.append("✗ Diagnosis doesn't match")
        
        # 2b. LOCATION MATCH
        counties_served = program.get('counties_served', [])
        location_field = program.get('location', '')
        
        if counties_served or location_field:
            total_criteria += 1
            location_match = False
            
            # Check against counties served
            for county in counties_served:
                if location in county.lower() or county.lower() in location:
                    location_match = True
                    break
            
            # Check against location field
            if not location_match and location_field:
                if location in location_field.lower() or location_field.lower() in location:
                    location_match = True
            
            if location_match:
                match_score += 1
                criteria_details.append("✓ Location matches")
            else:
                criteria_details.append("✗ Location doesn't match")
        
        # 2c. INTEREST/PROGRAM TYPE MATCH
        program_types = program.get('program_type', [])
        if program_types and interests:
            total_criteria += 1
            interest_match = False
            
            for interest in interests:
                for prog_type in program_types:
                    if interest.lower() in prog_type.lower() or prog_type.lower() in interest.lower():
                        interest_match = True
                        break
                if interest_match:
                    break
            
            if interest_match:
                match_score += 1
                criteria_details.append("✓ Interest matches")
            else:
                criteria_details.append("✗ Interest doesn't match")
        
        # 2d. SUPPORT REQUIREMENTS (if provided in user profile)
        support_needs = user_profile.get('support_needs', {})
        if support_needs:
            program_requirements = program.get('support_requirements', {})
            if program_requirements:
                total_criteria += 1
                support_match = True
                
                # Check key support factors
                if support_needs.get('toilet_trained') == False and program_requirements.get('toilet_trained') == True:
                    support_match = False
                if support_needs.get('eating_independence') == False and program_requirements.get('eating_independence') == True:
                    support_match = False
                if support_needs.get('mobility_independence') == False and program_requirements.get('mobility_independence') == True:
                    support_match = False
                
                if support_match:
                    match_score += 1
                    criteria_details.append("✓ Support level appropriate")
                else:
                    criteria_details.append("✗ Support needs don't match requirements")
        
        # Step 3: CALCULATE MATCH PERCENTAGE
        if total_criteria > 0:
            match_percentage = (match_score / total_criteria) * 100
        else:
            match_percentage = 0
        
        # Step 4: APPLY THRESHOLD (60% minimum)
        if match_percentage >= 60:
            recommendations.append({
                'program': program,
                'match_percentage': match_percentage,
                'match_score': match_score,
                'total_criteria': total_criteria,
                'criteria_details': criteria_details
            })
    
    # Step 5: SORT BY MATCH PERCENTAGE (highest first)
    recommendations.sort(key=lambda x: x['match_percentage'], reverse=True)
    
    return recommendations


def format_program_recommendations(recommendations, max_programs=5):
    """
    Format program recommendations into a user-friendly string.
    
    Args:
        recommendations (list): List of recommended programs with scores
        max_programs (int): Maximum number of programs to show
    
    Returns:
        str: Formatted recommendation text
    """
    if not recommendations:
        return """I couldn't find any programs that match your criteria at this time. 
This might be because:
- Your location is outside our current service areas
- The age doesn't match our current program offerings
- We may need more information to find the right fit

I recommend contacting AbilityPath directly at intake@abilitypath.org or calling them 
to discuss specialized options that might be available."""
    
    output = []
    output.append("Based on your needs, here are my top recommendations:\n")
    
    # Show top programs (up to max_programs)
    for i, rec in enumerate(recommendations[:max_programs], 1):
        program = rec['program']
        match_pct = rec['match_percentage']
        
        output.append(f"\n{'='*70}")
        output.append(f"#{i} - {program['name']} (Match: {match_pct:.0f}%)")
        output.append(f"{'='*70}")
        
        # Description
        output.append(f"\n📋 DESCRIPTION:")
        output.append(f"{program.get('description', 'No description available.')}\n")
        
        # Location
        output.append(f"📍 LOCATION:")
        output.append(f"{program.get('physical_location', 'Various locations')}")
        counties = program.get('counties_served', [])
        if counties:
            output.append(f"Serves: {', '.join(counties)}")
        output.append("")
        
        # Age Range
        age_range = program.get('age_range', {})
        min_age = age_range.get('min_age', 'Any')
        max_age = age_range.get('max_age', 'Any')
        if min_age != 'Any' and max_age != 'Any':
            output.append(f"👤 AGE RANGE: {min_age}-{max_age} years old")
        elif min_age != 'Any':
            output.append(f"👤 AGE RANGE: {min_age}+ years old")
        else:
            output.append(f"👤 AGE RANGE: All ages")
        
        # Diagnosis
        diagnosis = program.get('diagnosis_accepted', [])
        if diagnosis:
            output.append(f"🏥 ACCEPTS: {', '.join(diagnosis)}")
        
        # Program Type
        program_types = program.get('program_type', [])
        if program_types:
            output.append(f"🎯 PROGRAM TYPE: {', '.join(program_types)}")
        
        # Schedule
        schedule = program.get('schedule', '')
        if schedule:
            output.append(f"\n⏰ SCHEDULE:")
            output.append(f"{schedule}")
        
        # Enrollment Process
        enrollment = program.get('enrollment_process', '')
        if enrollment:
            output.append(f"\n📝 HOW TO GET STARTED:")
            output.append(f"{enrollment}")
        
        # Match Details
        output.append(f"\n✨ WHY THIS MATCHES ({match_pct:.0f}%):")
        for detail in rec['criteria_details']:
            output.append(f"  {detail}")
        
        output.append("")
    
    # Summary footer
    if len(recommendations) > max_programs:
        output.append(f"\n💡 Note: I found {len(recommendations)} total matches. Showing top {max_programs}.")
        output.append("Would you like to see more options?\n")
    
    output.append("\n" + "="*70)
    output.append("NEXT STEPS:")
    output.append("="*70)
    output.append("1. Review these programs and choose which interests you most")
    output.append("2. Follow the 'How to Get Started' instructions for your chosen program(s)")
    output.append("3. Contact AbilityPath if you have questions: intake@abilitypath.org")
    output.append("\nWould you like more information about any of these programs?")
    
    return "\n".join(output)


def get_all_programs():
    """Return all available programs."""
    return PROGRAMS


def get_program_by_name(name: str):
    """Get a specific program by name."""
    for program in PROGRAMS:
        if program["name"].lower() == name.lower():
            return program
    return None


def get_programs_by_county(county: str):
    """Get programs serving a specific county."""
    return [p for p in PROGRAMS if county in p.get("counties_served", [])]


def get_programs_by_type(program_type: str):
    """Get programs of a specific type."""
    return [p for p in PROGRAMS if program_type in p.get("program_type", [])]


# For backwards compatibility
def match_programs(user_profile):
    """Alias for filter_programs_by_criteria"""
    return filter_programs_by_criteria(user_profile)
