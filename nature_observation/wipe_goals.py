import sqlite3
from main import NatureObservationTool

def wipe_goals():
    """Completely wipe all goals and user_goals from the database."""
    tool = NatureObservationTool()
    
    # Establish a direct connection
    conn = sqlite3.connect(tool.db_path)
    cursor = conn.cursor()
    
    # Delete all records from both tables
    cursor.execute('DELETE FROM user_goals')
    cursor.execute('DELETE FROM goals')
    
    # Reset the auto-increment counters
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="goals" OR name="user_goals"')
    
    conn.commit()
    conn.close()
    
    print("All goals have been wiped from the database!")

if __name__ == "__main__":
    wipe_goals()
