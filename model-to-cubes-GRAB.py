import bpy
import json
import math
import mathutils
from mathutils import Vector

def calculate_scale(face, obj):
    vertices = [obj.data.vertices[i].co for i in face.vertices]
    min_x = min(vertices, key=lambda v: v.x).x
    max_x = max(vertices, key=lambda v: v.x).x
    min_y = min(vertices, key=lambda v: v.y).y
    max_y = max(vertices, key=lambda v: v.y).y
    min_z = min(vertices, key=lambda v: v.z).z
    max_z = max(vertices, key=lambda v: v.z).z
    
    width = max_x - min_x
    height = max_y - min_y
    depth = max_z - min_z
    
    scale_factor_x = width / 2
    scale_factor_y = height / 2
    scale_factor_z = depth / 2
    
    return Vector((scale_factor_x, scale_factor_y, scale_factor_z))

selected_objects = bpy.context.selected_objects
all_face_data = []

for obj in selected_objects:
    for face in obj.data.polygons:
        position_local = Vector(face.center)
        position_world = obj.matrix_world @ position_local

        rotation_local = face.normal.rotation_difference(Vector((0, 0, 1)))
        rotation_world = obj.rotation_euler.to_quaternion() @ rotation_local

        bpy.ops.mesh.primitive_cube_add(location=position_world)
        cube = bpy.context.object
        
        cube.location.x = position_world.x
        cube.location.y = position_world.y
        cube.location.z = position_world.z
        
        cube.scale = calculate_scale(face, obj)
        
        material_index = face.material_index
        if material_index >= 0 and material_index < len(obj.data.materials):
            material = obj.data.materials[material_index]
            if material is not None:
                color = (*material.diffuse_color[:3], 1.0)  # Add alpha channel
                cube.data.materials.append(material)
                cube.active_material_index = len(cube.data.materials) - 1
                cube.active_material.diffuse_color = color
        
        face_data = {
            "levelNodeStatic": {
                "shape": 1000,
                "material": 8,
                "position": {
                    "x": -position_world.x,
                    "y": position_world.z,
                    "z": position_world.y
                },
                "scale": {
                    "x": calculate_scale(face, obj).x * 2,
                    "y": calculate_scale(face, obj).z * 2,
                    "z": calculate_scale(face, obj).y * 2
                },
                "rotation": {
                    "w": 1,
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "color": {
                    "r": color[0],
                    "g": color[1],
                    "b": color[2],
                    "a": color[3]
                },
                "isNeon": False
            }
        }
        all_face_data.append(face_data)

# replaces the path with a pfile path to your json file
with open('insert\\json-file\\path\\here.json', 'w') as file:
    json.dump(all_face_data, file)
