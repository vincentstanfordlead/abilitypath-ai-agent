# How to Update Your Screening Agent with Real AbilityPath Programs

**Created:** 2025-01-08  
**Purpose:** Step-by-step guide to replace sample programs with real CSV data

---

## WHAT YOU'LL DO

You'll use the CSV file you uploaded to automatically replace the 10 sample programs in your screening agent with the **15 real AbilityPath programs**.

---

## STEP-BY-STEP INSTRUCTIONS

### **Step 1: Download the CSV Loader Tool**

I've created a Python script that reads your CSV and converts it to the format your agent needs.

Download these files to your Mac:
- `csv_program_loader.py` - The conversion tool
- Your CSV file: `WIP_Nov 7_ Tech For Good AbilityPath Info. - Program Info.csv`

Save both files in your project folder:
```
/Users/a12345/abilitypath_prototype/
```

---

### **Step 2: Run the Conversion**

Open Terminal and navigate to your project folder:

```bash
cd /Users/a12345/abilitypath_prototype/
```

Run the converter:

```bash
python3 csv_program_loader.py "WIP_Nov 7_ Tech For Good AbilityPath Info. - Program Info.csv"
```

**What this does:**
- Reads your CSV file
- Parses program information (age, diagnosis, location, etc.)
- Creates two output files:
  - `programs_database_real.py` - Ready-to-use Python module
  - `programs_data.json` - Human-readable version for review

---

### **Step 3: Review the Converted Data**

Open `programs_data.json` in a text editor to verify the data looks correct:

```bash
open programs_data.json
```

**Check for:**
- All 15 programs are present
- Age ranges are correct
- Diagnosis types are accurate
- Counties/locations are properly parsed

---

### **Step 4: Backup Your Old Programs**

Before replacing, save your original sample programs:

```bash
cp programs_database.py programs_database_BACKUP.py
```

---

### **Step 5: Replace with Real Programs**

Replace the old database with the new one:

```bash
cp programs_database_real.py programs_database.py
```

---

### **Step 6: Restart Your Screening Agent**

