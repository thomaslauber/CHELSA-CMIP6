# CHELSA-CMIP6

This repository contains a jupyter notebook that should facilitate the access and use of the [CHELSA-CMIP6 package](https://doi.org/10.1111/ecog.06535). It allows to check the model combinations that can be used to create bioclimatic variables with the CHELSA-CMIP6 package, as many CMIP6 models do not provide input data for all SPP scenarios. Furthermore, this notebook allows users to run the package in their browser and to generate bioclimatic variables for their region of interest. It is part of the News and Views piece ["Improving access and use of climate projections for ecological research" in Ecography](https://doi.org/10.1111/ecog.07186). The notebook can also be run directly using Deepnote [here](https://deepnote.com/workspace/Tom-Lauber-8823942f-5d9d-4334-a4af-7dca06f14d96/project/CHELSA-CMIP6-c7435d00-916d-4787-8797-c90e1c929bdb/notebook/chelsacmip6-f64dae7722e9453b91a3ae5b4a462124?utm_source=share-modal&utm_medium=product-shared-content&utm_campaign=notebook&utm_content=c7435d00-916d-4787-8797-c90e1c929bdb).

## Background Info

CHELSA-CMIP6 allows users to create relevant bioclimatic variables using a particular combination of climate models and SSP scenarios for a given time period. Downscaling the information from CMIP6 is done through the delta change method, which uses the difference between climate in the current (or another user-defined reference time) and the future time of interest to create a climate anomaly map. This anomaly map is combined with interpolated high-resolution climatologies for the reference period, to downscale future projections. Finally, bioclimatic variables are created using the ANUCLIM methodology.

![Fig 1. - Example](https://nsojournals.onlinelibrary.wiley.com/cms/asset/77e4a13c-e1a4-4d50-afdf-14937ea6285f/ecog12994-fig-0001-m.jpg)
*Example of the delta change method applied on the model MPI-ESM1-2-LR for ssp585, the reference period 1981–2010, and the future period 2041–2070 (from [1]).*


References: 

[1] Karger, D. N., Chauvier, Y., & Zimmermann, N. E. (2023). chelsa‐cmip6 1.0: a python package to create high resolution bioclimatic variables based on CHELSA ver. 2.1 and CMIP6 data. Ecography, e06535.

[2] Paz, A., Lauber, T., Crowther, T. W., & van den Hoogen, J. (2024). Improving access and use of climate projections for ecological research through the use of a new Python tool. Ecography, e07186.

