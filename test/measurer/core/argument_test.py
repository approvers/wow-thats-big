import unittest
from typing import List

from src.measure import generate_argument
from src.type.argument_definition import ArgumentDefinition
from test.measurer.util.exception_test import expect_success, expect_fail


class ArgumentTest(unittest.TestCase):
    def generate_required_arguments(self):
        required_argument: List[ArgumentDefinition] = [
            ArgumentDefinition(name="str_nodef", default_value=None, arg_type=str),
            ArgumentDefinition(name="str_def", default_value="default_value", arg_type=str),
            ArgumentDefinition(name="int_nodef", default_value=None, arg_type=int),
            ArgumentDefinition(name="int_def", default_value=12345, arg_type=int),
        ]
        expected_argument_key = {"str_nodef", "str_def", "int_nodef", "int_def"}

        return [required_argument, expected_argument_key]

    def test_fully_provided(self):
        required_argument, expected_argument_key = self.generate_required_arguments()

        # Fully provided
        #   - override default value
        #   - no error
        fully_provided = expect_success(self, lambda: generate_argument(required_argument, {
            "str_nodef": "provided_value",
            "str_def": "provided_value_2",
            "int_nodef": 123,
            "int_def": 456
        }))
        self.assertEqual(set(fully_provided.keys()), expected_argument_key)
        self.assertEqual(fully_provided["str_nodef"], "provided_value")
        self.assertEqual(fully_provided["str_def"], "provided_value_2")
        self.assertEqual(fully_provided["int_nodef"], 123)
        self.assertEqual(fully_provided["int_def"], 456)

    def test_extra_provided(self):
        required_argument, expected_argument_key = self.generate_required_arguments()

        # Extra provided; unnecessary arguments are passed with required ones
        #  - matches requirements in Fully overrided test
        #  - remove extra arguments
        extra_provided = expect_success(self, lambda: generate_argument(required_argument, {
            "str_nodef": "provided_value",
            "str_def": "provided_value_2",
            "int_nodef": 123,
            "int_def": 456,
            "extra_str": "extra_value",
            "extra_int": 789
        }))
        self.assertEqual(set(extra_provided.keys()), expected_argument_key)
        self.assertEqual(extra_provided["str_nodef"], "provided_value")
        self.assertEqual(extra_provided["str_def"], "provided_value_2")
        self.assertEqual(extra_provided["int_nodef"], 123)
        self.assertEqual(extra_provided["int_def"], 456)

    def test_partial_default_used(self):
        required_argument, expected_argument_key = self.generate_required_arguments()

        # Partial default used; some argument with default value are omitted (int_def: 12345)
        #  - fill omitted arguments using default value
        partial_default_used = expect_success(self, lambda: generate_argument(required_argument, {
            "str_nodef": "provided_value",
            "str_def": "provided_value_2",
            "int_nodef": 123,
        }))
        self.assertEqual(set(partial_default_used.keys()), expected_argument_key)
        self.assertEqual(partial_default_used["str_nodef"], "provided_value")
        self.assertEqual(partial_default_used["str_def"], "provided_value_2")
        self.assertEqual(partial_default_used["int_nodef"], 123)
        self.assertEqual(partial_default_used["int_def"], 12345)

    def test_fully_default_used(self):
        required_argument, expected_argument_key = self.generate_required_arguments()

        # Fully default used; all argument with default value are omitted
        #  - fill omitted arguments using default value
        fully_default_used = expect_success(self, lambda: generate_argument(required_argument, {
            "str_nodef": "provided_value",
            "int_nodef": 123,
        }))
        self.assertEqual(set(fully_default_used.keys()), expected_argument_key)
        self.assertEqual(fully_default_used["str_nodef"], "provided_value")
        self.assertEqual(fully_default_used["str_def"], "default_value")
        self.assertEqual(fully_default_used["int_nodef"], 123)
        self.assertEqual(fully_default_used["int_def"], 12345)

    def test_not_enough_args_passed(self):
        required_argument, expected_argument_key = self.generate_required_arguments()

        # Not enough arguments passed; arguments with no default value are omitted
        expect_fail(self, lambda: generate_argument(required_argument, {
            "str_nodef": "provided_value",
        }), RuntimeError)

    def test_type_mismatch(self):
        required_argument, expected_argument_key = self.generate_required_arguments()

        # Type mismatch; the type of value is different between provided and required
        expect_fail(self, lambda: generate_argument(required_argument, {
            "str_nodef": 123,
            "int_nodef": "str"
        }), TypeError)
