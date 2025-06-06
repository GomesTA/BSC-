# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

#My_imports_
import re
import math
############### apagando o modelo base
#del mdb.models['Model-1']

print("************************* SCRIPT BEGINNING *************************")

model_number=0


 
##########Criando o modelo #########################
try:
    Model_name='BSC'
except:
    Model_name='BSC'
#else:
    #Model_name='BSC'+str(BSC_pol)+'_Model_'+str(model_number)+'_th_'+str(thickness_of_neck)+'_X_'+str(dim_semi_axis_x)+'_Y_'+str(Semi_axis_vert)[:2]
print(Model_name)
mdb.Model(modelType=STANDARD_EXPLICIT, name=Model_name)
Part_name = 'My_BSC_'+str(model_number)
Part_name_2 = 'My_Bell_Mouth_'+str(model_number)
Part_name_3 = 'My_dog_'+str(model_number)
if model_number==0:
    del mdb.models['Model-1'] #apagando o modelo default ATENCAO AQUI


################## INPUTS ###############################
    
with open(r"C:\Users\limadb\.spyder-py3\output_abq.txt", 'r') as file:
    # Read the entire content of the file
    data = file.read()
    
    # Use eval to interpret the string as Python code and store in coordinates
    coordinates = eval(data)


coordinates_1 = coordinates[0]
coordinates_2 = coordinates[1]
coordinates_3 = coordinates[2]
coordinates_4 = coordinates[3]
coordinates_5 = coordinates[4]
coordinates_6 = coordinates[5]#bell mouth
Tuple_Loads = coordinates[7]
List_Set_Edge = coordinates[8]#sets edge
List_Set_Node = coordinates[9]#sets nodes
mid_length = coordinates[10]#changes the number of surfaces of the BSC. Conditional for surface creation
Surface_kit=coordinates[11]
mesh_size_BM=coordinates[12][0]
mesh_size_BSC=coordinates[12][1]

print(Tuple_Loads)

################## PART - BSC ##################################

mdb.models[Model_name].ConstrainedSketch(name='__profile__', sheetSize=5000)
mdb.models[Model_name].sketches['__profile__'].ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
mdb.models[Model_name].sketches['__profile__'].FixedConstraint(entity=mdb.models[Model_name].sketches['__profile__'].geometry[2])

for polyline in [coordinates_1,coordinates_2,coordinates_3,coordinates_4,coordinates_5]:
    for my_index in range(0,len(polyline)-1,1):
        point1=polyline[my_index]
        point2=polyline[my_index+1]
        #print(point1,point2)
        mdb.models[Model_name].sketches['__profile__'].Line(point1=point1, point2=point2)

    
mdb.models[Model_name].Part(dimensionality=THREE_D, name=Part_name, type=DEFORMABLE_BODY)
mdb.models[Model_name].parts[Part_name].BaseSolidRevolve(angle=360.0, flipRevolveDirection=OFF, sketch=mdb.models[Model_name].sketches['__profile__'])
#del mdb.models[Model_name].sketches['__profile__']

########################################## PARTITIONS ##########################################

mdb.models[Model_name].parts[Part_name].DatumPlaneByPrincipalPlane(offset=0.0, principalPlane=XYPLANE)
number_of_radial_partitions=4
for i in range(1,number_of_radial_partitions):
    mdb.models[Model_name].parts[Part_name].DatumPlaneByRotation(angle=(180/number_of_radial_partitions)*i, axis=mdb.models[Model_name].parts[Part_name].datums[1], plane=mdb.models[Model_name].parts[Part_name].datums[2])

    
Cells_List = mdb.models[Model_name].parts[Part_name].cells
for j in range(1,number_of_radial_partitions+1):
    for i in Cells_List:
        try:
            mdb.models[Model_name].parts[Part_name].PartitionCellByDatumPlane(cells=i, datumPlane=mdb.models[Model_name].parts[Part_name].datums[1+j])
            #print("fiz o "+str(i)+" corte")
        except:
            None


#CRIANDO UMA SURFACE PARA O COUPLING DO FLANGE COM BOUNDING BOX.
mdb.models[Model_name].parts[Part_name].Surface(name='Surf-FLANGE-BASE', side1Faces=mdb.models[Model_name].parts[Part_name].faces.getByBoundingBox(-800,-5,-700,700,-4,800))

########################################## PROPERTY ##########################################
mdb.models[Model_name].Material(name='Steel')
mdb.models[Model_name].materials['Steel'].Density(table=((7.8e-09, ), ))
mdb.models[Model_name].materials['Steel'].Elastic(table=((207000.0, 0.3), ))

