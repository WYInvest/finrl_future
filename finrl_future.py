
def _buy_future(self, index, action):
    def _do_buy():
        if (self.state[index + 2 * self.stock_dim + 1] != True):  # check if the stock is able to buy
            # if self.state[index + 1] >0:
            # Buy only if the price is > 0 (no missing data in this particular date)
            # available_amount = self.state[0] // (
            #         self.state[index + 1] * (1 + self.buy_cost_pct[index]))
            # when buying stocks, we should consider the cost of trading when calculating available_amount, or we may be have cash<0
            # print('available_amount:{}'.format(available_amount))

            if self.state[index + self.stock_dim + 1] < 0:
                cover_shares = 0 - self.state[index + self.stock_dim + 1]
                cover_amount = cover_shares * self.state[index + 1]
                self.state[0] += cover_amount
                available_amount = self.state[0] // (
                        self.state[index + 1] * (1 + self.buy_cost_pct[index]))
                buy_num_shares = min(available_amount, abs(self.state[index + self.stock_dim + 1]) + action)
                buy_amount = (
                        self.state[index + 1]
                        * buy_num_shares
                        * (1 + self.buy_cost_pct[index])
                )
                self.state[0] -= buy_amount

                self.state[index + self.stock_dim + 1] += buy_num_shares

                self.cost += (
                        self.state[index + 1] * buy_num_shares * self.buy_cost_pct[index]
                )
                self.trades += 1

            else:
                if action > self.state[index + self.stock_dim + 1]:
                    available_amount = self.state[0] // (
                            self.state[index + 1] * (1 + self.buy_cost_pct[index]))
                    buy_num_shares = min(available_amount, action - self.state[index + self.stock_dim + 1])
                    buy_amount = (
                            self.state[index + 1]
                            * buy_num_shares
                            * (1 + self.buy_cost_pct[index])
                    )
                    self.state[0] -= buy_amount
                    self.state[index + self.stock_dim + 1] += buy_num_shares
                    self.cost += (
                            self.state[index + 1] * buy_num_shares * self.buy_cost_pct[index]
                    )
                    self.trades += 1
                elif action < self.state[index + self.stock_dim + 1]:
                    buy_num_shares = action - self.state[index + self.stock_dim + 1]
                    sell_shares = self.state[index + self.stock_dim + 1] - action
                    sell_amount = sell_shares * self.state[index + 1]
                    self.state[0] += sell_amount
                    self.state[index + self.stock_dim + 1] += buy_num_shares
                    self.trades += 1
                else:
                    buy_num_shares = 0

        else:
            buy_num_shares = 0

        return buy_num_shares

    # perform buy action based on the sign of the action
    if self.turbulence_threshold is None:
        buy_num_shares = _do_buy()
    else:
        if self.turbulence < self.turbulence_threshold:
            buy_num_shares = _do_buy()
        else:
            buy_num_shares = 0
            pass

    return buy_num_shares

def _short_future(self, index, action):
    def _do_short():
        if (self.state[index + 2 * self.stock_dim + 1] != True):  # check if the stock is able to buy
            # if self.state[index + 1] >0:
            # Buy only if the price is > 0 (no missing data in this particular date)
            # available_amount = self.state[0] // (
            #         self.state[index + 1] * (1 + self.buy_cost_pct[index]))
            # when buying stocks, we should consider the cost of trading when calculating available_amount, or we may be have cash<0
            # print('available_amount:{}'.format(available_amount))

            if self.state[index + self.stock_dim + 1] > 0:
                sell_shares = self.state[index + self.stock_dim + 1]
                sell_amount = sell_shares * self.state[index + 1]
                self.state[0] += sell_amount
                available_amount = self.state[0] // (
                        self.state[index + 1] * (1 + self.sell_cost_pct[index]))
                short_num_shares = min(available_amount, self.state[index + self.stock_dim + 1] + abs(action))
                short_amount = (
                        self.state[index + 1]
                        * short_num_shares
                        * (1 - self.sell_cost_pct[index])
                )
                self.state[0] += short_amount

                self.state[index + self.stock_dim + 1] -= short_num_shares

                self.cost += (
                        self.state[index + 1] * short_num_shares * self.sell_cost_pct[index]
                )
                self.trades += 1

            else:
                if action < self.state[index + self.stock_dim + 1]:
                    available_amount = self.state[0] // (
                            self.state[index + 1] * (1 + self.buy_cost_pct[index]))
                    short_num_shares = min(available_amount, self.state[index + self.stock_dim + 1] - action)
                    short_amount = (
                            self.state[index + 1]
                            * short_num_shares
                            * (1 - self.sell_cost_pct[index])
                    )
                    self.state[0] += short_amount
                    self.state[index + self.stock_dim + 1] -= short_num_shares
                    self.cost += (
                            self.state[index + 1] * short_num_shares * self.sell_cost_pct[index]
                    )
                    self.trades += 1
                elif action > self.state[index + self.stock_dim + 1]:
                    short_num_shares = self.state[index + self.stock_dim + 1] - action
                    cover_shares = action - self.state[index + self.stock_dim + 1]
                    cover_amount = cover_shares * self.state[index + 1]
                    self.state[0] += cover_amount
                    self.state[index + self.stock_dim + 1] -= short_num_shares
                    self.trades += 1
                else:
                    short_num_shares = 0

        else:
            short_num_shares = 0

        return short_num_shares

    # perform buy action based on the sign of the action
    if self.turbulence_threshold is None:
        short_num_shares = _do_short()
    else:
        if self.turbulence < self.turbulence_threshold:
            short_num_shares = _do_short()
        else:
            short_num_shares = 0
            pass
    return short_num_shares