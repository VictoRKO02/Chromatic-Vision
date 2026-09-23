# Chromatic Vision — Reconhecimento de Cores com OpenCV

O **Chromatic Vision** é um projeto de Visão Computacional desenvolvido em Python para detecção, identificação e localização de objetos com base em suas cores.

A ideia surgiu originalmente em 2024.1, durante uma iniciativa estudantil vinculada ao IEEE no SENAI CIMATEC, a partir do projeto **Chromatic Manipulator**, cuja proposta era utilizar visão computacional para auxiliar uma garra mecânica na identificação e separação de objetos por cor.

Posteriormente, o projeto foi retomado e aprimorado no contexto da **AWS Student Builder Group**, também no SENAI CIMATEC, com foco na consolidação da etapa de visão computacional, organização do código e expansão das funcionalidades de detecção.

---

## Objetivo

Desenvolver uma aplicação capaz de identificar objetos por cor em imagens ou vídeo em tempo real, determinar sua posição na cena e retornar as coordenadas do centro de cada objeto detectado.

O projeto explora conceitos fundamentais de:

* Visão Computacional
* Processamento Digital de Imagens
* Segmentação por cores
* Detecção de objetos por contornos
* Manipulação de imagens em tempo real

---

## Funcionalidades

O sistema possui suporte a processamento por webcam e imagens estáticas.

Entre as principais funcionalidades estão:

* Captura de vídeo em tempo real utilizando webcam
* Detecção de diferentes cores
* Conversão do espaço de cores BGR para HSV
* Segmentação por intervalos de cor
* Criação de máscaras binárias
* Redução de ruídos por operações morfológicas
* Detecção de contornos
* Filtragem de objetos por área
* Geração de bounding boxes
* Identificação das coordenadas centrais `(X, Y)` dos objetos
* Classificação da cor detectada
* Contagem de objetos encontrados
* Salvamento de capturas
* Processamento de imagens estáticas

---

## Tecnologias utilizadas

* **Python**
* **OpenCV**
* **NumPy**

---

## Estrutura do projeto

```text
chromatic-vision/
├── app.py
├── detectar_imagem.py
├── requirements.txt
├── README.md
├── .gitignore
└── capturas/
```

### Principais arquivos

`app.py`

Responsável pela execução da aplicação em tempo real utilizando a webcam.

`detectar_imagem.py`

Permite aplicar o mesmo processo de detecção em imagens estáticas.

`capturas/`

Diretório utilizado para armazenar as imagens capturadas durante a execução do sistema.

---

## Instalação

Clone o repositório:

```bash
git clone https://github.com/VictoRKO02/IEEE-reconhecimento-cores.git
```

Entre no diretório do projeto:

```bash
cd IEEE-reconhecimento-cores
```

Crie um ambiente virtual.

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

---

## Execução

Para iniciar a detecção de objetos em tempo real utilizando a webcam:

```bash
python app.py
```

### Controles

Durante a execução:

```text
S → Salvar captura
Q → Encerrar aplicação
```

As imagens capturadas são armazenadas automaticamente no diretório:

```text
capturas/
```

---

## Processamento de imagens estáticas

O sistema também pode processar imagens armazenadas localmente.

Execute:

```bash
python detectar_imagem.py imagem.jpg
```

Também é possível especificar o nome do arquivo de saída:

```bash
python detectar_imagem.py imagem.jpg --saida resultado.jpg
```

---

## Como funciona

O processamento realizado pelo Chromatic Vision segue o seguinte pipeline:

```text
Webcam / Imagem
       ↓
Aquisição da imagem
       ↓
Conversão BGR → HSV
       ↓
Segmentação por faixa de cor
       ↓
Criação das máscaras
       ↓
Operações morfológicas
       ↓
Redução de ruídos
       ↓
Detecção de contornos
       ↓
Filtro por área
       ↓
Bounding Box
       ↓
Centro do objeto (X, Y)
       ↓
Classificação da cor
```

---

## Por que utilizar HSV?

Imagens capturadas pelo OpenCV utilizam originalmente o formato **BGR**.

Entretanto, para segmentação por cores, o espaço **HSV — Hue, Saturation and Value —** pode ser mais adequado, pois separa as informações de:

* **Hue:** tonalidade da cor
* **Saturation:** intensidade ou saturação
* **Value:** nível de brilho

Essa separação facilita a definição de intervalos utilizados para reconhecer diferentes cores na imagem.

O processamento ocorre conceitualmente da seguinte forma:

```python
imagem_bgr
     ↓
cv2.cvtColor()
     ↓
imagem_hsv
     ↓
cv2.inRange()
     ↓
máscara binária
```

A partir dessa máscara, o OpenCV consegue localizar regiões da imagem que correspondem à cor desejada.

---

## Detecção e localização dos objetos

Após a segmentação, o sistema identifica os contornos presentes na máscara.

Objetos muito pequenos podem ser descartados utilizando um limite mínimo de área, reduzindo falsas detecções causadas por ruídos.

Para cada objeto válido é calculada uma região delimitadora:

```text
┌────────────────────┐
│                    │
│       OBJETO       │
│        ●           │
│      (X, Y)        │
│                    │
└────────────────────┘
```

O ponto `(X, Y)` representa aproximadamente o centro do objeto detectado.

Essas informações podem posteriormente ser utilizadas por outros sistemas, como controladores robóticos.

---

## Origem do projeto

A primeira versão da ideia foi chamada de **Chromatic Manipulator**.

A proposta era integrar uma câmera a uma garra mecânica capaz de identificar objetos por cor e utilizar sua posição para auxiliar no movimento do manipulador.

A arquitetura conceitual era:

```text
Objeto
  ↓
Câmera
  ↓
OpenCV
  ↓
Detecção de cor
  ↓
Posição (X, Y)
  ↓
Controlador
  ↓
Garra mecânica
```

Embora a integração completa com a parte mecânica não tenha sido finalizada na versão inicial, o módulo de visão computacional tornou-se a base para o desenvolvimento do **Chromatic Vision**.

---

## Evolução do projeto

A versão atual concentra-se no desenvolvimento e aprimoramento do módulo de visão computacional.

O sistema evoluiu para permitir:

```text
Imagem
   ↓
Segmentação
   ↓
Detecção
   ↓
Classificação
   ↓
Localização
   ↓
Informações estruturadas
```

Isso possibilita que o projeto seja posteriormente integrado a aplicações de automação, robótica ou análise visual.

---

## Possíveis evoluções

Entre as próximas possibilidades de desenvolvimento estão:

* Integração com Arduino
* Integração com ESP32
* Controle de servomotores
* Integração com braço robótico
* Separação automatizada de objetos
* Conversão de coordenadas em pixels para coordenadas físicas
* Detecção de formas geométricas
* Registro automático das detecções em CSV
* Armazenamento das detecções em banco de dados
* Criação de uma interface gráfica
* Desenvolvimento de uma API para disponibilizar as detecções
* Aplicação de algoritmos de Machine Learning
* Comparação entre segmentação tradicional e modelos de Visão Computacional baseados em Deep Learning

---

## Áreas relacionadas

O projeto está relacionado principalmente às áreas de:

* Inteligência Artificial
* Visão Computacional
* Processamento Digital de Imagens
* Automação
* Robótica
* Sistemas Embarcados

---

## Autor

**Victor Mendes**

Engenharia da Computação — SENAI CIMATEC

GitHub: `VictoRKO02`
