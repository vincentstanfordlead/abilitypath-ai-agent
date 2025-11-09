# ABILITYPATH PROGRAM INFORMATION INQUIRY LOGIC - CODE-READY SUMMARY

═══════════════════════════════════════════════════════════════════════════════════════

**Based on:** WIP_Nov 7 Program Info CSV + AbilityPath Services Overview  
**Created:** 2025-01-08  
**Purpose:** Handle program information inquiries (NOT enrollment screening)  
**Ready to:** Copy-paste into screening_agent.py as system prompt context

═══════════════════════════════════════════════════════════════════════════════════════

## PROGRAM INFORMATION INQUIRY FLOW SUMMARY

═══════════════════════════════════════════════════════════════════════════════════════

### STEP 1: DETECT INQUIRY TYPE

→ **General overview** ("What programs do you have?")  
→ **Category-specific** ("What employment programs do you offer?")  
→ **Program-specific** ("Tell me about Youth Social Recreation")  
→ **Requirements** ("What documents do I need to enroll?")

### STEP 2: PROVIDE APPROPRIATE INFORMATION

→ **General:** List all program types with brief descriptions  
→ **Category:** Show all programs in that category with details  
→ **Specific:** Full program details including activities, requirements, documents  
→ **Requirements:** Document checklist by program type

### STEP 3: OFFER NEXT STEPS

→ Provide contact information for enrollment  
→ Suggest related programs  
→ Ask if they have more questions

═══════════════════════════════════════════════════════════════════════════════════════

## 1. PROGRAM TYPES OVERVIEW

═══════════════════════════════════════════════════════════════════════════════════════

**WHEN USER ASKS:** "What types of programs do you have?" or "What services do you offer?"

**RESPONSE STRUCTURE:**

AbilityPath offers 6 main types of programs for individuals with developmental disabilities:

### 1. DAY PROGRAMS (5 locations)
**Purpose:** Structured weekday activities for adults 18+ to build skills and participate in community  
**Locations:** Burlingame, Daly City, Community Access (San Mateo), San Jose, Palo Alto  
**Who:** Adults 18+ with developmental disabilities  
**When:** Monday-Friday, 9:00 AM–3:00 PM (full-time or part-time options)

### 2. SOCIAL RECREATION (2 programs)
**Purpose:** Weekend and evening social activities to build friendships and explore interests  
**Types:**  
- Youth Social Recreation (ages 12-17)  
- Adult Social Recreation (ages 18-30)  
**Locations:** Various locations in San Mateo and Santa Clara Counties  
**When:** Weekends, weeknights, summer, school breaks

### 3. EMPLOYMENT SERVICES (3 programs)
**Purpose:** Job readiness, placement, and coaching for competitive employment  
**Types:**  
- Employment Services (San Mateo County)  
- Employment Services (Santa Clara County)  
- Immersion Work Readiness Program (Santa Clara - new)  
**Who:** Adults 18+ ready for employment  
**When:** Flexible scheduling

### 4. INDEPENDENT LIVING SKILLS (2 programs)
**Purpose:** 1:1 coaching to build daily living skills (cooking, budgeting, travel, etc.)  
**Types:**  
- ILS North (San Francisco to Palo Alto)  
- ILS South (Palo Alto to Santa Cruz)  
**Who:** Adults 18+ with developmental disabilities  
**When:** Flexible scheduling at home or in community

### 5. SPECIALIZED PROGRAMS (2 programs)
**Purpose:** Targeted services for specific needs  
**Types:**  
- Creative Arts Program (arts-focused day program - new)  
- REACH (therapeutic services for stroke/TBI survivors)  
**Locations:** Palo Alto  
**When:** Varies by program

### 6. TAILORED DAY SERVICES (1 program)
**Purpose:** Pre-employment focused 1:1 instruction with personalized goals  
**Location:** San Mateo County  
**Who:** Adults 18+ with developmental disabilities  
**When:** Flexible scheduling

**NEXT STEP:** "Which type of program interests you most? I can provide more details about any of these."

═══════════════════════════════════════════════════════════════════════════════════════

## 2. GENERAL INFO BY PROGRAM CATEGORY

═══════════════════════════════════════════════════════════════════════════════════════

### CATEGORY 1: DAY PROGRAMS

**WHEN USER ASKS:** "Tell me about day programs" or "What are day programs?"

**RESPONSE STRUCTURE:**

