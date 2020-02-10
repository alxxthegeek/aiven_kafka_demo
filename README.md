
Exercise




Installation




How to use



PostgreSQL schema

Database kaf_demo

Table system_metrics


CREATE TABLE public.system_metrics (
    id SERIAL NOT NULL,
    datetime timestamp without time zone,
    hostname character varying(64) NOT NULL,
    metric character varying(64) NOT NULL,
    value real NOT NULL,
    CONSTRAINT sys_metrics_prikey PRIMARY KEY (id)
);

 GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO aivenadmin;
 GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public To aivenadmin;
 ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO aivenadmin;



 kaf_demo=# SELECT COUNT(*) FROM system_metrics;
 count
-------
   848
(1 row)

kaf_demo=# select * from system_metrics;
 id  |        datetime         | hostname |        metric         |    value
-----+-------------------------+----------+-----------------------+-------------
   1 | 2020-02-09 22:17:50.37  | kaf      | total_cpu             |         9.1
   2 | 2020-02-09 22:17:50.37  | kaf      | current_cpu_frequency |     3092.84
   3 | 2020-02-09 22:17:50.37  | kaf      | memory_use            | 2.00993e+09
   4 | 2020-02-09 22:17:50.37  | kaf      | available_memory      | 6.86539e+08
   5 | 2020-02-09 22:17:50.37  | kaf      | percent_memory_use    |        65.8
   6 | 2020-02-09 22:17:50.37  | kaf      | network_traffic_in    | 2.27999e+08
   7 | 2020-02-09 22:17:50.37  | kaf      | network_traffic_out   | 2.27999e+08
   8 | 2020-02-09 22:17:50.37  | kaf      | total_network_traffic | 7.46554e+08
   9 | 2020-02-09 22:18:00.39  | kaf      | total_cpu             |        40.9
  10 | 2020-02-09 22:18:00.39  | kaf      | current_cpu_frequency |     3092.84
  11 | 2020-02-09 22:18:00.39  | kaf      | memory_use            | 2.00993e+09
  12 | 2020-02-09 22:18:00.39  | kaf      | available_memory      | 6.79444e+08
  13 | 2020-02-09 22:18:00.39  | kaf      | percent_memory_use    |        66.2
  14 | 2020-02-09 22:18:00.39  | kaf      | network_traffic_in    | 2.28014e+08
  15 | 2020-02-09 22:18:00.39  | kaf      | network_traffic_out   | 2.28014e+08
  16 | 2020-02-09 22:18:00.39  | kaf      | total_network_traffic | 7.46584e+08
  17 | 2020-02-09 22:18:10.51  | kaf      | total_cpu             |        23.9
  18 | 2020-02-09 22:18:10.51  | kaf      | current_cpu_frequency |     3092.84
  19 | 2020-02-09 22:18:10.51  | kaf      | memory_use            | 2.00993e+09
  20 | 2020-02-09 22:18:10.51  | kaf      | available_memory      | 6.77962e+08
  21 | 2020-02-09 22:18:10.51  | kaf      | percent_memory_use    |        66.3
  22 | 2020-02-09 22:18:10.51  | kaf      | network_traffic_in    | 2.28033e+08
  23 | 2020-02-09 22:18:10.51  | kaf      | network_traffic_out   | 2.28033e+08
  24 | 2020-02-09 22:18:10.51  | kaf      | total_network_traffic |  7.4662e+08
  25 | 2020-02-09 22:18:20.541 | kaf      | total_cpu             |        19.3
  26 | 2020-02-09 22:18:20.541 | kaf      | current_cpu_frequency |     3092.84
  27 | 2020-02-09 22:18:20.541 | kaf      | memory_use            | 2.00993e+09
  28 | 2020-02-09 22:18:20.541 | kaf      | available_memory      | 6.78019e+08
  29 | 2020-02-09 22:18:20.541 | kaf      | percent_memory_use    |        66.3
  30 | 2020-02-09 22:18:20.541 | kaf      | network_traffic_in    | 2.28045e+08
  31 | 2020-02-09 22:18:20.541 | kaf      | network_traffic_out   | 2.28045e+08
  32 | 2020-02-09 22:18:20.541 | kaf      | total_network_traffic | 7.46645e+08
  33 | 2020-02-09 22:18:30.584 | kaf      | total_cpu             |        26.2
  34 | 2020-02-09 22:18:30.584 | kaf      | current_cpu_frequency |     3092.84
  35 | 2020-02-09 22:18:30.584 | kaf      | memory_use            | 2.00993e+09
  36 | 2020-02-09 22:18:30.584 | kaf      | available_memory      | 6.78076e+08
  37 | 2020-02-09 22:18:30.584 | kaf      | percent_memory_use    |        66.3
  38 | 2020-02-09 22:18:30.584 | kaf      | network_traffic_in    | 2.28057e+08
  39 | 2020-02-09 22:18:30.584 | kaf      | network_traffic_out   | 2.28057e+08


Discussion

Logs are stored into
../kaf_demo/logs

Please note the logging is currently set to debug which will produce an excessive amount of log entries but is useful when learning how a
system works(as I've never used kafka before).
Logging code is from previous projects of mine(pretty simple).

Implementation is using a single producer and single consumer.
Performance could be improved by  implementing a separate producer for each metric type and a separate consumer using threads.
A threaded alternative to metrics.prod.py is metrics_producer.py. In this implementation it does not provide any benefits.

In the producer used the python-kafka serializer as I saw it in an example(medium article) and decided to use it.

Only eight metrics were implemented - total cpu %, current cpu frequency (GHz), memory use(Total memory usage), percent memory use(%),
network traffic in (bytes received), network traffic out(bytes sent) and total network traffic(bytes received and sent).
Used psutils as it works on all platforms, I have used it before and it is easy to get it up and running.

I used the pyscopg2 library for the postgres access.

I tried to use the pyscopg2.extra.execute_values but was getting tuple errors that I could not fix in the time I set myself
so reverted to using a loop and saving each metric from the message separately. Not optimal/in-efficient.

No recovery from errors is implemented.If an error or exception occurs the system will exit.

The table schema is simple(naive) for ease/speed of implementation and is fairly wasteful. It does not record the metric type or
type of units. A more optimal solution would be a table per metric

The solution is manually deployed.
A better solution would have been to setup the project in a virtual env and then deploy the virtual env via pip.
















