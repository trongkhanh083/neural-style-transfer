#! /bin/bash

mkdir checkpoints
mkdir results

mkdir data
cd data
wget http://www.vlfeat.org/matconvnet/models/beta16/imagenet-vgg-verydeep-19.mat
wget http://images.cocodataset.org/zips/train2014.zip
unzip -q train2014.zip
rm -rf train2014.zip