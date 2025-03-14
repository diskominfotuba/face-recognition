from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
import numpy as np

DATABASE_URL = "postgresql://devkh:devkh123@localhost:5500/face_recognation"

# Setup engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definisikan model untuk tabel faces
class Face(Base):
    __tablename__ = "faces"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    encoding = Column(Vector(128), nullable=False)  # Simpan encoding wajah sebagai vector

# Membuat tabel jika belum ada
Base.metadata.create_all(bind=engine)

# Fungsi untuk menyimpan encoding wajah ke database
def save_encoding(user_id, encoding):
    encoding_list = encoding.tolist()  # Ubah encoding ke format list
    db = SessionLocal()  # Membuka sesi database
    try:
        # Periksa apakah nama sudah ada dalam database
        existing_faces = db.query(Face).filter(Face.user_id == user_id).all()
        if len(existing_faces) >= 3: 
            # Jika sudah lebih dari 3, update encoding
            face = existing_faces[-1]  # Ambil record terakhir
            face.encoding = encoding_list
        else:
            # Jika belum ada, insert data baru
            face = Face(user_id=user_id, encoding=encoding_list)
            db.add(face)

        db.commit()  # Simpan perubahan ke database
    except Exception as e:
        db.rollback()  # Jika ada kesalahan, rollback
        print(f"Error: {e}")
    finally:
        db.close()  # Tutup sesi

# Fungsi untuk memuat encoding wajah dari database
def load_encodings(user_id):
    db = SessionLocal()  # Membuka sesi database
    try:
        faces = db.query(Face).filter(Face.user_id == user_id).all()  # Ambil semua data dari tabel faces
        encodings = {}
        for face in faces:
            encodings[face.user_id] = np.array(face.encoding)  # Simpan encoding sebagai numpy array
        return encodings
    except Exception as e:
        print(f"Error: {e}")
        return {}
    finally:
        db.close()  # Tutup sesi
