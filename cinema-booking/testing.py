import unittest
import os
import sys

def discover_tests(start_dir, exclude_dirs):
    tests = []
    for dirpath, dirnames, filenames in os.walk(start_dir):
        for filename in filenames:
            if filename.endswith('.py') and filename != '__init__.py' and filename.startswith('test_'):
                test_path = os.path.join(dirpath, filename)
                if not any(exclude_dir in test_path for exclude_dir in exclude_dirs):
                    print(f"Discovered test file: {test_path}")
                    tests.append(test_path)
    return tests


if __name__ == '__main__':
    tests = discover_tests('booking', ['database', 'databaseservice', 'frontend', 'identity'])

    sys.path.append('cinema-booking')

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Load and add test cases from each discovered test file
    for test in tests:
        print(f"Loading test module: {test}")
        try:
            module = loader.loadTestsFromModule(test)
            print(f"Loaded test module: {module}")

            for test_case in module:
                suite.addTest(test_case)

        except ImportError as e:
            print(f"Error importing test module {test}: {e}")
        except Exception as e:
            print(f"Error loading test module {test}: {e}")

    runner = unittest.TextTestRunner()
    runner.run(suite)
