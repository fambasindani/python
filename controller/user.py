from flask import jsonify, request, send_from_directory, send_file, url_for
from  connexion. myconnection  import get_connection
from flask_bcrypt import Bcrypt
import os
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager, create_access_token


from flask_socketio import SocketIO, join_room, emit
#select users.id AS id,  users.nom AS  nom , users.postnom  AS postnom ,  users.prenom AS  prenom ,  users.password AS password , users.email AS  email ,  users.avatar  AS  avatar , users.telephone  AS  telephone from  users  where !(users.id in (select demandes.recev_id  from   demandes   where  demandes.envoi_id = '1'))




def downloadi():
    
   
    conn = get_connection()
    cursor = conn.cursor()
    
  
    #query = "SELECT * FROM fichiers WHERE id = %s"
    #cursor.execute(query, (id,))
    #file_info = cursor.fetchone()

    #cursor.close()
   

    #return  file_info[1]
   
      
def download_pdf(id):
    # Récupérer le nom du fichier PDF à partir de la base de données
    cursor = db.cursor()
    query = "SELECT * FROM fichiers WHERE id = %s"
    cursor.execute(query, (id,))
    fiche = cursor.fetchone()
    filename=fiche[1]

    if filename:
        # Construire le chemin absolu du fichier PDF en ajoutant le dossier "mesfichiers"
        file_path = os.path.join(os.path.dirname(__file__), 'GsCarriere/mesfichiers', filename)
        file_paths = os.path.normpath(file_path)


        # Vérifier si le fichier existe
        if os.path.isfile(file_path):
            # Envoyer le fichier PDF en tant que réponse
            return send_file(file_path, mimetype='application/pdf', as_attachment=True)
        else:
            #return "Le fichier demandé n'existe pas.", 404
            return jsonify(file_paths) 
    else:
        return "Le fichier demandé n'existe pas.", 404
      # return  jsonify("famba")
    
    
def verifieremail():
    try:
        email = request.form.get('email')
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        count = cursor.fetchone()[0]

        if count > 0:
            return('email')
        else:
            return("email n'existe pas")
    except Exception as e:
        return(f"Une erreur est survenue : {e}")
     
  
def getuserss():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users")
        objets = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        data = [dict(zip(headers, row)) for row in objets]

        user_dir = os.path.expanduser("~")
        image_path = os.path.join(user_dir, 'Downloads', 'Securite_sociale', 'BD', 'Image', 'user.png')
        #image_url = url_for('static', filename=os.path.relpath(image_path, app.static_folder))
        #return image_path
       # return {'data': data, 'image_url': image_path}
    finally:
        cursor.close()
        conn.close()
        
        
        
 
        
def getuser():
    try:
        # Connexion à la base de données
        conn = get_connection()
        cursor = conn.cursor()

        # Récupération des données des utilisateurs
        cursor.execute("SELECT id, nom, postnom, prenom, email, password, avatar, telephone FROM listeamis")
        users = cursor.fetchall()

        # Conversion des données en format JSON
        data = []
        for id, nom, postnom, prenom, email, password, avatar, telephone in users:
            image_url = f'/static/Image/{avatar}'
            data.append({
                'id': id,
                'nom': nom,
                'postnom': postnom,    
                'prenom': prenom,
                'email': email,
                'password': password,
                 'avatar': image_url,
                'telephone': telephone,
                'url':avatar
            })

        return data

    except Exception as e:
       
        print(f"Erreur lors de la création de la localisation : {str(e)}")
        return 'Erreur'
    


