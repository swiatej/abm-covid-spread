import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import subprocess
subprocess.call(['pip', 'install', 'networkx'])
import networkx as nx

def plotting_infections_isolations():
  '''
  This function creates a visual representation of the COVID-19 Infections and Isolations CSV file
  '''
  # getting current directory, should be the same where model and the csv file were saved
  current_dir = os.getcwd()
  # create a folder to store plots
  folder_name = 'graphs'
  if not os.path.exists(os.path.join(current_dir, folder_name)):
    os.mkdir('graphs')
  else:
    pass
  # csv file name
  filename = "Isolation_And_Infection_counts.csv"
  full_path = os.path.join(current_dir, filename)
  # get the path to store a generated graph
  store_path = os.path.join(current_dir, 'graphs/' + 'COVID-19_infections_and_isolations_graph.png')
  df = pd.read_csv(full_path)
  np.random.seed(42)
  df['date'] = list(pd.date_range('2022-09-26', periods=len(df), freq='D'))
  # Create a figure and axis object
  fig, ax = plt.subplots(figsize=(12, 6))
  # Plot the number of infected people over time
  ax.plot(df['date'], df['number_infected'], label='Infected')
  # Plot the number of people in isolation over time
  ax.plot(df['date'], df['number_isolating'], label='Isolating')
  # Calculate the percentage of people in isolation
  pct_isolating = df['number_isolating'] / df['number_infected'] * 100
  # Plot the dotted line representing the percentage of people in isolation
  ax.plot(df['date'], pct_isolating, label='% Isolating', linestyle='--')
  # Set x-axis label and title
  ax.set_xlabel('Date')
  ax.set_title('COVID-19 Infections and Isolations')
  # Set y-axis label and legend
  ax.set_ylabel('Number of People')
  ax.legend()
  # Show the plot
  # plt.show()
  plt.savefig(store_path)

def plotting_community_network():
  '''
  This function creates a visual representation of a community network of spreaders and infected people across different faculties
  '''
  # getting current directory, should be the same where model and the csv file were saved
  current_dir = os.getcwd()
  # csv file name
  filename = "Infections_ID.csv"
  full_path = os.path.join(current_dir, filename)
  # get the path to store a generated graph
  store_path = os.path.join(current_dir, 'graphs/' + 'community_network_graph.png')
  df = pd.read_csv(full_path)
  np.random.seed(42)
  num_top_spreaders = int(input("Enter the number of top spreaders you want to be displayed: "))
  df['date'] = list(pd.date_range('2022-09-26', periods=len(df), freq='D'))
  # calculate the number of times each spreader appears in the dataset
  spreader_counts = df['Spreader_id'].value_counts()

  # pick the most common spreaders from user input
  top_spreaders = spreader_counts[:num_top_spreaders].index.tolist()

  # create a graph
  G = nx.Graph()

  # add nodes for each spreader and set their size according to the number of infections they caused
  for spreader in top_spreaders:
      size = spreader_counts[spreader] / 10
      G.add_node(spreader, size=size)

  # add edges between spreaders and infected people
  for _, row in df.iterrows():
      if row['Spreader_id'] in top_spreaders:
          G.add_edge(row['Spreader_id'], row['Infected_id'])

  # add node color based on faculty
  faculty_colors = {'computing': 'red', 'science': 'blue', 'business': 'green'}
  # create a list of node colors based on the faculty of the spreader
  node_color_map = []
  for node in G.nodes:
      if node in df['Spreader_id'].values:
          color = faculty_colors.get(df.loc[df['Spreader_id']==node, 'Spreader_faculty'].iloc[0], 'gray')
      else:
          color = 'gray'
      node_color_map.append(color)

  # create a list of node sizes based on the degree of each node
  node_size = [deg*100 for node, deg in G.degree()]

  # check that the node size list has the same length as the node color list
  if len(node_size) != len(node_color_map):
      raise ValueError("node_size and node_color_map must have the same length")

  # draw the graph
  pos = nx.spring_layout(G, k=0.3)
  nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color_map)
  nx.draw_networkx_edges(G, pos, alpha=0.5)
  nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')

  # add a legend showing what the colors represent
  legend = []
  for faculty, color in faculty_colors.items():
      legend.append(plt.Line2D([], [], color=color, marker='o', markersize=5, label=faculty))
  plt.legend(handles=legend)

  # set the axis limits and show the graph
  plt.xlim([-1.2,1.3])
  plt.ylim([-1.2,1.3])
  plt.axis('off')
  plt.title('Spreaders and Infected People Community Detection')
  #plt.show()
  # Save the graph as a PNG file
  plt.savefig(store_path)

if __name__ == '__main__':
	print('Creating visual representation of the model"s performance')
	plotting_infections_isolations()
	plotting_community_network()
	print('Created. Graphs are contained in the folder graphs.')

