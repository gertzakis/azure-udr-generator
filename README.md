# Azure UDR Generator

Generating UDRs for Azure vNets & subnets in order to pass the traffic from Hub vNet NetworkVirtualAppliance (firewall) in a Hub & Spoke topology.

The Network Topology should be inserted into CSV file (default: data.csv), with fields: "name,location,cidr,type"

generate_udr.py prints and generates the UDRs that should be implemented in Azure.

* UDRs for every Hub subnet with routes to other Hub-subnets and Spoke-vNets.
* UDRs for every Spoke-vNet, with routes pointing to other vNets (no intersubnet routing inside the Spokes).
* generates terraform file with RouteTables (UDRs) in tf_files dir, in order to be implemented in an IaC solution.

create_udr.py will also do the necessary changes on the Azure subscription. still **work in progress** because python azure-sdk documentation is too convoluted. 


## Usage examples
Only with gateway IP, it will use data.csv and routeTables.tf file:

`python3 generate_udr.py -g <GATEWAY_IP>`


With csv & tf files specified:

`python3 generate_udr.py -g <GATEWAY_IP> -f <CSV_FILE>`

`python3 generate_udr.py -g <GATEWAY_IP> -f <CSV_FILE> -tf <TERRAFORM_FILE>`  
