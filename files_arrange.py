#Last edit: 15/05/2024
#Author: Diego Pereiro, edits Patricia Navarro Gonzalez
#Description: this code aggreagtes NETCDF ROMS files for the desired time 
#period using coordinates, u, v, mask, time, and angle

from netCDF4 import Dataset, num2date
from datetime import datetime
import os
import glob

def agregar_netcdfs(filelist, name):
    ''' Agregagates the NETCDF files in "filelist" in a unique file "name" '''
       
    # Read coordinates of the first item in the list
    with Dataset(filelist[0], 'r') as nc:
        lonp = nc.variables['lon_rho'][:]; Mp, Lp = lonp.shape
        latp = nc.variables['lat_rho'][:]
        lonu = nc.variables['lon_u'][:];   Mu, Lu = lonu.shape
        latu = nc.variables['lat_u'][:]
        lonv = nc.variables['lon_v'][:];   Mv, Lv = lonv.shape
        latv = nc.variables['lat_v'][:]
        maskp = nc.variables['mask_rho'][:]
        masku = nc.variables['mask_u'][:]
        maskv = nc.variables['mask_v'][:]
        angle = nc.variables['angle'][:]                                       # NUEVO !!!!!!!
        
    # Create file NetCDF
    if os.path.isfile(name):
        os.remove(name)
    with Dataset(name, 'w') as nc:
        
        ''' Create dimensions '''
        nc.createDimension('ocean_time', 0)
        nc.createDimension('eta_rho', Mp)
        nc.createDimension('xi_rho', Lp)
        nc.createDimension('eta_u', Mu)
        nc.createDimension('xi_u', Lu)
        nc.createDimension('eta_v', Mv)
        nc.createDimension('xi_v', Lv)
        
        
        ''' Longitude '''
        lon_rho = nc.createVariable('lon_rho', 'f8', dimensions=('eta_rho', 'xi_rho'))
        lon_rho.long_name = 'longitude of RHO-points'
        lon_rho.units = 'degree_east' 
        lon_rho[:] = lonp
        
        ''' Latitude '''
        lat_rho = nc.createVariable('lat_rho', 'f8', dimensions=('eta_rho', 'xi_rho'))
        lat_rho.long_name = 'latitude of RHO-points'
        lat_rho.units = 'degree_north'        
        lat_rho[:] = latp
        
        ''' Longitude '''
        lon_u = nc.createVariable('lon_u', 'f8', dimensions=('eta_u', 'xi_u'))
        lon_u.long_name = 'longitude of U-points'
        lon_u.units = 'degree_east'       
        lon_u[:] = lonu
        
        ''' Latitude '''
        lat_u = nc.createVariable('lat_u', 'f8', dimensions=('eta_u', 'xi_u'))
        lat_u.long_name = 'latitude of U-points'
        lat_u.units = 'degree_north'      
        lat_u[:] = latu
        
        ''' Longitude '''
        lon_v = nc.createVariable('lon_v', 'f8', dimensions=('eta_v', 'xi_v'))
        lon_v.long_name = 'longitude of V-points'
        lon_v.units = 'degree_east'       
        lon_v[:] = lonv
        
        ''' Latitude '''
        lat_v = nc.createVariable('lat_v', 'f8', dimensions=('eta_v', 'xi_v'))
        lat_v.long_name = 'latitude of V-points'
        lat_v.units = 'degree_north'    
        lat_v[:] = latv
        
        ''' Angle '''
        anglevar = nc.createVariable('angle', 'f8', dimensions=('eta_rho', 'xi_rho'))   # NUEVO !!!
        anglevar.long_name = 'angle between XI-axis and EAST'                           # NUEVO !!!
        anglevar.units = 'radians'                                                      # NUEVO !!!
        anglevar[:] = angle                                                             # NUEVO !!!
        
        ''' Land/Sea Masks ''' 
        mask_rho = nc.createVariable('mask_rho', 'f8', dimensions=('eta_rho', 'xi_rho'))
        mask_rho.long_name = 'mask on RHO-points'
        mask_rho.flag_values = [0, 1]
        mask_rho.flag_meanings = 'land water'
        mask_rho[:] = maskp
        
        mask_u = nc.createVariable('mask_u', 'f8', dimensions=('eta_u', 'xi_u'))
        mask_u.long_name = 'mask on U-points'
        mask_u.flag_values = [0, 1]
        mask_u.flag_meanings = 'land water'
        mask_u[:] = masku
        
        mask_v = nc.createVariable('mask_v', 'f8', dimensions=('eta_v', 'xi_v'))
        mask_v.long_name = 'mask on V-points'
        mask_v.flag_values = [0, 1]
        mask_v.flag_meanings = 'land water'
        mask_v[:] = maskv        
        
        
        ''' Time '''
        timevar = nc.createVariable('ocean_time', 'f8', dimensions=('ocean_time'))
        timevar.long_name = 'time since initialization'
        timevar.units = 'seconds since 1968-05-23'
        
        ''' u '''
        uvar = nc.createVariable('u', 'f4', dimensions=('ocean_time', 'eta_u', 'xi_u'))
        uvar.long_name = 'u-momentum component'
        uvar.units = 'meter second-1'
        
        ''' v '''
        vvar = nc.createVariable('v', 'f4', dimensions=('ocean_time', 'eta_v', 'xi_v'))
        vvar.long_name = 'v-momentum component'
        vvar.units = 'meter second-1'
        
        ''' MAIN LOOP '''
        for i, f in enumerate(filelist):
            with Dataset(f, 'r') as ROMS:
                time = ROMS.variables['ocean_time']
                ocean_time = time[:]
                time = num2date(time[:], time.units)[0]
                time_i = datetime(time.year, time.month, time.day, time.hour).strftime('%Y-%b-%d %H:%M')
                                
                print(f'Procesing {time_i}...')
                
                # Write time
                timevar[i] = ocean_time
                
                # Read u
                this_u = ROMS.variables['u'][:]
                # Write u
                uvar[i, :, :] = this_u
                
                # Read v
                this_v = ROMS.variables['v'][:]
                # Write v
                vvar[i, :, :] = this_v
   





#location of the ROMS folder
ROMS=["E:\\NEATL_201902*.nc"]
lista=[]
for i in ROMS:
    files = sorted(glob.glob(i))
    lista += files

lista = sorted(lista)

#dir=location of the output file (*.nc)
agregar_netcdfs(lista, "dir")