def activer():
    conn = get_connection()
    cur = conn.cursor()
    id = request.form.get('id') 
    role = request.form.get('role') 
    monrole=int(role)
    try:
        # Compter les utilisateurs avec le rôle 1
       # cur.execute("SELECT COUNT(*) FROM users WHERE role=%s", (1,))
       # count = cur.fetchone()[0]

        if monrole == 0:
            # Mettre à jour le rôle à 3
            cur.execute("UPDATE users SET role=%s WHERE id=%s", (2, id))
            message = 'Rôle mis à jour à 3.'
        elif monrole==2:
            # Mettre à jour le rôle à 1
            cur.execute("UPDATE users SET role=%s WHERE id=%s", (0, id))
            message = 'Rôle mis à jour à 1.'
         

        conn.commit()
        return {'message': message}, 200

    except Exception as e:
        conn.rollback()
        print(f"Opération échouée : {str(e)}")
        return {'error': 'Opération échouée.'}, 500

    finally:
        cur.close()
        conn.close()




def getall(page=1, per_page=10):
    try:
        # Connexion à la base de données
        conn = get_connection()
        cursor = conn.cursor()
       
        # Récupération du nombre total d'utilisateurs
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        # Calcul de l'offset et de la limite pour la pagination
        offset = (page - 1) * per_page
        limit = per_page

        # Récupération des données des utilisateurs avec la pagination
        cursor.execute("SELECT users.id AS id, users.nom AS nom, users.postnom AS postnom, users.prenom AS prenom, users.email AS email, users.avatar AS avatar, users.telephone AS telephone, role FROM users where id!=%s LIMIT %s OFFSET %s",(1,limit, offset))
     

        
        users = cursor.fetchall()

        # Conversion des données en format JSON
        user_data = []
        for id, nom, postnom, prenom, email, avatar, telephone, role in users:
            image_url = f'/static/Image/{avatar}'
            user_data.append({
                'id': id,
                'nom': nom,
                'postnom': postnom,    
                'prenom': prenom,
                'email': email,
                'role': role,
                 'avatar': image_url,
                'telephone': telephone,
                'url':avatar
            })

        # Calcul du nombre total de pages
        total_pages = (total_users + per_page - 1) // per_page

        return {
            'data': user_data,
            'total_pages': total_pages,
            'current_page': page
        }

    except Exception as e:
        print(f"Erreur lors de la création de la localisation : {str(e)}")
        return 'Erreur'    
    
     
    
def getuserpage(page=1, per_page=10, envoi_id=None):
    try:
        # Connexion à la base de données
        conn = get_connection()
        cursor = conn.cursor()
        id=1
        # Récupération du nombre total d'utilisateurs
        cursor.execute("SELECT COUNT(*) FROM users WHERE users.id NOT IN (SELECT demandes.recev_id FROM demandes WHERE demandes.envoi_id = %s)", (envoi_id,))
        total_users = cursor.fetchone()[0]

        # Calcul de l'offset et de la limite pour la pagination
        offset = (page - 1) * per_page
        limit = per_page

        # Récupération des données des utilisateurs avec la pagination
        cursor.execute("""
    SELECT u.id AS id, 
           u.nom AS nom, 
           u.postnom AS postnom, 
           u.prenom AS prenom, 
           u.email AS email, 
           u.password AS password, 
           u.avatar AS avatar, 
           u.telephone AS telephone 
    FROM users u 
    WHERE u.id NOT IN (
        SELECT d.envoi_id 
        FROM demandes d 
        WHERE d.recev_id = %s
    ) 
    AND u.id NOT IN (
        SELECT d.recev_id 
        FROM demandes d 
        WHERE d.envoi_id = %s
    )
    LIMIT %s OFFSET %s
""", (envoi_id, envoi_id, limit, offset))
        
        users = cursor.fetchall()

        # Conversion des données en format JSON
        user_data = []
        for id, nom, postnom, prenom, email, password, avatar, telephone in users:
            image_url = f'/static/Image/{avatar}'
            user_data.append({
                'id': id,
                'nom': nom,
                'postnom': postnom,    
                'prenom': prenom,
                'email': email,
                'password': password,
                 'avatar': image_url,
                'telephone': telephone,
                'url':avatar
            })

        # Calcul du nombre total de pages
        total_pages = (total_users + per_page - 1) // per_page

        return {
            'data': user_data,
            'total_pages': total_pages,
            'current_page': page
        }

    except Exception as e:
        print(f"Erreur lors de la création de la localisation : {str(e)}")
        return 'Erreur'    
    
    
   
    
