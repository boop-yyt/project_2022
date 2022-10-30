cat output-2.txt | grep -P "^T" | cut -f 2- > ref.txt
cat output-2.txt | grep -P "^G" | cut -f 3- > hyp.txt
sacrebleu ref.txt -i hyp.txt -w 2 -b