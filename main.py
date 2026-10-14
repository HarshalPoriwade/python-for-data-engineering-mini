# Command-line entry point: prints the four budget features and the report.
from budget_data import EXPENSES, TOTAL_BUDGET
import budget


def print_title(text):
    print()
    print(text.upper())
    print("=" * len(text))


def main():
    print_title("Checking expense data")
    valid, errors = budget.validate_expenses(EXPENSES)
    for message in errors:
        print(message)
    print("Valid expenses: " + str(len(valid)) + ", skipped: " + str(len(errors)))

    print_title("Budget totals")
    totals = budget.compute_totals(valid, TOTAL_BUDGET)
    print("Total budget:     " + budget.format_money(TOTAL_BUDGET))
    print("Total estimated:  " + budget.format_money(totals["estimated"]))
    print("Total actual:     " + budget.format_money(totals["actual"]))
    print("Remaining budget: " + budget.format_money(totals["remaining"]))
    if totals["remaining"] < 0:
        print("Warning: actual spending is over the total budget!")

    print_title("Category breakdown")
    for category, percent in budget.category_percentages(valid).items():
        print(category + ": " + str(percent) + "% of estimated budget")

    print_title("Expense status")
    with_status = budget.add_statuses(valid)
    for e in with_status:
        print(e["description"] + ": " + e["status"])

    print_title("Summary report")
    for line in budget.format_report(budget.sort_by_actual(with_status)):
        print(line)

    print()
    print("Categories over budget: " + str(budget.count_over_budget_categories(valid)))


if __name__ == "__main__":
    main()