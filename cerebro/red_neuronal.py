import random
import re

class RedNeuronalPato:
    def __init__(self, memoria):
        self.memoria = memoria
        self.vocab = ["<PAD>", "<INI>", "<FIN>", "cuac", "..."]
        self.palabra_a_idx = {w: i for i, w in enumerate(self.vocab)}
        self.sinapsis = {}
        self.alfabeto = set(["c", "u", "a", ".", "?"])
        self.experiencia = 0
        self._activo = True  # Estado interno
        
        estado = self.memoria.cargar_red()
        if estado:
            self.vocab = estado.get("vocab", self.vocab)
            self.palabra_a_idx = {w: i for i, w in enumerate(self.vocab)}
            self.sinapsis = estado.get("sinapsis", {})
            self.alfabeto = set(estado.get("alfabeto", list(self.alfabeto)))
            self.experiencia = estado.get("experiencia", 0)

    @property
    def activo(self):
        return self._activo

    @activo.setter
    def activo(self, valor):
        self._activo = bool(valor)

    @property
    def etapa(self) -> int:
        if self.experiencia < 5: return 0
        if self.experiencia < 20: return 1
        if self.experiencia < 50: return 2
        return 3

    def tokenizar(self, texto: str) -> list:
        for ch in texto.lower():
            if ch.isalpha() or ch in "¿?¡!.,": self.alfabeto.add(ch)
        return re.findall(r"[a-záéíóúñü0-9]+|[¿?¡!.,]", texto.lower())

    def aprender(self, texto: str):
        tokens = self.tokenizar(texto)
        if not tokens: return
        
        for t in tokens:
            if t not in self.palabra_a_idx:
                self.palabra_a_idx[t] = len(self.vocab)
                self.vocab.append(t)
        
        for i in range(len(tokens)-1):
            t1, t2 = tokens[i], tokens[i+1]
            self.sinapsis.setdefault(t1, {})[t2] = self.sinapsis.get(t1, {}).get(t2, 0) + 1
            
        self.experiencia += max(1, len(tokens) // 2)
        self.guardar()

    def responder(self, texto: str) -> str:
        if not self.activo:
            return "Zzz... [Sistema Apagado]"

        self.aprender(texto)
        tokens_usr = self.tokenizar(texto)
        etapa_act = self.etapa
        
        if etapa_act == 0:
            letras = list(self.alfabeto)
            return random.choice(["...", ".. c u a ..?", "".join(random.choices(letras, k=4)) + "?"])
        elif etapa_act == 1:
            eco = random.choice(tokens_usr) if tokens_usr else "cuac"
            return f"... {eco}? cuac."
        else:
            respuesta = []
            actual = random.choice(tokens_usr) if tokens_usr and tokens_usr[0] in self.sinapsis else "cuac"
            for _ in range(random.randint(4, 12)):
                respuesta.append(actual)
                siguientes = self.sinapsis.get(actual, {})
                if siguientes:
                    actual = max(siguientes, key=siguientes.get)
                    if random.random() < 0.3: actual = random.choice(list(siguientes.keys()))
                else:
                    break
            res = " ".join(respuesta).strip()
            return res if res else "cuac..."

    def generar_impulso(self) -> str:
        if not self.activo: return ""
        et = self.etapa
        if et == 0: return "¿...?"
        elif et == 1: return "cuac?"
        else:
            palabras = [w for w in self.vocab if w not in ["<PAD>", "<INI>", "<FIN>"]]
            if palabras: return f"{random.choice(palabras)} {random.choice(palabras)}?"
            return "cuac."

    def guardar(self):
        self.memoria.guardar_red({
            "vocab": self.vocab, "sinapsis": self.sinapsis,
            "alfabeto": list(self.alfabeto), "experiencia": self.experiencia
        })
