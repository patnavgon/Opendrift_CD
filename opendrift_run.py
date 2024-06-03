#Last edit: 18/04/2024
#Author: Diego Pereiro, edits Patricia Navarro Gonzalez
#Steps: in quotes
#Description: This code runs an Opendrift reverse drift modelling for 
#stranded common dolphins
#The variables related to the 


from opendrift.models.oceandrift import OceanDrift # Import OceanDrift module
from opendrift.readers import reader_ROMS_native  
from opendrift.readers import reader_global_landmask
from datetime import datetime, timedelta
import os #for joining datatypes

landmask = reader_global_landmask.Reader()

''' Here we created a function that runs Opendrift one time. It needs: 
    (1) The name of the file where the results will be generated (filename)
    (2) Latitude  (Manually added)
    (3) Longitude (Manually added)
    (4) Initial date to release the particles (stranding date) (manually added)
    (5) Aggregated ROMS file 
    

    In the function, the duration of the drift needs to be changed manually
    according to the DCC of each case. Each case is commented. 
    '''

def opendrift_run(outputfile, lat, lon, idate, ROMS):#edate removed

    R = 200 # Radius for dispersion around source [meters]
      
    N = 1000 # Number of particles
         
    step = -timedelta(minutes=10) # OpenDrift time step (negative for backward tracking)
        
    NHIS = 1 # Frequency of writing output to file
    
    # Initialize OpenDrift 
    o = OceanDrift(loglevel=20)

    # Initialize ocean reader  
    phys = reader_ROMS_native.Reader(ROMS)#edited for ROMS2d, see README file
    
    # Add readers
    o.add_reader([landmask, phys])
    
    # Use this line to allow a stranded body to go back to the water 
    o.set_config('general:coastline_action', 'previous')
    o.set_config('drift:horizontal_diffusivity', 5) #degree of difusion
    
    # Seed particles
    o.seed_elements(lon=lon, lat=lat,          # Seed at the specified coordinates
                        number=N,              # Number of elements
                        radius=R,              # Radius for dispersion around source 
                        time=[idate],   #final date elimnated# Initial and end date for particle release                    
                        z=0)                   # Seed at the surface
             
    # Run the model for 2 DAYS (DCC1)
    o.run(duration=timedelta(days=2), # Run for 2/5/15 days, manually corrected for each case      
          time_step=step,             # Time step
          time_step_output=NHIS*step, # Output frequency
          outfile=outputfile,           # Output NetCDF file name
          export_variables=['lon', 'lat', 'time']) # Output variables 
                                                    #(just lon, lat and time)
                                            
    #Run the model for 5 DAYS (DCC2)
    o.run(duration=timedelta(days=5), # Run for 2/5/15 days, manually corrected for each case      
          time_step=step,             # Time step
          time_step_output=NHIS*step, # Output frequency
          outfile=outputfile,           # Output NetCDF file name
          export_variables=['lon', 'lat', 'time']) # Output variables 
                                                    # (just lon, lat and time)     
    
    #Run the model for 15 DAYS (DCC3)                                               
    o.run(duration=timedelta(days=15), # Run for 2/5/15 days, manually corrected for each case      
          time_step=step,             # Time step
          time_step_output=NHIS*step, # Output frequency
          outfile=outputfile,           # Output NetCDF file name
          export_variables=['lon', 'lat', 'time']) # Output variables 
                                                    # (just lon, lat and time)

    o.plot(background=['x_sea_water_velocity', 'y_sea_water_velocity'])

    #o.animation(fast=True)#will show the last run    

      
''' MAIN PROGRAMME '''
''' this programme calls the function for each case '''

# Names of the output files (using the stranding ID)
cases= [ "2019_045.nc" ]


#Folder where the output file will be saved
dirname= ""

outputfile = [] #join the folder with the name
for file_name in cases:
    outputfile.append(os.path.join(dirname, 
                             file_name))
    print(outputfile)


longitudes = [ -9.5] #Longitudes of each of the cases
latitudes =  [ 51.5] #Latitudes of each of the cases

# Original stranding date (YYYY-MM-DD)
idates = [ datetime(2019, 2, 25)]


#ROMS files
ROMS = "aggregated\\201902.nc"

# Call Opendrift in a loop
for name, lon, lat, start in zip(outputfile, longitudes, latitudes, idates):
    opendrift_run(name, lat, lon, start, ROMS)#ROMS

