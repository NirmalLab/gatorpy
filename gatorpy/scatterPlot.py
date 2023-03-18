# -*- coding: utf-8 -*-
#Created on Fri Mar 17 10:00:18 2023
#@author: Ajit Johnson Nirmal
#Plotting function to visualize postive cells

"""
!!! abstract "Short Description"
    The scatterPlot function can be used to create scatter plots of single-cell spatial data. 
    This function can be used to visualize the spatial distribution of positive 
    cells for a given marker, providing a quick and intuitive way to view the final predictions.

## Function
"""

# Libs
import anndata as ad
import pathlib
import matplotlib.pyplot as plt
import argparse

# Function
def scatterPlot (gatorObject, 
                 markers=None, 
                 gatorOutput='gatorOutput',
                 x_coordinate='X_centroid',
                 y_coordinate='Y_centroid',
                 poscellsColor='#78290f',
                 negcellsColor='#e5e5e5',
                 s=None,
                 ncols=5,
                 alpha=1,
                 dpi=200,
                 figsize=(5, 5),
                 outputDir=None,
                 outputFileName='gatorPlot.png',
                 **kwargs):
    """
Parameters:
    gatorObject (anndata):
        Pass the `gatorObject` loaded into memory or a path to the `gatorObject` 
        file (.h5ad).
        
    markers (str or list of str, optional): 
        The name(s) of the markers to plot. If not provided, all markers will be plotted.
        
    gatorOutput (str, optional): 
        The label underwhich the Gator output is stored within the object.
        
    x_coordinate (str, optional):
        The column name in `single-cell spatial table` that records the
        X coordinates for each cell. 

    y_coordinate (str, optional):
        The column name in `single-cell spatial table` that records the
        Y coordinates for each cell.
        
    poscellsColor (str, optional): 
        The color of positive cells.
        
    negcellsColor (str, optional): 
        The color of negative cells. 
        
    s (float, optional): 
        The size of the markers.
        
    ncols (int, optional): 
        The number of columns in the final plot when multiple makers are plotted. 
        
    alpha (float, optional): 
        The alpha value of the points (controls opacity).
        
    dpi (int, optional): 
        The DPI of the figure.
        
    figsize (tuple, optional): 
        The size of the figure.
        
    outputDir (str, optional): 
        The directory to save the output plot. 
        
    outputFileName (str, optional): 
        The name of the output file. Use desired file format as 
        suffix (e.g. `.png` pr `.pdf`)

    **kwargs (keyword parameters):
        Additional arguments to pass to the `matplotlib.scatter` function.


Returns:
    Plot (image):
        If `outputDir` is provided the plot will saved within the
        provided outputDir.

Example:

        ```python
        gatorObject = '/Users/aj/Desktop/gatorExampleData/GATOR/gatorOutput/exampleImage_gatorPredict.ome.h5ad'
        # Plot image to console
        ga.scatterPlot (gatorObject, 
                         markers=['ECAD', 'CD8A'], 
                         poscellsColor='#78290f',
                         negcellsColor='#e5e5e5',
                         s=0.1,
                         ncols=1,
                         dpi=200,
                         figsize=(4, 10),
                         outputDir=None,
                         outputFileName='gatorplot.png')
        
        # Same function if the user wants to run it via Command Line Interface
        python scatterPlot.py --gatorObject /Users/aj/Desktop/gatorExampleData/GATOR/gatorOutput/exampleImage_gatorPredict.ome.h5ad \
                            --markers ECAD CD8A \
                            --outputDir /Users/aj/Desktop/gatorExampleData/GATOR
        
    """
    
    # Load the andata object
    if isinstance(gatorObject, str):
        adata = ad.read(gatorObject)
    else:
        adata = gatorObject.copy()
        
    # break the function if gatorOutput is not detectable
    def check_key_exists(dictionary, key):
        try:
            # Check if the key exists in the dictionary
            value = dictionary[key]
        except KeyError:
            # Return an error if the key does not exist
            return "Error: " + str(gatorOutput) + " does not exist, please check!"
    # Test
    check_key_exists(dictionary=adata.uns, key=gatorOutput)

    
    # convert marter to list
    if markers is None:
        markers = list(adata.uns[gatorOutput].columns)
    if isinstance (markers, str):
        markers = [markers]
        
    # identify the x and y coordinates
    x = adata.obs[x_coordinate]
    y = adata.obs[y_coordinate]
    
    # subset the gatorOutput with the requested markers
    subset = adata.uns[gatorOutput][markers]
    # get the list of columns to plot
    cols_to_plot = subset.columns
    
    # identify the number of columns to plot
    ncols = min(ncols, len(cols_to_plot))
    
    # calculate the number of rows needed for the subplot
    nrows = (len(cols_to_plot) - 1) // ncols + 1
    
    # resolve figsize
    figsize = (figsize[0], figsize[1]*nrows)
    
    # Estimate point size
    if s is None:
        s = (100000 / adata.shape[0]) / len(cols_to_plot)
        
    # FIIGURE
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, dpi=dpi)
    for i, col in enumerate(cols_to_plot):
        # get the classes for the current column
        classes = list(subset[col])
        
        # get the current subplot axes
        if nrows==1 or ncols==1:
            ax = axs[i]
        else:
            ax = axs[i // ncols, i % ncols]
        
        # set the title of the subplot to the current column name
        ax.set_title(col)
        
        # plot the 'neg' points with a small size
        neg_x = [x[j] for j in range(len(classes)) if classes[j] == 'neg']
        neg_y = [y[j] for j in range(len(classes)) if classes[j] == 'neg']
        ax.scatter(x=neg_x, y=neg_y, c=negcellsColor, s=s, alpha=alpha, **kwargs)
    
        # plot the 'pos' points on top of the 'neg' points with a larger size
        pos_x = [x[j] for j in range(len(classes)) if classes[j] == 'pos']
        pos_y = [y[j] for j in range(len(classes)) if classes[j] == 'pos']
        ax.scatter(x=pos_x, y=pos_y, c=poscellsColor, s=s, alpha=alpha, **kwargs)
    
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_xticks([])
        ax.set_yticks([])
        
    # remove any unused subplots
    for i in range(len(cols_to_plot), nrows * ncols):
        fig.delaxes(axs[i // ncols, i % ncols])

    plt.tight_layout()
    plt.show()

    # save figure
    if outputDir is not None:
        plt.savefig(pathlib.Path(outputDir) / outputFileName)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a scatter plot of cells from a Gator object.')
    parser.add_argument('--gatorObject', type=str, help='Path to the gatorObject file or name of the variable in memory.')
    parser.add_argument('--markers', type=str, nargs='+', default=None, help='The name(s) of the markers to plot. If not provided, all markers will be plotted.')
    parser.add_argument('--gatorOutput', type=str, default='gatorOutput', help='The label underwhich the Gator output is stored within the object.')
    parser.add_argument('--x_coordinate', type=str, default='X_centroid', help='The column name in `single-cell spatial table` that records the X coordinates for each cell.')
    parser.add_argument('--y_coordinate', type=str, default='Y_centroid', help='The column name in `single-cell spatial table` that records the Y coordinates for each cell.')
    parser.add_argument('--poscellsColor', type=str, default='#78290f', help='The color of positive cells.')
    parser.add_argument('--negcellsColor', type=str, default='#e5e5e5', help='The color of negative cells.')
    parser.add_argument('--s', type=float, default=None, help='The size of the markers.')
    parser.add_argument('--ncols', type=int, default=5, help='The number of columns in the final plot when multiple markers are plotted.')
    parser.add_argument('--alpha', type=float, default=1, help='The alpha value of the points (controls opacity).')
    parser.add_argument('--dpi', type=int, default=200, help='The DPI of the figure.')
    parser.add_argument('--figsize', type=float, nargs=2, default=[5, 5], help='The size of the figure.')
    parser.add_argument('--outputDir', type=str, default=None, help='The directory to save the output plot.')
    parser.add_argument('--outputFileName', type=str, default='gatorPlot.png', help='The name of the output file. Use desired file format as suffix (e.g. `.png` or `.pdf`).')
    args = parser.parse_args()
    
    # Call the function with the argparse arguments as parameters
    scatterPlot(gatorObject=args.gatorObject,
                markers=args.markers,
                gatorOutput=args.gatorOutput,
                x_coordinate=args.x_coordinate,
                y_coordinate=args.y_coordinate,
                poscellsColor=args.poscellsColor,
                negcellsColor=args.negcellsColor,
                s=args.s,
                ncols=args.ncols,
                alpha=args.alpha,
                dpi=args.dpi,
                figsize=tuple(args.figsize),
                outputDir=args.outputDir,
                outputFileName=args.outputFileName)

