## CTA Code Challenge

#### Setup
This application was built using Flask. To install dependencies in a virtual environment run the following commands.
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
At that point, you should be able to run the application and access it on `localhost:5000/api/winner`. by typing
```
flask run
```

#### Development Process
I spent a little time deciding how to set this up, I landed on Flask for simplicity and speed. In terms of application structure I separated out a data directory to contain both JSON, and data processing assistance.

I envisioned getting this data and imagined it would probably be one endpoint that would accept parameters related to scale, ie whether it was state or county data required, or if the `level` parameter
was left off we would return all data.

My ultimate goal was to separate the data processing steps between the county and local level but to flatten the objects into a more useful version - for instance when we see county primary results, county
names repeat across the country so there was a data transformation step to flatten the county objects out from under state dictionary keys and instead add the state as an addendum to name, ie "Baltimore, MD".

Standardizing the state and local data structure let one function be used on both to determine winners (or was the goal).

#### Things I'd do differently & Future Improvements
* **tests**: this application would benefit from both unit and integration tests
* **generate more test JSON**: if developing this as a real feature would want more data to check edge cases
* **structure**: this application structure is more or less nothing, and not how I'd wind up doing a project in real life
* **efficiency**: there are some areas with nested loops that I am sure there is a way to avoid, I wanted to have time to refine that at the end but ran out before thinking of how to get out of that
* **brittleness**: this logic is brittle, and would need to be generalized to accept erroneous data or third party candidates in primaries
* **core functionality**: **this is the most important**, I ran out of time to get some things working. I realized that might happen, but I wanted to get the broad strokes of my plan out there to show what I was thinking and assumed that it might be understood that with the time limit I ran out of time to debug some portions of this that weren't working 
