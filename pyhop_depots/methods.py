import pyhop
from tasks import find_shortest_path as find_sh

def go_to_waypoint_m(state,truck,waypoint): 
    if state.at[truck]==waypoint:
        return [('already_there', truck)]
    else:
        if len(find_sh(state.can_traverse, state.at[truck], waypoint))+len(find_sh(state.can_traverse, waypoint, 'FUEL'))-2>int(state.fuel[truck]):
            return [('go_to_fuel',truck,waypoint)]
        
        next_point=find_sh(state.can_traverse, state.at[truck], waypoint)[1]
        state.at[truck]=next_point
        state.fuel[truck]=int(state.fuel[truck])-1
        return [('go_to_waypoint', truck, waypoint)]
pyhop.declare_methods('go_to_waypoint', go_to_waypoint_m)
        
def go_to_fuel_m(state,truck,waypoint): 
    if state.at[truck]=='FUEL':
        state.fuel[truck]=state.fuel_limit[truck]
        print('++++++++++++++++++++REFUEL+++++++++++++++++')
        return [('go_to_waypoint', truck, waypoint)]
    else:
        next_point=find_sh(state.can_traverse, state.at[truck], 'FUEL')[1]
        state.at[truck]=next_point
        state.fuel[truck]=int(state.fuel[truck])-1
        return [('go_to_fuel', truck, waypoint)]
pyhop.declare_methods('go_to_fuel', go_to_fuel_m)
    
def unload_all_m (state, cran, truck, pallet):
    if state.empty[truck] is True:
        return [('already_unloaded', truck)]
    else:
        return [('unload', cran, truck),('drop', cran, pallet) ,('unload_all', cran, truck, pallet)]
pyhop.declare_methods('unload_all', unload_all_m)

def move_container_m(state, container_list, destination):
    platform_dst=[plat for plat,pallet in state.pallet_board.items() if destination in pallet][0]
    cran_dst=[cran for cran,platform in state.crans.items() if platform_dst is platform][0]
    #search for container
    for container in container_list:
        print('=======CONTAINER ',container,'=======')
        truck=''
        distance_from_tr_min=0
        pallet_src=[loc for loc,cont in state.empty.items() if cont is not True and container in cont][0]

        if pallet_src==destination:
            print('++++++++++++CONTINUE++++++++++++++')
            continue
        else:
            #check, if container is in a truck
            if [tr for tr in state.truck if pallet_src in tr]: #check, if container is in a truck
                truck=[tr for tr in state.truck if pallet_src in tr][0]
                print('==========CONTAINER IS ALLREADY AT TRUCK ',truck,'================')
                return [('go_to_waypoint', truck, platform_dst),('unload', cran_dst, truck),('drop', cran_dst, destination),('move_container', container_list, destination)]

                        
            platform_src=[plat for plat,pallet in state.pallet_board.items() if pallet_src in pallet][0]
            cran_src=[cran for cran,platform in state.crans.items() if platform_src is platform][0]
            
            #check,that we can move container from src to dst
            if len(find_sh(state.can_traverse, platform_src, platform_dst)) > 0:
                #check if its on top
                if state.empty[pallet_src][-1] is not container:   
                    #not at top-pick & move upper container
                    if len(state.pallet_board[platform_src])>1:
                        #if we have 2 pallets move locally until needed will be at top
                        p2=[p for p in state.pallet_board[platform_src] if pallet_src not in p][0]
                        return [('lift', cran_src, pallet_src), ('drop', cran_src, p2), ('move_container', container_list, destination)]
                    else:
                        #put in a truck and move to another direction
                        #getting direction info
                        false_pallet=list([p for b,p in state.pallet_board.items() if pallet_src not in p and destination not in p][0])[0]
                        false_platform=[plat for plat,pallet in state.pallet_board.items() if false_pallet in pallet][0]
                        false_cran=[cran for cran,platform in state.crans.items() if false_platform is platform][0]
                       
                    #selecting  truck
                        for tr,pos in state.at.items():
                            if int(state.fuel_limit[tr])<len(find_sh(state.can_traverse, platform_src, platform_dst))+len(find_sh(state.can_traverse, platform_dst, 'FUEL'))-2:
                                continue
                            if find_sh(state.can_traverse, pos, platform_src):
                                distance_from_tr=len(find_sh(state.can_traverse,pos, platform_src))
                                if distance_from_tr_min==0 or distance_from_tr<distance_from_tr_min:
                                    distance_from_tr_min=distance_from_tr
                                    truck=tr
                        print('============TRUCK SELECTED for moving wrong container',truck,'=============')
                        #if truck not full
                        #if state.empty[truck] is not True and len(state.empty[truck])+1 == int(state.carry_limit[truck]):
                        
                        if state.empty[truck] is not True and len(state.empty[truck]) == int(state.carry_limit[truck]):
                            return [('go_to_waypoint', truck, false_platform),('unload_all', false_cran, truck, false_pallet),('move_container', container_list, destination)]
                        
                        if state.empty[truck] is not True and len(state.empty[truck])+1 == int(state.carry_limit[truck]):
                            return [('go_to_waypoint', truck, platform_src),('lift', cran_src, pallet_src),('load', cran_src, truck),('go_to_waypoint', truck, false_platform),('unload_all', false_cran, truck, false_pallet),('move_container', container_list, destination)]
                        
                        if state.empty[truck] is True and int(state.carry_limit[truck])==1:
                            return [('go_to_waypoint', truck, platform_src),('lift', cran_src, pallet_src),('load', cran_src, truck),('go_to_waypoint', truck, false_platform),('unload_all', false_cran, truck, false_pallet),('move_container', container_list, destination)]
                        
                        
                        if state.empty[truck] is True or len(state.empty[truck])< int(state.carry_limit[truck]):
                            return [('go_to_waypoint', truck, platform_src),('lift', cran_src, pallet_src),('load', cran_src, truck),('move_container', container_list, destination)]
                           
                            #pick an fill one cont  - return
                        #else move to 
                        return False
                    #[('go_to_waypoint', truck, false_platform),('unload', false_cran, truck),('drop', false_cran, false_pallet),('move_container', container_list, destination)]
                        #return [('go_to_waypoint', truck, platform_src),('lift', cran_src, pallet_src),('load', cran_src, truck),('go_to_waypoint', truck, false_platform),('unload', false_cran, truck),('drop', false_cran, false_pallet),('move_container', container_list, destination)]

                else:
                    #find nearest truck
                    for tr,pos in state.at.items():
                        if int(state.fuel_limit[tr])<len(find_sh(state.can_traverse, platform_src, platform_dst))+len(find_sh(state.can_traverse, platform_dst, 'FUEL'))-2:
                            continue
                        if find_sh(state.can_traverse, pos, platform_src):
                            distance_from_tr=len(find_sh(state.can_traverse,pos, platform_src))
                            if distance_from_tr_min==0 or distance_from_tr<distance_from_tr_min:
                                distance_from_tr_min=distance_from_tr
                                truck=tr
                    print('============TRUCK SELECTED ',truck,'=============')
                    return [('go_to_waypoint', truck, platform_src),('lift', cran_src, pallet_src),('load', cran_src, truck),('go_to_waypoint', truck, platform_dst),('unload', cran_dst, truck),('drop', cran_dst, destination),('move_container', container_list, destination)]
    if set(container_list).issubset(state.empty[destination]):
        return[('done',container_list,destination)]
pyhop.declare_methods('move_container', move_container_m)            
            
 
