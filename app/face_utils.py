import face_recognition
import numpy as np
# from .database import save_encoding, load_encodings
from .db import save_encoding, load_encodings

def register_face(image_path, user_id):
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        return {"message": "not_detected"}

    save_encoding(user_id, encodings[0])  # Simpan encoding pertama

    return {"message": f"{user_id} registered successfully"}

def recognize_face(user_id, image_path):
    known_encodings = load_encodings(user_id)
    
    if not known_encodings:
        return {"message": "not_registered"}

    image = face_recognition.load_image_file(image_path)
    unknown_encodings = face_recognition.face_encodings(image)

    if len(unknown_encodings) == 0:
        return {"message": "not_detected"}

    results = {}
    for user_id, known_encoding in known_encodings.items():
        for unknown_encoding in unknown_encodings:
            match = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=0.4)
            if match[0]:
                results[user_id] = True

    recognized = [user_id for user_id, matched in results.items() if matched]

    return {"message": "recognized" if recognized else "not_recognized"}
