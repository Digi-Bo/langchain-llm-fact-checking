# Importation des bibliothèques nécessaires
import streamlit as st  # Pour créer l'interface utilisateur web
from langchain_groq import ChatGroq  # Pour utiliser le modèle de langage Groq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper  # Pour accéder aux APIs Arxiv et Wikipedia
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun  # Outils de recherche
from langchain.agents import initialize_agent, AgentType  # Pour créer et configurer l'agent IA
from langchain.callbacks import StreamlitCallbackHandler  # Pour afficher les actions de l'agent dans Streamlit
import os
from dotenv import load_dotenv  # Pour gérer les variables d'environnement

# Configuration des outils de recherche
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)  # Configure la recherche Arxiv
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)  # Crée l'outil de recherche Arxiv

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)  # Configure la recherche Wikipedia
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)  # Crée l'outil de recherche Wikipedia

search = DuckDuckGoSearchRun(name="Search")  # Crée l'outil de recherche DuckDuckGo

# Configuration de l'interface Streamlit
st.title("🔎 LangChain - Chat with search")  # Titre de l'application
# ... (Texte explicatif omis pour la brièveté)

# Barre latérale pour les paramètres
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")  # Champ pour saisir la clé API

# Initialisation de l'historique des messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

# Affichage de l'historique des messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

# Gestion de l'entrée utilisateur
if prompt := st.chat_input(placeholder="What is machine learning?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Configuration du modèle de langage et de l'agent
    llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)
    tools = [search, arxiv, wiki]
    search_agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handling_parsing_errors=True)

    # Génération et affichage de la réponse
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({'role': 'assistant', "content": response})
        st.write(response)