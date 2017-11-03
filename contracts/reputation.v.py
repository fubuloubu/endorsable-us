# Earn reputation based on positive transactions
# Burn reputation to earn intention (temporary "gas")
# Intentions fuel transactions that can add to reputation
# You can transfer your intention to someone who needs it
# You can pay someone money to ask them to burn their reputation
# and give you their intention (they might choose to do this for
# economic circumstances e.g. they have more than they need, need
# money for whatever reason, leaving the system, "retirement", etc.)
class Account():
    def use_intention(amt: num): pass

reputation: num
intention: num
competencies: num[bytes20]
top_10: bytes20[10]
last_converted: timestamp

owner: address
wallet: address

def __init__(_wallet: address):
    self.owner = msg.sender
    self.wallet = _wallet

def burn_reputation(amt: num):
    assert self.reputation >= amt
    self.reputation -= amt
    self.intention += amt

def use_intention(amt: num):
    assert msg.sender == self.owner
    self.intention -= amt

def receive_intention(amt: num):
    assert msg.sender != self.owner
    Account(msg.sender).use_intention(amt)
    self.intention += amt

# Add up to 5 compentencies from the endorsement
# It costs an amount of intention equal to the sum of the current comptency scores
# to increase the comptency score by 1 (increased difficulty)
# Add endorsement_hash to be able to prove that endorsement contained comptencies
def add_endorsement(endorsement_hash: bytes32, _competencies: bytes20[5]):
    assert msg.sender != self.owner
    amt: num = 0
    for i in range(0, 5):
        if _competencies[i] != None:
            amt += self.competencies[_compentencies[i]]
    Account(msg.sender).use_intention(amt)
    # Do this loop twice to prevent re-entrancy
    amt = 0
    for i in range(0, 5):
        for i in range(0, 5):
            
        if _competencies[i] != None:
            self.competencies[_compentencies[i]] += 1
            amt += self.competencies[_compentencies[i]]
    self.repution += amt

def convert_competency():
    # Can only do this about once a day
    assert block.timestamp + 5760 > self.last_converted
    self.last_converted = block.timestamp
    for competency in top_10:
        self.reputation += self.competencies[competency]