material_table = {'S355':((345.0, 0.0), (573.0, 0.2)),
                  'F52':((360.0, 0.0), (546.0, 0.18)),
                  'F65':((450.0, 0.0), (636.0, 0.18)),
                  'F22':((517.0, 0.0), (772.9, 0.17))}
mdb.models[Model_name].materials['Steel'].Plastic(scaleStress=None, table=material_table['F52'])

#mdb.models[Model_name].materials['Steel'].Plastic(scaleStress=None, table=((345.0, 0.0), (573.0, 0.2)))
mdb.models[Model_name].HomogeneousSolidSection(material='Steel', name='Steel_solid', thickness=None)
mdb.models[Model_name].parts[Part_name].Set(cells=mdb.models[Model_name].parts[Part_name].cells, name='Set-1')
mdb.models[Model_name].parts[Part_name].SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=mdb.models[Model_name].parts[Part_name].sets['Set-1'], sectionName='Steel_solid', thicknessAssignment=FROM_SECTION)

######################################## PART - BELL MOUTH #########################################
del mdb.models[Model_name].sketches['__profile__']
mdb.models[Model_name].ConstrainedSketch(name='__profile__', sheetSize=5000)
mdb.models[Model_name].sketches['__profile__'].ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
mdb.models[Model_name].sketches['__profile__'].FixedConstraint(entity=mdb.models[Model_name].sketches['__profile__'].geometry[2])

for polyline in [coordinates_6]:
    for my_index in range(0,len(polyline)-1,1):
        point1=polyline[my_index]
        point2=polyline[my_index+1]
        #print(point1,point2)
        mdb.models[Model_name].sketches['__profile__'].Line(point1=point1, point2=point2)
        
BM_height=[coordinates_6][-1][-1][1]

mdb.models[Model_name].Part(dimensionality=THREE_D, name=Part_name_2, type=DEFORMABLE_BODY)
mdb.models[Model_name].parts[Part_name_2].BaseSolidRevolve(angle=360.0, flipRevolveDirection=OFF, sketch=mdb.models[Model_name].sketches['__profile__'])

############ \/ BM partition

mdb.models[Model_name].parts[Part_name_2].DatumPlaneByPrincipalPlane(offset=0.0, principalPlane=XYPLANE)
number_of_radial_partitions=1
for i in range(1,number_of_radial_partitions):
    #mdb.models[Model_name].parts[Part_name_2].DatumPlaneByRotation(angle=(180/number_of_radial_partitions)*i, axis=mdb.models[Model_name].parts[Part_name_2].datums[1], plane=mdb.models[Model_name].parts[Part_name_2].datums[2])
    mdb.models[Model_name].parts[Part_name_2].DatumPlaneByRotation(angle=(0)*i, axis=mdb.models[Model_name].parts[Part_name_2].datums[1], plane=mdb.models[Model_name].parts[Part_name_2].datums[2])

    
Cells_List = mdb.models[Model_name].parts[Part_name_2].cells
for j in range(1,number_of_radial_partitions+1):
    for i in Cells_List:
        try:
            mdb.models[Model_name].parts[Part_name_2].PartitionCellByDatumPlane(cells=i, datumPlane=mdb.models[Model_name].parts[Part_name_2].datums[1+j])
            #print("fiz o "+str(i)+" corte")
        except:
            None

############ /\ BM partition

#assigning a material to the BM
mdb.models[Model_name].parts[Part_name_2].Set(cells=mdb.models[Model_name].parts[Part_name_2].cells, name='Set-BM')
mdb.models[Model_name].parts[Part_name_2].SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=mdb.models[Model_name].parts[Part_name_2].sets['Set-BM'], sectionName='Steel_solid', thicknessAssignment=FROM_SECTION)


##########SURFACE CREATION for bell mouth
print("The bell mouth height is: "+str(BM_height))
mdb.models[Model_name].parts[Part_name_2].Surface(name='BM-Top-surf', side1Faces=mdb.models[Model_name].parts[Part_name_2].faces.getByBoundingBox(-950,BM_height-1,-950,950,BM_height+1,950))


########################################## INSTANCE CREATION - BSC ##########################################
mdb.models[Model_name].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models[Model_name].rootAssembly.Instance(dependent=ON, name=Model_name+'_'+str(model_number)+'_inst', part=mdb.models[Model_name].parts[Part_name])
mdb.models[Model_name].rootAssembly.ReferencePoint(point=(0.0, -5.0, 0.0))

