import unittest,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.prompts=json.loads((ROOT/'data/prompts.json').read_text());cls.gold=json.loads((ROOT/'data/reference_answers.json').read_text())
 def test_six_cases(self):self.assertEqual(len(self.gold),6)
 def test_unique_ids(self):self.assertEqual(len(set(x['id'] for x in self.gold)),6)
 def test_images_exist(self):
  for p in self.prompts:self.assertTrue((ROOT/p['image']).is_file())
 def test_train_examples(self):
  for g in self.gold:self.assertEqual(len(g['train']),3)
 def test_answer_rectangular(self):
  for g in self.gold:
   a=g['answer'];self.assertTrue(a);self.assertEqual(len(set(map(len,a))),1)
 def test_answers_ints(self):
  for g in self.gold:
   for row in g['answer']:
    for value in row:self.assertIsInstance(value,int);self.assertGreaterEqual(value,0);self.assertLessEqual(value,9)
 def test_dimensions_match(self):
  for g in self.gold:self.assertEqual([len(g['input']),len(g['input'][0])],[len(g['answer']),len(g['answer'][0])])
 def test_score_perfect(self):
  import score
  r={'responses':[{'id':g['id'],'response':json.dumps({'answer':g['answer']})} for g in self.gold]}
  path=ROOT/'results'/'_test_temp.json'
  try:
   path.write_text(json.dumps(r));self.assertEqual(score.evaluate(path)['exact_matches'],6)
  finally:path.unlink(missing_ok=True)
if __name__=='__main__':unittest.main()
