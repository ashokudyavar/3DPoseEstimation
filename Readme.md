# Find the intial pose of an object given a CAD model [or a 3d model without textures] 
Requirements :
blender 2.79,VS Studio 15 
python 3.7
<p align ="left">
Step 1:
  </p>
  Make sure the model is axis aligned to its principal components and is scaled to have maximum length 1.
  Generate 3d keypoints for the given obj from 3dKeyPointGenerator. Uses PCL for Visual Studio 15 : vcpkg install pcl:x64-windows. Save the generated keypoints as csv.
  <p align ="left">
 
  Step 2:
  </p>
  <p>
  Generate 4 views. For each of the views get the projections of the keypoints. Use raytracing to eliminate the points which are not visible.</p>
  <p>run :
  <p>blender blank.blend --background --python run_render.py 02818832/car.obj 0 0 0 2 0.png</p>
  <p>blender blank.blend --background --python run_render.py 02818832/car.obj 90 0 0 2 1.png</p>
  <p>blender blank.blend --background --python run_render.py 02818832/car.obj 180 0 0 2 2.png</p>
  <p>blender blank.blend --background --python run_render.py 02818832/car.obj 270 0 0 2 3.png</p>
  
  
  <div class="grid">
  <img height = 240 width = 500 src="https://user-images.githubusercontent.com/34507375/168487619-60b0153d-858d-49cd-9e00-981e834ad47f.png">
  <img height = 240 width = 500 src="https://user-images.githubusercontent.com/34507375/168487622-476319c4-0dcc-4dc2-a858-e66f40eb0ed5.png">
  <img height = 240 width = 500 src="https://user-images.githubusercontent.com/34507375/168487623-763b931e-dee1-4824-b721-a0cdc50e6e65.png">
  <img height = 240 width = 500 src="https://user-images.githubusercontent.com/34507375/168487624-24558dd1-b7c0-4214-a769-57b8752fc4e3.png">
</div>

<p align = "center" > Kepoints on one of the poses </p>
<img height = 240 width = 500 src="https://user-images.githubusercontent.com/34507375/168487850-d3d8e358-4527-42c4-8aad-2282de7c84a9.png">

 <p align ="left">Step 3:  </p>
<p align = "left" > Process the 4 views and the features for mapping. Save the data as 0.pickle,1.pickle,2.pickle,3.pickle. Use csvread.py</p>
 <p align ="left">Step 4:  </p>
<p align = "left" > Generate 2d Harris keypoints for the test image. Reduce the features using mean-shift. Use harrisC.py </p>
<p align ="left">Step 5:  </p>
<p align = "left" > Use match.py for all the poses to find inital guess. The pose with the least error is the best starting pose. Use matchIter.py to refine further. The two files are nearly same except for a few refinement functions. </p>

<p align ="center">Input  </p>
<img height = 240 width = 500 src="https://user-images.githubusercontent.com/34507375/168488563-e7d7932c-6b64-4dd8-8297-60948c297989.png">

<p align ="center">First guess with the reprojection of sampled points of the original mesh</p>
<img height = 240 width = 500 src="https://user-images.githubusercontent.com/34507375/168488597-5cd45ea7-eef9-42f9-bf70-0bd537837790.png">
<p align ="center">Iter 1  </p>
<img height = 240 width = 500 src="https://user-images.githubusercontent.com/34507375/168488705-06717ea9-a7f7-464c-9526-118111b503fb.png">
<p align ="center">Iter 2  </p>
<img height = 240 width = 500 src="https://user-images.githubusercontent.com/34507375/168488704-28125c25-ad1f-4202-800c-0585ac76b8d9.png">
<p align ="left">Monitor the reprojection error in matchIter.py. Pose with the minimum error is the best pose </p>
<p align ="left">Further refinement is possible using Chamfer matching or other image registration techniques </p>

