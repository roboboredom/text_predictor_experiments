#!/bin/bash

echo "[START SCRIPT] Available text \".txt\" files to build the model with: "
ls -l -h training_data/

echo "[START SCRIPT] Starting \"bigram_text_predictor.py\"... "
python3 bigram_text_predictor.py

read -rsp $'[START SCRIPT] Program stopped. Press enter to exit start script...\n'