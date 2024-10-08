from typing import List
from datetime import datetime


class Node:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class BusinessGroup(Node):
    def __init__(self, id: str, name: str, revenue: float = None, time_stamp: str = str(datetime.date(datetime.now()))):
        super().__init__(id, name)
        self.revenue = revenue
        self.time_stamp = time_stamp


class ProductFamily(Node):
    def __init__(self, id: str, name: str, business_group_id: str, time_stamp: str = str(datetime.date(datetime.now()))):
        super().__init__(id, name)
        self.business_group_id = business_group_id  # Foreign Key
        self.time_stamp = time_stamp


class ProductOffering(Node):
    def __init__(self, id, name, product_family_id, inventory: int = None, demand: int = None, time_stamp: str = str(datetime.date(datetime.now()))):
        super().__init__(id, name)
        self.inventory = inventory
        self.demand = demand
        self.product_family_id = product_family_id  # Foreign Key
        self.time_stamp = time_stamp

    def print_details(self):
        print(f"Product Offering ID: {self.id}\nProduct Offering Name: {self.name}\nProduct Family ID: {self.product_family_id}\nInventory: {self.inventory}\nDemand: {self.demand}\nTime Stamp: {self.time_stamp}\n")


class Modules(Node):
    def __init__(self, id, name, product_offering_id: List, inventory: int = None, importance: int = None, time_stamp: str = str(datetime.date(datetime.now()))):
        super().__init__(id, name)
        self.inventory = inventory
        self.importance = importance
        self.product_offering_id = product_offering_id  # Foreign Key
        self.time_stamp = time_stamp

    def print_details(self):
        print(f"Module ID: {self.id}\nModule Name: {self.name}\nProduct Offering ID: {self.product_offering_id}\nInventory: {self.inventory}\nImportance: {self.importance}\nTime Stamp: {self.time_stamp}\n")


class Parts(Node):
    def __init__(self, id, name, module_id: List, inventory: int = None, importance: int = None, production_cost: float = None, part_type: str = "Purchase", level: int = 1, time_stamp: str = str(datetime.date(datetime.now()))):
        super().__init__(id, name)
        self.inventory = inventory
        self.importance = importance
        self.production_cost = production_cost
        self.part_type = part_type
        self.level = level  # 1
        self.module_id = module_id  # Foreign Key
        self.time_stamp = time_stamp
