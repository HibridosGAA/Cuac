import os
import sqlite3
import json
import time
from datetime import datetime

class MemoriaLargoPlazo:
    def __init__(self, base_dir="data"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.db_path = os.path.join(self.base_dir, "cerebro_pato.db")
        self.weights_path = os.path.join(self.base_dir, "pesos_red.json")
        self._inicializar_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _inicializar_db(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                fecha_creacion TEXT
            )
        """)
        # Tabla de interacciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                fecha_legible TEXT,
                usuario_id INTEGER,
                emisor TEXT,
                mensaje TEXT,
                etapa INTEGER,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        """)
        conn.commit()
        conn.close()

    def obtener_o_crear_usuario(self, username: str) -> int:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            uid = row[0]
        else:
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO usuarios (username, fecha_creacion) VALUES (?, ?)", (username, fecha_actual))
            uid = cursor.lastrowid
            conn.commit()
        conn.close()
        return uid

    def registrar_interaccion(self, username: str, emisor: str, mensaje: str, etapa: int):
        uid = self.obtener_o_crear_usuario(username)
        conn = self._get_conn()
        cursor = conn.cursor()
        fecha_legible = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO interacciones (timestamp, fecha_legible, usuario_id, emisor, mensaje, etapa) VALUES (?, ?, ?, ?, ?, ?)",
            (time.time(), fecha_legible, uid, emisor, mensaje, etapa)
        )
        conn.commit()
        conn.close()

    def obtener_historial_completo(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.fecha_legible, u.username, i.emisor, i.mensaje, i.etapa
            FROM interacciones i
            JOIN usuarios u ON i.usuario_id = u.id
            ORDER BY i.id ASC
        """)
        filas = cursor.fetchall()
        conn.close()
        return filas

    def obtener_conversaciones_usuario(self, username: str):
        uid = self.obtener_o_crear_usuario(username)
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT emisor, mensaje, fecha_legible
            FROM interacciones
            WHERE usuario_id = ?
            ORDER BY id ASC
        """, (uid,))
        filas = cursor.fetchall()
        conn.close()
        return [{"emisor": f[0], "mensaje": f[1], "fecha": f[2]} for f in filas]

    def guardar_red(self, estado: dict):
        with open(self.weights_path, "w", encoding="utf-8") as f:
            json.dump(estado, f, ensure_ascii=False)

    def cargar_red(self):
        if os.path.exists(self.weights_path):
            try:
                with open(self.weights_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: pass
        return None
