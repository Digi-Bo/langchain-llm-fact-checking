
Voici un résumé des principales étapes implémentées dans ce script :

1. Le LLM donne une réponse initiale à la question traduite en anglais.
2. Cette réponse est analysée pour identifier les faits à vérifier.
3. Pour chaque fait à vérifier, une question de recherche est générée.
4. Ces questions sont utilisées pour rechercher des informations sur des sources fiables (Wikipedia, arXiv, etc.) à l'aide de l'agent de recherche.
5. Toutes les informations collectées sont compilées et synthétisées par le LLM pour produire une réponse finale.
6. La réponse finale est traduite en français.

Ce processus combine la capacité du LLM à donner une réponse initiale avec la vérification des faits à partir de sources fiables.
 
Quelques points à noter :

- J'ai ajusté le nombre de résultats pour les recherches Wikipedia et arXiv à 2 pour équilibrer la quantité d'informations et le temps de traitement.
- L'interface Streamlit affiche chaque étape du processus pour plus de transparence.
- Le code gère les erreurs potentielles et affiche des messages d'erreur appropriés.

N'hésitez pas à tester cette nouvelle version et à me faire savoir si vous souhaitez des ajustements ou si vous avez des questions supplémentaires.

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