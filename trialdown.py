from flask import*
import sqlite3
import os
app=Flask(__name__)
connect=sqlite3.connect('trial.db')
app.config['UPLOAD_FOLDER']='uploads'
app.config['SECRET_KEY']='abc'
connect.execute('CREATE TABLE IF NOT EXISTS files(id INTEGER PRIMARY KEY AUTOINCREMENT,filename TEXT,filedata BLOB)')
@app.route('/')
def index():
    return render_template('indexpage.html')
@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        file=request.files['file']
        if file:
            filename=file.filename
            filepath=os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(filepath)
            with open(filepath,'rb')as f:
                filedata=f.read()
            with sqlite3.connect('trial.db')as con:
                curr=con.cursor()
                curr.execute('INSERT INTO files(filename,filedata)VALUES(?,?)',(filename,filedata))
                con.commit()
            return redirect(url_for('index'))
    else:
        return render_template('upload.html')
@app.route('/view')
def view():
    with sqlite3.connect('trial.db')as conn:
        cur=conn.cursor()
        cur.execute('SELECT filename,filedata FROM files')
        files=cur.fetchall()
    return render_template('displaypage.html',files=files)
@app.route('/download/<int:id>')
def download(id):
    with sqlite3.connect('trial.db')as con:
        curr=con.execute('SELECT filename,filedata FROM files WHERE id=?',(id,))
        file=curr.fetchone()
        if file:
            filename,filedata=file
        else:
            return "<html><body><h1>file not found</h1></body></html>"
if __name__=='__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)



    
        









    
