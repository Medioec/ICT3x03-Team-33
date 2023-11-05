import unittest
from unittest.mock import patch, MagicMock
from app import delete_inactive_sessions

class TestApp(unittest.TestCase):

    @patch('app.psycopg2.connect')
    def test_delete_inactive_sessions(self, mock_connect):
        # Test case where inactive sessions exist.
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = True  # Simulate that an inactive session exists
        delete_inactive_sessions()
        mock_cursor.execute.assert_called_with("DELETE FROM UserSessions WHERE currStatus = %s", ('inactive',))

    @patch('app.psycopg2.connect')
    def test_delete_inactive_sessions_no_sessions(self, mock_connect):
        # Test case where no inactive sessions exist.
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None  # Simulate that no inactive session exists
        delete_inactive_sessions()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM usersessions WHERE currStatus = %s", ('inactive',))

    @patch('app.psycopg2.connect')
    def test_delete_inactive_sessions_exception(self, mock_connect):
        # Test case where an exception is raised.
        mock_connect.side_effect = Exception("Test exception")  # Simulate an exception
        with self.assertRaises(UnboundLocalError):
            delete_inactive_sessions()
            

if __name__ == '__main__':
    unittest.main()
