import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import sys

def main(argv):

    df = pd.read_csv(argv[1]) # read csv and convert it to data frame
    dt = df.dtypes # check dtype of each variables
    dfs = [] # to save more than 1 data frame
    numcat = 1 # number of categories
    cats = [] # categories

    # separate data into categories (if any)
    if 'cat' in argv:
        headers = list(df.columns.values) # make list of headers

        for i in range(len(dt)):
            if dt[i] == 'O':
                group = df.groupby(headers[i]) # group data by categories found in df[headers[i]]
                dfs = [group.get_group(x) for x in group.groups] # turn split data into list
                numcat = len(dfs)

                cats.append(headers[i])

                for d in dfs:
                    cats.append(pd.Series.unique(d[headers[i]])[0])
                    del d[headers[i]] # delete categorical data
                break

    # default properties of scatterplot matrix
    plotsize = (10,10) # size of plot
    labelsize = 14 # size of axis label
    marker = {'color':'b', 'shape':'o', 'alpha':0.5, 'size':50} # marker properties
    font = {'style':'normal', 'weight':'light','size':8} # font properties

    markers = []

    # properties customization according to arguments in argv
    if 'plot' in argv: # customize plot size
        ind = argv.index('plot')+1
        plotsize = tuple([float(size) for size in argv[ind].split('x')])

    if 'label' in argv: # customize label size
        ind = argv.index('label')+1
        labelsize = int(argv[ind])

    indl = len(argv) # last idx of argv

    for num in range(numcat):
        markers.append(dict.copy(marker))

    if 'marker' in argv: # customize marker properties
        indf = argv.index('marker')+1
        if 'font' in argv:
            indl = argv.index('font')

        for x in range(indf, indl):
            prop = argv[x].split(':')
            if numcat > 1:
                catprop = prop[1].split('|')
                for num in range(numcat):
                    if prop[0] == 'alpha' or prop[0] == 'size':
                        catprop[num] = float(catprop[num])
                    markers[num][prop[0]] = catprop[num]
            else:
                if prop[0] == 'alpha' or prop[0] == 'size':
                    prop[1] = float(prop[1])
                markers[num][prop[0]] = prop[1]

    if 'font' in argv: # customize font properties
        indf = argv.index('font')+1
        indl = len(argv)

        for x in range(indf, indl):
            prop = argv[x].split(':')
            if prop[0] == 'size':
                prop[1] = int(prop[1])
            font[prop[0]] = prop[1]

    # create scatterplot matrix
    if numcat > 1:
        scatterplot_matrix(dfs, plotsize, labelsize, markers, font, cat=True, catname=cats)
    else:
        scatterplot_matrix(df, plotsize, labelsize, markers, font)

# function that create scatterplot matrix using matplotlib
def scatterplot_matrix(dataframe, plotsize, labelsize, marker, font, cat=False, catname = None):
    headers = []
    if cat == False:
        headers = list(dataframe.columns.values)
    else:
        headers = list(dataframe[0].columns.values)

    size = len(headers) # size of matrix (number of column in dataframe)

    # construct empty scatterplot matrix
    fig, axis = plt.subplots(size,size, sharex='col', sharey='row', figsize=plotsize)

    # set font properties according to input
    matplotlib.rc('font', **font)

    # plot the data + set label and marker properties
    # data has to be plotted such that subplots in a columns share x-axis and subplots in a row share y-axis
    plots = []
    legtitle = ''
    if cat == True:
        legtitle = catname[0]
        catname = [catname[c] for c in range(1,len(catname))]

    # create subplot + set marker properties + legend (if any)
    for row in range(0, size):
        for col in range(0, size):

            if cat == False:
                axis[row][col].scatter(dataframe[headers[col]], dataframe[headers[row]], color=marker[0]['color'], marker=marker[0]['shape'], alpha=marker[0]['alpha'], s=marker[0]['size'])
            else:
                for num in range(len(dataframe)):
                    axis[row][col].scatter(dataframe[num][headers[col]], dataframe[num][headers[row]], color=marker[num]['color'], marker=marker[num]['shape'], alpha=marker[num]['alpha'], s=marker[num]['size'])
                    if row == size-1 and col == size-1:
                        # ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
                        plots.append(axis[row][col].scatter(dataframe[num][headers[col]], dataframe[num][headers[row]], color=marker[num]['color'], marker=marker[num]['shape'], alpha=marker[num]['alpha'], s=marker[num]['size']))
                        # plt.legend(plots, catname, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., title=legtitle)
                        plt.figlegend(plots, catname, loc='upper right', ncol = size, title=legtitle)

            # set label only on y-axes of 1st column and x-axes of last row
            if col == 0:
                axis[row][col].set_ylabel(headers[row], size=labelsize)
            if row == size-1:
                axis[row][col].set_xlabel(headers[col], size=labelsize)

    # show the plot
    plt.show()

if __name__ == '__main__':
    main(sys.argv)
