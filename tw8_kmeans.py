import pandas as pd
import random

class Color(object):
    """
    Adpated from Guttag Fig. 23.2, Example class
    This one is all about 24-bit RGB colors.
    Stores an RGB color and and optional name, knows about distance
    and has a static method to compute a centroid.
    """

    @staticmethod
    def centroid(colors):
        """
        Compute a centroid for a list of Color objects.
        :param colors: list of Colors
        :return:       the average Color of colors
        >>> Colors.centroid([Color(0), Color(0xffffff)])
        #0x7f7f7f: 0x0x7f7f7f

        >>> colors = [Color(0x020202), Color(0x998877), Color(0xbadbad), Color(0xffffff, 'white')]
        >>> Color.centroid(colors)
        Color(0x959989, '#959989')
        """
        rgbs = [color.rgb for color in colors]
        center = rgb_center(rgbs)
        return Color(center)

    def __init__(self, rgb, name=None):
        if name is None:
            name = '#{:06x}'.format(rgb)
        self.name = name
        self.rgb = rgb

    def distance(self, other):
        return rgb_distance(self.rgb, other.rgb)

    def __str__(self):
        return '{}: 0x{:06x}'.format(self.name, self.rgb)
    
    def __repr__(self):
        return "Color(0x{:06x}, '{}')".format(self.rgb, self.name)
    
def rgb_distance(color1, color2):
    """
    Calculate the distance between two colors in the RGB color space.
    :param color1: RGB color value 1
    :param color2: RGB color value 2
    :return: distance between color1 and color2

    >>> color1 = 0x8a3324
    >>> color2 = 0x0000FF
    >>> distance = rgb_distance(color1, color2)
    >>> print(f"Distance between color1 and color2: {distance:.2f}")
    Distance between color1 and color2: 263.83
    """
    red1 = color1 >> 16 & 0xff
    green1 = color1 >> 8 & 0xff
    blue1 = color1 & 0xff

    red2 = color2 >> 16 & 0xff
    green2 = color2 >> 8 & 0xff
    blue2 = color2 & 0xff

    distance = ((red1 - red2) ** 2 + (green1 - green2) ** 2 + (blue1 - blue2) ** 2) ** 0.5
    return distance

def rgb_center(colors):
    """
    Calculate the average color of a sequence of colors in the RGB color space.
    :param colors: sequence of RGB color values
    :return: average color

    >>> colors = [0xFF0000, 0x00FF00, 0x0000FF]
    >>> average_color = rgb_center(colors)
    >>> print(f"Average color: {average_color:#06x}")
    Average color: 0x555555
    """
    total_red = 0
    total_green = 0
    total_blue = 0

    for color in colors:
        total_red += color >> 16 & 0xff
        total_green += color >> 8 & 0xff
        total_blue += color & 0xff

    average_red = total_red // len(colors)
    average_green = total_green // len(colors)
    average_blue = total_blue // len(colors)

    average_color = average_red << 16 | average_green << 8 | average_blue
    return average_color

def get_data(filename):
    """
    Read a CSV file containing color data and return a list of Color objects.
    
    :param filename: the name of the CSV file to read
    :return: a list of Color objects

    >>> get_data('X11colors.csv')[21]
    Color(0x00008b, 'Dark Blue')
    """
    data = pd.read_csv(filename)
    colors = []
    for _, row in data.iterrows():
        hex_value = int(row['Hex'][1:], 16)
        color = Color(hex_value, row['Name'])
        colors.append(color)
    return colors


