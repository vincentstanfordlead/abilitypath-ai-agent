"""
CSV Program Loader for AbilityPath Screening Agent
==================================================

This module reads program information from a CSV file and converts it
into the structured format needed by the screening agent.

Usage:
    python csv_program_loader.py path/to/programs.csv

Author: AbilityPath Hackathon Team
Created: 2025-01-08
"""

import csv
import json
import re
from typing import Dict, List, Any


class ProgramCSVLoader:
    """Loads program data from CSV and converts to agent-friendly format."""
    
    def __init__(self, csv_path: str):
        """
        Initialize the loader with a CSV file path.
        
        Args:
            csv_path: Path to the CSV file containing program information
        """
        self.csv_path = csv_path
        self.programs = []
        
    def load_programs(self) -> List[Dict[str, Any]]:
        """
        Read the CSV file and parse program information.
        
        Returns:
            List of program dictionaries ready for the screening agent
        """
        with open(self.csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                program = self._parse_program_row(row)
                self.programs.append(program)
        
        return self.programs
    
    def _parse_program_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """
        Convert a CSV row into a structured program dictionary.
        
        Args:
            row: Dictionary from CSV DictReader
            
        Returns:
            Structured program dictionary
        """
        program = {
            "name": row.get("Program", "").strip(),
            "description": row.get("Description", "").strip(),
            "location": self._parse_location(row),
            "age_range": self._parse_age_range(row.get("Population", "")),
            "diagnosis_accepted": self._parse_diagnosis(row.get("Population", "")),
            "support_requirements": self._parse_support_requirements(row.get("Other Entrance Criteria", "")),
            "counties_served": self._parse_counties(row.get("What County/City does this program serve? ", "")),
            "physical_location": row.get("What is the location of this program/service?", "").strip(),
            "schedule": row.get("When?", "").strip(),
            "enrollment_process": row.get("How to get started?", "").strip(),
            "program_type": self._infer_program_type(row.get("Program", ""), row.get("Description", ""))
        }
        
        return program
    
    def _parse_age_range(self, population_text: str) -> Dict[str, Any]:
        """
        Extract age range from population text.
        
        Args:
            population_text: Text describing the population
            
        Returns:
            Dictionary with min_age and max_age
        """
        age_range = {"min_age": None, "max_age": None}
        
        # Look for age patterns
        if "18+" in population_text or "Ages 18+" in population_text:
            age_range["min_age"] = 18
            age_range["max_age"] = None  # No upper limit
        elif "12-17" in population_text or "Ages 12-17" in population_text:
            age_range["min_age"] = 12
            age_range["max_age"] = 17
        
        # Check for other age patterns
        age_match = re.search(r'(\d+)\s*-\s*(\d+)', population_text)
        if age_match:
            age_range["min_age"] = int(age_match.group(1))
            age_range["max_age"] = int(age_match.group(2))
        
        return age_range
    
    def _parse_diagnosis(self, population_text: str) -> List[str]:
        """
        Extract accepted diagnosis types from population text.
        
        Args:
            population_text: Text describing the population
            
        Returns:
            List of accepted diagnosis types
        """
        diagnoses = []
        
        text_lower = population_text.lower()
        
        if "developmental disabilit" in text_lower:
            diagnoses.append("Developmental Disability")
        
        if "intellectual disabilit" in text_lower:
            diagnoses.append("Intellectual Disability")
        
        if "traumatic brain injury" in text_lower or "tbi" in text_lower:
            diagnoses.append("Traumatic Brain Injury")
        
        if "stroke" in text_lower:
            diagnoses.append("Stroke")
        
        if "physical" in text_lower and "disabilit" in text_lower:
            diagnoses.append("Physical Disability")
        
        if "mental health" in text_lower:
            diagnoses.append("Mental Health Condition")
        
        # If no specific diagnosis found, assume developmental disability (most common)
        if not diagnoses and "disability" in text_lower:
            diagnoses.append("Developmental Disability")
        
        return diagnoses
    
    def _parse_support_requirements(self, criteria_text: str) -> Dict[str, Any]:
        """
        Parse support requirements from entrance criteria text.
        
        Args:
            criteria_text: Text describing entrance criteria
            
        Returns:
            Dictionary of support requirements
        """
        requirements = {
            "toilet_trained": True,  # Default assumption
            "eating_independence": True,
            "mobility_independence": True,
            "medication_independence": True,
            "behavioral_requirements": []
        }
        
        text_lower = criteria_text.lower()
        
        # Check for independence requirements
        if "restroom" in text_lower or "toilet" in text_lower:
            requirements["toilet_trained"] = "doesn't need support" in text_lower
        
        if "eating" in text_lower:
            requirements["eating_independence"] = "doesn't need support" in text_lower
        
        if "mobility" in text_lower:
            requirements["mobility_independence"] = "doesn't need support" in text_lower
        
        if "medication" in text_lower:
            requirements["medication_independence"] = "doesn't need support" in text_lower
        
        # Check for behavioral requirements
        if "not" in text_lower and "disruptive" in text_lower:
            requirements["behavioral_requirements"].append("Non-disruptive")
        
        if "not" in text_lower and "dangerous" in text_lower:
            requirements["behavioral_requirements"].append("Safe to self and others")
        
        if "not" in text_lower and "destructive" in text_lower:
            requirements["behavioral_requirements"].append("Non-destructive of property")
        
        if "not" in text_lower and "eloping" in text_lower:
            requirements["behavioral_requirements"].append("No elopement risk")
        
        return requirements
    
    def _parse_counties(self, county_text: str) -> List[str]:
        """
        Extract counties served from location text.
        
        Args:
            county_text: Text describing counties/cities served
            
        Returns:
            List of counties
        """
        counties = []
        
        text = county_text.strip()
        
        if "San Mateo" in text:
            counties.append("San Mateo County")
        
        if "Santa Clara" in text:
            counties.append("Santa Clara County")
        
        if "San Francisco" in text or "SF" in text:
            counties.append("San Francisco")
        
        # Handle geographic descriptions
        if "Palo Alto to Santa Cruz" in text:
            counties.extend(["Santa Clara County", "Santa Cruz County"])
        
        if "San Francisco to Palo Alto" in text:
            if "San Mateo County" not in counties:
                counties.append("San Mateo County")
        
        return list(set(counties))  # Remove duplicates
    
    def _parse_location(self, row: Dict[str, str]) -> str:
        """
        Determine primary location category for matching.
        
        Args:
            row: CSV row dictionary
            
        Returns:
            Location category string
        """
        county_text = row.get("What County/City does this program serve? ", "").strip()
        
        if "San Mateo" in county_text and "Santa Clara" not in county_text:
            return "San Mateo County"
        elif "Santa Clara" in county_text and "San Mateo" not in county_text:
            return "Santa Clara County"
        elif "San Francisco to Palo Alto" in county_text:
            return "SF to Palo Alto"
        elif "Palo Alto to Santa Cruz" in county_text:
            return "Palo Alto to Santa Cruz"
        elif "San Mateo" in county_text and "Santa Clara" in county_text:
            return "Both San Mateo and Santa Clara"
        else:
            return county_text
    
    def _infer_program_type(self, program_name: str, description: str) -> List[str]:
        """
        Infer program type/interest category from name and description.
        
        Args:
            program_name: Name of the program
            description: Program description
            
        Returns:
            List of program types/interests
        """
        types = []
        
        combined_text = (program_name + " " + description).lower()
        
        # Employment-related
        if any(word in combined_text for word in ["employment", "job", "work", "career", "vocational", "internship"]):
            types.append("Employment Support")
        
        # Living skills
        if any(word in combined_text for word in ["living skills", "independent living", "ils", "daily living", "life skills"]):
            types.append("Living Skills")
        
        # Social/Recreation
        if any(word in combined_text for word in ["social", "recreation", "friendship", "community engagement"]):
            types.append("Social Activities")
        
        # Day programs
        if any(word in combined_text for word in ["day program", "day service", "tailored day"]):
            types.append("Day Programs")
        
        # Creative/Arts
        if any(word in combined_text for word in ["creative", "arts", "artistic"]):
            types.append("Creative Arts")
        
        # Therapeutic
        if any(word in combined_text for word in ["therapy", "therapeutic", "rehabilitation", "reach"]):
            types.append("Therapeutic Services")
        
        return types if types else ["General Support"]
    
    def save_as_python_module(self, output_path: str = "programs_database_real.py"):
        """
        Save loaded programs as a Python module that can replace programs_database.py
        
        Args:
            output_path: Path to save the Python module
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('"""\n')
            f.write('AbilityPath Real Programs Database\n')
            f.write('=====================================\n')
            f.write('Auto-generated from CSV file\n')
            f.write('Created: 2025-01-08\n')
            f.write('"""\n\n')
            
            f.write('PROGRAMS = [\n')
            
            for program in self.programs:
                f.write('    {\n')
                for key, value in program.items():
                    if isinstance(value, str):
                        f.write(f'        "{key}": {repr(value)},\n')
                    else:
                        f.write(f'        "{key}": {value},\n')
                f.write('    },\n')
            
            f.write(']\n\n')
            
            # Add helper functions
            f.write('''
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
''')
        
        print(f"✅ Saved {len(self.programs)} programs to {output_path}")
    
    def save_as_json(self, output_path: str = "programs_data.json"):
        """
        Save loaded programs as JSON file for easy inspection.
        
        Args:
            output_path: Path to save JSON file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.programs, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(self.programs)} programs to {output_path}")
    
    def print_summary(self):
        """Print a summary of loaded programs."""
        print(f"\n{'='*70}")
        print(f"LOADED {len(self.programs)} PROGRAMS FROM CSV")
        print(f"{'='*70}\n")
        
        for i, program in enumerate(self.programs, 1):
            print(f"{i}. {program['name']}")
            print(f"   Location: {program['location']}")
            print(f"   Age Range: {program['age_range']}")
            print(f"   Diagnosis: {', '.join(program['diagnosis_accepted'])}")
            print(f"   Type: {', '.join(program['program_type'])}")
            print()


def main():
    """Main function to load and convert CSV program data."""
    import sys
    
    # Check if CSV path is provided
    if len(sys.argv) < 2:
        print("Usage: python csv_program_loader.py path/to/programs.csv")
        print("\nExample:")
        print("  python csv_program_loader.py 'WIP_Nov 7_ Tech For Good AbilityPath Info. - Program Info.csv'")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    
    print(f"📂 Loading programs from: {csv_path}\n")
    
    # Load programs
    loader = ProgramCSVLoader(csv_path)
    programs = loader.load_programs()
    
    # Print summary
    loader.print_summary()
    
    # Save outputs
    loader.save_as_python_module("programs_database_real.py")
    loader.save_as_json("programs_data.json")
    
    print(f"\n{'='*70}")
    print("✅ CONVERSION COMPLETE!")
    print(f"{'='*70}\n")
    print("Next steps:")
    print("1. Review programs_data.json to verify data accuracy")
    print("2. Replace programs_database.py with programs_database_real.py")
    print("3. Restart your screening agent")
    print()


if __name__ == "__main__":
    main()
