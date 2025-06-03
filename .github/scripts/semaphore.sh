#!/bin/bash

set -e

JSON_FILE="$1"

if [ ! -f "$JSON_FILE" ]; then
    echo "JSON file not found: $JSON_FILE"
    exit 1
fi

echo "== Code quality evaluation for each function =="
echo "Semaphore: 🟢 (Good), 🟡 (Warning), 🔴 (Bad)"
echo "file: $JSON_FILE"

# Extract functions with metrics from the JSON file
functions=$(jq -c '.. | objects | select(.kind == "function" and .metrics?)' "$JSON_FILE")
if [ -z "$functions" ]; then
    echo "No functions with metrics found in the JSON file."
    exit 0
fi

# Loop through each function and evaluate its metrics
while IFS= read -r function; do
    name=$(jq -r '.name' <<< "$function")
    loc=$(jq -r '.metrics.loc.sloc' <<< "$function")	
    cyclomatic=$(jq -r '.metrics.cyclomatic.sum' <<< "$function")
    mi=$(jq -r '.metrics.mi.mi_original' <<< "$function")
    effort=$(jq -r '.metrics.halstead.effort' <<< "$function")

    color_loc="🟢"
    if (( $(echo "$loc > 100" | bc -l ) )); then
        color_loc="🔴"
    elif (( $(echo "$loc > 50" | bc -l) )); then
        color_loc="🟡"
    fi

    color_cyclo="🟢"
    if (( $(echo "$cyclomatic > 20" | bc -l) )); then
        color_cyclo="🔴"
    elif (( $(echo "$cyclomatic > 10" | bc -l) )); then
        color_cyclo="🟡"
    fi

    color_mi="🟢"
    if (( $(echo "$mi < 60" | bc -l) )); then
        color_mi="🔴"
    elif (( $(echo "$mi < 80" | bc -l) )); then
        color_mi="🟡"
    fi
    
    color_effort="🟢"
    if (( $(echo "$effort > 2000" | bc -l) )); then
        color_effort="🔴"
    elif (( $(echo "$effort > 1000" | bc -l) )); then
        color_effort="🟡"
    fi

    semaforo="🟢"
    if [[ "$color_loc" == "🔴" || "$color_cyclo" == "🔴" || "$color_mi" == "🔴" || "$color_effort" == "🔴" ]]; then
        semaforo="🔴"
    elif [[ "$color_loc" == "🟡" || "$color_cyclo" == "🟡" || "$color_mi" == "🟡" || "$color_effort" == "🟡" ]]; then
        semaforo="🟡"
    fi

    # Print the function metrics with colors
    echo "----------------------------------------"
    echo "Function: $name"
    echo "  LOC: $loc $color_loc"
    echo "  Cyclomatic Complexity: $cyclomatic $color_cyclo"
    echo "  Maintainability Index: $mi $color_mi"
    echo "  Halstead Effort: $effort $color_effort"
    echo "  Overall Quality: $semaforo"
    echo "----------------------------------------"

done <<< "$functions"
echo "== Code quality evaluation completed =="
# End of script