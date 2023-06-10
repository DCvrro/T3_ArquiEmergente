# T3_ArquiEmergente
 Tarea 3 Arquitectura emergentes, API IoT

POST
    
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

Datos extras para rellenar la Base con más informacion para los sensores. 


    {
      "api_key": "abcdef12345",
      "json_data": [
        {
          "timestamp": 1622875200,
          "data_column1": "Valor 1",
          "data_column2": "Valor 2",
          "data_column3": "Valor 3"
        },
        {
          "timestamp": 1622961600,
          "data_column1": "Valor 4",
          "data_column2": "Valor 5",
          "data_column3": "Valor 6"
        },
        {
          "timestamp": 1623048000,
          "data_column1": "Valor 7",
          "data_column2": "Valor 8",
          "data_column3": "Valor 9"
        },
        {
          "timestamp": 1623134400,
          "data_column1": "Valor 10",
          "data_column2": "Valor 11",
          "data_column3": "Valor 12"
        },
        {
          "timestamp": 1623220800,
          "data_column1": "Valor 13",
          "data_column2": "Valor 14",
          "data_column3": "Valor 15"
        }
      ]
    }
