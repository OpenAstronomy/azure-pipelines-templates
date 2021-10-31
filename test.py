import os
import sys
import warnings

import pytest

if 'cache' in os.environ['ENVNAME']:
    import urllib.request, json
    url = 'https://dev.azure.com/OpenAstronomy/azure-pipelines-templates/_apis/pipelines/1/runs'
    data = urllib.request.urlopen(url).read()
    json_data = json.loads(data)
    BUILD_ID = str(json_data['value'][0]['id'])


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
@pytest.mark.parametrize('name,dir', [('data_x', 'cache_x'), ('data_y', 'cache_y')])
def test_cache_a(name, dir):
    print(f'BUILD_ID:{BUILD_ID}')
    filename = os.path.join(dir, 'test.txt')
    delayed_errors = []
    try:
        if os.path.exists(filename):  # should be cached from previous build
            with open(filename, 'r') as f:
                assert f.readline().startswith(f'writing to {name} cache in')
        else:  # probably first run or cleared cache
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
                warnings.warn(UserWarning(f'Created nonexistent directory "{dir}".'))
            warnings.warn(UserWarning(f'Cached file {filename} was not restored from a previous build.'))
    except AssertionError as e:
        delayed_errors.append(e)
    with open(filename, 'w') as f:
        f.write(f'writing to {name} cache in {BUILD_ID}:cache-a')
    if len(delayed_errors) > 0:
        raise delayed_errors[0]


@pytest.mark.skipif('cache-b' not in os.environ['ENVNAME'], reason='env not cache-b')
@pytest.mark.parametrize('name,dir', [('data_x', 'cache_x'), ('data_y', 'cache_y')])
def test_cache_b(name, dir):
    print(f'BUILD_ID:{BUILD_ID}')
    delayed_errors = []
    try:
        with open(os.path.join(dir, 'test.txt'), 'r') as f:
            assert f.readline() == f'writing to {name} cache in {BUILD_ID}:cache-a'
    except AssertionError as e:
        delayed_errors.append(e)
    with open(os.path.join(dir, 'test.txt'), 'w') as f:
        f.write(f'writing to {name} cache in {BUILD_ID}:cache-b')
    if len(delayed_errors) > 0:
        raise delayed_errors[0]

@pytest.mark.skipif('cache-c' not in os.environ['ENVNAME'], reason='env not cache-c')
def test_cache_c():
    print(f'BUILD_ID:{BUILD_ID}')
    with open(os.path.join('cache_x', 'test.txt'), 'r') as f:
        assert f.readline() == f'writing to data_x cache in {BUILD_ID}:cache-b'
    # data_z key should create cache unique to data_y key
    assert not os.path.exists(os.path.join('cache_y', 'test.txt'))
