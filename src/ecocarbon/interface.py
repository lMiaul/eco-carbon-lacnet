from decimal import Decimal
from IPython.display import display, HTML, clear_output
import ipywidgets as widgets
import pandas as pd
from .simulator import EcoCarbonSimulator

class EcoCarbonInterface:
    def __init__(self):
        self.simulator = EcoCarbonSimulator()
        self.current_user = "admin_address"

    def create_widgets(self):
        display(HTML("<h3>PRELIMINARY PYTHON VERSION</h3><p>Production will be on LAC-Net.</p>"))
        tabs = widgets.Tab()
        tabs.children = [
            self._create_process_tab(),
            self._create_balance_tab(),
            self._create_analysis_tab(),
        ]
        for i, t in enumerate(["Process Waste","View Balances","Analytics"]):
            tabs.set_title(i,t)
        display(tabs)

    def _create_process_tab(self):
        farmer=widgets.Dropdown(options=self.simulator.farmers[:10], description="Farmer:")
        waste=widgets.FloatText(value=1000, description="Waste (kg):")
        btn=widgets.Button(description="Process Waste", button_style="success")
        out=widgets.Output()
        def go(_):
            with out:
                clear_output()
                ok,d=self.simulator.process_agricultural_waste(farmer.value, Decimal(str(waste.value)))
                print("OK" if ok else "ERR", d)
        btn.on_click(go)
        return widgets.VBox([farmer,waste,btn,out])

    def _create_balance_tab(self):
        import pandas as pd
        out=widgets.Output()
        with out:
            if self.simulator.contract.balances:
                df=pd.DataFrame([{"addr":a,"bal":float(b)} for a,b in self.simulator.contract.balances.items()])
                display(df.sort_values("bal",ascending=False).head(5))
        return out

    def _create_analysis_tab(self):
        btn=widgets.Button(description="Run Analytics")
        out=widgets.Output()
        def go(_):
            with out:
                self.simulator.generate_analytics()
        btn.on_click(go)
        return widgets.VBox([btn,out])
