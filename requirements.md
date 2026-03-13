



FORMULA 1
ANALYTICS DASHBOARD

Product Requirements Document
Comprehensive Season View  |  Grand Prix View  |  Sprint View  |  Race View








Table of Contents

1. Overview & Purpose
This document defines the full product requirements for an F1 Analytics Dashboard — a multi-view web application providing deep data insight across a full Formula 1 season, each Grand Prix weekend, Sprint weekends, and per-driver analysis.

The dashboard serves three primary personas:
Analysts & data enthusiasts — need granular lap, sector, and telemetry metrics
Casual fans — need narrative-friendly race summaries
Content creators / media — need exportable charts and comparative visualisations

The framework is structured into four hierarchical views:



2. Data Sources & API Layer
2.1 Primary Source — OpenF1 API
OpenF1 is the recommended open-source API providing near-real-time F1 data at 3.7 Hz telemetry sampling. Key endpoints:


2.2 Supplementary — FastF1 / Ergast API
FastF1 (Python) provides additional historical telemetry comparisons and corner metadata. Ergast REST API provides historical season data back to 1950 for trend and record context.

2.3 Data Freshness & Caching Rules
Live session data: poll OpenF1 every 4–10 seconds during active sessions
Post-session: fetch complete session data within 15 minutes of session end
Historical sessions: cache per session in database — never re-fetch completed sessions
Telemetry blobs: cache compressed in object storage (e.g., S3) keyed by session_key + driver


3. Season View
  SEASON VIEW  
The Season View is the top-level entry point covering the complete championship calendar and evolving standings for Drivers and Constructors.

3.1 Championship Standings Module
3.1.1 Driver Championship Table
Current points ranking with delta vs. previous round
Points breakdown per race — colour-coded cells: win = gold, podium = silver, points = green, DNF = red, DNS = grey
Cumulative points chart — line chart with per-driver line, all 20 drivers, filterable by top-N
Points gap to leader — chart showing gap shrinking or widening over rounds
Best and worst round annotation markers on the timeline

3.1.2 Constructor Championship Table
Team points per round with car livery colour coding
Points contribution split: both drivers' share per race — stacked bar per round
Reliability chart: DNF count and reason breakdown per team across season

3.2 Season Calendar & Schedule Module
Grid layout: all rounds as cards — circuit image, country flag, round number, dates
Each card shows: race result (winner/podium if completed), qualifying pole position, fastest lap holder
Sprint weekend badge indicator on applicable rounds (currently 6 per season)
Status tags: Completed | Upcoming | Live
Click-through to Grand Prix View per round

3.3 Performance Trends Module
3.3.1 Driver Metrics Over Season
Average qualifying position per driver by round — line chart
Average finishing position per driver by round
Lap 1 position gained/lost heatmap: all drivers × all rounds
Fastest lap count per driver — bar chart
Points scored from pole vs. non-pole start positions

3.3.2 Team Performance Metrics
Average pit stop time per team across season — bar chart with trend line
Undercut and overcut success rate per team
Tyre strategy diversity index: how frequently teams varied compound choices
Safety car exposure: how many laps per team were neutralised by SC or VSC

3.4 Head-to-Head Teammate Comparison Module
Select any two drivers (defaulting to teammates) for season-long comparison


3.5 Circuit Type Analysis Module
Segments circuits by archetype to reveal team and driver strengths per track category:
High-speed power circuits — Monza, Spa, Baku long straight
Technical slow-speed — Monaco, Singapore, Hungary
Mixed high-downforce — Suzuka, Silverstone, COTA
Street circuits — Monaco, Singapore, Baku, Las Vegas, Jeddah, Miami
Per category metrics: average team performance ranking, average tyre degradation rate, average overtake count, safety car probability.


4. Grand Prix View
  GRAND PRIX VIEW  
The Grand Prix View aggregates the entire race weekend — practice, qualifying, and race (plus Sprint where applicable) — into a unified weekend summary with drill-down capability per session.

4.1 Weekend Overview Header
Circuit name, country, round number, dates
Circuit map (SVG or static image) with DRS zones, pit lane entry/exit, key corner markers and numbers
Circuit characteristics: total lap distance, race lap count, corner count, elevation change, average speed, percentage of lap at full throttle
Weather summary across all sessions: temperature range, dry/wet indicator per session
Sprint weekend indicator: Sprint schedule displayed alongside Race schedule

4.2 Practice Sessions (FP1 / FP2 / FP3)
4.2.1 Session Lap Time Summary
Top-10 fastest lap times per session with driver, tyre compound, and lap number
Lap time progression chart: each driver's best time improvement over session duration
Long-run pace analysis (FP2 focus): exclude push laps, calculate mean long-run pace per driver per compound

