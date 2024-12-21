import json
from typing import Optional

from cryptography.hazmat.primitives.asymmetric import rsa

from src.daad.clients.Kalshi.Requests import KalshiRequests


class KalshiExchange(KalshiRequests):
    def __init__(
        self,
        exchange_api_base: str,
        key_id: str,
        private_key: rsa.RSAPrivateKey,
        cache_session: str,
    ):

        super().__init__(
            exchange_api_base,
            key_id,
            private_key,
            cache_session,
        )
        self.key_id = key_id
        self.private_key = private_key
        self.exchange_url = "/exchange"
        self.markets_url = "/markets"
        self.events_url = "/events"
        self.series_url = "/series"
        self.portfolio_url = "/portfolio"
        self.warm_up_cache()

    def warm_up_cache(self):
        """Warming up the cache with a lightweight, cached call."""
        try:
            self.get_exchange_status()  # Replace with a lightweight cached API call
            print("Cache warmed up")
        except Exception as e:
            print(f"Cache warm-up failed: {e}")

    # def logout(self,):
    #     result = self.post("/logout")
    #     return result

    def get_exchange_status(
        self,
    ):
        result = self.get(self.exchange_url + "/status")
        return result

    # market endpoints!

    def get_markets(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        event_ticker: Optional[str] = None,
        series_ticker: Optional[str] = None,
        max_close_ts: Optional[int] = None,
        min_close_ts: Optional[int] = None,
        status: Optional[str] = None,
        tickers: Optional[str] = None,
    ):
        query_string = self.query_generation(params={k: v for k, v in locals().items()})
        dictr = self.get(self.markets_url + query_string)
        return dictr

    def get_market_url(self, ticker: str):
        return self.markets_url + "/" + ticker

    def get_market(self, ticker: str):
        market_url = self.get_market_url(ticker=ticker)
        dictr = self.get(market_url)
        return dictr

    def get_event(self, event_ticker: str):
        dictr = self.get(self.events_url + "/" + event_ticker)
        return dictr

    def get_events(
        self,
        limit: Optional[int] = None,  # default 100, up to 200
        cursor: Optional[str] = None,
        status: Optional[
            str
        ] = None,  # accepted strings: unopened, open, closed, settled
        series_ticker: Optional[str] = None,
        with_nested_markets: Optional[bool] = None,
    ):
        query_string = self.query_generation(params={k: v for k, v in locals().items()})
        dictr = self.get(self.events_url + query_string)
        return dictr

    def get_series(self, series_ticker: str):
        dictr = self.get(self.series_url + "/" + series_ticker)
        return dictr

    def get_market_history(
        self,
        ticker: str,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        max_ts: Optional[int] = None,
        min_ts: Optional[int] = None,
    ):
        relevant_params = {k: v for k, v in locals().items() if k != "ticker"}
        query_string = self.query_generation(params=relevant_params)
        market_url = self.get_market_url(ticker=ticker)
        dictr = self.get(market_url + "/history" + query_string)
        return dictr

    def get_orderbook(
        self,
        ticker: str,
        depth: Optional[int] = None,
    ):
        relevant_params = {k: v for k, v in locals().items() if k != "ticker"}
        query_string = self.query_generation(params=relevant_params)
        market_url = self.get_market_url(ticker=ticker)
        dictr = self.get(market_url + "/orderbook" + query_string)
        return dictr

    def get_trades(
        self,
        ticker: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        max_ts: Optional[int] = None,
        min_ts: Optional[int] = None,
    ):
        query_string = self.query_generation(params={k: v for k, v in locals().items()})
        if ticker != None:
            if len(query_string):
                query_string += "&"
            else:
                query_string += "?"
            query_string += "ticker=" + str(ticker)

        trades_url = self.markets_url + "/trades"
        dictr = self.get(trades_url + query_string)
        return dictr

    # portfolio endpoints!

    def get_balance(
        self,
    ):
        dictr = self.get(self.portfolio_url + "/balance")
        return dictr

    def create_order(
        self,
        ticker: str,
        client_order_id: str,
        side: str,
        action: str,
        count: int,
        type: str,
        yes_price: Optional[int] = None,
        no_price: Optional[int] = None,
        expiration_ts: Optional[int] = None,
        sell_position_floor: Optional[int] = None,
        buy_max_cost: Optional[int] = None,
    ):

        relevant_params = {
            k: v for k, v in locals().items() if k != "self" and v != None
        }

        print(relevant_params)
        order_json = json.dumps(relevant_params)
        orders_url = self.portfolio_url + "/orders"
        result = self.post(path=orders_url, body=order_json)
        return result

    def batch_create_orders(self, orders: list):
        orders_json = json.dumps({"orders": orders})
        batched_orders_url = self.portfolio_url + "/orders/batched"
        result = self.post(path=batched_orders_url, body=orders_json)
        return result

    def decrease_order(
        self,
        order_id: str,
        reduce_by: int,
    ):
        order_url = self.portfolio_url + "/orders/" + order_id
        decrease_json = json.dumps({"reduce_by": reduce_by})
        result = self.post(path=order_url + "/decrease", body=decrease_json)
        return result

    def cancel_order(self, order_id: str):
        order_url = self.portfolio_url + "/orders/" + order_id
        result = self.delete(path=order_url + "/cancel")
        return result

    def batch_cancel_orders(self, order_ids: list):
        order_ids_json = json.dumps({"ids": order_ids})
        batched_orders_url = self.portfolio_url + "/orders/batched"
        result = self.delete(path=batched_orders_url, body=order_ids_json)
        return result

    def get_fills(
        self,
        ticker: Optional[str] = None,
        order_id: Optional[str] = None,
        min_ts: Optional[int] = None,
        max_ts: Optional[int] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ):

        fills_url = self.portfolio_url + "/fills"
        query_string = self.query_generation(params={k: v for k, v in locals().items()})
        dictr = self.get(fills_url + query_string)
        return dictr

    def get_orders(
        self,
        ticker: Optional[str] = None,
        event_ticker: Optional[str] = None,
        min_ts: Optional[int] = None,
        max_ts: Optional[int] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ):
        orders_url = self.portfolio_url + "/orders"
        query_string = self.query_generation(params={k: v for k, v in locals().items()})
        dictr = self.get(orders_url + query_string)
        return dictr

    def get_order(self, order_id: str):
        orders_url = self.portfolio_url + "/orders"
        dictr = self.get(orders_url + "/" + order_id)
        return dictr

    def get_positions(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        settlement_status: Optional[str] = None,
        ticker: Optional[str] = None,
        event_ticker: Optional[str] = None,
    ):
        positions_url = self.portfolio_url + "/positions"
        query_string = self.query_generation(params={k: v for k, v in locals().items()})
        dictr = self.get(positions_url + query_string)
        return dictr

    def get_portfolio_settlements(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ):

        positions_url = self.portfolio_url + "/settlements"
        query_string = self.query_generation(params={k: v for k, v in locals().items()})
        dictr = self.get(positions_url + query_string)
        return dictr
