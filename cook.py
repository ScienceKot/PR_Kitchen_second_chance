# Importing all needed libraries.
import random
import threading
from cooking_aparatus import CookingAparatus
import time

# Defining the Cook class.
class Cook:
    def __init__(self, kitchen, id : int, cook_settings : dict, menu : list) -> None:
        '''
            The constructor of the cook class.
        :param kitchen: Kitchen
            The object of the Kitchen that the cook is part of.
        :param id: int
            The id of the cook.
        :param cook_settings: dict
            The dictionary with the setting of the cook.
        :param menu: list
            The list with the information about each type of food.
        '''
        self.kitchen = kitchen
        self.id = id
        self.rank = cook_settings['rank']
        self.proficiency = cook_settings["proficiency"]
        self.name = cook_settings["name"]
        self.catch_phrase = cook_settings["catch-phrase"]
        self.cooking_items_counter = 0
        self.food_items_to_prepare = []
        self.menu = menu
        self.order_list_mutex = threading.Lock()

    def working(self):
        '''
            This function is the main working function of the cook.
        '''
        while True:
            # Checking if the cook is available.
            if not self.is_available():
                continue

            # Searching for food item to prepare.
            food_item, apparatus = self.find_food_item()

            time.sleep(random.randint(1, 3))

            if not food_item:
                continue
            else:
                self.cooking_items_counter += 1

            # Creating a Thread for cooking the chosen food.
            threading.Thread(target=self.cooking, args=(food_item, apparatus)).start()

    def find_food_item(self):
        '''
            Searching of a food item to be prepared.
        '''
        self.kitchen.order_list_mutex.acquire()
        self.kitchen.apparatus_mutex.acquire()

        # Getting the food item and the apparatus.
        food_item, apparatus = self.search_order_list()

        # Setting the chosen food item in preparation state.
        if food_item is not None:
            food_item.state = "IN_PREPARATION"

            # Blocking the chosen apparatus.
            if apparatus:
                apparatus.is_available = False

        # Releasing the mutex.
        self.kitchen.apparatus_mutex.release()
        self.kitchen.order_list_mutex.release()

        return food_item, apparatus

    def search_order_list(self):
        '''
            This function find a food item and the apparatus needed to cook it.
        '''
        for _, order in self.kitchen.order_list.queue:
            for food_item in order.food_items:
                # Getting a foot which is not distributed and matches the rank.
                if food_item.state == "NOT_DISTRIBUTED" and self.mathes_rank(food_item):
                    apparatus = None

                    # Getting the apparatus if it exists.
                    if food_item.apparatus:
                        apparatus = self.find_apparatus(food_item.apparatus)

                        if apparatus is None:
                            continue
                    return food_item, apparatus

        return None, None

    def cooking(self, food_item, apparatus):
        '''
            The cooking function.
        :param food_item: Food
            The object representing the food.
        :param apparatus: CookingApparatus
            The object representing the needed cooking apparatus for cooking.
        '''
        # "preparing" the food.
        food_item.cook_id = self.id
        time.sleep(food_item.preparation_time)
        food_item.state = "PREPARED"

        if apparatus:
            apparatus.is_available = True
        self.cooking_items_counter -= 1

    def mathes_rank(self, order_item):
        '''
            This function verifies if the cook's rank matches with the food's complexity.
        :param order_item: Food
            The food object.
        :return:
        '''
        return (self.rank == order_item.complexity) or (self.rank == order_item.complexity + 1)

    def is_available(self):
        '''
            This function return returns the state of the cook.
        '''
        return self.proficiency > self.cooking_items_counter

    def find_apparatus(self, apparatus_type):
        '''
            This function searching for an available apparatus and returns it, if not None is returned.
        :param apparatus_type: str
            The string representing what type of apparatus in needed.
        :return: None or CookingApparatus.
        '''
        for apparatus in self.kitchen.cooking_apparatus[apparatus_type]:
            if apparatus.is_available:
                return apparatus
        return None