 
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
 
# Generate a sinusoidal surface
x = np.linspace(0, 10, 100) #plug in X
y = np.linspace(0, 10, 100) #plug in Y
X, Y = np.meshgrid(x, y)
Z = np.sin(X) + np.cos(Y) #plug in Z
 
# Flatten the grid for point cloud creation
x_flat = X.flatten()
y_flat = Y.flatten()
z_flat = Z.flatten()
 
# Create a point cloud
points = np.vstack((x_flat, y_flat, z_flat)).T
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
 
# Visualize the point cloud
o3d.visualization.draw_geometries([pcd], window_name="Generated Sinusoidal Point Cloud")
 
# Estimate normals for the point cloud
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
pcd.orient_normals_consistent_tangent_plane(100)
 
# Poisson surface reconstruction
with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
 
# Crop the mesh (optional, depending on the dataset)
bbox = pcd.get_axis_aligned_bounding_box()
mesh = mesh.crop(bbox)
 
# Visualize the surface mesh
o3d.visualization.draw_geometries([mesh], window_name="Reconstructed Surface Mesh (Poisson)")
 
# Optionally, visualize the mesh using matplotlib
vertices = np.asarray(mesh.vertices)
triangles = np.asarray(mesh.triangles)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(vertices[:, 0], vertices[:, 1], vertices[:, 2], triangles=triangles, color='cyan', edgecolor='none')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Reconstructed Surface Mesh (Poisson)')
plt.show()
# Save the point cloud to a PLY file
output_file_path = "sinusoidal_pointcloud.ply"
o3d.io.write_point_cloud(output_file_path, pcd)