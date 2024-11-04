import heapq 
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium import plugins

# Judul Aplikasi
st.title("Pencarian Rute Terdekat dengan Algoritma A*")

st.write("""
Aplikasi ini menggunakan algoritma A* untuk menemukan rute terdekat antara dua kota di Jawa Tengah. 
Silakan pilih kota awal dan tujuan untuk melihat rute terbaik beserta total jaraknya.
""")

# Definisikan graf dengan jarak antar kota dan jalur alternatif
graph = {
    'Keraton Kasunanan Surakarta': [('Pura Mangkunegaran', 1), ('Alun-Alun Kidul', 2), ('Museum Batik Danar Hadi', 3),('Taman Hutan Rakyat', 5)],
    'Pura Mangkunegaran': [('Keraton Kasunanan Surakarta', 1), ('Alun-Alun Kidul', 2), ('The Heritage Palace', 10)],
    'Alun-Alun Kidul': [('Keraton Kasunanan Surakarta', 2), ('Pura Mangkunegaran', 2)],
    'The Heritage Palace': [('Pura Mangkunegaran', 10), ('Museum Radya Pustaka', 8)],
    'Museum Batik Danar Hadi': [('Keraton Kasunanan Surakarta', 3), ('Museum Radya Pustaka', 1)],
    'Museum Radya Pustaka': [('Museum Batik Danar Hadi', 1), ('The Heritage Palace', 8)],
    'Grojogan Sewu Tawangmangu': [('Candi Cetho', 7), ('Sekipan Campground', 3)],
    'Candi Cetho': [('Grojogan Sewu Tawangmangu', 7), ('Sekipan Campground', 5),('Telaga Madirda',8)],
    'Taman Hutan Rakyat': [('Keraton Kasunanan Surakarta', 5), ('Candi Cetho',13)],
    'Telaga Madirda': [('Candi Cetho', 8)],
    'Vihara Dhamma Sundara': [('Keraton Kasunanan Surakarta', 4)],
    'De Tjolomadoe': [('Pura Mangkunegaran', 12)],
    'Triwindu Antique Market': [('Museum Radya Pustaka', 1)],
    'Sekipan Campground': [('Grojogan Sewu Tawangmangu', 3), ('Candi Cetho', 5)],
    'Agrowisata Sondokoro Karanganyar': [('Keraton Kasunanan Surakarta', 15)]
}


positions = {
    'Keraton Kasunanan Surakarta': (-7.577731957297213, 110.8279313535551),
    'Pura Mangkunegaran': (-7.56702610922588, 110.8228664842368),
    'Alun-Alun Kidul': (-7.582045701996743, 110.82647454006087),
    'The Heritage Palace': (-7.554557613999496, 110.75479883821411),
    'Museum Batik Danar Hadi': (-7.568570249825605, 110.81640376889594),
    'Museum Radya Pustaka': (-7.568249555765034, 110.8145505554016),
    'Grojogan Sewu Tawangmangu': (-7.66129956499744, 111.12871459773204),
    'Candi Cetho': (-7.595392337206488, 111.15746481122578),
    'Taman Hutan Rakyat': (-7.623004078067024, 111.13674132841342),
    'Telaga Madirda': (-7.63977268680755, 111.13085244006133),
    'Vihara Dhamma Sundara': (-7.569821021775316, 110.84892854190724),
    'De Tjolomadoe': (-7.533890659511755, 110.74994135355475),
    'Triwindu Antique Market': (-7.569101944983985, 110.82253829588468),
    'Sekipan Campground': (-7.672442462948099, 111.14676833622471),
    'Agrowisata Sondokoro Karanganyar': (-7.576176434128673, 110.93154892789619)
}
# Fungsi heuristik: estimasi jarak langsung dari node ke tujuan menggunakan koordinat posisi
def heuristic(a, b):
    from math import radians, cos, sin, asin, sqrt
    # Haversine formula untuk menghitung jarak antara dua titik di permukaan bumi
    lat1, lon1 = positions[a]
    lat2, lon2 = positions[b]
    # Konversi derajat ke radian
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a_hav = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a_hav)) 
    r = 6371 # Radius bumi dalam kilometer
    return c * r

# Fungsi A* untuk menemukan rute terdekat
def a_star_search(start, goal, graph):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    cost_so_far = {}
    
    came_from[start] = None
    cost_so_far[start] = 0
    
    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current == goal:
            break
        
        for next_node, cost in graph.get(current, []):
            new_cost = cost_so_far[current] + cost
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(next_node, goal)
                heapq.heappush(open_list, (priority, next_node))
                came_from[next_node] = current
    
    if goal not in cost_so_far:
        return [], float('inf'), came_from, cost_so_far
    
    # Rekonstruksi rute dari goal ke start
    route = []
    current = goal
    while current:
        route.append(current)
        current = came_from.get(current)
    route.reverse()
    
    return route, cost_so_far[goal], came_from, cost_so_far  # Return rute, total biaya, dan detail perhitungan

