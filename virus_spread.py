import pycxsimulator
from pylab import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from random import random,choice

population = 1000 # human population
p_covid = 0.1 # probability that person has covid

# set parameters for movement and probability threshold
m = 0.13


class nubar:
    def __init__(self):
        self.x = 0.77
        self.y = 0.7

class business:
    def __init__(self):
        self.x = 0.68
        self.y = 0.17
class computing:
    def __init__(self):
        self.x = 0.37
        self.y = 0.18
class science:
    def __init__(self):
        self.x = 0.13
        self.y = 0.2
class library:
    def __init__(self):
        self.x = 0.11
        self.y = 0.6
class gym:
    def __init__(self):
        self.x = 0.3
        self.y = 0.86

# create human class
class human:
    def __init__(self, i):
        self.x = random()
        self.y = random()
        self.home_x = 0.93
        self.home_y = 0.18
        self.covid_status = 'infected' if random() < p_covid else 'normal'
        self.status = choice(['science','business','computing'])
        self.evening_status = choice(['gym','library','nubar'])
        self.weekend_status = choice(['gym','library','nubar'])
        self.time_at_gym = randint(10,15) # for weekends
        self.days_infected = 0
        self.mask_wearing = choice([0,1])
        self.vaccinations = choice([0,1])
        self.covid_prob = 0.001
        self.quarantine = 0
        self.infection_loc = ""
        self.infection_time = ""
        self.id = 0


    def change_status(self):
        # allow students to change status for weekend
        self.weekend_status = choice(['gym','library','nubar'])


    def eveningstatus(self):
        prob = random()
        # every day is a new evening status
        if self.status == 'science':
            if prob > 0.5:
                self.evening_status = 'library'
            if prob < 0.4:
                self.evening_status = 'gym'
            if prob >= 0.4 and prob <= 0.5:
                self.evening_status = 'nubar'
        if self.status == 'business':
            if prob > 0.5:
                self.evening_status = 'nubar'
            if prob < 0.35:
                self.evening_status = 'gym'
            if prob >= 0.35 and prob <= 0.5:
                self.evening_status = 'library'
        if self.status == 'computing':
            self.evening_status = 'library' if prob >= 0.5 else 'gym'

    def move_wknd(self, m, time):
        if self.weekend_status == 'gym' and time > 10 and time < 17:
            try:
                x_move = (gym.x - self.x) / abs(gym.x - self.x)
                y_move = (gym.y- self.y) / abs(gym.y - self.y)

            except ZeroDivisionError:
                x_move, y_move = 0, 0
                pass
            if x_move==0:
                self.x += uniform(-2*m, 2*m)
            else:
                self.x += x_move*m
            if y_move==0:
                self.y += uniform(-2*m, 2*m)
            else:
                self.y += y_move*m

        elif self.weekend_status == 'library' and time > 10 and time <= 17:

            try:
                x_move = (library.x - self.x) / abs(library.x - self.x)
                y_move = (library.y- self.y) / abs(library.y - self.y)

            except ZeroDivisionError:
                x_move, y_move = 0, 0
                pass
            if x_move==0:
                self.x += uniform(-2*m, 2*m)
            else:
                self.x += x_move*m
            if y_move==0:
                self.y += uniform(-2*m, 2*m)
            else:
                self.y += y_move*m

        elif self.weekend_status == 'nubar' and time > 18 and time <= 24:
            try:
                x_move = (nubar.x - self.x) / abs(nubar.x - self.x)
                y_move = (nubar.y- self.y) / abs(nubar.y - self.y)

            except ZeroDivisionError:
                x_move, y_move = 0, 0
                pass
            if x_move==0:
                self.x += uniform(-2*m, 2*m)
            else:
                self.x += x_move*m
            if y_move==0:
                self.y += uniform(-2*m, 2*m)
            else:
                self.y += y_move*m

        else:
            try:
                x_move = (self.home_x - self.x) / abs(self.home_x - self.x)
                y_move = (self.home_y - self.y) / abs(self.home_y - self.y)
            except ZeroDivisionError:
                x_move, y_move = 0, 0
                pass

            if x_move==0:
                self.x += uniform(-2*m, 2*m)
            else:
                self.x += x_move*m
            if y_move==0:
                self.y += uniform(-2*m, 2*m)
            else:
                self.y += y_move*m
        # correct x and y values if any individuals have been moved off the map
        self.x = 1 if self.x > 1 else 0 if self.x < 0 else self.x
        self.y = 1 if self.y > 1 else 0 if self.y < 0 else self.y


    def move(self, m, time):
        # send students to university and back home
        if time >= 8 and time < 18:
            if self.status == 'business':
                #select portion of student to move towards university
                # business students go to classes 50% of the time
                if random() > 0.5:
                    try:
                        x_move = (business.x - self.x) / abs(business.x - self.x)
                        y_move = (business.y - self.y) / abs(business.y - self.y)
                    except ZeroDivisionError:
                        x_move, y_move = 0, 0
                        pass
                else:
                    try:
                        x_move = (self.home_x - self.x) / abs(self.home_x - self.x)
                        y_move = (self.home_y - self.y) / abs(self.home_y - self.y)
                    except ZeroDivisionError:
                        x_move, y_move = 0, 0
                        pass

            elif self.status == 'science':
                #science students always go to classes
                try:
                    x_move = (science.x - self.x) / abs(science.x - self.x)
                    y_move = (science.y - self.y) / abs(science.y - self.y)
                except ZeroDivisionError:
                    x_move, y_move = 0, 0
                    pass


            elif self.status == 'computing':
                #select portion of student to move towards university
                if random() > 0.3:
                    try:
                        x_move = (computing.x - self.x) / abs(computing.x - self.x)
                        y_move = (computing.y - self.y) / abs(computing.y - self.y)
                    except ZeroDivisionError:
                        x_move, y_move = 0, 0
                        pass
                else:
                    try:
                        x_move = (self.home_x - self.x) / abs(self.home_x - self.x)
                        y_move = (self.home_y - self.y) / abs(self.home_y - self.y)
                    except ZeroDivisionError:
                        x_move, y_move = 0, 0
                        pass
            if x_move==0:
                self.x += uniform(-2*m, 2*m)
            else:
                self.x += x_move*m
            if y_move==0:
                self.y += uniform(-2*m, 2*m)
            else:
                self.y += y_move*m
        elif time >= 18 and time <= 24:
            if self.evening_status == 'library':
                try:
                    x_move = (library.x - self.x) / abs(library.x - self.x)
                    y_move = (library.y- self.y) / abs(library.y - self.y)
                except ZeroDivisionError:
                    x_move, y_move = 0, 0
                    pass
            elif self.evening_status == 'gym' and time < 23:
                try:
                    x_move = (gym.x - self.x) / abs(gym.x - self.x)
                    y_move = (gym.y- self.y) / abs(gym.y - self.y)

                except ZeroDivisionError:
                    x_move, y_move = 0, 0
                    pass

            elif self.evening_status == 'nubar':
                try:
                    x_move = (nubar.x - self.x) / abs(nubar.x - self.x)
                    y_move = (nubar.y- self.y) / abs(nubar.y - self.y)

                except ZeroDivisionError:
                    x_move, y_move = 0, 0
                    pass
            else:
                try:
                    x_move = (self.home_x - self.x) / abs(self.home_x - self.x)
                    y_move = (self.home_y - self.y) / abs(self.home_y - self.y)
                except ZeroDivisionError:
                    x_move, y_move = 0, 0
                    pass
            if x_move==0:
                self.x += uniform(-2*m, 2*m)
            else:
                self.x += x_move*m
            if y_move==0:
                self.y += uniform(-2*m, 2*m)
            else:
                self.y += y_move*m
        else:
            try:
                x_move = (self.home_x - self.x) / abs(self.home_x - self.x)
                y_move = (self.home_y - self.y) / abs(self.home_y - self.y)
            except ZeroDivisionError:
                x_move, y_move = 0, 0
                pass
            if x_move==0:
                self.x += uniform(-2*m, 2*m)
            else:
                self.x += x_move*m
            if y_move==0:
                self.y += uniform(-2*m, 2*m)
            else:
                self.y += y_move*m
        # correct x and y values if any individuals have been moved off the map
        self.x = 1 if self.x > 1 else 0 if self.x < 0 else self.x
        self.y = 1 if self.y > 1 else 0 if self.y < 0 else self.y


    def infection(self):
        global hours, day, week_count,df
        if self.x == self.home_x:
            # if at home, they can't get infected
            return
        if self.covid_status == 'infected':
            return
        temp_covid_prob = self.covid_prob
        # detecting collision and simulating covid catching.
        #increase probability for gym and nubar
        if self.x == gym.x and self.y == gym.y: # if in the gym
            temp_covid_prob = self.covid_prob * 5
        if self.x == nubar.x and self.y == nubar.y: # if in nubar
            temp_covid_prob = self.covid_prob * 4
        if self.x == science.x and self.y == science.y:
            temp_covid_prob = self.covid_prob * 2
        if self.x == business.x and self.y == business.y:
            temp_covid_prob = self.covid_prob * 2
        if self.x == computing.x and self.y == computing.y:
            temp_covid_prob = self.covid_prob * 2
        if self.x == library.x and self.y == library.y:
            temp_covid_prob = self.covid_prob * 2


        temp = [h for h in humans if h.covid_status == 'infected' and h.quarantine == 0 and h.days_infected >=6 and h.days_infected <= 13]
        if len(temp) == 0:
            return
        # find closest human
        hum_id, distance, faculty = closest_human(self.x, self.y, temp)
        if distance < 0.001:
            self.covid_status = 'infected' if random() < temp_covid_prob else self.covid_status
            if self.covid_status == 'infected':
                self.infection_loc = str(self.x) + ", " + str(self.y)
                t = "Week " + str(week_count) + " " + day + " "+str(hours)
                self.infection_time = t
                df2 = pd.DataFrame([[hum_id,faculty,self.id,self.status,self.infection_time]], columns=[
                                   'Spreader_id', 'Spreader_faculty','Infected_id','Infected_faculty','Time_of_infection'])
                df1 = df
                df = pd.concat([df1,df2])



