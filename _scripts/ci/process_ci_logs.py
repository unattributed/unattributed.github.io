import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

# Path to the extracted logs
LOG_DIR = "_tmpbkup/logs"

# Error patterns for common issues
ERROR_PATTERNS = {
    "ModuleNotFoundError": r"ModuleNotFoundError: No module named '([^']+)'",
    "ImportError": r"ImportError: cannot import name '([^']+)'",
    "FileNotFoundError": r"FileNotFoundError: (.*)",
    "SyntaxError": r"SyntaxError: (.*)"
}

# Function to process each log file and categorize errors
def process_log_file(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        log_content = f.read()

    errors = {}
    
    for error_type, pattern in ERROR_PATTERNS.items():
        matches = re.findall(pattern, log_content)
        if matches:
            errors[error_type] = matches

    return errors

# Function to generate remediation suggestions
def suggest_remediation(errors, log_file):
    remediation_suggestions = []
    
    if "ModuleNotFoundError" in errors:
        for module in errors["ModuleNotFoundError"]:
            remediation_suggestions.append(f"ModuleNotFoundError: Install the missing module using `pip install {module}`")
    
    if "ImportError" in errors:
        for module in errors["ImportError"]:
            remediation_suggestions.append(f"ImportError: Verify the module `{module}` is properly installed or check for circular imports.")
    
    if "FileNotFoundError" in errors:
        for file in errors["FileNotFoundError"]:
            remediation_suggestions.append(f"FileNotFoundError: Check if the file or path `{file}` exists and is accessible.")
    
    if "SyntaxError" in errors:
        for message in errors["SyntaxError"]:
            remediation_suggestions.append(f"SyntaxError: Check the following in the log: {message}")
    
    # Additional checks can be added here

    return remediation_suggestions

# Function to generate a timestamped file name
def get_output_filename(first_run_id, last_run_id):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    return f"{timestamp}-ci_run_{first_run_id}-ci_run_{last_run_id}.txt"

# Main function to process all logs and suggest fixes
def process_logs():
    all_suggestions = {}
    first_run_id, last_run_id = None, None
    
    # Iterate over each log file in the logs directory
    for log_file in Path(LOG_DIR).glob("*.log"):
        print(f"Processing log: {log_file.name}")
        
        # Set first_run_id during the first loop
        if first_run_id is None:
            first_run_id = log_file.stem.split('__')[0].replace("ci_run_", "")
        
        # Process log file to find errors
        errors = process_log_file(log_file)
        
        # If errors were found, suggest fixes
        if errors:
            suggestions = suggest_remediation(errors, log_file)
            all_suggestions[log_file.name] = suggestions
        else:
            print(f"No errors found in {log_file.name}")
        
        # Update the last_run_id
        last_run_id = log_file.stem.split('__')[0].replace("ci_run_", "")
    
    # Create the output file name
    output_filename = get_output_filename(first_run_id, last_run_id)
    output_file_path = Path("_tmpbkup/logs") / output_filename
    
    # Write the suggestions to the output file
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        for log, errors in all_suggestions.items():
            output_file.write(f"\nLog File: {log}\n")
            if errors:
                for error in errors:
                    output_file.write(f"  - {error}\n")
            else:
                output_file.write("  No issues detected.\n")
    
    print(f"Remediation suggestions saved to: {output_file_path}")

if __name__ == "__main__":
    process_logs()
