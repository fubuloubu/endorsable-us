class Account():
    def use_intention(amt: num): pass
    def receive_intention(amt: num): pass

owner: address
fee: wei_value

for_sale: {amt: num, price: wei_value}[address]

def __init__(_fee: wei_value):
    self.fee = _fee
    self.owner = msg.sender

# So owner can operate the exchange
def change_fee(_fee: wei_value):
    assert self.owner == msg.sender
    self.fee = _fee

def use_intention(amt: num):
    pass # No need to do anything here, exchange has no intentions

def sell_intention(amt: num, wallet: address, price: wei_value):
    Account(msg.sender).use_intention(amt)
    amt += self.for_sale[wallet].amt # Add to existing
    self.for_sale[wallet] = {amt: amt, price: price}

@payable
def buy_intention(_from: address):
    amt = (msg.value - self.fee) / self.for_sale[_from].price
    assert amt <= self.for_sale[_from].amt
    Account(msg.sender).receive_intention(amt)
    send(self.owner, self.fee)
    send(_from, amt)
    send(msg.sender, msg.value - amt - self.fee)