def closest_human(x, y, humans):
    point = np.array((x, y))
    human_ids = np.array([h.id for h in humans])
    human_faculties = np.array([h.status for h in humans])
    humans = np.array([[h.x, h.y] for h in humans])
    distance = np.sum((humans - point)**2, axis=1)

    return human_ids[np.argmin(distance)], distance[np.argmin(distance)], human_faculties[np.argmin(distance)] # returns closest human id and distance, and faculty


def create_population():
    humans = []
    for i in range(population):
        h = human(i)
        h.id = i
        if h.mask_wearing ==1:
            h.covid_prob /= 2

        if h.vaccinations ==1:
            h.covid_prob /= 2
        humans.append(h)

    return humans

def set_up_abm_environment():
    global humans,df, time, day,library, business, computing, science, nubar, gym, week_count,student_isolation_counts
    time = 0
    week_count = 0
    # create dataframe for number of infected people and number of isolating people
    student_isolation_counts = pd.DataFrame(columns=['time','number_isolating','number_infected'])
    # create dataframe for spreaders and newly infected people
    df = pd.DataFrame(columns=[
                                   'Spreader_id', 'Spreader_faculty','Infected_id','Infected_faculty','Time_of_infection'])
    humans = create_population()
    library = library()
    gym = gym()
    nubar = nubar()
    computing = computing()
    science = science()
    business = business()


