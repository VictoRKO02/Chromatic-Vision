# Chromatic Manipulator — Reconhecimento de Cores com OpenCV

Projeto desenvolvido a partir de uma ideia iniciada por mim em 2024.1 no IEEE, iniciativa estudantil do SENAI CIMATEC.

A proposta original do **Chromatic Manipulator** era utilizar visão computacional para identificar objetos por cor e, a partir dessa classificação, orientar o movimento de uma garra mecânica.

O projeto completo não foi concluído naquele momento, porém a etapa de reconhecimento de cores foi implementada como prova de conceito e posteriormente reorganizada neste repositório.

## Objetivo

Detectar objetos por cor utilizando uma câmera, identificar sua posição na imagem e retornar as coordenadas do centro do objeto.

## Funcionalidades

- Captura de vídeo em tempo real pela webcam
- Reconhecimento de diferentes cores
- Conversão de imagens de BGR para HSV
- Criação de máscaras por faixa de cor
- Redução de ruídos com operações morfológicas
- Detecção de contornos
- Criação de bounding boxes
- Identificação das coordenadas X e Y do objeto
- Contagem de objetos detectados
- Salvamento de capturas
- Processamento de imagens estáticas

## Tecnologias utilizadas

- Python
- OpenCV
- NumPy

## Estrutura do projeto

```text
IEEE-reconhecimento-cores/
├── app.py
├── detectar_imagem.py
├── requirements.txt
├── README.md
├── .gitignore
└── capturas/
```

## Instalação

Clone o repositório:

```bash
git clone https://github.com/VictoRKO02/IEEE-reconhecimento-cores.git
```

Entre na pasta:

```bash
cd IEEE-reconhecimento-cores
```

Crie um ambiente virtual:

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

## Execução

Para iniciar o reconhecimento pela webcam:

```bash
python app.py
```

### Controles

- `S` — salva uma captura
- `Q` — encerra o programa

As imagens salvas ficam armazenadas na pasta `capturas`.

## Processamento de imagem estática

Também é possível detectar cores em uma imagem já existente:

```bash
python detectar_imagem.py imagem.jpg
```

Para definir o nome da imagem de saída:

```bash
python detectar_imagem.py imagem.jpg --saida resultado.jpg
```

## Como funciona

O fluxo principal do sistema é:

```text
Webcam / Imagem
      ↓
Conversão BGR → HSV
      ↓
Máscaras de cor
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

O espaço de cores HSV é utilizado porque facilita a segmentação das cores ao separar tonalidade, saturação e brilho.

## Aplicação original

A ideia inicial do Chromatic Manipulator era integrar a detecção visual com uma garra mecânica:

```text
Câmera → OpenCV → Cor + posição → Controlador → Garra mecânica
```

Assim, a posição e a cor de um objeto poderiam ser utilizadas para orientar automaticamente o movimento da garra.

## Possíveis evoluções

- Integração com Arduino ou ESP32
- Comunicação com servomotores
- Separação automática de objetos por cor
- Detecção de formas
- Registro das detecções em CSV ou banco de dados
- Conversão de coordenadas em pixels para coordenadas físicas
- Integração com um braço robótico

## Autor

**Victor Mendes**
