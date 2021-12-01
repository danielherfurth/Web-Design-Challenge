# %%
import pandas as pd
import matplotlib.pyplot
import seaborn as sns
import plotly.graph_objects as go

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

geography_df = pd.read_csv(
    r'data/ddf--entities--geo--country.csv',
    index_col='country'
)[['name', 'world_4region']]

mortality_df = pd.read_csv(
    r'data/ddf--datapoints--sp_dyn_imrt_in--by--economy--year.csv'
).groupby('economy').agg('max')

poverty_df = pd.read_csv(
    r'data/ddf--datapoints--si_pov_nahc--by--economy--year.csv'
).groupby('economy').agg('max')

pov_mort_df = mortality_df['sp_dyn_imrt_in'].merge(
    poverty_df, on='economy'
).reset_index()

cols = 'economy infant_mortality year poverty_rate'.split()

pov_mort_df.columns = cols

merged = pov_mort_df.merge(geography_df, left_on='economy', right_on='country')
merged_cols = 'year name economy world_4region infant_mortality poverty_rate'.split()

merged = merged.reindex(columns=merged_cols)
merged.columns = ['year', 'country', 'abbrev', 'region', 'infant_mortality', 'poverty_rate']

life_expec_df = pd.read_csv(
    r'data/ddf--datapoints--sp_dyn_le00_in--by--geo--time.csv'
).groupby('geo').agg('max').reset_index()



merged = merged.set_index('abbrev').join(
    life_expec_df.set_index('geo')['life_exp']
).reset_index()


gdp_df = pd.read_csv(
    r'data/ddf--datapoints--ny_gdp_pcap_pp_cd--by--geo--time.csv'
).groupby('geo').agg('max')

merged = merged.set_index('abbrev').join(
    gdp_df['gdp_per_cap']
).reset_index()

merged.head()

#%%
hdi_df = pd.read_csv(r'data/hdi_by_country.csv', index_col='country')

merged = merged.set_index('country').join(
    hdi_df['hdi']
).reset_index()

#%%
gini_df = pd.read_csv(r'data/gini.csv', index_col='geo').groupby('geo').agg('max')
gini_df = gini_df.join(
    geography_df[['name','world_4region']]
).sort_index()

gini_hdi = hdi_df.merge(gini_df)

life_expec_df[['geo','life_exp']].set_index('geo').join(gini_df,lsuffix='_',how='inner')