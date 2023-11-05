import unittest
import os

def run_tests_in_directory(directory, loader, suite, exclusions):
    """Run tests in the given directory, excluding the ones specified."""
    print(f"Running tests in: {directory}")
    for dirpath, dirnames, filenames in os.walk(directory, topdown=True):
        # Skip excluded directories
        dirnames[:] = [d for d in dirnames if os.path.abspath(os.path.join(dirpath, d)) not in exclusions]

        # Perform test discovery in this directory
        tests = loader.discover(start_dir=dirpath, pattern='test*.py')
        suite.addTests(tests)

def run_all_tests(start_dir, exclusions=None):
    if exclusions is None:
        exclusions = []

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Normalize paths to avoid issues with OS-specific path formats
    exclusions = [os.path.abspath(exclusion) for exclusion in exclusions]

    # Iterate through each subdirectory and run tests
    for item in os.listdir(start_dir):
        dirpath = os.path.join(start_dir, item)
        if os.path.isdir(dirpath) and dirpath not in exclusions:
            run_tests_in_directory(dirpath, loader, suite, exclusions)

    if suite.countTestCases() == 0:
        print("No tests found. Check that your test files are correctly named and located.")
        return False

    print("Running tests...")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()

if __name__ == '__main__':
    test_dir = os.path.abspath('cinema-booking')
    exclusions = [
        os.path.join(test_dir, 'database'),
        os.path.join(test_dir, 'databaseservice'),
        os.path.join(test_dir, 'frontend'),
        os.path.join(test_dir, 'identity'),
    ]

    print("Exclusion directories:", exclusions)
    success = run_all_tests(test_dir, exclusions=exclusions)
    exit_code = 0 if success else 1
    exit(exit_code)
