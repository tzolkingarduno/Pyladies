Instalando virtualenv

$ pip3 install virtualenv

$ mkdir <nombre_dir_Venv>

$ cd <nombre_dir_Venv>

$ python3 -m venv <nombre_amb_virt>

$ source bin/activate

$ python3 -m pip install -r requirements.txt  # Instalacion de librerías en ambiente virtual que usará la app


Instalando gcloud

$ mkdir GoogleCloud_SDK/

$ cd GoogleCloud_SDK/

$ curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-346.0.0-linux-x86_64.tar.gz

$ tar -xvzf google-cloud-sdk-346.0.0-linux-x86_64.tar.gz 

$ ./google-cloud-sdk/install.sh

$ ./google-cloud-sdk/bin/gcloud init

$ gcloud projects create    # Seguir las instrucciones y guardar el ID del proyecto



Desplegando en la red

$ gcloud config set project <id_proyecto>

$ gcloud app deploy    # Despliega en servidor back-end

$ gcloud app browse
