from copy import copy
import time
from connector import ConnectorSterling
# from connector import send_limit

# hardcode the account
ACCOUNT = "DMSTPU0017020" # "ASDF" live, "JKL" demo

ROUTE = 'EDGA'
SIDE = 'B'

def buy_func(con: ConnectorSterling, symbol: str, size: int, price: float) -> None:
    """
    """

    # create a copy of size
    quantity = copy(size)

    # Loop until we have bought the specified amount of shares
    while quantity > 0:
        
        # get latest price here
        # price = latest_price_func()

        # place the order
        ordId, status = con.send_limit(ACCOUNT, symbol, quantity, price, ROUTE, SIDE)

        # wait 5 seconds for the order to fill
        for _ in range(5):
            order_status = con.order_status(ordId)
            print(order_status)
            if order_status == 5: # means order is completely filled
                break
            time.sleep(1)

        # if the order is not filled, cancel the order
        if not con.order_status(ordId) == 5:
            con.cancel_order_id(ACCOUNT, ordId)
            time.sleep(1)
            ordId += 'cancel'
            print('order status after cancel: ', con.order_status(ordId))
            assert con.order_status(ordId) == 8
        else:
            assert con.order_status(ordId) == 5

        # check if there's any trades
        num_trades = con.fill_qty(ordId)
        if num_trades == 0:
            continue

        # print the trade to the console
        print(f"shares bought {num_trades}")

        # modify quantity and if it's greater than 0, repeat loop
        quantity -= num_trades
        
    return

if __name__ == "__main__":

    con = ConnectorSterling(verbose=False)
    
    size = 100

    price = 300

    symbol = 'AAPL'

    # con.send_limit(ACCOUNT, symbol, size, price, ROUTE, SIDE)

    buy_func(con, symbol, size, price)