#### WHAT ARE DAY PROGRAMS?
Day programs provide structured weekday activities for adults with developmental disabilities who are not in school or work. Participants learn skills to make informed decisions about community engagement, including employment, volunteering, and social/recreational activities.

#### WHO THEY'RE FOR:
- Adults ages 18+
- Have a developmental disability
- Not currently served by school system
- Can participate safely in group settings

#### WHAT PARTICIPANTS DO:
- Explore employment options and build work readiness skills
- Practice daily living and social skills
- Participate in community outings and activities
- Engage in recreation, arts, and personal interest pursuits
- Build independence and decision-making skills

#### OUR 5 DAY PROGRAM LOCATIONS:

**1. Adult Day Program, Burlingame**
- Location: 899 Stanton Rd, Burlingame, CA 94010
- Serves: San Mateo County
- Schedule: M-F 9am-3pm (full-time or part-time)

**2. Adult Day Program, Daly City**
- Location: 550 Washington St #100, Daly City, CA 94015
- Serves: San Mateo County
- Schedule: M-F 9am-3pm (full-time or part-time)

**3. Community Access Adult Day Program**
- Location: Various community locations
- Serves: San Mateo County
- Schedule: M-F 9am-3pm (full-time or part-time)

**4. Adult Day Program, San Jose**
- Location: Based at 2248 N. First Street, San Jose, CA 95131
- Serves: Santa Clara County
- Schedule: M-F 9am-3pm (full-time or part-time)

**5. Adult Day Program, Palo Alto**
- Location: Based at 3864 Middlefield Rd, Palo Alto, CA 94303
- Serves: Santa Clara County
- Schedule: M-F 9am-3pm (full-time or part-time)

#### NEXT STEP:
"Would you like details about a specific location, or information about how to enroll?"

---

### CATEGORY 2: SOCIAL RECREATION PROGRAMS

**WHEN USER ASKS:** "Tell me about social recreation" or "What social programs do you have?"

**RESPONSE STRUCTURE:**

#### WHAT IS SOCIAL RECREATION?
Social recreation provides inclusive programming for individuals with developmental disabilities to build meaningful connections, friendships, and explore abilities and interests through fun activities during evenings, weekends, and school breaks.

#### WHO THEY'RE FOR:
**Youth (ages 12-17):**
- Have a developmental disability
- Want to make friends and try new activities
- Can participate safely without constant supervision

**Adults (ages 18-30):**
- Have a developmental disability
- Want social connections and community involvement
- Can participate safely in group activities

#### WHAT PARTICIPANTS DO:
- Weekend outings (movies, bowling, parks, museums)
- Evening social events (game nights, cooking classes, art activities)
- Summer camps and programs
- School break activities (winter, spring breaks)
- Community events and celebrations
- Skill-building workshops (photography, music, sports)

#### OUR 2 SOCIAL RECREATION PROGRAMS:

**1. Youth Social Recreation (Ages 12-17)**
- Serves: San Mateo County AND Santa Clara County
- When: Varies - check website for upcoming programs
- Format: Drop-in activities, multi-week programs, special events
- Contact: socialrec@abilitypath.org

**2. Adult Social Recreation (Ages 18-30)**
- Serves: San Mateo County AND Santa Clara County
- When: Varies - check website for upcoming programs
- Format: Drop-in activities, multi-week programs, special events
- Contact: socialrec@abilitypath.org

#### CURRENT ACTIVITIES:
Visit https://abilitypath.org/services/adult-services/social-recreation-programs/ for the latest schedule and registration.

#### NEXT STEP:
"Would you like to enroll in social recreation, or do you have questions about specific activities?"

---

### CATEGORY 3: EMPLOYMENT SERVICES

**WHEN USER ASKS:** "What employment programs do you have?" or "Tell me about job services"

**RESPONSE STRUCTURE:**

#### WHAT ARE EMPLOYMENT SERVICES?
Employment services help individuals with developmental disabilities prepare for, find, and succeed in community-based jobs. Services include job exploration, resume development, interview preparation, job placement, and ongoing job coaching.

#### WHO THEY'RE FOR:
- Adults ages 18+
- Have foundational workplace readiness
- Want to work in the community
- Can work independently or with support

#### WHAT PARTICIPANTS GET:

**Job Exploration:**
- Discover interests and strengths
- Explore different career paths
- Visit worksites and meet employers

**Job Readiness:**
- Resume and cover letter development
- Interview preparation and practice
- Workplace communication skills
- Professional behavior training

**Job Placement:**
- Customized job matches based on skills
- Paid internships
- Group employment opportunities
- Individual job placements

