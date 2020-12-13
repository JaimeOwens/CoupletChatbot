#!/bin/bash
source /root/anaconda3/bin/activate couplet 
chmod 777 /root/Couplet/get_dataset_from_mysql.py
python /root/Couplet/get_dataset_from_mysql.py
if [ $? -eq 0 ]; then
	echo "get_dataset_from_mysql done."
	chmod 777 /root/Couplet/preprocess.py
	echo "preprocess start..."
	python /root/Couplet/preprocess.py --input /root/Couplet/couplet --output /root/Couplet/dataset
	if [ $? -eq 0 ]; then
		echo "train start..."
		chmod 777 /root/Couplet/main.py
		python /root/Couplet/main.py --epochs 100 --batch_size 256 --output /root/Couplet/output --dir /root/Couplet/dataset --logdir /root/Couplet/runs --n_layer 3 --hidden_dim 512
		echo "train done."
	else
		echo "preprocess failed!!!"
	fi
else
	echo "get_dataset_from_sqlite failed!!!"
fi
