import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.externals import joblib
import os
import tkinter.messagebox as tkMessageBox
import tkinter as tk
from tkinter import *

################################################
## INÍCIO DA CRIAÇÃO DE MODELO SUPERVISIONADO ##
################################################
root = tk.Tk()
root.geometry("200x100")
root.title("Avaliação de Candidato")
root.resizable(0, 0)
root.configure()
def treina():
    print("*** Iniciando Treinamento")
    ss = StandardScaler()
    # desabilita mensagens de aviso
    pd.options.mode.chained_assignment = None  # default='warn'

    # obtem dados para criar modelo
    df = pd.read_csv('registro_candidatos.csv')

    # obter recursos e resultados correspondentes
    feature_names = ['Nota', 'DinamicadeGrupo', 'Agressividade', 'MediaAvaliacao', 'ErrosPraticos']

    training_features = df[feature_names]

    outcome_name = ['Recomenda']
    outcome_labels = df[outcome_name]

    #  listar recursos com base no tipo
    numeric_feature_names = ['MediaAvaliacao', 'ErrosPraticos']
    categoricial_feature_names = ['Nota', 'DinamicadeGrupo','Agressividade']



    # Ajusta como 'scaler' os recursos numéricos
    ss.fit(training_features[numeric_feature_names])

    # scale numeric features now
    training_features[numeric_feature_names] = ss.transform(training_features[numeric_feature_names])


    training_features = pd.get_dummies(training_features, columns=categoricial_feature_names)

    # print(training_features)

    categorical_engineered_features = list(set(training_features.columns) - set(numeric_feature_names))


    # Ajusta o modelo
    lr = LogisticRegression()
    model = lr.fit(training_features, np.array(outcome_labels['Recomenda']))

    pred_labels = model.predict(training_features)
    actual_labels = np.array(outcome_labels['Recomenda'])



    # print('Precisão:', float(accuracy_score(actual_labels, pred_labels))*100, '%')
    # print('Estatísticas de Classiicação:')
    # print(classification_report(actual_labels, pred_labels))

    # cria as pastas no sistema caso não existam
    if not os.path.exists('Model'):
        os.mkdir('Model')
    if not os.path.exists('Scaler'):
        os.mkdir('Scaler')

    # Salvando os modelos
    joblib.dump(model, r'Model/model.pickle')
    joblib.dump(ss, r'Scaler/scaler.pickle')
    print("*** Modelo Treinado ***")


    tkMessageBox.showinfo("Concluído!", "O Modelo foi treinado com sucesso!")

#############################################
## FIM DA CRIAÇÃO DE MODELO SUPERVISIONADO ##
#############################################

