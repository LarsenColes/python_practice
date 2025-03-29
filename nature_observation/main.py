import sqlite3
import datetime
import os
from typing import List, Dict, Any, Optional

class NatureObservationTool:
    def __init__(self, db_path: str = "nature_observations.db"):
        """Initialize the Nature Observation Tool with a database connection."""
        self.db_path = db_path
        self._create_tables_if_not_exist()
    
    def _create_tables_if_not_exist(self) -> None:
        """Create necessary database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create observations table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            location TEXT,
            observation_date TEXT NOT NULL,
            weather_conditions TEXT,
            temperature REAL,
            species_observed TEXT,
            notes TEXT,
            image_path TEXT,
            created_at TEXT NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_observation(self, 
                        title: str, 
                        description: Optional[str] = None,
                        location: Optional[str] = None,
                        observation_date: Optional[str] = None,
                        weather_conditions: Optional[str] = None,
                        temperature: Optional[float] = None,
                        species_observed: Optional[str] = None,
                        notes: Optional[str] = None,
                        image_path: Optional[str] = None) -> int:
        """
        Add a new nature observation to the database.
        
        Returns:
            int: The ID of the newly created observation
        """
        if observation_date is None:
            observation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO observations (
            title, description, location, observation_date, 
            weather_conditions, temperature, species_observed, 
            notes, image_path, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            title, description, location, observation_date,
            weather_conditions, temperature, species_observed,
            notes, image_path, created_at
        ))
        
        observation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return observation_id
    
    def get_observation(self, observation_id: int) -> Dict[str, Any]:
        """Retrieve a specific observation by ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM observations WHERE id = ?', (observation_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return dict(row)
        return {}
    
    def get_all_observations(self) -> List[Dict[str, Any]]:
        """Retrieve all observations from the database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM observations ORDER BY observation_date DESC')
        rows = cursor.fetchall()
        
        observations = [dict(row) for row in rows]
        conn.close()
        
        return observations
    
    def update_observation(self, observation_id: int, **kwargs) -> bool:
        """
        Update an existing observation.
        
        Args:
            observation_id: The ID of the observation to update
            **kwargs: Fields to update and their new values
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not kwargs:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build the SET part of the SQL query
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(observation_id)
        
        cursor.execute(f"UPDATE observations SET {set_clause} WHERE id = ?", values)
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    def delete_observation(self, observation_id: int) -> bool:
        """
        Delete an observation from the database.
        
        Returns:
            bool: True if successful, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM observations WHERE id = ?", (observation_id,))
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success


# Example usage
if __name__ == "__main__":
    tool = NatureObservationTool()
    
    # Add a sample observation
    observation_id = tool.add_observation(
        title="Morning Bird Watching",
        description="Observed several species of birds at the local park",
        location="Sunset Park",
        weather_conditions="Sunny, light breeze",
        temperature=72.5,
        species_observed="Robin, Blue Jay, Cardinal",
        notes="Cardinals were particularly active around the berry bushes"
    )
    
    print(f"Added observation with ID: {observation_id}")
    
    # Retrieve and display the observation
    observation = tool.get_observation(observation_id)
    print("\nObservation details:")
    for key, value in observation.items():
        print(f"{key}: {value}")

