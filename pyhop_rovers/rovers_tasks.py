import pyhop

def already_there(state, rover):
    state.crossed[rover]=[state.at[rover]]
    return state

def navigate(state, rover, to):
    fr=state.at[rover]
    if to in state.visible[fr]:
        state.at[rover]=to
        state.crossed[rover].append(state.at[rover])
        return state
    else:
        return False

def sample_soil(state,rover):
    st=state.at[rover]
    store=state.store_of[rover]
    print(st, store)
    if st in state.at_soil_sample and state.empty[store]==True:
        state.empty[store]=False
        state.have_soil_analysis[rover].append(st)
        state.at_soil_sample.remove(st)
        return state
    else:
        return False
    
def sample_rock(state,rover):
    st=state.at[rover]
    store=state.store_of[rover]
    if st in state.at_rock_sample and state.empty[store]==True:
        state.empty[store]=False
        state.have_rock_analysis[rover].append(st)
        state.at_rock_sample.remove(st)
        return state
    else:
        return False
    
def drop(state,rover):
    store=state.store_of[rover]
    if state.empty[store]==False:
        state.empty[store]=True
    return state


def calibrate(state,rover,camlist,obj):
    rstate=state.at[rover]
    for cam in camlist:
        if cam in state.calibration_target and rstate in state.visible_from[obj] and state.calibrated[rover][cam]==False:
                state.calibrated[rover][cam]=True #  hint state.calibrated[rover][cam]=not state.calibrated[rover][cam]
    return state
        
        
def take_image(state, rover, camlist, obj, mode):#added rover as param, camlist instead of cam
#el rover, la cámara a utilizar, el objetivo del cual se va a tomar la imagen y el modo de dicha imagen
#Si la cámara está calibrada, se toma la imagen (se actualiza have_image) y la cámara ya no se encuentra calibrada.
    for cam in camlist:
        if state.calibrated[rover][cam]==True:
            state.have_image[rover].append(obj+'_'+rover+state.at[rover]+'_'+cam+'_'+mode)
            state.calibrated[rover][cam]=False
    return state


def communicate_soil_data_to_lander(state,rover,probe_p):#    зачем передавать позицию бича,когда она и так в стейте
    #rstate=state.at[rover]
    if state.at_lander in state.visible[state.at[rover]]:
        state.communicated_soil_data.append(probe_p)
        return state
    else:
        return False

def communicate_rock_data_to_lander(state,rover,probe_p):#    зачем передавать позицию бича,когда она и так в стейте
    rstate=state.at[rover]
    if state.at_lander in state.visible[state.at[rover]]:
        state.communicated_rock_data.append(probe_p)
        return state
    else:
        return False

def communicate_image_data_to_lander(state,rover, obj, mode): #    зачем передавать позицию бича,когда она и так в стейте
    rstate=state.at[rover]
    if state.have_image[rover] and state.at_lander in state.visible[state.at[rover]]: #add. check,if we made some photos
        state.communicated_image_data.append(state.have_image[rover])
        return state
    else:
        return False


pyhop.declare_operators(already_there,navigate,sample_soil,sample_rock,drop,calibrate,take_image,communicate_soil_data_to_lander,communicate_rock_data_to_lander,communicate_image_data_to_lander)
