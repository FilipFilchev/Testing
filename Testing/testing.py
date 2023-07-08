"""
Unit Testing
Unit testing is a software testing method by which individual units of source code, such as functions, methods, or classes, 
are tested to verify that they work correctly. 
The unittest framework in Python provides a solid base upon which to build your testing suite.
"""

import unittest

def add(x, y):
    return x + y

class TestAdd(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-2, -3), -5)

if __name__ == "__main__":
    unittest.main()


"""
Best Practices for Unit Testing:
Each unit test should be independent of the others. This allows you to run the tests in any order.

Tests should be fast. If they are slow, you will not want to run them frequently, which defeats the purpose of having tests.

Always assert in your tests. The assertions verify that the output is as expected.

Use meaningful names for your test functions. The function name should describe what the test is doing.
"""


x = 11
assert x > 0, "x should be positive"
assert x % 2 == 0, "x should be even"

system = False

while system:
    print("Happy, happy, happy")

if system != True:
    raise ValueError("Not Happy")



"""

Automation Testing
Automated testing is a way to ensure your code continues to work properly as changes are made. 
It involves writing scripts to automatically test your code rather than manually checking it. 
A common way to automate tests in Python is by using the pytest framework. """

import pytest

def add(x, y):
    return x + y

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5

"""
Best Practices for Automation Testing:
Maintain your tests: As your codebase evolves, make sure your tests are updated to match.

Avoid hard-coding data: Use fixtures or factories to create the data you need for tests.

Don’t ignore flaky tests: If a test is failing intermittently, don’t ignore it. These tests can indicate a real problem.

Use continuous integration (CI) tools: CI tools can automatically run your test suite whenever changes are pushed to your codebase.
"""

"""

Integration Testing
Integration testing is a level of software testing where individual units are combined and tested as a group. 
The purpose of this level of testing is to expose faults in the interaction between integrated units.

"""
import pytest

class Calc:
    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

class TestCalc:
    @classmethod
    def setup_class(cls):
        cls.calc = Calc()

    def test_add(self):
        assert self.calc.add(2, 3) == 5

    def test_subtract(self):
        assert self.calc.subtract(3, 2) == 1

"""
Best Practices for Integration Testing:
Test different parts of your application together to ensure they interact correctly.

Keep in mind that integration tests should go beyond just checking if components can run together — they should also ensure the components interact correctly.

Use mocks and stubs to isolate the parts of your application you're not testing.

Make sure your test suite has a good balance of unit tests and integration tests.

Like with unit tests, run your integration tests often to catch problems early.

Don't let your integration tests grow too large. If they get too big, they can become hard to maintain and slow to run.

Overall, testing is an essential aspect of software development that helps ensure your code is working as expected, and makes it easier to maintain and extend your codebase.
"""