4.2.2 Tyre Programme Tracker
Compound usage matrix: which drivers used which sets, on which laps
Performance window analysis: early vs. late stint time delta per compound per team
Degradation estimate: slope of lap time vs. tyre age scatter per compound per team

4.3 Qualifying Module
4.3.1 Qualifying Results Table
Q1 / Q2 / Q3 tabs with: position, driver, team, best lap time, gap to pole, laps run, tyre compound used on best lap
Lap time delta waterfall chart: each driver's time relative to pole — visually shows compression at top and spread at bottom
Fastest lap evolution chart: pole time progression across the session (each flying lap that improves the benchmark)

4.3.2 Sector Analysis — Qualifying
Theoretical best lap: sum of best S1 + S2 + S3 across all drivers — shows time left on the table vs. pole
Sector time heatmap: all drivers × 3 sectors, colour gradient from fastest (green/purple) to slowest (red)
Purple sector indicator: fastest sector in each sector highlighted in F1-standard purple
Speed trap data: top speeds at S1 intermediate, S2 intermediate, finish line, and speed trap locations

4.3.3 Qualifying Telemetry Comparison
Select any two drivers for telemetry overlay on their best qualifying lap:
Speed trace vs. distance along lap (km)
Throttle percentage vs. distance
Brake application vs. distance
Gear selection vs. distance
RPM vs. distance
DRS status (open/closed) vs. distance
Corner annotations on X-axis (corner number and name)
Delta time strip chart: running time delta between the two drivers across the lap
Auto-generated insight callouts: where Driver A gains or loses vs. Driver B (e.g., 'HAM gains 0.12s braking into T4')

4.4 Starting Grid Visualisation
Full 20-car grid with driver name, team colour, car number, qualifying time, gap to pole
Grid penalty indicators: engine penalty, gearbox, pit lane starts — with penalty reason tooltip
Tyre choice indicator: starting compound for each driver
Historical context: how many times pole has converted to a race win at this specific circuit


5. Race View
  RACE VIEW  
The Race View is the most data-dense view. It covers all race dimensions: position changes, lap pace, strategy, tyres, battles, incidents, and driver-level telemetry.

5.1 Race Result & Podium Module
Top-3 podium display: driver photo, team, finish time and gap to winner
Full classified results: position, driver, team, laps completed, race time/gap, points, fastest lap indicator, final tyre compound, status (Classified / DNF / DSQ / DNS / Retired)
DNF summary panel: driver, lap of retirement, reason (engine, crash, mechanical, collision)
Points scored this round — visual delta showing championship position movement per driver

5.2 Race Lap Chart — Position Over Time
The primary race narrative chart and the single most important visualisation in the Race View.
Multi-line chart: X-axis = lap number (1 to end), Y-axis = track position (1–20), inverted so P1 is at top
Each driver = one line, team colour coded
Pit stop markers: vertical tick on each driver's line at pit lap, with tyre compound icon
Safety car and VSC periods: shaded vertical bands across the full chart
Event annotations: incidents, penalties, retirements at the relevant lap
Hover tooltip: driver, position, lap time, gap to leader, tyre compound
Filter controls: show/hide individual drivers, toggle SC bands, highlight selected driver

5.3 Lap Time Analysis Module
5.3.1 Lap Time Chart — Full Race
Line chart: lap time (ms) vs. lap number for all or selected drivers
Outlier lap flagging: SC laps, in-laps, out-laps flagged visually and optionally excluded from pace calculations
Rolling average pace overlay per driver (5-lap window)
Stint colour coding: line colour changes per compound (soft=red, medium=yellow, hard=white, inter=green, wet=blue)

5.3.2 Lap Time Distribution
Box plot or violin plot per driver showing lap time spread across the race
Identifies consistency vs. erratic pace — critical for strategy analysis
Outlier lap labels: indicates reason for slow lap (traffic, SC, yellow flag, technical issue)

5.3.3 Pace Heatmap
Grid: rows = drivers, columns = laps, cell fill = lap time relative to best lap for that lap number
Shows at a glance: who was fast when, where degradation set in, who benefited from SC restart timing

5.4 Strategy & Tyre Module
5.4.1 Tyre Strategy Timeline
Horizontal bar chart: X-axis = laps, Y-axis = drivers
Each segment = one stint, colour = tyre compound
Segment width = stint length in laps
Pit stop gap annotations: stop duration labelled on transition points
Undercut window indicator: calculated optimal undercut lap vs. actual stop lap per driver

5.4.2 Pit Stop Analysis Table


5.4.3 Tyre Degradation Curves
Scatter plot: lap time delta from fresh tyre pace vs. tyre age (laps on compound)
Per compound, per team — shows cliff degradation vs. linear degradation profile
Cross-team overlay: identifies which teams manage a given compound best

5.5 Race Pace & Gap Analysis Module
5.5.1 Gap-to-Leader Chart
Line chart: gap to race leader (seconds) vs. lap for all drivers
Visually identifies: drivers closing on leader, SC compression effect, restart scramble dynamics

