# Documentación del Proyecto: Ejercicio: AB Testing

### Descripción

Este proyecto tiene como objetivo analizar las interacciones de los usuarios en una plataforma antes de realizar una compra (o no). Utilizamos A/B Testing para determinar qué características, ideas o variantes impulsan a los usuarios a comprar. El dataset incluye un registro de todos los experimentos a los que un usuario fue sometido durante su navegación. El proyecto incluye:

- Implementación de notebooks para calcular el número de compras asociadas a cada experimento.
- Comparación de las diferentes variantes de los experimentos para identificar cuál es la más efectiva.
- Realización de verificaciones de datos para asegurar la confianza en los resultados.
- Desarrollo de una API que permita consultar los resultados de un experimento en una fecha y hora específica.
- Implementación y despliegue de la API en un proveedor en GCP.

### Estructura del proyecto:

* readme.md
* eda.ipynb
* create_data.py
* config.py
* requirements.txt
* .gitignore
* módulos/
    * bigquery.py
    * cleaning.py
* deploy/
    * Dockerfile
    * app/
        * app.py
        * config.py
* config.py
* credential.json
* requirements.txt

En la carpeta raíz se encuentra:
- Un notebook con el EDA de los datos suministrados
- Un script de python que procesa los datos para generar una tabla almacenada en GCP que posteriormente será consumida en la API.
- Un archivo configuración, de requerimientos y gitignore
- Una carpeta *modulos* se encuentran funciones que permiten la limpieza del set de datos
- Una carpeta *deploy* se podrá implementar la API de forma local o en la nube

Es importante resaltar que el usuario debe crear un archivo .env para las variables de entorno y crear el archivo .json de credenciales de gcp. Esto se explicaré en la instalación.

### Instalación

Para configurar el proyecto, debes instalar las dependencias necesarias. 
Este proyecto incluye dos archivos `requirements.txt` en diferentes ubicaciones:

**Pasos para la instalación:**

1. **Instalación de dependencias del entorno principal:**

Crea un entorno virtual, navega hasta la carpeta principal del proyecto y ejecuta en la consola:

```
pip install -r requirements.txt
```

El archivo que está en la carpeta de deploy se utilizará cuando se haga el despliegue de la API.

2. **Archivo .env**

Crea un archivo .env en la carpeta raíz y en la carpeta *deploy* con la siguiente estructura, recuerde agregar la información de su proyecto:

```
PROJECT_ID=tu-id-del-proyecto
DATASET_ID=tu-dataset-id
TABLE_NAME=tu-tabla
```

3. **Archivo credenciales gcp**
    
