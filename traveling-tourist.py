from flask import Flask
from flask import render_template
import requests

app = Flask(__name__)

class TravelingTourist:
    'The class containing the logic for retrieving the optimal intinery.'

    # mode = string representing mode
    #       ["driving", "walking", "bicycling", "transit"]
    mode = "driving"
    # transit_mode = string representing mode of transit, only if mode = transit
    #       ["bus", "subway", "train", "tram", "rail"]
    transit_mode = ""
    # transit_preferences = string representing preferences
    #       ["less_walking", "fewer_transfers"]
    transit_preferences = "less_walking"
    # avoid = string representing things to avoid
    #       ["tolls", "highways", "ferries", "indoor"]
    avoid = ""
    # locations = array of string addresses
    locations = []

    def __init__(self, mode, transit_mode, transit_preferences, avoid, locations):
        self.mode = mode
        self.transit_mode = transit_mode
        self.transit_preferences = transit_preferences
        self.avoid = avoid
        self.locations = locations


    # Returns:  a list of ints representing the weights (ex. for 1, 2, 3, 4, 5, 
    #           it will be [1&2, 1&3, 1&4, 1&5, 2&3, 2&4, 2&5, 3&4, 3&5, 4&5])
    def get_weights(self):
        weights = []
        for i in range(0, len(self.locations) - 1):
            for j in range(i+1, len(self.locations)):
                weights.append(self.calculate_weight(self.locations[i], self.locations[j]))

        return weights

    def calculate_weight(self, loc_a, loc_b):
        # TODO: add Google map api call here with the query params
        return loc_a+loc_b

    # Return a json object with the first field being the minimum time required to hit
    # all the places and the second field being the sequence that yields the shortest time.
    def request_shortest_path(self, num_nodes, weights):
        wolfram_url = "https://www.wolframcloud.com/objects/6493b8d9-10db-4b57-9d98-a0f2c44cc47d"
        comma_delim_locations = ""

        for i in range(1, num_nodes + 1):
            comma_delim_locations += str(i)
            comma_delim_locations += ","

        # Cut off the last comma.
        comma_delim_locations = comma_delim_locations[:-1]

        params = {'locations': comma_delim_locations, 'weights': weights}
        result = requests.get(wolfram_url, params=params)
        return result.json()

class Time:
# LOL MAKING OUR OWN TIME CLASS
    # 0 to 59
    minute = 0
    # 0 to 23
    hour = 0
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def to_string(self):
        return str(self.hour) + ":" + str(self.minute)

    def add(self, minutes):
        temp_min = self.minute + minutes
        if temp_min < 59:
            self.minute = temp_min
        else:
            temp_hour = temp_min / 60
            self.minute = temp_min % 60
            self.hour = (self.hour + temp_hour) % 24


class Itinerary:

    # dictionary mapping location to amount of time allocated at that location.
    loc_to_duration = {}

    current_time = ""

    travel_sequence = ""

    def __init__(self, loc_to_duration, current_time, sequence):
        self.loc_to_duration = loc_to_duration
        self.current_time = current_time
        self.travel_sequence = sequence




@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/example')
def example_page():
    locations = ["1", "2", "3", "4", "5"]
    tourist = TravelingTourist("walking", "", "", "", locations)
    weights = tourist.get_weights()
    weights_string = ",".join(weights)
    tourist.request_shortest_path(5, weights_string)
    return render_template('example.html', name=weights_string)

if __name__ == '__main__':
    app.run(debug=True)

# Idea for shortest route with opening hour constraints.
# Do a check to make sure nothing is already closed.
# Try to get shortest route. See if closing hour activities are satisfied.
# Sort the list based on closing hours.
# Place all the ones that must be hit in place.
# Try to minimize time after.