import json

class DataHelper:
    def __init__(self, params):
        self.election_data = self.load_election_data()
        self.filtered_primary_winners = self.get_filtered_election_data(params)


    def load_election_data(self) -> dict:
        """
        Processes JSON file data with minor error handling,
        TODO refine error logic
        """
        try:
            with open('./data/data.json') as file:
                return json.load(file)
        except Exception as e:
            return { "statusCode": 500, "status": "Internal Server Error - corrupted or missing data source" }


    def flatten_county_results(self) -> dict:
        """
        Handles request for county level primary data, flattening data
        structure for later logic that determines winners. Reformats county
        name to include state for clarity
        """
        results = {}

        for state in self.election_data:
            for county in self.election_data[state]:
               results[f"{county}, {state}"] = self.election_data[state][county]


        print("\n LOCAL RESULTS")
        print(results)
        return results


    def flatten_state_results(self) -> dict:
        """
        Collapses state results from distinct counties into only two child objects
        for democrat and republican contenders

        TODO brittle, would not handle third party candidates yet
        """
        results = {}

        for state in self.election_data:
            if not state in results:
                print(f"No entry, building {state}")
                # create state entry for new state
                results[state] = { "Democrats": {}, "Republicans": {}}

            for county in self.election_data[state]:
               results[state]["Democrats"].update(self.election_data[state][county]["Democrats"])
               results[state]["Republicans"].update(self.election_data[state][county]["Republicans"])

        print("\n STATE RESULTS")
        print(results)
        return results


    def process_winners(self, filtered_data) -> dict:
        """
        Distils each party field into the primary challenger who received most votes

        TODO brittle, doesn't deal with third parties
        """
        results = {}

        for item in filtered_data:
            race = filtered_data[item]
            print("RACE")
            print(race)
            print("ITEM")
            print(item)

            if item not in results: # build base entry if none exists
                results[item] = {
                    "rep_winner": None,
                    "rep_winner_votes": 0,
                    "dem_winner": None,
                    "dem_winner_votes": 0
                }

            high_dem = max(race["Democrats"], key=lambda key: race[key])
            high_rep = max(race["Republicans"], key=lambda key: race[key])

            if race["Democrats"][high_dem] > results[race]["dem_winner_votes"]:
                results[race]["dem_winner"] = high_dem
                results[race]["dem_winner_votes"] = race["Democrats"][high_dem]

            if race["Republican"][high_rep] > results[race]["rep_winner_votes"]:
                results[race]["rep_winner"] = high_dem
                results[race]["rep_winner_votes"] = race["Republicans"][high_rep]

        print("\nPROCESS WINNERS")
        print(results)
        return results


    def get_filtered_election_data(self, params) -> dict:
        """
        Core logic that formats and distils data into all winners based on
        parameters. Works off a copy of election data in case we may want to avoid mutating it
        for future added functionality
        """
        win_data = self.election_data.copy()

        if 'level' in params:
            if params['level'] == county:
                win_data = self.flatten_county_results()
            elif params['level'] == state:
                win_data = self.flatten_state_results()
            else:
                return { "statusCode": 400, "status": "Bad Request - valid parameters are: county, state"}

            win_data = self.process_winners(win_data)
        else:
            # form full dictionary of all state and locality primary winners
            county = self.process_winners(self.flatten_county_results())
            state = self.process_winners(self.flatten_state_results())
            print("\n FINAL RESULTS")
            print(county)
            print(state)

        return {}
