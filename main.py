import os
import json
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    """
    Endpoint raíz para confirmar que el servicio está funcionando correctamente.
    """
    return {"message": "El servicio está funcionando correctamente."}

@app.post("/webhook")
async def webhook(request: Request):
    """
    Procesa las solicitudes entrantes desde el webhook de Meta para detectar qué botón fue presionado.
    """
    try:
        # Leer el cuerpo de la solicitud
        body = await request.json()
        print(f"Payload recibido: {json.dumps(body, indent=2)}")

        # Validar que el payload contenga datos relevantes
        if "entry" in body and isinstance(body["entry"], list):
            for entry in body["entry"]:
                if "changes" in entry and isinstance(entry["changes"], list):
                    for change in entry["changes"]:
                        if "value" in change and "messages" in change["value"]:
                            messages = change["value"]["messages"]
                            for message in messages:
                                if "button" in message:
                                    button_payload = message["button"].get("payload")
                                    print(f"Botón presionado: {button_payload}")
                                    return {"message": "Botón presionado", "payload": button_payload}

        return {"status": "no_button", "message": "No se encontró información de botón en el payload."}

    except Exception as e:
        print(f"Error al procesar el webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@app.get("/webhook")
async def verify_webhook(request: Request):
    
    VERIFY_TOKEN = "traslada"

    # Obtener los parámetros manualmente
    params = request.query_params
    hub_mode = params.get("hub.mode")
    hub_verify_token = params.get("hub.verify_token")
    hub_challenge = params.get("hub.challenge")

    # Log para depurar
    print(f"Recibido: hub_mode={hub_mode}, hub_verify_token={hub_verify_token}, hub_challenge={hub_challenge}")

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        #return hub_challenge  # Devolver texto plano
        return PlainTextResponse(content=hub_challenge)
    else:
        raise HTTPException(status_code=403, detail="Token de verificación inválido.")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)