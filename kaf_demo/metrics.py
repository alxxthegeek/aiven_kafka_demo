#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import psutil
from hurry.filesize import size


def get_total_cpu_usage():
    return psutil.cpu_percent()


def get_current_cpu_frequency():
    cpu_freq = psutil.cpu_freq()
    return cpu_freq.current


def get_total_mem_usage():
    sysmem = psutil.virtual_memory()
    return sysmem.total


def get_percent_mem_usage():
    sysmem = psutil.virtual_memory()
    return sysmem.percent


def get_available_memory():
    sysvmem = psutil.virtual_memory()
    return sysvmem.available


def get_network_traffic_in():
    net = psutil.net_io_counters()
    return net.bytes_recv


def get_network_traffic_out():
    net = psutil.net_io_counters()
    return net.bytes_sent


def get_total_network_traffic():
    net = psutil.net_io_counters()
    return net.bytes_recv + net.bytes_sent


class metrics(object):

    def create_metrics_json():
        system_metrics = {
            "total_cpu": get_total_cpu_usage(),
            "current_cpu_frequency": get_current_cpu_frequency(),
            "memory_use": get_total_mem_usage(),
            "available_memory": get_available_memory(),
            "percent_memory_use": get_percent_mem_usage(),
            "network_traffic_in": get_network_traffic_out(),
            "network_traffic_out": get_network_traffic_out(),
            "total_network_traffic": get_total_network_traffic()
        }
        return system_metrics


if __name__ == "__main__":
    metrics()
    print(metrics.create_metrics_json())