# Carregando os modelos salvos anteriormente
def predicao():
    ss = StandardScaler()


    ss = StandardScaler()
    # desabilita mensagens de aviso
    pd.options.mode.chained_assignment = None  # default='warn'

    # obtem dados para criar modelo
    df = pd.read_csv('registro_candidatos.csv')

    # obter recursos e resultados correspondentes
    feature_names = ['Nota', 'DinamicadeGrupo', 'Agressividade', 'MediaAvaliacao', 'ErrosPraticos']

    training_features = df[feature_names]

    outcome_name = ['Recomenda']
    outcome_labels = df[outcome_name]

    #  listar recursos com base no tipo
    numeric_feature_names = ['MediaAvaliacao', 'ErrosPraticos']
    categoricial_feature_names = ['Nota', 'DinamicadeGrupo','Agressividade']



    # Ajusta como 'scaler' os recursos numéricos
    ss.fit(training_features[numeric_feature_names])

    # scale numeric features now
    training_features[numeric_feature_names] = ss.transform(training_features[numeric_feature_names])


    training_features = pd.get_dummies(training_features, columns=categoricial_feature_names)

    # print(training_features)

    categorical_engineered_features = list(set(training_features.columns) - set(numeric_feature_names))


    feature_names = ['Nota', 'DinamicadeGrupo', 'Agressividade', 'MediaAvaliacao', 'ErrosPraticos']
    numeric_feature_names = ['MediaAvaliacao', 'ErrosPraticos']
    categoricial_feature_names = ['Nota', 'DinamicadeGrupo','Agressividade']


    model = joblib.load(r'Model/model.pickle')
    scaler = joblib.load(r'Scaler/scaler.pickle')


    ## novos dados para classificação
    root.geometry("500x500")

    w = Label(root, text="Nome do Candidato")
    w.pack()
    nome2 = Entry(root)
    nome2.pack()
    nome2.delete(0, END)
    nome2.insert(0, "")

    w = Label(root, text="")
    w.pack()

    w = Label(root, text="Digite a Nota:\n(Excelente - Alta - Boa - Média - Ruim - Péssima)")
    w.pack()
    nota2 = Entry(root)
    nota2.pack()
    nota2.delete(0, END)
    nota2.insert(0, "")

    w = Label(root, text="")
    w.pack()

    w = Label(root, text="Tem dinâmica de Grupo? (Sim - Não)")
    w.pack()
    dinamica = Entry(root)
    dinamica.pack()
    dinamica.delete(0, END)
    dinamica.insert(0, "")

    w = Label(root, text="")
    w.pack()

    w = Label(root, text="Tem agressividade? (Sim - Não)")
    w.pack()
    agressivida = Entry(root)
    agressivida.pack()
    agressivida.delete(0, END)

    w = Label(root, text="")
    w.pack()


    w = Label(root, text="Média na avaliação:")
    w.pack()
    media = Entry(root)
    media.pack()
    media.delete(0, END)

    w = Label(root, text="")
    w.pack()

    w = Label(root, text="Erros em teste prático:")
    w.pack()
    erros = Entry(root)
    erros.pack()
    erros.delete(0, END)

    w = Label(root, text="")
    w.pack()

    def consul():
        nome = nome2.get()
        nota = nota2.get()
        dinamicadegrupo = dinamica.get()
        agressividade = agressivida.get()
        mediaavaliacao = int(media.get())
        errospraticos = int(erros.get())

        new_data = pd.DataFrame([{'Nome': nome, 'Nota': nota, 'DinamicadeGrupo': dinamicadegrupo, 'Agressividade': agressividade,'MediaAvaliacao':int(mediaavaliacao), 'ErrosPraticos': int(errospraticos)}])
        new_data = new_data[['Nome', 'Nota', 'DinamicadeGrupo', 'Agressividade', 'MediaAvaliacao', 'ErrosPraticos']]


        ## preparando predição com novos dados
        prediction_features = new_data[feature_names]

        # escalando
        prediction_features[numeric_feature_names] = scaler.transform(prediction_features[numeric_feature_names])

        # Variáveis categóricas
        prediction_features = pd.get_dummies(prediction_features, columns=categoricial_feature_names)

        # adicionar coluna de recurso categórico ausente

        current_categorical_engineered_features = set(prediction_features.columns) - set(numeric_feature_names)
        missing_features = set(categorical_engineered_features) - current_categorical_engineered_features
        for feature in missing_features:
            # add zeros, desde que o recurso esteja ausente nessas amostras de dados
            prediction_features[feature] = [0] * len(prediction_features)

        # predição usando o modelo previamente treinado
        predictions = model.predict(prediction_features)

        # Resultados
        new_data['Recomenda'] = predictions

        print(new_data)
        tkMessageBox.showinfo("Consulta Concluída!", "O sistema recomenda este candidato:\n *** " + str(new_data['Recomenda'][0] + str("***\n")))

    busca = Button(root, text="Consultar", command=lambda: consul())
    busca.pack()
    root.mainloop()

def opcao():

    w = Label(root, text="")
    w.pack()
    busca = Button(root, text="Treinar Modelo", command=lambda: treina())
    busca.pack()
    busca = Button(root, text="Consultar Perfil", command=lambda: predicao())
    busca.pack()
    w = Label(root, text="")
    w.pack()
    root.mainloop()

    opcao = input("Deseja treinar um modelo ou fazer consulta de perfil? (Treinar - Consultar)\n")

    if opcao == "Treinar":
        treina()
    if opcao == "Consultar":
        predicao()
    else:
        pass


while True:
    opcao()