**Ongoing Support:**
- Dedicated job coaching
- Employer communication
- Problem-solving support
- Skill development on the job

#### OUR 3 EMPLOYMENT PROGRAMS:

**1. Employment Services, San Mateo County**
- Serves: San Mateo County residents
- For: Adults 18+ with developmental disabilities
- Enrollment: Requires DOR (Department of Rehabilitation) application
- Process: Complete DOR form → DOR sends referral to AbilityPath → We contact you

**2. Employment Services, Santa Clara County**
- Serves: Santa Clara County residents
- For: Adults 18+ with developmental/intellectual disability, or stroke/TBI (case-by-case)
- Enrollment: Requires DOR application
- Process: Complete DOR form → DOR sends referral to AbilityPath → We contact you

**3. Immersion Work Readiness Program (NEW)**
- Location: 2248 N. First Street, San Jose, CA 95131
- Serves: Santa Clara County
- For: Adults 18+ with range of disabilities (physical, intellectual, developmental, mental health, stroke, TBI)
- Schedule: M-F 9am-2pm
- Format: Small-group modules + individualized planning
- Status: New program - interest list (not yet DOR-approved)
- Enrollment: Fill out AbilityPath Interest Form

#### NEXT STEP:
"Are you interested in employment services? I can help you understand the DOR application process or add you to the Immersion interest list."

---

### CATEGORY 4: INDEPENDENT LIVING SKILLS

**WHEN USER ASKS:** "What is ILS?" or "Tell me about living skills programs"

**RESPONSE STRUCTURE:**

#### WHAT IS INDEPENDENT LIVING SKILLS (ILS)?
ILS offers one-on-one coaching at home or in the community to help participants learn everyday skills for living more independently. Coaches work individually with participants to build confidence and capability.

#### WHO IT'S FOR:
- Adults ages 18+
- Have a developmental disability
- Want to build independence in daily activities
- Can participate safely with 1:1 support

#### WHAT PARTICIPANTS LEARN:

**Home Skills:**
- Cooking meals and meal planning
- Cleaning and organizing living space
- Laundry and clothing care
- Basic home maintenance

**Money Management:**
- Budgeting and tracking expenses
- Banking basics
- Shopping and comparing prices
- Paying bills

**Travel & Transportation:**
- Using public transit
- Reading maps and schedules
- Planning routes
- Pedestrian safety

**Safety Skills:**
- Emergency procedures
- Internet and phone safety
- Stranger awareness
- Home security

**Social & Communication:**
- Making phone calls
- Email and messaging
- Making appointments
- Social interactions

#### OUR 2 ILS PROGRAMS:

**1. Independent Living Skills, North**
- Serves: Everything between San Francisco to Palo Alto
- Where: At your residence or in the community
- Schedule: Flexible, arranged between you and your staff member
- Format: 1:1 coaching sessions
- Enrollment: Requires Regional Center referral

**2. Independent Living Skills, South**
- Serves: Everything between Palo Alto to Santa Cruz
- Where: At your residence or in the community
- Schedule: Flexible, arranged between you and your staff member
- Format: 1:1 coaching sessions
- Enrollment: Requires Regional Center referral

#### HOW IT WORKS:
1. Your Regional Center Service Coordinator sends referral to intake@abilitypath.org
2. We review your information
3. We match you with a coach
4. You and your coach decide what skills to work on
5. Coach visits you weekly/bi-weekly based on your plan
6. You practice skills together until you feel confident

#### NEXT STEP:
"Are you interested in ILS? I can explain how to get a Regional Center referral, or answer questions about what you'd work on with a coach."

---

### CATEGORY 5: SPECIALIZED PROGRAMS

**WHEN USER ASKS:** "What specialized programs do you have?" or "Do you have programs for [specific need]?"

**RESPONSE STRUCTURE:**

#### WHAT ARE SPECIALIZED PROGRAMS?
These programs serve specific populations or focus on unique activities not covered by our main program types.

#### OUR 2 SPECIALIZED PROGRAMS:

**1. CREATIVE ARTS PROGRAM (NEW)**

**What It Is:**
An upcoming arts-focused day program for adults with intellectual and developmental disabilities to express creativity, develop artistic and vocational skills, and build community connections through the arts.

**Who It's For:**
- Adults ages 18+
- Have a developmental disability
- Interested in creative expression and arts

