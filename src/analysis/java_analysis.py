import os
import shutil
import time
import xml.etree.ElementTree as ET
import glob

from src.analysis.java_assertion_ratios import assertions_density_java, assertions_mccabe_ratio_java
from src.analysis.python_validation import CompileStatus

JAVA_SRC_DIR = 'data/javaSetup/src/main/java/org/example/package'
JAVA_TEST_DIR = 'data/javaSetup/src/test/java/org/example/package'
JAVA_PROJECT_ROOT = 'data/javaSetup'
CHECKSTYLE_JAR_PATH = "./checkstyle-10.18.1-all.jar"
CHECKSTYLE_CONFIG = "./checkstyle-config.xml"
TEST_REPORTS = "data/javaSetup/target/surefire-reports/*.xml"

import subprocess


def run_checkstyle(java_file_path):
    """ Run Checkstyle for a Java file and return a list of errors """
    try:
        result = subprocess.run(
            ['java', '-jar', CHECKSTYLE_JAR_PATH, '-c', CHECKSTYLE_CONFIG, java_file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        if result.stdout:
            print("Checkstyle stdout output:")
            print(result.stdout)

        if result.stderr:
            print("Checkstyle stderr output:")
            print(result.stderr)

        # Combine both stdout and stderr for processing, as errors might be in either
        output = result.stdout + result.stderr

        # Extract errors from the output
        errors = parse_checkstyle_errors(output)

        if errors:
            print("Found Checkstyle errors:")
            for error in errors:
                print(error)
        else:
            print("No Checkstyle issues found for this file.")

        return errors

    except Exception as e:
        print(f"Error running Checkstyle: {e}")
        return []


def parse_checkstyle_errors(output):
    """ Parse the Checkstyle output to extract errors """
    errors = []

    # Split the output into lines and look for lines that indicate errors
    for line in output.splitlines():
        if "error" in line.lower():
            errors.append(line.strip())

    return errors


def run_maven_test_compile(project_dir, timeout):
    """
    Runs 'mvn test-compile' in the given project directory with the specified timeout.

    Returns a tuple: (syntax_maven_output, syntax, timeout_occurred, error)
    """
    syntax_maven_output = None
    syntax = None
    timeout_occurred = False
    error = False

    try:
        result = subprocess.run(
            ['mvn', 'test-compile'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        syntax_maven_output = result.stdout
        print(result.stdout)
        print(result.stderr)
        if result.returncode == 0:
            print("TEST COMPILE PASSED")
            syntax = CompileStatus.OK
        else:
            print("TEST COMPILE FAILED")
            syntax = CompileStatus.SYNTAX_ERROR
    except subprocess.TimeoutExpired:
        timeout_occurred = True
        syntax_maven_output = "Test compilation timed out."
        syntax = CompileStatus.EXCEPTION_OCCURRED
    except Exception as e:
        print("Error occurred during compilation: ", e)
        error = True
        syntax = CompileStatus.EXCEPTION_OCCURRED
        syntax_maven_output = None

    return syntax_maven_output, syntax, timeout_occurred, error


def run_maven_clean_test(project_dir, timeout):
    """
    Runs 'mvn clean test' in the given project directory with the specified timeout.

    Returns a tuple: (test_maven_output, timeout_occurred, error, execution_time)
    """
    test_maven_output = None
    timeout_occurred = False
    error = False
    start_time = time.time()
    try:
        result = subprocess.run(
            ['mvn', 'clean', 'verify'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        test_maven_output = result.stdout
    except subprocess.TimeoutExpired:
        timeout_occurred = True
        test_maven_output = "Test execution timed out."
    except Exception as e:
        print("Error occurred during test execution: ", e)
        error = True
    end_time = time.time()
    execution_time = end_time - start_time
    return test_maven_output, timeout_occurred, error, execution_time


def compute_coverage_percentage(project_dir, src_file_path, timeout_occurred):
    """
    Parses the JaCoCo coverage report and computes both line and branch coverage percentages.

    Returns:
        A dictionary with line and branch coverage percentages, or None if the report is not found or a timeout occurred.
    """
    if timeout_occurred:
        return {"line": None, "branch": None}

    coverage_report_path = os.path.join(project_dir, 'target', 'site', 'jacoco', 'jacoco.xml')
    if os.path.exists(coverage_report_path):
        try:
            tree = ET.parse(coverage_report_path)
            root = tree.getroot()

            # Initialize coverage metrics
            coverage = {"line": None, "branch": None}

            file_name = os.path.basename(src_file_path)
            # Find the <sourcefile> element with the specified file name
            source_file = root.find(f".//sourcefile[@name='{file_name}']")
            if source_file is None:
                print(f"File '{file_name}' not found in the coverage report.")
                return coverage

            # Extract LINE and BRANCH counters for the file
            for counter_type in ["LINE", "BRANCH"]:
                counter = source_file.find(f"./counter[@type='{counter_type}']")
                if counter is not None:
                    covered = int(counter.get("covered", 0))
                    missed = int(counter.get("missed", 0))
                    print("COVERED: " + str(covered) + " MISSED: " + str(missed))
                    if covered + missed > 0:
                        coverage[counter_type.lower()] = (covered / (covered + missed)) * 100
                else:
                    if coverage["line"] is not None and coverage["branch"] is None:
                        # case when branch coverage isn't in report because code has no branches that need covering
                        coverage["branch"] = 100
            return coverage

        except Exception as e:
            print(f"Error processing coverage report: {e}")
            return {"line": None, "branch": None}
    else:
        print("Coverage report not found.")
        return {"line": None, "branch": None}


def process_java_files_and_run_test_analysis(
        input_dir,
        test_input_file_path,
        src_dir=JAVA_SRC_DIR,
        test_dir=JAVA_TEST_DIR,
        project_dir=JAVA_PROJECT_ROOT,
        timeout=30
):
    # Track copied files for cleanup later
    copied_files = []
    timeout_occurred = False
    error = False
    source_file_path = None
    test_file_path = None
    try:
        print("INPUT FILE: ", test_input_file_path)
        # Step 1: Copy .java files to the respective directories
        v = os.listdir(input_dir)
        print("DIR: ", input_dir, "DIR CONTENT: ", v)
        for file_name in os.listdir(input_dir):
            print("List dir: ", file_name)
            if file_name.endswith(".java"):
                source_path = os.path.join(input_dir, file_name)
                if file_name == os.path.basename(test_input_file_path):
                    destination_path = os.path.join(test_dir, file_name)
                    test_file_path = destination_path
                else:
                    destination_path = os.path.join(src_dir, file_name)
                    source_file_path = destination_path
                shutil.copy(source_path, destination_path)
                copied_files.append(destination_path)


        print("TEST FILE PATH: ", test_file_path)
        print("SOURCE_FILE_PATH: ", source_file_path)
        print("INPUT DIR: ", input_dir)
        # Step 1.5: Run 'mvn test-compile' using the extracted method
        compile_results = run_maven_test_compile(project_dir, timeout)
        syntax_maven_output, syntax, compile_timeout_occurred, compile_error = compile_results

        # Update the overall timeout and error status
        timeout_occurred = timeout_occurred or compile_timeout_occurred
        # error = error or compile_error

        # Calculate assertion density and McCabe ratio
        assertions_density = assertions_density_java(test_file_path)
        print("Assertion density passed")
        try:
            mccabe = assertions_mccabe_ratio_java(source_file_path, test_file_path)
        except Exception as e:
            print("Error occurred during computation of McCabe ratio: ", e)
            mccabe = None

        if syntax != CompileStatus.OK:
            # Cleanup copied files
            return {
                "execution_time_sec": None,
                "line_coverage_percent": None,
                "branch_coverage_percent": None,
                "timeout_occurred": timeout_occurred,
                "internal_error_occurred": error,
                "syntax": syntax,
                "syntax_maven_output": syntax_maven_output,
                "assertion_density": assertions_density,
                "assertions_mccabe_ratio": mccabe,
                "runtime_errors": None,
                "test_pass_rate": None,
                "test_maven_output": None
            }

        # Run 'mvn clean test' using the extracted method
        test_results = run_maven_clean_test(project_dir, timeout)
        test_maven_output, test_timeout_occurred, test_error, execution_time = test_results
        if test_error:
            print("TEST ERROR")

        # Update the overall timeout and error status
        timeout_occurred = timeout_occurred or test_timeout_occurred
        error = error or test_error

        if timeout_occurred:
            print("TIMEOUT")

        # Parse test report and compute pass rate
        pass_rate, runtime_errors = parse_report_and_compute_pass_rate(TEST_REPORTS)
        if runtime_errors > 0:
            print("RUNTIME ERROR")

        # Compute coverage percentage using the extracted method
        coverage_percentage = compute_coverage_percentage(project_dir, source_file_path, timeout_occurred)

        # Cleanup copied files

        return {
            "execution_time_sec": execution_time,
            "line_coverage_percent": coverage_percentage["line"],
            "branch_coverage_percent": coverage_percentage["branch"],
            "timeout_occurred": timeout_occurred,
            "test_maven_output": test_maven_output,
            "syntax_maven_output": syntax_maven_output,
            "internal_error_occurred": error,
            "syntax": syntax,
            "runtime_errors": runtime_errors,
            "test_pass_rate": pass_rate,
            "assertion_density": assertions_density,
            "assertions_mccabe_ratio": mccabe
        }
    finally:
        for copied_file in copied_files:
            os.remove(copied_file)


# def validate_java_file_with_javac(file_path):
#     try:
#         # Run the javac command to compile the Java file
#         result = subprocess.run(['javac', file_path], capture_output=True, text=True)
#
#         # Check the return code
#         if result.returncode == 0:
#             # Compilation was successful, so syntax is valid
#             return CompileStatus.OK
#         else:
#             # Compilation failed, likely due to a syntax error
#             print(f"Syntax Error in file {file_path}:\n\n\n\n\n\n{result.stderr}")
#             return CompileStatus.SYNTAX_ERROR
#
#     except Exception as e:
#         # Handle any other unexpected exceptions
#         print(f"Exception occurred while validating file {file_path}: {e}")
#         return CompileStatus.EXCEPTION_OCCURRED


def parse_report_and_compute_pass_rate(test_reports):
    # Directory containing the XML report files
    print(os.getcwd())
    report_files = glob.glob(test_reports)

    total_tests = 0
    total_failures = 0
    total_skipped = 0
    total_runtime_errors = 0

    for report_file in report_files:
        tree = ET.parse(report_file)
        root = tree.getroot()
        total_tests += int(root.attrib.get('tests', 0))
        total_failures += int(root.attrib.get('failures', 0))
        total_skipped += int(root.attrib.get('skipped', 0))
        total_runtime_errors += int(root.attrib.get('errors', 0))


    print(f"Total Tests: {total_tests}")
    print(f"Failures: {total_failures}")
    print(f"Skipped: {total_skipped}")
    print(f"Passed: {total_tests - total_failures - total_skipped}")

    total_passed = total_tests - total_failures - total_skipped
    pass_percentage = (total_passed / total_tests) * 100 if total_tests != 0 else None
    return pass_percentage, total_runtime_errors