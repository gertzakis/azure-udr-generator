from pprint import pprint
from azure.identity import AzureCliCredential
from azure.mgmt.network import NetworkManagementClient
from generate_udr import read_csv_data, udr_list
import os

# Retrieve subscription ID from environment variable.
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
print(f"Using subscription '{subscription_id}'")

# CONSTANTS
###########
RESOURCE_GROUP_NAME = "tzakisg-udr-test"
LOCATION = "West Europe"
FW_IP_ADDRESS = "10.1.1.1"
FILE_LOCATION = "/home/memos/Projects/azure-udr-generator/data.csv"
###########
# CONSTANTS

topology_data = read_csv_data(FILE_LOCATION)
udrs = udr_list(topology_data, FW_IP_ADDRESS)

# Acquire a credential object using CLI-based authentication.
credential = AzureCliCredential()

# Obtain the management object for networks
network_client = NetworkManagementClient(credential, subscription_id)

def create_route_tables(udr):
    """Creates Route Table"""
    result = network_client.route_tables.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        udr.name,
        {"location": LOCATION, "disable_bgp_route_propagation": True},
    ).result()

    return result


def create_route(udr_name, route):
    """Create Route on a specific UDR"""
    result = network_client.routes.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        udr_name,
        route.name,
        {
            "address_prefix": route.dest_subnet,
            "next_hop_type": route.next_hop_type,
            "next_hop_ip_address": route.next_hop_ip,
        },
    ).result()

    return result


for udr in udrs:
    # Provision Route table and wait for completion
    route_table_result = create_route_tables(udr)
    print(f"Provisioned Route Table: {route_table_result.name}")
    
for udr in udrs:
    # Iterate through all routes of table    
    for route in udr.routes:
        # Provision route and wait for completion
        route_result = create_route(udr.name, route)
        print(f"Provisioned route '{route_result.name}' on route table '{udr.name}'")

