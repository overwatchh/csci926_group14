import os
import subprocess

# Create output folder
os.makedirs("unit_test_report", exist_ok=True)

# Run pytest with HTML report and coverage
subprocess.run(
    [
        "python",
        "-m",
        "pytest",
        "unit_tests",
        "--html=unit_test_report/index.html",
        "--self-contained-html",
        "--cov=matplotlib",  # specify folder to check coverage
        "--cov-report=term",  # show summary in terminal
        "--cov-report=html:unit_test_report/cov",  # generate HTML report
    ]
)
