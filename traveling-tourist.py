from flask import Flask
from flask import render_template

app = Flask(__name__)

class TravellingTourist:
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


@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/example')
def example_page():
    locations = ["1", "2", "3", "4", "5"]
    tourist = TravellingTourist("walking", "", "", "", locations)
    weights = tourist.get_weights()
    weights_string = " ".join(weights)
    return render_template('example.html', name=weights_string)

if __name__ == '__main__':
    app.run(debug=True)
