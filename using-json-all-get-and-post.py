import sys
import datetime as dt
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from datetime import *
from typing import Optional
import json

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


with open('banga.json') as file:
    jsonfile = json.load(file)
with open('banga.json') as file:
    data = json.load(file)

@app.post('/letstrade/')
async def update_Json_File(trade: Trade):
    jsonfile.append(trade)
    return jsonfile

@app.get("/all-trades")
async def all_trades():
      return jsonfile

@app.get("/find-trade-by-unique-id/{trade_id}")
async def fetch_Particular_Trade(trade_id: str):

    for trade in jsonfile:
        if trade["trade_id"] == trade_id:
            return trade
    return {"message": "Trade not found"}

@app.get("/search-trades-common/{search}")
async def search_trades(search: str):
    findthenadd=[]

    for letsfindit in jsonfile:
        if letsfindit["counterparty"]==search:
            findthenadd.append(letsfindit)
        elif letsfindit["instrument_id"]==search:
            findthenadd.append(letsfindit)
        elif letsfindit["instrument_name"]==search:
            findthenadd.append(letsfindit)
        elif letsfindit["trader"]==search:
            findthenadd.append(letsfindit)
    return findthenadd


@app.get("/sorting-the-data")
async def sorting_the_data(price_or_quantity: str = None, asc_or_desc: str = None):
    if price_or_quantity == "price":
        jsonfile.sort(key=lambda x: x['trade_details']['price'])
    elif price_or_quantity == "quantity":
        jsonfile.sort(key=lambda x: x['trade_details']['quantity'])

    if asc_or_desc == "descending":
        jsonfile.reverse()

    return jsonfile



@app.get("/filter-according-to-price-date-type")
async def filter_according_to_price_date_type(*, assetClass: Optional[str] = None, end: Optional[dt.datetime] = "3000-12-31T23:59:59", maxPrice: Optional[int] = sys.maxsize, minPrice: Optional[int] = -sys.maxsize - 1, start: Optional[dt.datetime] = "1900-12-31T23:59:59", tradeType: Optional[str] = None):
    data2 = [t for t in jsonfile
            if ((assetClass is None) or (t.get("asset_class") == assetClass))
            and ((tradeType is None) or (t["trade_details"].get("buySellIndicator") == tradeType))
            and (int(t["trade_date_time"].replace('-', '').replace(':', '').replace('T', '')) >= int(start.replace('-', '').replace(':', '').replace('T', '')))
            and (int(t["trade_date_time"].replace('-', '').replace(':', '').replace('T', '')) <= int(end.replace('-', '').replace(':', '').replace('T', '')))
            and (t["trade_details"]["price"] <= maxPrice)
            and (t["trade_details"]["price"] >= minPrice)]
    return data2