########################################## COUPLING - BSC ##########################################
mdb.models[Model_name].Coupling(adjust=True, alpha=0.0, controlPoint=Region(referencePoints=(mdb.models[Model_name].rootAssembly.referencePoints[4], )), couplingType=KINEMATIC, influenceRadius=WHOLE_SURFACE, localCsys=None, name='Coupling_base', surface=
mdb.models[Model_name].rootAssembly.instances[Model_name+'_'+str(model_number)+'_inst'].surfaces['Surf-FLANGE-BASE'], u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)

########################################### MESH ######################################################
##################BSC
mdb.models[Model_name].parts[Part_name].seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=mesh_size_BSC)
mdb.models[Model_name].parts[Part_name].generateMesh()

######## SETS CREATION FOR POST PROCESSING \/

# Obtain nodes from part
my_nodes = mdb.models[Model_name].parts[Part_name].nodes
for set_node in List_Set_Node:
    try:
        nodeSetName=set_node[0]
        initialCoord=set_node[1]
        endCoord=set_node[2]
    
        # Create a list to store the selected nodes
        selectedNodes = []
    
        # Loop through each node and check if it falls within the coordinate range
        for node in my_nodes:
            x, y, z = node.coordinates
            if (initialCoord[0] <= x <= endCoord[0] and
                initialCoord[1] <= y <= endCoord[1] and
                initialCoord[2] <= z <= endCoord[2]):
                selectedNodes.append(node)
    
        #print(selectedNodes)
    
        selectedNodeLabels = [node.label for node in selectedNodes]
        
        # Create the set using sequenceFromLabels with the list of labels
        mdb.models[Model_name].parts[Part_name].Set(
            name=nodeSetName,
            nodes=mdb.models[Model_name].parts[Part_name].nodes.sequenceFromLabels(labels=selectedNodeLabels)
        )
    except:
        pass


# Obtain edges from part
my_edges = mdb.models[Model_name].parts[Part_name].edges
print("My edge length is "+str(len(my_edges)))
for set_edge in List_Set_Edge:
    try:
        edgeSetName=set_edge[0]
        initialCoord=set_edge[1]
        endCoord=set_edge[2]
        
        
        
        # Create a list to store the selected nodes
        selectedEdges = []
        
        # Loop through each edge and check if it falls within the coordinate range
        for edge in my_edges:
            x, y, z = (edge.pointOn)[0]
            if (initialCoord[0] <= x <= endCoord[0] and
                initialCoord[1] <= y <= endCoord[1] and
                initialCoord[2] <= z <= endCoord[2]):
                #print(x,y,z)
                selectedEdges.append(edge)
            
        selectedEdges_findAt = [my_edges.findAt(edge.pointOn) for edge in selectedEdges]
        # Create the set using sequenceFromLabels with the list of labels
        mdb.models[Model_name].parts[Part_name].Set(name=edgeSetName,edges=selectedEdges_findAt)
    except:
        pass


######### SETS CREATION FOR POST PROCESSING /\


###############################Bell Mouth
mdb.models[Model_name].parts[Part_name_2].seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=mesh_size_BM)
mdb.models[Model_name].parts[Part_name_2].generateMesh()

############################# INSTANCE CREATION - BELL MOUTH ########################################

mdb.models[Model_name].rootAssembly.regenerate()
mdb.models[Model_name].rootAssembly.Instance(dependent=ON, name=Part_name_2+'_'+str(model_number)+'_inst', part=mdb.models[Model_name].parts[Part_name_2])
mdb.models[Model_name].rootAssembly.ReferencePoint(point=(0.0, BM_height, 0.0))
mdb.models[Model_name].rootAssembly.regenerate()

print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
########### Creating the surfaces that will be used in the BC and Interaction for the BM
model_name = Model_name
# Access the model and part
#Surf_Set_name=['Top_BM_Encastre']
Surf_Set_name=['BM-contact-surf']

instance_name = Part_name_2+'_'+str(model_number)+'_inst'
print(instance_name)

# Get the instance from the assembly
assembly = mdb.models[model_name].rootAssembly
instance = assembly.instances[instance_name]


faces = instance.faces
print("A QUANTIDADE DE FACES NA PARTE BM E DE :" + str(len(faces)))
#print(faces)

# Print the list of face labels
#print("Faces in the part:")
if len(faces) == 24:#BSN900E
    Top_BM_face_index_list = [2, 5, 7, 9, 19, 20, 21, 22]           
elif len(faces)==20:
    Top_BM_face_index_list=[5, 7, 17, 18]#BSN900C or BSN300
elif len(faces)==56:
    Top_BM_face_index_list=[21,23,25,27,52,53,54,55]#PPC300