class Cluster(object):
    """
    Adapted from Guttag Fig. 23.3, except this one is a Cluster of Colors.
    """

    def __init__(self, colors):
        self.colors = colors
        self.centroid = Color.centroid(self.colors)

    def update(self, colors):
        """Assume examples is a non-empty list of Colors
           Replace examples; return amount centroid has changed"""
        old_centroid = self.centroid
        self.colors = colors
        self.centroid = Color.centroid(self.colors)
        return old_centroid.distance(self.centroid)

    def get_centroid(self):
        return self.centroid

    def to_html(self):
        """Produce an html table with the cluster's colors.
        
        >>> colors = [Color(0x020202), Color(0x998877), Color(0xbadbad), Color(0xffffff, 'white')]
        >>> cluster = Cluster(colors)
        >>> html_table = cluster.to_html()
        >>> print(html_table)
        <table><tbody>
        <tr style="background:#020202">
        <td>#020202</td><td>0x020202</td>
        </tr>
        <tr style="background:#998877">
        <td>#998877</td><td>0x998877</td>
        </tr>
        <tr style="background:#badbad">
        <td>#badbad</td><td>0xbadbad</td>
        </tr>
        <tr style="background:#ffffff">
        <td>white</td><td>0xffffff</td>
        </tr>
        </tbody></table>
        """
        color_map = {color.rgb: color for color in self.colors}
        colors = [color_map[color] for color in sorted(color_map)]
        html = ['<table><tbody>']
        for color in self.colors:
            html.append('<tr style="background:#{:06x}">'.format(color.rgb))
            html.append('<td>{}</td><td>0x{:06x}</td>'.format(color.name, color.rgb))
            html.append('</tr>')
        html.append('</tbody></table>')
        return '\n'.join(html)

    def __str__(self):
        color_map = {color.rgb: color for color in self.colors}
        colors = [str(color_map[color]) for color in sorted(color_map)]
        return 'Cluster with centroid {} contains:\n{}'.format(self.centroid, ', '.join(colors))

def kmeans(examples, k, verbose=False):
    """
    Adapted from Guttag, Figure 23.5
    :param examples: list of colors
    :param k: number of clusters to gather
    :param verbose: print out the story as we go if True
    :return: clusters of colors

    >>> colors = get_data('X11colors.csv')
    >>> result = kmeans(colors, k=5, verbose=True)
    # 6, 20, 9 Iterations
    """
    initialCentroids = random.sample(examples, k)
    clusters = []
    for e in initialCentroids:
        clusters.append(Cluster([e]))

    converged = False
    numIterations = 0
    while not converged:
        numIterations += 1
        newClusters = [[] for _ in range(k)]

        for e in examples:
            smallestDistance = e.distance(clusters[0].get_centroid())
            index = 0
            for i in range(1, k):
                distance = e.distance(clusters[i].get_centroid())
                if distance < smallestDistance:
                    smallestDistance = distance
                    index = i
            newClusters[index].append(e)

        for c in newClusters:  
            if len(c) == 0:
                raise ValueError('Empty Cluster')

        converged = True
        for i in range(k):
            if clusters[i].update(newClusters[i]) > 0.0:
                converged = False
        if verbose:
            print('Iteration #' + str(numIterations))
            for c in clusters:
                print(c)
            print('')  
    return clusters

def kmeans_to_html(input_data_file, output_html_file, k, verbose=False):
    """
    Process data file of colors via k-means clustering into an html file
    with a table of the various color clusters.
    :param input_data_file:   colors csv file with columns 'Hex' and 'Name'
    :param output_html_file:  output html file of the resulting clusters
    :param k:                 number of clusters to make
    """
    colors = get_data(input_data_file)
    result = kmeans(colors, k, verbose=verbose)
    tables = [cluster.to_html() for cluster in result]
    html_side_by_side_table(output_html_file, tables)


def html_side_by_side_table(html_filename, contents):
    """
    Make an html table of one row whose cells contain given contents.
    :param html_filename:  output filename
    :param contents:       html fragments to put into each cell
    """
    html = ['<table><tbody><tr>']
    for item in contents:
        html.append('<td>{}</td>'.format(item))
    html.append('</tr></tbody></table>')
    file_contents = '\n'.join(html)
    with open(html_filename, 'w') as f:
        f.write(file_contents)


if __name__ == '__main__':
    kmeans_to_html('X11colors.csv', 'tw8_kmeans.html', k=6, verbose=False)