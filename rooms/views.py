from django.shortcuts import render,redirect
import mysql.connector as m
# Create your views here.
details=[]
abc=[]
p=''
d=''
n=''
def home(request):
    conn=m.connect(host="localhost",user="root",password="aditya",database="HM")
    c=conn.cursor()
    c.execute("create table if not exists users(name varchar(20),email varchar(100) primary key,password varchar(50),pho varchar(15),gender varchar(10))")
    conn.commit()
    c.execute("select * from users")
    k=c.fetchall()
    if k==[]:
        c.execute("insert into users values('{}','{}','{}',{},'{}')".format("Admin","admin","password","NULL","NULL"))
        conn.commit()
        conn.close()
    return render(request,"home.html")

def signup(request):
    conn=m.connect(host="localhost",user="root",password="aditya",database="HM")
    c=conn.cursor()
    p=request.POST.get("pass")
    if p=="password":
        c.execute("create table if not exists transactions(tid int primary key,CName varchar(20),email varchar(30),phoneno varchar(20),dateofbooking varchar(20),rcategory varchar(20),rooms varchar(20),price int,status varchar(30))")
        conn.commit()
        return render(request,"checkin.html")
    else:
        a="Invalid Password"
        return render(request,"home.html",{"err":a})


def addr(request):
    conn=m.connect(host="localhost",user="root",password="aditya",database="hm")
    c=conn.cursor()
    c.execute("create table if not exists rooms(roomno int primary key,category varchar(25),price int)")
    c=AID("rooms")
    return render(request,"rooms.html",{"addr":"1","roomno":c})

def addrooms(request):
    conn=m.connect(host="localhost",user="root",password="aditya",database="hm")
    z=conn.cursor()
    a=request.GET.get("roomno")
    b=request.GET.get("category")
    if b=="Luxury Room":
        c=5000
    elif b=="AC Room":
        c=3000
    else:
        c=1500
    z.execute("insert into rooms values('{}','{}',{})".format(a,b,c))
    conn.commit()
    return redirect("/addr")

def delr(request):
    conn=m.connect(host="localhost",user="root",password="aditya",database="hm")
    z=conn.cursor()
    z.execute("select * from rooms")
    f=z.fetchall()
    conn.commit()
    if f!=[]:
        return render(request,"rooms.html",{"delr":"1","rooms":f})
    else:
        nr="No rooms available"
        return render(request,"rooms.html",{"delr":"1","nr":nr})

def deleteroom(request):
    a="room"
    conn=m.connect(host="localhost",user="root",password="aditya",database="hm")
    z=conn.cursor()
    b=request.GET.get("rno")
    z.execute("delete from rooms where roomno={}".format(b))
    conn.commit()
    return redirect("/delr")

def er(request):
    conn=m.connect(host="localhost",user="root",password="aditya",database="hm")
    z=conn.cursor()
    z.execute("select * from rooms")
    f=z.fetchall()
    conn.commit()
    if f!=[]:
        return render(request,"rooms.html",{"er":"1","rooms":f})
    else:
        nr="No rooms available"
        return render(request,"rooms.html",{"er":"1","nr":nr})

def editrooms(request):
    conn=m.connect(host="localhost",user="root",password="aditya",database="hm")
    acc=request.GET.get("rno")
    z=conn.cursor()
    z.execute("select * from rooms where roomno={}".format(acc))
    f=z.fetchone()
    conn.commit()
    return render(request,"rooms.html",{"er":"1","d":f})

def editroom(request):
    a="room"
    conn=m.connect(host="localhost",user="root",password="aditya",database="hm")
    z=conn.cursor()
    a=request.GET.get("roomno")
    b=request.GET.get("category")
    if b=="Luxury Room":
        c=5000
    elif b=="AC Room":
        c=3000
    else:
        c=1500
    z.execute("update rooms set category='{}',price={} where roomno='{}' ".format(b,c,a))
    conn.commit()
    return redirect("/er")

def searchr(request):
    global abc
    conn=m.connect(host="localhost",user="root",password="aditya",database="hm")
    z=conn.cursor()
    c=request.GET.get("category")
    d=request.GET.get("date")
    z.execute("select roomno from rooms where category='{}' ".format(c))
    f=z.fetchall()
    conn.commit()
    l1=[]
    for i in f:
        for j in i:
            l1.append(j)
    z.execute("select rooms from transactions where rcategory='{}' and dateofbooking='{}' ".format(c,d))
    r=z.fetchall()
    l2=[]
    for i in r:
        for j in i:
            j=j.split(',')
            for k in j:
                if k!="":
                    l2.append(int(k))
    l=[]
    for i in l1:
        if i not in l2:
            l.append(i)
    name=request.GET.get("name")
    id=request.GET.get("id")
    phno=request.GET.get("phno")
    nor=int(request.GET.get("nor"))
    if len(l)>nor or len(l)==nor:
        s=l[0:nor]
        last=s[len(s)-1]
        abc=[name,id,phno,d,c,nor]
        return render(request,"checkin.html",{"rooms":s,"last":last,"l":abc})
    else:
        abc=[name,id,phno,d,c,nor]
        n="Rooms Not Available"
        return render(request,"checkin.html",{"n":n,"l":abc})

def checkinr(request):
    global abc,p
    l=abc[4]
    conn=m.connect(host="localhost",user="root",password="aditya",database="hm")
    z=conn.cursor()
    r=request.GET.get("room")
    if l=="Luxury Room":
        p=5000
    elif l=="AC Room":
        p=3000
    else:
        p=1500
    r=(len(r.split(",")))
    p=p*r
    tid=AID("transactions")
    s="CheckIn"
    z.execute("insert into transactions values({},'{}','{}','{}','{}','{}','{}',{},'{}')".format(tid,abc[0],abc[1],abc[2],abc[3],abc[4],r,p,s))
    conn.commit()
    return redirect('/checkin')

def Checkout(request):
    global d,n
    n=request.GET.get("tid")
    conn=m.connect(host="localhost",user="root",password="aditya",database="hm")
    z=conn.cursor()
    z.execute("select * from transactions where tid={}".format(n))
    f=z.fetchall()
    conn.commit()
    a=f[0]
    d={"Bill Number":a[0],"Customer Name":a[1],"Customer Id":a[2],"Phone Number":a[3],"Date of Booking":a[4],"Room Number":a[6],"Price":a[7]}
    d=d.items()
    z.execute("delete from transactions where tid={}".format(a[0]))
    conn.commit()
    return render(request,"bill.html",{"d":d})
def checkin(request):
    return render(request,"checkin.html")
def checkout(request):
    conn=m.connect(host="localhost",user="root",password="aditya",database="hm")
    c=conn.cursor()
    c.execute("select * from transactions")
    d=c.fetchall()
    if d!=[]:
        return render(request,"checkout.html",{"det":d})
    else:
        return render(request,"checkout.html",{"n":"No Check INs"})
def AID(table):
    conn=m.connect(host="localhost",user="root",password="aditya",database="hm")
    c=conn.cursor()
    c.execute("select * from {}".format(table))
    a=c.fetchall()
    conn.commit()
    if a==[]:
        return 1
    else:
        return a[len(a)-1][0]+1
