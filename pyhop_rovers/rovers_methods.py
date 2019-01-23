import pyhop

def go_to_waypoint_m(state,rover,waypoint):
    if state.at[rover]==waypoint:
        return [('already_there', rover)]
    else:
        for path in state.can_traverse[rover]:
            if state.at[rover]==path[0] and path[1] not in state.crossed[rover]:
                next_waypoint=path[1]
                break
        return [('navigate', rover, next_waypoint), ('go_to_waypoint', rover, waypoint)]

pyhop.declare_methods('go_to_waypoint', go_to_waypoint_m)

def communicate_soil_data_m(state, rover, waypoint):
    if state.equipped_for_soil_analysis:
        return [('go_to_waypoint', rover, waypoint), ('sample_soil', rover), ('drop', rover), ('communicate_soil_data_to_lander', rover, waypoint)]
pyhop.declare_methods('communicate_soil_data', communicate_soil_data_m)

def communicate_rock_data_m(state, rover, waypoint):
    if state.equipped_for_rock_analysis:
        return [('go_to_waypoint', rover, waypoint), ('sample_rock', rover), ('drop', rover), ('communicate_rock_data_to_lander', rover, waypoint)]
pyhop.declare_methods('communicate_rock_data', communicate_rock_data_m)

def communicate_image_data_m(state, rover, objective, mode):
    camlist=[key for key,value in state.supports[rover].items() if mode in value] #list of cameras with mode support
    if camlist and rover in state.equipped_for_imaging: # rover in state.equipped_for_imaging is exscessively
        #cam=camlist[0] #ill send the whole camlist
        return [('calibrate',rover,camlist,objective), ('take_image',rover, camlist, objective, mode), ('communicate_image_data_to_lander', rover, objective, mode)]#Calibrate, Take_image y Communicate_image_data_to_lander
pyhop.declare_methods('communicate_image_data', communicate_image_data_m)
