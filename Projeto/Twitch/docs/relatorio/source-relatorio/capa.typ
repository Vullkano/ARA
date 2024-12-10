#import "setup/template.typ": *

#let titulo = "Análise de Redes Regionais da Twitch: Ligações e Padrões de Interação"
#let subtitulo = "Trabalho de Grupo realizado no âmbito da Unidade Curricular de Análise de Redes Avançada do 1º ano do Mestrado em Ciência de Dados"
#let indice= false
// TODO change to grid
// let versao
// let data
// let autores para ter for loop
#set align(center)
#set page(
  margin: (x: 3cm, y: 2.5cm),
)
#set text(
  hyphenate: false
)
#set par(
  first-line-indent: 0pt,
  justify: false,
)
#par(leading: 0.15cm)[
  #show: smallcaps

  #text(13pt)[ISCTE-IUL] \
  #text(12.5pt)[Mestrado em Ciência de Dados]
]
#v(0.1cm)
#line(length: 100%, stroke: 0.5pt)

#v(0.4cm)
#par(leading: 0.22cm)[
  #text(28pt)[#titulo]
  #linebreak()
  #v(0.1cm)
  #text(16pt)[#subtitulo]
]
#v(0.4cm)
#line(length: 100%, stroke: 1pt)
#if indice {
  v(0.4cm)
} else {
  v(2cm)
}
#v(2cm)
#par(leading: 0.3cm)[
  #text(20pt)[Diogo Freitas, 104841, MCD-LCD]\
  #link("mailto:daafs@iscte-iul.pt")
  #v(0.12cm)
  #text(20pt)[João Francisco Botas, 104782, MCD-LCD]\
  #link("mailto:Joao_Botas@iscte-iul.pt")
  #v(0.12cm)
  #text(20pt)[Rebeca Sampaio, 126628, MCD-LCD]\
  #link("mailto:rhmso1@iscte-iul.pt")
]
#if indice {
  v(2cm)
} else {
  v(6.5cm)
}
#par(leading: 0.2cm)[
  #text(16pt)[21 de dezembro 2024]\
  #text(16pt)[Versão 0.2.0] 
  // 1st number: versão "final" para entregar
  // 2nd number: incremento de conteúdo e tópicos
  // 3rd number: correções de escrita e + info/comments
  // ao aumentar um número, da direita desse passam a 0
]
#v(3cm)
#set align(left)
// #outline(
//   title: text(weight: 600)[Índice],
//   fill: text(15pt, spacing: 220%)[#repeat(" . ")]
// )

