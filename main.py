import os
from fastapi import FastAPI, Query, HTTPException
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

@app.get("/process")
async def process_data(data: str = Query(...)):
    """
    Procesa los datos enviados desde el botón de WhatsApp.

    Formato esperado:
    - data: "<phone>-<option>" o solo "<option>"
    """
    try:
        # Dividir los datos recibidos
        parts = data.split("-")
        
        # Validar si incluye teléfono
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
                "message": f"Número: {phone}, opción seleccionada: {option}"
            }
        else:
            return {
                "message": f"Opción seleccionada: {option} (Número no proporcionado)"
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