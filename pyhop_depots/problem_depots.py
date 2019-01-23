import pyhop
import methods
import tasks
%load_ext autoreload
%autoreload 2

state1=pyhop.State('state1')
#state1.call_area='3'
state1.at={'T1':'D0','T0':'D1'}
state1.fuel={'T0':'4','T1':'4'}

state1.empty={'H0':True,'H1':True,'H2':True,'H3':True,'H4':True,'T0':['C05','C07'],'T1':True,'P00':['C1','C11','C12'],'P01':True, 'P10':['C0','C01','C02','C03'],'P20':True,'P30':True,'P40':True}
state1.crossed={'T1':['D0'],'T0':['D1']}

#Static info
#state1.can_traverse=[['D0','D1'],['D1','D0'],['D1','D2'],['D2','D1'],['D0','D2'],['D2','D0']]
state1.can_traverse={'D0':['D1','D2'], 'D1':['D0','D2','FUEL'], 'D2':['D0','D1','D3'], 'D3':['D2','D4'], 'D4':['D3'], 'FUEL':['D1']}
state1.pallet_board={'D0':{'P00','P01'},'D1':{'P10'},'D2':{'P20'},'D3':{'P30'},'D4':{'P40'}}
state1.crans={'H0':'D0', 'H1':'D1', 'H2':'D2', 'H3':'D3', 'H4':'D4'}
state1.fuel_limit={'T0':'8','T1':'8'}
state1.carry_limit={'T0':'2','T1':'2'}
state1.truck=['T1','T0']

#GOAL
pyhop.print_methods()
pyhop.print_operators()
#pyhop.pyhop(state1, [('go_to_waypoint','T1','D4')], verbose=3)
pyhop.pyhop(state1,[('move_container', ['C0','C11','C05'], 'P40')], verbose=3)
#pyhop.pyhop(state1,[('move_container', ['C01'], 'P40')], verbose=3)

  
    #find shortestpath -done
    #move method replaced on base of shortpath - done
    #find nearest truck - done
    #fuel count, limit, consumption - done
    #refuel if needed-done
    #select nearest truck based on fuel limit (if path consumptin is lesser,than truck limit) - done
    #add check if its on truck -done
    #double pallet container replacement use instead of truck moving if available
    #add check if its on cran - done,but removed.
    #truck carry_limit added and managed

   