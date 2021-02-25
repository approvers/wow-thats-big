import unittest

from src.type.argument_definition import ArgumentDefinition, InvalidDefinitionError
from test.measurer.util.exception_test import expect_success, expect_fail


class ArgumentDefinitionValidationTest(unittest.TestCase):

    def test(self):
        expect_success(self, lambda: ArgumentDefinition("success_plz", str, "123"), InvalidDefinitionError)
        expect_success(self, lambda: ArgumentDefinition("success_plz", str, None), InvalidDefinitionError)
        expect_fail(self, lambda: ArgumentDefinition("fail_plz", str, 123), InvalidDefinitionError)
        expect_success(self, lambda: ArgumentDefinition("success_plz", int, 123), InvalidDefinitionError)
        expect_success(self, lambda: ArgumentDefinition("success_plz", int, None), InvalidDefinitionError)
        expect_fail(self, lambda: ArgumentDefinition("fail_plz", int, "123"), InvalidDefinitionError)
        expect_fail(self, lambda: ArgumentDefinition("fail_plz", int, 123.4), InvalidDefinitionError)
        expect_success(self, lambda: ArgumentDefinition("success_plz", float, 123.1), InvalidDefinitionError)
        expect_success(self, lambda: ArgumentDefinition("success_plz", float, None), InvalidDefinitionError)
        expect_fail(self, lambda: ArgumentDefinition("fail_plz", float, 123), InvalidDefinitionError)
        expect_fail(self, lambda: ArgumentDefinition("fail_plz", float, "123"), InvalidDefinitionError)
