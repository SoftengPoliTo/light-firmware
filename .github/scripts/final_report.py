#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from datetime import datetime

def check_code_quality():
    """Check code quality results focusing on 'Overall Quality' metric."""
    home_dir = Path.home()
    report_file = home_dir / "final-artifacts" / "step1" / "report.txt"

    if not report_file.exists():
        return "🔴", "Code quality report not found"
    
    try:
        with open(report_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        green = yellow = red = 0
        for line in lines:
            if "Overall Quality" in line:
                if "🟢" in line:
                    green += 1
                elif "🟡" in line:
                    yellow += 1
                elif "🔴" in line:
                    red += 1

        total = green + yellow + red
        if total == 0:
            return "🔴", "No quality metrics found in report"
            ""
        if red/total > total/2:
            return "🔴", f"Critical issues in code quality ({red}/{total} functions)"
        elif yellow/total > total/3:
            return "🟡", f"Warnings in code quality ({yellow}/{total} functions)"
        else:
            return "🟢", f"All functions passed ({green}/{total} functions)"

    except Exception as e:
         return "🔴", f"Error parsing code quality report: {str(e)}"


def check_anomaly_detection():
    """Check anomaly detection results and return semaphore status"""
    home_dir = Path.home()
    anomaly_file = home_dir / "final-artifacts" / "step2" / "anomaly-detection-report.txt"
    
    if not anomaly_file.exists():
        return "🔴", "Anomaly detection report not found"

    try:
        with open(anomaly_file, 'r', encoding='utf-8') as file:
            content = file.read().lower()

        # Customize these checks based on your actual anomaly detection logic
        if "critical" in content or "error" in content:
            return "🔴", "Critical anomalies detected"
        elif "warning" in content or "suspicious" in content:
            return "🟡", "Potential anomalies detected"
        elif "no anomalies" in content:
            return "🟢", "No anomalies detected"
        else:
            return "🟡", "Anomaly detection completed with unknown status"

    except Exception as e:
        return "🔴", f"Error reading anomaly report: {str(e)}"


def check_manifest_producer():
    """Check manifest-producer results and return semaphore status"""
    home_dir = Path.home()
    results_dir = home_dir / "final-artifacts" / "step3"
    json_dir = results_dir / "json"

    if not results_dir.exists():
        return "🔴", "Manifest analysis directory not found"

    # Check presence of checker files
    checker_files = list(results_dir.glob("*_checker.json"))
    if not checker_files:
        return "🔴", "No checker file found in manifest analysis"
    
    try:
        # Use first checker file found
        with open(checker_files[0], 'r', encoding='utf-8') as f:
            checker_data = json.load(f)
        
        total_checks = 0
        failed_checks = 0

        for category in checker_data.get("categories", []):
            for check in category.get("checks", []):
                total_checks += 1
                if not check.get("status", True):
                    failed_checks += 1
    
        if total_checks == 0:
            return "🔴", "No checks found in manifest checker file"

        # Check for presence of at least 3 json files
        json_files = list(json_dir.glob("*.json"))
        json_file_count = len(json_files)

        if failed_checks > 0:
            status = "🔴" if failed_checks / total_checks >= 0.3 else "🟡"
        else:
            status = "🟢"

        msg = f"{failed_checks}/{total_checks} checks failed"
        if json_file_count < 3:
            msg += f"; warning: only {json_file_count} JSON files found in directory"

        return status, msg

    except json.JSONDecodeError:
        return "🔴", "Invalid JSON in manifest checker"
    except Exception as e:
        return "🔴", f"Error reading checker file: {str(e)}"
    
def generate_final_report():
    """Generate final markdown report with semaphores for all sections"""

    print("🔍 Analyzing results from all steps...")

    # Check each section
    code_quality_status, code_quality_msg = check_code_quality()
    anomaly_status, anomaly_msg = check_anomaly_detection()
    manifest_status, manifest_msg = check_manifest_producer()

    print(f"📊 Code Quality: {code_quality_status} - {code_quality_msg}")
    print(f"🔍 Anomaly Detection: {anomaly_status} - {anomaly_msg}")
    print(f"📋 Manifest Producer: {manifest_status} - {manifest_msg}")

    # Generate final report
    home_dir = Path.home()
    final_report_path = home_dir / "final-artifacts" / "FINAL_REPORT.md"

    # Ensure directory exists
    final_report_path.parent.mkdir(parents=True, exist_ok=True)

    # Calculate overall project status
    all_statuses = [code_quality_status, anomaly_status, manifest_status]
    if "🔴" in all_statuses:
        overall_status = "🔴"
        overall_message = "Critical issues found - Action required"
    elif "🟡" in all_statuses:
        overall_status = "🟡"
        overall_message = "Warnings found - Review recommended"
    else:
        overall_status = "🟢"
        overall_message = "All checks passed successfully"

    # Count files in each step for summary
    step1_files = count_files_in_step(home_dir / "final-artifacts" / "step1")
    step2_files = count_files_in_step(home_dir / "final-artifacts" / "step2")
    step3_files = count_files_in_step(home_dir / "final-artifacts" / "step3")

    # Generate markdown report
    report_content = f"""# Firmware Compliance Analysis Report
**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Overall Status: {overall_status}

**{overall_message}**

---

## Analysis Results Summary

| Section | Status | Message |
|---------|--------|---------|
| Code Quality | {code_quality_status} | {code_quality_msg} |
| Anomaly Detection | {anomaly_status} | {anomaly_msg} |
| Manifest Producer | {manifest_status} | {manifest_msg} |

---

## Detailed Results

### 1. Code Quality Analysis {code_quality_status}
- **Status:** {code_quality_status}
- **Message:** {code_quality_msg}
- **Tool:** rust-code-analysis
- **Metrics analyzed:** LOC, Cyclomatic Complexity, Maintainability Index, Halstead Effort
- **Details:** Check `step1/` directory for detailed reports and JSON files

### 2. Anomaly Detection {anomaly_status}
- **Status:** {anomaly_status}
- **Message:** {anomaly_msg}
- **Details:** Check `step2/` directory for anomaly detection reports

### 3. Manifest-Producer Analysis {manifest_status}
- **Status:** {manifest_status}
- **Message:** {manifest_msg}
- **Tool:** behaviour-assessment
- **Details:** Check `step3/` directory for manifest analysis results

---

## Status Legend

- 🟢 **Good**: All checks passed successfully
- 🟡 **Warning**: Some issues found, review recommended
- 🔴 **Critical**: Issues found, action required

---

## Artifact Structure

```
final-artifacts/
├── step1/                              # Code quality analysis results
│   ├── ~/*.json                        # rust-code-analysis output
│   └── report.txt                      # Quality evaluation report
├── step2/                              # Anomaly detection results
│   └── anomaly-detection-report.txt
├── step3/                              # Manifest-producer analysis results
│   ├── light-firmware_checker.json     # Manifest checker results
│   └── [other manifest files]          # Additional manifest files
└── FINAL_REPORT.md                     # This report
```

---

## Recommendations

{generate_recommendations(overall_status, code_quality_status, anomaly_status, manifest_status)}

---

## Compliance Status

This firmware analysis {'**PASSES**' if overall_status == '🟢' else '**REQUIRES ATTENTION**'} compliance checks.

{f"✅ The firmware meets all compliance standards and is ready for deployment." if overall_status == "🟢" else ""}
{f"⚠️ The firmware has some warnings that should be reviewed before deployment." if overall_status == "🟡" else ""}
{f"🚨 The firmware has critical issues that must be resolved before deployment." if overall_status == "🔴" else ""}

---

*Report generated by Firmware Compliance Analysis Pipeline*
"""

    with open(final_report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"📄 Final report generated: {final_report_path}")
    print(f"🚦 Overall project status: {overall_status} - {overall_message}")

    # Return appropriate exit code
    return 0 if overall_status in ["🟢", "🟡"] else 1


def generate_recommendations(overall_status, code_quality_status, anomaly_status, manifest_status):
    """Generate recommendations based on analysis results"""
    recommendations = []

    if code_quality_status == "🔴":
        recommendations.append("- **Code Quality**: Refactor functions with high complexity or low maintainability")
    elif code_quality_status == "🟡":
        recommendations.append("- **Code Quality**: Consider reviewing functions with warnings")

    if anomaly_status == "🔴":
        recommendations.append("- **Anomaly Detection**: Investigate critical anomalies before deployment")
    elif anomaly_status == "🟡":
        recommendations.append("- **Anomaly Detection**: Review potential anomalies for false positives")

    if manifest_status == "🔴":
        recommendations.append("- **Manifest Analysis**: Fix manifest-producer errors before proceeding")
    elif manifest_status == "🟡":
        recommendations.append("- **Manifest Analysis**: Review manifest-producer warnings and validate results")

    if not recommendations:
        recommendations.append("- **All systems**: Continue with standard deployment procedures")

    return "\n".join(recommendations)


def count_files_in_step(step_dir):
    """Count files in a step directory for summary"""
    if not step_dir.exists():
        return 0

    return len([f for f in step_dir.iterdir() if f.is_file()])

def main():
    """Main Function to run the final compliance report."""
    if len(sys.argv) > 1:
        print("Usage: python final_report.py")
        print("This script analyses all step results and generates a final compliance report.")
        sys.exit(1)

    try:
        exit_code = generate_final_report()
        sys.exit(exit_code)
    except Exception as e:
        print(f"❌ Error generating final report: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()