# Pilihan Kota
cities = list(graph.keys())

# Sidebar untuk memilih kota awal dan tujuan
st.sidebar.header("Pengaturan Rute")
start = st.sidebar.selectbox("Kota Awal", options=cities, index=cities.index('Magelang') if 'Magelang' in cities else 0)
goal = st.sidebar.selectbox("Kota Tujuan", options=cities, index=cities.index('Tawangmangu') if 'Tawangmangu' in cities else 0)

# Tombol untuk menjalankan pencarian
if st.sidebar.button("Cari Rute"):
    with st.spinner('Mencari rute terbaik...'):
        route, total_cost, came_from, cost_so_far = a_star_search(start, goal, graph)
    
    if route:
        st.success(f'Rute terdekat dari **{start}** ke **{goal}**:')
        st.write(" → ".join(route))
        st.write(f'**Total Jarak:** {total_cost} km')
        
        # Detail Perhitungan
        st.subheader("Detail Perhitungan:")
        st.markdown("**Rute alternatif yang dipertimbangkan dari setiap kota:**")
        
        for city in route:
            connections = graph.get(city, [])
            connection_details = ""
            for next_city, distance in connections:
                h = heuristic(next_city, goal)
                connection_details += f"- **{city} → {next_city}** (Jarak: {distance} km + Heuristik: {h:.2f} km)\n"
            st.markdown(f"**{city}:**\n{connection_details}")
        
        st.markdown("**Total jarak yang dihitung dari tiap node sampai tujuan:**")
        for i in range(len(route) - 1):
            from_city = route[i]
            to_city = route[i + 1]
            distance = next((cost for neighbor, cost in graph[from_city] if neighbor == to_city), None)
            if distance is not None:
                st.write(f"{from_city} → {to_city}: {distance} km")
        
        # Menampilkan Peta dengan Rute
        st.subheader("Peta Rute Terdekat")
        # Buat peta Folium
        # Pusatkan peta di kota awal
        map_center = positions[start]
        m = folium.Map(location=map_center, zoom_start=8)

        # Tambahkan marker untuk setiap kota
        for city, (lat, lon) in positions.items():
            folium.Marker(
                location=[lat, lon],
                popup=city,
                tooltip=city,
                icon=folium.Icon(color='blue' if city not in route else 'red', icon='info-sign')
            ).add_to(m)
        
        # Tambahkan garis antar kota
        for city, connections in graph.items():
            for neighbor, distance in connections:
                folium.PolyLine(
                    locations=[positions[city], positions[neighbor]],
                    weight=2,
                    color='gray',
                    opacity=0.5
                ).add_to(m)
        
        # Highlight rute yang ditemukan
        if len(route) > 1:
            route_locations = [positions[city] for city in route]
            folium.PolyLine(
                locations=route_locations,
                weight=4,
                color='red',
                opacity=0.8,
                tooltip="Rute Terdekat"
            ).add_to(m)
        
        # Tambahkan fitur zoom
        folium.TileLayer('OpenStreetMap').add_to(m)
        folium.LayerControl().add_to(m)
        
        # Tampilkan peta
        folium_static(m)
    else:
        st.error(f"Rute dari **{start}** ke **{goal}** tidak ditemukan.")

# Menampilkan Peta (Opsional)
st.sidebar.header("Posisi Kota")
if st.sidebar.checkbox("Tampilkan Posisi dan Jalur Kota"):
    # Buat peta Folium
    # Tentukan pusat peta
    default_city = 'Keraton Kasunanan Surakarta'
    map_center = positions[default_city]
    m = folium.Map(location=map_center, zoom_start=8)

    # Tambahkan marker untuk setiap kota
    for city, (lat, lon) in positions.items():
        folium.Marker(
            location=[lat, lon],
            popup=city,
            tooltip=city,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
    
    # Tambahkan garis antar kota
    for city, connections in graph.items():
        for neighbor, distance in connections:
            folium.PolyLine(
                locations=[positions[city], positions[neighbor]],
                weight=2,
                color='gray',
                opacity=0.5
            ).add_to(m)
    
    # Tambahkan fitur zoom dan layer kontrol
    folium.TileLayer('OpenStreetMap').add_to(m)
    folium.LayerControl().add_to(m)

    # Tampilkan peta
    folium_static(m)
