import datetime, hashlib, random, time
from decimal import Decimal
from typing import Dict, Tuple, List
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from .contract import EcoCarbonToken

random.seed(42); np.random.seed(42)
CO2_PER_KG_BIOCHAR = Decimal("0.01104")  # tCO2eq per kg

class EcoCarbonSimulator:
    def __init__(self):
        self.contract = EcoCarbonToken()
        self.iot_data: List[Dict] = []
        self.processing_history: List[Dict] = []
        self.project_data = {"location":"San Martín, Peru","families":127,"processed_tons":1000,
                             "co2_sequestered":11040,"income_increase":0.35,"carbon_benefit_ratio":54,
                             "deployment":"Preliminary Python (LAC-Net pending)"}
        self.farmers = [f"farmer_{i:03d}" for i in range(1,128)]

    def simulate_iot_reading(self, batch_id:str)->Dict:
        r={"batch_id":batch_id,"timestamp":datetime.datetime.now(),"temperature":random.uniform(450,550),
           "pressure":random.uniform(0.9,1.1),"humidity":random.uniform(5,15),"carbon_content":random.uniform(85,92),
           "ph":random.uniform(8.5,10.5),"quality_score":random.uniform(85,95),
           "gps":f"-6.{random.randint(1000,9999)}, -76.{random.randint(1000,9999)}","source":"Simulated IoT"}
        self.iot_data.append(r); return r

    def process_agricultural_waste(self, farmer_id:str, waste_kg:Decimal, batch_id:str|None=None)->Tuple[bool,Dict]:
        if batch_id is None: batch_id=f"batch_{int(time.time())}_{random.randint(1000,9999)}"
        iot=self.simulate_iot_reading(batch_id)
        biochar_kg=waste_kg*Decimal("0.23")
        co2=biochar_kg*CO2_PER_KG_BIOCHAR
        if iot["quality_score"]<85: return False,{"error":"Quality insufficient"}
        ok,msg=self.contract.mint_carbon_credit(farmer=farmer_id,amount=co2,batch_id=batch_id,gps_location=iot["gps"],
                                                methodology="VCS VM0044",ipfs_hash=f"Qm{hashlib.sha256(batch_id.encode()).hexdigest()[:44]}",
                                                biochar_mass=biochar_kg,quality_score=int(iot["quality_score"]))
        if ok:
            rec={"batch_id":batch_id,"farmer":farmer_id,"waste_input":float(waste_kg),"biochar_output":float(biochar_kg),
                 "co2_sequestered":float(co2),"tokens_minted":float(biochar_kg*self.contract.CONVERSION_RATE/1000),
                 "quality":float(iot["quality_score"]),"timestamp":datetime.datetime.now().isoformat(),
                 "platform":"Python Simulation (LAC-Net pending)"}
            self.processing_history.append(rec); return True, rec
        return False,{"error":msg}

    def simulate_pilot_program(self, num_batches:int=10):
        res=[]; tpb=self.project_data["processed_tons"]/num_batches
        for _ in range(num_batches):
            farmer=random.choice(self.farmers)
            ok,d=self.process_agricultural_waste(farmer, Decimal(tpb*1000))
            if ok: res.append(d)
        return res

    def generate_analytics(self):
        if not self.processing_history:
            print("⚠️ No processing data available for analysis"); return
        df=pd.DataFrame(self.processing_history)
        plt.style.use("seaborn-v0_8-darkgrid")
        import matplotlib.pyplot as plt
        fig,axes=plt.subplots(2,2,figsize=(15,10))
        axes[0,0].hist(df["quality"],bins=20,edgecolor="black"); axes[0,0].axvline(85,linestyle="--")
        axes[0,1].bar(range(len(df)), df["tokens_minted"])
        df["efficiency"]=df["biochar_output"]/df["waste_input"]
        sc=axes[1,0].scatter(df["waste_input"],df["biochar_output"],c=df["quality"],s=100,alpha=0.6)
        plt.colorbar(sc,ax=axes[1,0])
        df["co2_cumulative"]=df["co2_sequestered"].cumsum()
        axes[1,1].plot(df["co2_cumulative"],marker="o",linewidth=2,markersize=8)
        plt.tight_layout(); plt.show()
