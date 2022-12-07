import time
import dbconnect

#user validation
def checkuser(userid):
    db = dbconnect.connection()  
    cursor = db.cursor()
    message = '''SELECT USERID FROM PRODUCT'''
    cursor.execute(message)
    userid2 = int(userid)
    result = cursor.fetchall()
    check = any(userid2 in sublist for sublist in result)
    if check:
        return True
    else:
        return False


#retrieve image
def GetImage(FilePath):
    with open(FilePath, 'rb') as File:
        Image = File.read()
    return Image


#store database image in folder
def StoreImage(FilePath,imagenum):
    Image = GetImage(FilePath)
    db = dbconnect.connection()
    cursor = db.cursor()
    message = "SELECT MAX(ID) FROM PRODUCT"
    cursor.execute(message)
    result = cursor.fetchone()
    id = result[0]
    id += 1
    first = "C:\\Users\\BigMan\\Desktop\\Product Inventory Python Project\\Images\\Product{0}".format(str(id))
    second = 'Image{0}.jpg'.format(str(imagenum))
    fullpath = first + second 
    with open(fullpath, 'ab') as File:
        File.write(Image)
        File.close()


#product validation
def checkproduct(id):
    db = dbconnect.connection()  
    cursor = db.cursor()
    message = '''SELECT ID FROM PRODUCT'''
    cursor.execute(message)
    userid2 = int(id)
    result = cursor.fetchall()
    check = any(userid2 in sublist for sublist in result)
    if check:
        return True
    else:
        return False

