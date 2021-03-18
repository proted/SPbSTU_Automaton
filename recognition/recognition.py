#!/usr/bin/python3
import sys
import wave
import shutil
import os

from convert import conv_mp3_to_wav
from recognize import recognize 
from infile import save_in_file
from downsample import reset_sample
from merge import merge
from direalize import direalize


def sample_check(path):
	sample_list = [8000, 16000, 32000, 48000]
	#sample_list = [16000]
	wf = wave.open(path, "rb")
	sample = wf.getframerate()
	wf.close()
	tmp = sample
	new_sample = 0

	#Если частота не подходит для передачи в следующий модуль, то она изменяется на ближаюшую
	if sample not in sample_list:
		for i in sample_list:
			if abs(sample-i) < tmp:
				new_sample = i
				tmp = abs(sample-i)		
		
		return reset_sample(path,new_sample)
	return 0
	

def recognition(path):
	audio_mp3 = path
	name = audio_mp3.split('/')[-1]
	name = name.replace('.mp3','')

	audio_wav = conv_mp3_to_wav(str(audio_mp3))
	result = recognize(str(audio_wav))
	'''
	Сохранение результатов перевода в папку text/
	'''

	out_r = "text/" + name +"1.txt"
	save_in_file(result,out_r)

	'''
	Код ниже нужен лишь для перевода в нужную частоту, если вдруг исходная не подходит для диаризации
	'''

	new_wav = sample_check(audio_wav)
	if(new_wav != 0):
		audio_wav = new_wav
		
	
	
	# Задумка в том, чтобы сохранять результаты в текстовик, которы будет лежать в папке text
	# Сохранение результатов перевода в папку text/
	
	
	
	#str(audio_wav) - путь к записи, если нужен формат mp3, то можно заменить на audio_mp3
	#out_d путь по которому нужно сохранить результат
	out_d = "text/" + name +"2.txt"
	direalize(str(audio_wav), out_d)
	
	
	result_src = merge(out_r,out_d)
	
	result_dst = "done/" + name + ".txt"
	open(result_dst, 'a')
	shutil.copyfile(result_src, result_dst)
	os.remove(result_src)
	
	#Удаление промежуточных результатов
	os.remove(out_r)
	os.remove(out_d)








	
