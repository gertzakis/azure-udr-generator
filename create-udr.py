# Import the needed credential and management objects from the libraries.
from azure.identity import AzureCliCredential
from azure.mgmt.network import NetworkManagementClient
import os


# Acquire a credential object using CLI-based authentication.
credential = AzureCliCredential()

# Retrieve subscription ID from environment variable.
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

print(subscription_id)

# Step 1: Provision a resource group

# Obtain the management object for resources, using the credentials from the CLI login.
# resource_client = ResourceManagementClient(credential, subscription_id)

# Constants we need in multiple places: the resource group name and the region
# in which we provision resources. You can change these values however you want.
RESOURCE_GROUP_NAME = "tzakisg-udr-test"
LOCATION = "West Europe"
# Network and IP address names
VNET_NAME = "tzakisg-vnet-test"
SUBNET_NAME = "tzakisg-subnet-test"

# Obtain the management object for networks
network_client = NetworkManagementClient(credential, subscription_id)

# Provision Route table and wait for completion
poller = network_client.route_tables.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    "tzakisg-route-table-test",
    {"location": LOCATION, "disable_bgp_route_propagation": True},
)

route_table_result = poller.result()

print(f"Provisioned virtual subnet {route_table_result.name}")

poller = network_client.routes_operations.begin_create_or_update(
    RESOURCE_GROUP_NAME, "tzakisg-route-table-test", "default", 
    {"name": "default",
    "address_prefix": "10.10.10./24", 
    "next_hop_type": "VirtualAppliance", 
    "next_hop_ip_address": "10.1.1.1"}
)

route_result = poller.result()

print(f"provisioned{route_result.name}")

url = "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/routeTables/{routeTableName}?api-version=2021-03-01"
