def electrical_appliance_comparison(duration):
    # Calculation formula source: https://www.digitaltechnologieshub.edu.au/media/huppewx4/home-energy-use_calculating-ghg-emissions_electricial-appliances.pdf

    # Step 1. Calculate the kilowatt hours (kWh) of your electrical appliance
    # In this example, we will use an average phone charger
    # source: https://www.jackery.com/blogs/knowledge/how-many-watts-is-a-phone-charger#:~:text=A%20regular%20phone%20charger%20uses,5.4%20kiloWatt%20hours%20per%20year.
    '''
    hours: 3 per day
    days: 7 per week
    wattage: 5W based on source
    '''
    kWh = (3 * 7 * 5)/1000

    # Step 2. Next multiply the kilowatt hours (kWh) by the Emissions Factor (EF) for your state
    # source: https://www.ema.gov.sg/resources/singapore-energy-statistics/chapter2
    # EF for Singapore in 2022 is 0.4168 kg CO2/kWh
    EF = 0.4168
    GHG = kWh * EF #GHG refers to greenhouse gas
    
    # Since GHG is in kg CO2, we will convert into g CO2
    grams_GHG = GHG *1000
    
    car_comparison = carbon_emissions_car(duration)
    percentage = (grams_GHG/car_comparison) * 100

    return percentage