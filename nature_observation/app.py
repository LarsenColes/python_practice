from flask import Flask, render_template, request, redirect, url_for, session
from main import NatureObservationTool
from geo_utils import LocationResolver
import random
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Used for session management
tool = NatureObservationTool()
location_resolver = LocationResolver()

@app.route('/')
def index():
    """Render the main page with goal suggestion and observation form."""
    # Get or initialize user's current goal
    user_goal = tool.get_current_user_goal()
    debug_info = {}
    
    # If no active goal, suggest a new one based on location
    if not user_goal:
        user_location = location_resolver.get_user_location()
        debug_info['raw_location'] = user_location
        
        # Store location in session for future use
        session['user_location'] = user_location
        
        # Determine state code
        state_code = user_location.get('state', '')
        if not state_code and user_location.get('latitude') and user_location.get('longitude'):
            state_code = location_resolver.get_state_from_coordinates(
                user_location['latitude'], 
                user_location['longitude']
            )
        
        debug_info['state_code'] = state_code
        
        # Get goals for this state
        state_goals = tool.get_goals_by_region(state_code) if state_code else []
        debug_info['num_state_goals'] = len(state_goals)
        
        # If no specific goals for this state, use generic goals
        if not state_goals:
            debug_info['fallback'] = 'Using generic goals'
            state_goals = tool.get_goals_by_region("Unknown")
            debug_info['num_generic_goals'] = len(state_goals)
        
        # Choose a random goal from available ones
        if state_goals:
            selected_goal = random.choice(state_goals)
            debug_info['selected_goal_id'] = selected_goal['id']
            debug_info['selected_goal_text'] = selected_goal['goal_text']
            
            location_display = f"{user_location.get('city', '')}, {user_location.get('state_name', '')}"
            if not location_display.strip(' ,'):
                location_display = "Unknown location"
                
            user_goal_id = tool.assign_goal_to_user(
                selected_goal['id'],
                location_display
            )
            debug_info['assigned_user_goal_id'] = user_goal_id
            
            user_goal = tool.get_current_user_goal()
            debug_info['retrieved_user_goal'] = bool(user_goal)
    
    # Debug information
    debug_info = False
    
    return render_template('index.html', user_goal=user_goal, debug_info=debug_info)

@app.route('/set_state', methods=['POST'])
def set_state():
    """Manually set the user's state."""
    state_code = request.form.get('state', 'Unknown')
    
    # Clear any existing incomplete goals
    conn = sqlite3.connect(tool.db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_goals WHERE is_completed = 0')
    conn.commit()
    conn.close()
    
    # Get goals for this state
    state_goals = tool.get_goals_by_region(state_code)
    
    # If no specific goals for this state, use generic goals
    if not state_goals:
        state_goals = tool.get_goals_by_region("Unknown")
    
    # Choose a random goal
    if state_goals:
        selected_goal = random.choice(state_goals)
        tool.assign_goal_to_user(
            selected_goal['id'],
            f"Manually set: {state_code}"
        )
    
    return redirect(url_for('index'))

@app.route('/complete_goal/<int:user_goal_id>', methods=['POST'])
def complete_goal(user_goal_id):
    """Mark the current goal as completed."""
    tool.complete_user_goal(user_goal_id)
    return redirect(url_for('index'))

@app.route('/skip_goal/<int:user_goal_id>', methods=['POST'])
def skip_goal(user_goal_id):
    """Skip the current goal and get a new one."""
    tool.complete_user_goal(user_goal_id)  # Mark as completed but with a skip flag
    return redirect(url_for('index'))

@app.route('/log_observation', methods=['POST'])
def log_observation():
    """Handle the form submission to log a new observation."""
    title = request.form['title']
    description = request.form.get('description', '')
    location = request.form.get('location', '')
    observation_date = request.form.get('observation_date', '')
    weather_conditions = request.form.get('weather_conditions', '')
    temperature = request.form.get('temperature', '')
    if temperature and temperature.strip():
        try:
            temperature = float(temperature)
        except ValueError:
            temperature = None
    else:
        temperature = None
    species_observed = request.form.get('species_observed', '')
    notes = request.form.get('notes', '')
    image_path = request.form.get('image_path', '')
    
    # Add the observation to the database
    observation_id = tool.add_observation(
        title=title,
        description=description,
        location=location,
        observation_date=observation_date if observation_date else None,
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

@app.route('/delete_observation/<int:observation_id>', methods=['POST'])
def delete_observation(observation_id):
    """Delete an observation from the database."""
    success = tool.delete_observation(observation_id)
    
    if success:
        # Optional: add a flash message if you want to inform the user
        # flash("Observation deleted successfully!")
        pass
    else:
        # Optional: inform the user if deletion failed
        # flash("Failed to delete observation.")
        pass
        
    # Redirect back to the observations list
    return redirect(url_for('view_observations'))

if __name__ == '__main__':
    app.run(debug=True)
