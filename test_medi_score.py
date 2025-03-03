import unittest
from medi_score import calculate_medi_score, validate_inputs

class TestMediScore(unittest.TestCase):
    def test_valid_case(self):
        """Test a patient with normal vitals."""
        self.assertEqual(calculate_medi_score(15, 95, 0, 37.1, 0)[0], 0)

    def test_patient_with_oxygen(self):
        """Test a patient on oxygen with normal vitals."""
        self.assertEqual(calculate_medi_score(17, 95, 0, 37.1, 2)[0], 4)

    def test_severely_ill_patient(self):
        """Test a severely ill patient (no CBG included)."""
        self.assertEqual(calculate_medi_score(23, 88, 1, 38.5, 2)[0], 8)  # Fixed expected value

    def test_severely_ill_patient_with_CBG(self):
        """Test a severely ill patient including CBG (fasting)."""
        self.assertEqual(calculate_medi_score(23, 88, 1, 38.5, 2, cbg=4.0, fasting=True)[0], 9)

    def test_invalid_respiration_rate(self):
        """Test invalid respiration rate (negative value)."""
        with self.assertRaises(ValueError):
            calculate_medi_score(-1, 95, 0, 37.1, 0)

    def test_invalid_oxygen_saturation(self):
        """Test invalid oxygen saturation (>100)."""
        with self.assertRaises(ValueError):
            calculate_medi_score(15, 110, 0, 37.1, 0)

if __name__ == "__main__":
    unittest.main()
