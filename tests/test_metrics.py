import metrics
from unittest import mock, TestCase


class Test(TestCase):


    @mock.patch("psutil.cpu_percent")
    def test_get_total_cpu_usage(self, cpu_percent):
        cpu_percent.return_value = 66.4
        test_value = metrics.get_total_cpu_usage()
        self.assertEqual(test_value, cpu_percent())

    def test_get_current_cpu_frequency(self):
        self.fail()

    def test_get_total_mem_usage(self):
        self.fail()

    def test_get_percent_mem_usage(self):
        self.fail()

    def test_get_available_memory(self):
        self.fail()

    def test_get_network_traffic_in(self):
        self.fail()

    def test_get_network_traffic_out(self):
        self.fail()

    def test_get_total_network_traffic(self):
        self.fail()

    def test_metrics(self):
        self.fail()
