import unittest
import re
from datetime import datetime

class pico_placa_predictor(object):

    _picoplaca_interval = [('7:00','9:30'),('16:00','19:30')]
    _picoplaca_day_digit = {0:(1,2),1:(3,4),2:(5,6),3:(7,8),4:(9,0),5:(),6:()}

    def predictor(self, licence_plate_number, date, time):
        '''
        This function predict if a car can be in a road because "pico y placa"
        :param licence_plate_number: license plate number (the full number, not the last digit)
        :param date: the date to verify example: 23/07/2016
        :param time: the time to verify example: 18:20
        '''
        #license plate number must be CCC-XXXX, C is a character, X is a number
        assert re.match('^[a-zA-Z]{3}-[\d]{4}$', licence_plate_number)
        #date must be a valid date whit the format DD/MM/YYYY
        assert re.match('^[\d]{1,2}/[\d]{1,2}/[\d]{4}$', date)
        #time must be a valid time whit the format HH:MM
        assert re.match('^[\d]{1,2}:[\d]{1,2}$', time)
        
        date_time_obj = datetime.strptime(date + time, '%d/%m/%Y%H:%M')
        week_day = date_time_obj.weekday()        
        digit_plate = int(licence_plate_number[7:8])
        
        if digit_plate in self._picoplaca_day_digit[week_day]:
            for interval in self._picoplaca_interval:
                if time >= interval[0] and time <= interval[1]:
                    return False
        
        return True
        
class TestPicoPlaca(unittest.TestCase):


    def test_workday(self):
        test = pico_placa_predictor()
        self.assertFalse(test.predictor('ABC-7776', '7/09/2016', '9:00'))
        self.assertTrue(test.predictor('ABC-7770', '8/09/2016', '17:00'))
        self.assertFalse(test.predictor('ABC-7771', '5/09/2016', '18:40'))
        self.assertTrue(test.predictor('ABC-7775', '28/09/2016', '15:00'))

    def test_weekend(self):
        test = pico_placa_predictor()
        self.assertTrue(test.predictor('ABC-7772', '10/09/2016', '7:00'))
        self.assertTrue(test.predictor('ABC-7779', '11/09/2016', '14:00'))

if __name__ == '__main__':
    unittest.main()