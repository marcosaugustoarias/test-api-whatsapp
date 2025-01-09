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
    - data: "<phone>-<option>"
    """
    try:
        phone, option = data.split("-")

        if not phone.isdigit():
            raise ValueError("El número de teléfono debe contener solo dígitos.")
        
        return {
            "message": f"Usted seleccionó la opción {option}"
        }
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="Formato de datos inválido. Asegúrate de enviar 'phone-option'."
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
