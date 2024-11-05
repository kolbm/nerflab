import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Constants
GRAVITY = 10  # gravity constant (m/s^2)

# Display a centered title image using HTML and CSS styling
st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <img src="https://github.com/kolbm/nerflab/blob/main/nerflab.jpg?raw=true" alt="Title Image" width="90%">
    </div>
    """,
    unsafe_allow_html=True
)

# Title and introduction
st.title("Nerf Gun Muzzle Velocity and Spring Constant Calculator")
st.write("""
This app simulates the firing of a Nerf gun based on parameters such as range, muzzle length (spring compression), 
starting and ending heights, and dart mass. Given these parameters, it calculates the muzzle velocity, spring constant, 
and plots the trajectory.
""")

# User inputs with preferred starting values
range_distance = st.number_input("Enter the horizontal range (m):", min_value=0.1, step=0.1, value=30.0)
starting_height = st.number_input("Enter the starting height (m):", min_value=0.1, step=0.1, value=2.0)
ending_height = st.number_input("Enter the ending height (m):", min_value=0.1, step=0.1, value=1.0)
muzzle_length = st.number_input("Enter the muzzle length (spring compression) (m):", min_value=0.01, step=0.01, value=0.15)
dart_mass = st.number_input("Enter the mass of the dart (kg):", min_value=0.001, step=0.001, value=0.01)

# Calculate the difference in height
height_difference = starting_height - ending_height

if st.button("Calculate"):
    # Calculate time of flight based on vertical distance
    time_of_flight = np.sqrt((2 * abs(height_difference)) / GRAVITY)
    
    # Calculate muzzle velocity
    muzzle_velocity = range_distance / time_of_flight
    
    # Calculate spring constant using Hooke's law: k = (m * v^2) / (2 * spring_compression)
    spring_constant = (dart_mass * muzzle_velocity**2) / (2 * muzzle_length)
    
    # Display results
    st.write(f"### Results:")
    st.write(f"Muzzle Velocity: {muzzle_velocity:.2f} m/s")
    st.write(f"Spring Constant: {spring_constant:.2f} N/m")
    
    # Time values for the trajectory
    time_values = np.linspace(0, time_of_flight, num=100)
    
    # Calculate x and y positions over time
    x_values = muzzle_velocity * time_values
    y_values = starting_height - (0.5 * GRAVITY * time_values ** 2)
    
    # Create a DataFrame for the trajectory points
    trajectory_data = pd.DataFrame({
        "Time (s)": time_values,
        "X Position (m)": x_values,
        "Y Position (m)": y_values
    })
    
    # Plotting the trajectory
    fig, ax = plt.subplots()
    ax.plot(x_values, y_values, label="Dart Trajectory", color="blue")
    ax.set_xlabel("Horizontal Distance (m)")
    ax.set_ylabel("Vertical Height (m)")
    ax.set_title("Trajectory of the Nerf Dart")
    ax.legend()
    ax.grid(True)
    ax.set_ylim(0, max(starting_height, np.max(y_values)) + 0.5)
    
    # Show the plot in Streamlit
    st.pyplot(fig)
    
    # Provide download link for the CSV
    csv = trajectory_data.to_csv(index=False)
    st.download_button(
        label="Download Trajectory Data as CSV",
        data=csv,
        file_name="nerf_dart_trajectory.csv",
        mime="text/csv"
    )
