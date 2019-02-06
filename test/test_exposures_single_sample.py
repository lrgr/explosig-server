import requests
import json
import unittest

from constants_for_tests import *

class TestExposuresSingleSample(unittest.TestCase):

    def test_exposures_single_sample(self):
        url = API_BASE + '/plot-exposures-single-sample'
        payload = {
            "sample_id": "TCGA-BRCA_BRCA_mc3.v0.2.8.WXS TCGA-AN-A046-01A-21W-A050-09", 
            "projects": [
                "TCGA-BRCA_BRCA_mc3.v0.2.8.WXS"
            ], 
            "signatures": [
                "COSMIC 1",
                "COSMIC 2",
                "COSMIC 3",
                "COSMIC 4",
                "COSMIC 5",
                "COSMIC 6",
                "COSMIC 7",
                "COSMIC 8",
                "COSMIC 9",
                "COSMIC 10",
                "COSMIC 11",
                "COSMIC 12",
                "COSMIC 13",
                "COSMIC 14",
                "COSMIC 15",
                "COSMIC 16",
                "COSMIC 17",
                "COSMIC 18",
                "COSMIC 19",
                "COSMIC 20",
                "COSMIC 21",
                "COSMIC 22",
                "COSMIC 23",
                "COSMIC 24",
                "COSMIC 25",
                "COSMIC 26",
                "COSMIC 27",
                "COSMIC 28",
                "COSMIC 29",
                "COSMIC 30"
            ],
            "mut_type": "SBS",
            "tricounts_method": "None"
        }
        r = requests.post(url, data=json.dumps(payload))
        r.raise_for_status()
        res = r.json()

        self.assertEqual(30, len(res))
        self.assertEqual({'sig_SBS', 'exp_SBS_TCGA-BRCA_BRCA_mc3.v0.2.8.WXS TCGA-AN-A046-01A-21W-A050-09'}, set(res[0].keys()))
        self.assertEqual('COSMIC 1', res[0]['sig_SBS'])
        self.assertAlmostEqual(108.97955986816336, res[0]['exp_SBS_TCGA-BRCA_BRCA_mc3.v0.2.8.WXS TCGA-AN-A046-01A-21W-A050-09'])
