import matplotlib.pyplot as plt

def make_piechart(labels, sizes):
    plt.cla()
    plt.pie(sizes)
    plt.legend(labels=labels, loc="upper left")
    plt.savefig("pie.png")