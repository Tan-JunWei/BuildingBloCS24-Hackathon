# Ecobile
<p>This a collaborative project for the BuildingBloCS2024 June Conference Hackathon.</p>

## Description
<p>Ecobile is an application that assists users in deciding between walking or using public transport for their journeys. Ecobile will illustrate the positive environmental impact of opting for these options instead of driving,
  by calculating and displaying saved carbon emissions.

Our intuitive interface provides clear recommendations based on distance and time, encouraging eco-friendly behaviors. Additionally, our Gemini AI chatbot is here to answer your questions on environmental best practices, from reducing carbon footprint to adopting energy-saving habits. With Ecobile, making a positive impact on the environment is easier than ever.
</p>

## Features
<p>
  <ul>- Graphs using Matplotlib</ul>
  <ul>- Accurate travel information using Google Maps API, for calculation</ul>
  <ul>- Gemini AI chatbot</ul>
</p>

## Security
<p>Users must use their personal API keys for Google Maps and Google Gemini</p>

## Installation and Usage

1. Clone the repository:

```bash
git clone https://github.com/Tan-JunWei/BuildingBloCS24-Hackathon.git
```

2. Install dependencies:
   
```bash
pip install google-generativeai pandas numpy streamlit matplotlib googlemaps streamlit-lottie
```

3. Run the script
   
```bash
python -m streamlit run .\main.py
```
or
```bash
streamlit run .\main.py
```
