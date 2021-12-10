# Importing all needed libraries.
from food import Food
import time

class Order:
    def __init__(self, order_dict : dict, menu : list) -> None:
        '''
            The constructor of the order class.
        :param order_dict: dict
            The dictionary with the order information.
        :param menu: list
            The list with all menu items.
        '''
        self.order_id = order_dict['order_id']
        self.table_id = order_dict['table_id']
        self.waiter_id = order_dict['waiter_id']
        self.items = order_dict['items']
        self.items_processed = [False for _ in range(len(self.items))]
        self.priority = order_dict['priority']
        self.max_wait = order_dict['max_wait']
        self.pick_up_time = order_dict['pick_up_time']
        self.received_time = int(time.time())
        self.prepared_time = None
        self.cooking_time = None
        self.food_items = [Food(order_id=self.order_id, food_id=item_id, menu=menu) for item_id in self.items]
        self.is_delivered = False

    def is_finished(self) -> bool:
        '''
            This function returns True if the order is finished and False vice versa.
        :return: bool
            The finished status of the order.
        '''
        for item in self.food_items:
            if item.state != "PREPARED":
                return False
        return True

    def __lt__(self, other):
        '''
            This function is used for comparison 2 orders in the priority queue.
        :param other: Order
            other order.
        :return: bool
            True if the priority of first order is lower than the priority of the second order.
        '''
        self_priority = (self.priority, self.order_id)
        other_priority = (other.priority, other.order_id)
        return self_priority < other_priority