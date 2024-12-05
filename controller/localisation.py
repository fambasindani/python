from  connexion. myconnection  import get_connection
from flask import Flask, render_template, request, jsonify
from datetime import datetime


def create_localisation():
    try:
        
     
    
        iduser = request.form.get('iduser')
        longitude = request.form.get('longitude')
        latitude = request.form.get('latitude')
        longitudeDelta= request.form.get('longitudeDelta')
        latitudeDelta= request.form.get('latitudeDelta')
        datep = datetime.now()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM localisations WHERE iduser = %s", (iduser,))
        count = cursor.fetchone()[0]

        if count > 0:
            cursor.execute("UPDATE localisations SET  longitude=%s, latitude=%s, datelocalisation=%s, longitudeDelta=%s, latitudeDelta=%s  WHERE iduser=%s", (longitude, latitude, datep,longitudeDelta,latitudeDelta, iduser))
        else:
            cursor.execute("INSERT INTO localisations (iduser, longitude, latitude, datelocalisation,longitudeDelta, latitudeDelta ) VALUES (%s, %s, %s, %s, %s, %s)", (iduser, longitude, latitude, datep, longitudeDelta,latitudeDelta))

        conn.commit()
        conn.close()

        return ({'message': 'Opération effectuée'}), 200
    except Exception as e:
        return ({'error': f'Erreur lors de la création de la localisation : {str(e)}'}), 500
    
def  recupererid():
    db=get_connection()
    iduser=1

    # Vérifier si l'email existe déjà
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM localisations WHERE iduser = %s", (iduser,))
    count = cur.fetchone()[0]
    #if count > 0:
    return count

   

def update_localisation():
    conn = get_connection()
    cursor = conn.cursor()
    iduser=1

    try:
        iduser = request.form.get('iduser')
        longitude = request.form.get('longitude')
        latitude = request.form.get('latitude')
       # datelocalisation = request.form.get('datelocalisation')
        datep = datetime.now()
  

        cursor.execute("UPDATE localisations SET  longitude=%s, latitude=%s, datelocalisation=%s WHERE iduser=%s", (longitude, latitude, datep, iduser))
        conn.commit()

        return 'update a été effectuée'
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la création de la localisation : {str(e)}")
        return 'Erreur lors de la création de la publication'
    
    
          
def getlocalisation(id):
    try:
        # Connexion à la base de données
        conn = get_connection()
        cursor = conn.cursor()

        # Récupération des données des utilisateurs
        cursor.execute("SELECT id, iduser, latitude,longitude, longitudeDelta, latitudeDelta, nom, postnom, prenom, avatar, telephone FROM listelocalisations Where iduser=%s",(id,))
        users = cursor.fetchall()

        # Conversion des données en format JSON
        data = []
        for id,iduser,latitude, longitude, longitudeDelta,latitudeDelta, nom, postnom, prenom, avatar, telephone in users:
            image_url = f'/static/Image/{avatar}'
            data.append({
                'id': id,
                'iduser': iduser,
                'latitude': latitude,
                'longitude': longitude,
                'longitudeDelta': longitudeDelta,
                'latitudeDelta': latitudeDelta,
                'nom': nom,
                'postnom': postnom,    
                'prenom': prenom,
                'avatar': image_url,
                'telephone': telephone,
                'url':avatar
            })

        return data

    except Exception as e:
       
        print(f"Erreur lors de la création de la localisation : {str(e)}")
        return 'Erreur'
    
                 
def getlocalisationadmin(id):
    try:
        # Connexion à la base de données
        conn = get_connection()
        cursor = conn.cursor()

        # Récupération des données des utilisateurs
        cursor.execute("SELECT id, iduser, latitude,longitude, longitudeDelta, latitudeDelta, nom, postnom, prenom, avatar, telephone FROM listelocalisations Where id=%s",(id,))
        users = cursor.fetchall()

        # Conversion des données en format JSON
        data = []
        for id,iduser,latitude, longitude, longitudeDelta,latitudeDelta, nom, postnom, prenom, avatar, telephone in users:
            image_url = f'/static/Image/{avatar}'
            data.append({
                'id': id,
                'iduser': iduser,
                'latitude': latitude,
                'longitude': longitude,
                'longitudeDelta': longitudeDelta,
                'latitudeDelta': latitudeDelta,
                'nom': nom,
                'postnom': postnom,    
                'prenom': prenom,
                'avatar': image_url,
                'telephone': telephone,
                'url':avatar
            })

        return data

    except Exception as e:
       
        print(f"Erreur lors de la création de la localisation : {str(e)}")
        return 'Erreur'
    
        