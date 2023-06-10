# T3_ArquiEmergente
 Tarea 3 Arquitectura emergentes, API IoT



Como acceder a la informacion de un sensor
    http://127.0.0.1:4000/api/v1/sensor_data?company_api_key=%3Capi_key_123%3E
    
Para poder ingresar informacion a un sensor se hace mediante la siguiente ruta: 
    http://127.0.0.1:4000/api/v1/sensor_data

    y con el siguiente JSON 
    {
    "api_key": "api_key_sensor_123",
    "json_data": [
      {
        "timestamp": 1645369200,
        "data_column1": 1,
        "data_column2": 2,
        "data_column3": 3
      },
      {
        "timestamp":1645369200,
        "data_column1": 4,
        "data_column2": 5,
        "data_column3": 6
      }
                 ]
    }