"""
Quick Diagnostic Script for AbilityPath Screening Agent
Run this to see what's wrong when programs aren't showing
"""

print("="*70)
print("ABILITYPATH AGENT DIAGNOSTIC")
print("="*70)

# Test 1: Check if programs database loads
print("\n[TEST 1] Loading programs database...")
try:
    from programs_database import PROGRAMS, filter_programs_by_criteria, format_program_recommendations
    print(f"✅ SUCCESS: Loaded {len(PROGRAMS)} programs")
    print(f"   First program: {PROGRAMS[0]['name']}")
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    print("   Fix: Make sure programs_database.py has all functions")
    exit(1)
except Exception as e:
    print(f"❌ ERROR: {e}")
    exit(1)

# Test 2: Check program data structure
print("\n[TEST 2] Checking program data structure...")
first_program = PROGRAMS[0]
required_fields = ['name', 'age_range', 'diagnosis_accepted', 'location', 'counties_served']
missing_fields = []

for field in required_fields:
    if field not in first_program:
        missing_fields.append(field)
    else:
        value = first_program[field]
        print(f"   ✓ {field}: {value}")

if missing_fields:
    print(f"❌ MISSING FIELDS: {missing_fields}")
else:
    print("✅ All required fields present")

# Test 3: Test matching with simple profile
print("\n[TEST 3] Testing matching algorithm...")
test_profile = {
    'age': 15,
    'diagnosis': 'developmental disability',
    'location': 'san mateo',
    'interests': ['social']
}

print(f"Test profile: {test_profile}")

try:
    results = filter_programs_by_criteria(test_profile)
    print(f"✅ Matching works: Found {len(results)} matches")
    
    if results:
        print(f"   Top match: {results[0]['program']['name']} ({results[0]['match_percentage']:.0f}%)")
        print(f"   Match details: {results[0]['criteria_details']}")
    else:
        print("⚠️  WARNING: No matches found for test profile")
        print("   This might be a data issue")
except Exception as e:
    print(f"❌ MATCHING ERROR: {e}")

# Test 4: Check age filtering
print("\n[TEST 4] Testing age filtering...")
youth_programs = []
adult_programs = []

for prog in PROGRAMS:
    age_range = prog.get('age_range', {})
    min_age = age_range.get('min_age')
    max_age = age_range.get('max_age')
    
    if max_age and max_age < 18:
        youth_programs.append(prog['name'])
    elif min_age and min_age >= 18:
        adult_programs.append(prog['name'])

print(f"Youth programs (max age < 18): {len(youth_programs)}")
if youth_programs:
    for name in youth_programs:
        print(f"   - {name}")

print(f"\nAdult programs (min age >= 18): {len(adult_programs)}")
if adult_programs:
    for name in adult_programs[:3]:
        print(f"   - {name}")
    if len(adult_programs) > 3:
        print(f"   ... and {len(adult_programs) - 3} more")

# Test 5: Check diagnosis coverage
print("\n[TEST 5] Checking diagnosis acceptance...")
diagnosis_stats = {}

for prog in PROGRAMS:
    diagnoses = prog.get('diagnosis_accepted', [])
    for dx in diagnoses:
        diagnosis_stats[dx] = diagnosis_stats.get(dx, 0) + 1

print("Diagnosis types found:")
for dx, count in diagnosis_stats.items():
    print(f"   {dx}: {count} programs")

if not diagnosis_stats:
    print("⚠️  WARNING: No diagnosis types found in any program!")

# Test 6: Check location coverage
print("\n[TEST 6] Checking location coverage...")
location_stats = {}

for prog in PROGRAMS:
    counties = prog.get('counties_served', [])
    for county in counties:
        location_stats[county] = location_stats.get(county, 0) + 1

print("Counties served:")
for county, count in location_stats.items():
    print(f"   {county}: {count} programs")

if not location_stats:
    print("⚠️  WARNING: No counties found in any program!")

# Test 7: Test with multiple profiles
print("\n[TEST 7] Testing with various user profiles...")

test_cases = [
    {
        'name': 'Youth in San Mateo',
        'profile': {'age': 15, 'diagnosis': 'developmental disability', 'location': 'san mateo', 'interests': ['social']}
    },
    {
        'name': 'Adult in Santa Clara',
        'profile': {'age': 25, 'diagnosis': 'developmental disability', 'location': 'santa clara', 'interests': ['employment']}
    },
    {
        'name': 'Young adult seeking living skills',
        'profile': {'age': 20, 'diagnosis': 'intellectual disability', 'location': 'palo alto', 'interests': ['living skills']}
    },
]

for test in test_cases:
    results = filter_programs_by_criteria(test['profile'])
    print(f"\n{test['name']}:")
    print(f"   Matches: {len(results)}")
    if results:
        print(f"   Top: {results[0]['program']['name']} ({results[0]['match_percentage']:.0f}%)")
    else:
        print("   ❌ No matches")

# Test 8: Check if screening_agent.py can be imported
print("\n[TEST 8] Checking screening_agent.py...")
try:
    from screening_agent import ScreeningAgent
    print("✅ ScreeningAgent imported successfully")
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Summary
print("\n" + "="*70)
print("DIAGNOSTIC SUMMARY")
print("="*70)

print(f"""
✓ Programs loaded: {len(PROGRAMS)}
✓ Youth programs: {len(youth_programs)}
✓ Adult programs: {len(adult_programs)}
✓ Diagnosis types: {len(diagnosis_stats)}
✓ Counties covered: {len(location_stats)}

Next steps:
1. If all tests passed: Check web_app.py logs when you test
2. If matching returned 0: Check program data in programs_database.py
3. If imports failed: Check file paths and syntax errors
""")

print("\nRun the agent and watch Terminal for errors:")
print("  python3 web_app.py")
print("\nThen test at: http://localhost:5001")
print("="*70)
