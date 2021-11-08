import csv
from pprint import pprint
from models.data import RouteTable, Route


def read_csv_data(data_file):
    """Reading CSV file and retuning dictionary of dicts with azure networks info."""
    try:
        with open(data_file, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            next(csv_reader)  # skipping csv header from data
            topology_data = {}
            for row in csv_reader:
                topology_data[row[0]] = {
                    "location": row[1],
                    "cidr": row[2],
                    "type": row[3],
                }
    except IOError:
        print("cannot open file")
    return topology_data


def udr_list(topology_data, fw_ip_address):
    """For every net/subnet in topology calculates the UDRs and return a full list of UDRs needed.
    Returns: a List with RouteTable objects.
    """
    udr_data = []

    for key, value in topology_data.items():
        if not (value["location"] == "hub" and value["type"] == "vnet"):
            udr_data.append(
                RouteTable(key + "-udr", routes_list(topology_data, key, value, fw_ip_address))
            )
        elif value["location"] == "spoke":
            udr_data.append(
                RouteTable(key + "-udr", routes_list(topology_data, key, value, fw_ip_address))
            )
        elif value["location"] == "hub" and value["type"] == "subnet":
            udr_data.append(
                RouteTable(key + "-udr", routes_list(topology_data, key, value, fw_ip_address))
            )

    return udr_data


def routes_list(topology_data, network_name, network_info, fw_ip_address):
    """Generated a list of routes for Specific UDR. Every route is a Route object."""
    route_list = []
    route = Route("0.0.0.0_0", "0.0.0.0/0", "VirtualAppliance", fw_ip_address)
    route_list.append(route)

    for key, value in topology_data.items():
        if key != network_name:
            if network_info["location"] == "hub":
                if value["location"] == "hub" and value["type"] == "subnet":
                    route_list.append(
                        Route(
                            value["cidr"].replace("/", "_"),
                            value["cidr"],
                            "VirtualAppliance",
                            fw_ip_address
                        )
                    )
                elif value["location"] == "spoke" and value["type"] == "vnet":
                    route_list.append(
                        Route(
                            value["cidr"].replace("/", "_"),
                            value["cidr"],
                            "VirtualAppliance",
                            fw_ip_address
                        )
                    )
            else:
                if value["location"] == "hub" and value["type"] == "vnet":
                    route_list.append(
                        Route(
                            value["cidr"].replace("/", "_"),
                            value["cidr"],
                            "VirtualAppliance",
                            fw_ip_address
                        )
                    )
                elif value["location"] == "spoke" and value["type"] == "vnet":
                    route_list.append(
                        Route(
                            value["cidr"].replace("/", "_"),
                            value["cidr"],
                            "VirtualAppliance",
                            fw_ip_address
                        )
                    )

    return route_list


def main():
    file_location = "/home/memos/Projects/azure-udr-generator/data.csv"
    fw_ip_address = "10.1.1.1"
    topology_data = read_csv_data(file_location)
    udrs = udr_list(topology_data, fw_ip_address)

    for udr in udrs:
        print("===========")
        print(f"UDR: '{udr.name}'")
        print("---------------------------")
        pprint(udr.routes)
        print("===========")


if __name__ == "__main__":
    main()
