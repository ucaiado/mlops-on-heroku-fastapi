#!/bin/sh

source activate mlops_exercise
autopep8 --in-place --aggressive --aggressive $1
pylint $1