**What Participants Do:**
- Create artwork in various mediums
- Develop artistic skills
- Participate in community art projects
- Build portfolio and artistic identity
- Connect with inclusive community art spaces

**Location:** 525 East Charleston Road, Palo Alto, CA 94306  
**Serves:** Santa Clara County  
**Schedule:** Days and times TBD  
**Status:** NEW PROGRAM - not yet approved by San Andreas Regional Center  
**Enrollment:** Interest list - fill out AbilityPath Interest Form

---

**2. REACH (Stroke & Traumatic Brain Injury Services)**

**What It Is:**
Therapeutic services and programming for people with stroke and traumatic brain injuries, offering physical therapy, speech therapy, and occupational therapy from licensed therapists with decades of expertise.

**Who It's For:**
- Individuals who have had a stroke
- Individuals who have had a traumatic brain injury
- All ages (typically adults)

**What Participants Get:**
- Physical therapy to improve mobility and strength
- Speech therapy to improve communication and swallowing
- Occupational therapy to improve daily living skills
- Group classes for peer support
- 1-on-1 therapy sessions

**Location:** Cubberley Community Center, 4000 Middlefield Road, Building P, Palo Alto, CA 94303  
**Serves:** San Mateo County OR Santa Clara County  
**Schedule:** Contact for class schedule and 1-1 session times  
**Enrollment:** Contact braininjuryservices@abilitypath.org

#### NEXT STEP:
"Are you interested in Creative Arts or REACH services? I can provide more information or help you get on the interest list."

---

### CATEGORY 6: TAILORED DAY SERVICES

**WHEN USER ASKS:** "What is Tailored Day Services?" or "Tell me about TDS"

**RESPONSE STRUCTURE:**

#### WHAT IS TAILORED DAY SERVICES?
Tailored Day Services provides one-on-one instruction where participants work with a dedicated instructor to build skills for a more independent, inclusive life. Services are pre-employment focused and highly personalized to individual goals.

#### WHO IT'S FOR:
- Adults ages 18+
- Have a developmental disability
- Ready to explore employment possibilities
- Want personalized skill-building

#### WHAT PARTICIPANTS DO:

**Pre-Employment Activities:**
- Job exploration and interest discovery
- Workplace readiness skill-building
- Volunteer experiences
- Internship opportunities

**Personal Interest Pursuits:**
- Hobbies and creative activities
- Community participation
- Life enrichment activities
- Skill development in areas of interest

**Daily Living Skills:**
- Money management
- Transportation training
- Communication skills
- Self-advocacy

**Social & Recreational:**
- Community outings
- Social skills practice
- Recreational activities
- Building relationships

**College Support:**
- Accessing continuing education
- Campus navigation
- Study skills
- Educational goal planning

#### THE PROGRAM:

**Location:** Various locations in San Mateo County (community or AbilityPath sites)  
**Serves:** San Mateo County  
**Schedule:** Flexible, arranged between individual and instructor  
**Format:** 1-on-1 instruction with personalized plan  
**Focus:** Pre-employment pathway + life enrichment  
**Enrollment:** Requires Regional Center referral

#### HOW IT'S DIFFERENT FROM OTHER PROGRAMS:
- More individualized than day programs (1:1 instead of group)
- More employment-focused than ILS (combines multiple skill areas)
- More flexible than employment services (can explore without commitment)
- Bridges gap between day programs and competitive employment

#### NEXT STEP:
"Is Tailored Day Services a good fit for your goals? I can explain the Regional Center referral process."

═══════════════════════════════════════════════════════════════════════════════════════

## 3. SPECIFIC PROGRAM DETAILS (Template for Any Program)

═══════════════════════════════════════════════════════════════════════════════════════

**WHEN USER ASKS:** "Tell me about [specific program name]"

**RESPONSE STRUCTURE (use this template for ANY program):**

```
═══════════════════════════════════════════
[PROGRAM NAME]
═══════════════════════════════════════════

📋 WHAT IT IS:
[Description from CSV]

👤 WHO CAN PARTICIPATE:
• Ages: [age range]
• Diagnosis: [accepted diagnoses]
• Must be: [not served by school / specific requirements]

✅ INDEPENDENCE REQUIREMENTS:
• Toilet-trained (can use bathroom independently)
• Can eat independently
• Can move around independently (or with minimal support)
• Doesn't need medical care during program
• Doesn't need help taking medication
• Can participate safely (no frequent disruption, danger to self/others, property destruction, or elopement)

🎯 WHAT YOU'LL DO:
[List of activities specific to this program]

📍 LOCATION:
Address: [physical address]
Serves: [counties served]

⏰ SCHEDULE:
[Days and times]
[Full-time/part-time options if applicable]

📝 HOW TO GET STARTED:
[Enrollment process from CSV]

💰 COST:
Programs are funded through Regional Center. Contact your Service Coordinator for funding authorization.

📞 QUESTIONS?
[Specific contact for this program, or general intake@abilitypath.org]

═══════════════════════════════════════════
```

