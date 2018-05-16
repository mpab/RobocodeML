#!/usr/bin/env python3

import pandas as pd
import cfg


def targets_info(fp, target):
    data = pd.read_csv(fp)
    print('targets information from: {}'.format(fp))

    print(target)
    print('val  count')
    print(data[target].value_counts(ascending=True))

    z_count = 0
    nz_count = 0
    idx = 0
    for cnt in data[target].value_counts(ascending=True):
        if idx == 0:
            z_count = cnt
        else:
            nz_count = nz_count + cnt
        idx = idx + 1

    print('{}={}%'.format(target, (nz_count / (nz_count + z_count))*100))

    print()


def test_targets_info():
    obs_fp = cfg.ensure_fp(cfg.observations_root, cfg.observations)
    targets_info(obs_fp, 'wall_collisions')

    test_obs_fp = cfg.observations_root + 'minimise_wall_collisions.csv'
    targets_info(test_obs_fp, 'wall_collisions')


if __name__ == "__main__":
    test_targets_info()
