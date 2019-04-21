from django.test import SimpleTestCase

from api.utils.text_tool import reverse
from .data.text_tool import POSITIVE_CASES, NEGATIVE_CASES


class ReverseTextCase(SimpleTestCase):

    def test_positive_cases(self):
        for case, result in POSITIVE_CASES.items():
            self.assertEqual(
                reverse(case),
                result
            )

    def test_negative_cases(self):
        for case in NEGATIVE_CASES:
            self.assertEqual(
                reverse(case),
                ''
            )
