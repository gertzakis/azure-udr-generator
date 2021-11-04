import json, csv
from pprint import pprint


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


def udr_list(topology_data):
    """For every net/subnet in topology calculates the UDRs and return a full list of UDRs needed.
    Returns: a Dictionary with key: udr-name, value:list of dictionaries (routes info).
    """
    udr_diction = {}

    for key, value in topology_data.items():
        udr_data = []
        if value["location"] == "spoke":
            udr_data.append(routes_list(topology_data, key))
            udr_diction[key + "-udr"] = udr_data

        elif value["location"] == "hub" and value["type"] == "subnet":
            udr_data.append(routes_list(topology_data, key))
            udr_diction[key + "-udr"] = udr_data

    return udr_diction


def routes_list(topology_data, network_name):
    """Generated a dictionary of routes for Specific UDR. Every route is a dictionary also.
    key: route-name
    values: dict with route info
    """
    routes = {}
    routes["0.0.0.0_0"] = {
        "dest-subnet": "0.0.0.0/0",
        "next-hop": "virtual-appliance",
    }
    for key, value in topology_data.items():
        if key != network_name:
            if value["location"] == "spoke" and value["type"] != "subnet":
                routes[value["cidr"].replace("/", "_")] = {
                    "dest-subnet": value["cidr"],
                    "next-hop": "virtual-appliance",
                }
            elif value["location"] == "hub" and value["type"] == "subnet":
                routes[value["cidr"].replace("/", "_")] = {
                    "dest-subnet": value["cidr"],
                    "next-hop": "virtual-appliance",
                }
    return routes


def main():
    file_location = "/home/memos/Projects/azure-udr-generator/data.csv"
    topology_data = read_csv_data(file_location)
    udrs = udr_list(topology_data)

    print(type(udrs))
    for k, v in udrs.items():
        print("===============")
        pprint(k)
        print("--------")
        pprint(v)
        print("--------")

if __name__ == "__main__":
    main()
