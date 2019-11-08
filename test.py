import os
import sys

import pytest

def test_32bit():
    if '32' in os.environ['ENVNAME']:
        assert sys.maxsize == 2147483647
    else:
        assert sys.maxsize == 9223372036854775807


def test_opengl():
    if 'opengl' in os.environ['ENVNAME']:
        from vispy import scene
        from vispy.gloo import gl
        from vispy.gloo.gl.gl2 import _get_gl_func
        canvas = scene.SceneCanvas(keys=None, size=(800, 600), show=True)
        version = gl.glGetParameter(gl.GL_VERSION)
        assert len(version) > 0
    else:
         pytest.skip()
