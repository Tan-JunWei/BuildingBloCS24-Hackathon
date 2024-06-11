carbon_emission_csv_path = 'historical_emissions.csv'

def load_data():
    try:
        data = pd.read_csv(carbon_emission_csv_path)
        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")

data = load_data()

if data is not None:
    countries = data['Country'].unique() #only unique countries

    years = [int(col) for col in data.columns if col.isdigit()]

    # Plot for each country
    plt.figure(figsize=(15, 8))
    for country in countries:
        country_data = data[data['Country'] == country]
        emissions = country_data.iloc[:, 5:].values.flatten()
        plt.plot(years, emissions, label=country)

    plt.title('CO2 Emissions by Country Over the Years')
    plt.xlabel('Year')
    plt.ylabel('CO2 Emissions (MtCO₂e)')
    plt.xticks(years, rotation=45)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),ncol=6)
    plt.grid(True)
    plt.tight_layout()

    st.pyplot(plt)