************************************
BlenRig 5 Rigging System for Blender 2.8
************************************

**Author:** Juan Pablo Bouza

**Email:** jpbouza@gmail.com


BlenRig is an Auto-rigging and skinning system that provides the user of a Feature Film quality rig (including an advanced facial system).

The current version only supports Biped characters, but more presets will be supported in the near future.

Rig creation includes:

_BlenRig armature

_BlenRig Mesh Deform cage and Lattices

_Basic body mesh for creating low resolution proxy versions of the characters.


Usage
=====


You will find the rig in the **Object Add Panel**, under the **Armature Menu**.

In the **View3d Sidebar** you will find all the animation controls. In the **Armature Data Panel** you will find all the rigging related tools.

You can find more information at https://cloud.blender.org/p/blenrig/

Don't forget to check the `Introduction Guide <https://cloud.blender.org/p/blenrig/56966411c379cf44546120e8>`_

Also check `Vincent's Timelapse <https://cloud.blender.org/p/blenrig/57343500c379cf109d9e4ecc>`_ to have a quick guide about the complete process of rigging a character



For a detailed step by step tutorial, check the `BlenRig Tutorials <https://cloud.blender.org/p/blenrig/56e2fdafc379cf26b1cd8595>`_ section at the Blender Cloud (Subscription required)




System Requirements for animation:  
----------------------------------

**Minimum Processor spec:** Intel i3 or AMD equivalent. 

In this type of computer a high resolution character will roughly reach 24 fps.

**Recommended Processor spec:** Intel i7 or AMD equivalent. 

In this type of computer most rigged high resolution characters will run at 35+ fps. Low resolution proxy versions may run at 50+ fps.





####################
WHAT'S NEW
####################


V 1.001
=======

    - Biped Armature updated to 1.001, fix IK torso bug


V 1.002
=======

    - General changes:

        - New Layer Scheme option in Layer Settings tab (Compact and Expanded Scheme)
    
        - Updated version of generate_customprops script to work with the new armature layer schemes
        
        - New Armature UPDATE button (to update the user's rig with the latest improvements)

    - Biped Armature updated to 1.005:
        
        - Fixed shoulder offset when using FK and Hinge in arms
        
        - Removed Rotation locks in forearm and shin FK controllers
        
        - New lattice_eye_L and R controller in TOON 2 layer
        
        - Look_l and R scaling now makes the eye scale with the Lattice of the eye, giving a smoother result
        
        - Various bone layers and bone shapes fixes
        
    - Bug Fixes:
       
        - Fix for timeline scrubbing slowdown bug
        
        - Fix for error when adding BlenRig to the scene while using local view or local layers
        
 V 1.003
=======

    - Scropt spaces cleanup
    
V 1.004
=======

    - Port to Blender 2.80  
    - Note that for the "Reset Deformers" operator to have an effect on the lattices, you must have the lattices collection turned on in the viewport. (This will be fixed later)
