# Un chat fournissant des réponses précises et vérifiées sur des sources fiables

## Objectif de l'application

Cette application a pour objectif de permettre la génération de réponses précises et vérifiées en français à partir de questions posées par l'utilisateur. Elle utilise un modèle de langage (LLM) pour générer une réponse initiale, puis vérifie les faits en s'appuyant sur des sources fiables comme Wikipedia, arXiv, et DuckDuckGo. La réponse finale est ensuite traduite en français.

## Création d'un environnement virtuel adapté

Pour garantir que l'application fonctionne correctement, il est recommandé de créer un environnement virtuel Python avec `conda`. Voici les étapes à suivre :

1. **Créer un environnement virtuel avec conda**
    ```bash
    conda create -p ./venv python==3.11 -y
    ```
   L'option `-p` permet de créer l'environnement dans le dossier de travail.

2. **Activer l'environnement virtuel**
    ```bash
    conda activate ./venv
    ```

3. **Installer les dépendances**
    ```bash
    pip install -r requirements.txt
    ```

4. **Supprimer l'environnement virtuel (si nécessaire)**
    ```bash
    rm -rf ./venv
    ```

## Technologies clés utilisées

Les technologies et bibliothèques principales utilisées dans ce projet sont :

- **LangChain** : Pour la gestion des chaînes de traitement du langage naturel.
- **Groq** : Pour l'optimisation des modèles de langage à haute vitesse.
- **Streamlit** : Pour la création d'une interface utilisateur interactive.
- **WikipediaAPIWrapper, ArxivAPIWrapper** : Pour interagir avec les API de Wikipedia et arXiv.
- **DuckDuckGoSearchRun** : Pour effectuer des recherches sur le web.
- **LLM (Llama3-8b-8192)** : Modèle de langage utilisé pour la génération des réponses.

## Étapes clés du code

1. **Traduction de la question** : La question posée par l'utilisateur en français est traduite en anglais pour le traitement par le modèle de langage.
2. **Génération d'une réponse initiale** : Le LLM produit une première réponse basée sur la question traduite.
3. **Identification des faits à vérifier** : La réponse initiale est analysée pour identifier les faits nécessitant une vérification.
4. **Recherche des faits** : Des questions de recherche sont générées pour chaque fait, et des recherches sont effectuées via les API disponibles.
5. **Synthèse des informations** : Les informations vérifiées sont compilées pour produire une réponse finale.
6. **Traduction de la réponse finale** : La réponse finale en anglais est traduite en français.

## Utilisation du code

1. **Configurer l'application** : Lancez l'application avec Streamlit en utilisant la commande suivante :
    ```bash
    streamlit run app.py
    ```

2. **Entrez votre clé API Groq dans la barre latérale** 



3. **Interagir avec l'application** : Posez une question en français dans le champ prévu à cet effet. L'application générera une réponse en suivant les étapes décrites ci-dessus.














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