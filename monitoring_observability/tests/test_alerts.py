import unittest
from unittest.mock import patch
import slack_alerts

class TestAlerts(unittest.TestCase):

    @patch('slack_alerts.requests.post')
    def test_slack_alert(self, mock_post):
        # Simuler succès de la requête
        mock_post.return_value.status_code = 200
        slack_alerts.send_slack_alert("Test alert Slack")
        mock_post.assert_called_once()
        print("✅ Slack alert test passed")

    @patch('slack_alerts.smtplib.SMTP')
    def test_email_alert(self, mock_smtp):
        # Simuler connexion SMTP
        instance = mock_smtp.return_value
        instance.sendmail.return_value = {}
        slack_alerts.send_email_alert("Test Email", "Body of test email")
        instance.starttls.assert_called_once()
        instance.login.assert_called_once()
        instance.sendmail.assert_called_once()
        print("✅ Email alert test passed")

if __name__ == "__main__":
    unittest.main()
