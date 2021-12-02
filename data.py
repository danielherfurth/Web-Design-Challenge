# %%
# region
import pandas as pd
import matplotlib.pyplot
import seaborn as sns
import plotly.graph_objects as go

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
# endregion


geography_df = pd.read_csv(
    r'data/ddf--entities--geo--country.csv',
    index_col='country'
)[['name', 'world_4region']]

poverty_df = pd.read_csv(
    r'data/ddf--datapoints--poverty_less_than_320.csv'
).groupby('geo').agg('max')

mortality_df = pd.read_csv(
    r'data/ddf--datapoints--sp_dyn_imrt_in-infant_mortality.csv'
).groupby('economy').agg('max')

life_expec_df = pd.read_csv(
    r'data/ddf--datapoints--sp_dyn_le00_in--by--geo--time_life_exp.csv'
).groupby('geo').agg('max').reset_index()

pov_mort_df = mortality_df.merge(
    poverty_df[['poverty_320']],
    how='left',
    left_index=True,
    right_index=True
).rename_axis('country')

merged = pov_mort_df.merge(geography_df, left_index=True, right_index=True)

gdp_df = pd.read_csv(
    r'data/ddf--datapoints--ny_gdp_pcap_pp_cd--by--geo--time_gdp_per.csv'
).groupby('geo').agg('max')

hdi_df = pd.read_csv(r'data/hdi_by_country.csv', index_col='country')

gini_df = pd.read_csv(r'data/gini.csv', index_col='geo').groupby('geo').agg('max')

gini_hdi_df = gini_df[['gini']].merge(
    geography_df[['name']],
    how='outer',
    left_index=True,
    right_index=True
).join(
    hdi_df[['hdi']],
    how='left',
    on='name'
).reset_index()

gini_hdi_df = gini_hdi_df.rename(columns={'index': 'country'})

gini_hdi_df = gini_hdi_df.join(
    gdp_df[['gdp_per_cap']],
    on='country'
).join(
    merged[['infant_mortality', 'poverty_320', 'world_4region']],
    on='country'
)

print(gini_hdi_df.head())
# gini_hdi_df = gini_hdi_df.reindex(columns=['country', 'name', 'gini', 'hdi', 'gdp_per_cap'])