5.5.2 Battle Tracker
Identifies on-track battles (within 1 second DRS range) and tracks duration and resolution.
Battle log: attacker, defender, start lap, end lap, duration (laps), DRS activations, outcome (passed / held / retired)
Battle timeline: X-axis = lap, shows which laps each battle was active simultaneously
DRS activation count per driver: total DRS zones where driver had DRS enabled across race

5.5.3 Overtake Log
Complete on-track passes: lap, overtaking driver, defending driver, corner/straight, method (DRS, brake-late, outside pass, undercut)
Overtake heatmap on circuit map: highlights which corners and straights saw the most passes
Net position gained per driver: lap 1 chaos vs. in-race overtaking vs. pit strategy — split attribution

5.6 Driver Performance Deep-Dive Module
5.6.1 Sector Analysis — Race
Sector 1, 2, 3 average pace per driver — excluding SC laps, in-laps, out-laps
Mini-sector heat strip on circuit map: each mini-sector colour coded by relative pace
Theoretical best race lap: sum of best S1 + S2 + S3 achieved in any single lap of the race

5.6.2 Speed Analysis
Top speed distribution per driver: box plot of all speed trap readings across the race
Straight-line speed in each DRS zone: per driver maximum speed comparison
Average cornering speed per key corner (derived from position data)

5.6.3 Fastest Lap Telemetry Comparison
Same telemetry overlay structure as qualifying but applied to any selected race lap. Enables:
Driver A's fastest race lap vs. Driver B's fastest race lap — head-to-head pace
Driver's fastest race lap vs. their own qualifying lap — fuel load and tyre adjusted pace delta
Same driver: early stint lap vs. late stint lap — degradation and fuel effect visualisation

5.7 Incident & Race Control Log
Chronological log of all race control messages: flag status, SC deployment, VSC, DRS enable/disable, penalties, investigations
Penalty table: driver, penalty type, reason, lap applied, time added or positions dropped
Safety car effect analysis: estimated time delta vs. no-SC scenario for top-5 runners

5.8 Weather Module
Time-series overlay on the lap chart: air temp, track temp, wind speed
Rainfall indicator: lap-by-lap rain sensor data or probability estimate
Weather-tyre correlation: flags laps where changing conditions may have influenced compound choice


6. Sprint View
  SPRINT VIEW  
The Sprint View is active for the 6 Sprint weekend rounds per season. It contains two sub-views: Sprint Qualifying (SQ) and Sprint Race. Sprint sessions have unique characteristics — no mandatory tyre, limited distance (~100km), direct championship points, and no pit stops in the sprint race.

6.1 Sprint Weekend Context Panel
Sprint schedule timeline: SQ1 / SQ2 / SQ3 and Sprint Race timing within the full weekend
Points on offer: Sprint Race points allocation (8 pts for P1 down to 1 pt for P8)
Regulation note: free tyre choice in Sprint Qualifying, parc ferme conditions apply after SQ3
Championship stakes panel: current standings with projected points delta after sprint

6.2 Sprint Qualifying (SQ)
6.2.1 SQ1 / SQ2 / SQ3 Results
Identical sector analysis and results table structure as main qualifying (see Section 4.3)
Key regulatory difference callout: no mandatory tyre compound in SQ — compound choices displayed prominently
Elimination markers: SQ1 eliminates P16–20, SQ2 eliminates P11–15
Sprint grid: final grid order after SQ3 with starting tyre compound per driver

6.2.2 SQ Telemetry
All qualifying telemetry overlays apply (Section 4.3.3)
Additional comparison: SQ best lap vs. main qualifying best lap for the same driver — reveals setup and priority tradeoffs

6.3 Sprint Race
The Sprint Race covers 17–19 laps depending on circuit. Analysis is a focused version of the Race View with Sprint-specific insight additions.

6.3.1 Sprint Race Result
Classified results: finish position, driver, team, race time/gap, points scored, fastest lap, tyre at finish
P1–P8 points display: highlighted separately as these are championship-relevant
Regulation note: fastest lap bonus point does not apply in Sprint Race

6.3.2 Sprint Lap Chart
Same structure as Race Lap Chart (Section 5.2) adapted for sprint length
Lap 1 expanded view: zoomed-in position change detail for opening lap
No pit stop markers (Sprint Race is no-pit in normal conditions)

6.3.3 Sprint Pace Analysis
Lap time chart: all drivers across all sprint laps
No pit stop variable — pure pace and tyre degradation analysis on a single stint
Sprint pace vs. qualifying pace delta: does SQ pace predict sprint race performance?
Tyre life projection to end of sprint: how much degradation to lap 18 on chosen compound — informs main race tyre strategy

