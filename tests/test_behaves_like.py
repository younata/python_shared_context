import unittest

from shared_context import behaves_like


def adds_tests_to_class(self):
    self.assertTrue(True)


def can_specify_multiple_tests_as_args(self):
    self.assertTrue(True)


def can_specify_any_kwarg_as_context(self, **kwargs):
    self.assertDictEqual(kwargs, {"foo": "bar"})


def passes_context_to_all_tests(self, **kwargs):
    self.assertDictEqual(kwargs, {"foo": "bar"})


@behaves_like(adds_tests_to_class)
class TestBehavesLikeSingleTest(unittest.TestCase):
    pass


@behaves_like(adds_tests_to_class, can_specify_multiple_tests_as_args)
class TestBehavesLikeWithoutContext(unittest.TestCase):
    pass


@behaves_like(can_specify_any_kwarg_as_context, passes_context_to_all_tests, foo="bar")
class TestBehavesLikeWithContext(unittest.TestCase):
    pass


can_pass_tests_to_add_as_list = [adds_tests_to_class, can_specify_multiple_tests_as_args]


@behaves_like(can_pass_tests_to_add_as_list)
class TestBehavesLikeCanReceiveTestsAsListInsteadOfArgs(unittest.TestCase):
    pass


@behaves_like(can_pass_tests_to_add_as_list, lambda self: self.assertTrue(True))
class TestBehavesLikeCanReceiveTestsAsListAndArgs(unittest.TestCase):
    pass


class TestCorrectNumberOfTestsAddedToEachTestCase(unittest.TestCase):
    def assert_has_tests(self, klass, number):
        tests = [method for method in dir(klass) if callable(getattr(klass, method)) and method.startswith("test_")]
        self.assertEqual(len(tests), number)

    def test_single_test_has_1(self):
        self.assert_has_tests(TestBehavesLikeSingleTest, 1)

    def test_multiple_without_context_has_2(self):
        self.assert_has_tests(TestBehavesLikeWithoutContext, 2)

    def test_with_contexts_has_2(self):
        self.assert_has_tests(TestBehavesLikeWithContext, 2)

    def test_can_receive_tests_as_list_instead_of_args_has_2(self):
        self.assert_has_tests(TestBehavesLikeCanReceiveTestsAsListInsteadOfArgs, 2)

    def test_can_receive_tests_as_list_and_args_has_3(self):
        self.assert_has_tests(TestBehavesLikeCanReceiveTestsAsListAndArgs, 3)
