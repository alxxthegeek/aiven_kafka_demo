from unittest import TestCase


class TestMetricsProducer(TestCase):

    def __init__(self):
        self.test_metrics_message = b'{"hostname": "kaf", "system_metrics": {"total_cpu": 3.0"}'


    def test_send_message(self):
        self.fail()

