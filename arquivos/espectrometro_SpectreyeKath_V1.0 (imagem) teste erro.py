'''
UNIVERSIDADE DO ESTADO DA BAHIA
DEPARTAMENTO DE CIÊNCIAS EXATAS E DA TERRA - DCET I
LICENCIATURA EM FÍSICA
DISCIPLINA: INSTRUMENTAÇÃO EM FÍSICA III
DISCENTE(s):ANTÔNIO AUGUSTO GASCH SOUSA CHAVES
            LEVI SIMÕES CARDOZO
            OSMAR SANTOS VIEIRA FILHO            
            VITOR SILVA ROCHA
'''

'''
As bibliotecas são importantes para a execução do programa.

Caso não esteja com o arquivo *.exe e sim o *.py, é importante fazer
a instalação das respectivas bibliotecas:
> numpy; matplotlib; cv2 (opencv); scipy.

Podem ser instalados pelo pip installer ou configurações de plug-in
'''

#importando bibliotecas, módulos e pacotes necessários...


import numpy as np #para as operações com array
import matplotlib.pyplot as plt # para o plot do gráfico
import matplotlib.image as mpimg # para reconhecer a imagem
from matplotlib.widgets import Button, RadioButtons, CheckButtons
import cv2 as cv #biblioteca OpenCV para acesso visual a recursos
from scipy.signal import find_peaks

"""
SPECTREYEKATH_V1.0_Beta(imagem)

IMPORTANTE!!!!


INSTRUÇÕES DE USO

O programa irá solicitar o nome do arquivo de imagem e sua extensão,
então inserir o mesmo nome e sua extensão de arquivo, por exemplo:

imagem.png ; foto2.jpg; figuraA.jpeg

Essas imagens devem estar na mesma pasta que o arquivo *.py do espectrômetro

É importante que a imagem esteja iniciando da frequência que corresponde
a cor azul até a vermelha para que tenha uma leitura eficiente do
espectro

__________________________________________
azul                                 vermelho


A imagem pode ser rotacionada no próprio visualizador de imagem do
sistema operacional.

Após isso, o programa vai pedir um nome para que seja colocado no
gráfico, para facilitar a identificação do objeto ao final e poder
salvar a imagem do gráfico já com o nome no título.

Com a imagem carregada, uma janela irá aparecer para confirmar se é
mesmo o arquivo.

Pressionando "1", o usuário confirma e passa para a parte de seleção.

na janela "Selecione a imagem", desenhe um retângulo com o mouse sobre
o trecho da imagem que deseja analisar. Lembrando, a imagem deve estar
na horizontal, iniciando da frequência azul para a frequência vermelha.

Ao desenhar a área, pressionar Enter.

Abrirá uma janela confirmando o frame para captura. Se tudo estiver certo,
pressione "2" para iniciar a análise.


Será plotado o gráfico contendo a imagem do espectro em estudo, bem como
um gráfico com o comprimento de onda associado.

Há duas caixas com opções ao lado do gráfico para mostrar apenas linhas,
picos com máximos ou ambos.


"""

#-----------------------------------------------------------------------
# Definindo a função para início do programa

print("{:-^50}\n{:^50}\n{:^50}\n{:-^50}\n\n".format("", "Bem-vindo! Siga as instruções atentamente", "(programa em versão Beta)", ""))