Stop the current running agent (press `Ctrl+C` in the terminal where it's running).

Start it again:

```bash
python3 web_app.py
```

---

### **Step 7: Test with Real Scenarios**

Go to http://localhost:5001 and test with a realistic scenario:

**Test Scenario 1: Youth looking for social activities**
```
Hi, my daughter is 15 years old and has Down Syndrome (intellectual disability). 
We live in San Mateo County. She's looking for social activities and friendship 
opportunities on weekends. She's toilet-trained and doesn't need medical support 
during activities.
```

**Expected Recommendation:**
- Youth Social Recreation (100% match)

---

**Test Scenario 2: Adult seeking employment**
```
Hello, I'm helping my 22-year-old brother who has autism. He lives in Santa Clara 
County and wants to find a job. He's high-functioning, drives himself, and needs 
help with resume writing and interview preparation.
```

**Expected Recommendations:**
- Employment Services, Santa Clara County (100% match)
- Immersion Work Readiness Program (high match)

---

**Test Scenario 3: Adult needing day program**
```
My 30-year-old son has a developmental disability and lives in Burlingame 
(San Mateo County). He's not working and needs a structured day program 
where he can learn skills and socialize. He's toilet-trained and doesn't 
have behavioral challenges.
```

**Expected Recommendations:**
- Adult Day Program, Burlingame (100% match)
- Community Access Adult Day Program (high match)

---

## WHAT THE CONVERTER EXTRACTS FROM YOUR CSV

### **From "Population" Column:**
- **Age Range:** "Ages 18+" → min_age: 18, max_age: None
- **Age Range:** "Ages 12-17" → min_age: 12, max_age: 17
- **Diagnosis:** "developmental disability" → ["Developmental Disability"]
- **Diagnosis:** "intellectual or developmental disability or stroke or traumatic brain injury" → ["Intellectual Disability", "Developmental Disability", "Stroke", "Traumatic Brain Injury"]

### **From "Other Entrance Criteria" Column:**
- **Support Requirements:**
  - Toilet training status
  - Eating independence
  - Mobility independence
  - Medication independence
  - Behavioral requirements (non-disruptive, safe, non-elopement)

### **From "What County/City does this program serve?" Column:**
- **Counties Served:** ["San Mateo County", "Santa Clara County", etc.]
- **Location Category:** "San Mateo County", "Both counties", "SF to Palo Alto", etc.

### **From "Program" and "Description" Columns:**
- **Program Type (Auto-detected):**
  - "Employment Services" → Employment Support
  - "Independent Living Skills" → Living Skills
  - "Social Recreation" → Social Activities
  - "Day Program" → Day Programs
  - "Creative Arts" → Creative Arts
  - "REACH" → Therapeutic Services

---

## UNDERSTANDING THE OUTPUT FILES

### **programs_data.json (For Review)**

```json
[
  {
    "name": "Adult Day Program, Burlingame",
    "description": "Day Program at Burlingame provides adults...",
    "location": "San Mateo County",
    "age_range": {
      "min_age": 18,
      "max_age": null
    },
    "diagnosis_accepted": [
      "Developmental Disability"
    ],
    "support_requirements": {
      "toilet_trained": true,
      "eating_independence": true,
      "mobility_independence": true,
      "medication_independence": true,
      "behavioral_requirements": [
        "Non-disruptive",
        "Safe to self and others",
        "Non-destructive of property",
        "No elopement risk"
      ]
    },
    "counties_served": [
      "San Mateo County"
    ],
    "physical_location": "899 Stanton Rd, Burlingame, CA 94010...",
    "schedule": "5 days per week (Monday-Friday) from 9:00 AM–3:00 PM...",
    "enrollment_process": "To begin the intake process, please contact...",
    "program_type": [
      "Day Programs",
      "Social Activities"
    ]
  },
  ...
]
```

### **programs_database_real.py (For Your Agent)**

```python
PROGRAMS = [
    {
        "name": "Adult Day Program, Burlingame",
        "description": "Day Program at Burlingame provides adults...",
        "location": "San Mateo County",
        "age_range": {"min_age": 18, "max_age": None},
        ...
    },
    ...
]
```

---

## TROUBLESHOOTING

### **Problem: "python3: command not found"**

**Solution:** Use `python` instead:
```bash
python csv_program_loader.py "WIP_Nov 7_ Tech For Good AbilityPath Info. - Program Info.csv"
```

---

### **Problem: "No such file or directory"**

**Solution:** Make sure you're in the correct folder:
```bash
pwd  # Check current directory
ls   # List files - you should see csv_program_loader.py and your CSV
```

---

### **Problem: Agent still shows old programs**

**Solution:** Make sure you:
1. Copied `programs_database_real.py` to `programs_database.py`
2. Restarted the web app (stopped and started again)
3. Refreshed your browser page

---

### **Problem: Age ranges look wrong**

**Solution:** Manually edit `programs_database_real.py` to fix:
```python
"age_range": {"min_age": 18, "max_age": None},  # 18+ (no upper limit)
"age_range": {"min_age": 12, "max_age": 17},    # 12-17
```

---

### **Problem: Program type not detected correctly**

**Solution:** The converter guesses program types from keywords. You can manually add:
```python
"program_type": ["Employment Support", "Living Skills"],
```

---

## CUSTOMIZING THE MATCHING LOGIC

After updating programs, you may want to adjust how matching works.

### **Location: programs_database.py, Lines 174-230**

Current threshold: **60% minimum match**

To make matching **stricter** (fewer recommendations):
```python
if match_percentage >= 75:  # Changed from 60 to 75
    recommendations.append({...})
```

To make matching **looser** (more recommendations):
```python
if match_percentage >= 50:  # Changed from 60 to 50
    recommendations.append({...})
```

---

## WHAT'S INCLUDED IN YOUR 15 REAL PROGRAMS

Based on your CSV, here are the programs that will be loaded:

### **Day Programs (5 programs):**
1. Adult Day Program, Burlingame (San Mateo)
2. Adult Day Program, Daly City (San Mateo)
3. Community Access Adult Day Program (San Mateo)
4. Adult Day Program, San Jose (Santa Clara)
5. Adult Day Program, Palo Alto (Santa Clara)

### **Social Recreation (2 programs):**
6. Youth Social Recreation (Ages 12-17, Both counties)
7. Adult Social Recreation (Ages 18+, Both counties)

### **Independent Living Skills (2 programs):**
8. Independent Living Skills, North (SF to Palo Alto)
9. Independent Living Skills, South (Palo Alto to Santa Cruz)

### **Tailored Services (1 program):**
10. Tailored Day Services, San Mateo County

### **Employment Services (3 programs):**
11. Employment Services, San Mateo County
12. Employment Services, Santa Clara County
13. Immersion Work Readiness Program (Santa Clara)

### **Specialized Programs (2 programs):**
14. Creative Arts Program (Santa Clara) - **NEW**
15. REACH - Stroke & TBI Services (Both counties) - **Specialized**

---

## KEY DIFFERENCES FROM SAMPLE PROGRAMS

### **1. Geographic Coverage is Precise**
- Sample: Generic "San Mateo County"
- Real: Specific cities (Burlingame, Daly City, San Jose, Palo Alto)

### **2. Support Requirements are Detailed**
- Sample: Basic criteria
- Real: Detailed entrance criteria including toilet training, eating, mobility, behavioral requirements

### **3. Enrollment Processes Vary**
- Some programs: Contact Regional Center
- Employment programs: Complete DOR application first
- New programs (Creative Arts, Immersion): Interest list process

### **4. Multiple Day Program Locations**
- Sample: 1 generic day program
- Real: 5 day program locations across both counties

### **5. Specialized Programs for TBI/Stroke**
- REACH program specifically for Traumatic Brain Injury and Stroke survivors
- Employment Services in Santa Clara accepts TBI (case-by-case)

---

## NEXT STEPS AFTER UPDATING

### **1. Test All Program Types**

Test scenarios covering:
- ✅ Youth programs (ages 12-17)
- ✅ Adult programs (ages 18+)
- ✅ Employment seekers
- ✅ Day program needs
- ✅ Living skills support
- ✅ Social/recreation
- ✅ TBI/Stroke survivors
- ✅ Different counties (San Mateo, Santa Clara)

### **2. Verify Enrollment Processes**

Make sure the agent provides the correct "How to get started" instructions for each program type:
- Regional Center referral programs
- DOR application programs
- Interest list programs
- Direct email contact programs

### **3. Update Conversation Prompts**

Edit `screening_agent.py` to mention the real programs by name:

**Line ~45 (System Prompt):**
```python
You are a friendly intake specialist for AbilityPath, a Bay Area nonprofit 
serving 1,500+ families weekly with developmental disability programs including:
- 5 Adult Day Programs across San Mateo and Santa Clara Counties
- Youth and Adult Social Recreation programs
- Independent Living Skills training (North and South)
- Employment Services with job placement support
- Specialized programs like Creative Arts and REACH for TBI/Stroke
...
```

### **4. Prepare Demo Talking Points**

For your hackathon presentation:
- "We've loaded **15 real AbilityPath programs** covering 5 counties"
- "The agent matches based on **age, diagnosis, location, interests, and support needs**"
- "Families get personalized recommendations in **under 2 minutes** vs. 2-year wait"
- "Real enrollment processes are provided for each program"

---

## VALIDATION CHECKLIST

Before your demo, verify:

- [ ] All 15 programs loaded successfully
- [ ] Age ranges are correct (12-17 for youth, 18+ for adults)
- [ ] Counties are accurate (San Mateo, Santa Clara, Both)
- [ ] Diagnosis types include Developmental Disability, Intellectual Disability, TBI, Stroke
- [ ] Support requirements are parsed correctly
- [ ] Program types are auto-detected (Employment, Living Skills, Day Programs, etc.)
- [ ] Enrollment processes are complete and accurate
- [ ] Test scenarios return expected programs
- [ ] Agent provides correct "How to get started" instructions

---

## FILE LOCATIONS SUMMARY

```
/Users/a12345/abilitypath_prototype/
├── csv_program_loader.py              ← NEW: Conversion tool
├── WIP_Nov 7_... - Program Info.csv   ← Your uploaded CSV
├── programs_data.json                 ← NEW: Generated for review
├── programs_database_real.py          ← NEW: Generated program database
├── programs_database_BACKUP.py        ← Backup of original samples
├── programs_database.py               ← UPDATED: Now contains real programs
├── screening_agent.py
├── web_app.py
└── templates/
    └── index.html
```

---

## QUESTIONS FOR YOUR STAKEHOLDER MEETING

Now that you have the CSV data, ask stakeholders:

1. **Missing Information:**
   - "Are there any programs missing from this CSV?"
   - "Should we include early childhood programs (0-5 years)?"

2. **Eligibility Clarifications:**
   - "Can programs make exceptions to support requirements?"
   - "Are there any priority populations (e.g., aging out of school)?"

3. **Waitlist Status:**
   - "Which programs currently have waitlists?"
   - "Should the agent indicate program capacity?"

4. **Future Programs:**
   - "Creative Arts and Immersion are marked as 'new' - when will they launch?"
   - "Should we show them in recommendations now or wait?"

---

**You're ready to update your agent with real AbilityPath programs! This will make your demo much more impactful.** 🚀

---

**Files You Need:**
- [csv_program_loader.py](computer:///mnt/user-data/outputs/csv_program_loader.py) ← Download this
- Your CSV (already uploaded)
