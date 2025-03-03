def validate_inputs(respiration_rate, oxygen_saturation, consciousness, temperature, air_or_oxygen, previous_score=None):
    """
    Validates the input values to ensure they fall within the acceptable ranges.
    Raises a ValueError if any input is invalid.
    """
    if not isinstance(respiration_rate, int) or not (0 <= respiration_rate <= 50):
        raise ValueError("Respiration rate must be an integer between 0 and 50.")

    if not isinstance(oxygen_saturation, int) or not (0 <= oxygen_saturation <= 100):
        raise ValueError("Oxygen saturation must be an integer between 0 and 100.")

    if not isinstance(consciousness, int) or consciousness < 0:
        raise ValueError("Consciousness must be an integer (0 for alert, non-zero for confusion/unconsciousness).")

    if not isinstance(temperature, (int, float)) or not (30.0 <= temperature <= 42.0):
        raise ValueError("Temperature must be a float between 30.0°C and 42.0°C.")

    if air_or_oxygen not in [0, 2]:
        raise ValueError("Air or oxygen value must be 0 (air) or 2 (oxygen).")

    return True  # All inputs are valid


def calculate_medi_score(respiration_rate, oxygen_saturation, consciousness, temperature, air_or_oxygen, cbg=None, fasting=None, previous_score=None):
    """
    Function to calculate the Medi Score for a patient based on vital signs.
    """
    # Validate Inputs
    validate_inputs(respiration_rate, oxygen_saturation, consciousness, temperature, air_or_oxygen)

    # Initialize score
    score = 0

    # Respiration Rate Scoring
    if respiration_rate <= 8:
        score += 3
    elif 9 <= respiration_rate <= 11:
        score += 2
    elif 12 <= respiration_rate <= 20:
        score += 0  # Normal range
    elif 21 <= respiration_rate <= 24:
        score += 2
    else:
        score += 3

    # Oxygen Saturation (SpO2) Scoring
    if oxygen_saturation <= 83:
        score += 3
    elif 84 <= oxygen_saturation <= 85:
        score += 2
    elif 86 <= oxygen_saturation <= 87:
        score += 1
    elif 88 <= oxygen_saturation <= 92 and air_or_oxygen == 0:
        score += 0  # Normal range on air
    elif 88 <= oxygen_saturation <= 92 and air_or_oxygen == 2:
        score += 0
    elif 93 <= oxygen_saturation <= 94 and air_or_oxygen == 2:
        score += 1
    elif 95 <= oxygen_saturation <= 96 and air_or_oxygen == 2:
        score += 2
    else:  # SpO2 ≥ 97 is normal
        score += 0

    # Consciousness Scoring
    if consciousness != 0:
        score += 3  # If the patient is unconscious/confused

    # Temperature Scoring
    if temperature <= 35.0:
        score += 3
    elif 35.1 <= temperature <= 36.0:
        score += 2
    elif 36.1 <= temperature <= 38.0:
        score += 0  # Normal range
    elif 38.1 <= temperature <= 39.0:
        score += 1
    else:  # Temperature >= 39.1
        score += 2

    # Additional 2 points if the patient is on Oxygen
    if air_or_oxygen == 2:
        score += 2  # Oxygen usage penalty

    # **CBG Scoring (Only if CBG and fasting info are provided)**
    if cbg is not None and fasting is not None:
        if fasting:
            if cbg <= 3.4:
                score += 3
            elif 3.5 <= cbg <= 3.9:
                score += 2
            elif 4.0 <= cbg <= 5.4:
                score += 1
            elif 5.5 <= cbg <= 5.9:
                score += 0
            else:
                score += 1
        else:  # Not fasting (2 hours after eating)
            if cbg <= 4.5:
                score += 3
            elif 4.6 <= cbg <= 5.8:
                score += 2
            elif 5.9 <= cbg <= 7.8:
                score += 1
            elif 7.9 <= cbg <= 8.9:
                score += 0
            else:
                score += 1

    # Check if the patient's Medi Score has increased by more than 2 points
    # compared to the previous score within 24 hours. If so, trigger an alert.
    alert_message = ""
    if previous_score is not None and score - previous_score > 2:
        alert_message = "ALERT: Medi Score increased by more than 2 points in 24 hours!"

    return score, alert_message


if __name__ == "__main__":
    try:
        # Test Case 1 (With CBG)/Bonus
        patient_score1, alert1 = calculate_medi_score(15, 95, 0, 37.1, 0, cbg=5.5, fasting=True)
        print("Patient 1 Medi Score:", patient_score1)
        if alert1:
            print(alert1)

        # Test Case 2 (Without CBG)
        patient_score2, alert2 = calculate_medi_score(17, 95, 0, 37.1, 2)
        print("Patient 2 Medi Score:", patient_score2)
        if alert2:
            print(alert2)

        # Test Case 3 (Without CBG)
        patient_score3, alert3 = calculate_medi_score(23, 88, 1, 38.5, 2)
        print("Patient 3 Medi Score :", patient_score3)
        if alert3:
            print(alert3)

        # Trend Alert Testing/Bonus
        previous_score = 5
        new_score, alert = calculate_medi_score(23, 88, 1, 38.5, 2, cbg=4.0, fasting=True, previous_score=5)
        print(f"New Medi Score: {new_score}")
        if alert:
            print(alert)
    except ValueError as e:
        print("Error:", e)