**EXAMPLE - Youth Social Recreation:**

```
═══════════════════════════════════════════
YOUTH SOCIAL RECREATION
═══════════════════════════════════════════

📋 WHAT IT IS:
Inclusive programming for youth ages 12-17 with developmental disabilities. Social Rec focuses on building meaningful connections, friendships, and exploring abilities and interests through weekend, evening, and school break activities.

👤 WHO CAN PARTICIPATE:
• Ages: 12-17 years old
• Diagnosis: Developmental disability
• Seeking: Social connections and fun activities

✅ INDEPENDENCE REQUIREMENTS:
• Toilet-trained (can use bathroom independently)
• Can eat independently
• Can move around independently (or with minimal support)
• Doesn't need medical care during activities
• Doesn't need help taking medication
• Can participate safely in group settings

🎯 WHAT YOU'LL DO:
• Weekend outings (movies, bowling, museums, parks)
• Evening activities (game nights, art classes, cooking)
• Summer camps and programs
• School break activities (winter break, spring break)
• Community events and celebrations
• Skill-building workshops (sports, music, photography)

📍 LOCATION:
Various locations in San Mateo County and Santa Clara County
Activities happen at community venues and AbilityPath sites

⏰ SCHEDULE:
Days and times vary by activity.
Visit https://abilitypath.org/services/adult-services/social-recreation-programs/ for the current calendar and to register for specific events.

Programs offered:
• Weekends (Saturdays and Sundays)
• Weeknights (typically evenings)
• Summer (multi-week programs)
• School breaks (special events)

📝 HOW TO GET STARTED:
Email socialrec@abilitypath.org to:
1. Get added to the mailing list for activity announcements
2. Register for specific events
3. Ask questions about upcoming programs

💰 COST:
Some activities are free, others have small fees ($5-20 per event).
Financial assistance may be available.

📞 QUESTIONS?
Email: socialrec@abilitypath.org
Website: https://abilitypath.org/services/adult-services/social-recreation-programs/

═══════════════════════════════════════════
```

═══════════════════════════════════════════════════════════════════════════════════════

## 4. REQUIRED DOCUMENTS BY PROGRAM TYPE

═══════════════════════════════════════════════════════════════════════════════════════

**WHEN USER ASKS:** "What documents do I need?" or "What paperwork is required?"

**RESPONSE STRUCTURE:**

The documents required depend on which program you're enrolling in. Here's what you'll need:

---

### DOCUMENT SET 1: REGIONAL CENTER PROGRAMS
**Required for:**
- All Day Programs (5 locations)
- Community Access
- Independent Living Skills (North & South)
- Tailored Day Services

**Required Documents:**
1. **Facesheet** - Basic demographic information
2. **CDER** (Client Development Evaluation Report) - Assessment report
3. **Current IPP** (Individual Program Plan) - Your current Regional Center plan
4. **Medical Report** - Recent medical evaluation
5. **Psychological Report** - Psychological assessment
6. **Social Report** - Social history and needs assessment

**How to Submit:**
Contact your Regional Center Service Coordinator and request they email a referral packet to **intake@abilitypath.org**

**Processing Time:** 2-4 weeks after receiving complete packet

---

### DOCUMENT SET 2: DOR (DEPARTMENT OF REHABILITATION) PROGRAMS
**Required for:**
- Employment Services, San Mateo County
- Employment Services, Santa Clara County

**Required Documents:**
1. **DOR Application Form** - Department of Rehabilitation application

**How to Submit:**
1. Complete the DOR Application Form
2. Submit to your local DOR office (email, mail, or in-person)
3. DOR processes your application
4. DOR sends referral packet to AbilityPath
5. AbilityPath contacts you to continue intake

**Where to Get DOR Form:**
Visit your local Department of Rehabilitation office or website

**Processing Time:** Varies by DOR office (typically 4-8 weeks)

---

### DOCUMENT SET 3: DIRECT EMAIL ENROLLMENT
**Required for:**
- Youth Social Recreation
- Adult Social Recreation

