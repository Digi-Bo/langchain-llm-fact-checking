Pour documenter cette modification dans votre fichier README, vous pouvez inclure une section dédiée aux prérequis de l'environnement et expliquer les raisons de cette spécification de version Python. Voici un exemple de texte à ajouter dans votre README :

---




## Installation de l'environnement python avec Conda

1. **Créer un environnement virtuel avec conda**
    ```
    conda create -p ./venv python==3.11 -y
    ```
le `p`implique qu'il sera créé dans le dossier de travail


- **Pour l'activer**

    ```
    conda activate ./venv
    ```

- **Si vous souhaitez le supprimer par la suite**
    ```
    rm -rf ./venv
    ```




**Lancer l'app streamlit** 

    ```
    streamlit run app.py

    ```