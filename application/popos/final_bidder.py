from sqlalchemy import func
from application.models.bid import Bid

# when we get the end of bidding time from FE we will run this function to determine the highest_bid
# will query the highest_bid to determine the owner
# return the bidders name email and bid amount in a json response back to the FE

def final_bidder():
    highest_bid = Bid.query(func.max(Bid.amount)).scalar()
    bidder = Bid.query.filter(Bid.amount == highest_bid).first()
    return bidder
