import sqlite3

def all_restaurants():
    db = sqlite3.connect("restaurantmenu.db")
    c=db.cursor()
    query="select * from restaurant"
    c.execute(query)
    return c.fetchall()
    db.close()

def new_restaurant(message):
    db = sqlite3.connect("restaurantmenu.db")
    c=db.cursor()
    n_rest = message[0]
    query="insert into restaurant values (null, '%s')" % n_rest
    c.execute(query)
    db.commit()
    return
    db.close()

def edit_restaurant(oldname, newname):
    db = sqlite3.connect("restaurantmenu.db")
    c=db.cursor()
    o_name = oldname[0]
    n_name = newname[0]
    query="update restaurant set name = '%s' where name = '%s'" % (n_name, o_name)
    print query
    c.execute(query)
    db.commit()
    return
    db.close()