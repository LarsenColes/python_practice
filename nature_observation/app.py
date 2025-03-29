from flask import Flask, render_template, request, redirect, url_for
from main import NatureObservationTool

app = Flask(__name__)
tool = NatureObservationTool()  # Initialize your NatureObservationTool

@app.route('/')
def index():
    """Render the main page with a form to log observations."""
    return render_template('index.html')

@app.route('/log_observation', methods=['POST'])
def log_observation():
    """Handle the form submission to log a new observation."""
    title = request.form['title']
    description = request.form['description']
    location = request.form['location']
    observation_date = request.form['observation_date']
    weather_conditions = request.form['weather_conditions']
    temperature = request.form['temperature']
    species_observed = request.form['species_observed']
    notes = request.form['notes']
    image_path = request.form['image_path']
    
    # Add the observation to the database
    observation_id = tool.add_observation(
        title=title,
        description=description,
        location=location,
        observation_date=observation_date,
        weather_conditions=weather_conditions,
        temperature=temperature,
        species_observed=species_observed,
        notes=notes,
        image_path=image_path
    )
    
    # Redirect to the newly created observation
    return redirect(url_for('view_observation', observation_id=observation_id))

@app.route('/observations')
def view_observations():
    """Render a page displaying all logged observations."""
    observations = tool.get_all_observations()
    return render_template('observations.html', observations=observations)

@app.route('/observation/<int:observation_id>')
def view_observation(observation_id):
    """Render a page displaying a single observation."""
    observation = tool.get_observation(observation_id)
    if not observation:
        return "Observation not found", 404
    return render_template('observation_detail.html', observation=observation)

if __name__ == '__main__':
    app.run(debug=True)
