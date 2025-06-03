#!/bin/bash

    OUTPUT_DIR="$HOME/code-quality-report"
    mkdir -p "$OUTPUT_DIR"
    REPORT_FILE="$OUTPUT_DIR/report.txt"

    echo "== Looking for JSON files in $HOME/rca-json ==" | tee "$REPORT_FILE"
        find $HOME/rca-json -name "*.json" | tee -a "$REPORT_FILE"

        EXIT_CODE=0

        for json_file in $(find $HOME/rca-json -name "*.json"); do
          echo "" | tee -a "$REPORT_FILE"
          echo "Processing: $json_file" | tee -a "$REPORT_FILE"
          if ! .github/scripts/semaphore.sh "$json_file" | tee -a "$REPORT_FILE"; then
            echo "Code quality evaluation failed for $json_file" | tee -a "$REPORT_FILE"
            EXIT_CODE=1
          fi
        done

        exit $EXIT_CODE