#add a product to database
def CreateProduct(request):
    db = dbconnect.connection()
    cursor = db.cursor()
    oldprice = int(0)
    updatedat = 0
    id = 0
    name = request.form['name']
    metaname = name.replace(" ", "_")
    userid = request.form['userid']
    description = request.form['description']
    weight = request.form['weight']
    dimension = request.form['dimensions']
    min = request.form['min']
    max = request.form['max']
    price = request.form['price']
    keys = request.form['keywords']
    keywords = []
    keywords.append(keys)
    status = 'pending'
    createdat = time.asctime(time.localtime(time.time()))

    path1 = request.form['image1']
    path2 = request.form['image2']
    path3 = request.form['image3']
    path4 = request.form['image4']
    path5 = request.form['image5']
    
    if (len(description))>300:
        shortdescription = description[0:301]
    if (len(description))<300:
        shortdescription = description[0:101]
    if (len(description))<100:
        shortdescription = description
    dimensions = dimension.split(',')
    height = int(dimensions[0])
    length = int(dimensions[1])
    breadth = int(dimensions[2])
    weight2 = int(weight)
    min2 = int(min)
    max2 = int(max)
    price2 = int(price)
    userid2 = int(userid)
    if (weight2>10):
        weight2 *= 1000
    #input validations
    list = []
    if bool(name) != 1:
        list.append("Enter product name")
    if bool(request.form['userid']) != 1:
        list.append("Enter userid")
    if bool(description) != 1:
        list.append("Enter description")
    if bool(weight) != 1:
        list.append("Enter weight")
    if bool(dimension) != 1:
        list.append("Enter dimensions:H,L,B")
    if height>100:
        list.append('Exceeded maximum  height of 100m')
    if length>200:
        list.append('Exceeded maximum length of 200m')
    if breadth>300:
        list.append('Exceeded maximum breadth of 300m')
    if bool(min) != 1:
        list.append("Enter minimun quantity to be sold")
    if bool(max) != 1:
        list.append("Enter max quantity to be sold")
    if bool(price) != 1:
        list.append("Enter price of product")
    if bool(keys) != 1:
        list.append("Enter product keywords")
    if bool(path1) != 1:
        list.append("Enter image1")
    if bool(path2) != 1:
            list.append("Enter image2")
    if bool(path3) != 1:
            list.append("Enter image3")
    if bool(path4) != 1:
            list.append("Enter image4")
    if bool(path5) != 1:
            list.append("Enter image5")
    if list:
        return list
    
    image1 = GetImage(path1)
    StoreImage(path1,1)
    image2 = GetImage(path2)
    StoreImage(path2,2)
    image3 = GetImage(path3)
    StoreImage(path3,3)
    image4 = GetImage(path4)
    StoreImage(path4,4)
    image5 = GetImage(path5)    
    StoreImage(path5,5)

    message = '''INSERT INTO PRODUCT VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    data = [id,name,metaname,userid2,description,shortdescription,weight2,dimension,min2,max2,price2,oldprice,image1,image2,image3,image4,image5,keys,status,createdat,updatedat]
    
    
    # try:
    #     cursor.execute(message,data)
    #     db.commit()
    #     return "Successfully stored product in database"
    # except:
    #     db.rollback()
    #     return 'Error storing product in database'

    cursor.execute(message,data)
    db.commit()
    return "Successfully stored product in database"

#cloning an product in database
def DuplicateProduct(request):
    db = dbconnect.connection()  
    cursor = db.cursor()
    id = request.form['id']
    #input validation
    if bool(id) != 1:
        return "Enter product id"
    message = ''' SELECT NAME,METANAME,USERID,DESCRIPTION,SHORTDESCRIPTION,WEIGHT,DIMENSIONS,MINQUANTITY,MAXQUANTITY,PRICE,IMAGE1,IMAGE2,IMAGE3,IMAGE4,IMAGE5,KEYWORDS FROM PRODUCT WHERE ID = %s'''
    message2 = '''INSERT INTO PRODUCT VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    info = [id]
       
    #check if product exists in database
    if (checkproduct(id)) != 1:
        return "This product does not exist in the database"
    cursor.execute(message,info)
    result = cursor.fetchall()
    for row in result:
        name = row[0]
        meta = row[1]
        userid = row[2]
        desc = row[3]
        short = row[4]
        weight = row[5]
        dim = row[6]
        min = row[7]
        max = row[8]
        price = row[9]
        image1 = row[10]
        image2 = row[11]
        image3 = row[12]
        image4 = row[13]
        image5 = row[14]
        keywords = row[15]
            
    productid = 0
    createdat = time.asctime(time.localtime(time.time()))
    updatedat = 0
    oldprice = 0
    status = 'pending'
    data = [productid,name,meta,userid,desc,short,weight,dim,min,max,price,oldprice,image1,image2,image3,image4,image5,keywords,status,createdat,updatedat]
    return data
    try:
        cursor.execute(message2,data)
        db.commit()
        return 'Successfully duplicated product and added to database'
    except:
        db.rollback()
        return 'Error duplicating product'
    
 

#delete a product from the database
def DeleteProduct(request):

    db = dbconnect.connection()  
    cursor = db.cursor()

    prodid = int(request.form['id'])
    userid = request.form['userid']

    #input validations
    list = []
    if bool(prodid) != 1:
        list.append("Enter product id")
    if bool(userid) != 1:
        list.append("Enter userid")
    if list:
        return list

    #check if product exists in database
    if (checkproduct(prodid)) != 1:
        return "This product does not exist in the database"

    #user validation
    if checkuser(userid) != 1:
        return "Error, this user does not exist"

    #check if user has privilege to delete product
    message = ''' SELECT USERID FROM PRODUCT WHERE ID = %s'''
    info = [prodid]
    cursor.execute(message,info)
    trueid = cursor.fetchone()
    true = trueid[0]    
    
    if (str(true) != str(userid)):
        return "You do not have access to delete this product"
    
    message2 = '''DELETE FROM PRODUCT WHERE ID = %s'''

    try:
        cursor.execute(message2,info)
        db.commit()
        return 'This product has been successfully deleted from database'
    except:
        db.rollback()
        return 'Error in deleting this product from database'


