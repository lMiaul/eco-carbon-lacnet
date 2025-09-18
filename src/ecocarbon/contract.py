from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
import datetime
from typing import Dict, List, Optional, Tuple

class Role(Enum):
    ADMIN="ADMIN"; MINTER="MINTER"; VERIFIER="VERIFIER"; FARMER="FARMER"; BUYER="BUYER"; RETIREMENT="RETIREMENT"

@dataclass
class TokenEconomics:
    carbon_sequestered: Decimal
    biochar_mass: Decimal
    quality_multiplier: int
    permanence_score: int
    origin_gps: str
    methodology: str
    timestamp: datetime.datetime
    batch_id: str
    ipfs_hash: str
    is_retired: bool

@dataclass
class FeeStructure:
    minting_fee:int=200; transfer_fee:int=50; cross_border_fee:int=100
    compliance_fee: Decimal = Decimal("50")
    retirement_fee: Decimal = Decimal("25")

class EcoCarbonToken:
    NAME="Eco-Carbon San Martin"; SYMBOL="ECOCO2"; DECIMALS=3
    CONVERSION_RATE=Decimal("11.04")  # tCO2eq per tonne biochar

    def __init__(self):
        self.token_batches: Dict[str, TokenEconomics] = {}
        self.balances: Dict[str, Decimal] = {}
        self.farmer_rewards: Dict[str, Decimal] = {}
        self.fees = FeeStructure()
        self.total_carbon_sequestered=Decimal("0"); self.total_retired=Decimal("0"); self.total_supply=Decimal("0")
        self.roles: Dict[str, List[Role]] = {}; self.owner="admin_address"
        for r in (Role.ADMIN, Role.MINTER, Role.VERIFIER, Role.RETIREMENT):
            self._grant_role(self.owner, r)
        self.events=[]

    def _grant_role(self, address:str, role:Role):
        self.roles.setdefault(address, [])
        if role not in self.roles[address]: self.roles[address].append(role)
    def grant_role(self, address:str, role:Role): self._grant_role(address, role)
    def _has_role(self, address:str, role:Role)->bool: return role in self.roles.get(address, [])

    def _emit_event(self, et:str, data:dict):
        self.events.append({"type":et,"timestamp":datetime.datetime.now(),"data":data,"note":"simulated"})

    def mint_carbon_credit(self, farmer:str, amount:Decimal, batch_id:str, gps_location:str,
                           methodology:str, ipfs_hash:str, biochar_mass:Decimal, quality_score:int,
                           minter_address:Optional[str]=None) -> Tuple[bool,str]:
        if minter_address is None: minter_address=self.owner
        if not self._has_role(minter_address, Role.MINTER): return False,"❌ Error: MINTER role required"
        if amount<=0 or biochar_mass<=0: return False,"❌ Error: Invalid amounts"
        if quality_score<85: return False,"❌ Error: Quality score must be >= 85%"
        if batch_id in self.token_batches: return False,"❌ Error: Batch ID already exists"

        te = TokenEconomics(amount,biochar_mass,150 if quality_score>90 else 100,100,gps_location,
                            methodology,datetime.datetime.now(),batch_id,ipfs_hash,False)
        tokens_to_mint = (biochar_mass*self.CONVERSION_RATE)/Decimal("1000")
        self.token_batches[batch_id]=te
        self.balances[farmer]=self.balances.get(farmer,Decimal("0"))+tokens_to_mint
        self.total_carbon_sequestered+=amount; self.total_supply+=tokens_to_mint
        self._emit_event("TokenMinted",{"batch_id":batch_id,"farmer":farmer,"amount":float(tokens_to_mint)})
        return True, f"✅ Minted {tokens_to_mint:.3f} {self.SYMBOL} for {farmer}"

    def distribute_token_revenue(self, total_revenue:Decimal):
        if total_revenue<=0: return False,{}
        d={"farmers":total_revenue*Decimal("0.60"),"technology":total_revenue*Decimal("0.20"),
           "verification":total_revenue*Decimal("0.10"),"insurance":total_revenue*Decimal("0.10")}
        self._emit_event("RevenueDistributed",{"total":float(total_revenue),"distribution":{k:float(v) for k,v in d.items()}})
        return True,d

    def retire_credits(self, batch_id:str, amount:Decimal, reason:str, retirement_address:Optional[str]=None)->Tuple[bool,str]:
        if retirement_address is None: retirement_address=self.owner
        if not self._has_role(retirement_address, Role.RETIREMENT): return False,"❌ Error: RETIREMENT role required"
        if batch_id not in self.token_batches: return False,"❌ Error: Invalid batch ID"
        if self.token_batches[batch_id].is_retired: return False,"❌ Error: Credits already retired"
        if self.balances.get(retirement_address,Decimal("0"))<amount: return False,"❌ Error: Insufficient balance"
        self.balances[retirement_address]-=amount; self.total_supply-=amount; self.total_retired+=amount
        self.token_batches[batch_id].is_retired=True
        self._emit_event("TokenRetired",{"batch_id":batch_id,"retirer":retirement_address,"amount":float(amount),"reason":reason})
        return True, f"✅ Retired {amount:.3f} {self.SYMBOL} - Reason: {reason}"

    def get_balance(self,address:str)->Decimal: return self.balances.get(address,Decimal("0"))
    def get_batch_info(self,batch_id:str): return self.token_batches.get(batch_id)
