import pyhop

def already_there(state, truck):
    state.crossed[truck]=[state.at[truck]]
    return state

def already_unloaded(state,truck):
    return state

#Lift(grúa, contenedor, localización): permite desapilar el contenedor con la grúa en la 
#localización indicada. La grúa quedará sosteniendo el contenedor. Sólo se puede desapilar un contenedor que no tiene otro #contenedor sobre él.
def lift(state, cran, pallet):
    if pallet in state.pallet_board[state.crans[cran]] and state.empty[pallet] is not True and state.empty[cran]==True:
        state.empty[cran]=[state.empty[pallet][-1]]
        state.empty[pallet].pop()
        if state.empty[pallet] == []:
            state.empty[pallet]=True
        return state
    else:
        return False

#Drop(grúa, contenedor, localización): permite apilar el contenedor que actualmente 
#sostiene la grúa en la localización indicada. El contenedor sólo puede apilarse en 
#un contenedor o un pallet sin ningún otro contenedor sobre él.
def drop(state, cran, pallet):
    if pallet in state.pallet_board[state.crans[cran]] and state.empty[cran] is not True:
        if state.empty[pallet]==True:
            state.empty[pallet]=state.empty[cran]
        else:
            state.empty[pallet].extend(state.empty[cran])
        state.empty[cran]=True
        return state
    else:
        return False

#Load(grúa, contenedor, camión, localización): permite cargar el contenedor que 
#sostiene la grúa en el camión, todos ellos en la localización indicada. Los camiones tienen capacidad ilimitada.
#Se asume que existe un camión disponible en dicha localización.
def unload(state, cran, truck):
    if state.at[truck] is state.crans[cran] and state.empty[truck] is not True and state.empty[cran] is True:
        state.empty[cran]=[state.empty[truck][-1]]
        state.empty[truck].pop()
        if state.empty[truck] == []:
            state.empty[truck]=True
        return state
    else:
        return False
    
#Unload(grúa, contenedor, camión, localización): permite descargar el contenedor 
#cargado en el camión, que quedará sostenido por la grúa (todos ellos en la localización indicada).
def load(state, cran, truck):
    if state.at[truck] is state.crans[cran] and state.empty[cran] is not True:
        if state.empty[truck]==True:
            state.empty[truck]=state.empty[cran]
        else:
            state.empty[truck].extend(state.empty[cran])
        state.empty[cran]=True
        return state
    else:
        return False


def find_shortest_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start not in graph.keys():
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest
    
    
    
def done(state, container_list, destination):
    return state
#find_shortest_path(path,'D', 'D5')

pyhop.declare_operators(already_there,already_unloaded,lift,drop,load,unload,find_shortest_path,done)
#pyhop.declare_operators(already_there,navigatsample_soil,sample_rock,drop,calibrate,take_image,communicate_soil_data_to_lander,communicate_rock_data_to_lander,communicate_image_data_to_lander)