def getadminpage(page=1, per_page=10, envoi_id=None):
    try:
        # Connexion à la base de données
        conn = get_connection()
        cursor = conn.cursor()
        role="1"
        # Récupération du nombre total d'utilisateurs
        cursor.execute("SELECT COUNT(*) FROM users WHERE users.id NOT IN (SELECT demandes.recev_id FROM demandes WHERE demandes.envoi_id = %s)", (envoi_id,))
        total_users = cursor.fetchone()[0]

        # Calcul de l'offset et de la limite pour la pagination
        offset = (page - 1) * per_page
        limit = per_page

        # Récupération des données des utilisateurs avec la pagination
        cursor.execute("""
    SELECT u.id AS id, 
           u.nom AS nom, 
           u.postnom AS postnom, 
           u.prenom AS prenom, 
           u.email AS email, 
           u.password AS password, 
           u.avatar AS avatar, 
           u.telephone AS telephone 
    FROM users u 
    WHERE u.id NOT IN (
        SELECT d.envoi_id 
        FROM demandes d 
        WHERE d.recev_id = %s
    ) 
    AND(
         u.role=%s            
        )
    AND u.id NOT IN (
        SELECT d.recev_id 
        FROM demandes d 
        WHERE d.envoi_id = %s
    )
    LIMIT %s OFFSET %s
""", (envoi_id, role, envoi_id, limit, offset))
        
        users = cursor.fetchall()

        # Conversion des données en format JSON
        user_data = []
        for id, nom, postnom, prenom, email, password, avatar, telephone in users:
            image_url = f'/static/Image/{avatar}'
            user_data.append({
                'id': id,
                'nom': nom,
                'postnom': postnom,    
                'prenom': prenom,
                'email': email,
                'password': password,
                 'avatar': image_url,
                'telephone': telephone,
                'url':avatar
            })

        # Calcul du nombre total de pages
        total_pages = (total_users + per_page - 1) // per_page

        return {
            'data': user_data,
            'total_pages': total_pages,
            'current_page': page
        }

    except Exception as e:
        print(f"Erreur lors de la création de la localisation : {str(e)}")
        return 'Erreur'    
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def getuserpageddd(page=1, per_page=10, envoi_id=None):
    try:
        # Connexion à la base de données
        conn = get_connection()
        cursor = conn.cursor()

        # Récupération du nombre total d'utilisateurs
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        # Calcul de l'offset et de la limite pour la pagination
        offset = (page - 1) * per_page
        limit = per_page

        # Récupération des données des utilisateurs avec la pagination
        #cursor.execute("SELECT id, nom, postnom, prenom, email, password, avatar, telephone FROM listeamis LIMIT %s OFFSET %s", (limit, offset))
       
        cursor.execute("SELECT users.id AS id, users.nom AS nom, users.postnom AS postnom, users.prenom AS prenom, users.password AS password, users.email AS email, users.avatar AS avatar, users.telephone AS telephone FROM users WHERE users.id NOT IN (SELECT demandes.recev_id FROM demandes WHERE demandes.envoi_id = %s and confirmation!=2 )LIMIT %s OFFSET %s", (limit, offset,envoi_id)),
    
       
       
        users = cursor.fetchall()

        # Conversion des données en format JSON
        user_data = []
        for id, nom, postnom, prenom, email, password, avatar, telephone in users:
            image_url = f'/static/Image/{avatar}'
            user_data.append({
                'id': id,
                'nom': nom,
                'postnom': postnom,    
                'prenom': prenom,
                'email': email,
                'password': password,
                 'avatar': image_url,
                'telephone': telephone,
                'url':avatar
            })

        # Calcul du nombre total de pages
        total_pages = (total_users + per_page - 1) // per_page

        return {
            'data': user_data,
            'total_pages': total_pages,
            'current_page': page
        }

    except Exception as e:
        print(f"Erreur lors de la création de la localisation : {str(e)}")
        return 'Erreur'
    
    
    
    
    
    
     
    
