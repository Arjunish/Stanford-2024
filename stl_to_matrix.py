from stl import mesh
import numpy as np
import os

# Print the current working directory to debug the file path
print("Current working directory:", os.getcwd())

# Define the path to the STL file
stl_file_path = input("File name:")  # Update with the correct path if necessary

# Desired height in mm
target_height = 2.675

# Check if the file exists
if not os.path.exists(stl_file_path):
    print(f"No file found named '{stl_file_path}'")
else:
    # Load the STL file
    your_mesh = mesh.Mesh.from_file(stl_file_path)

    # Extract all vertices from the mesh
    vertices = your_mesh.vectors.reshape(-1, 3)

    # Scale the vertices to mm (assuming they are in meters)
    scaled_vertices = vertices * 1000.0  # Convert meters to millimeters

    # Find all unique vertices (bumps)
    unique_vertices, counts = np.unique(scaled_vertices, axis=0, return_counts=True)

    # Filter vertices based on the desired height with a tolerance
    bumps = unique_vertices[np.isclose(unique_vertices[:, 2], target_height, atol=0.499)]

    # Round off each point in the array to 3 decimal points
    bumps_rounded = np.round(bumps, 3)

    # Define the corners of the STL
    num_bumps = len(bumps_rounded)
    print(f"Number of bumps at {target_height} mm: {len(bumps_rounded)}")
    print("Bump coordinates:")
    print(bumps_rounded)

    # Save the filtered and rounded vertices to a file
    np.savetxt('bumpsd7.csv', bumps_rounded, fmt='%.3f', delimiter=',', header='', comments='')
    np.savetxt('bumpsd7.txt', bumps_rounded, fmt='%.3f', delimiter=',', header='', comments='')

