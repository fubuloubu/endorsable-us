"""
Intention (NTNT) is a Burnable/Mintable ERC-20 Token.
The Burning and Minting functions are only available
for the connected application contract(s) as a means
of collecting toll
"""

# Standard ERC20 variables
totalSupply: num256
balances: address -> num256
allowed: address -> address -> num256
# Standard ERC20 logs
Transfer: log(from: address, to: address, value: num256)
Approval: log(owner: address, spender: address, value: num256)

# Burnable logs
Mint: log(minter: address, value: num256)

# Mintable logs
Burn: log(burner: address, value: num256)

# Custom
applications: queue(address)
maintainer: address

def __init__(initalSupply: num256):
    self.totalSupply = initialSupply
    self.maintainer = msg.sender

# Token Details (for exchanges)
def decimals() -> num:
    return 0

def name() -> bytes <= 16:
    return b"Intention Token"

def symbol() -> bytes <= 4:
    return b"NTNT"

# ERC20 Methods
@constant
def balanceOf(_owner: address) -> num256:
    return self.balances[_owner]

def transfer(_to: address, _value: num256) -> bool:
    assert _to != 0x0
    assert self.balances[msg.sender] >= _value
    self.balances[msg.sender] -= _value
    self.balances[_to] += _value
    log.Transfer(msg.sender, _to, _value)
    return True

@constant
def allowance(_owner: address, _spender: address) -> num256:
    return self.allowed[_owner][_spender]

def approve(_spender: address, _value: num256) -> bool:
    self.allowed[_spender][msg.sender] = _value
    log.Approval(msg.sender, _spender, _value)

def transferFrom(_from: address, _to: address, _value: num256) -> bool:
    assert _to != 0x0
    assert self.balances[_from] >= _value
    assert self.allowance(_from, msg.sender) >= _value
    self.balances[_from] -= _value
    self.balances[_to] += _value
    log.Transfer(_from, _to, _value)
    return True

# Burnable Token (Locked to usage contract)
def burn(burner: address, value: num256) -> bool:
    assert msg.sender in self.applications
    assert self.balances[burner] >= value
    self.balances[burner] -= value
    self.totalSupply -= value
    log.Burn(burner, value)
    return True

# Mintable Token (Locked to usage contract)
def mint(minter: address, value: num256) -> bool:
    assert msg.sender in self.applications
    assert self.totalSupply + value >= self.totalSupply
    self.balances[minter] += value
    self.totalSupply += value
    log.Mint(minter, value)
    return True

# Application management functions
# Only allowed by maintainer address
# Eventually managed via token governance
def updateMaintainer(newMaintainer: address):
    assert msg.sender == maintainer
    self.maintainer = newMaintainer

def addApplication(newApplication: address):
    assert msg.sender == maintainer
    self.applications.push(newApplication)

def delApplication(oldApplication: address):
    assert msg.sender == maintainer
    self.applications.pop(oldApplication)
