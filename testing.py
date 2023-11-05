import unittest

def all_tests_suite():
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    # Add tests from each folder
    test_suite.addTests(test_loader.discover('cinema-booking\booking'))
    test_suite.addTests(test_loader.discover('cinema-booking\common\test_api_crypto.py'))
    test_suite.addTests(test_loader.discover('cinema-booking\databaseservice'))
    test_suite.addTests(test_loader.discover('cinema-booking\identity'))
    test_suite.addTests(test_loader.discover('cinema-booking\movie'))
    test_suite.addTests(test_loader.discover('cinema-booking\sessioncleaning\test_app.py'))
    test_suite.addTests(test_loader.discover('cinema-booking\payment'))
    # Add more folders as needed

    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(all_tests_suite())
