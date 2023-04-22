import sys
import datetime as dt
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from datetime import *
from typing import Optional
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(['http://localhost:9200'])
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Could not connect to Elasticsearch")

class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")

    price: float = Field(description="The price of the Trade.")

    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")

    counterparty: Optional[str] = Field(default=None, description="The counterparty the trade was executed with. May not always be available")

    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")

    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")

    trade_date_time: dt.datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")

    trade_details: TradeDetails = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")

    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")

    trader: str = Field(description="The name of the Trader")
    

app=FastAPI()


@app.post('/letstrade/')
async def update_Json_File(trade: Trade):
    es = Elasticsearch(['http://localhost:9200'])
    es.index(index='trades', body=trade.dict())
    return trade


@app.get("/all-trades")
async def all_trades():
    result = es.search(index='trades', body={'query': {'match_all': {}}})
    trades = [hit['_source'] for hit in result['hits']['hits']]
    return trades



es = Elasticsearch(["http://localhost:9200"])

@app.get("/find-trade-by-unique-id/{trade_id}")
async def fetch_Particular_Trade(trade_id: str):
    query = {
        "query": {
            "match": {
                "trade_id": trade_id
            }
        }
    }
    res = es.search(index="trades", body=query)

    if not res["hits"]["hits"]:
        return {"error": "Trade not found"}

    trade = res["hits"]["hits"][0]["_source"]
    return trade



@app.get("/search-trades-common/{search}")
async def search_trades(search: str):
    query = {
        'query': {
            'bool': {
                'should': [
                    {'match': {'counterparty': search}},
                    {'match': {'instrument_id': search}},
                    {'match': {'instrument_name': search}},
                    {'match': {'trader': search}}
                ]
            }
        }
    }
    result = es.search(index='trades', body=query)
    data1 = [hit['_source'] for hit in result['hits']['hits']]
    return data1