#!/bin/bash

sdf=$1
N=`grep "TOR" $sdf | wc -l`
echo $N