def spectreyekath():
    
    nome_arqv = input("\nInsira o nome da image e a extensão \n (ex: foto1.jpg): "  )

    objeto = input("\n\nQual o nome do objeto a ser analisado:\n (ex.: Lâmpada, etc.) ")
    
    #Carregando arquivos de imagem:
    image = cv.imread("{}".format(nome_arqv))
    #Laço para manter a janela de captura aberta até os comandos
    roi_selected = False
    
    while(True):
        #ret, frame = cap.read()  #Fazendo a leitura e confirmando captura do dispositivo 
        k = cv.waitKey(1) #Aguardando as teclas de comando
        
        if k & 0xFF == ord('2'): # Comando para analisar o histograma de intensidade para os pixels
            shape = crop.shape # largura da imagem capturada
            dist = []
            
            for i in range(shape[1]):
                intensidade = np.mean(crop[:, i][:, 0]) + np.mean(crop[:, i][:, 1]) + np.mean(crop[:, i][:, 2])
                dist.append(intensidade)                           
            
            
    #--------------------------------------------------------------------
            #Plotando os gráficos
                
            # Gráfico 01 (espectro):                
                    
            fig, ax = plt.subplots(2,1, constrained_layout = False)
            fig.subplots_adjust(hspace = 0.5)        
                    
            fig.suptitle("Gráficos para {}".format(objeto), ha = "center", fontsize = 18)
            RGB_conv = cv.cvtColor(crop, cv.COLOR_BGR2RGB) #troca dos canais (por default, OpenCv utiliza BGR)        
            
            ax[0].imshow((np.flipud(RGB_conv)))
            ax[0].set_title("Espectro Obtido")
            ax[0].invert_yaxis()
            ax[0].set_xlabel("pixels (px)")
            ax[0].set_ylabel("pixels (px)")                  
                                                               
            # Gráfico 02 (gráfico comp. de onda):              
            calib = np.sin(40)      
            escala = np.linspace(400, 700, shape[1]) #Enquanto não se faz os ajustes melhores para calibrar os pixels        
            escala_lamb = escala.tolist()
            
            p, = ax[1].plot(escala_lamb, dist, color = 'magenta', linewidth = 1)        
            ax[1].set_title("Gráfico para o comprimento de onda")
            ax[1].set_xlabel(r"$\lambda  (nm)$")     
            ax[1].set_yticklabels([])
            ax[1].grid(alpha = 0.8)
            
            #Botão para identificar os máximos
            dist_arr = np.array(dist)
            peaks, _ = find_peaks(dist_arr, prominence=1, width=10)
            
            p1, = plt.plot(escala[peaks], dist_arr[peaks], "x", color = "orange")
            
            #IOnserindo botões de controle
            lines = [p, p1]
            labels = ["Linhas", "Picos"]
             
             
            def func(label):
                index = labels.index(label)
                lines[index].set_visible(not lines[index].get_visible())
                fig.canvas.draw()
             
             
            label = [True, True]
             
            # xposition, yposition, width and height
            ax_check = plt.axes([0.01, 0.3, 0.1, 0.1])
            plot_button = CheckButtons(ax_check, labels, label)
            plot_button.on_clicked(func)
                    
            print("\n{:-^30}\n{:^30}\n{:^30}\n{:-^30}".format("", "Valores para \u03BB dos picos ", "{}".format(objeto), ""))
            for i in range(len(escala[peaks])):
                print("{:^15}{:^.3f} nm\n".format(f"\u03BB{i} =", np.round(escala[peaks][i], decimals = 3) ))
            print("{:-^30}".format(""))
                    
            
            #plt.subplot_tool() #Caso seja necessária a configuração 
            plt.show()
            
    #--------------------------------------------------------------------

        elif k & 0xFF == ord('1'):
            r = cv.selectROI("Selecione a imagem", image)    
            roi_selected = True
            
        elif k & 0xFF == ord('q'): # sair do programa
            break
        
        else:
            if roi_selected:
                crop = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])].copy()
                cv.imshow("Pressione '2' para capturar o frame", crop)
            else:
                cv.imshow("(Pressione '1' para enquadrar)", image)
        
    cap.release()
    cv.destroyAllWindows()


#---------------------------------------------------------------------------------

while True: #laço para 'limitar' as entradas apenas ao que se pede (evitar o stop de erro)
        try:
            # Início do programa
            spectreyekath()
            
        except:
            print("\n\nInsira respostas conforme solicitado...\n Reinicie o programa")  #Saída para possíveis erros durante o programa
            perg = input("\nDeseja reiniciar?\n(S = sim ou N = não) : ").lower()
            lista_resp = ["s"]
            
            if perg[0] in lista_resp:
                spectreyekath()
            else:
                print("\nObrigado! Por usar o programa.")
                plt.close()
                cv.destroyAllWindows()
                exit()
                break
            
                
# Executando a função para dar início ao programa                    
spectreyekath()           





