python -m bleurt.score_files \
  -reference_file=./references/GQA_ref.txt \
  -candidate_file=./candidates/GQA_can.txt \
  -bleurt_checkpoint=../../BLEURT-20 \
  -score_file=./score_file/