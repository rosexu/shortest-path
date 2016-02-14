from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import requests
import json
import sys

app = Flask(__name__)

class TravelingTourist:
    'The class containing the logic for retrieving the optimal intinery.'

    def __init__(self, mode, transit_mode, transit_preferences, avoid, locations):
        # mode = string representing mode
        #       ["driving", "walking", "bicycling", "transit"]
        self.mode = mode
        # transit_mode = string representing mode of transit, only if mode = transit
        #       ["bus", "subway", "train", "tram", "rail"]
        self.transit_mode = transit_mode
        # transit_preferences = string representing preferences
        #       ["less_walking", "fewer_transfers"]
        self.transit_preferences = transit_preferences
        # avoid = string representing things to avoid
        #       ["tolls", "highways", "ferries", "indoor"]
        self.avoid = avoid
        # locations = array of string addresses
        self.locations = locations
        # loc_to_duration = mapping of travel duration between two locations
        self.loc_to_duration = {}
        # the shortest duration for the entire trip
        self.shortest_duration = 0
        # the sequence of locations to visit
        self.travel_sequence = []


    # Returns:  a list of ints representing the weights (ex. for 1, 2, 3, 4, 5, 
    #           it will be [1&2, 1&3, 1&4, 1&5, 2&3, 2&4, 2&5, 3&4, 3&5, 4&5])
    def get_weights(self):
        weights = []
        for i in range(0, len(self.locations) - 1):
            for j in range(i+1, len(self.locations)):
                duration = self.calculate_weight(self.locations[i], self.locations[j])
                weights.append(str(duration))
                self.loc_to_duration[(self.locations[i], self.locations[j])] = duration
        return weights

    # Returns: the list of int weights as a comma-delimited string.
    def weights_as_string(self, weights):
        return ",".join(weights)

    def calculate_weight(self, location_a, location_b):
        baseUrl = "https://maps.googleapis.com/maps/api/distancematrix/json?&key=AIzaSyD1VgpTw216ScP1Vo23YrWQEKoL1pSUvys"
        params = {'origins': location_a, 'destinations': location_b, 'mode': self.mode, 
            'avoid': self.avoid, 'transit_preferences': self.transit_preferences }
        if self.mode == "transit":
            params['transit_mode'] = self.transit_mode
        data = json.loads(requests.get(baseUrl, params).text)
        if data['status'] == "OK":
            element = data['rows'][0]['elements'][0]
            if element['status'] == "OK":
                return element['duration']['value']
            else:
                return sys.maxint
        else:
            raise Exception("API call failure.")

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
        result = requests.get(wolfram_url, params=params).json()
        self.shortest_duration = result[0]

        return result

    def get_travel_sequence(self, sequence):
        for i in range(0, len(sequence) - 1):
            self.travel_sequence.append(self.locations[sequence[i] - 1])
        return self.travel_sequence

    # Return an array of travel times from one place in the travel_sequence to the next, in order.
    def get_travel_duration(self):
        travel_duration = []
        for i in range(0, len(self.travel_sequence) - 1):
            loc_a = self.travel_sequence[i]
            loc_b = self.travel_sequence[i+1]
            if (loc_a, loc_b) in self.loc_to_duration:
                travel_duration.append(self.loc_to_duration[(loc_a, loc_b)])
            elif (loc_b, loc_a) in self.loc_to_duration:
                travel_duration.append(self.loc_to_duration[(loc_b, loc_a)])
            else:
                raise Exception("Unable to find duration for"+loc_a+", "+loc_b)
        return travel_duration


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

    class TravelLeg:
        def __init__(self, start_loc, end_loc, duration, travel_duration, start_time):
            self.start_loc = start_loc
            self.end_loc = end_loc
            # the time to spend at the location, in seconds
            self.duration = duration
            # the time that the user will begin to travel to the current location
            self.start_time = start_time
            # the travel duration needed to get to the current location in seconds
            # the origin's travel_duration is 0
            self.travel_duration = travel_duration

        def get_end_time(self):
            self.start_time.add(self.travel_duration/60) 
            self.start_time.add(self.duration/60)
            return self.start_time

    def __init__(self, loc_to_duration, start_time, sequence, travel_duration):
        # user input -> dictionary mapping location to amount of time allocated at that location.
        self.loc_to_duration = loc_to_duration
        # the time the user specifies as the start of their adventures.
        self.start_time = start_time
        # the order in which the locations will be visited, as determined by algorithmn.
        self.travel_sequence = sequence
        # an array of time going from place to place, in order
        self.travel_duration = travel_duration
        # an array of TravelLegs
        self.result = []

    def create_itinerary(self):
        time = self.start_time
        for i in range(0, len(self.travel_sequence) - 1): 
            loc_from = self.travel_sequence[i]
            loc_to = self.travel_sequence[i+1]
            leg = self.TravelLeg(loc_from, loc_to, self.loc_to_duration[loc_from] ,self.travel_duration[i], time)
            self.result.append(json.dumps(leg, default=lambda o: o.__dict__))
            time = leg.get_end_time()
        return self.result


@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/getItinerary', methods=['POST'])
def itinerary_page():
    data = request.json
    location_to_duration = data['locations']
    locations = location_to_duration.keys()
    mode = data['mode']
    transit_mode = data['transit_mode']
    transit_preferences = data['transit_preferences']
    avoid = data['avoid']
    start_time_raw = data['start_time'] 

    start_time = Time(start_time_raw['hours'], start_time_raw['minutes'])
    tourist = TravelingTourist(mode, transit_mode, transit_preferences, avoid, locations)
    weights = tourist.get_weights()
    result = tourist.request_shortest_path(len(locations), tourist.weights_as_string(weights))
    travel_sequence = tourist.get_travel_sequence(result[1])
    travel_duration = tourist.get_travel_duration()
    itinerary_instance = Itinerary(location_to_duration, start_time, travel_sequence, travel_duration)
    itinerary = itinerary_instance.create_itinerary()
    result = {}
    result['data'] = itinerary
    return jsonify(**result)

@app.route('/example')
def example_page():
    location_to_duration = {"San Mateo": 1, "San Francisco": 2, "Stanford": 3, "Oakland": 1, 
    "Redwood City": 2}
    locations = ["San Mateo", "San Francisco", "Stanford", "Redwood City", "Oakland"]
    tourist = TravelingTourist("walking", "", "less_walking", "", locations)
    weights = tourist.get_weights()
    result = tourist.request_shortest_path(5, tourist.weights_as_string(weights))
    travel_sequence = tourist.get_travel_sequence(result[1])

    start_time = Time(9, 0)
    travel_duration = tourist.get_travel_duration()
    itinerary_instance = Itinerary(location_to_duration, start_time, travel_sequence, travel_duration)
    itinerary = itinerary_instance.create_itinerary()
    return render_template('example.html', name=itinerary)

if __name__ == '__main__':
    app.run(debug=True)

# Idea for shortest route with opening hour constraints.
# Do a check to make sure nothing is already closed.
# Try to get shortest route. See if closing hour activities are satisfied.
# Sort the list based on closing hours.
# Place all the ones that must be hit in place.
# Try to minimize time after.