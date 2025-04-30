import os
import subprocess

# Create output folder
os.makedirs("unit_test_report", exist_ok=True)
import glob

test_files = glob.glob("unit_tests/test_*.py")
# Run pytest with HTML report and coverage
subprocess.run(
    [
        "python",
        "-m",
        "pytest",
        *test_files,
        "--html=unit_test_report/index.html",
        "--self-contained-html",
        "--cov=matplotlib/matplotlib/",  # specify folder to check coverage
        "--cov-report=term",  # show summary in terminal
        "--cov-report=html:unit_test_report/cov",  # generate HTML report
    ]
)
