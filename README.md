# 📸 Galeria Moderna

## Descrição
Este projeto é uma aplicação de galeria de imagens desenvolvida em Python, utilizando a biblioteca `tkinter` para a interface gráfica e `ttkbootstrap` para um visual moderno. Ele permite navegar por diretórios de imagens, visualizar miniaturas, abrir imagens em tela cheia, e oferece funcionalidades de gerenciamento básico, como exclusão e renomeação de arquivos.

## Recursos
*   **Navegação de Imagens:** Explore imagens em um diretório selecionado.
*   **Filtros de Busca:** Busque imagens por nome de arquivo e filtre por tipo de extensão.
*   **Visualização em Tela Cheia:** Abra imagens em uma janela separada com navegação entre a imagem anterior e próxima.
*   **Exclusão de Imagens:** Delete imagens diretamente da aplicação (com opção de confirmação).
*   **Renomeação de Imagens:** Renomeie arquivos de imagem facilmente através da interface.
*   **Barra Lateral Colapsável:** Minimize ou restaure a barra lateral para otimizar o espaço de visualização.
*   **Barra de Progresso Discreta:** Feedback visual e textual durante o carregamento de imagens na galeria.
*   **Configurações:** Altere o tema da aplicação e o tamanho das miniaturas.

## Como Funciona
A aplicação é construída com `tkinter` e estilizada com `ttkbootstrap`. A lógica principal envolve:
1.  **Busca de Imagens:** A função `buscar_imagens` percorre um diretório e subdiretórios para encontrar arquivos com extensões de imagem suportadas.
2.  **Carregamento da Galeria:** A função `carregar_galeria` gera miniaturas para cada imagem encontrada no diretório e as exibe em um layout de grade dinâmico. O redimensionamento e ajuste das miniaturas são feitos usando a biblioteca `PIL (Pillow)`.
3.  **Visualização:** Ao clicar em uma miniatura, uma nova janela (`Toplevel`) é aberta para exibir a imagem em tamanho maior, permitindo navegação com as setas do teclado e um botão para deletar ou renomear.
4.  **Gerenciamento de Arquivos:** As funções `deletar_imagem` e `renomear_imagem` interagem diretamente com o sistema de arquivos para realizar as operações, atualizando a galeria em seguida.

## Requisitos
Para rodar esta aplicação, você precisará ter Python instalado (versão 3.x recomendada) e as seguintes bibliotecas:
*   `Pillow` (PIL)
*   `ttkbootstrap`

Você pode instalá-las usando pip:
```bash
pip install Pillow ttkbootstrap
```

## Problema Conhecido: Lentidão
Atualmente, a aplicação pode apresentar lentidão, especialmente ao carregar um grande número de imagens ou ao navegar por diretórios com muitas fotos de alta resolução. Isso ocorre principalmente devido ao processamento das miniaturas e ao carregamento das imagens em tempo real na thread principal da interface.

**Possíveis melhorias para o desempenho:**
*   **Carregamento Assíncrono:** Implementar o carregamento de imagens e miniaturas em threads separadas para não travar a interface.
*   **Cache de Miniaturas:** Salvar miniaturas geradas em um diretório temporário para evitar processá-las novamente cada vez que o aplicativo é iniciado ou o diretório é revisitado.
*   **Virtualização da Lista:** Para galerias muito grandes, carregar e renderizar apenas as miniaturas visíveis na tela.
