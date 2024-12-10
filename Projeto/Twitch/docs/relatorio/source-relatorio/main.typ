#import "setup/template.typ": *
#include "capa.typ"
#import "setup/sourcerer.typ": code
#show: project
#counter(page).update(1)
#import "@preview/algo:0.3.3": algo, i, d, comment //https://github.com/platformer/typst-algorithms
#import "@preview/tablex:0.0.8": gridx, tablex, rowspanx, colspanx, vlinex, hlinex
#set text(lang: "pt", region: "pt")
#show link: set text(rgb("#004C99"))

#page(numbering:none)[
  #outline(indent: 2em)  
  // #outline(target: figure)
]
#pagebreak()
#counter(page).update(1)

= Introdução

No âmbito da unidade curricular de Análise de Redes Avançada 

== O que é a Twitch?
Fundada em 2011 e adquirida pela Amazon em 2014, a Twitch é uma plataforma de transmissão ao vivo (_live-streaming_) focada principalmente em videojogos, mas abrangendo também outros tipos de conteúdo, como música, desporto, arte e conversas ao vivo. Foi projetada para ser uma plataforma de conteúdo que incluísse torneios de e-Sports, _streams _pessoais de jogadores individuais e programas de entrevistas relacionados a jogos. A página inicial da Twitch atualmente exibe jogos com base na visualização. O espetador típico é do sexo masculino e tem entre 18 e 34 anos.

=== Como funciona?

A plataforma conta com 4 características que destacam a singularidade e sucesso no universo de transmissões _on-line_:

- Transmissões ao vivo: Os criadores de conteúdo (chamados de _streamers_) transmitem ao vivo enquanto jogam, conversam ou realizam outras atividades;
 
- Interação em tempo real: A Twitch é conhecida pelo seu _chat_ ao vivo, que permite uma interação instantânea entre os streamers e a audiência. Adicionalmente, recursos inovadores como mensagens lidas por Inteligência Artificial (IA) aumentam o dinamismo das transmissões, onde mensagens enviadas por utilizadores são convertidas automaticamente em áudio;

- Monetização: Os streamers podem ser monetizados por meio de:

           - Inscrições pagas (Subscriptions);
           - Doações de espetadores (Bits e doações diretas);
           - Publicidade (Advertisements de entidades externas exibidos durante as transmissões);
           - Parcerias e patrocínios que os próprios _streamers_ têm.

- Programas personalizados de apoio a _streamers_:
           - Afiliado: //TODO: explicar
           - Parceiro: //TODO: explicar 

           
=== Impacto da Twitch na era digital

 A Twitch transformou a forma como as pessoas consomem conteúdo ao vivo, permitindo conexões diretas entre criadores e espetadores.Influenciou diretamente o sucesso de vários jogos, como Among Us, Fall Guys, entre outros.
Para além disso a plataforma dá voz a criadores de diferentes culturas, promovendo a diversidade. Contudo enfrenta alguns problemas a nível da moderação (apesar de cada criador poder atribuir moderadores à sua escolha para as suas streams) tais como discursos de ódio, assédio e conteúdo inadequado.

== Revisão de Literatura

/* A Twitch é uma plataforma de streaming ao vivo que pode ser analisada como uma rede social complexa, devido à interação direta entre criadores de conteúdo e a sua audiência. Apesar de ser conhecida como um espaço voltado para jogos, a Twitch também abrange categorias diversificadas, como música, arte, esportes e conversas ao vivo (Just Chatting).

Na análise de redes sociais, a Twitch permite a aplicação de métricas como centralidade, densidade e modularidade. A centralidade destaca os streamers mais influentes, considerados hubs da rede devido ao grande número de seguidores ou inscritos. A densidade avalia o nível de interação dentro de comunidades, medido pela frequência de mensagens no chat ou colaborações entre criadores. Já a modularidade identifica clusters, ou seja, grupos formados por interesses específicos, como fãs de determinados jogos ou categorias de conteúdo.

*/

Nos últimos anos, a análise de redes sociais tem registado um avanço significativo, graças ao desenvolvimento de técnicas baseadas em matrizes e grafos, apoiadas por ferramentas informáticas. Este progresso tem sido complementado pela aplicação de estatística e matemática, que ajudam a tornar as análises mais objetivas e rigorosas.

