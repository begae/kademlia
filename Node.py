
import random

id_space = (0, pow(2, 160))

k = 20 # system-wide replication parameter
alpha = 3 # system-wide concurrency parameter

irregularities = 0 # bucket split exeption counter
expected = 5 # irregularities limit

triple_example = {'addr': 1233445, 'port': 3322, 'nid': 13}
bucket_example = {'prefix': '000...', 'covering': (8, 16), 'triples':[triple_example]}

class Node:

    def __init__(self, addr, port, nid, node_w):
        self.addr = addr
        self.port = port
        self.nid = nid
        self.triple = {'addr': addr, 'port': port, 'nid': nid} # contact information for communication
        self.table = [{'prefix': '', 'covering': id_space, 'triples': []}] # initial routing table
        self.pairs = {} # initial database for key-value pairs
        self.insert(node_w) # triple of a node already in the network
        self.node_lookup(nid)

    def appropriate(self, target_id):
        for bucket in self.table:
            if target_id in range(bucket['covering']): # no overlap in ranges
                return bucket
    
    def closest_k(self, target_id):
        bucket = self.appropriate(target_id)
        nodes = bucket['triples']
        if len(nodes) == k:
            return nodes
        i = self.table.index(bucket)
        upper = self.table[i-1] or bucket
        lower = self.table[i+1] or bucket
        nodes.extend(upper['triples'])
        nodes.extend(lower['triples'])
        sorted = set(nodes).sort(key=lambda x: target_id ^ x['nid'])
        return sorted[:k] or sorted

    def split_bucket(self, bucket):
        return

    def insert(self, new):
        bucket = self.appropriate(new['nid'])
        if new in bucket['triples']:
            bucket['triples'].remove(new) # jump to bottom line
        if len(bucket['triples']) == k:
            head = bucket['triples'][0]['nid']
            if self.ping(head):
                if self.nid not in range(bucket['covering']):
                    if irregularities > expected:
                        return
                    irregularities += 1
                self.split_bucket(bucket)
            return self.insert(new)
        bucket['triples'].append(new)

    def send_find_node(self, recipient, target_id):
        # send rpc, parse k_nodes from response
        return

    def reply_find_node(self, recipient, target_id):
        k_nodes = self.closest_k(target_id)
        # send rpc with k_nodes
        return

    def send_find_value(self, recipient, target_key):
        # send rpc, parse k_nodes or value from response
        return

    def reply_find_value(self, recipient, target_key):
        value = self.pairs[target_key] or self.closest_k(target_key)
        # send rpc with value
        return

    def send_store(self, recipient, pair):
        # send rpc with key-value pair
        return

    def node_lookup(self, target_id, k_nodes=None, queried=[]):
        if not k_nodes: # base case
            k_nodes = self.closest_k(target_id) # k_nodes from self.table
        a_nodes = pick_alpha()
        if not a_nodes: # 0 unseen nodes in k_nodes
            queried.sort(key=lambda x: target_id ^ x['nid']) # sort results by distance
            return queried[:k]
        for node in a_nodes: # parallel, asynchronous RPCs (not for-loop)
            k_nodes = self.send_find_node(node, target_id)
            self.node_lookup(target_id, k_nodes, queried)

        def pick_alpha():
            closer, not_seen, a_nodes = [], [], []
            reached = target_id ^ queried[0]['nid'] # smallest distance obtained
            for node in k_nodes:
                if node not in queried: # if have queried, return empty
                    distance = target_id ^ node['nid']
                    if distance < reached:
                        closer.append(node)
                    not_seen.append(node)
            a_nodes = closer or not_seen
            if len(a_nodes) > alpha:
                a_nodes = random.sample(a_nodes, alpha)
            queried.extend(a_nodes)
            return a_nodes






end = 'end'
