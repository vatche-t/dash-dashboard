import pandas as pd
import numpy as np
import plotly.io as pio
from functions import functions as func


pd.options.plotting.backend = "plotly"
pio.templates.default = "plotly_dark"

digi_df = func.get_digi_data()

digi_list = digi_df["report_name"].unique()
digi_list = np.sort(digi_list)

digi_list = pd.DataFrame(digi_list, columns=["report_name"])
digi_list = func.add_report_long_names(digi_list)
digi_list.sort_values(by=["report_long_name"], inplace=True)

#dropdown
digi_list_abbrev = dict(zip(digi_list["report_name"], digi_list["report_long_name"]))


if __name__ == "__main__":
    print("logic")