def  update_users(id):
    #bcrypt = Bcrypt()
    conn = get_connection()
    cur = conn.cursor()

    try:
        nom = request.form.get('nom')   
        postnom = request.form.get('postnom')
        prenom = request.form.get('prenom')
    
        telephone = request.form.get('telephone')
        #hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        #cursor = db.cursor()
       
     
        #monimage = "user.png"
        cur.execute("UPDATE  users SET nom=%s,postnom=%s, prenom=%s,telephone=%s WHERE id=%s", (nom, postnom, prenom,telephone, id))
        conn.commit()
         
        cur.close()

        return 'Opération effectuée.'

    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la modification de user : {str(e)}")
        return 'Erreur lors de la modification de user'
    

   

def  update_admin(id):
    #bcrypt = Bcrypt()
    conn = get_connection()
    cur = conn.cursor()

    try:
        nom = request.form.get('nom')   
        postnom = request.form.get('postnom')
        prenom = request.form.get('prenom')
        
        telephone = request.form.get('telephone')
        #hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        #cursor = db.cursor()
       
     
        #monimage = "user.png"
        cur.execute("UPDATE  users SET nom=%s,postnom=%s, prenom=%s,telephone=%s WHERE id=%s", (nom, postnom, prenom,telephone, id))
        conn.commit()
         
        cur.close()

        return 'Opération effectuée.'

    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la modification de user : {str(e)}")
        return 'Erreur lors de la modification de user'
    
   
    
    
    
def  create_users():
    bcrypt = Bcrypt()
    conn = get_connection()
    cur = conn.cursor()

    try:
        nom = request.form.get('nom')
       
        email = request.form.get('email')
        password = request.form.get('password')
       # image = request.form.get('image')
        telephone = request.form.get('telephone')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        #cursor = db.cursor()
       
     
        monimage = "user.png"
        cur.execute("INSERT INTO users (nom, email, password, avatar,telephone) VALUES (%s,%s,%s,%s,%s)", (nom, email, hashed_password, monimage, telephone))
        conn.commit()
         
        cur.close()

        return 'Opération effectuée.'

    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la création de user : {str(e)}")
        return 'Erreur lors de la création de user'
    


   
def  create_admin():
    bcrypt = Bcrypt()
    conn = get_connection()
    cur = conn.cursor()

    try:
        nom = request.form.get('nom')
        email = request.form.get('email')
        password = request.form.get('password')
        #postnom = request.form.get('postnom')
        prenom = request.form.get('prenom')
        role = "1"
     
       # image = request.form.get('image')
        telephone = request.form.get('telephone')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        #cursor = db.cursor()
       
     
        monimage = "user.png"
        cur.execute("INSERT INTO users (nom,prenom, email, password, avatar,telephone, role) VALUES (%s, %s, %s,%s,%s,%s,%s)", (nom, prenom, email, hashed_password, monimage, telephone, role))
        conn.commit()
         
        cur.close()

        return 'Opération effectuée.'

    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la création de user : {str(e)}")
        return 'Erreur lors de la création de user'
    






