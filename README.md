# Route Finder with A* Algorithm

This application is a **route-finding tool** that uses the **A* algorithm** to calculate the shortest path between two tour places in Central Java, Indonesia. The tool allows users to interactively select a starting and destination to find the optimal route and view it on a map.

## Features

- **Interactive Map**: Visualize the route on a Folium map embedded in the Streamlit application.
- **Shortest Path Calculation**: Find the shortest path between cities using the A* algorithm.
- **Real-time Results**: View the calculated route and total distance instantly.

## Technology Stack

- **Python**
- **Streamlit**: For creating the interactive web application.
- **Folium**: For rendering maps and visualizing routes.
- **Heapq**: For efficient priority queue management in the A* algorithm.

## How to Run the Application

1. **Install Requirements**:
    ```bash
    pip install streamlit folium streamlit-folium
    ```

2. **Run the Application**:
    ```bash
    streamlit run app_ver2.0.py
    ```

3. **Open in Browser**:
    The application should open in your default web browser, displaying the route-finding interface.

## Usage

1. Launch the app and select your starting and destination cities.
2. Click to view the calculated shortest path and total distance.
3. The map will display the optimal route visually.

## Files

- `app_ver2.0.py`: Main application file containing the A* algorithm and interactive UI setup.

## License

This project is open-source. You are welcome to modify and use it under the terms of the MIT License.

