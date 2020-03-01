# import the module
from __future__ import print_function
from aerospike import predicates as p
from aerospike import exception as ex
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

try:
    client.index_integer_create("test", "customers", "phone", "test_customers_phone_idx")
except ex.IndexFoundError:
    pass

def add_customer(customer_id, phone_number, lifetime_value):
    client.put(('test', 'customers', customer_id), {'phone': phone_number, 'ltv': lifetime_value})

def get_ltv_by_id(customer_id):
    try:
        (key, metadata, record) = client.get(('test', 'customers', customer_id))
        return record['ltv']
    except:
        logging.error('Requested non-existent customer ' + str(customer_id))

def get_ltv_by_phone(phone_number):
    try:
        query = client.query('test', 'customers')
        query.select('phone', 'ltv')
        query.where(p.equals('phone', phone_number))
        records = query.results()
        return records[0][2]['ltv']
    except:
        logging.error('Requested non-existent customer ' + str(phone_number))

for i in range(0,1000):
    add_customer(i,i,i + 1)

        
for i in range(0,1000):
    assert (i + 1 == get_ltv_by_id(i)), "No LTV by ID " + str(i)
    assert (i + 1 == get_ltv_by_phone(i)), "No LTV by phone " + str(i)

add_customer(1001,2001,10)
add_customer(2001,3001,20)
assert (10 == get_ltv_by_phone(2001)), "Incorrect LTV for phone 2001"

client.close()
