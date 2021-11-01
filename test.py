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


@pytest.mark.skipif('cache-a' not in os.environ['ENVNAME'], reason='env not cache-a')
@pytest.mark.parametrize('name,dir', [('data_x', 'cache_1'), ('data_y', 'cache_2')])
def test_cache_a(name, dir):
    assert not os.path.exists(dir)  # should be a cache miss
    os.makedirs(dir)
    with open(os.path.join(dir, 'test.txt'), 'w') as f:
        f.write(f'writing to {name}:{dir} cache in cache-a')


@pytest.mark.skipif('cache-b' not in os.environ['ENVNAME'], reason='env not cache-b')
def test_cache_b():
    assert not os.path.exists('cache_1')  # should be a cache miss
    assert not os.path.exists('cache_2')  # should not have loaded global cache
    with open(os.path.join('cache_3', 'test.txt'), 'r') as f:  # should load from cache-a
        assert f.readline() == f'writing to data_x:cache_1 cache in cache-a'
