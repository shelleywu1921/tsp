#!/bin/bash
for i in `seq 100`; do
  python hanle_to_teeth7.1.py $i  >&! job_$i &
done

