import pyhop
import rovers_methods
import rovers_tasks

state1=pyhop.State('state1')

state1.at={'r0':'w3'}
state1.at_lander='w0'
state1.empty={'r0store':True}
state1.calibrated={'r0':{'c0':False}}
state1.at_soil_sample={'w0','w2','w3'}
state1.at_rock_sample={'w1','w2','w3'}
state1.have_rock_analysis={'r0':[]}
state1.have_soil_analysis={'r0':[]}
state1.have_image={'r0':[]}
state1.communicated_soil_data=[]
state1.communicated_rock_data=[]
state1.communicated_image_data=[]
state1.crossed={'r0':['w3']}

#Static info
state1.can_traverse={'r0':[['w0','w3'],['w1','w3'],['w1','w2'],['w2','w0'],['w3','w0'],['w3','w1'],['w2','w1'],['w0','w2']]}
state1.equipped_for_soil_analysis={'r0'}
state1.equipped_for_rock_analysis={'r0'}
state1.equipped_for_imaging={'r0'}
state1.supports={'r0':{'c0':{'colour','high-res'}}}
state1.calibration_target={'c0':'o1'}
state1.on_board={'r0':{'c0'}}
state1.visible={'w0':{'w1','w2','w3'}, 'w1':{'w0','w2','w3'}, 'w2':{'w0','w1','w3'}, 'w3':{'w0','w1','w2'}}
state1.visible_from={'o1':{'w0','w1','w2','w3'}}
state1.store_of={'r0':'r0store'}
state1.rovers=['r0']

#GOAL

pyhop.pyhop(state1, [('communicate_soil_data','w2')], verbose=3)
#pyhop.pyhop(state1, [('communicate_rock_data','w3')], verbose=3)
#pyhop.pyhop(state1, [('communicate_image_data','o1','high-res')], verbose=3)