import argparse,json
from pathlib import Path

def evaluate(response_path):
 gold={a['id']:a for a in json.loads(Path('data/reference_answers.json').read_text())}
 data=json.loads(Path(response_path).read_text(encoding='utf-8-sig'))
 results=[]
 for entry in data['responses']:
  id=entry['id'];raw=entry['response']
  if not raw:results.append({'id':id,'status':'NOT_TESTED'});continue
  try:
   obj=json.loads(raw) if isinstance(raw,str) else raw
   candidate=obj['answer'];expected=gold[id]['answer']
   valid=(isinstance(candidate,list) and all(isinstance(row,list) for row in candidate))
   same_shape=valid and len(candidate)==len(expected) and all(len(a)==len(b) for a,b in zip(candidate,expected))
   total=sum(map(len,expected));matched=sum(a==b for rowa,rowb in zip(candidate,expected) for a,b in zip(rowa,rowb)) if same_shape else 0
   exact=(same_shape and candidate==expected)
   results.append({'id':id,'status':'SCORED','exact_match':exact,'dimension_match':same_shape,'matched_cells':matched,'total_cells':total,'cell_accuracy':round(100*matched/total,2),'score':100 if exact else 0})
  except Exception as e:results.append({'id':id,'status':'INVALID','error':str(e),'score':0})
 done=[x for x in results if x['status']!='NOT_TESTED']
 return {'completed':len(done),'total':len(results),'exact_matches':sum(x.get('exact_match',False) for x in done),'results':results}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--responses',default='results/model_responses.json');p.add_argument('--output',default='results/scores.json');args=p.parse_args()
 report=evaluate(args.responses);Path(args.output).write_text(json.dumps(report,indent=2)+'\n')
 print(f"Completed {report['completed']}/{report['total']} | exact matches {report['exact_matches']}/{report['completed']}")
 for x in report['results']:print(x['id'],x['status'],('PASS' if x.get('exact_match') else 'FAIL') if x['status']=='SCORED' else '',x.get('cell_accuracy',''))
 print('Report:',args.output)