elif len(faces)==60:
    Top_BM_face_index_list=[19,21,23,25,27,29,54,55,56,57,58,59]#PPC350 needs to be coded
    #Top_BM_face_index_list=[19,21,23,25,27,29]#PPC350 needs to be coded




# Initialize an empty list to store face points
Top_BM_tuple_package = []

for face in faces:
    #print(str(face.getCentroid()))
    print(str(face.index) + "___" + str(face.pointOn) + "___" + str(face.getCentroid()))
    if face.index in Top_BM_face_index_list:
        Top_BM_tuple_package.append((face.pointOn[0],))  # Ensure it's a tuple inside a list

###########new


instance = mdb.models[model_name].rootAssembly.instances[Model_name+'_'+str(model_number)+'_inst']

#Dovetail surface
outer_faces_dovetail = instance.faces.getByBoundingCylinder(
    center1=(0, Surface_kit[0], 0), #O y do center 1 e o ultimo y do inf_dovetail-1
    center2=(0, Surface_kit[1], 0), #O y do center 2 e o P3[1]+1
    radius=1e4 #arbitratiamente grande
)


inner_faces_dovetail = instance.faces.getByBoundingCylinder(
    center1=(0, Surface_kit[0], 0), #O y do center1 e o ultimo y do inf_dovetail-1
    center2=(0, Surface_kit[2], 0), #O y do center 2 e o P1[1]+1
    radius=Surface_kit[3]# O raio das inner faces e o ultimo x do inf_dovetail+1
)

print('Total faces found from large cylinder:', len(outer_faces_dovetail))
mdb.models[model_name].rootAssembly.Surface(side1Faces=outer_faces_dovetail, name='LargeCylinderSurface_dovetail')

print('Total faces found from small cylinder:', len(inner_faces_dovetail))
mdb.models[model_name].rootAssembly.Surface(side1Faces=inner_faces_dovetail, name='SmallCylinderSurface_dovetail')

intersection_faces_dovetail = []
count_intersection=0
for face in outer_faces_dovetail:
    if face not in inner_faces_dovetail:
        intersection_faces_dovetail.append(face)
        count_intersection+=1

print(count_intersection)
# Create the surface
mdb.models[model_name].rootAssembly.Surface(side1Faces=FaceArray(intersection_faces_dovetail), name='IntersectionSurface_dovetail')


### External cylinder surface
outer_faces_ext_cyl = instance.faces.getByBoundingCylinder(
    center1=(0, Surface_kit[4], 0), #O y do center 1 e o P3[1]-1
    center2=(0, 1e4, 0), #arbitratiamente grande
    radius=1e4 #arbitratiamente grande
)


inner_faces_ext_cyl = instance.faces.getByBoundingCylinder(
    center1=(0, Surface_kit[4], 0), #O y do center 1 e o P3[1]-1
    center2=(0, 1e4, 0), #arbitratiamente grande
    radius=Surface_kit[5] # O raio e o ponto do fillet externo do external cylinder mais 1
)

print('Total faces found from large cylinder:', len(outer_faces_ext_cyl))
mdb.models[model_name].rootAssembly.Surface(side1Faces=outer_faces_ext_cyl, name='LargeCylinderSurface_ext_cyl')

print('Total faces found from small cylinder:', len(inner_faces_ext_cyl))
mdb.models[model_name].rootAssembly.Surface(side1Faces=inner_faces_ext_cyl , name='SmallCylinderSurface_ext_cyl')


intersection_faces_ext_cyl = []
count_intersection=0
for face in outer_faces_ext_cyl:
    if face not in inner_faces_ext_cyl :
        intersection_faces_ext_cyl.append(face)
        count_intersection+=1

print(count_intersection)
# Create the surface
mdb.models[model_name].rootAssembly.Surface(side1Faces=FaceArray(intersection_faces_ext_cyl), name='IntersectionSurface_ext_cyl')

Contact_surface_BSC = intersection_faces_ext_cyl+intersection_faces_dovetail

mdb.models[model_name].rootAssembly.Surface(side1Faces=FaceArray(Contact_surface_BSC), name='Contact-Surf-BSC-from-faces')


################ new

# Get the assembly and instances
assembly = mdb.models[model_name].rootAssembly
instance_1 = assembly.instances[instance_name]

# Creating the surface for the top BM
assembly.Surface(name=Surf_Set_name[0], side1Faces=instance_1.faces.findAt(*Top_BM_tuple_package))



