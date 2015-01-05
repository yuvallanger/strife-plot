A stochastic cellular automaton model of evolutionary divergence of quorum sensing
==================================================================================

**A work in progress**

Department of Molecular Microbiology and Biotechnology  
The George S. Wise Faculty of Life Sciences  
Tel-Aviv University

Yuval Langer  
Dr. Avigdor Eldar

Introduction
------------

Quorum sensing is the ability of bacteria to sense their own concentration.
When in small numbers, quorum sensing receptors are not activated, but when
a critical threshold is achieved, these receptors cause production of
"public goods", extracellular products, e.g. surfactants which add motility,
scavenging materials such as siderophores, hydrolases that tear down
otherwise unreachable [weird wording] nutritious polymers,
which benefit each bacteria only when large enough numbers of neighboring
bacteria produce them as well.

[//]: # (What about the lingua franca of quorum sensing?)

"Multiple bacterial species show intraspecific
divergence of their QS systems, where signals from one strain can
activate their own receptor but fail to activate and sometimes inhibit
a receptor from a different strain (2–7)."

In gram positive bacteria, evolutionary close species
[what's evolutionary close? check avigdor's references] exhibit
high diversity of their quorum sensing machinery. "This divergence
seems to be under strong selection, as implied by the functional
divergence and is also corroborated by rapid sequence divergence
(8–9), the signatures of diversifying selection (10–11), and the
spread of divergent QS systems through horizontal gene transfer
(3, 12)."

A proprosed model
that explains how such diversity forms introduces an evolutionary ratchet
in which the order of divergence in QS signal or receptor matters.
The approach used by Eldar et el. to investigate the interactions between
strains was to create a set of differential equations.
This approach is amenable [?] to mathematical analysis
but disregards spatial effects. (Avigdor Eldar et el., 2011)

Stochastic cellular automata simulations were used to investigate social
interactions in bacteria, in which a lattice of abstract cells
compete with their immediate neighbors according to the state of their
microenvironment, thus mimicking a kind of biofilm.
The model used had only one dialect of quorum sensing, examining the existance
or loss of signal, receptor or public goods. Leaving the effects of
multi-lingual quorum sensing systems. (Czaran et el. 2009).

Methods
-------

I've used a combination of Eldar's theoretical model of divergent dialects
and Czaran's stochastic cellular automaton. The simulation consists of a toroid board for which both the width and the height are equal to N.
Each cell has two QS related loci, one loci for the receptor and
another for the signal.
There are two possible receptor alleles, R_{1} and R_{2} and two possible
signal alleles, S_{1} and S_{2}.
The each generation of the simulation follows two stages:
A competition stage and a diffusion stage.
Within the competition stage, a cell is drawn out of the whole board and

[Image: overview of the Avigdorian model]
