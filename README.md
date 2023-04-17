# Agent-Based Model for COVID-19 spread

This project is a group assignment for the CA4024 "Building Complex Computational Models" module.
---

## How to run model


The main python code is stored in [**virus_spread.py**](virus_spread.py) file and the code for a 2D graphical display of the model's performance is presented in [**pycxsimulator.py**](pycxsimulator.py) file.

The user should be able to run the model by cloning this repository, and running "python virus_spread.py" in their terminal.

It is possible to change parameters such as population size, movement speed, probability of contracting COVID, probability of wearing masks / vaccinations (or getting rid of them altogether).

The *virus_spread.py* script outputs two .csv files once it has finished running:
* [**Infections_ID.csv**](Infections_ID.csv) - Dated counts of isolating people and people currently infected
* [**Isolation_And_Infection_Counts.csv**](Isolation_And_Infection_Counts.csv) - Time of new infection, along with student id and faculty name of COVID spreader, and student id and faculty name of newly infected

The script [**visualisation.py**](visualisation.py) takes in the Infections_ID and Isolation_And_Infection_Counts csv's and creates plots. These can be accessed in the [**graphs folder**](graphs).
The plot repreenting Isolation_And_Infection_Counts is called [**COVID-19_infections_and_isolations_graph.png**](graphs/COVID-19_infections_and_isolations_graph.png) and the plot representing Infections_ID is called [**community_network_graph.png**](graphs/community_network_graph.png)

## Model overview

Over the course of this assignment, an agent-based model for COVID-19 spread was developed.
We decided to base the model on Dublin City University's campus, with a couple buildings representing the different locations that COVID-19 can spread in. The buildings we chose are as follows: NuBar (DCU's student bar), Gym, Library, Business building, Science building, Computing building.

The model is based on the PYCX simulator, providing an easy visualisation of COVID hotspots and infections.
The model has an easy-to-use GUI: the user can change parameters such as probability of COVID, movement speed, as well as mask wearing and vaccination uptake.

The model is designed to be as accurate as possible:

* People are more prone to infections in areas such as the gym or the bar
* People are only infectious on days 6-13 of their sickness, and recover on day 14
* While sick, a portion of people chooses to self-isolate at home, thus not infecting anyone
* Masks and vaccinations lessen the chances of becoming infected
* People are not able to transmit COVID when they are at home


