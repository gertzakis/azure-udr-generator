# Azure UDR Generator

Generating UDRs for vNets & subnets in order to pass the traffic from Hub vNet NetworkVirtualAppliance (firewall) in a Hub & Spoke Azure topology.

The Network Topology should be inserted into data.csv

generate_udr.py generates and prints the UDRs that should be implemented in Azure.

* UDRs for every Hub subnet with routes to other Hub-subnets and Spoke-vNets.
* UDRs for every Spoke-vNet, with routes pointing to other vNets (no intersubnet routing inside the Spokes)

create_udr.py will also do the necessary changes on the Azure subscription. still work in progress because python azure-sdk documentation is too convoluted. 

generate_tf.py generates terraform file with RouteTables (UDRs) in tf_files dir, in order to be implemented in an IaC solution. 


## Usage examples
Only with gateway IP, it will use data.csv and routeTables.tf file:

`python3 generate_udr.py -g <GATEWAY_IP>`


With csv & tf specified:

`python3 generate_udr.py -g <GATEWAY_IP> -f <CSV_FILE>`

`python3 generate_udr.py -g <GATEWAY_IP> -f <CSV_FILE> -tf <TERRAFORM_FILE>`  