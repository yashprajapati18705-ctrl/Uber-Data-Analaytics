# Uber Data Analytics

A comprehensive data analytics dashboard built with Python and Streamlit to analyze Uber ride data. The application provides dataset exploration, business KPIs, advanced visualizations, and a natural language data assistant for interactive insights.

## Features

- Dataset explorer with search and filtering
- Key performance indicators (KPIs)
- Revenue and ride analytics
- Interactive visualizations using Plotly
- Sunburst, Treemap, Box Plot, and Sankey charts
- Data Assistant for answering common business questions
- Download filtered dataset as CSV

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- streamlit-option-menu

## Project Structure
```
Uber-Data-Analytics/
├── uber_analytics.py
├── uber_analytics_dataset.csv
├── users.csv
├── requirements.txt
├── .gitignore
└── README.md
```
## Installation

```bash
git clone https://github.com/yashprajapati18705-ctrl/Uber-Data-Analytics.git
cd Uber-Data-Analytics
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
````

## Run the Project

```bash
streamlit run uber_analytics.py
```

## Dashboard Modules

### Dataset Explorer

* Search and filter data
* View statistics
* Download filtered records

### Overview

* Gross Booking Value
* Fulfilment Rate
* Average Distance
* Customer Ratings

### Ride Analytics

* Sunburst Chart
* Treemap
* Box Plot
* Sankey Diagram

### Data Assistant

Ask questions such as:

* total rides
* revenue
* distance
