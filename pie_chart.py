import matplotlib.pyplot as plt

def make_piechart(labels, sizes):
    plt.pie(sizes, labels=labels)
    plt.savefig("save as pie.png")