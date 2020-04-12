"""Test network operations."""

import pytest
import numpy as np
from cymr import network


@pytest.fixture()
def net():
    n_c = 5
    n_f = 3
    net = network.Network(n_c, n_f)
    return net


@pytest.fixture()
def weights():
    mat = np.arange(15).reshape((5, 3))
    return mat


def test_network_init(net):
    n_f = net.n_f
    n_c = net.n_c
    assert net.w_cf_exp.shape == (n_f, n_c)
    assert net.w_cf_pre.shape == (n_f, n_c)
    assert net.w_fc_exp.shape == (n_c, n_f)
    assert net.w_fc_pre.shape == (n_c, n_f)
    assert net.c.shape[0] == n_c
    assert net.f.shape[0] == n_f


def test_pre_weights(net, weights):
    net.add_pre_weights(weights)
    np.testing.assert_array_equal(net.w_fc_pre, weights)
    np.testing.assert_array_equal(net.w_cf_pre, weights.T)


def test_update(net, weights):
    net.add_pre_weights(weights)
    net.c[0] = 1
    net.present_item(0, .5)
    np.testing.assert_allclose(np.linalg.norm(net.c, 2), 1)
    expected = np.array(
        [0.8660254, 0.09128709, 0.18257419, 0.27386128, 0.36514837])
    np.testing.assert_allclose(net.c, expected)
