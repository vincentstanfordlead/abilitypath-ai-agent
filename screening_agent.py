"""
AI Screening Agent using LangChain
This is the core AI that conducts conversations and makes program recommendations
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from programs_database import filter_programs_by_criteria, format_program_recommendations
import json


class ScreeningAgent:
    """
    AI Agent that conducts eligibility screening conversations
    """
    
    def __init__(self, openai_api_key):
        """Initialize the screening agent with OpenAI"""
        
        # Initialize the LLM (Language Model)
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",  # Using GPT-3.5 for cost efficiency
            temperature=0.7,  # Some creativity but mostly consistent
            openai_api_key=openai_api_key
        )
        
        # Conversation memory to track the dialogue
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Information collected during screening
        self.collected_info = {
            "name": None,
            "age": None,
            "needs": {}
        }
        
        # Screening questions to ask
        self.questions_asked = set()
        
    def create_system_prompt(self):
        """Create the system prompt that defines the AI's behavior"""
        
        return ChatPromptTemplate.from_messages([
            ("system", """You are a warm, empathetic intake specialist for AbilityPath, 
            a Bay Area organization serving individuals with developmental disabilities.
            
            Your role is to:
            1. Welcome families warmly and make them feel heard
            2. Gather essential information through natural conversation:
               - Individual's name and age
               - Current needs and challenges
               - What kind of support they're looking for
            3. Be compassionate - many families are stressed and overwhelmed
            4. Ask follow-up questions naturally, one at a time
            5. Once you have enough information, offer to find matching programs
            
            IMPORTANT GUIDELINES:
            - Be conversational and empathetic, not robotic
            - Don't ask all questions at once - have a natural dialogue
            - Show you understand their situation (like Maria & Kevin's story)
            - When ready, say "Let me find the best programs for you"
            
            Keep responses concise and caring."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
    
    def reset_conversation(self):
        """Reset the conversation for a new screening"""
        self.memory.clear()
        self.collected_info = {
            "name": None,
            "age": None,
            "needs": {}
        }
        self.questions_asked = set()
    
    def extract_information(self, user_message, ai_response):
        """
        Extract structured information from the conversation
        This is a simple version - production would use more sophisticated NLP
        """
        
        user_lower = user_message.lower()
        
        # Extract age
        if "year" in user_lower or "age" in user_lower:
            words = user_message.split()
            for i, word in enumerate(words):
                if word.isdigit():
                    age = int(word)
                    if 0 <= age <= 120:
                        self.collected_info["age"] = age
                        break
        
        # Extract needs based on keywords
        needs_keywords = {
            "developmental_delay": ["delay", "delayed", "behind", "developmental"],
            "requires_behavioral_support": ["behavior", "behavioral", "challenging", "tantrum"],
            "requires_mobility_support": ["mobility", "wheelchair", "walker", "physical"],
            "requires_social_skills_support": ["social", "friends", "interaction", "isolated"],
            "needs_daytime_support": ["daytime", "day program", "during day", "while i work"],
            "can_participate_in_groups": ["group", "class", "social"],
            "recently_graduated": ["graduated", "finished school", "out of school", "22"],
            "seeking_employment": ["job", "work", "employment", "career"],
            "can_work_with_support": ["with support", "job coach", "help working"],
            "lives_independently": ["lives alone", "apartment", "independent"],
            "needs_ongoing_support": ["ongoing", "regular", "continued"],
            "has_challenging_behaviors": ["aggressive", "self-harm", "dangerous", "severe behavior"],
            "needs_intensive_support": ["intensive", "24/7", "constant", "full-time"],
            "has_family_caregiver": ["i care", "i'm caring", "family cares", "parent", "mom", "dad"],
            "seeks_social_activities": ["activities", "fun", "recreation", "friends", "social"]
        }
        
        for need, keywords in needs_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                self.collected_info["needs"][need] = True
    
    def check_if_ready_to_match(self):
        """Determine if we have enough information to make recommendations"""
        return (
            self.collected_info["age"] is not None and
            len(self.collected_info["needs"]) >= 2  # At least 2 needs identified
        )
    
    def get_program_recommendations(self):
        """Get matching programs based on collected information"""
        
        if not self.check_if_ready_to_match():
            return None
        
        age = self.collected_info["age"]
        needs = self.collected_info["needs"]
        
        matches = filter_programs_by_criteria(age, needs)
        return format_program_recommendations(matches)
    
    def chat(self, user_message):
        """
        Main chat method - processes user input and returns AI response
        """
        
        # Extract information from user message
        self.extract_information(user_message, "")
        
        # Check if user is asking for recommendations
        user_lower = user_message.lower()
        ready_keywords = ["what program", "find program", "recommend", "help me", "what can", "options"]
        user_wants_recommendations = any(keyword in user_lower for keyword in ready_keywords)
        
        # If we have enough info and user wants recommendations
        if self.check_if_ready_to_match() and user_wants_recommendations:
            recommendations = self.get_program_recommendations()
            
            if recommendations:
                return {
                    "response": recommendations + "\n\nWould you like more details about any of these programs, or shall I connect you with our enrollment team?",
                    "recommendations_provided": True,
                    "collected_info": self.collected_info
                }
        
        # Otherwise, continue conversation
        prompt = self.create_system_prompt()
        
        conversation = LLMChain(
            llm=self.llm,
            prompt=prompt,
            memory=self.memory,
            verbose=False
        )
        
        try:
            response = conversation.predict(input=user_message)
            
            # Extract info from AI response too
            self.extract_information(user_message, response)
            
            return {
                "response": response,
                "recommendations_provided": False,
                "collected_info": self.collected_info
            }
            
        except Exception as e:
            return {
                "response": f"I apologize, but I encountered an error: {str(e)}. Let me connect you with a team member who can help.",
                "error": str(e)
            }


# Simple test function
def test_agent():
    """Test the agent with a sample conversation"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Please set OPENAI_API_KEY in .env file")
        return
    
    agent = ScreeningAgent(api_key)
    
    print("AbilityPath Screening Agent Test")
    print("=" * 50)
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            break
        
        result = agent.chat(user_input)
        print(f"\nAgent: {result['response']}\n")
        
        if result.get('recommendations_provided'):
            print(f"\n[Info collected: {result['collected_info']}]\n")


if __name__ == "__main__":
    test_agent()
