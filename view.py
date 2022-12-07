from __future__ import print_function
from flask import Flask,request
import controller

app = Flask(__name__)

@app.route('/createproduct', methods=['POST'])
def createproduct():
    return controller.CreateProduct(request)

@app.route('/changestatus', methods=['POST'])
def changestatus():
    return controller.ChangeStatus(request)

@app.route('/duplicateproduct', methods=['POST'])
def duplicateproduct():
    return controller.DuplicateProduct(request)

@app.route('/displayproduct', methods=['GET'])
def displayproduct():
    return controller.DisplayProduct(request)
 
@app.route('/displayallproducts', methods=['GET'])
def displayuser():
    return controller.DisplayAllProducts()

@app.route('/deleteproduct', methods=['DELETE'])
def deleteproduct():
    return controller.DeleteProduct(request)


    
if __name__ == '__main__':
    app.run(debug=True,port=5000)

    
