# CSV to Code Field Mapping

**Purpose:** Shows how CSV columns are converted into program database fields  
**Created:** 2025-01-08

---

## FIELD MAPPING TABLE

| CSV Column | Code Field | Extraction Logic | Example |
|------------|------------|------------------|---------|
| **Program** | `name` | Direct copy | "Adult Day Program, Burlingame" |
| **Description** | `description` | Direct copy | "Day Program at Burlingame provides..." |
| **Population** (Age part) | `age_range` | Parse "Ages 18+" or "Ages 12-17" | `{"min_age": 18, "max_age": None}` |
| **Population** (Diagnosis part) | `diagnosis_accepted` | Detect keywords: "developmental disability", "TBI", etc. | `["Developmental Disability"]` |
| **Other Entrance Criteria** | `support_requirements` | Parse independence needs and behavioral requirements | See below |
| **What County/City does this program serve?** | `location` + `counties_served` | Parse county names and regions | `"San Mateo County"` + `["San Mateo County"]` |
| **What is the location of this program/service?** | `physical_location` | Direct copy | "899 Stanton Rd, Burlingame, CA 94010" |
| **When?** | `schedule` | Direct copy | "M-F 9:00 AM–3:00 PM" |
| **How to get started?** | `enrollment_process` | Direct copy | "To begin the intake process..." |
| **Program** + **Description** | `program_type` | Auto-detect from keywords | `["Day Programs", "Social Activities"]` |

---

## DETAILED EXTRACTION EXAMPLES

### 1. AGE RANGE PARSING

**CSV Input (Population column):**
```
Ages 18+
Has a developmental disability
Not currently served by school system
```

**Code Output:**
```python
"age_range": {
    "min_age": 18,
    "max_age": None  # None means no upper limit
}
```

**Another Example:**
```
Ages 12-17
Has a developmental disability
```

**Code Output:**
```python
"age_range": {
    "min_age": 12,
    "max_age": 17
}
```

---

### 2. DIAGNOSIS ACCEPTANCE PARSING

**CSV Input (Population column):**
```
Ages 18+
Has a developmental disability
```

**Code Output:**
```python
"diagnosis_accepted": ["Developmental Disability"]
```

**Complex Example:**
```
Ages 18+
Has an intellectual or developmental disability or stroke or traumatic brain injury (case by case situation)
```

**Code Output:**
```python
"diagnosis_accepted": [
    "Intellectual Disability",
    "Developmental Disability", 
    "Stroke",
    "Traumatic Brain Injury"
]
```

**Detection Keywords:**
- "developmental disabilit" → "Developmental Disability"
- "intellectual disabilit" → "Intellectual Disability"
- "traumatic brain injury" or "tbi" → "Traumatic Brain Injury"
- "stroke" → "Stroke"
- "physical" + "disabilit" → "Physical Disability"
- "mental health" → "Mental Health Condition"

---

### 3. SUPPORT REQUIREMENTS PARSING

**CSV Input (Other Entrance Criteria column):**
```
Doesn't need support AbilityPath staff during service hours for the following: 
using the restroom, eating, mobility, medical needs, and taking medication

Doesn't need support from AbilityPath staff to safely participate without 
frequently being: disruptive, dangerous to self/others, destructive of property, 
or eloping
```

**Code Output:**
```python
"support_requirements": {
    "toilet_trained": True,
    "eating_independence": True,
    "mobility_independence": True,
    "medication_independence": True,
    "behavioral_requirements": [
        "Non-disruptive",
        "Safe to self and others",
        "Non-destructive of property",
        "No elopement risk"
    ]
}
```

**Detection Logic:**
- "restroom" or "toilet" + "doesn't need support" → `toilet_trained: True`
- "eating" + "doesn't need support" → `eating_independence: True`
- "mobility" + "doesn't need support" → `mobility_independence: True`
- "medication" + "doesn't need support" → `medication_independence: True`
- "not disruptive" → adds "Non-disruptive"
- "not dangerous" → adds "Safe to self and others"
- "not destructive" → adds "Non-destructive of property"
- "not eloping" → adds "No elopement risk"

