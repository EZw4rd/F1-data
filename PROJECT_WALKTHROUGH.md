# F1 Analytics Dashboard — Phase 1 MVP Walkthrough

I have successfully completed the development of **Phase 1: Core MVP** as outlined in the implementation plan. The Streamlit dashboard is fully functional, using `fastf1` to pull live data and displaying it with the requested F1 dark mode aesthetic.

## Features Completed

### 1. Unified Navigation & Styling
- Multi-page routing via the sidebar.
- Custom CSS injected to enforce the F1 brand dark theme (`#15151E` background, monospace fonts for tables).
- Global dictionary mapping F1 teams to their official HEX colors.

### 2. Season View
- **Driver Standings:** Automatically calculated based on race and sprint results up to the current date.
- **Constructor Standings:** Computed and visualized as an interactive horizontal bar chart.
- **Calendar Grid:** Displays the schedule for the season cleanly, highlighting which events are Sprint weekends.

### 3. Grand Prix View
- **Event Picker:** Dropdown to select any completed race.
- **Overview:** Displays official circuit name, location, and dates.
- **Result Tables:** Renders complete classifications for Quick Qualifying and the Main Race.

### 4. Race View
- **Track Position Over Time (Lap Chart):** A line chart tracking every driver's position on every lap. The Y-axis is inverted so P1 remains visually at the top.
- **Gap-to-Leader Line Chart:** Computes the time delta (seconds) between every driver and the race leader at every lap.
- **Race Pace Heatmap:** A visual grid showing lap times across the race, filtering out VSC/Pit outlaps to identify pure tyre degradation patterns.
- **Tyre Strategy Timeline:** A Gantt-style chart showing how long each driver ran on each compound (Softs, Mediums, Hards), sorted logically by finishing position.
- **Pit Stop Summary:** A table extracting pit in/out times and compound changes during the race.
- **Automated Insight Cards:** Dynamically generates text snippets at the top of the view detailing the Fastest Lap, Biggest position Mover, and Longest Tyre Stint.

---
## Phase 2: Analytical Depth (Advanced Insights)

Building upon the Core MVP, the following advanced analytics were added in Phase 2:

**1. Data & Color Management:** 
- Hooked into FastF1's native driver color palettes. This means teammates now have distinct, recognizable colors (e.g. Verstappen is Dark Blue, Perez is slightly lighter blue) instead of sharing one flat team hex.

**2. Season View Enhancements:**
- **Cumulative Points Chart:** A line chart letting you track the driver's championship battle organically over time round-by-round.
- **Teammate H2H:** Quick stats aggregating race finishes to show who comes out on top within the same machinery.

**3. Grand Prix View Enhancements:**
- **Qualifying Sector Heatmap:** Visualizes S1, S2, and S3 times per driver across the grid using a diverging red-to-green scale.
- **Telemetry Overlay Comparison:** An interactive tool allowing you to select any two drivers and instantly overlay their Speed, Throttle, and Brake traces on their fastest Q3 laps.

## How to Test
The application is currently running locally. 
You can view the interactive dashboard in your browser here:
👉 **[http://localhost:8503](http://localhost:8503)**

*(Note: The first time you load a specific race or attempt to pull Q3 Telemetry, it might take ~10-15 seconds to stream the dense data into the local cache. Subsequent loads are instant.)*
