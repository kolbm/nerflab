import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Constants
GRAVITY = 10  # gravity constant (m/s^2)

# Title and introduction
st.title("Nerf Gun Muzzle Velocity and Spring Constant Calculator")
st.write("""
This app simulates the firing of a Nerf gun based on parameters such as range, muzzle length, height of impact, 
and dart mass. Given these parameters, it calculates the muzzle velocity, spring constant, and plots the trajectory.
""")

# User inputs
range_distance = st.number_input("Enter the horizontal range (m):", min_value=0.1, step=0.1)
muzzle_length = st.number_input("Enter the muzzle length (m):", min_value=0.01, step=0.01)
height_of_impact = st.number_input("Enter the height of impact (m):", min_value=0.1, step=0.1)
spring_compression = st.number_input("Enter the spring compression (m):", min_value=0.01, step=0.01)
dart_mass = st.number_input("Enter the mass of the dart (kg):", min_value=0.001, step=0.001)

if st.button("Calculate"):
    # Calculate time of flight based on vertical distance
    time_of_flight = np.sqrt((2 * height_of_impact) / GRAVITY)
    
    # Calculate muzzle velocity
    muzzle_velocity = range_distance / time_of_flight
    
    # Calculate spring constant using Hooke's law
    spring_constant = (dart_mass * muzzle_velocity**2) / (2 * spring_compression)
    
    # Display results
    st.write(f"### Results:")
    st.write(f"Muzzle Velocity: {muzzle_velocity:.2f} m/s")
    st.write(f"Spring Constant: {spring_constant:.2f} N/m")
    
    # Time values for the trajectory
    time_values = np.linspace(0, time_of_flight, num=100)
    
    # Calculate x and y positions over time
    x_values = muzzle_velocity * time_values
    y_values = height_of_impact - (0.5 * GRAVITY * time_values ** 2)
    
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
    ax.set_ylim(0, max(height_of_impact, np.max(y_values)) + 0.5)
    
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
