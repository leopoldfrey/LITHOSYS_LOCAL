#!/bin/sh

#echo KILLING ALL SCRIPTS

cd $(dirname $0)

echo opening IAGOBOT
open ../IAGOBOT/LAUNCHER_IAGOBOT.COMMAND &

echo opening IAGOWIKI
open ../IAGOWIKI/LAUNCHER_IAGOWIKI.COMMAND &

echo opening IAGOGENERATOR
open ../IAGOGENERATOR/LAUNCHER_IAGOGENERATOR.COMMAND &

echo opening IAGOGOTCHI+LITHOSYS+LIMITER
open ./LYTHO_NEW_ENG.maxpat &

echo opening ENG Translator
python3 -W ignore ./GoogleTrans_ENG.py

# echo opening VOCODER LIVE SET
# open ./LITHOLOCAL_VOCODER/LITHOLOCAL_VOCODER.als &

echo Done
