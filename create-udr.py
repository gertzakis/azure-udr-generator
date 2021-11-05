# Import the needed credential and management objects from the libraries.
from azure.identity import AzureCliCredential
from azure.mgmt.network import NetworkManagementClient
from generate_udr import read_csv_data, udr_list
import os

# Acquire a credential object using CLI-based authentication.
credential = AzureCliCredential()

# Retrieve subscription ID from environment variable.
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
print(f"Using subscription '{subscription_id}'")

RESOURCE_GROUP_NAME = "tzakisg-udr-test"
LOCATION = "West Europe"
FW_IP_ADDRESS = "10.1.1.1"
FILE_LOCATION = "/home/memos/Projects/azure-udr-generator/data.csv"
topology_data = read_csv_data(FILE_LOCATION)
udrs = udr_list(topology_data)

# Obtain the management object for networks
network_client = NetworkManagementClient(credential, subscription_id)


def create_route_tables(udr_name):
    route_table = network_client.route_tables.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        udr_name,
        {"location": LOCATION, "disable_bgp_route_propagation": True},
    ).result()

    return route_table


def create_route(udr_name, route_name, route_info):
    route = network_client.routes.begin_create_or_update(
        RESOURCE_GROUP_NAME,
        udr_name,
        route_name,
        {
            "address_prefix": route_info["dest-subnet"],
            "next_hop_type": "VirtualAppliance",
            "next_hop_ip_address": FW_IP_ADDRESS,
        },
    ).result()

    return route


for udr in udrs.keys():
    # Provision Route table and wait for completion
    route_table = create_route_tables(udr)
    print(f"Provisioned Route Table: {route_table.name}")

for udr_routes in udrs.values():
    # Iterate through all routes of table
    for routes in udr_routes:
        for key, value in routes.items():
            # Provision Routes and wait for completion
            route = create_route(udr, key, value)
            print(f"Provisioned route '{route.name}' on route table '{udr_routes}'")

