Pour documenter cette modification dans votre fichier README, vous pouvez inclure une section dédiée aux prérequis de l'environnement et expliquer les raisons de cette spécification de version Python. Voici un exemple de texte à ajouter dans votre README :

---

## Prérequis

Pour garantir la compatibilité des dépendances utilisées dans ce projet, il est nécessaire d'utiliser une version spécifique de Python. Assurez-vous d'avoir Python installé dans la plage de versions suivante :

- Python >= 3.10, < 3.13

Cette plage de versions est spécifiée pour garantir la compatibilité avec la bibliothèque `unstructured`, qui nécessite une version de Python comprise entre 3.9.0 et 3.13 (exclusif). Cela permet d'éviter les conflits de version et d'assurer une installation sans erreur des dépendances.


## Installation de l'environnement python avec Conda

1. **Créer un environnement virtuel avec conda**
    ```
    conda create -p ./venv python==3.10 -y
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


2. **Initialisation des dépendance avec `poetry`** 


    Pour installer les dépendances une fois `poetry` installé sur votre machine
    ```
    poetry install
    ```


3. **Lancer l'app streamlit avec `poetry`** 

    ```
    poetry run streamlit run main.py

    ```