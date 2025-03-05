from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada de datos
class UserData(BaseModel):
    nombre: str
    correo: str
    telefono: str
    peso: float
    altura: float
    edad: int
    genero: str
    actividad: str
    objetivo: str
    dieta: str

# Función para calcular calorías y macronutrientes
def calcular_macros(peso, altura, edad, genero, actividad, objetivo, dieta):
    # Fórmula de Harris-Benedict
    if genero == "Masculino":
        tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
    else:
        tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)
    
    # Factor de actividad
    actividad_factores = {
        "Sedentario": 1.2,
        "Ligero": 1.375,
        "Moderado": 1.55,
        "Activo": 1.725,
        "Muy Activo": 1.9
    }
    calorias_mantenimiento = tmb * actividad_factores.get(actividad, 1.2)
    
    # Ajuste según objetivo
    objetivos = {"Perder Peso": -500, "Mantener Peso": 0, "Ganar Músculo": 500}
    calorias_objetivo = calorias_mantenimiento + objetivos.get(objetivo, 0)
    
    # Distribución de macronutrientes según la dieta
    dietas = {
        "Balanceada": (0.3, 0.3, 0.4),
        "Keto": (0.6, 0.3, 0.1),
        "Low-Carb": (0.4, 0.4, 0.2),
        "Alta en Carbs": (0.2, 0.3, 0.5)
    }
    prote, grasas, carbs = dietas.get(dieta, (0.3, 0.3, 0.4))
    
    proteinas = (calorias_objetivo * prote) / 4
    grasas = (calorias_objetivo * grasas) / 9
    carbohidratos = (calorias_objetivo * carbs) / 4
    
    return {
        "calorias": round(calorias_objetivo, 2),
        "proteinas": round(proteinas, 2),
        "grasas": round(grasas, 2),
        "carbohidratos": round(carbohidratos, 2)
    }

@app.post("/calcular")
def calcular(user_data: UserData):
    try:
        resultado = calcular_macros(
            user_data.peso,
            user_data.altura,
            user_data.edad,
            user_data.genero,
            user_data.actividad,
            user_data.objetivo,
            user_data.dieta
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