def update_user(id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        if 'image' in request.files:
            file = request.files['image']
            filename = file.filename
            
            # Définir le chemin d'enregistrement de l'image
            image_path = os.path.join('static/Image', filename)
            file.save(image_path)

            # Mettre à jour le nom de l'image dans la base de données
            cur.execute("UPDATE users SET avatar=%s WHERE id=%s", (filename, id))
            conn.commit()

            return ({'message': 'Opération effectuée avec succès.'}), 200

        return ({'error': 'Aucune image fournie.'}), 400

    except Exception as e:
        conn.rollback()
        print(f"Opération échouée : {str(e)}")
        return ({'error': 'Opération échouée.'}), 500

    finally:
        cur.close()
        conn.close()
    
    
    
    
def  create_user():
    bcrypt = Bcrypt()
    conn = get_connection()
    cur = conn.cursor()

    try:
        nom = request.form.get('nom')
        postnom = request.form.get('postnom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        password = request.form.get('password')
       # image = request.form.get('image')
        telephone = request.form.get('telephone')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        #cursor = db.cursor()
       
        if 'image' in request.files:
            file = request.files['image']
            filename = file.filename

            image_path = os.path.join('static/Image', filename)
            file.save(image_path)

            cur.execute("INSERT INTO users (nom, postnom, prenom, email, password, avatar,telephone) VALUES (%s,%s,%s,%s,%s,%s,%s)", (nom,postnom, prenom, email, hashed_password, filename, telephone,))
            conn.commit()
            cur.close()

            return 'Opération effectuée avec succès.'
        else:
            monimage = "user.png"
            cur.execute("INSERT INTO users (nom, postnom, prenom, email, password, avatar,telephone) VALUES (%s,%s,%s,%s,%s,%s,%s)", (nom,postnom, prenom, email, hashed_password, monimage, telephone,))
            conn.commit()
         
            cur.close()

            return 'Fichier image  enregistré avec succès.'

    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la création de la localisation : {str(e)}")
        return 'Erreur lors de la création de la publication'
    
    
    
    
def login():
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        bcrypt = Bcrypt()
        email = request.form.get('email')
        password = request.form.get('password')

        # Vérification de l'utilisateur dans la base de données
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[5], password):
            # Création du token d'accès
            access_token = create_access_token(identity=user[0])
            response = {
                'access_token': access_token,
                'user': {
                    'id': user[0],
                    'nom': user[1],
                    'postnom': user[2],
                    'prenom': user[3],
                    'email': user[4],
                    'role': user[8]
                }
            }
            return response
        else:
            return 'password'
    except Exception as e:
        # Gérer les exceptions ici
        print(f"Une erreur est survenue : {e}")
        return 'Une erreur est survenue', 500




        
def getuserid(identifiant):
    try:
        # Connexion à la base de données
        conn = get_connection()
        cursor = conn.cursor()

        # Récupération des données des utilisateurs
        cursor.execute("SELECT id, nom, postnom, prenom, email, password, avatar, telephone FROM users WHERE id=%s", (identifiant,))
        users = cursor.fetchall()

        # Vérification si des utilisateurs ont été trouvés
        if not users:
            return []

        # Conversion des données en format JSON
        data = []
        for id, nom, postnom, prenom, email, password, avatar, telephone in users:
            image_url = f'/static/Image/{avatar}' if avatar else None  # Vérification de l'avatar
            data.append({
                'id': id,
                'nom': nom,
                'postnom': postnom,
                'prenom': prenom,
                'email': email,
                'password': password,  # Note: ne pas inclure le mot de passe dans les données retournées.
                'avatar': image_url,
                'telephone': telephone,
                'url': avatar
            })

        return data

    except Exception as e:
        print(f"Erreur lors de la récupération des données utilisateur : {str(e)}")
        return 'Erreur'

    finally:
        # Assurez-vous que la connexion à la base de données est fermée
        cursor.close()
        conn.close()    
    

    
def delete_user(id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Exécutez la commande de suppression
        cur.execute("DELETE FROM users WHERE id=%s", (id,))
        conn.commit()
        
        cur.close()
        
        return 'Utilisateur supprimé avec succès.'

    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la suppression de l'utilisateur : {str(e)}")
        return 'Erreur lors de la suppression de l’utilisateur'