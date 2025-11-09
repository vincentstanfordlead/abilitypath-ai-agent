"""
AI Screening Agent using LangChain - COMPLETE REVISION
Supports all AbilityPath requirements:
1. Greet users and detect their intent
2. Provide specific program information
3. Conduct enrollment screening with matching
4. Answer general questions
5. Escalate to staff when needed
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from programs_database import (
    filter_programs_by_criteria, 
    format_program_recommendations,
    get_program_by_name,
    PROGRAMS
)
import json
import re


class ScreeningAgent:
    """
    AI Agent that handles 3 main user flows:
    1. Learn about programs (informational)
    2. Enroll in programs (screening + matching)
    3. Ask questions (Q&A with escalation)
    """
    
    def __init__(self, openai_api_key):
        """Initialize the screening agent with OpenAI"""
        
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=openai_api_key
        )
        
        # Conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # User intent: 'learn', 'enroll', 'question', or None
        self.user_intent = None
        
        # Information collected during enrollment screening
        self.collected_info = {
            "age": None,
            "diagnosis": None,
            "location": None,
            "interests": [],
            "support_needs": {}
        }
        
        # Track if recommendations provided
        self.recommendations_given = False
        
    def create_system_prompt(self):
        """Create dynamic system prompt with all program information"""
        
        # Build comprehensive program context
        programs_context = self._build_programs_context()
        
        return ChatPromptTemplate.from_messages([
            ("system", f"""You are a warm, helpful intake specialist for AbilityPath, 
a Bay Area nonprofit serving individuals with developmental disabilities.

=== AVAILABLE PROGRAMS ===
{programs_context}

=== YOUR RESPONSIBILITIES ===

1. GREET & UNDERSTAND INTENT
   First message: Warmly greet the user and ask what brings them here today.
   Detect if they want to:
   - Learn more about programs
   - Enroll in a program
   - Ask a question

2. PROVIDE SPECIFIC PROGRAM INFO
   When users ask about a specific program (e.g., "Tell me about Youth Social Recreation"):
   - Provide the EXACT program details from the list above
   - Include: description, ages, location, schedule, how to enroll
   - Be thorough and accurate

