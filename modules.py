import pandas as pd
import xarray as xr 
import rioxarray as rio 
import glob
import os 
import folium
import geopandas as gpd
from shapely.geometry import Polygon
from chelsa_cmip6.GetClim import chelsa_cmip6

def check_requirements(scenarios):
    query = dict(
    activity_id='ScenarioMIP',
    experiment_id=scenarios,
    table_id='Amon',
    variable_id=['pr','tas','tasmax','tasmin']
    )
    catalog = pd.read_csv("https://cmip6.storage.googleapis.com/pangeo-cmip6.csv")
    query_string = ' and '.join(f"{k} in {v}" if isinstance(v, list) else f"{k} == '{v}'" for k, v in query.items())
    query_result = catalog.query(query_string)
    # Check that all variables are there 
    df_vars = query_result.groupby(['activity_id','institution_id','source_id','experiment_id','member_id'])['variable_id'].count()
    df_vars = df_vars[df_vars == 4].reset_index()
    # Check that all scenarios are there 
    df_scen = df_vars.groupby(['activity_id','institution_id','source_id','member_id'])['experiment_id'].count()
    df_scen = df_scen[df_scen == len(scenarios)].reset_index()
    df = df_scen
    # Count the number of members 
    df_nrMem = df_scen.groupby(['activity_id','institution_id','source_id'])['member_id'].count()
    # Reduce the members into one field
    df_mem = df_scen.groupby(['activity_id','institution_id','source_id'])['member_id'].apply(list)
    # Combine 
    df = df_scen[['institution_id','source_id']].drop_duplicates().reset_index(drop=True).rename(columns={"source_id": "model"})
    df['members'] = df_mem.reset_index()['member_id']
    df['nr of members'] = df_nrMem.reset_index()['member_id']
    df = df.set_index('institution_id')
    return df

def plotRegion(region):
    xmin,xmax,ymin,ymax = region[0], region[1], region[2], region[3]
    x_y_list = [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]
    polygon_geom = Polygon(x_y_list)
    polygon = gpd.GeoDataFrame(index=[0], crs='epsg:4326', geometry=[polygon_geom])
    bounds = polygon.total_bounds.tolist()
    m = folium.Map(tiles='cartodbpositron')
    m.fit_bounds([bounds[:2][::-1], bounds[2:][::-1]])
    folium.GeoJson(polygon).add_to(m)
    folium.LatLngPopup().add_to(m)
    return m

def run_chelsa_cmip6(model_members, scenarios, region, fefp, refp = ('1981-01-15', '2010-12-15'), output_folder = 'output'):
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    df = check_requirements(scenarios)
    xmin, xmax, ymin, ymax = region[0], region[1], region[2], region[3]
    for scenario in scenarios:
        for model_member in model_members:
            source_id = model_member[0]
            member_id = model_member[1]
            institution_id = df[df['model'] == source_id].index[0]
            for period in fefp:
                fefps = period[0]
                fefpe = period[1]
                # Generate the bioclimatic variables 
                chelsa_cmip6(
                    activity_id='ScenarioMIP',
                    table_id='Amon',
                    experiment_id=scenario, 
                    institution_id=institution_id, 
                    source_id=source_id, 
                    member_id=member_id, 
                    refps=refp[0], 
                    refpe=refp[1], 
                    fefps=fefps,
                    fefpe=fefpe, 
                    xmin=xmin, 
                    xmax=xmax,
                    ymin=ymin, 
                    ymax=ymax,
                    output=output_folder + '/') 

def ncToTif(output_folder):
    files = glob.glob('./' + output_folder + '/*.nc')
    filesToExclude = [f for f in files if any(var in f for var in ['pr','tas','tasmin','tasmax'])]
    filesToKeep = sorted(list(set(files) - set(filesToExclude)))
    for f in filesToKeep:
        raster = xr.open_dataset(f, engine='netcdf4')
        raster = raster.rio.set_spatial_dims(x_dim='lon', y_dim='lat')
        raster.rio.write_crs("epsg:4326", inplace=True)
        raster.rio.to_raster(f.rsplit('.', 1)[0] + '.tif', driver = 'GTiff')
        os.remove(f)


    # import pandas as pd 
# !pip install esgf-pyclient
# from pyesgf.search import SearchConnection
# conn = SearchConnection('https://esgf-data.dkrz.de/esg-search', distrib=False)
# # ctx = conn.new_context(
# #     activity_id=activity_id,
# #     table_id='Amon',
# #     # source_id='MPI-ESM1-2-LR',
# #     experiment_id=experiment_id,
# #     # member_id='r1i1p1f1',
# #     variable='pr,tas,tasmax,tasmin',
# #     # to_timestamp="2100-01-01T00:00:00Z"
# #     )
# ctx = conn.new_context(
#     activity_id=activity_id,
#     table_id='Amon',
#     experiment_id=experiment_id,
#     source_id='GFDL-ESM4'
#     )
# result = ctx.search()
# ids = [i.dataset_id for i in list(result)]

# data = {
#     'project': [id_.split('.')[0] for id_ in ids],
#     'activity_id': [id_.split('.')[1] for id_ in ids],
#     'institution_id': [id_.split('.')[2] for id_ in ids],
#     'source_id': [id_.split('.')[3] for id_ in ids],
#     'experiment_id': [id_.split('.')[4] for id_ in ids],
#     'member_id': [id_.split('.')[5] for id_ in ids],
#     'table_id': [id_.split('.')[6] for id_ in ids],
#     'variable': [id_.split('.')[7] for id_ in ids]
# }

# df = pd.DataFrame(data)
# df.sort_values(by = list(pd.DataFrame(data).columns)).reset_index(drop=True)
# df

# # dat = df.groupby(by = ['institution_id','source_id','experiment_id','member_id','table_id'])['variable'].count().reset_index()
# # dat[dat['variable'] >= 4].drop(columns = 'variable')