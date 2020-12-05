from src.data.data_fetcher import (
    _handle_two_year_transaction_period,
    _handle_recipient_committee_type,
)


class TestTransactionPeriod:
    pass


class TestCommitteeType:
    def test_allows_lower(self):
        expected = "H"

        result = _handle_recipient_committee_type("h")
        assert expected == result

        result = _handle_recipient_committee_type("house")
        assert expected == result

    def test_allows_lower_s(self):
        expected = "S"
        result = _handle_recipient_committee_type("s")
        assert expected == result

        result = _handle_recipient_committee_type("senate")
        assert expected == result

    def test_allows_lower_p(self, capsys):
        """
        This one additionally tests that the error message doesn't fire
        """
        error_msg = "Invalid input, defaulting to Presidential\n"
        expected = "P"

        result = _handle_recipient_committee_type("p")
        captured = capsys.readouterr().out
        assert expected == result
        assert captured == ""

        result = _handle_recipient_committee_type("presidential")
        captured = capsys.readouterr().out
        assert expected == result
        assert captured == ""
