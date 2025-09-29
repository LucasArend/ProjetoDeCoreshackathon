# Sistema de Identificação de Tampinhas para Pessoas Cegas 

Este projeto foi desenvolvido durante o **hackathon APEX** com o objetivo de auxiliar pessoas cegas a **separar tampinhas por cor** de forma autônoma.
A aplicação utiliza **visão computacional (OpenCV)** para identificar a cor de tampas plásticas e **áudio (sons de diferentes frequências)** para informar ao usuário quando a tampa está posicionada na área correta.

---

## 🎯 Objetivo

Permitir que pessoas com deficiência visual consigam organizar tampinhas por cor, recebendo feedback sonoro que indica se a tampa foi corretamente identificada.

---

## ⚙️ Como Funciona

1. A **câmera** captura a imagem da mesa com a tampa.
2. O algoritmo:

   * Detecta círculos (representando tampinhas).
   * Analisa a **cor média** da tampa em espaço de cor LAB.
   * Compara a cor detectada com grupos pré-definidos (preto, vermelho, laranja, amarelo, verde, azul, roxo, branco).
3. O sistema emite um **beep** com frequência associada à cor detectada:

   * Quanto mais próxima a tampa estiver da cor correta, mais o beep se mantém consistente.
   * Cada cor possui uma **frequência base única**, facilitando a diferenciação auditiva.
4. Um overlay colorido é exibido na tela, mostrando os grupos de cores e a posição detectada da tampa (para fins de depuração e demonstração).

---

## 🛠️ Tecnologias Utilizadas

* [Python 3](https://www.python.org/)
* [OpenCV](https://opencv.org/) → Processamento de imagem e detecção de formas.
* [NumPy](https://numpy.org/) → Operações matemáticas e vetoriais.
* [scikit-image](https://scikit-image.org/) → Conversão de cores para LAB.
* [Pygame](https://www.pygame.org/) → Geração de sons em tempo real.

---

## 🚀 Instalação e Uso

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Criar ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o programa

```bash
python tampinhas.py
```

---

## 📦 Dependências

No arquivo `requirements.txt`:

```
opencv-python
numpy
pygame
scikit-image
```

---

## 📸 Demonstração

* A janela da câmera exibe:

  * Faixas coloridas representando os **grupos de cores**.
  * O círculo detectado da tampa.
  * O índice do grupo identificado.

* O usuário cego recebe o **feedback sonoro** para saber se a tampa foi corretamente classificada.

---

## 🔮 Possíveis Melhorias

* Ampliar o número de cores suportadas.
* Implementar **interface sonora mais rica**,
* Treinamento com **machine learning** para maior precisão na classificação de cores.
* Adicionar suporte a **hardware dedicado**, como Raspberry Pi com câmera acoplada.

---

## 👥 Autoria

Projeto desenvolvido por **[Lucas Arend Maciel]** durante o **Hackathon APEX** com foco em acessibilidade e inclusão digital.
