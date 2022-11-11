"""Route and RouteTable data models."""
from dataclasses import dataclass
from typing import List


@dataclass
class Route:
    """Route model for representing udr routes."""

    name: str
    dest_subnet: str
    next_hop_type: str
    next_hop_ip: str


@dataclass
class RouteTable:
    """RouteTable models for representing UDRs."""

    name: str
    routes: List[Route]