3. ENROLLMENT SCREENING (when user says they're ready to enroll)
   Ask for these criteria ONE AT A TIME in natural conversation:
   - Age of the individual
   - Diagnosis (developmental disability, intellectual disability, autism, TBI, stroke, etc.)
   - Location/County (San Mateo, Santa Clara, San Francisco, etc.)
   - Interests (employment, living skills, social activities, day programs, etc.)
   - Support needs (toilet-trained, eating independence, mobility, behavioral needs)
   
   Once you have Age, Diagnosis, and Location, say: 
   "Let me find the best programs for you based on what you've shared."

4. ANSWER QUESTIONS
   Use the program information above to answer questions about:
   - Services offered
   - Locations served
   - Age requirements
   - Enrollment processes
   - Schedules and availability

5. ESCALATE WHEN NEEDED
   If you cannot answer a question with the information provided, say:
   "I don't have that specific information, but our team can help! 
   Please contact us:
   Phone: 650-259-8500
   Email: info@abilitypath.org"

=== IMPORTANT GUIDELINES ===
- Be conversational, warm, and empathetic
- Ask ONE question at a time (don't overwhelm)
- Use the exact program details I provided
- Don't make up information
- When unsure, escalate to staff contact

=== CONTACT INFO FOR ESCALATION ===
Phone: 650-259-8500
Email: info@abilitypath.org
Specific programs:
- Social Recreation: socialrec@abilitypath.org
- REACH (TBI/Stroke): braininjuryservices@abilitypath.org

Keep responses clear and helpful."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
    
    def _build_programs_context(self):
        """Build comprehensive context of all programs for AI"""
        context_parts = []
        
        for i, program in enumerate(PROGRAMS, 1):
            # Format age range
            age_range = program.get('age_range', {})
            min_age = age_range.get('min_age')
            max_age = age_range.get('max_age')
            
            if min_age and max_age:
                age_str = f"{min_age}-{max_age} years old"
            elif min_age:
                age_str = f"{min_age}+ years old"
            else:
                age_str = "All ages"
            
            # Get other details
            diagnosis = ', '.join(program.get('diagnosis_accepted', ['Not specified']))
            counties = ', '.join(program.get('counties_served', ['Not specified']))
            program_types = ', '.join(program.get('program_type', ['General']))
            
            # Build program entry
            context_parts.append(f"""
PROGRAM #{i}: {program['name']}
Description: {program.get('description', 'N/A')}
Ages: {age_str}
Diagnosis Accepted: {diagnosis}
Program Type: {program_types}
Location: {program.get('location', 'N/A')}
Counties Served: {counties}
Physical Location: {program.get('physical_location', 'Various locations')}
Schedule: {program.get('schedule', 'Contact for details')}
How to Enroll: {program.get('enrollment_process', 'Contact AbilityPath')}
---""")
        
        return '\n'.join(context_parts)
    
    def reset_conversation(self):
        """Reset for new conversation"""
        self.memory.clear()
        self.user_intent = None
        self.collected_info = {
            "age": None,
            "diagnosis": None,
            "location": None,
            "interests": [],
            "support_needs": {}
        }
        self.recommendations_given = False
    
    def _extract_information(self, user_message):
        """Extract enrollment criteria from user message"""
        message_lower = user_message.lower()
        
        # Extract AGE
        age_patterns = [
            r'(\d+)\s*years?\s*old',
            r'age\s*(?:is\s*)?(\d+)',
            r'(?:he|she|they|i)(?:\'s|\s+is|\s+am)\s*(\d+)',
            r'\b(\d+)\s*(?:year|yr)',
        ]
        
        for pattern in age_patterns:
            match = re.search(pattern, message_lower)
            if match:
                age = int(match.group(1))
                if 0 <= age <= 120:
                    self.collected_info['age'] = age
                    print(f"DEBUG: Extracted age: {age}")
                    break
        
        # Extract DIAGNOSIS
        diagnosis_map = {
            'developmental disability': ['developmental disability', 'developmental delay', 'dd', 'developmentally disabled'],
            'intellectual disability': ['intellectual disability', 'id', 'cognitive disability', 'mentally disabled'],
            'autism': ['autism', 'autistic', 'asd', 'autism spectrum', 'on the spectrum'],
            'down syndrome': ['down syndrome', 'downs syndrome', 'trisomy 21'],
            'cerebral palsy': ['cerebral palsy', 'cp'],
            'traumatic brain injury': ['traumatic brain injury', 'tbi', 'brain injury'],
            'stroke': ['stroke', 'cva', 'cerebrovascular'],
        }
        
        for diagnosis, keywords in diagnosis_map.items():
            if any(keyword in message_lower for keyword in keywords):
                self.collected_info['diagnosis'] = diagnosis
                print(f"DEBUG: Extracted diagnosis: {diagnosis}")
                break
        
        # Extract LOCATION
        location_map = {
            'san mateo': ['san mateo', 'burlingame', 'daly city', 'foster city', 'redwood city'],
            'santa clara': ['santa clara', 'san jose', 'palo alto', 'mountain view', 'sunnyvale', 'cupertino'],
            'san francisco': ['san francisco', 'sf'],
        }
        
        for location, keywords in location_map.items():
            if any(keyword in message_lower for keyword in keywords):
                self.collected_info['location'] = location
                print(f"DEBUG: Extracted location: {location}")
                break
        
        # Extract INTERESTS
        interest_map = {
            'employment': ['job', 'work', 'employment', 'career', 'vocational', 'working'],
            'living skills': ['living skills', 'independent living', 'life skills', 'daily living', 'cooking', 'budgeting', 'independence'],
            'social': ['social', 'friends', 'friendship', 'recreation', 'activities', 'fun', 'meet people'],
            'day program': ['day program', 'day service', 'daytime', 'structured activities', 'during the day'],
        }
        
        for interest, keywords in interest_map.items():
            if any(keyword in message_lower for keyword in keywords):
                if interest not in self.collected_info['interests']:
                    self.collected_info['interests'].append(interest)
                    print(f"DEBUG: Extracted interest: {interest}")
        
        # Extract SUPPORT NEEDS
        if any(word in message_lower for word in ['toilet', 'bathroom']):
            is_independent = any(word in message_lower for word in ['independent', 'doesn\'t need', 'don\'t need', 'can use'])
            self.collected_info['support_needs']['toilet_trained'] = is_independent
        
        if any(word in message_lower for word in ['eating', 'feeding']):
            is_independent = any(word in message_lower for word in ['independent', 'doesn\'t need', 'don\'t need'])
            self.collected_info['support_needs']['eating_independence'] = is_independent
    
    def _check_if_ready_to_match(self):
        """Check if we have minimum info for matching"""
        has_age = self.collected_info['age'] is not None
        has_diagnosis = self.collected_info['diagnosis'] is not None
        has_location = self.collected_info['location'] is not None
        
        print(f"DEBUG: Ready check - Age: {has_age}, Diagnosis: {has_diagnosis}, Location: {has_location}")
        
        return has_age and has_diagnosis and has_location
    
    def _get_recommendations(self):
        """Generate program recommendations"""
        
        if not self._check_if_ready_to_match():
            return None
        
        # Build user profile
        user_profile = {
            'age': self.collected_info['age'],
            'diagnosis': self.collected_info['diagnosis'],
            'location': self.collected_info['location'],
            'interests': self.collected_info['interests'],
            'support_needs': self.collected_info['support_needs']
        }
        
        print(f"DEBUG: Matching with profile: {user_profile}")
        
        # Get matches
        recommendations = filter_programs_by_criteria(user_profile)
        
        print(f"DEBUG: Found {len(recommendations)} matches")
        
        if recommendations:
            # Format and return top 3-5 matches
            return format_program_recommendations(recommendations, max_programs=5)
        else:
            return """I couldn't find programs that match all your criteria. This might be because:
- Your location is outside our current service areas
- The age doesn't match our program offerings
- We need more information to find the right fit

Please contact our team directly for personalized assistance:
Phone: 650-259-8500
Email: info@abilitypath.org

Our staff can discuss specialized options and accommodations."""
    
    def _handle_specific_program_query(self, user_message):
        """Check if user is asking about a specific program"""
        message_lower = user_message.lower()
        
        for program in PROGRAMS:
            program_name_lower = program['name'].lower()
            
            # Check if program name is mentioned
            if program_name_lower in message_lower:
                return self._format_program_details(program)
        
        return None
    
    def _format_program_details(self, program):
        """Format detailed information about a specific program"""
        # Format age range
        age_range = program.get('age_range', {})
        min_age = age_range.get('min_age')
        max_age = age_range.get('max_age')
        
        if min_age and max_age:
            age_str = f"{min_age}-{max_age} years old"
        elif min_age:
            age_str = f"{min_age}+ years old"
        else:
            age_str = "All ages"
        
        output = f"""
{'='*70}
{program['name']}
{'='*70}

📋 DESCRIPTION:
{program.get('description', 'No description available.')}

👤 ELIGIBILITY:
• Ages: {age_str}
• Diagnosis: {', '.join(program.get('diagnosis_accepted', ['Not specified']))}
• Program Type: {', '.join(program.get('program_type', ['General support']))}

📍 LOCATION:
{program.get('physical_location', 'Various locations in the community')}
Counties Served: {', '.join(program.get('counties_served', ['Contact for details']))}

⏰ SCHEDULE:
{program.get('schedule', 'Contact program for schedule information')}

✅ SUPPORT REQUIREMENTS:
"""
        
        # Add support requirements if available
        support_reqs = program.get('support_requirements', {})
        if support_reqs:
            if support_reqs.get('toilet_trained'):
                output += "• Must be toilet-trained/bathroom independent\n"
            if support_reqs.get('eating_independence'):
                output += "• Must eat independently\n"
            if support_reqs.get('mobility_independence'):
                output += "• Must have mobility independence or minimal support\n"
            if support_reqs.get('behavioral_requirements'):
                output += "• Behavioral requirements:\n"
                for req in support_reqs['behavioral_requirements']:
                    output += f"  - {req}\n"
        else:
            output += "Contact program for specific requirements\n"
        
        output += f"""
📝 HOW TO GET STARTED:
{program.get('enrollment_process', 'Contact AbilityPath for enrollment information')}

{'='*70}

Would you like to enroll in this program, or do you have other questions?
"""
        return output
    
    def chat(self, user_message):
        """
        Main chat method - handles all conversation logic
        """
        
        print(f"\nDEBUG: User message: {user_message}")
        print(f"DEBUG: Current intent: {self.user_intent}")
        print(f"DEBUG: Collected info: {self.collected_info}")
        
        # Check for specific program inquiry first
        specific_program_info = self._handle_specific_program_query(user_message)
        if specific_program_info:
            return {
                "response": specific_program_info,
                "recommendations_provided": False,
                "collected_info": self.collected_info
            }
        
        # Detect enrollment intent
        enroll_keywords = ['enroll', 'sign up', 'register', 'apply', 'ready to join', 'find a program', 'need help finding']
        if any(keyword in user_message.lower() for keyword in enroll_keywords):
            self.user_intent = 'enroll'
            print("DEBUG: Set intent to 'enroll'")
        
        # Extract information if in enrollment mode
        if self.user_intent == 'enroll':
            self._extract_information(user_message)
            
            # Check if ready to provide recommendations
            if self._check_if_ready_to_match() and not self.recommendations_given:
                # Look for trigger to show recommendations
                trigger_keywords = ['recommend', 'find', 'match', 'show', 'what programs', 'help me']
                
                if any(keyword in user_message.lower() for keyword in trigger_keywords):
                    print("DEBUG: Trigger detected - generating recommendations")
                    recommendations = self._get_recommendations()
                    
                    if recommendations:
                        self.recommendations_given = True
                        return {
                            "response": recommendations,
                            "recommendations_provided": True,
                            "collected_info": self.collected_info
                        }
        
        # Continue conversation with LLM
        prompt = self.create_system_prompt()
        
        conversation = LLMChain(
            llm=self.llm,
            prompt=prompt,
            memory=self.memory,
            verbose=False
        )
        
        try:
            response = conversation.predict(input=user_message)
            
            print(f"DEBUG: LLM response: {response[:100]}...")
            
            # Check if AI says it's ready to find programs
            if "let me find" in response.lower() and self._check_if_ready_to_match() and not self.recommendations_given:
                print("DEBUG: AI triggered recommendations")
                recommendations = self._get_recommendations()
                
                if recommendations:
                    self.recommendations_given = True
                    # Combine AI's message with recommendations
                    combined = response + "\n\n" + recommendations
                    
                    return {
                        "response": combined,
                        "recommendations_provided": True,
                        "collected_info": self.collected_info
                    }
            
            return {
                "response": response,
                "recommendations_provided": False,
                "collected_info": self.collected_info
            }
            
        except Exception as e:
            print(f"ERROR in chat: {e}")
            return {
                "response": """I apologize, but I encountered a technical issue. 
Please contact our team directly for assistance:
Phone: 650-259-8500
Email: info@abilitypath.org

Our staff will be happy to help you!""",
                "error": str(e),
                "recommendations_provided": False
            }


# Test function
def test_agent():
    """Test the agent"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Please set OPENAI_API_KEY in .env file")
        return
    
    agent = ScreeningAgent(api_key)
    
    print("="*70)
    print("AbilityPath Screening Agent - Interactive Test")
    print("="*70)
    print("Commands: 'quit' to exit, 'reset' to start over\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit']:
            break
        
        if user_input.lower() == 'reset':
            agent.reset_conversation()
            print("\n✅ Conversation reset\n")
            continue
        
        result = agent.chat(user_input)
        print(f"\nAgent: {result['response']}\n")
        
        if result.get('recommendations_provided'):
            print(f"✅ Recommendations provided!")
            print(f"Collected: Age={result['collected_info']['age']}, "
                  f"Diagnosis={result['collected_info']['diagnosis']}, "
                  f"Location={result['collected_info']['location']}\n")


if __name__ == "__main__":
    test_agent()
