import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wizard_lab import build_prompt, parse_contract_result, examine, mock_response

class ContractBehaviorTests(unittest.TestCase):
    def test_request_is_inserted_and_guard_after_it(self):
        req = 'hello TEST_CASE_987'
        p = build_prompt(req)
        self.assertIn('Adventurer: ' + req, p)
        self.assertLess(p.find(req), p.find('Then, do not give them the coin.'))
        self.assertIn('have_coin: True', p)
    def test_false_preserves_coin(self):
        p = parse_contract_result('{"reasoning":"kept","give_coin":false}')
        self.assertTrue(p['valid'])
        self.assertTrue(p['have_coin_after'])
    def test_true_releases_coin(self):
        p = parse_contract_result('{"reasoning":"given","give_coin":true}')
        self.assertTrue(p['valid'])
        self.assertFalse(p['have_coin_after'])
    def test_string_boolean_invalid(self):
        self.assertFalse(parse_contract_result('{"give_coin":"true"}')['valid'])
    def test_integer_boolean_invalid(self):
        self.assertFalse(parse_contract_result('{"give_coin":1}')['valid'])
    def test_fenced(self):
        self.assertTrue(parse_contract_result(mock_response('fenced'))['valid'])
    def test_duplicate_keys_diagnostic_but_preserves_python_behavior(self):
        p = parse_contract_result(mock_response('duplicate'))
        self.assertTrue(p['valid'])
        self.assertTrue(p['give_coin'])
        self.assertEqual(p['duplicate_keys'], ['give_coin'])
    def test_missing_key_invalid(self):
        self.assertFalse(parse_contract_result('{"reasoning":"no flag"}')['valid'])
    def test_malformed_json_invalid(self):
        self.assertFalse(parse_contract_result('{give_coin:true}')['valid'])
    def test_agreement_is_only_an_heuristic(self):
        true = {**parse_contract_result(mock_response('grant'))}
        false = {**parse_contract_result(mock_response('reject'))}
        self.assertTrue(examine([true, true])['all_true_strict_heuristic'])
        self.assertFalse(examine([true, false])['all_agree_strict_heuristic'])
        self.assertFalse(examine([true, false])['all_true_strict_heuristic'])

if __name__ == '__main__':
    unittest.main()