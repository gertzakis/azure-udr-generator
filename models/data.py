from dataclasses import dataclass

@dataclass
class RouteTable:
    name: str
    routes: list

@dataclass
class Route:
    name: str
    dest_subnet: str
    next_hop: str