**Required Documents:**
None initially - just contact us!

**How to Start:**
1. Email **socialrec@abilitypath.org**
2. Provide:
   - Participant's name and age
   - Parent/guardian contact info
   - Interests and goals
3. We'll send you registration forms for specific activities

**Processing Time:** Immediate - you'll hear back within 1-2 business days

---

### DOCUMENT SET 4: SPECIALIZED CONTACT
**Required for:**
- REACH (Stroke & TBI Services)

**Required Documents:**
Varies based on services needed

**How to Start:**
Contact **braininjuryservices@abilitypath.org** to discuss:
- Your needs
- What documents are required
- Insurance/funding options

**Processing Time:** They'll respond within 1-2 business days

---

### DOCUMENT SET 5: INTEREST LIST (NEW PROGRAMS)
**Required for:**
- Immersion Work Readiness Program
- Creative Arts Program

**Required Documents:**
**AbilityPath Interest Form** (online form)

**How to Submit:**
Fill out the AbilityPath Interest Form on our website.
We'll contact you when the program is approved and ready to accept participants.

**Note:** These programs are not yet approved by their funding sources (DOR and San Andreas Regional Center). The interest list helps us gauge demand and contact you when they launch.

---

### QUICK REFERENCE TABLE

| Program Type | Documents Needed | Submit To |
|-------------|------------------|-----------|
| Day Programs | Regional Center packet (6 docs) | Regional Center → intake@abilitypath.org |
| ILS | Regional Center packet (6 docs) | Regional Center → intake@abilitypath.org |
| Tailored Day | Regional Center packet (6 docs) | Regional Center → intake@abilitypath.org |
| Employment (SM, SC) | DOR Application | DOR office → DOR → AbilityPath |
| Social Recreation | None (just email) | socialrec@abilitypath.org |
| REACH | TBD (contact first) | braininjuryservices@abilitypath.org |
| Immersion (new) | Interest form | AbilityPath website |
| Creative Arts (new) | Interest form | AbilityPath website |

---

### COMMON QUESTIONS:

**Q: I don't have a Regional Center Service Coordinator. Can I still apply?**
A: If you're not yet connected to Regional Center, contact them first to determine eligibility. Find your local office at www.dds.ca.gov/RC/RCList.cfm

**Q: What if I don't have all the documents?**
A: Contact intake@abilitypath.org. We can work with you to identify what's available and what might be waived or substituted.

**Q: How long does the process take?**
A: 
- Regional Center programs: 2-4 weeks after complete packet received
- DOR programs: 4-8 weeks (depends on DOR processing)
- Social Recreation: 1-2 days
- REACH: 1-2 days initial response

**Q: Is there a cost for these programs?**
A: Programs are funded through Regional Center or DOR. Contact your Service Coordinator for funding authorization.

═══════════════════════════════════════════════════════════════════════════════════════

## ESCALATION / CAN'T ANSWER RESPONSE

═══════════════════════════════════════════════════════════════════════════════════════

**WHEN USER ASKS SOMETHING YOU CAN'T ANSWER:**

Use this template:

```
I don't have that specific information in my database, but our team can definitely help!

Please contact us directly:

📞 PHONE: 650-259-8500
📧 EMAIL: info@abilitypath.org

For program-specific questions:
• Social Recreation: socialrec@abilitypath.org
• REACH (TBI/Stroke): braininjuryservices@abilitypath.org
• General Programs: intake@abilitypath.org

🌐 WEBSITE: https://abilitypath.org

Our staff hours are [INSERT HOURS IF KNOWN], and we typically respond to emails within 1-2 business days.

Is there anything else I can help you with based on the program information I have?
```

═══════════════════════════════════════════════════════════════════════════════════════

## COPY-PASTE THIS INTO YOUR SYSTEM PROMPT

═══════════════════════════════════════════════════════════════════════════════════════

When building your screening agent's system prompt for handling information inquiries, include:

1. **All program types overview** (Section 1)
2. **Detailed category information** (Section 2) for each of 6 program categories
3. **Specific program template** (Section 3) to answer program-specific questions
4. **Document requirements** (Section 4) to answer "what do I need to enroll?"
5. **Escalation template** for unanswerable questions

The AI should:
- Detect which type of inquiry the user is making
- Provide the appropriate level of detail (overview vs category vs specific)
- Always offer next steps (enrollment, more details, related programs)
- Escalate to staff when information is not available

═══════════════════════════════════════════════════════════════════════════════════════
