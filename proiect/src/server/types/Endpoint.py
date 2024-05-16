from enum import Enum


class Endpoint(Enum):
    INSERTUSER = "insertUser"
    INSERTPRODUCT = "insertProduct"
    STARTAUCTION = "startAuction"
    GETPRODUCTS = "getProducts"
    BID = "bid"
    AUCTIONSTATUS = "auctionStatus"