Exportar el archivo de credenciales de gcp, para saber como exportarlo de clic [aqui](https://developers.google.com/workspace/guides/create-credentials?hl=es-419#:~:text=Click%20Keys%20%3E%20Add%20key%20%3E%20Create,json%20in%20your%20working%20directory.).

Este archivo debe ser guardado en la carpeta *deploy*.

### Supuestos
- La granularidad de la información será experimento y variante, por fecha (A-M-D H), evento, usuario e item. 
- Si la diferencia entre los registros es menor a un minuto y contienen la misma información, se conservará solo un registro.
- Para mirar que experimentos llevaron a la compra se tomo el ID y Usario de los eventos BUY, creando un identificador combinado. Luego se mira en que otros eventos se tiene este mismo identificador, y así se marcan los experimentos llevaron a una compra en cada uno de los eventos.
- Se considera el flujo de los eventos como Search, Product, Checkout1, Checkout2, Checkout3 y Buy, aunque es claro que los eventos no necesariamente siguen este orden.
- El supuesto anterior se aplica para los eventos Search, ya que al no tener item_id, no se podían asociar las comprar. Para este caso se valida si el evento siguiente es marcado con compra. En ese caso la búsqueda también se marcará con compra.
- Para la limpieza del dataset se analizaron eventos previos y siguientes a cada registro

### Consumo de la API

Ingrese en el [link](https://app2-2f6pyd7ana-uc.a.run.app)

Para acceder a un experimento utilice la siguiente estructura, reemplazando <:id> con el id del experimento y YYYY-MM-DD HH por la fecha que desea consultar:

```
https://app2-2f6pyd7ana-uc.a.run.app/experiment/<:id>/result?day=YYYY-MM-DD HH
```

Los id's de los experimentos disponibles son los siguientes:

    | exp_name                                            | exp_id |
    |-----------------------------------------------------|--------|
    | buyingflow/address_hub                              | 1      |
    | buyingflow/escWebMLA                                | 2      |
    | buyingflow/secure_card                              | 3      |
    | cookiesConsentBanner                                | 5      |
    | filters/sort-by-ranking                             | 6      |
    | frontend/assetsCdnDomainMLA                         | 7      |
    | frontend/assetsCdnDomainMLU                         | 8      |
    | mclics/ads-adsearch-boost-incremental-desktop-mla   | 9      |
    | mclics/search-list-algorithms                       | 10     |
    | mclics/search-pads-none-desktop-mla                 | 11     |
    | mclics/show-pads-global                             | 12     |
    | mclics/show-pads-search-list                        | 13     |
    | mshops/HideTransitionModal                          | 14     |
    | pdp/compatibilityWidget                             | 15     |
    | pdp/cpgShowOnlyAddToCart                            | 16     |
    | pdp/viewItemPageMigrationDesktopRES                 | 19     |
    | pdp/viewItemPageMigrationDesktopHirableSRV          | 17     |
    | pdp/viewItemPageMigrationReturns                    | 22     |
    | qadb/sa-on-vip                                      | 23     |
    | reviewsOnOff                                        | 24     |
    | search/back-filters                                 | 25     |
    | search/best-seller-aa-testing-fail-fast-edition     | 26     |
    | search/best-seller-fail-fast-edition-MLA            | 27     |
    | search/checkOnBehavior                              | 28     |
    | search/enable-map-layout                            | 29     |
    | search/remove-ecn-tag                               | 30     |
    | search/results-target-web-motors                    | 31     |
    | search/tendency-landing-enabled-MLA                 | 32     |
    | search/ungroup-products                             | 33     |
    | search/web-layout-default-res                       | 34     |
    | searchbackend/cbt-antiboost                         | 35     |
    | searchbackend/item-reputation                       | 36     |
    | searchbackend/official-store-orders-boost           | 37     |
    | searchbackend/recommended-products                  | 38     |
    | searchbackend/seller-reputation-change              | 39     |
    | splinter/official-stores                            | 40     |
    | vip/carousel-v2p-above-the-fold                     | 41     |
    | vip/classiWordingFree                               | 42     |
    | vip/servicesQuoteUnification                        | 44     |
    | vip/shippingCalculatorMigrationModalExperiment      | 45     |
    | wasPrice                                            | 47     |


### Arquitectura de la API

![arquitectura](https://lh3.googleusercontent.com/pw/AP1GczOZX0pnheoRzpXvI4FaosIfhmLvQQuzCE7pYKTWPiHtwatNk4b0pA8l57xC2w4zelGhZvO7Dlfw5hFJn0wqvVSPkDl7nGaRt9qscYiMKRvnusVRSoLHS0UtfIOUEr0gFdO53dK7tXQ2N9RoeRt6xrVm=w660-h270-s-no-gm?authuser=0)

La API interactúa con Google Cloud Platform, específicamente con los servicios de Cloud Run y BigQuery.

- API: En una interfaz we que expone una funcionalidad específica. Actúa como un punto de entrada para solicitudes externas.
- Cloud Run: La API envía las solicitudes a Cloud Run, donde se ejecuta el código que procesa la petición. Este es un servicio de contenedores serverless.
- BigQuery: El código en Cloud Run interactúa con BigQuery para realizar consultas a una tabla y obtener los resultados necesarios para responder a la solicitud de la API. Un servicio de almacenamiento de datos masivos.

### Despliegue local

En la ubicación de la carpeta deploy ejecute los siguientes comando

```
docker build -t my-fastapi-app . 
```

Y luego este comando
```
docker run -p 8080:8080 --env-file .env -v $(pwd)/credential.json:/app/credential.json my-fastapi-app
```

Puede usar [thunder client](https://www.thunderclient.com/) para enviar la petición a la API.

### Despliegue cloud run en GCP

En la ubicación de la carpeta deploy ejecute los siguientes comando, recuerde cambiar {PROJECT_ID} por el nombre de su proyecto

```
gcloud builds submit --tag gcr.io/{PROJECT_ID}/app  
```                

luego ejecute este comando, recuerde cambiar {PROJECT_ID} por el nombre de su proyecto:
```
gcloud run deploy --image gcr.io/{PROJECT_ID}/app --allow-unauthenticated --region=us-central1
``` 


### Contacto

Sharon Camacho

sharoncamachog@gmail.com