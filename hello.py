from flask import Flask
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from werkzeug.contrib.fixers import ProxyFix
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE='/tmp/flaskr.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config.from_object(__name__)
joueurs=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Creates the database tables."""
    with app.app_context():
        #db = get_db()
        #with app.open_resource('base.sql', mode='r') as f:
        #    db.cursor().executescript(f.read())
        #db.commit()
        db = get_db()
        for j in range(len(joueurs)/2):
            cur = db.execute("update matchs set j1='" + str(joueurs[j]) + "',j2='" + str(joueurs[15 - j])  + "' where numero=" + str(j + 1))
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()



@app.route('/matches')
def show_entries():
    db = get_db()
    cur = db.execute('select numero, trou, score,j1,j2 from matchs order by id')
    matchs = cur.fetchall()
    return render_template('matches.html', matchs=matchs,joueurs=joueurs)

@app.route('/partie/<partie>/trou/<trou>/score/<score>')
def majdb(partie,trou,score):
    db = get_db()
    cur = db.execute('update matchs set trou=' + str(trou) + ',score=' + str(score) + ' where numero=' + str(partie))
    db.commit()
    cur = db.execute('select j1,j2 from matchs where numero=' + str(partie))
    match=cur.fetchone()
    db = get_db()
    if int(partie) < 9:
        if int(score)>0 and int(partie)%2==1:
            cur = db.execute("update matchs set j1='" + str(match[0]) + "'where numero=" + str(9 + (int(partie)-1)//2))
        if int(score)<0 and int(partie)%2==1:
            cur = db.execute("update matchs set j1='" + str(match[1]) + "'where numero=" + str(9 + (int(partie)-1)//2))
        if int(score)>0 and int(partie)%2==0:
            cur = db.execute("update matchs set j2='" + str(match[0]) +  "'where numero=" + str(9 + (int(partie)-1)//2))
        if int(score)<0 and int(partie)%2==0:
            cur = db.execute("update matchs set j2='" + str(match[1]) +  "'where numero=" + str(9 + (int(partie)-1)//2))
        if int(score)==0 and int(partie)%2==1:
            cur = db.execute("update matchs set j1='' where numero=" + str(9 + (int(partie)-1)//2))
        if int(score)==0 and int(partie)%2==0:
            cur = db.execute("update matchs set j2='' where numero=" + str(9 + (int(partie)-1)//2))
    if int(partie) > 8 and int(partie) < 13:
        if int(score)>0 and int(partie)%2==1:
            cur = db.execute("update matchs set j1='" + str(match[0]) + "'where numero=" + str(9 + (int(partie)-1)//2))
        if int(score)<0 and int(partie)%2==1:
            cur = db.execute("update matchs set j1='" + str(match[1]) + "'where numero=" + str(9 + (int(partie)-1)//2))
        if int(score)>0 and int(partie)%2==0:
            cur = db.execute("update matchs set j2='" + str(match[0]) +  "'where numero=" + str(9 + (int(partie)-1)//2))
        if int(score)<0 and int(partie)%2==0:
            cur = db.execute("update matchs set j2='" + str(match[1]) +  "'where numero=" + str(9 + (int(partie)-1)//2))
        if int(score)==0 and int(partie)%2==1:
            cur = db.execute("update matchs set j1='' where numero=" + str(9 + (int(partie)-1)//2))
        if int(score)==0 and int(partie)%2==0:
            cur = db.execute("update matchs set j2='' where numero=" + str(9 + (int(partie)-1)//2))

    if int(partie) > 12 and int(partie) < 15:
        if int(score)>0 and int(partie)%2==1:
            cur = db.execute("update matchs set j1='" + str(match[0]) + "'where numero=" + str(9 + (int(partie)-1)//2))
        if int(score)<0 and int(partie)%2==1:
            cur = db.execute("update matchs set j1='" + str(match[1]) + "'where numero=" + str(9 + (int(partie)-1)//2))
        if int(score)>0 and int(partie)%2==0:
            cur = db.execute("update matchs set j2='" + str(match[0]) +  "'where numero=" + str(9 + (int(partie)-1)//2))
        if int(score)<0 and int(partie)%2==0:
            cur = db.execute("update matchs set j2='" + str(match[1]) +  "'where numero=" + str(9 + (int(partie)-1)//2))
        if int(score)==0 and int(partie)%2==1:
            cur = db.execute("update matchs set j1='' where numero=" + str(9 + (int(partie)-1)//2))
        if int(score)==0 and int(partie)%2==0:
            cur = db.execute("update matchs set j2='' where numero=" + str(9 + (int(partie)-1)//2))

    db.commit()


    return render_template('mp.html', partie=int(partie),trou=int(trou),score=int(score),joueurA=match[0],joueurB=match[1])

@app.route('/partie/<partie>')
def getmatch(partie):
    db = get_db()
    try:
        cur = db.execute('select trou,score,j1,j2 from matchs where numero=' + str(partie))
        match=cur.fetchone()
        return render_template('mp.html', partie=int(partie),trou=int(match[0]),score=int(match[1]),joueurA=match[2],joueurB=match[3])
    except:
        return render_template('mp.html', partie=int(partie),trou=0,score=0,joueurA="??",joueurB="??")

 
app.wsgi_app = ProxyFix(app.wsgi_app)
 
if __name__ == '__main__':
    init_db()
    app.run()
