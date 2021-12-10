class Food:
    def __init__(self, order_id : int, food_id : int, menu : list) -> None:
        '''
            The constructor of the Food class.
        :param order_id: int
            The id of the order from which this food is part of.
        :param food_id: int
            The id of the food.
        :param menu: list
            The list with all menu items.
        '''
        self.order_id = order_id
        self.food_id = food_id
        self.estimated_prep_time = None
        self.preparation_time = menu[food_id-1]['preparation-time']
        self.state = "NOT_DISTRIBUTED"
        self.apparatus = menu[food_id-1]["cooking-apparatus"]
        self.complexity = menu[food_id-1]["complexity"]
        self.cook_id = None