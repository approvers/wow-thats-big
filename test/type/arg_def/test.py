import unittest

from src.type.argument_definition import ArgumentDefinition, InvalidDefinitionError


class ArgumentDefinitionValidationTest(unittest.TestCase):
    def expect_success(self, f):
        try:
            f()
        except InvalidDefinitionError as e:
            self.fail(e)

    def expect_fail(self, f):
        try:
            f()
            self.fail("Fall expected, but succeeded")
        except InvalidDefinitionError as e:
            pass

    def test(self):
        self.expect_success(lambda: ArgumentDefinition("success_plz", str, "123"))
        self.expect_success(lambda: ArgumentDefinition("success_plz", str, None))
        self.expect_fail(lambda: ArgumentDefinition("fail_plz", str, 123))
        self.expect_success(lambda: ArgumentDefinition("success_plz", int, 123))
        self.expect_success(lambda: ArgumentDefinition("success_plz", int, None))
        self.expect_fail(lambda: ArgumentDefinition("fail_plz", int, "123"))
        self.expect_fail(lambda: ArgumentDefinition("fail_plz", int, 123.4))
        self.expect_success(lambda: ArgumentDefinition("success_plz", float, 123.1))
        self.expect_success(lambda: ArgumentDefinition("success_plz", float, None))
        self.expect_fail(lambda: ArgumentDefinition("fail_plz", float, 123))
        self.expect_fail(lambda: ArgumentDefinition("fail_plz", float, "123"))
