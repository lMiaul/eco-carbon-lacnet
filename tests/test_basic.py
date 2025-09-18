from decimal import Decimal
from src.ecocarbon.contract import EcoCarbonToken

def test_mint_alignment():
    c=EcoCarbonToken()
    ok,msg=c.mint_carbon_credit("f1", Decimal("11.04"), "b1", "gps", "meth", "Qm", Decimal("1000"), 90)
    assert ok, msg
    assert c.get_balance("f1")==Decimal("11.04")
