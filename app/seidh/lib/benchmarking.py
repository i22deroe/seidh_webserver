'''

    The benchmarking module for Seidh. Included only as a means of demonstration.

    No warranty of proper working until beta release.

'''


from seidh import *
from auxiliar import *
import timeit
import platform
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

def plot_results(benchmarks,NUM_PROC):
    bar_labels = [NUM_PROC]

    fig = plt.figure(figsize=(10,8))

    # plot bars
    y_pos = numpy.arange(len(benchmarks))
    plt.yticks(y_pos, bar_labels, fontsize=16)
    bars = plt.barh(y_pos, benchmarks,
             align='center', alpha=0.4, color='g')

    # annotation and labels

    for ba,be in zip(bars, benchmarks):
        plt.text(ba.get_width() + 2, ba.get_y() + ba.get_height()/2,
                '{0:.2%}'.format(be/benchmarks[0]),
                ha='center', va='bottom', fontsize=12)

    plt.xlabel('time in seconds', fontsize=14)
    plt.ylabel('number of processes', fontsize=14)
    t = plt.title('Single Vs. multicore approach on Seidh algorithm', fontsize=18)
    plt.ylim([-1,len(benchmarks)+0.5])
    plt.xlim([0,max(benchmarks)*1.1])
    plt.vlines(benchmarks[0], -1, len(benchmarks)+0.5, linestyles='dashed')
    plt.grid()

    fig.savefig(predictions+'MULTIPROC/'+'BENCHMARK_.pdf',format='pdf')

def run_benchmarks(protein,peptide,fasta,NUM_PROC):
	benchmarks = []
	
	for core in NUM_PROC:
	
		benchmarks.append(timeit.Timer('seidh(protein,peptide,fasta,'+core+')','from __main__ import *').timeit(number=1))
	
	return benchmarks