---

### 4. LOCATION & COUNTIES PARSING

**CSV Input (What County/City does this program serve?):**
```
San Mateo County
```

**Code Output:**
```python
"location": "San Mateo County",
"counties_served": ["San Mateo County"]
```

**Complex Example:**
```
San Mateo County and Santa Clara County
```

**Code Output:**
```python
"location": "Both San Mateo and Santa Clara",
"counties_served": ["San Mateo County", "Santa Clara County"]
```

**Regional Example:**
```
Everything between San Francisco to Palo Alto
```

**Code Output:**
```python
"location": "SF to Palo Alto",
"counties_served": ["San Mateo County"]  # Implied by region
```

**Another Regional Example:**
```
Everything between Palo Alto to Santa Cruz
```

**Code Output:**
```python
"location": "Palo Alto to Santa Cruz",
"counties_served": ["Santa Clara County", "Santa Cruz County"]
```

---

### 5. PROGRAM TYPE AUTO-DETECTION

**CSV Input (Program + Description):**
```
Program: "Employment Services, San Mateo County"
Description: "Employment Services supports individuals with foundational 
workplace readiness in their employment journey through customized employment 
tracks (ex: paid internships, group employment, or job placement)..."
```

**Code Output:**
```python
"program_type": ["Employment Support"]
```

**Detection Keywords:**
- "employment", "job", "work", "career", "vocational", "internship" → "Employment Support"
- "living skills", "independent living", "ils", "daily living" → "Living Skills"
- "social", "recreation", "friendship", "community engagement" → "Social Activities"
- "day program", "day service", "tailored day" → "Day Programs"
- "creative", "arts", "artistic" → "Creative Arts"
- "therapy", "therapeutic", "rehabilitation", "reach" → "Therapeutic Services"

**Complex Example:**
```
Program: "Adult Day Program, Burlingame"
Description: "Day Program at Burlingame provides adults with developmental 
disabilities the experiential knowledge and skills to make informed decisions 
about and participate in their preferred types and levels of community engagement, 
including employment, volunteering, and social and recreational activities."
```

**Code Output:**
```python
"program_type": ["Day Programs", "Social Activities"]
# Both detected because description mentions "day program" and "social and recreational"
```

---

## COMPLETE CONVERSION EXAMPLE

**CSV Row:**
```
Program: "Youth Social Recreation"
Description: "Social Recreation has inclusive programming for youth ages 12-17 
with developmental disabilities. Social Rec focuses on building meaningful 
connections, friendships, and exploring abilities and interests."
Population: "Ages 12-17
Has a developmental disability"
Other Entrance Criteria: "Doesn't need support AbilityPath staff during service 
hours for the following: using the restroom, eating, mobility, medical needs, 
and taking medication..."
What County/City does this program serve?: "San Mateo County and Santa Clara County"
What is the location of this program/service?: "Various locations in the community 
or at an AbilityPath site"
When?: "Days and times vary. Please visit https://abilitypath.org/services/..."
How to get started?: "To begin the intake process, please email socialrec@abilitypath.org"
```

**Converted to Code:**
```python
{
    "name": "Youth Social Recreation",
    "description": "Social Recreation has inclusive programming for youth ages 12-17 with developmental disabilities. Social Rec focuses on building meaningful connections, friendships, and exploring abilities and interests.",
    "age_range": {
        "min_age": 12,
        "max_age": 17
    },
    "diagnosis_accepted": [
        "Developmental Disability"
    ],
    "support_requirements": {
        "toilet_trained": True,
        "eating_independence": True,
        "mobility_independence": True,
        "medication_independence": True,
        "behavioral_requirements": [
            "Non-disruptive",
            "Safe to self and others",
            "Non-destructive of property",
            "No elopement risk"
        ]
    },
    "location": "Both San Mateo and Santa Clara",
    "counties_served": [
        "San Mateo County",
        "Santa Clara County"
    ],
    "physical_location": "Various locations in the community or at an AbilityPath site",
    "schedule": "Days and times vary. Please visit https://abilitypath.org/services/...",
    "enrollment_process": "To begin the intake process, please email socialrec@abilitypath.org",
    "program_type": [
        "Social Activities"
    ]
}
```

