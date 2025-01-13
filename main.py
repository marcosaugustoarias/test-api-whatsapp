import os
import json
from urllib.parse import unquote, urlparse, parse_qs
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

        # Decodificar datos si están codificados como URL
        decoded_data = unquote(data)
        print(f"Datos decodificados: {decoded_data}")

        # Detectar si el dato decodificado es otra URL
        if "?" in decoded_data:
            parsed_url = urlparse(decoded_data)
            query_params = parse_qs(parsed_url.query)
            # Intentar obtener el parámetro `data` interno si existe
            if "data" in query_params:
                decoded_data = query_params["data"][0]
                print(f"Datos internos procesados: {decoded_data}")

        # Procesar los datos como antes
        parts = decoded_data.split("-")

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
                "raw_data": data,
                "decoded_data": decoded_data,
            }
        else:
            return {
                "message": f"Opción seleccionada: {option} (Número no proporcionado)",
                "raw_data": data,
                "decoded_data": decoded_data,
            }
    except ValueError as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Formato de datos inválido: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error inesperado: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)