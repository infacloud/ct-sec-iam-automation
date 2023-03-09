from flask import Flask, redirect, url_for, request, Response
from controller import run_terraform as apply
app = Flask(__name__)

@app.route('/iam/aws/oidc/addprovider',methods = ['POST'])
def addProvider():
   if request.method == 'POST':
    req = request.json
    #TODO Input validations
    #TODO update existing roles
    res = apply(req)
    return Response(res)
   else:
      return Response(
        "Invalid Method",
        status=405,
    )

if __name__ == '__main__':
   app.run(debug = True)