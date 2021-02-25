from unittest import TestCase


def expect_success(test_case: TestCase, f, type=Exception):
    try:
        return f()
    except type as e:
        test_case.fail(e)


def expect_fail(test_case: TestCase, f, type=Exception):
    try:
        f()
        test_case.fail("Fall expected, but succeeded")
    except type as e:
        pass
