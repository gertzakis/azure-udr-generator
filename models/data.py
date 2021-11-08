from dataclasses import dataclass
from typing import List

@dataclass
class Route:
    name: str
    dest_subnet: str
    next_hop: str

@dataclass
class RouteTable:
    name: str
    routes: List[Route]

