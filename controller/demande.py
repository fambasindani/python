from flask import jsonify, request, send_from_directory, send_file, url_for
from  connexion. myconnection  import get_connection
from flask_bcrypt import Bcrypt
import os
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager, create_access_token
from datetime import datetime

        
    
def getalertpage(page=1, per_page=10, envoi_id=None):
    try:
        # Connexion à la base de données
        conn = get_connection()
        cursor = conn.cursor()

        # Vérification si envoi_id est fourni
        if envoi_id is None:
            raise ValueError("L'ID d'envoi ne peut pas être None.")

        # Récupération du nombre total d'utilisateurs
        cursor.execute("SELECT COUNT(*) FROM notifications WHERE recev_id = %s", (envoi_id,))
        total_users = cursor.fetchone()[0]

        # Calcul de l'offset et de la limite pour la pagination
        offset = (page - 1) * per_page
        limit = per_page

        # Récupération des données des utilisateurs avec la pagination
        cursor.execute("""
            SELECT id, nom, postnom, prenom, email, avatar, telephone, datenotification, contenu,envoi_id, recev_id 
            FROM listenotifications
            WHERE envoi_id = %s
            LIMIT %s OFFSET %s
        """, (envoi_id, limit, offset))
        
        users = cursor.fetchall()

        # Conversion des données en format JSON
        user_data = []
        for id, nom, postnom, prenom, email, avatar, telephone, datenotification,contenu,envoi_id, recev_id  in users:
            image_url = f'/static/Image/{avatar}'
            user_data.append({
                'id': id,
                'nom': nom,
                'postnom': postnom,
                'prenom': prenom,
                'email': email,
                'avatar': image_url,
                'telephone': telephone,
                'datenotification': datenotification.strftime("%Y-%m-%d %H:%M:%S"),
                'contenu': contenu,
                'envoi_id': envoi_id,
                'recev_id': recev_id,
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
    
    
    
def handle_notifications(socketio):
    try:
        # Connexion à la base de données
        conn = get_connection()
        cursor = conn.cursor()

        contenu = "Je suis en danger"
        temps = datetime.now()
        id = "27"  # Assurez-vous que cet ID correspond à une entrée valide dans votre table

        # Récupérer les données des demandes
        query = "SELECT recev_id, envoi_id FROM demandes WHERE envoi_id = %s"
        cursor.execute(query, (id,))  # Exécutez la requête avec l'ID

        # Récupérer tous les résultats
        demandes = cursor.fetchall()

        # Boucle pour insérer dans la table notifications
        for recev_id, envoi_id in demandes:
            cursor.execute(
                "INSERT INTO notifications (recev_id, envoi_id, contenu, datenotification) VALUES (%s, %s, %s, %s)",
                (envoi_id, recev_id, contenu, temps)
            )

        # Valider les changements
        conn.commit()

        # Récupérer les utilisateurs pour les notifications
        cursors = conn.cursor()
        cursors.execute("SELECT envoi_id, nom, postnom, prenom, email, avatar, telephone, datenotification FROM listenotifications")
        users = cursors.fetchall()

        # Conversion des données en format JSON
        user_data = []
        for id, nom, postnom, prenom, email, avatar, telephone,datenotification in users:
            image_url = f'/static/Image/{avatar}'
            user_data.append({
                'envoi_id': id,
                'nom': nom,
                'postnom': postnom,
                'prenom': prenom,
                'email': email,
            
                'avatar': image_url,
                'telephone': telephone,
                'datenotification': datenotification.strftime("%Y-%m-%d %H:%M:%S"),
                'url': avatar
            })

        # Émettre les notifications via SocketIO
       # donnees = request.form.get('donnees')
        socketio.emit('v', {'data': user_data})

        # Retourner les données au format JSON
        return jsonify(user_data)

    except Exception as e:
        # Gérer les erreurs ici
        print(f"Erreur lors du traitement des notifications : {e}")
        return ({'error': str(e)}), 500

    finally:
        # Fermer le curseur et la connexion
        cursor.close()
        conn.close()





def create_demande():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        recev_id = request.form.get('recev_id')
        envoi_id = request.form.get('envoi_id')
        confirmation = "0"
       # datelocalisation = request.form.get('datelocalisation')
        datedemande = datetime.now()
       

        cursor.execute("INSERT INTO demandes (recev_id,envoi_id, datedemande, confirmation) VALUES (%s,%s, %s, %s)", (recev_id,envoi_id, datedemande, confirmation))
        conn.commit()

        return 'demande envoyée'
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la création de la localisation : {str(e)}")
        return "Erreur lors de l'envoi de demande"
      
    
       
def verifierdemande(recev_id):
    try:
        #recev_id = request.form.get('recev_id')
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM demandes WHERE recev_id = %s"
        cursor.execute(query, (recev_id,))
        count = cursor.fetchone()[0]

        if count > 0:
            return('demande')
        
    except Exception as e:
        return(f"Une erreur est survenue : {e}")
     
    