def display_model():
    global time, day,library, business, computing, science, nubar, gym, week_count, hours
    cla()
    a = plt.imread('images/dcu_map.png')
    hours = time%24

    clock_time = time - week_count*7*24

    if clock_time < 24:
        day = 'Monday'
    elif clock_time >= 24 and clock_time < 48:
        day = 'Tuesday'
    elif clock_time >= 48 and clock_time < 72:
        day = 'Wednesday'
    elif clock_time >= 72 and clock_time < 96:
        day = 'Thursday'
    elif clock_time >= 96 and clock_time < 120:
        day = 'Friday'
    elif clock_time >= 120 and clock_time < 144:
        day = 'Saturday'
    elif clock_time >= 144 and clock_time < 168:
        day = 'Sunday'


    title('Time: ' + day +","+ str(hours) +' hours'+ ", Week "+str(week_count))
    plt.imshow(a, extent=[0, 1, 0, 1])
    for h in humans:
        if h.covid_status == 'infected':
            plot(h.x, h.y, 'r^')
        else:
            plot(h.x, h.y, 'g.')
    if clock_time==167:
        week_count +=1

def move_all_one_step():
    global time, hours, day, week_count
    time += 1
    # simulating movement through a day
    for h in humans:
        if hours == 0:
            if h.covid_status == 'infected' and h.days_infected != 14:
                h.days_infected +=1
                # stay home if prob >= 0.7
                prob = random()
                if prob >= 0.7:
                    h.x = h.home_x
                    h.y = h.home_y
                    h.quarantine = 1
                else:
                    h.quarantine = 0
            if h.covid_status == 'infected' and h.days_infected == 14:
                h.covid_status = 'normal'
                h.days_infected = 0
                h.covid_prob = 0.0001 #reset probability
                if h.vaccinations == 1:
                    h.covid_prob /=2
                if h.mask_wearing == 1:
                    h.covid_prob /=2

        # if weekend, choose a new status for the day
        if day in ['Saturday','Sunday'] and h.quarantine != 1:
            if hours == 0:
                h.change_status()
            h.move_wknd(m,hours)
            h.infection()
        # if not weekend, carry on as normal
        else:
            if h.quarantine != 1:
                # if 18, humans choose evening status
                if hours == 18:
                    h.eveningstatus()
                h.move(m, hours)
                h.infection()


def refresh_model():
    global df, hours, day, week_count,humans,student_isolation_counts
    move_all_one_step()

    # saving number of infected / isolating people
    if hours == 23:
        l = sum([1 for h in humans if h.covid_status =='infected'])
        m = sum([1 for h in humans if h.quarantine == 1 and h.covid_status == 'infected'])
        t = "Week " + str(week_count) + " " + day + " "+str(hours)
        student_isolation = pd.DataFrame([[t,m,l]],columns=['time','number_isolating','number_infected'])
        temp = student_isolation_counts
        student_isolation_counts = pd.concat([temp,student_isolation])

pycxsimulator.GUI().start(func=[set_up_abm_environment, display_model, refresh_model])
df.to_csv('Infections_ID.csv')
student_isolation_counts.to_csv('Isolation_And_Infection_Counts.csv')
