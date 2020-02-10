from unittest import TestCase


class TestpostgresDatabaseHandler(TestCase):

    @pytest.fixture(autouse=True)
    def _mock_db_connection(mocker, db_connection):
        mocker.patch('db.database.dbc', db_connection)
        return True

    def test_connect(self):
        self.fail()

    def test_get_cursor(self):
        self.fail()

    def test_check_database(self):
        self.fail()

    def test_close_database(self):
        self.fail()

    def test_logging_start(self):
        self.fail()

    def test_create_log_file(self):
        self.fail()
