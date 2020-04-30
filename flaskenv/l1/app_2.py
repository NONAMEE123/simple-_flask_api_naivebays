from flask import Flask,jsonify,request
app=Flask(__name__)


@app.route('/multi/<int:nbr>',methods=['GET'])
def getmultiplication(nbr):
    return jsonify({"res":nbr*10})  


if __name__ == "__main__":
    app.run(debug=True)



