#! /bin/bash

mkdir checkpoints

mkdir data
cd data
wget http://www.vlfeat.org/matconvnet/models/beta16/imagenet-vgg-verydeep-19.mat
wget http://images.cocodataset.org/zips/val2017.zip
unzip -q val2017.zip
rm -rf val2017.zip