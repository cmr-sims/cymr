"""Test fitting to summary statistics."""

import importlib
import pytest
import numpy as np
import pandas as pd
from psifr import fr
from cymr import statistics


@pytest.fixture()
def raw():
    """Create raw free recall data."""
    subjects = [1, 1, 2, 2]
    lists = [1, 2, 1, 2]
    study = [
        ['absence', 'hollow', 'pupil'], 
        ['fountain', 'piano', 'pillow'],
        ['absence', 'hollow', 'pupil'], 
        ['fountain', 'piano', 'pillow'],
    ]
    recall = [
        ['hollow', 'pupil', 'empty'], 
        ['pillow', 'fountain', 'pillow'],
        ['absence', 'hollow'],
        ['piano', 'fountain', 'pillow'],
    ]
    item_index = ([[0, 1, 2], [3, 4, 5], [0, 1, 2], [3, 4, 5]], None)
    task = ([[1, 1, 1], [2, 2, 2], [1, 1, 1], [2, 2, 2]], None)
    raw = fr.table_from_lists(
        subjects, study, recall, lists, item_index=item_index, task=task
    )
    return raw


@pytest.fixture()
def data(raw):
    """Create merged free recall data."""
    data = fr.merge_free_recall(raw, study_keys=['task', 'item_index'])
    return data


@pytest.fixture()
def stats_def():
    stats_def = statistics.Statistics()
    stats_def.set_stat(
        "spc", "psifr.fr:spc", ["input"], "recall", "group", conditions=["task"]
    )
    stats_def.set_stat(
        "lag_crp", "psifr.fr:lag_crp", ["lag"], "prob", "subject", conditions=["task"]
    )
    return stats_def


def test_eval_stats(data, stats_def):
    stats, results = stats_def.eval_stats(data)