#display a specified product in database
def DisplayProduct(request):
    
    db = dbconnect.connection()  
    cursor = db.cursor()
    id = request.form['id']
    #user input validations
    check = []
    if bool(id) != 1:
        check.append("Enter product id")
    if check:
        return check

    #check if product exists in database
    if (checkproduct(id)) != 1:
        return "This product does not exist in the database"
    
    message = '''SELECT ID,NAME,SHORTDESCRIPTION,WEIGHT,DIMENSIONS,PRICE,KEYWORDS FROM PRODUCT WHERE ID =  %s'''
    info = [id]
    list = []
    try:
        cursor.execute(message,info)
        result = cursor.fetchall()

        for row in result:
            id = row[0]
            name = row[1]
            desc = row[2]
            weight = row[3]
            dim = row[4]
            price = row[5]
            key = row[6]
            iddict = {'ID' : str(id)}
            namedict = {'Name': str(name)}
            descdict = {'Description': str(desc)}
            weightdict = {'Weight': str(weight)}
            dimdict = {'Dimensions(H,L,B)': str(dim)}
            pricedict = {'Price': str(price)}
            keydict = {'Keywords': str(key)}
            list.append(iddict)
            list.append(namedict)
            list.append(descdict)
            list.append(weightdict)
            list.append(dimdict)
            list.append(pricedict)
            list.append(keydict)

        return list
    except:
        return "Error fetching product information"

#display all products in database
def DisplayAllProducts():

    db = dbconnect.connection()  
    cursor = db.cursor()
    message = '''SELECT ID,NAME,SHORTDESCRIPTION,WEIGHT,DIMENSIONS,PRICE,KEYWORDS FROM PRODUCT '''
    list = []
    try:
        cursor.execute(message)
        result = cursor.fetchall()

        for row in result:
            id = row[0]
            name = row[1]
            desc = row[2]
            weight = row[3]
            dim = row[4]
            price = row[5]
            key = row[6]
            iddict = {'ID': str(id)}
            namedict = {'Name': str(name)}
            descdict = {'Description': str(desc)}
            weightdict = {'Weight': str(weight)}
            dimdict = {'Dimensions(H,L,B)': str(dim)}
            pricedict = {'Price': str(price)}
            keydict = {'Keywords': str(key)}
            list.append(iddict)
            list.append(namedict)
            list.append(descdict)
            list.append(weightdict)
            list.append(dimdict)
            list.append(pricedict)
            list.append(keydict)

        return list
    except:
        return "Error fetching information on all products"


#admin approval of product
def Approve(request):
    db = dbconnect.connection()
    cursor = db.cursor()
    id = request.form['id']
    message = '''UPDATE PRODUCT SET STATUS = 'APPROVED' WHERE ID = %s'''
    info = [id]
    try:
        cursor.execute(message,info)
        db.commit()
        return "This product has successfully been approved"
    except:
        db.rollback()
        return "Error occurred in approving this product"


#admin declining  product
def Decline(request):
    db = dbconnect.connection()
    cursor = db.cursor()
    id = request.form['id']
    message = '''UPDATE PRODUCT SET STATUS = 'DECLINED' WHERE ID = %s'''
    info = [id]
    try:
        cursor.execute(message,info)
        db.commit()
        return "This product has successfully been declined"
    except:
        db.rollback()
        return "Error occurred in declining this product"

#admin change status of product
def ChangeStatus(request):
    list = []
    if bool(request.form['choice']) != 1:
        list.append("Enter option: approved or declined")
    if bool(request.form['id']) != 1:
        list.append("Enter product id")
    if list:
        return list

    #check if product exists in database
    if (checkproduct(request.form['id'])) != 1:
        return "This product does not exist in the database"

    if (request.form['choice'].lower()) == 'approved':
        return Approve(request)
    elif(request.form['choice'].lower()) == 'declined':
        return Decline(request)
    else:
        return "Invalid input. Enter option: approved or declined"