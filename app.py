import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re

# Configuration de l'interface Streamlit
st.title("🔎 LangChain - Chat avec recherche avancée et vérification des faits")

# Barre latérale pour la clé API
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Entrez votre clé API Groq :", type="password")

# Vérification de la présence de la clé API
if not api_key:
    st.warning("Veuillez entrer votre clé API Groq dans la barre latérale avant de continuer.")
    st.stop()

# Configuration du modèle de langage
try:
    llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)
except Exception as e:
    st.error(f"Erreur lors de l'initialisation du modèle : {str(e)}")
    st.stop()

# Configuration des outils de recherche
arxiv_wrapper = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500)
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)
wiki_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=500)
wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)
search = DuckDuckGoSearchRun(name="Search")

tools = [search, arxiv, wiki]

# Initialisation de l'historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour, je suis un chatbot qui peut effectuer des recherches avancées et vérifier les faits. Comment puis-je vous aider ?"}
    ]

# Affichage de l'historique des messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

# Chaînes de traduction
fr_to_en_chain = LLMChain(llm=llm, prompt=PromptTemplate(
    template="Traduisez la question suivante du français vers l'anglais : {question}",
    input_variables=["question"]
))

en_to_fr_chain = LLMChain(llm=llm, prompt=PromptTemplate(
    template="Traduisez la réponse suivante de l'anglais vers le français : {answer}",
    input_variables=["answer"]
))

# Chaîne pour la réponse initiale
initial_answer_chain = LLMChain(llm=llm, prompt=PromptTemplate(
    template="Répondez à la question suivante en anglais : {question}\nRéponse :",
    input_variables=["question"]
))

# Chaîne pour identifier les faits à vérifier
fact_identification_chain = LLMChain(llm=llm, prompt=PromptTemplate(
    template="Identifiez les principaux faits à vérifier dans cette réponse :\n{answer}\n\nFaits à vérifier (listez-les un par ligne) :",
    input_variables=["answer"]
))

# Chaîne pour générer des questions de recherche
search_question_chain = LLMChain(llm=llm, prompt=PromptTemplate(
    template="Générez une question de recherche précise pour vérifier ce fait : {fact}\nQuestion de recherche :",
    input_variables=["fact"]
))

# Agent pour la recherche
agent_template = """Answer the following question in English. You have access to the following tools:
{tools}

Use the following format:

Question: {input}
Thought: [your thought here]
Action: [tool name]
Action Input: [input for the tool]
Observation: [result of the action]
... (repeat Thought/Action/Action Input/Observation if necessary)
Thought: I have collected enough information
Final Answer: [concise relevant information in English]

Important: 
- Provide only the most relevant information.
- Always include "Action Input:" after "Action:".
- End with "Final Answer:" followed by the relevant information.

Available tools: {tool_names}

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

agent_prompt = PromptTemplate.from_template(agent_template)
tool_names = ", ".join([tool.name for tool in tools])
agent = create_react_agent(llm, tools, agent_prompt.partial(tool_names=tool_names))
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, max_iterations=3)

# Chaîne pour la synthèse finale
final_synthesis_chain = LLMChain(llm=llm, prompt=PromptTemplate(
    template="Synthesize the following information into a comprehensive answer in English:\nInitial answer: {initial_answer}\nVerified information:\n{verified_info}\nFinal comprehensive answer:",
    input_variables=["initial_answer", "verified_info"]
))

# Fonction pour extraire la réponse finale
def extract_final_answer(output):
    match = re.search(r"Final Answer\s*:\s*(.*)", output, re.DOTALL)
    if match:
        return match.group(1).strip()
    return output

# Gestion de l'entrée utilisateur
prompt = st.chat_input(placeholder="Qu'est-ce que l'apprentissage automatique ?")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        
        try:
            # Étape 1: Traduction de la question en anglais
            translated_question = fr_to_en_chain.run(question=prompt)
            st.write("Question traduite :", translated_question)

            # Étape 2: Réponse initiale du LLM
            initial_answer = initial_answer_chain.run(question=translated_question)
            st.write("Réponse initiale :", initial_answer)

            # Étape 3: Identification des faits à vérifier
            facts_to_verify = fact_identification_chain.run(answer=initial_answer)
            st.write("Faits à vérifier :", facts_to_verify)

            # Étape 4: Génération de questions de recherche et vérification
            verified_info = []
            for fact in facts_to_verify.split('\n'):
                if fact.strip():
                    search_question = search_question_chain.run(fact=fact)
                    st.write("Question de recherche :", search_question)
                    
                    search_result = agent_executor.invoke(
                        {"input": search_question},
                        callbacks=[st_cb]
                    )
                    verified_info.append(extract_final_answer(search_result['output']))

            # Étape 5: Synthèse finale
            verified_info_str = "\n".join(verified_info)
            final_synthesis = final_synthesis_chain.run(initial_answer=initial_answer, verified_info=verified_info_str)
            st.write("Synthèse finale en anglais :", final_synthesis)

            # Étape 6: Traduction de la réponse finale en français
            final_answer = en_to_fr_chain.run(answer=final_synthesis)
            st.write("Réponse finale en français :", final_answer)

            st.session_state.messages.append({"role": "assistant", "content": final_answer})
        except Exception as e:
            st.error(f"Une erreur s'est produite : {str(e)}")
            st.write("Voici la dernière réponse partielle :")
            st.write(locals().get('final_synthesis', "Aucune réponse disponible"))