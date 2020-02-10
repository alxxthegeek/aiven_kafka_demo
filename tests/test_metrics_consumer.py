import datetime
from unittest import TestCase

from kaf_demo.metrics_consumer import message_extraction


class TestMetricsConsumer(TestCase):
    def __init__(self):
        self.test_message = b'{"hostname": "kaf", "system_metrics": {"total_cpu": 3.0, "current_cpu_frequency": 3092.839, ' \
                            b'"memory_use": 2009927680, "available_memory": 685264896, "percent_memory_use": 65.9, ' \
                            b'"network_traffic_in": 366622694, "network_traffic_out": 366622694, "total_network_traffic": 905024520}}'

        self.test_metrics_message = b'{"hostname": "kaf", "system_metrics": {"total_cpu": 3.0"}'

        self.test_metric_value = '{"hostname": "kaf", "system_metrics": {"total_cpu": 3.3} }'
        self.test_consumer_message = "ConsumerRecord(topic='SystemMetrics', timestamp=1581375803446, value=b'{}')"

        self.test_timestamp = datetime.datetime(2020, 2, 11, 10, 3, 23, 446000)  # timestamp 1581374929365

        self.test_consumer_data = [[datetime.datetime(2020, 2, 11, 10, 3, 23, 446000), 'kaf', 'total_cpu', 3.3]]

    def test_message_extraction(self):
        test_data = message_extraction(self.test_consumer_message)
        self.assertEqual(test_data, self.test_consumer_data)
