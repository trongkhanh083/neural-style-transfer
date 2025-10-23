#! /bin/bash

mkdir checkpoints
mkdir results

mkdir data
cd data
wget http://www.vlfeat.org/matconvnet/models/beta16/imagenet-vgg-verydeep-19.mat
wget http://images.cocodataset.org/zips/val2014.zip
unzip -q val2014.zip
rm -rf val2014.zip