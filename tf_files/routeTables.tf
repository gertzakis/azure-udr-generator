
resource "azurerm_route_table" "makissubnet-udr" {
  name                          = "makissubnet-udr"
  location                      = "europe"
  resource_group_name           = "my-rg"
  disable_bgp_route_propagation = false
  route {
    name           = "0.0.0.0_0"
    address_prefix = "0.0.0.0/0"
    next_hop_type  = "VirtualAppliance"
    next_hop_in_ip_address = "10.0.1.4"
  }
  route {
    name           = "10.0.2.0_24"
    address_prefix = "10.0.2.0/24"
    next_hop_type  = "VirtualAppliance"
    next_hop_in_ip_address = "10.0.1.4"
  }
  route {
    name           = "10.1.0.0_16"
    address_prefix = "10.1.0.0/16"
    next_hop_type  = "VirtualAppliance"
    next_hop_in_ip_address = "10.0.1.4"
  }
  route {
    name           = "10.2.0.0_16"
    address_prefix = "10.2.0.0/16"
    next_hop_type  = "VirtualAppliance"
    next_hop_in_ip_address = "10.0.1.4"
  }
}
resource "azurerm_route_table" "makissubnet02-udr" {
  name                          = "makissubnet02-udr"
  location                      = "europe"
  resource_group_name           = "my-rg"
  disable_bgp_route_propagation = false
  route {
    name           = "0.0.0.0_0"
    address_prefix = "0.0.0.0/0"
    next_hop_type  = "VirtualAppliance"
    next_hop_in_ip_address = "10.0.1.4"
  }
  route {
    name           = "10.0.1.0_24"
    address_prefix = "10.0.1.0/24"
    next_hop_type  = "VirtualAppliance"
    next_hop_in_ip_address = "10.0.1.4"
  }
  route {
    name           = "10.1.0.0_16"
    address_prefix = "10.1.0.0/16"
    next_hop_type  = "VirtualAppliance"
    next_hop_in_ip_address = "10.0.1.4"
  }
  route {
    name           = "10.2.0.0_16"
    address_prefix = "10.2.0.0/16"
    next_hop_type  = "VirtualAppliance"
    next_hop_in_ip_address = "10.0.1.4"
  }
}
resource "azurerm_route_table" "tzakisvnet-udr" {
  name                          = "tzakisvnet-udr"
  location                      = "europe"
  resource_group_name           = "my-rg"
  disable_bgp_route_propagation = false
  route {
    name           = "0.0.0.0_0"
    address_prefix = "0.0.0.0/0"
    next_hop_type  = "VirtualAppliance"
    next_hop_in_ip_address = "10.0.1.4"
  }
  route {
    name           = "10.0.0.0_16"
    address_prefix = "10.0.0.0/16"
    next_hop_type  = "VirtualAppliance"
    next_hop_in_ip_address = "10.0.1.4"
  }
  route {
    name           = "10.2.0.0_16"
    address_prefix = "10.2.0.0/16"
    next_hop_type  = "VirtualAppliance"
    next_hop_in_ip_address = "10.0.1.4"
  }
}
resource "azurerm_route_table" "tzakisvnet02-udr" {
  name                          = "tzakisvnet02-udr"
  location                      = "europe"
  resource_group_name           = "my-rg"
  disable_bgp_route_propagation = false
  route {
    name           = "0.0.0.0_0"
    address_prefix = "0.0.0.0/0"
    next_hop_type  = "VirtualAppliance"
    next_hop_in_ip_address = "10.0.1.4"
  }
  route {
    name           = "10.0.0.0_16"
    address_prefix = "10.0.0.0/16"
    next_hop_type  = "VirtualAppliance"
    next_hop_in_ip_address = "10.0.1.4"
  }
  route {
    name           = "10.1.0.0_16"
    address_prefix = "10.1.0.0/16"
    next_hop_type  = "VirtualAppliance"
    next_hop_in_ip_address = "10.0.1.4"
  }
}
