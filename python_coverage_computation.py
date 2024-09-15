import json
import os.path
import signal
import subprocess
import threading
import time

import pytest
import coverage

def run_pytest_with_timeout(filename, timeout=60):
    def run():
        pytest.main([filename, '--tb=short'])

    thread = threading.Thread(target=run)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        raise TimeoutError("Test execution exceeded the time limit of 60 seconds")


def timeout_handler(a, b):
    raise Exception("Timeout")


@pytest.mark.timeout(30, signal)  # Optional timeout for individual tests
def get_coverage(filename, branch=False):
    directory = os.path.dirname(filename)

    # cov = coverage.Coverage(source=[directory], omit=[f'{directory}/**/test_*.py'], branch=branch)
    # cov.start()
    #
    # try:
    #     # Run pytest in the specified directory
    #     pytest.main([directory, '--tb=short', "--timeout=30", '--timeout-method=signal', filename])
    # except TimeoutError:
    #     print("Test execution exceeded the time limit and was terminated")
    # finally:
    #
    #     cov.stop()
    #     cov.save()

    if branch:
        args = ["pytest", directory, "--tb=short", "--timeout=30", "--timeout-method=signal",
                "--cov", directory, "--cov-report=json", "--cov-branch", filename]
    else:
        args = ["pytest", directory, "--tb=short", "--timeout=30", "--timeout-method=signal",
                "--cov", directory, "--cov-report=json", filename]

    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Monitor the time
    start_time = time.time()

    # Wait for the process to complete or terminate it if it exceeds the timeout
    while process.poll() is None:
        if time.time() - start_time > 30:
            # Kill the process if the timeout is exceeded
            process.terminate()  # Kill all processes in the group
            print(f"Test execution exceeded {30} seconds and was terminated.")
            return None
        time.sleep(1)

    # Collect stdout and stderr after the process completes
    stdout, stderr = process.communicate()

    # Print the output of pytest
    print(stdout.decode())
    print(stderr.decode())

    # Parse the coverage JSON report
    json_report_path = 'coverage.json'
    if os.path.exists(json_report_path):
        with open(json_report_path, 'r') as json_file:
            coverage_data = json.load(json_file)
            # Extract the overall coverage percentage
            coverage_percentage = round(coverage_data['totals']['percent_covered'], 2)
            return coverage_percentage
    else:
        print("Coverage report not found.")
        return None

    # Calculate total lines and executed lines
    total_lines = 0
    executed_lines = 0

    # for file in cov.get_data().measured_files():
    #     print("Computing for " + file)
    #     _, executable_lines, executed, _ = cov.analysis(file)
    #     total_lines += len(executable_lines)
    #     executed_lines += len(executed)

    # Report coverage summary
    return round(0, 2)

if __name__ == '__main__':
    coverage_percentage = get_coverage(filename="/Users/alex/PycharmProjects/chatgptApi/llm-test-gen/data/generated/python/flipping_bits_game/test_davinci_002_flipping_bits_game.py")
    if coverage_percentage is not None:
        print(f"Test Coverage: {coverage_percentage}%")