6.3.4 Sprint vs. Race Pace Correlation
Unique cross-session intelligence module correlating sprint data with main race outcome:
Scatter plot: sprint race average pace (ms/lap) vs. main race average pace per driver
Trend line and R-squared value to quantify how predictive sprint pace is for race outcome
Driver callouts: who over or under-performs relative to sprint baseline in the main race

6.3.5 Overtake & Battle Analysis — Sprint
Same Battle Tracker and Overtake Log structure as Race View (Section 5.5.2 and 5.5.3)
Sprint-specific context: without pit stops, all position changes are on-track passes — higher purity for overtake analysis
Overtake efficiency: ratio of DRS passes vs. non-DRS passes
Lap 1 position change leaderboard: drivers who gained or lost the most in the opening lap


7. Cross-View Analytics & Insight Engine
Beyond per-view analysis, the dashboard surfaces intelligence features automatically across views.

7.1 Automated Insight Cards
Post-session, the system generates narrative insight cards at the top of each view:
Pace insight example: 'Norris's Sector 2 was 0.3s faster than the field average across 14 consecutive laps — exceptional mid-corner speed'
Strategy insight example: 'McLaren's undercut on Lap 32 was worth 1.2s net — the decisive strategic call of the race'
Fastest lap example: 'Russell missed the fastest lap bonus point by 0.034s on the penultimate lap'
Sprint-to-race prediction: 'Sprint tyre data suggests Ferrari will struggle on a one-stop strategy on Sunday'

7.2 Driver Consistency Score
A composite index per driver per session computed from:
Lap time standard deviation (normalised — lower is more consistent)
Sector time consistency across comparable laps (same compound, same fuel load window)
Qualifying vs. race pace delta relative to team average
Displayed as a 0–100 index with percentile ranking vs. field and vs. teammate.

7.3 Strategy Effectiveness Rating
Post-race team strategy rating per driver:
Undercut timing accuracy: how close to the optimal window did the team pit?
Track position vs. pace tradeoff: did the team sacrifice position for better tyres and was it correct?
Pit stop execution: stationary time vs. team's season average
Net positions gained or lost attributable purely to pit strategy decisions

7.4 Historical Context Lookup
Any metric in any view can be clicked to see historical context:
Fastest ever pole at this circuit vs. today's pole time
Most overtakes in a race at this circuit historically
Driver's best historical finish at this circuit
Team's historical win rate at this specific circuit


8. UI / UX Requirements
8.1 Navigation Structure

8.2 Visual Design System
Theme: dark mode primary (background #15151E per F1 brand), with light mode toggle
Team colours: official HEX codes per team applied to driver lines, sector highlights, tyre indicators
Tyre compound colours: Soft = Red, Medium = Yellow, Hard = White/Grey, Intermediate = Green, Wet = Blue (FIA standard palette)
Typography: monospace font for all lap times and sector times; sans-serif for labels and navigation
Charts: responsive, zoomable (pinch/scroll), hover tooltips with full data on all chart points
Mobile: Season View and results tables fully supported; full telemetry analysis on desktop only

8.3 Filters & Controls
Global driver filter: show or hide individual drivers across all charts in current view
Lap range filter: analyse any sub-section of a race (e.g., laps 30–55 post-safety car)
Tyre compound filter: isolate all analysis to a single compound
Outlier laps toggle: exclude SC laps, in-laps, out-laps from all pace calculations
Compare mode: select any two sessions, drivers, or rounds for side-by-side layout

8.4 Export & Sharing
Export any chart as PNG or SVG
Export data tables as CSV
Shareable URL: current view state encoded in URL params (selected drivers, lap range, chart type)
Embed code (iframe) for charts — for media and content creator use case


9. Metrics & Data Dictionary
Complete glossary of metrics used across all dashboard views:



10. Recommended Tech Stack


11. Build Priority & Phasing
Phase 1 — Core MVP
Season View: standings table, calendar grid, cumulative points chart
Grand Prix View: weekend overview, qualifying results table, race result table
Race View: lap chart (position over time), tyre strategy timeline, pit stop table
Data layer: OpenF1 integration, session caching, basic derived metrics

Phase 2 — Analytical Depth
Race View: pace heatmap, sector analysis, gap-to-leader chart, battle tracker, overtake log
Grand Prix View: sector heatmap, qualifying telemetry comparison, FP long-run analysis
Season View: H2H module, performance trends, circuit type analysis
Sprint View: full SQ and Sprint Race views with pace analysis

Phase 3 — Intelligence Layer
Automated insight cards per session
Driver consistency score and strategy effectiveness rating
Historical context lookup on any metric
Sprint vs. Race pace correlation module
Export, shareable URL, and embed features
Mobile-optimised layouts for Season and Results views

Document v1.0  |  Primary data source: OpenF1 API (open-source, openf1.org)  |  F1 Analytics Dashboard Product Requirements