---

## HOW THE AGENT USES THESE FIELDS

### During Conversation:
```python
# Agent extracts from user:
user_age = 15
user_diagnosis = "Down Syndrome"  # → "Intellectual Disability"
user_location = "San Mateo"
user_interests = ["social activities", "friendship"]
```

### Matching Process:
```python
for program in PROGRAMS:
    # 1. AGE CHECK (hard filter)
    if not (program["age_range"]["min_age"] <= user_age <= program["age_range"]["max_age"]):
        continue  # Skip this program
    
    # 2. DIAGNOSIS CHECK
    if user_diagnosis in program["diagnosis_accepted"]:
        match_score += 1
    
    # 3. LOCATION CHECK
    if user_location in program["counties_served"]:
        match_score += 1
    
    # 4. INTEREST CHECK
    if any(interest in program["program_type"] for interest in user_interests):
        match_score += 1
    
    # 5. CALCULATE MATCH PERCENTAGE
    match_percentage = (match_score / total_criteria) * 100
    
    # 6. THRESHOLD CHECK
    if match_percentage >= 60:
        recommend(program)
```

### Final Recommendation Display:
```python
# Uses these fields in response:
f"I recommend {program['name']} (Match: {match_percentage}%)"
f"Description: {program['description']}"
f"Location: {program['physical_location']}"
f"Schedule: {program['schedule']}"
f"How to get started: {program['enrollment_process']}"
```

---

## CUSTOMIZATION TIPS

### To Adjust Age Range Manually:
Edit `programs_database_real.py`:
```python
"age_range": {"min_age": 14, "max_age": None},  # Change 18 to 14
```

### To Add Missing Diagnosis:
```python
"diagnosis_accepted": ["Developmental Disability", "Autism Spectrum Disorder"],
```

### To Change Location Category:
```python
"location": "Santa Clara County",  # Change from "Both counties"
```

### To Add Program Type:
```python
"program_type": ["Employment Support", "Living Skills"],  # Add second type
```

---

## VALIDATION CHECKLIST

After conversion, check `programs_data.json`:

- [ ] All 15 programs present?
- [ ] Age ranges make sense? (12-17 for youth, 18+ for adults)
- [ ] Diagnosis types accurate? (DD, ID, TBI, Stroke)
- [ ] Counties match CSV? (San Mateo, Santa Clara)
- [ ] Program types detected correctly?
- [ ] Support requirements parsed?
- [ ] Enrollment processes complete?

---

## MANUAL FIXES (If Needed)

If auto-detection is wrong, manually edit `programs_database_real.py`:

**Example Fix - Wrong Age Range:**
```python
# BEFORE (Auto-detected wrong):
"age_range": {"min_age": None, "max_age": None},

# AFTER (Manual fix):
"age_range": {"min_age": 18, "max_age": 30},
```

**Example Fix - Missing Program Type:**
```python
# BEFORE (Not detected):
"program_type": ["General Support"],

# AFTER (Manual fix):
"program_type": ["Living Skills", "Employment Support"],
```

**Example Fix - Wrong County:**
```python
# BEFORE:
"counties_served": ["San Mateo County"],

# AFTER:
"counties_served": ["Santa Clara County"],
```

---

## QUICK REFERENCE: Python Data Types

```python
# STRING (text)
"name": "Program Name"

# LIST (multiple items)
"diagnosis_accepted": ["DD", "ID", "TBI"]

# DICTIONARY (nested data)
"age_range": {"min_age": 18, "max_age": None}

# BOOLEAN (true/false)
"toilet_trained": True

# NONE (no value/unlimited)
"max_age": None
```

---

**This mapping guide helps you understand how the CSV converter works and how to manually fix any issues!** 🔧
