from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3

itmajor = Flask(__name__)

@itmajor.route("/")
def main():
    return render_template("index.html")

@itmajor.route("/input", methods=["POST"])
def input():
    if request.method=="POST":
            firstname = request.form["fname"]
            lastname = request.form["lname"]
            age = int(request.form["age"])
            con=sqlite3.connect("data.db")
            cur=con.cursor()
            cur.execute("INSERT INTO tbl_personal_data(firstname,lastname,age)values(?,?,?)",(firstname,lastname,age))
            con.commit()
            return redirect(url_for("view"))
            con.close()

@itmajor.route("/results")
def view():
    con=sqlite3.connect("data.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM tbl_personal_data")
    data=cur.fetchall()
    con.close()
    return render_template("results.html", data=data)

@itmajor.route("/edit/<string:id>", methods=["POST","GET"])
def edit(id):
    con=sqlite3.connect("data.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM tbl_personal_data where id=?",(id))
    data=cur.fetchone()
    con.close()

    if request.method=="POST":
        firstname = request.form["fname"]
        lastname = request.form["lname"]
        age = int(request.form["age"]) 
        con=sqlite3.connect("data.db")
        cur=con.cursor()
        cur.execute("UPDATE tbl_personal_data SET firstname=?,lastname=?,age=? WHERE id=?", (firstname,lastname,age,id))
        con.commit()
        return redirect(url_for("view"))
    else:
        return render_template("update.html", data=data)
        con.close()

@itmajor.route("/delete/<string:id>")
def delete(id):
    con=sqlite3.connect("data.db")
    cur=con.cursor()
    cur.execute("DELETE FROM tbl_personal_data WHERE id=?",(id))
    con.commit()
    return redirect(url_for("view"))
    con.close()


if __name__ == "__main__":
    itmajor.run(debug=True)
