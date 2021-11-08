import csv
from pprint import pprint
from models.data import RouteTable, Route
from funcy import omit


def read_csv_data(data_file: str) -> dict:
    """read_csv_data reads a CSV file into a dictionary

    Args:
        data_file (str): filename of the CSV file

    Returns:
        dict: Structured representation (dict of dicts) with Azure networks info
    """
    try:
        with open(data_file, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            
            # Populate dictionary using headers as keys
            topology_data = {}
            headers = next(csv_reader)[1:]
            for row in csv_reader:
                topology_data[row[0]] = {key: value for key, value in zip(headers, row[1:])}
    except IOError:
        print("cannot open file")
    return topology_data


def udr_list(topology_data: dict) -> list:
    """udr_list calculates and returns the UDRs needed for the given data

    Args:
        topology_data (dict): Dictionary that contains Azure networks info

    Returns:
        list: List of RouteTable objects
    """
    udr_data = []

    for key, value in topology_data.items():
        if (
            (value["location"] == "hub" and value["type"] == "subnet") or \
            (value["location"] == "spoke")
        ):
            udr_data.append(
                RouteTable(
                    key + "-udr",
                    routes_list(omit(topology_data, [key]), value["location"]),
                )
            )

    return udr_data


def routes_list(topology_data: dict, src_location: str) -> list:
    """routes_list generates a list of routes (Route objects) for specific UDR.

    Args:
        topology_data (dict): Azure networks info
        network_name (str): Name of the network that the UDR will attach to
        network_info (dict): Information about the network at hand

    Returns:
        list: [description]
    """

    route_list = [Route("0.0.0.0_0", "0.0.0.0/0", "VirtualAppliance")]

    for dst in topology_data.values():
        if (
            (src_location == "hub" and dst["location"] == "hub" and dst["type"] == "subnet") or\
            (src_location == "hub" and dst["location"] == "spoke" and dst["type"] == "vnet") or\
            (src_location == "spoke" and dst["location"] == "hub" and dst["type"] == "vnet") or\
            (src_location == "spoke" and dst["location"] == "spoke" and dst["type"] == "vnet")
        ):
            route_list.append(
                Route(
                    dst["cidr"].replace("/", "_"),
                    dst["cidr"],
                    "VirtualAppliance",
                )
            )

    return route_list


def main():
    file_location = "./data.csv"
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
