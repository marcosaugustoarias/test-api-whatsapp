import os
import json
from fastapi import FastAPI, Query, HTTPException
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

@app.get("/process")
async def process_data(data: str = Query(...)):
    """
    Procesa los datos enviados desde el botón de WhatsApp.
    """
    try:
        # Registrar los datos recibidos para depuración
        print(f"Datos recibidos (raw): {data}")
        
        # Intentar analizar como JSON si es posible
        try:
            data_as_json = json.loads(data)
            print(f"Datos analizados como JSON: {data_as_json}")
        except json.JSONDecodeError:
            print("No se pudo analizar como JSON. Procesando como texto plano.")

        # Dividir los datos por guión
        parts = data.split("-")
        
        if len(parts) == 2:
            phone, option = parts
            if not phone.isdigit():
                raise ValueError("El número de teléfono debe contener solo dígitos.")
        elif len(parts) == 1:
            option = parts[0]
            phone = None
        else:
            raise ValueError("Formato incorrecto de datos.")

        if phone:
            return {
                "message": f"Número: {phone}, opción seleccionada: {option}",
                "raw_data": data
            }
        else:
            return {
                "message": f"Opción seleccionada: {option} (Número no proporcionado)",
                "raw_data": data
            }
    except ValueError as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Formato de datos inválido. {str(e)} Asegúrate de enviar '<phone>-<option>' o '<option>'."
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)