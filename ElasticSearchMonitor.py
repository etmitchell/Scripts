# Make a ElasticSearch monitor. Print an alert
# when server(s) in cluster show signs of slowdown.
#
# A few assumptions are made:
# * Normal range for requests is under 0.1 sec
#   anything outside that range is a timeout/
#   indication of a system slowdown.
# * Garbage Collection happens every 10 seconds
# * PEP 8 Line Length conventions are also relaxed
#
# Note: This was tested in a fresh install of ES
#       on a personal VPS.
#
# TODO: (in no specific order)
# * Provide Front-End for graphs of system.
# * Save logs to SQLite DB for historical data.
# * Handle Timeout/etc Exceptions more gracefully.
import requests
import json
from collections import defaultdict
import time

ENDPOINT = 'http://localhost:9200'
CLUSTER = '_cluster'
NODES = '_nodes'
TIMEOUT = 0.1

CURRENT_NODES = 1
CPU_THRESH = 95 # Percent
MEM_THRESH = 100 # Percent
GC_THRESH = 10000 # In milliseconds
MAX_SHARDS = 10 # For now
JVM_MEM_THRESH = 95 # JVM Heap size is set automatically, 50% of system RAM

class ESMonitor(object):
    # Generic __init__
    def __init__(self):
        self.connect = ''
        self.payload = ''
        self.timeout = ''

    # Return list of all nodes in cluster.
    def node_list(self,payload):
        payload = json.loads(payload)
        n_list = defaultdict(dict)

        for id, node in payload['nodes'].iteritems():
            n_list[node['name']] = node['http_address']
        return n_list

    # Parse stats for each node in cluster, return
    # warnings for different instances
    def parse_stats(self, stats):
        stats = json.loads(stats)
        s_list = defaultdict(list)

        for id, node in stats['nodes'].iteritems():
            usage = node['os']

            # Return each node in the format [(Node Name: [CPU %, MEM %]),(...),...]
            s_list[node['name']] = '{0}, {1}'.format(usage['cpu_percent'], usage['mem']['used_percent'])

            # If CPU usage by node is over 95% we're in trouble.
            if usage['cpu_percent'] >= CPU_THRESH:
               print 'WARNING! CPU usage at {0}% for {1}!!!'.format(usage['cpu_usage'], node['name'])

            # If RAM usage by node is 100% that's a problem.
            if usage['mem']['used_percent'] == MEM_THRESH:
                print 'WARNING! RAM usage at {0}% for {1}!!!'.format(usage['used_percent'], node['name'])

            # If Garbage Collection hasn't happened in a while (10 seconds), throw an error.
            for age,info in node['jvm']['gc']['collectors'].iteritems():
                if info['collection_time_in_millis'] >= GC_THRESH:
                    print 'WARNING! JVM Garbage Collection older than 10,000 milliseconds for {0}!!!'.format(node['name'])

            # If the JVM Heap is getting too full, throw a warning.
            if node['jvm']['mem']['heap_used_percent'] >= JVM_MEM_THRESH:
                print 'WARNING! JVM Heap at {0} for {1}!'.format(node['jvm']['mem']['heap_used_percent'], node['name'])

            if node['breakers']['request']['estimated_size_in_bytes'] >= node['breakers']['request']['limit_size_in_bytes']:
                print 'WARNING! Request size on {0} greater than limit! Request: {1}, Limit: {2}'.format(node['name'],
                                                                                                         node['breakers']['request']['estimated_size_in_bytes'],
                                                                                                         node['breakers']['request']['limit_size_in_bytes'])

            else:
                return s_list

    def query(self,param):
        # Connect to cluster
        # Check Health, Nodes, and Stats endpoints
        # if there is a timeout, Alert user and return False.
        try:
            if 'health' in param:
                self.connect = requests.get('{0}/{1}/{2}'.format(ENDPOINT,CLUSTER,param), timeout = TIMEOUT)
            elif 'nodes' in param:
                self.connect = requests.get('{0}/{1}'.format(ENDPOINT,NODES), timeout = TIMEOUT)
            elif 'stats' in param:
                self.connect = requests.get('{0}/{1}/{2}'.format(ENDPOINT,NODES,param), timeout = TIMEOUT)
            return self.connect
        except requests.exceptions.Timeout:
            print requests.exceptions.Timeout
            # return requests.exceptions.Timeout
            return False

    # Display errors if there are issues during
    # initial health stats request.
    def connection_debug(self, payload):
        if 'green' not in payload['status']:
            print 'WARNING! Cluster {0} is at Status {1}. Displaying Health for all Indices.\n'.format(payload['cluster_name'],
                                                                                                     payload['status'])
            print monitor.query('health?level=indices')
        elif payload['number_of_nodes'] > CURRENT_NODES:
            print 'ERROR! Cluster {0} has {1} nodes, we are expecting {2}!!!'.format(payload['cluster_name'],
                                                                                     payload['number_of_nodes'],
                                                                                     CURRENT_NODES)
        elif payload['active_shards'] > MAX_SHARDS:
            print 'WARNING! Cluster {0} has {1} active shards, more than the Max allowed: {2}'.format(payload['cluster_name'],
                                                                                                      payload['active_shards'],
                                                                                                      MAX_SHARDS)

        print 'Cluster Request: {0}. Cluster Health: {1}\n'.format(connection.reason, payload['status'])

if __name__ == "__main__":
    # Init/main
    print '\nElasticSearch Health Monitor Started...'

    monitor = ESMonitor()
    connection = monitor.query('health')
    payload = json.loads(connection._content)

    if connection:
        monitor.connection_debug(payload)

        nodes = monitor.query('nodes')
        n_list = monitor.node_list(nodes._content)
        print [(node,info) for node,info in n_list.iteritems()]

        stats = monitor.query('stats')
        stat_parse = monitor.parse_stats(stats._content)
        print [(stat,info) for stat,info in stat_parse.iteritems()]
    else:
        print 'TIMEOUT'

    # Run until an error or use Ctrl-c out
    while True:
        connection = monitor.query('health')
        if connection:
            print connection.reason

            stat_parse = monitor.parse_stats(stats._content)
            print [(stat,info) for stat,info in stat_parse.iteritems()]

        else:
            print 'ElasticSearch Health Timeout! See logs for cluster system stats history.'
        # Sleep for 1 second and continue looping
        time.sleep(1)

    print 'ElasticSearch Health Monitor Terminated.'
