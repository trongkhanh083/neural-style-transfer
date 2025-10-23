#! /bin/bash

mkdir checkpoints
mkdir results

mkdir data
cd data
wget http://www.vlfeat.org/matconvnet/models/beta16/imagenet-vgg-verydeep-19.mat
wget http://images.cocodataset.org/zips/test2015.zip
unzip -q test2015.zip
rm -rf test2015.zip