O enquadramento teórico das redes sociais privilegia as relações entre indivíduos para compreender a estrutura social, contrastando com as abordagens tradicionais das ciências sociais. Nessas abordagens clássicas, parte-se da definição de categorias preexistentes (como classes sociais, grupos ou organizações), para depois se identificar unidades independentes que são posteriormente agrupadas, com o objetivo de analisar a consistência dos seus comportamentos. Contudo, este método tende a desconsiderar informações importantes resultantes das interações entre as entidades sociais.

Embora grande parte das teorias sociológicas se foque nas relações entre atores, a análise de redes sociais destaca-se por introduzir ferramentas técnicas que permitem verificar empiricamente hipóteses teóricas sobre a natureza das relações e a estrutura das redes.


O significado atribuído à análise de redes sociais é alvo de alguma ambiguidade. Estas incertezas decorrem da diversidade de interpretações e abordagens existentes em diferentes disciplinas e correntes, que conferem ao conceito de rede múltiplos significados, muitas vezes contraditórios, dificultando a sua clarificação.

Apesar dos avanços na área, a análise de redes sociais ainda está amplamente associada a um grupo restrito de cientistas sociais que utilizam uma linguagem técnica muito específica. Esta característica pode representar um entrave para outros investigadores, particularmente para aqueles que estão mais habituados a trabalhar com abordagens baseadas na lógica dos atributos para estudar fenómenos sociais.

Nesta linguagem técnica, matrizes e grafos destacam-se como ferramentas fundamentais para mapear e ilustrar as interações entre indivíduos, grupos e organizações. No entanto, como apontam Alejandro e Norman (2005), as particularidades da análise de redes sociais tornam inadequadas muitas das ferramentas estatísticas tradicionalmente utilizadas para análises sociais.

*(PARTE DO ARTIGO https://dspace.uevora.pt/rdpc/bitstream/10174/12831/1/20881-41419-1-PB_FINAL.pdf)*





#pagebreak()

= Entendimento das redes a estudar

Para a realização deste projeto foram extraídas as redes da Twitch do portal de #link("https://snap.stanford.edu/data/twitch-social-networks.html")[Stanford]. Estas redes fazem parte do #link("https://arxiv.org/abs/1909.13021")[MUSAE], uma coleção de _datasets_ projetada para estudar e auxiliar pesquisas na área de ciência de redes, _Machine Learning_ em grafos, análise de redes sociais e deteção de comunidades. Estes grafos são criados a partir de redes sociais como Facebook, GitHub, Twitch, entre outras. 

No caso da Twitch, dão acesso a redes de 6 línguas diferentes que contêm as informações _user_-_user_ entre _streamers_ da Twitch, recolhidas em Maio de 2018. Ou seja, temos 6 redes semelhantes que são estáticas, porque foram extraídas num determinado momento do tempo; não direcionadas, pois a ligação entre dois _streamers_ é mútua. Como primeiro passo para a análise, é necessário compreender as redes iniciais sem que tenham sido efetuadas quaisquer alterações. 

Tal como foi mencionado, eram fornecidas redes com diferentes idiomas, sendo estas DE, EN, ES, FR, PT-BR e RU, que correspondem a _streams_ onde a língua principal é alemão, inglês, espanhol, francês, português (do Brasil) e russo, respetivamente. Os nodos representam um _streamer_ de uma das 6 línguas especificadas, enquanto as ligações representam as amizades entre esses _streamers_.
/*
- *DE*: Streams onde a língua principal é alemão;
- *EN*: Streams onde a língua principal é inglês;
- *ES*: Streams onde a língua principal é espanhol;
- *FR*: Streams onde a língua principal é francês;
- *PT-BR*: Streams onde a língua principal é português do Brasil;
- *RU*: Streams onde a língua principal é russo.
*/

A informação do número de nodos e de arestas de cada uma destas redes encontra-se na @tabela_inicial.

#figure(
  tablex(
    columns: 3,
    align: (col, row) => {
      if row == 0 {
        center
      } else if (0,5).contains(col) {
        center
      } else {right}
    },
    header-rows:1,
    auto-lines: false,
    // hlinex(),
    [*Língua da Rede*], [*Nº de nodos*], [*Nº de arestas*],
    hlinex(stroke:0.2mm),
    [DE],  [9498] ,  [153138], [EN], [7126], [35324],
    [ES],  [4648] ,  [59382], [FR], [6549], [112666],
    [PT-BR],  [1912] ,  [31299], [RU], [4385], [37304]
),
caption: [Nº de nodos e arestas da rede inicial],
kind:table
)<tabela_inicial>

