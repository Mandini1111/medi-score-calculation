
# Medi Score Calculation
## Background
Write a function to calculate the score for aa patient. This is a simple rule of thumb score used to identify ill patients.
## Introduction

The Mediscore calculation is a python based scoring system
which is designed to assess a patients vital signs and detect their potential health issues.
The following system follows a structured scoring model.
The following features are used to determine the mediscore.

**Respiration rate**, **Saturated oxygen level (SpO2)**, **consciousness**, **body temperature** and **oxygen usage**.

A score for each property is allocated as it is measured. The score for the property reflects how different the measurement is from the range of expected values.

The scores for each property are added together, and 2 additional points are added for patients requiring supplemental oxygen to maintain their oxygen saturation level. This final sum is the Medi score, which ranges from 0 to 14.

## Thought process and Design Decisions

To calculate the Medi score efficiently, I followed these key steps:

1.**Understanding the Requirements**- The code is based on five parameters.It follows a predefined scoring table. And the patients requiring oxygen get additional points.
An alert should be triggered if the score increases by more than 2 in 24 hours.

2.**Choosing a function structure**- I created a function calculate_medi_score()that takes vital signs as input. This validates the inputs to prevent errors. This returns the final score and an alert message if needed.

3.**Handling edge cases**-
Incorrect values (the negatve respiration rate)- trigger validation errors
The function correctly differentiates between patients on oxygen and air
The score system ensures no unfair advantage or miscalculation of the final medi score.

4.**Adding efficiency and readability**
Using **if-elif** conditions for scoring instead of multiple function calls
Adding inline comments for better clarity

# Application Requirements

The Medi score for a patient is the sum of the scores for each property in the following table. Ranges are inclusive.

Your function can either take these measures as separate parameters or take a single struct/object containing these values as attributes/properties.

The Medi score for the patient should be returned as an integer.

| Parameter          | Type   | Description                                      |
|--------------------|--------|--------------------------------------------------|
| respiration_rate    | int    | Breaths per minute (0-50).                       |
| oxygen_saturation   | int    | SpO₂ percentage (0-100).                         |
| consciousness       | int    | 0 for alert, non-zero for confused/unconscious.  |
| temperature         | float  | Body temperature in Celsius (30.0-42.0°C).       |
| air_or_oxygen       | int    | 0 for breathing air, 2 for supplemental oxygen.  |
| cbg (optional)      | float  | Capillary Blood Glucose (mmol/L).                |
| fasting (optional)  | bool   | True if fasting, False if not.                   |
| previous_score (optional) | int | Previous Medi Score (to check for trend alerts). |

# Scoring System

### Respiration_rate

| Range (breaths per min) | Score |
|-------------------------|-------|
| ≤8                      | 3     |
| 9 – 11                   | 2     |
| 12 – 20                  | 0 (Normal) |
| 21 – 24                  | 2     |
| ≥25                      | 3     |

### Oxygen_Saturation

| SpO₂ (%)   | Score (Air) | Score (Oxygen) |
|-------------|-------------|----------------|
| ≤83         | 3           | 3              |
| 84 – 85     | 2           | 2              |
| 86 – 87     | 1           | 1              |
| 88 – 92     | 0 (Normal)  | 1              |
| 93 – 94     | -           | 1              |
| 95 – 96     | -           | 2              |


### Consciousness

| Consciousness | Condition          | Score |
|---------------|--------------------|-------|
| Alert (0)     | -                  | 0     |
| Confused/Unconscious (1) | -          | 3     |


### Temperature 

| Temperature (°C) | Score           |
|------------------|-----------------|
| ≤35.0            | 3               |
| 35.1 – 36.0      | 2               |
| 36.1 – 38.0      | 0 (Normal)      |
| 38.1 – 39.0      | 1               |
| ≥39.1            | 2               |

### CBG when fasting

| CBG (mmol/L)   | Score (Fasting) |
|-----------------|-----------------|
| ≤3.4           | 3               |
| 3.5 – 3.9      | 2               |
| 4.0 – 5.4      | 1               |
| 5.5 – 5.9      | 0               |
| ≥6.0           | 1               |

### CBG 2 hours after eating

| CBG (mmol/L)   | Score (Post-meal) |
|-----------------|-------------------|
| ≤4.5           | 3                 |
| 4.5 – 5.8      | 2                 |
| 5.9 – 7.8      | 1                 |
| 7.9 – 8.9      | 0                 |
| ≥9.0           | 1                 |


## Testing Strategy ##

To ensure accuracy, I wrote unit tests in test_medi_score.py, covering:
1.Normal and extreme values (e.g., very low oxygen, high fever)
2.Patients with and without oxygen
3.Patients with and without consciousness issues
4.Edge cases (invalid inputs should raise errors)

tests are run using,
The repository includes unit tests to validate the scoring system. Run tests using:
<pre>
python -m unittest test_medi_score.py
</pre>

## Example test cases from the code

<pre>import unittest
from medi_score import calculate_medi_score

class TestMediScore(unittest.TestCase):
    def test_normal_case(self):
        self.assertEqual(calculate_medi_score(15, 95, 0, 37.1, 0)[0], 0)

    def test_patient_on_oxygen(self):
        self.assertEqual(calculate_medi_score(17, 95, 0, 37.1, 2)[0], 4)

    def test_severe_case(self):
        self.assertEqual(calculate_medi_score(23, 88, 1, 38.5, 2)[0], 10)

if __name__ == "__main__":
    unittest.main()</pre>

## Challenges and Improvements ##
Challenge: Handling patients on oxygen vs. air required special logic.

Solution: I added conditions to apply different thresholds for oxygen users.

Future Improvement: I could integrate more advanced trend monitoring to predict patient deterioration.
## Bonus Features Implemented ##

I have successfully implemented the bonus requirements as follows:

1.Trend Alerts: If the score increases by more than 2 points in 24 hours, an alert is triggered.

2.Capillary Blood Glucose (CBG) scoring: Additional health monitoring based on fasting/post-meal glucose levels.

3.CBG score integration: The function calculates an additional score based on glucose levels when available.

## Final Thoughts ##

This project was a great opportunity for me to apply structured programming and medical scoring logic.The Medi Score system ensures patients are monitored accurately, and alerts provide an early warning for healthcare professionals. Future improvements could include integrating this system into a real-time monitoring platform with more predictive analytics for patient care.

