import os
import sys
import subprocess

import pytest

if 'cache' in os.environ['ENVNAME']:
    import urllib.request, json
    url = 'https://dev.azure.com/OpenAstronomy/azure-pipelines-templates/_apis/pipelines/1/runs'
    data = urllib.request.urlopen(url).read()
    json_data = json.loads(data)
    BUILD_ID = str(json_data['value'][0]['id'])
    subprocess.call(["echo", f"##vso[task.logdetail]Received BUILD_ID {BUILD_ID} from Azure API"])


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


@pytest.mark.skipif('cache-a' not in os.environ['ENVNAME'])
@pytest.mark.parameterize('name,dir', [('data_x', 'cache_x'), ('data_y', 'cache_y')])
def test_cache_a(name, dir):
    filename = os.path.join(dir, 'test.txt')
    if os.path.exists(filename):  # should be cached from previous build
        with open(filename, 'r') as f:
            assert f.readline().startswith(f'writing to {name} cache in')
    else:  # probably first run or cleared cache
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        subprocess.call(["echo", f"##vso[task.logissue type=warning;]Cached file {filename}"
                                 f" was not restored from a previous build."])
    with open(filename, 'w') as f:
        f.write(f'writing to {name} cache in {BUILD_ID}:cache-a')


@pytest.mark.skipif('cache-b' not in os.environ['ENVNAME'])
@pytest.mark.parameterize('name,dir', [('data_x', 'cache_x'), ('data_y', 'cache_y')])
def test_cache_b(name, dir):
    with open(os.path.join(dir, 'test.txt'), 'r') as f:
        assert f.readline() == f'writing to {name} cache in {BUILD_ID}:cache-a'
    with open(os.path.join(dir, 'test.txt'), 'w') as f:
        assert f.write(f'writing to {name} cache in {BUILD_ID}:cache-b')


@pytest.mark.skipif('cache-c' not in os.environ['ENVNAME'])
def test_cache_c():
    with open(os.path.join('cache_x', 'test.txt'), 'r') as f:
        assert f.readline() == f'writing to data_x cache in {BUILD_ID}:cache-b'
    # data_z key should create cache unique to data_y key
    assert not os.path.exists(os.path.join('cache_y', 'test.txt'))
