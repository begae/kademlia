


from random import randrange as dice

k = 20
alpha = 3
kv_pairs = {}

class Bucket:

    prefix = '' # binary string
    triples = []
    size = 0

    def __init__(self, bin_prefix, first_node):
        self.prefix = bin_prefix
        self.triples = [first_node.info]
        self.size = 1

    def coverage(self):
        start = int((self.prefix).ljust('0', 160), 2)
        stop = int((self.prefix).ljust('1', 160), 2)
        return (start, stop)
    
    def is_full(self):
        if self.size < k:
            return False
        
    
    def insert(self, target):
        return



class Node:
    
    ip_addr = '' # binary string
    udp_port = -1 # integer
    node_id = '' # binary string
    table = []

    def __init__(self, ip, port, id, w_id):
        self.ip_addr = ip
        self.udp_port = port
        self.node_id = id
        self.table = [Bucket('', w_id)]

    def where_to_put(self, target):
        distance = int(self.node_id, 2) ^ int(target.node_id, 2)
        for i in range(len(self.table)-1, 1, -1):
            bucket = self.table[i]
            if distance in range(bucket.coverage()):
                if bucket.size < k:
                    return bucket
                elif self.node_id in range(bucket.coverage()):
                    zero, one = self.split_bucket(bucket)
                    if (target.node_id).startswith(zero.prefix):
                        return zero
                    return one
                return None
            return self.table[0]

    def closest_know_of(self, target):
        best_match = self.buckets[0] # top-down
        for bucket in self.buckets:
            if (target.id).startswith(bucket.prefix):
                best_match = bucket
        # if number < k, fill in from others
        return best_match
    
    def find_value_of(self, target, key):
        if kv_pairs[key]:
            return kv_pairs[key]
        return self.closest_know_of(target)
    
    def look_for(self, target, source=None, queried=[]):
        samples = []
        if len(queried) > k:
            return
        if not source:
            source = self.buckets[-1] # nearest first
        if source.contains(target):
            return 
        while len(samples) < alpha: # from here
            rand_node = source[dice(k)]
            while queried.contains(rand_node.id):
                rand_node = source[dice(k)]
            samples.append(rand_node)
            queried.append(rand_node.id)
        for friend in samples:
            f_of_f = friend.closest_know_of(target) # to here : Refreshing
            self.look_for(target, f_of_f, queried)

