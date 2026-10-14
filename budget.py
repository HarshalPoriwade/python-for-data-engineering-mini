# Calculation and formatting functions for the wedding budget planner.
# Nothing in this file prints: every function returns a value so it can be tested.

REQUIRED_KEYS = ["category", "description", "estimated", "actual"]
STATUS_LIMIT = 10  # percent away from the estimate before we raise a flag


def validate_expense(expense):
    """Return (clean_expense, None) if valid, or (None, error_message) if not."""
    for key in REQUIRED_KEYS:
        if key not in expense:
            name = str(expense.get("description", "(no description)"))
            return None, "Error: " + name + " is missing the '" + key + "' key"

    clean = {
        "category": str(expense["category"]).strip().title(),
        "description": str(expense["description"]).strip(),
    }
    for key in ["estimated", "actual"]:
        try:
            value = float(expense[key])
        except (ValueError, TypeError):
            return None, "Error: " + clean["description"] + " has a non-numeric " + key + " value: " + repr(expense[key])
        if value < 0:
            return None, "Error: " + clean["description"] + " has a negative " + key + " value: " + str(expense[key])
        clean[key] = value
    return clean, None


def validate_expenses(expenses):
    """Split a list of expenses into (valid_expenses, error_messages)."""
    valid = []
    errors = []
    for expense in expenses:
        clean, error = validate_expense(expense)
        if error is None:
            valid.append(clean)
        else:
            errors.append(error)
    return valid, errors


def compute_totals(expenses, total_budget):
    """Return a dictionary with total estimated, total actual and remaining budget."""
    total_estimated = sum([e["estimated"] for e in expenses])
    total_actual = sum([e["actual"] for e in expenses])
    return {
        "estimated": total_estimated,
        "actual": total_actual,
        "remaining": total_budget - total_actual,
    }


def group_by_category(expenses):
    """Return {category: {"estimated": total, "actual": total}} in first-seen order."""
    groups = {}
    for e in expenses:
        if e["category"] not in groups:
            groups[e["category"]] = {"estimated": 0.0, "actual": 0.0}
        groups[e["category"]]["estimated"] += e["estimated"]
        groups[e["category"]]["actual"] += e["actual"]
    return groups


def category_percentages(expenses):
    """Return {category: percent of the total estimated budget, one decimal place}."""
    groups = group_by_category(expenses)
    total_estimated = sum([g["estimated"] for g in groups.values()])
    percentages = {}
    for category, totals in groups.items():
        try:
            percentages[category] = round(totals["estimated"] / total_estimated * 100, 1)
        except ZeroDivisionError:
            percentages[category] = 0.0
    return percentages


def get_status(estimated, actual):
    """Compare actual with estimated and return a status string."""
    try:
        change = (actual - estimated) / estimated * 100
    except ZeroDivisionError:
        # Nothing was estimated, so any spending at all is over budget.
        if actual > 0:
            return "Over budget"
        return "On track"
    if change > STATUS_LIMIT:
        return "Over budget"
    if change < -STATUS_LIMIT:
        return "Under budget"
    return "On track"


def add_statuses(expenses):
    """Return new expense dictionaries that also contain a 'status' key."""
    result = []
    for e in expenses:
        row = dict(e)
        row["status"] = get_status(e["estimated"], e["actual"])
        result.append(row)
    return result


def get_actual(expense):
    return expense["actual"]


def sort_by_actual(expenses):
    """Return the expenses sorted by actual cost, largest first."""
    return sorted(expenses, key=get_actual, reverse=True)


def count_over_budget_categories(expenses):
    """Count categories whose combined actual is more than 10% over their estimate."""
    groups = group_by_category(expenses)
    over = [c for c, t in groups.items() if get_status(t["estimated"], t["actual"]) == "Over budget"]
    return len(over)


def format_money(amount):
    """Format a number as money, e.g. 1234.5 -> '$1,234.50' and -50 -> '-$50.00'."""
    if amount < 0:
        return "-$" + format(-amount, ",.2f")
    return "$" + format(amount, ",.2f")


def format_report(expenses):
    """Return the summary report as a list of text lines (already sorted and with status)."""
    header = "Category".ljust(14) + "Description".ljust(28) + "Estimated".rjust(12) + "Actual".rjust(12) + "  Status"
    lines = [header, "-" * len(header)]
    for e in expenses:
        lines.append(
            e["category"].ljust(14)
            + e["description"].ljust(28)
            + format_money(e["estimated"]).rjust(12)
            + format_money(e["actual"]).rjust(12)
            + "  " + e["status"]
        )
    return lines