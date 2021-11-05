# Azure UDR Generator

Generating UDRs for vNets & subnets in order to pass the traffic from Hub vNet NetworkVirtualAppliance (firewall) in a Hub & Spoke Azure topology.

The Network Topology should be inserted into data.csv

generate-udr.py generates and prints the UDRs that should be implemented in Azure.

* UDRs for every Hub subnet with routes to other Hub-subnets and Spoke-vNets.
* UDRs for every Spoke-vNet, with routes pointing to other vNets (no intersubnet routing inside the Spokes)

create-udr.py will also do the necessary changes on the Azure subscription. still work in progress because python azure-sdk documentation is too convoluted. 

Still don't know if i go with python-sdk or fallback to the good old http request


