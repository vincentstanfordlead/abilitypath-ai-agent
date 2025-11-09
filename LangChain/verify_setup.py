#!/usr/bin/env python3
"""
Setup Verification Script for AbilityPath Prototype
Run this to check if everything is configured correctly
"""

import sys
import os
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_result(test_name, passed, message=""):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {test_name}")
    if message:
        print(f"     {message}")

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    passed = version.major == 3 and version.minor >= 8
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print_result(
        "Python Version",
        passed,
        f"Found Python {version_str} (need 3.8+)"
    )
    return passed

def check_file_structure():
    """Check if all required files exist"""
    required_files = [
        "requirements.txt",
        "programs_database.py",
        "screening_agent.py",
        "web_app.py",
        "templates/index.html",
        "README.md"
    ]
    
    all_exist = True
    for file in required_files:
        exists = Path(file).exists()
        if not exists:
            print_result(f"File: {file}", False, "Missing")
            all_exist = False
    
    if all_exist:
        print_result("File Structure", True, "All required files present")
    
    return all_exist

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'langchain': 'langchain',
        'openai': 'openai',
        'flask': 'flask',
        'flask_cors': 'flask-cors',
        'dotenv': 'python-dotenv'
    }
    
    all_installed = True
    for package, pip_name in required_packages.items():
        try:
            __import__(package.replace('_', '.'))
            print_result(f"Package: {pip_name}", True)
        except ImportError:
            print_result(f"Package: {pip_name}", False, f"Run: pip install {pip_name}")
            all_installed = False
    
    return all_installed

def check_env_file():
    """Check if .env file exists and has API key"""
    env_exists = Path(".env").exists()
    
    if not env_exists:
        print_result(
            ".env file",
            False,
            "Run: cp .env.example .env and add your OpenAI API key"
        )
        return False
    
    # Check if API key is configured
    try:
        with open(".env", "r") as f:
            content = f.read()
            has_key = "OPENAI_API_KEY=" in content
            is_placeholder = "your_openai_api_key_here" in content
            
            if has_key and not is_placeholder:
                print_result(".env file", True, "API key configured")
                return True
            elif has_key and is_placeholder:
                print_result(
                    ".env file",
                    False,
                    "Replace 'your_openai_api_key_here' with actual key"
                )
                return False
            else:
                print_result(".env file", False, "No OPENAI_API_KEY found")
                return False
    except Exception as e:
        print_result(".env file", False, f"Error reading file: {e}")
        return False

def check_openai_connection():
    """Test OpenAI API connection"""
    try:
        from dotenv import load_dotenv
        import openai
        
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key or api_key == "your_openai_api_key_here":
            print_result(
                "OpenAI Connection",
                False,
                "API key not configured in .env file"
            )
            return False
        
        # Try a simple API call
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        
        print_result(
            "OpenAI Connection",
            True,
            "Successfully connected to OpenAI API"
        )
        return True
        
    except ImportError as e:
        print_result(
            "OpenAI Connection",
            False,
            f"Missing package: {e}"
        )
        return False
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower():
            msg = "Invalid API key"
        elif "quota" in error_msg.lower():
            msg = "API quota exceeded (need to add credits)"
        elif "rate_limit" in error_msg.lower():
            msg = "Rate limit - try again in a moment"
        else:
            msg = f"Error: {error_msg[:100]}"
        
        print_result("OpenAI Connection", False, msg)
        return False

def test_program_database():
    """Test if programs database works"""
    try:
        from programs_database import get_all_programs, filter_programs_by_criteria
        
        programs = get_all_programs()
        if len(programs) >= 10:
            print_result(
                "Programs Database",
                True,
                f"Found {len(programs)} programs"
            )
        else:
            print_result(
                "Programs Database",
                False,
                f"Only {len(programs)} programs (expected 10+)"
            )
            return False
        
        # Test matching
        matches = filter_programs_by_criteria(22, {"recently_graduated": True})
        
        print_result(
            "Matching Algorithm",
            len(matches) > 0,
            f"Found {len(matches)} matches for test case"
        )
        
        return True
        
    except Exception as e:
        print_result("Programs Database", False, f"Error: {e}")
        return False

def main():
    print_header("AbilityPath Prototype - Setup Verification")
    print("\nChecking your setup...\n")
    
    results = []
    
    # Run all checks
    results.append(("Python Version", check_python_version()))
    results.append(("File Structure", check_file_structure()))
    results.append(("Dependencies", check_dependencies()))
    results.append((".env Configuration", check_env_file()))
    results.append(("Programs Database", test_program_database()))
    results.append(("OpenAI Connection", check_openai_connection()))
    
    # Summary
    print_header("Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total} checks")
    
    if passed == total:
        print("\n🎉 SUCCESS! Your prototype is ready to run!")
        print("\nNext steps:")
        print("  1. Run: python web_app.py")
        print("  2. Open: http://localhost:5002")
        print("  3. Try the test scenarios in test_scenarios.txt")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nQuick fixes:")
        print("  • Missing packages: pip install -r requirements.txt")
        print("  • Missing .env: cp .env.example .env")
        print("  • API key: Edit .env and add your OpenAI key")
    
    print("\n" + "="*60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
