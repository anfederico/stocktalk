from bokeh.layouts  import row, column
from bokeh.plotting import figure, curdoc
from bokeh.models   import LinearAxis, Range1d
from bokeh.driving  import count
import random

def readUpdates(filename):
	updates = {}
	with open(filename, 'r') as infile:
		for line in infile:
			l = line.strip('\n').split(',')
			volume = int(l[1])
			sentiment = 0
			if l[2] != 'N/A': sentiment = float(l[2])
			updates[l[0]] = (volume, sentiment)
	return updates

def extrapolate(tweets):
	return tweets*99+random.randint(0,99)

def getPlot(title):
	p = figure(plot_height=200, plot_width=400, min_border=40, toolbar_location=None, title=title)
	p.background_fill_color = "#515052"          # Background color
	p.title.text_color = "#333138"               # Title color
	p.title.text_font = "helvetica"              # Title font
	p.x_range.follow = "end"                     # Only show most recent window of data
	p.x_range.follow_interval = 60               # Moving window size
	p.xaxis.major_tick_line_color = None         # Turn off x-axis major ticks
	p.xaxis.minor_tick_line_color = None         # Turn off x-axis minor ticks
	p.yaxis.major_tick_line_color = None         # Turn off y-axis major ticks
	p.yaxis.minor_tick_line_color = None         # Turn off y-axis minor ticks
	p.xgrid.grid_line_alpha = 0                  # Hide X-Axis grid
	p.ygrid.grid_line_alpha = 0                  # Hide Y-Axis grid
	p.xaxis.major_label_text_color = "#333138"   # X-Axis color
	p.yaxis.major_label_text_color = "#333138"   # Y-Axis color
	p.extra_y_ranges = {"sentiment": Range1d(start=-1, end=1)}
	p.add_layout(LinearAxis(y_range_name="sentiment", major_tick_line_color = None, minor_tick_line_color = None), 'right')
	return p

def visualize(coins, seconds, path):
	milliseconds = seconds*1000
	
	plots = []
	for coin in coins:
		plot = []
		plot.append(getPlot(coin))
		plot.append(plot[0].line([], [], line_alpha = 0.7, color="#C4D7F2", line_width=2))
		plot.append(plot[1].data_source)
		plot.append(plot[0].line([], [], line_alpha = 0.5, color="#FFFFFA", line_width=1, y_range_name="sentiment"))
		plot.append(plot[3].data_source)
		plots.append(plot)

	@count()
	def update(t):

		#Grab updates
		updates = readUpdates('%supdates.txt' % path)

		# Apply updates
		for i, plot in enumerate(plots):
			plot[2].data['x'].append(t) 
			plot[2].data['y'].append(extrapolate(updates[coins[i]][0]))
			plot[4].data['x'].append(t) 
			plot[4].data['y'].append(updates[coins[i]][1])

		# Trigger updates
		for plot in plots:
			plot[2].trigger('data', plot[2].data, plot[2].data)
			plot[4].trigger('data', plot[4].data, plot[4].data)

	rows = []
	for i in range(0, len(plots), 2):
		try: 
			rows.append(row(plots[i][0], plots[i+1][0]))
		except IndexError:
			rows.append(row(plots[i][0]))

	root = column([r for r in rows])
	curdoc().add_root(root)
	curdoc().add_periodic_callback(update, milliseconds)