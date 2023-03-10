from flask import Flask, redirect, url_for, request, Response
from controller import run_terraform as apply
import json
app = Flask(__name__)

def getBluePrint(blueprintname):
   with open(f'{blueprintname}.json') as f:
      bp = json.load(f)
      return bp

@app.route('/iam/aws/oidc/addprovider',methods = ['POST'])
def addProvider():
   if request.method == 'POST':
    req = request.json
    #TODO Input validations
    #TODO update existing roles
    roles = getBluePrint(req['blueprint'])
    res=[]
    for role in roles:
      res.append(apply(req,role))
    return Response(res)
   else:
      return Response(
        "Invalid Method",
        status=405,
    )

if __name__ == '__main__':
   app.run(debug = True)