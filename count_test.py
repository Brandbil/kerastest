import re
from collections import defaultdict

def parse_test_file(file_path):
    # Dictionary to store the number of tests per module (script)
    test_counts = defaultdict(int)
    
    # Regular expressions to match Module and TestCaseFunction lines
    module_pattern = re.compile(r"<Module (.+\.py)>")
    test_case_pattern = re.compile(r"<TestCaseFunction (.+)>")
    
    current_module = None
    in_test_collection = False
    
    # Open and read the file
    with open(file_path, 'r') as f:
        for line in f:
            # Skip session start and irrelevant lines before "collected ..."
            if "============================" in line:
                continue
            if "test session starts" in line or "platform" in line or "collecting" in line:
                continue
            if "collected" in line and "items" in line:
                # Start processing only after seeing the collected line
                in_test_collection = True
                continue

            # Process the test collection section
            if in_test_collection:
                # Check for Module lines
                module_match = module_pattern.match(line.strip())
                if module_match:
                    # Extract the module (script) name
                    current_module = module_match.group(1)
                
                # Check for TestCaseFunction lines
                test_case_match = test_case_pattern.match(line.strip())
                if test_case_match and current_module:
                    # Increment the count for the current module
                    test_counts[current_module] += 1

    # Print the results
    print("Test count per script:")
    for module, count in test_counts.items():
        print(f"{module}: {count} tests")

# Example usage:
parse_test_file('test_list.txt')
