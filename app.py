import streamlit as st
import numpy as np

# Constants
GRAVITY = 10  # gravity constant (m/s^2)

# Title and introduction
st.title("Nerf Gun Muzzle Velocity and Spring Constant Calculator")
st.write("""
This app simulates the firing of a Nerf gun based on parameters such as range, muzzle length, and height of impact. 
Given these parameters, it calculates the muzzle velocity and the spring constant of the Nerf gun.
""")

# User inputs
range_distance = st.number_input("Enter the horizontal range (m):", min_value=0.1, step=0.1)
muzzle_length = st.number_input("Enter the muzzle length (m):", min_value=0.01, step=0.01)
height_of_impact = st.number_input("Enter the height of impact (m):", min_value=0.1, step=0.1)
spring_compression = st.number_input("Enter the spring compression (m):", min_value=0.01, step=0.01)

if st.button("Calculate"):
    # Calculate time of flight based on vertical distance
    time_of_flight = np.sqrt((2 * height_of_impact) / GRAVITY)
    
    # Calculate muzzle velocity
    muzzle_velocity = range_distance / time_of_flight
    
    # Calculate spring constant using Hooke's law: F = k * x, where F = ma = m*v^2/(2 * spring_compression)
    dart_mass = 0.02  # Assume an average Nerf dart mass in kg (adjust if known)
    spring_constant = (dart_mass * muzzle_velocity**2) / (2 * spring_compression)
    
    # Display results
    st.write(f"### Results:")
    st.write(f"Muzzle Velocity: {muzzle_velocity:.2f} m/s")
    st.write(f"Spring Constant: {spring_constant:.2f} N/m")
    
    # Optional visualization
    st.write("The dart travels in a parabolic trajectory, reaching the ground after traveling the horizontal range.")
