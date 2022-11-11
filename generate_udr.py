"""Generate the necessary UDRs and Routes based on the csv data and create the tf templates."""
import argparse
import csv
import sys
from pprint import pprint

from funcy import omit

from generate_tf import generate_config, load_template
from models.data import Route, RouteTable
from tools import log


@log.log()
def read_csv_data(data_file: str) -> dict:
    """Read a CSV file into a dictionary.

    Args:
        data_file (str): filename of the CSV file

    Returns:
        dict: Structured representation (dict of dicts) with Azure networks info
    """
    try:
        with open(data_file, "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")

            # Populate dictionary using headers as keys
            topology_data = {}
            headers = next(csv_reader)[1:]
            for row in csv_reader:
                topology_data[row[0]] = {
                    key: value for key, value in zip(headers, row[1:])
                }
    except IOError:
        print(f"cannot open file {data_file}")
        sys.exit(1)
    return topology_data


@log.log()
def udr_list(topology_data: dict, fw_ip_address: str) -> list:
    """udr_list calculates and returns the UDRs needed for the given data.

    Args:
        topology_data (dict): Dictionary that contains Azure networks info
        fw_ip_address (str): Information about the next-hop IP address

    Returns:
        list: List of RouteTable objects
    """
    udr_data = []
    for key, value in topology_data.items():
        if (value["location"] == "hub" and value["type"] == "subnet") or (
            value["location"] == "spoke"
        ):
            udr_data.append(
                RouteTable(
                    key + "-udr",
                    routes_list(
                        omit(topology_data, [key]), value["location"], fw_ip_address
                    ),
                )
            )

    return udr_data


@log.log()
def routes_list(topology_data: dict, src_location: str, fw_ip_address: str) -> list:
    """routes_list generates a list of routes (Route objects) for specific UDR.

    Args:
        topology_data (dict): Azure networks info
        src_location (str): Location (hub/spoke) of the network at hand
        fw_ip_address (dict): Information about the next-hop IP address

    Returns:
        list: [description]
    """
    route_list = [Route("0.0.0.0_0", "0.0.0.0/0", "VirtualAppliance", fw_ip_address)]

    for dst in topology_data.values():
        if (
            (
                src_location == "hub"
                and dst["location"] == "hub"
                and dst["type"] == "subnet"
            )
            or (
                src_location == "hub"
                and dst["location"] == "spoke"
                and dst["type"] == "vnet"
            )
            or (
                src_location == "spoke"
                and dst["location"] == "hub"
                and dst["type"] == "vnet"
            )
            or (
                src_location == "spoke"
                and dst["location"] == "spoke"
                and dst["type"] == "vnet"
            )
        ):
            route_list.append(
                Route(
                    dst["cidr"].replace("/", "_"),
                    dst["cidr"],
                    "VirtualAppliance",
                    fw_ip_address,
                )
            )

    return route_list


@log.log()
def main():
    """Entrypoint of tool."""
    file_location = args.file
    fw_ip_address = args.gateway
    tf_file = args.tf_file

    topology_data = read_csv_data(file_location)
    udrs = udr_list(topology_data, fw_ip_address)
    template = load_template("templates/tf_route_table.j2")

    for udr in udrs:
        print("===========")
        print(f"UDR: '{udr.name}'")
        print("---------------------------")
        pprint(udr.routes)
        print("===========")

    generate_config(template=template, udrs=udrs, tf_file=tf_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate udr and terraform file to implement them based on csv data"
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=False,
        default="./data.csv",
        help="CSV file with the necessary data (name,location,cidr,type). Default: './data.csv'",
    )
    parser.add_argument(
        "-g",
        "--gateway",
        type=str,
        required=False,
        default="10.10.10.1",
        help="IP address of the default gateway (firewall NVA)",
    )
    parser.add_argument(
        "-tf",
        "--tf_file",
        type=str,
        required=False,
        default="tf_files/routeTables.tf",
        help="Destination file to generate tf config.",
    )

    args = parser.parse_args()
    main()
