import unittest

import budget
from budget_data import EXPENSES, TOTAL_BUDGET


def make(category, description, estimated, actual):
    return {"category": category, "description": description, "estimated": estimated, "actual": actual}


class TestValidation(unittest.TestCase):
    def test_valid_expense_is_cleaned(self):
        clean, error = budget.validate_expense(make("  venue ", "Hall ", "7000", 7500))
        self.assertIsNone(error)
        self.assertEqual(clean["category"], "Venue")
        self.assertEqual(clean["description"], "Hall")
        self.assertEqual(clean["estimated"], 7000.0)
        self.assertEqual(clean["actual"], 7500.0)

    def test_missing_key_is_an_error(self):
        clean, error = budget.validate_expense({"category": "Cake", "description": "Cake", "estimated": 300})
        self.assertIsNone(clean)
        self.assertIn("missing the 'actual' key", error)

    def test_missing_description_still_gives_a_message(self):
        clean, error = budget.validate_expense({"category": "Cake", "estimated": 1, "actual": 1})
        self.assertIsNone(clean)
        self.assertIn("(no description)", error)

    def test_negative_value_is_an_error(self):
        clean, error = budget.validate_expense(make("Transport", "Car", 350, -50))
        self.assertIsNone(clean)
        self.assertIn("negative actual", error)

    def test_non_numeric_value_is_an_error(self):
        clean, error = budget.validate_expense(make("Favours", "Gifts", "two hundred", 180))
        self.assertIsNone(clean)
        self.assertIn("non-numeric estimated", error)

    def test_none_value_is_an_error(self):
        clean, error = budget.validate_expense(make("Favours", "Gifts", 100, None))
        self.assertIsNone(clean)
        self.assertIn("non-numeric actual", error)

    def test_sample_data_skips_three_bad_expenses(self):
        valid, errors = budget.validate_expenses(EXPENSES)
        self.assertEqual(len(valid), 9)
        self.assertEqual(len(errors), 3)


class TestTotalsAndPercentages(unittest.TestCase):
    def setUp(self):
        self.valid, _ = budget.validate_expenses(EXPENSES)

    def test_totals_for_sample_data(self):
        totals = budget.compute_totals(self.valid, TOTAL_BUDGET)
        self.assertEqual(totals["estimated"], 20000)
        self.assertEqual(totals["actual"], 20850)
        self.assertEqual(totals["remaining"], -850)

    def test_totals_of_empty_list(self):
        totals = budget.compute_totals([], 20000)
        self.assertEqual(totals, {"estimated": 0, "actual": 0, "remaining": 20000})

    def test_category_percentages(self):
        percentages = budget.category_percentages(self.valid)
        self.assertEqual(percentages["Venue"], 35.0)
        self.assertEqual(percentages["Catering"], 28.0)
        self.assertEqual(percentages["Music"], 4.5)
        self.assertEqual(list(percentages.keys())[0], "Venue")
        self.assertAlmostEqual(sum(percentages.values()), 100.0)

    def test_percentages_round_to_one_decimal(self):
        percentages = budget.category_percentages([make("A", "a", 1, 1), make("B", "b", 2, 2)])
        self.assertEqual(percentages, {"A": 33.3, "B": 66.7})

    def test_percentages_when_everything_estimated_at_zero(self):
        percentages = budget.category_percentages([make("A", "a", 0.0, 10.0)])
        self.assertEqual(percentages, {"A": 0.0})


class TestStatus(unittest.TestCase):
    def test_over_budget(self):
        self.assertEqual(budget.get_status(1000, 1101), "Over budget")

    def test_under_budget(self):
        self.assertEqual(budget.get_status(1000, 899), "Under budget")

    def test_exactly_ten_percent_is_on_track(self):
        self.assertEqual(budget.get_status(1000, 1100), "On track")
        self.assertEqual(budget.get_status(1000, 900), "On track")

    def test_zero_estimate(self):
        self.assertEqual(budget.get_status(0, 50), "Over budget")
        self.assertEqual(budget.get_status(0, 0), "On track")

    def test_add_statuses_does_not_change_input(self):
        expenses = [make("A", "a", 100.0, 200.0)]
        result = budget.add_statuses(expenses)
        self.assertEqual(result[0]["status"], "Over budget")
        self.assertNotIn("status", expenses[0])


class TestReport(unittest.TestCase):
    def setUp(self):
        self.valid, _ = budget.validate_expenses(EXPENSES)

    def test_sort_by_actual_descending(self):
        actuals = [e["actual"] for e in budget.sort_by_actual(self.valid)]
        self.assertEqual(actuals, [7500, 5800, 2100, 2000, 1150, 1000, 550, 450, 300])

    def test_count_over_budget_categories(self):
        # Three expenses are over budget, but Attire as a whole is only 9.1% over.
        self.assertEqual(budget.count_over_budget_categories(self.valid), 2)

    def test_format_money(self):
        self.assertEqual(budget.format_money(1234.5), "$1,234.50")
        self.assertEqual(budget.format_money(-850), "-$850.00")

    def test_report_lines(self):
        rows = budget.sort_by_actual(budget.add_statuses(self.valid))
        lines = budget.format_report(rows)
        self.assertTrue(lines[0].startswith("Category"))
        self.assertEqual(set(lines[1]), {"-"})
        self.assertEqual(len(lines), 2 + 9)
        self.assertIn("Reception hall hire", lines[2])
        self.assertIn("$7,500.00", lines[2])
        self.assertTrue(lines[2].endswith("On track"))
        self.assertTrue(lines[-1].endswith("Under budget"))


if __name__ == "__main__":
    unittest.main()