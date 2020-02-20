# import the module
from __future__ import print_function
import logging
import aerospike

# Configure the client
config = {
  'hosts': [ ('127.0.0.1', 3000) ]
}

# Create a client and connect it to the cluster
try:
  client = aerospike.client(config).connect()
except:
  import sys
  print("failed to connect to the cluster with", config['hosts'])
  sys.exit(1)

def add_customer(customer_id, phone_number, lifetime_value):
    client.put(('test', 'customers', customer_id), {'phone': phone_number, 'ltv': lifetime_value})
    client.put(('test', 'customers', phone_number), {'id': customer_id, 'ltv': lifetime_value})

def get_ltv_by_id(customer_id):
    try:
        (key, metadata, record) = client.get(('test', 'customers', customer_id))
        return record['ltv']
    except:
        logging.error('Requested non-existent customer ' + str(customer_id))

def get_ltv_by_phone(phone_number):
    try:
        (key, metadata, record) = client.get(('test', 'customers', phone_number))
        return record['ltv']
    except:
        logging.error('Requested non-existent customer ' + str(phone_number))

for i in range(0,1000):
    add_customer(i,i,i + 1)

for i in range(0,1000):
    assert (i + 1 == get_ltv_by_id(i)), "No LTV by ID " + str(i)
    assert (i + 1 == get_ltv_by_phone(i)), "No LTV by phone " + str(i)
