import tkinter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np
from hierarchy import linkage
from colors import get_color
from scipy.cluster.hierarchy import dendrogram
import sys

np.random.seed(2)

rx = np.array([])  # random input
ry = np.array([])  # random input
test_x = [1, 2, 4, 7, 8]  # dummy data
test_y = [1, 1, 1, 1, 1]  # dummy data
x = []  # user input
y = []  # user input
cx = []  # user + rand input
cy = []  # user + rand input
link_mat = []
centroids = []
root = tkinter.Tk()
root.wm_title("Bottom-Up Clustering")

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def onclick(event):
    print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' % (event.button, event.x, event.y, event.xdata, event.ydata))
    x.append(event.xdata)
    y.append(event.ydata)
    plt.scatter(event.xdata, event.ydata, s=30, c='red')
    canvas.draw()


bind_id = canvas.mpl_connect('button_press_event', onclick)


def _quit():
    root.quit()
    root.destroy()


def _rand_scatter():
    global rx
    global ry
    rand_x = np.random.rand(10) * 10
    rand_y = np.random.rand(10) * 10
    rx = np.concatenate((rx, rand_x))
    ry = np.concatenate((ry, rand_y))
    plt.scatter(rand_x, rand_y, s=30, c='red')
    canvas.draw()


clusters = []
i = 0


def _show():
    global i
    if i >= len(clusters):
        return
    x_list = []
    y_list = []
    for point in clusters[i]:
        x_list.append(cx[point])
        y_list.append(cy[point])
    col = get_color(len(x_list))
    plt.scatter(x_list, y_list, s=50, c=col)
    if centroids:
        plt.scatter([centroids[i][0]], [centroids[i][1]], facecolors='none', edgecolors=col)
        if i > 0:
            plt.scatter([centroids[i - 1][0]], [centroids[i - 1][1]], c=[(1, 1, 1)], alpha=1, s=70)
    canvas.draw()
    i += 1


dendrogram_button = 0
show_button = 0


def _run():
    global dendrogram_button
    global show_button
    global cx
    global cy
    global clusters
    global link_mat
    global centroids
    run_button.pack_forget()
    random_button.pack_forget()
    cx = np.concatenate((x, rx))
    cy = np.concatenate((y, ry))
    if sys.argv[1] not in ["ward", "single", "complete", "centroids", "average"] and sys.argv[2] not in ["euclidean", "chebyshev"]:
        print("Method or metric chosen is wrong!")
        root.quit()
        root.destroy()
        return
    clusters, link_mat, centroids = linkage(cx, cy, method=sys.argv[1], metric=sys.argv[2])
    # plt.scatter([i[0] for i in centroids], [i[1] for i in centroids], facecolors='none', edgecolors='r')
    link_mat = np.array(link_mat)
    show_button = tkinter.Button(master=root, bd=3, text="Show", command=_show, pady=10, padx=25)
    show_button.pack(side=tkinter.LEFT)
    dendrogram_button = tkinter.Button(master=root, bd=3, text="Dendrogram", command=_plot_dendrogram, pady=10, padx=25)
    dendrogram_button.pack(side=tkinter.LEFT)
    canvas.mpl_disconnect(bind_id)


def _plot_dendrogram():
    fig.clf()
    canvas.draw()
    dendrogram(link_mat)
    canvas.draw()
    dendrogram_button.pack_forget()
    show_button.pack_forget()


quit_button = tkinter.Button(master=root, bd=3, text="Quit", command=_quit, fg="red", pady=10, padx=25)
quit_button.pack(side=tkinter.LEFT)

run_button = tkinter.Button(master=root, bd=3, text="Run", command=_run, fg="green", pady=10, padx=25)
run_button.pack(side=tkinter.LEFT)

random_button = tkinter.Button(master=root, bd=3, text="Random (10)", command=_rand_scatter, pady=10, padx=25)
random_button.pack(side=tkinter.LEFT)

tkinter.mainloop()
