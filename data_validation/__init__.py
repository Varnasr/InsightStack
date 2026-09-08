"""Data validation: a list of things wrong with a file, before it reaches a finding.

    from data_validation import validate, Rules

    report = validate(df, Rules(
        id="hh_id",
        required=["consent", "hh_size"],
        ranges={"age": (0, 110), "hh_size": (1, 30)},
        allowed={"gender": ["M", "F", "O"]},
        types={"income": "numeric", "date": "date"},
        names="snake_case",
    ))
    report.issues        # one row per problem: id, variable, value, check, message
    report.summary()     # counts by check
    report.ok            # True only when nothing fired

Everything here returns rows a person can act on, not a boolean. A validation
that prints "3 problems" has told you nothing you can fix; one that lists the
three ids and what is wrong with each has.

Nothing corrects anything. The version this replaced printed
`df[~df.gender.isin(["M", "F"])]` and stopped, which is a validation only in
the sense that a smoke alarm is a fire brigade.
"""

from .validate import Rules, Report, validate, check_cross_file_ids

__all__ = ["Rules", "Report", "validate", "check_cross_file_ids"]