// Acrescentar mais stats?

É evidente que, observando para a @tabela_inicial, as redes têm alguma disparidade entre elas, tendo em conta o número de nodos e arestas. Isto deve-se sobretudo ao facto de

Para cada uma das línguas eram fornecidos dois ficheiros, um com a informação sobre os nodos, com informação subjacente aos nodos/_streamers_ (musae_xxx_target.csv) e outro com a informação das arestas entre nodos/ligações entre _streamers_ (musae_xxx_edges.csv), onde "xxx" corresponde ao código da língua apresentado acima.

No ficheiro com a informação dos nodos tínhamos acesso às seguintes variáveis correspondentes ao _streamer_:

- `id`: Id único associado à conta da Twitch do _streamer_. Este valor corresponde mesmo a um id verdadeiro da própria Twitch e será dado mais importância na *COLOCAR LINK SECÇÃO*
- `days`: há quantos a conta foi criada;
- `mature`: variável que indica se o _streamer_ exibe conteúdo adulto nas suas _streams_;
- `views`: quantas views o nodo/_streamer_ teve na totalidade do seu canal;
- `partner`: se o _streamer_ é um utilizador parceiro da Twitch; // TODO: colocar imagem/link que explique melhor
- `new_id`: id diferente e único que serve para fazer correspondência de arestas entre nodos.

#pagebreak()

= Métodos 
== Tratamento de dados - > #link("https://dev.twitch.tv/docs/api/reference/")

#figure(code(lang:"JSON", ```JSON
    {
      id: 141981764,
      login: "davyjones",
      display_name: "DavyJones",
      type: "",
      broadcaster_type: "partner",
      description: "Supporting third-party developers",
      profile_image_url: "https://encurtador.com.br/jS9rY",
      offline_image_url: https:"https://encurtador.com.br/ZGdUa",
      view_count: This field has been deprecated,
      email: "not-real@email.com",
      created_at: 2016-12-14T20:32:28Z
    }
  ```), caption: "GET https://api.twitch.tv/helix/users")

#figure(code(lang:"JSON", ```JSON
    {
      broadcaster_id: 141981764,
      broadcaster_login: twitchdev,
      broadcaster_name: "TwitchDev",
      broadcaster_language: "en",
      game_id: 509670,
      game_name: "Science & Technology,
      title: "TwitchDev Monthly Update // May 6, 2021",
      delay: 0,
      tags: ["DevsInTheKnow"],
      content_classification_labels: ["Gambling", "DrugsIntoxication", "MatureGame"],
      is_branded_content: False
    }
  ```), caption: "GET https://api.twitch.tv/helix/channels")

EXPLICAR NOVAS VARS
  
Com os dados extraídos foi necessário verificar algumas incongruências que pudessem existir relativamente a valores omissos. Vê-se que alguns nodos não têm `username`, ...
  
#align(center)[
  #figure(
image("imagens/omissos_exemploRU.png", width: 80%),
  caption: [Distribuição de valores omissos para a rede RU - Rússia]
)
] 
== Análise Exploratória de dados

Após serem tratados todos os dados, segue-se a análise dos dados recolhidos. Nesta secção iremos dar um maior destaque à rede de ??? /* TODO ver se sim */ porque blablabla. Mais à frente iremos comparar redes de outros idiomas e tirar conclusões mais robustas e sustentadas.
  
#pagebreak()

= Modelling

#pagebreak()

= Evaluation

#pagebreak()

= Deployment

= Anexos
#set heading(numbering: (level1, level2,..levels ) => {
  if (levels.pos().len() > 0) {
    return []
  }
  ("Anexo", str.from-unicode(level2 + 64)/*, "-"*/).join(" ")
}) // seria so usar counter(heading).display("I") se nao tivesse o resto
//show heading(level:3)

== - Interface Twitch

/*#align(center)[
  #figure(
image("imagens/", width: 37%),
  caption: [Interface da Twitch]
)
]*/