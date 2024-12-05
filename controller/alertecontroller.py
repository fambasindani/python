from flask import jsonify, request, send_from_directory, send_file, url_for
from  connexion. myconnection  import get_connection
from flask_bcrypt import Bcrypt
import os
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager, create_access_token
from datetime import datetime



def getadminalertpage(page=1, per_page=10):
    conn = None  # Initialiser conn pour l'utilisation dans finally
    try:
        # Connexion à la base de données
        conn = get_connection()
        cursor = conn.cursor()

        # Calcul de l'offset et de la limite pour la pagination
        offset = (page - 1) * per_page
        limit = per_page

        # Récupération du nombre total de localisations
        cursor.execute("SELECT COUNT(*) FROM localisations")
        total_users = cursor.fetchone()[0]

        # Récupération des données des localisations avec la pagination
        cursor.execute("""
            SELECT id, nom, postnom, prenom, email, avatar , longitude, latitude,longitudeDelta,latitudeDelta
            FROM listelocalisations
            LIMIT %s OFFSET %s
        """, (limit, offset))
        
        users = cursor.fetchall()

        # Conversion des données en format JSON
        user_data = []
        for id, nom, postnom, prenom, email, avatar,longitude, latitude,longitudeDelta,latitudeDelta in users:
            image_url = f'/static/Image/{avatar}'
            user_data.append({
                'id': id,
                'nom': nom,
                'postnom': postnom,
                'prenom': prenom,
                'email': email,
                'avatar': image_url,
                'longitude': longitude,
                'latitude': latitude,
                'longitudeDelta': longitudeDelta,
                'latitudeDelta': latitudeDelta,


                'url': avatar
            })

        # Calcul du nombre total de pages
        total_pages = (total_users + per_page - 1) // per_page

        return {
            'data': user_data,
            'total_pages': total_pages,
            'current_page': page
        }

    except Exception as e:
        print(f"Erreur lors de la récupération des alertes : {str(e)}")
        return {'error': str(e)}
    finally:
        # Assurez-vous de fermer la connexion
        if conn:
            conn.close()
    
        
def getalert():
    try:
        # Connexion à la base de données
        conn = get_connection()
        cursor = conn.cursor()

        # Récupération des données des utilisateurs
        cursor.execute("SELECT id, contenu  FROM typealertes")
        users = cursor.fetchall()

        # Conversion des données en format JSON
        data = []
        for id, contenu,  in users:
          
            data.append({
                'id': id,
                'contenu': contenu,
           
            })

        return data

    except Exception as e:
       
        print(f"Erreur lors de la création de la localisation : {str(e)}")
        return 'Erreur'
    

 
def handle_notifications(socketio):
    conn = None
    cursor = None
    try:
        # Connexion à la base de données
        conn = get_connection()
        cursor = conn.cursor()

        
        temps = datetime.now()
        contenu = request.form.get('contenus')
        id_envoi = request.form.get('envoi_id')
        confiramtion = '1'
        # Récupérer les demandes avec envoi_id et recev_id
        query = "SELECT envoi_id, recev_id FROM demandes WHERE (envoi_id = %s OR recev_id = %s) and confirmation=%s"
        cursor.execute(query, (id_envoi, id_envoi,confiramtion))

        # Récupérer tous les résultats
        demandes = cursor.fetchall()

        # Boucle pour insérer dans la table notifications
        for envoi_id, recev_id in demandes:
            if int(id_envoi) != int(envoi_id):
                # Insertion pour le cas où l'envoi_id est différent
                cursor.execute(
                    "INSERT INTO notifications (envoi_id, recev_id, contenu, datenotification) VALUES (%s, %s, %s, %s)",
                    (envoi_id, recev_id, contenu, temps)
                )
            if int(id_envoi)  != int(recev_id):
                # Insertion pour le cas où le recev_id est différent
                cursor.execute(
                    "INSERT INTO notifications (envoi_id, recev_id, contenu, datenotification) VALUES (%s, %s, %s, %s)",
                    (recev_id, envoi_id,  contenu, temps)
                )
        #print(recev_id)
        # Valider les changements
        conn.commit()

        # Récupérer les utilisateurs pour les notifications
        cursor.execute("SELECT envoi_id, nom, postnom, prenom, email, avatar, telephone, datenotification, contenu FROM listenotifications")
        users = cursor.fetchall()

        # Conversion des données en format JSON
        user_data = []
        for user in users:
            id, nom, postnom, prenom, email, avatar, telephone, datenotification, contenu = user
            image_url = f'/static/Image/{avatar}'

            # Vérification de datenotification
            if datenotification is not None:
                datenotification_str = datenotification.strftime("%Y-%m-%d %H:%M:%S")
            else:
                datenotification_str = None  # Ou une valeur par défaut, par exemple: ""

            user_data.append({
                'envoi_id': id,
                'nom': nom,
                'postnom': postnom,
                'prenom': prenom,
                'email': email,
                'avatar': image_url,
                'telephone': telephone,
                'datenotification': datenotification_str,
                'contenu':contenu,
                'url': avatar
            })

        # Émettre les notifications via SocketIO
        socketio.emit('v', {'data': user_data})

        # Retourner les données au format JSON id_envoi
        return jsonify(user_data)
        #return jsonify(id_envoi)
    except Exception as e:
        # Gérer les erreurs ici
        print(f"Erreur lors du traitement des notifications : {e}")
        return jsonify({'error': str(e)}), 500

    finally:
        # Fermer le curseur et la connexion
        if cursor:
            cursor.close()
        if conn:
            conn.close()




     
def getadminalert():
    try:
        # Connexion à la base de données
        conn = get_connection()
        cursor = conn.cursor()

        # Récupération des données des utilisateurs
        cursor.execute("SELECT id, contenu FROM typealertes")
        alerts = cursor.fetchall()

        # Conversion des données en format JSON
        data = []
        for id, contenu in alerts:
           
            data.append({
                'id': id,
                'contenu': contenu
              
            })

        return data

    except Exception as e:
       
        print(f"Erreur lors de la création de la localisation : {str(e)}")
        return 'Erreur'
                
  
def  create_contenu():
  
    conn = get_connection()
    cur = conn.cursor()

    try:
        contenu = request.form.get('contenu')
        cur.execute("INSERT INTO typealertes (contenu) VALUES (%s)", (contenu,))
        conn.commit()
         
        cur.close()

        return 'Opération effectuée.'

    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la création de contenu : {str(e)}")
        return 'Erreur lors de la création de contenu'
    

def  update_contenu(id):
  
    conn = get_connection()
    cur = conn.cursor()

    try:
        contenu = request.form.get('contenu')
        cur.execute("UPDATE  typealertes SET contenu=%s WHERE id=%s", (contenu,id))
        conn.commit()
         
        cur.close()

        return 'Opération effectuée.'

    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la modification de contenu : {str(e)}")
        return 'Erreur lors de la modification de contenu'
    
  
def delete_contenu(id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Exécutez la commande de suppression
        cur.execute("DELETE FROM typealertes WHERE id=%s", (id,))
        conn.commit()
        
        cur.close()
        
        return 'Utilisateur supprimé avec succès.'

    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la suppression de l'utilisateur : {str(e)}")
        return 'Erreur lors de la suppression de l’utilisateur'