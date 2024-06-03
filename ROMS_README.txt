Title: Editing specifications for running a ROMS 2D model on Opendrift Oceandrift
Main author: Diego Pereiro
Metadata Author: Patricia Navarro Gonzalez
Date of editing: 04/04/2024

Reader_ROMS_native.py was edited to fit a 2D model from a 3D configuration
Dir: ".\opendrift\readers\reader_roms_native.py

Edit 1\
In    if 's_rho' not in self.Dataset.variables:
            dimensions = 2
        else:
            dimensions = 3
This line was added underneath the indentation of else to force 2 dimensions
        dimensions = 2 #forces the model to only have 2 dimensions

Resulting in
   if 's_rho' not in self.Dataset.variables:
            dimensions = 2
        else:
            dimensions = 3
        dimensions = 2 #forces the model to only have 2 dimensions


Edit 2\
In 	else:
            logger.warning("2D dataset, so deleting u and v from ROMS_variable_mapping")
            self.num_layers = 1
            self.ROMS_variable_mapping['ubar'] = 'x_sea_water_velocity'
            self.ROMS_variable_mapping['vbar'] = 'y_sea_water_velocity'
            del self.ROMS_variable_mapping['u']
            del self.ROMS_variable_mapping['v']

The following lines were deleted
	    self.ROMS_variable_mapping['ubar'] = 'x_sea_water_velocity'
            self.ROMS_variable_mapping['vbar'] = 'y_sea_water_velocity'
            del self.ROMS_variable_mapping['u']
            del self.ROMS_variable_mapping['v']

Resulting in 
	else:
            logger.warning("2D dataset, so deleting u and v from ROMS_variable_mapping")
            self.num_layers = 1