########################################## COUPLING BM TOP ##########################################
print(str(mdb.models[Model_name].rootAssembly.referencePoints))
mdb.models[Model_name].Coupling(adjust=False, alpha=0.0, controlPoint=Region(referencePoints=(mdb.models[Model_name].rootAssembly.referencePoints[8], )), couplingType=KINEMATIC, influenceRadius=WHOLE_SURFACE, localCsys=None, name='Coupling_Top_BM',
surface=mdb.models[Model_name].rootAssembly.instances[Part_name_2+'_'+str(model_number)+'_inst'].surfaces['BM-Top-surf'],
u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)



#assigning the surface of the Top encastre to an assembly Set
assembly.Set(faces=assembly.surfaces[Surf_Set_name[0]].faces, name=Surf_Set_name[0]+'_set')
assembly.Set(referencePoints=(mdb.models[Model_name].rootAssembly.referencePoints[8], ),name='Top_ref_set')


print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")

######################################## STEPS ########################################################
mdb.models[Model_name].ImplicitDynamicsStep(alpha=DEFAULT, amplitude=RAMP, application=QUASI_STATIC, initialConditions=OFF, initialInc=0.01, minInc=1e-08, name='Step-1', nohaf=OFF, previous='Initial')
#mdb.models[Model_name].ImplicitDynamicsStep(alpha=DEFAULT, amplitude=RAMP, application=QUASI_STATIC, initialConditions=OFF, initialInc=0.01, minInc=1e-08, name='Step-2', nohaf=OFF, previous='Step-1')
mdb.models[Model_name].fieldOutputRequests['F-Output-1'].setValues(frequency=1)
mdb.models[Model_name].steps['Step-1'].setValues(nlgeom=ON)

###################################### LOADS  ###########################################
mdb.models[Model_name].ConcentratedForce(cf1=Tuple_Loads[0], createStepName='Step-1', distributionType=UNIFORM, field='', localCsys=None, name='SF', region=Region(referencePoints=(mdb.models[Model_name].rootAssembly.referencePoints[4], )))
#mdb.models[Model_name].ConcentratedForce(cf2=(my_T*-1), createStepName='Step-1', distributionType=UNIFORM, field='', localCsys=None, name='T', region=Region(referencePoints=(mdb.models[Model_name].rootAssembly.referencePoints[4], )))
mdb.models[Model_name].Moment(cm3=Tuple_Loads[1], createStepName='Step-1', distributionType=UNIFORM, field='', localCsys=None, name='BM', region=Region(referencePoints=(mdb.models[Model_name].rootAssembly.referencePoints[4], )))

##################################### BOUNDARY CONDITION #########################################################
mdb.models[Model_name].rootAssembly.Set(name='Set-RP-Encastre', referencePoints=(mdb.models[Model_name].rootAssembly.referencePoints[8], ))
mdb.models[Model_name].EncastreBC(createStepName='Step-1', localCsys=None, name='BC-encastre-RP', region=mdb.models[Model_name].rootAssembly.sets['Set-RP-Encastre'])


########## CONTACT MODELLING #########################
mdb.models[Model_name].ContactProperty('IntProp-1')
mdb.models[Model_name].interactionProperties['IntProp-1'].TangentialBehavior(dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, table=((0.3, ), ), temperatureDependency=OFF)
mdb.models[Model_name].interactionProperties['IntProp-1'].NormalBehavior(allowSeparation=ON, constraintEnforcementMethod=DEFAULT, pressureOverclosure=HARD)
mdb.models[Model_name].ContactStd(createStepName='Initial', name='Int-1')
#mdb.models[Model_name].interactions['Int-1'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=ON)
mdb.models[Model_name].interactions['Int-1'].contactPropertyAssignments.appendInStep(assignments=((GLOBAL, SELF, 'IntProp-1'), ), stepName='Initial')
#mdb.models[model_name].interactions['Int-1'].includedPairs.setValuesInStep(addPairs=((mdb.models[model_name].rootAssembly.surfaces['BM-contact-surf'], mdb.models[model_name].rootAssembly.surfaces['BSC-contact-surf']), ), stepName='Initial', useAllstar=OFF)
mdb.models[model_name].interactions['Int-1'].includedPairs.setValuesInStep(addPairs=((mdb.models[model_name].rootAssembly.surfaces['BM-contact-surf'], mdb.models[model_name].rootAssembly.surfaces['Contact-Surf-BSC-from-faces']), ), stepName='Initial', useAllstar=OFF)
mdb.models[Model_name].rootAssembly.regenerate()




####################################### JOB ##########################################

mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model=Model_name, modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Job_'+Model_name, nodalOutputPrecision=SINGLE, 
    numCpus=1, numGPUs=0, numThreadsPerMpiProcess=1, queue=None, resultsFormat=
    ODB, scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, 
    waitMinutes=0)
print("************************* !SCRIPT FINISHED RUNNING! *************************")
