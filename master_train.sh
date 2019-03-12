#!/usr/bin/env bash
python monolithic_converter_train.py
python pose_interpolator_train.py
python masks_train.py
python train.py