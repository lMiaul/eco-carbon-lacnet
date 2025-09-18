import argparse
from decimal import Decimal
from .simulator import EcoCarbonSimulator

def main():
    p=argparse.ArgumentParser(description="Eco-Carbon San Martín CLI (core)")
    p.add_argument("--demo",action="store_true"); p.add_argument("--pilot",type=int,default=0)
    p.add_argument("--no-ui",action="store_true")
    a=p.parse_args()
    sim=EcoCarbonSimulator()
    if a.demo:
        ok,d=sim.process_agricultural_waste("farmer_001", Decimal("5000"), batch_id="demo_batch_001")
        if ok:
            print("✅ Demo minted tokens"); 
            print(f"   Waste: {d['waste_input']:,.0f} kg  Biochar: {d['biochar_output']:.2f} kg  CO2: {d['co2_sequestered']:.3f} t  Tokens: {d['tokens_minted']:.3f}")
        bal=sim.contract.get_balance("farmer_001"); print(f"Balance farmer_001: {bal:.3f} ECOCO2 (~${float(bal)*75:,.2f})")
    if a.pilot>0:
        res=sim.simulate_pilot_program(a.pilot); print(f"✅ Pilot completed: {len(res)} batches")
    if not a.no_ui:
        print("UI not included in CORE. Use the EXTRAS package for notebook UI.")

if __name__=='__main__': main()
