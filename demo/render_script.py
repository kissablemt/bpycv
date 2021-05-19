import bpy
import numpy as np
import cv2
import sys
sys.path.append(r"D:\git\bpycv")
import bpycv

def remove(target) -> None:
    if isinstance(target, bpy.types.Object):
        if isinstance(target.data, bpy.types.Mesh):
            bpy.data.meshes.remove(target.data, do_unlink=True)
        elif isinstance(target.data, bpy.types.Camera):
            bpy.data.cameras.remove(target.data, do_unlink=True)
        elif isinstance(target.data, bpy.types.PointLight):
            bpy.data.lights.remove(target.data, do_unlink=True)
        else:
            pass
    elif isinstance(target, bpy.types.ParticleSettings):
        bpy.data.particles.remove(target, do_unlink=True)
    elif isinstance(target, bpy.types.Collection):
        bpy.data.collections.remove(target, do_unlink=True)
    elif isinstance(target, bpy.types.Material):
        bpy.data.materials.remove(target, do_unlink=True)
    elif isinstance(target, bpy.types.Mesh):
        bpy.data.meshes.remove(target, do_unlink=True)
    else:
        pass


def clean() -> None:
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.context.scene.frame_set(0)
    for data_attr in ["meshes", "objects", "cameras", "particles", "collections", "materials", ]:
        for data in getattr(bpy.data, data_attr):
            try:
                remove(data)
            except Exception as e:
                print("clean->remove(): ", e)
                

def create_camera() -> bpy.types.Object:
    camera_data = bpy.data.cameras.new(name='Camera')
    camera_object = bpy.data.objects.new('Camera', camera_data)
    bpy.context.scene.collection.objects.link(camera_object)
    bpy.context.scene.camera = camera_object
    camera_object.location = (0, -3.0, 3)
    camera_object.rotation_euler = (0.785, 0, 0)
    return camera_object

def create_light(location) -> bpy.types.Object:
    light_data = bpy.data.lights.new(name='Light', type="POINT")
    light_object = bpy.data.objects.new('Light', light_data)
    bpy.context.scene.collection.objects.link(light_object)
    light_object.location = location
    return light_object
                
                
def create_monkey() -> bpy.types.Object:
    bpy.ops.mesh.primitive_monkey_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    target = bpy.context.object
    mat = bpy.data.materials.get("Monkey Material")
    if mat is None:
        # create material
        mat = bpy.data.materials.new(name="Monkey Material")

    # Assign it to object
    if target.data.materials:
        # assign to 1st material slot
        target.data.materials[0] = mat
    else:
        # no slots
        target.data.materials.append(mat)
    return target

def create_cube() -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    target = bpy.context.object
    mat = bpy.data.materials.get("Cube Material")
    if mat is None:
        # create material
        mat = bpy.data.materials.new(name="Cube Material")

    # Assign it to object
    if target.data.materials:
        # assign to 1st material slot
        target.data.materials[0] = mat
    else:
        # no slots
        target.data.materials.append(mat)
    return target

                
def build_scene() -> None:
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    camera = create_camera()
    light1 = create_light((0.5, 0.5, 1))
    light2 = create_light((-0.5, -0.5, 1))
    
    for i in range(5):
        cube = create_cube()
        cube.location = (np.random.random() * 2 - 1, np.random.random() * 2 - 1, np.random.random() * 2 - 1)
        cube.scale = (0.2, 0.2, 0.2)
        cube.rotation_euler = (np.random.random() * np.pi * 2, np.random.random() * np.pi * 2, np.random.random() * np.pi * 2)

    for j in range(5):
        monkey = create_monkey()
        monkey.location = (np.random.random() * 2 - 1, np.random.random() * 2 - 1, np.random.random() * 2 - 1)
        monkey.scale = (0.3, 0.3, 0.3)
        monkey.rotation_euler = (np.random.random() * np.pi * 2, np.random.random() * np.pi * 2, np.random.random() * np.pi * 2)
    
    for i, obj in enumerate(bpy.data.objects):
        # object ID
        obj["inst_id"] = i + 1 

        # category ID
        if "Cube" in obj.name:
            obj["sem_id"] = 1
        else:
            obj["sem_id"] = 2


def bpycv_test():
    result = bpycv.render_data()
    
    cv2.imwrite(r"D:\tmp\rgb.jpg", result["image"][..., ::-1])  # transfer RGB image to opencv's BGR

    cv2.imwrite(r"D:\tmp\inst.png", result["inst"], [cv2.IMWRITE_PNG_COMPRESSION, 0])

    cv2.imwrite(r"D:\tmp\sem.png", result["sem"], [cv2.IMWRITE_PNG_COMPRESSION, 0])
    

if __name__ == '__main__':
    clean()
    build_scene()
    bpycv_test()
