"""
Agent Evaluation Script
Run automated tests to evaluate agent performance
"""

from screening_agent import ScreeningAgent
import os
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

load_dotenv()

# Test cases with expected results
TEST_CASES = [
    {
        "name": "Maria & Kevin - Young Adult Transition",
        "messages": [
            "Hi, my son Kevin is 22 and just graduated high school.",
            "He needs daytime support while I work and job training.",
        ],
        "expected_age": 22,
        "expected_needs": ["recently_graduated", "needs_daytime_support", "seeking_employment"],
        "expected_program_ids": ["transition_services", "adult_day_program", "vocational_training"]
    },
    {
        "name": "Early Intervention - Toddler",
        "messages": [
            "My 2-year-old daughter has developmental delays.",
        ],
        "expected_age": 2,
        "expected_needs": ["developmental_delay"],
        "expected_program_ids": ["early_intervention"]
    },
    {
        "name": "Behavioral Support - School Age",
        "messages": [
            "We need help with our 10-year-old son who has autism and challenging behaviors.",
            "We need intensive support and respite care for our family.",
        ],
        "expected_age": 10,
        "expected_needs": ["has_challenging_behaviors", "needs_intensive_support", "has_family_caregiver"],
        "expected_program_ids": ["behavioral_services", "respite_care"]
    },
    {
        "name": "Adult Employment",
        "messages": [
            "My 28-year-old brother wants to get a job. He can work with support.",
        ],
        "expected_age": 28,
        "expected_needs": ["seeking_employment", "can_work_with_support"],
        "expected_program_ids": ["vocational_training"]
    },
]


def run_single_test(test_case, api_key):
    """Run a single test case"""
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}Testing: {test_case['name']}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    agent = ScreeningAgent(api_key)
    
    # Run through messages
    for i, msg in enumerate(test_case['messages'], 1):
        print(f"\n{Fore.YELLOW}Message {i}: {msg}{Style.RESET_ALL}")
        result = agent.chat(msg)
        print(f"{Fore.BLUE}Agent: {result['response'][:100]}...{Style.RESET_ALL}")
    
    # Get collected info
    collected_info = agent.collected_info
    
    # Evaluate age
    age_correct = collected_info['age'] == test_case['expected_age']
    age_status = f"{Fore.GREEN}✅" if age_correct else f"{Fore.RED}❌"
    
    # Evaluate needs
    extracted_needs = set(collected_info['needs'].keys())
    expected_needs = set(test_case['expected_needs'])
    needs_found = extracted_needs & expected_needs
    needs_missing = expected_needs - extracted_needs
    needs_extra = extracted_needs - expected_needs
    
    # Calculate needs score
    needs_score = len(needs_found) / len(expected_needs) if expected_needs else 0
    needs_status = f"{Fore.GREEN}✅" if needs_score >= 0.8 else f"{Fore.YELLOW}⚠️" if needs_score >= 0.5 else f"{Fore.RED}❌"
    
    # Print evaluation
    print(f"\n{Fore.MAGENTA}{'─'*70}")
    print(f"{Fore.MAGENTA}EVALUATION RESULTS:")
    print(f"{Fore.MAGENTA}{'─'*70}{Style.RESET_ALL}")
    
    print(f"\n{age_status} Age Extraction:{Style.RESET_ALL}")
    print(f"   Extracted: {collected_info['age']}")
    print(f"   Expected: {test_case['expected_age']}")
    
    print(f"\n{needs_status} Needs Extraction ({needs_score*100:.0f}%):{Style.RESET_ALL}")
    print(f"   Found: {list(needs_found) if needs_found else 'None'}")
    print(f"   Missing: {list(needs_missing) if needs_missing else 'None'}")
    print(f"   Extra: {list(needs_extra) if needs_extra else 'None'}")
    
    # Overall result
    overall_pass = age_correct and needs_score >= 0.8
    
    return {
        "name": test_case['name'],
        "age_correct": age_correct,
        "needs_score": needs_score,
        "passed": overall_pass
    }


def print_summary(results):
    """Print summary of all tests"""
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}SUMMARY")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    total = len(results)
    passed = sum(1 for r in results if r['passed'])
    age_correct = sum(1 for r in results if r['age_correct'])
    avg_needs_score = sum(r['needs_score'] for r in results) / total if total > 0 else 0
    
    # Overall stats
    overall_status = f"{Fore.GREEN}✅ PASSED" if passed == total else f"{Fore.YELLOW}⚠️ PARTIAL" if passed > 0 else f"{Fore.RED}❌ FAILED"
    
    print(f"{overall_status}{Style.RESET_ALL}")
    print(f"\n📊 Overall Results:")
    print(f"   Tests passed: {passed}/{total} ({passed/total*100:.0f}%)")
    print(f"   Age extraction: {age_correct}/{total} ({age_correct/total*100:.0f}%)")
    print(f"   Avg needs score: {avg_needs_score*100:.0f}%")
    
    # Individual results
    print(f"\n📋 Individual Test Results:")
    for r in results:
        status = f"{Fore.GREEN}✅" if r['passed'] else f"{Fore.RED}❌"
        print(f"   {status} {r['name']}{Style.RESET_ALL}")
        print(f"      Age: {'✓' if r['age_correct'] else '✗'}, Needs: {r['needs_score']*100:.0f}%")
    
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")


def main():
    """Run all tests"""
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print(f"{Fore.RED}❌ ERROR: OPENAI_API_KEY not found in .env file{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.GREEN}{'='*70}")
    print(f"{Fore.GREEN}🧪 AbilityPath Agent Evaluation Suite")
    print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
    print(f"\n📝 Running {len(TEST_CASES)} test cases...")
    
    results = []
    
    for test_case in TEST_CASES:
        result = run_single_test(test_case, api_key)
        results.append(result)
    
    print_summary(results)


if __name__ == "__main__":
    # Install colorama if not available
    try:
        from colorama import Fore, Style, init
    except ImportError:
        print("Installing colorama for colored output...")
        os.system("pip3 install colorama")
        from colorama import Fore, Style, init
    
    main()
