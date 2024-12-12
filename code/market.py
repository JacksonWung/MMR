class Market:
    def __init__(self, initial_money):
        self.player_money = initial_money
        self.player_stocks = 0

    def buy_stock(self, price, quantity):
        """
        根据价格和购买数量执行买入操作。
        """
        total_cost = price * quantity
        if self.player_money >= total_cost:
            self.player_money -= total_cost
            self.player_stocks += quantity
            return True
        return False

    def sell_stock(self, price, quantity):
        """
        根据价格和出售数量执行卖出操作。
        """
        if self.player_stocks >= quantity:
            self.player_stocks -= quantity
            self.player_money += price * quantity
            return True
        return False
