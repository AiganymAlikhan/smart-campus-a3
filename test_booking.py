import copy
import unittest

from booking import can_book

NOW = 540
EXISTING = [(600, 660)]


def check(start, end, now=NOW, blocked=False, existing=None):
    if existing is None:
        existing = list(EXISTING)
    return can_book(start, end, now, blocked, existing)


class TestRequiredCases(unittest.TestCase):
    def test_touching_end_of_existing_allowed(self):
        self.assertTrue(check(660, 720))

    def test_overlap_rejected(self):
        self.assertFalse(check(630, 690))

    def test_blocked_rejects_valid_request(self):
        self.assertFalse(check(660, 720, blocked=True))

    def test_duration_exactly_120_allowed(self):
        self.assertTrue(check(720, 840))

    def test_duration_121_rejected(self):
        self.assertFalse(check(720, 841))

    def test_start_equal_to_now_rejected(self):
        self.assertFalse(check(540, 570))


class TestTimeValidation(unittest.TestCase):
    def test_start_one_minute_after_now_allowed(self):
        self.assertTrue(check(541, 571))

    def test_start_before_now_rejected(self):
        self.assertFalse(check(500, 530))

    def test_reversed_times_rejected(self):
        self.assertFalse(check(760, 700))

    def test_zero_length_rejected(self):
        self.assertFalse(check(700, 700))

    def test_end_at_day_bound_allowed(self):
        self.assertTrue(check(1380, 1440))

    def test_end_past_day_bound_rejected(self):
        self.assertFalse(check(1380, 1441))

    def test_last_minute_of_day_allowed(self):
        self.assertTrue(check(1439, 1440, now=1438))

    def test_full_120_minutes_ending_at_midnight_allowed(self):
        self.assertTrue(check(1320, 1440))


class TestOverlap(unittest.TestCase):
    def test_touching_start_of_existing_allowed(self):
        self.assertTrue(check(570, 600))

    def test_one_minute_overlap_at_start_rejected(self):
        self.assertFalse(check(570, 601))

    def test_one_minute_overlap_at_end_rejected(self):
        self.assertFalse(check(659, 720))

    def test_exact_duplicate_rejected(self):
        self.assertFalse(check(600, 660))

    def test_containing_existing_rejected(self):
        self.assertFalse(check(590, 670))

    def test_inside_existing_rejected(self):
        self.assertFalse(check(610, 650))

    def test_empty_existing_allowed(self):
        self.assertTrue(check(600, 660, existing=[]))

    def test_fits_between_multiple_bookings(self):
        self.assertTrue(check(660, 720, existing=[(600, 660), (720, 780)]))

    def test_overlaps_second_of_multiple_bookings(self):
        self.assertFalse(check(690, 750, existing=[(600, 660), (720, 780)]))

    def test_overlap_detected_in_unsorted_existing(self):
        self.assertFalse(check(690, 750, existing=[(720, 780), (600, 660)]))


class TestTypes(unittest.TestCase):
    def test_float_start_rejected(self):
        self.assertFalse(check(700.0, 760))

    def test_float_end_rejected(self):
        self.assertFalse(check(700, 760.0))

    def test_bool_start_rejected(self):
        # With now=0, True (== 1) would pass every other check, so only
        # the bool guard in _is_int can reject this request.
        self.assertFalse(check(True, 60, now=0))

    def test_bool_end_rejected(self):
        self.assertFalse(check(700, True))


class TestNoMutation(unittest.TestCase):
    def test_existing_unchanged_on_accept(self):
        existing = [(600, 660), (720, 780)]
        before = copy.deepcopy(existing)
        self.assertTrue(can_book(660, 720, NOW, False, existing))
        self.assertEqual(existing, before)

    def test_existing_unchanged_on_reject(self):
        existing = [(600, 660), (720, 780)]
        before = copy.deepcopy(existing)
        self.assertFalse(can_book(630, 690, NOW, False, existing))
        self.assertEqual(existing, before)


if __name__ == "__main__":
    unittest.main()
