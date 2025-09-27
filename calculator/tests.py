# tests.py

import sys
import os
import unittest

# Add parent directory to path to import functions module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pkg.calculator import Calculator
from functions.get_files_info import get_files_info
from functions.get_files_info import get_file_content
from functions.get_files_info import write_file
from functions.get_files_info import run_python_file


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self):
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self):
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")


if __name__ == "__main__":
    # Get the working directory (parent of calculator directory)
    working_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Test running main.py without arguments (should print usage)
    result = run_python_file(working_dir, "calculator/main.py")
    print(result)
    print()

    # Test running main.py with calculation arguments
    result = run_python_file(working_dir, "calculator/main.py", ["3 + 5"])
    print(result)
    print()
    
    # Test running tests.py (should run unit tests)
    result = run_python_file(working_dir, "calculator/tests.py")
    print(result)
    print()
    
    # Test running non-existent file (should error)
    result = run_python_file(working_dir, "nonexistent.py")
    print(result)
    
    # Test running file outside working directory (should error)
    result = run_python_file(working_dir, "../main.py")
    print(result)
    print()
    
    
