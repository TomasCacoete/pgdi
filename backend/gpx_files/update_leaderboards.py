import sqlite3

# Connect to the database
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Define the table names
times_table = 'participant_times'
user_table = 'user'

try:
    # Fetch participants ordered by their times (ascending order)
    cursor.execute(f"""
        SELECT id, time 
        FROM {times_table} 
        ORDER BY time ASC
    """)
    
    participants = cursor.fetchall()
    total_participants = len(participants)
    
    # Assign points based on ranking (1st place gets total_participants points, last place gets 1 point)
    for rank, (participant_id, time) in enumerate(participants, start=1):
        points = total_participants - rank + 1
        
        # Update the user.points category with the new points
        cursor.execute(f"""
            UPDATE {user_table}
            SET points = points + ?
            WHERE id = ?
        """, (points, participant_id))
    
    # Commit the changes
    conn.commit()
    
    print(f"Points updated for {total_participants} participants.")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
    conn.rollback()

finally:
    # Close the connection
    conn.close()