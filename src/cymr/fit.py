"""Simulate free recall experiments."""

from abc import ABC, abstractmethod
import numpy as np
from scipy import optimize
import pandas as pd
from joblib import Parallel, delayed
from psifr import fr


def prepare_lists(data, study_keys=None, recall_keys=None, clean=True):
    """Prepare study and recall data for simulation."""
    if study_keys is None:
        study_keys = ['input', 'item_index']

    if recall_keys is None:
        recall_keys = ['input']

    s_keys = study_keys.copy()
    s_keys.remove('input')
    r_keys = recall_keys.copy()
    r_keys.remove('input')
    merged = fr.merge_free_recall(data, study_keys=s_keys, recall_keys=r_keys)
    if clean:
        merged = merged.query('~intrusion and repeat == 0')

    study = fr.split_lists(merged, 'study', study_keys)
    recall = fr.split_lists(merged, 'recall', recall_keys)

    for i in range(len(study['input'])):
        if 'input' in study_keys:
            study['input'][i] = study['input'][i].astype(int) - 1
        if 'item_index' in study_keys:
            study['item_index'][i] = study['item_index'][i].astype(int)

        if 'input' in recall_keys:
            recall['input'][i] = recall['input'][i].astype(int) - 1
        if 'item_index' in recall_keys:
            recall['item_index'][i] = recall['item_index'][i].astype(int)

    n = np.unique([len(items) for items in study['input']])
    if len(n) > 1:
        raise ValueError('List length must not vary.')
    return study, recall


def prepare_study(study_data, study_keys=None):
    """Prepare study phase data for simulation."""
    if study_keys is None:
        study_keys = ['position', 'item_index']

    study = fr.split_lists(study_data, 'raw', study_keys)
    for i in range(len(study['position'])):
        if 'position' in study_keys:
            study['position'][i] = study['position'][i].astype(int) - 1
        if 'item_index' in study_keys:
            study['item_index'][i] = study['item_index'][i].astype(int)
    return study


def add_recalls(study, recalls_list):
    """Add recall sequences to a study DataFrame."""
    lists = study['list'].unique()
    subjects = study['subject'].unique()
    if len(subjects) > 1:
        raise ValueError('Unpacking multiple subjects not supported.')
    subject = subjects[0]

    # initialize recall trials DataFrame
    n_recall = np.sum([len(r) for r in recalls_list])
    recall = pd.DataFrame({'subject': subject,
                           'list': np.zeros(n_recall, dtype=int),
                           'trial_type': 'recall',
                           'position': np.zeros(n_recall, dtype=int),
                           'item': ''})

    # set basic information (list, item, position)
    n = 0
    for i, seq in enumerate(recalls_list):
        pool = study.loc[study['list'] == lists[i], 'item'].to_numpy()
        for j, pos in enumerate(seq):
            recall.loc[n, 'list'] = lists[i]
            recall.loc[n, 'item'] = pool[pos]
            recall.loc[n, 'position'] = j + 1
            n += 1
    data = pd.concat((study, recall), axis=0, ignore_index=True)
    return data


class Recall(ABC):

    @abstractmethod
    def likelihood_subject(self, study, recall, param, patterns=None,
                           weights=None):
        pass

    def likelihood(self, data, group_param, subj_param=None, patterns=None,
                   weights=None):
        subjects = data['subject'].unique()
        logl = 0
        for subject in subjects:
            param = group_param.copy()
            if subj_param is not None:
                param.update(subj_param[subject])
            subject_data = data.loc[data['subject'] == subject]
            study, recall = self.prepare_sim(subject_data)
            subject_logl = self.likelihood_subject(study, recall, param,
                                                   patterns=patterns,
                                                   weights=weights)
            logl += subject_logl
        return logl

    @abstractmethod
    def prepare_sim(self, subject_data):
        pass

    def fit_subject(self, subject_data, fixed, var_names, var_bounds,
                    patterns=None, weights=None, method='de', **kwargs):
        study, recall = self.prepare_sim(subject_data)

        def eval_fit(x):
            eval_param = fixed.copy()
            eval_param.update(dict(zip(var_names, x)))
            eval_logl = self.likelihood_subject(study, recall, eval_param,
                                                patterns, weights)
            return -eval_logl

        group_lb = [var_bounds[k][0] for k in var_names]
        group_ub = [var_bounds[k][1] for k in var_names]
        bounds = optimize.Bounds(group_lb, group_ub)
        if method == 'de':
            res = optimize.differential_evolution(eval_fit, bounds, **kwargs)
        elif method == 'shgo':
            b = [(lb, ub) for lb, ub in zip(bounds.lb, bounds.ub)]
            res = optimize.shgo(eval_fit, b, **kwargs)
        else:
            raise ValueError(f'Invalid method: {method}')

        # fitted parameters
        param = fixed.copy()
        param.update(dict(zip(var_names, res['x'])))

        logl = -res['fun']
        return param, logl

    def run_fit_subject(self, data, subject, fixed, var_names, var_bounds,
                        patterns=None, weights=None, method='de', **kwargs):
        subject_data = data.loc[data['subject'] == subject]
        param, logl = self.fit_subject(subject_data, fixed, var_names,
                                       var_bounds, patterns, weights,
                                       method, **kwargs)
        results = {**param, 'logl': logl}
        return results

    def fit_indiv(self, data, fixed, var_names, var_bounds, patterns=None,
                  weights=None, n_jobs=None, method='de', **kwargs):
        subjects = data['subject'].unique()
        results = Parallel(n_jobs=n_jobs)(
            delayed(self.run_fit_subject)(
                data, subject, fixed,  var_names, var_bounds, patterns,
                weights, method, **kwargs)
            for subject in subjects)
        d = {subject: res for subject, res in zip(subjects, results)}
        results = pd.DataFrame(d).T
        results.index = results.index.rename('subject')
        return results

    @abstractmethod
    def generate_subject(self, study, param, **kwargs):
        pass

    def generate(self, study, group_param, subj_param=None):
        subjects = study['subject'].unique()
        data_list = []
        for subject in subjects:
            param = group_param.copy()
            if subj_param is not None:
                param.update(subj_param[subject])
            subject_study = study.loc[study['subject'] == subject]
            subject_data = self.generate_subject(subject_study, param)
            data_list.append(subject_data)
        data = pd.concat(data_list, axis=0, ignore_index=True)
        return data
