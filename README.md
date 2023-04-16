# Agent-Based Model for COVID-19 spread

This project is a group assignment for the CA4024 "Building Complex Computational Models" module.

Over the course of this assignment, an agent-based model for COVID-19 spread was developed.
We decided to base the model on Dublin City University's campus, with a couple buildings representing the different locations that COVID-19 can spread in. The buildings we chose are as follows: NuBar (DCU's student bar), Gym, Library, Business building, Science building, Computing building.

The model is based on PYCX simulator, providing an easy visualisation of COVID hotspots and infections.
The model has an easy-to-use GUI: the user can change parameters such as probability of COVID, movement speed, as well as mask wearing and vaccination uptake.

The model is designed to be as accurate as possible:

* People are more prone to infections in areas such as the gym or the bar
* People are only infectious 7 days after they contract COVID, and recover 7 days later
* While sick, a portion of people chooses to self-isolate at home, thus not infecting anyone
* Masks and vaccinations lessen the chances of becoming infected
