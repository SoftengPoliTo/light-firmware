#!/usr/bin/env python3

import json
import sys
import os
import glob
from pathlib import Path
from io import StringIO

def evaluate_single_file(json_file, output_stream=None):
    
    def print_to_stream(message):
        if output_stream:
            output_stream.write(message + '\n')
        else:
            print(message)
    
    # Check if file exists
    if not os.path.isfile(json_file):
        print_to_stream(f"JSON file not found: {json_file}")
        return False
    
    print_to_stream("== Code quality evaluation for each function ==")
    print_to_stream("Semaphore: 🟢 (Good), 🟡 (Warning), 🔴 (Bad)")
    print_to_stream(f"file: {json_file}")
    
    try:
        # Load JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print_to_stream(f"Error reading JSON file: {e}")
        return False
    
    # Extract functions with metrics
    functions = []
    
    def find_functions(obj):
        """Recursively find all functions with metrics in the JSON structure."""
        if isinstance(obj, dict):
            if obj.get('kind') == 'function' and 'metrics' in obj:
                functions.append(obj)
            for value in obj.values():
                find_functions(value)
        elif isinstance(obj, list):
            for item in obj:
                find_functions(item)
    
    find_functions(data)
    
    if not functions:
        print_to_stream("No functions with metrics found in the JSON file.")
        return True
    
    # Evaluate each function
    for function in functions:
        name = function.get('name', 'Unknown')
        metrics = function.get('metrics', {})
        
        # Extract metrics with safe access
        loc = metrics.get('loc', {}).get('sloc', 0)
        cyclomatic = metrics.get('cyclomatic', {}).get('sum', 0)
        mi = metrics.get('mi', {}).get('mi_original', 100)
        effort = metrics.get('halstead', {}).get('effort', 0)
        
        # Evaluate LOC
        if loc > 100:
            color_loc = "🔴"
        elif loc > 50:
            color_loc = "🟡"
        else:
            color_loc = "🟢"
        
        # Evaluate Cyclomatic Complexity  
        if cyclomatic > 20:
            color_cyclo = "🔴"
        elif cyclomatic > 10:
            color_cyclo = "🟡"
        else:
            color_cyclo = "🟢"
        
        # Evaluate Maintainability Index
        if mi < 60:
            color_mi = "🔴"
        elif mi < 80:
            color_mi = "🟡"
        else:
            color_mi = "🟢"
        
        # Evaluate Halstead Effort
        if effort > 2000:
            color_effort = "🔴"
        elif effort > 1000:
            color_effort = "🟡"
        else:
            color_effort = "🟢"
        
        # Determine overall quality
        colors = [color_loc, color_cyclo, color_mi, color_effort]
        if "🔴" in colors:
            semaforo = "🔴"
        elif "🟡" in colors:
            semaforo = "🟡"
        else:
            semaforo = "🟢"
        
        # Print function metrics
        print_to_stream("----------------------------------------")
        print_to_stream(f"Function: {name}")
        print_to_stream(f"  LOC: {loc} {color_loc}")
        print_to_stream(f"  Cyclomatic Complexity: {cyclomatic} {color_cyclo}")
        print_to_stream(f"  Maintainability Index: {mi} {color_mi}")
        print_to_stream(f"  Halstead Effort: {effort} {color_effort}")
        print_to_stream(f"  Overall Quality: {semaforo}")
        print_to_stream("----------------------------------------")
    
    print_to_stream("== Code quality evaluation completed ==")
    return True

def log_and_write(message, report_file):
    print(message)
    with open(report_file, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

def run_batch_evaluation():
    
    # Setup paths
    home_dir = Path.home()
    output_dir = home_dir / "code-quality-report"
    json_dir = home_dir / "rca-json"
    report_file = output_dir / "report.txt"
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Clear/create report file
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("")
    
    # Look for JSON files
    log_and_write(f"== Looking for JSON files in {json_dir} ==", report_file)
    
    # Find all JSON files
    json_pattern = str(json_dir / "*.json")
    json_files = glob.glob(json_pattern, recursive=True)
    
    # Also search recursively in subdirectories
    json_pattern_recursive = str(json_dir / "**" / "*.json")
    json_files.extend(glob.glob(json_pattern_recursive, recursive=True))
    
    # Remove duplicates and sort
    json_files = sorted(set(json_files))
    
    # Log found files
    for json_file in json_files:
        log_and_write(json_file, report_file)
    
    if not json_files:
        log_and_write("No JSON files found.", report_file)
        return 0
    
    exit_code = 0
    
    # Process each JSON file
    for json_file in json_files:
        log_and_write("", report_file)  # Empty line
        
        # Capture output in a StringIO object
        output_capture = StringIO()
        
        try:
            success = evaluate_single_file(json_file, output_capture)
            
            # Get the captured output
            output_content = output_capture.getvalue()
            
            # Write to report file
            with open(report_file, 'a', encoding='utf-8') as f:
                f.write(output_content)
            
            # Also print to console
            print(output_content, end='')
            
            if not success:
                exit_code = 1
                
        except Exception as e:
            error_msg = f"Code quality evaluation failed for {json_file}: {str(e)}"
            log_and_write(error_msg, report_file)
            exit_code = 1
        
        finally:
            output_capture.close()
    
    return exit_code

def main():
    
    if len(sys.argv) == 1:
        # No arguments - run batch evaluation
        exit_code = run_batch_evaluation()
        sys.exit(exit_code)
    elif len(sys.argv) == 2:
        # Single file evaluation
        json_file = sys.argv[1]
        success = evaluate_single_file(json_file)
        sys.exit(0 if success else 1)
    else:
        print("Usage:")
        print("  python script.py                    # Run batch evaluation on all JSON files")
        print("  python script.py <json_file>        # Evaluate single JSON file")
        sys.exit(1)

if __name__ == "__main__":
    main()