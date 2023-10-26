import matplotlib.pyplot as plt
from modules.environment.reader import TrackSequenceReader

reader = TrackSequenceReader("src/sdc/databases/tracks.json")
tracks = reader.track_sequence

# print(plt.style.available)
plt.style.use("fast")
['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-v0_8', 'seaborn-v0_8-bright', 'seaborn-v0_8-colorblind', 'seaborn-v0_8-dark', 'seaborn-v0_8-dark-palette', 'seaborn-v0_8-darkgrid', 'seaborn-v0_8-deep', 'seaborn-v0_8-muted', 'seaborn-v0_8-notebook', 'seaborn-v0_8-paper', 'seaborn-v0_8-pastel', 'seaborn-v0_8-poster', 'seaborn-v0_8-talk', 'seaborn-v0_8-ticks', 'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid', 'tableau-colorblind10']


for track in tracks:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    track.plot(ax)

    # turn off the axis planes
    ax.set_axis_off()

    plt.show()
