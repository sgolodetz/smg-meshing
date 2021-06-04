import math
import numpy as np
import open3d as o3d
import os

from smg.opengl import OpenGLTriMesh


class MeshUtil:
    """Utility functions related to meshes."""

    # PUBLIC STATIC METHODS

    @staticmethod
    def convert_trimesh_to_opengl(o3d_mesh: o3d.geometry.TriangleMesh) -> OpenGLTriMesh:
        """
        Convert an Open3D triangle mesh to an OpenGL one.

        :param o3d_mesh:    The Open3D triangle mesh.
        :return:            The OpenGL mesh.
        """
        o3d_mesh.compute_vertex_normals(True)
        return OpenGLTriMesh(
            np.asarray(o3d_mesh.vertices),
            np.asarray(o3d_mesh.vertex_colors),
            np.asarray(o3d_mesh.triangles),
            vertex_normals=np.asarray(o3d_mesh.vertex_normals)
        )

    # noinspection PyArgumentList
    @staticmethod
    def load_tello_mesh() -> o3d.geometry.TriangleMesh:
        """
        Load the DJI Tello mesh.

        .. note::
            There is a special function for this because the mesh needs some processing to get it into a usable format.

        :return:    The DJI Tello mesh.
        """
        filename: str = os.path.abspath(os.path.join(__file__, "../../../resources/tello.ply"))
        mesh: o3d.geometry.TriangleMesh = o3d.io.read_triangle_mesh(filename)
        mesh.translate(-mesh.get_center())
        mesh.scale(0.002, np.zeros(3))
        mesh.rotate(o3d.geometry.get_rotation_matrix_from_axis_angle(np.array([math.pi, 0, 0])))
        mesh.compute_vertex_normals()
        mesh.paint_uniform_color(np.array([0, 1, 1]))
        return mesh
