---
layout: default
title: Home
---

[![GitHub license](https://img.shields.io/github/license/materialsvirtuallab/matgl)](https://github.com/materialsvirtuallab/matgl/blob/main/LICENSE)
[![Linting](https://github.com/materialsvirtuallab/matgl/workflows/Linting/badge.svg)](https://github.com/materialsvirtuallab/matgl/workflows/Linting/badge.svg)
[![Testing](https://github.com/materialsvirtuallab/matgl/workflows/Testing%20-%20main/badge.svg)](https://github.com/materialsvirtuallab/matgl/workflows/Testing/badge.svg)
[![Downloads](https://pepy.tech/badge/matgl)](https://pepy.tech/project/matgl)

<img src="https://github.com/materialsvirtuallab/matgl/blob/main/assets/MatGL.png?raw=true" alt="matgl" width="30%" style="float: right">

# Materials Graph Library

## Table of Contents

- [Introduction](#introduction)
- [Status](#status)
- [Architectures](#architectures)
- [Installation](#installation)
- [Usage](#usage)
- [API Docs](#api-docs)
- [Developer's Guide](#developers-guide)
- [References](#references)
- [FAQs](#faqs)
- [Acknowledgements](#acknowledgments)

## Introduction

MatGL (Materials Graph Library) is a graph deep learning library for materials science. Mathematical graphs are a
natural representation for a collection of atoms (e.g., molecules or crystals). Graph deep learning models have been
shown to consistently deliver exceptional performance as surrogate models for the prediction of materials properties.

In this repository, we have reimplemented the original Tensorflow [MatErials 3-body Graph Network (m3gnet)][m3gnet]
and its predecessor, [MEGNet][megnet], using the [Deep Graph Library (DGL)][dgl] and PyTorch.
The goal is to improve the usability, extensibility and scalability of these models. Here are some key improvements
over the TF implementations:

- A more intuitive API and class structure based on DGL.
- Multi-GPU support via PyTorch Lightning. A training utility module has been developed.

This effort is a collaboration between the [Materials Virtual Lab][mavrl] and Intel Labs (Santiago Miret, Marcel
Nassar, Carmelo Gonzales). Please refer to the [official documentation][doc] for more details.

## Status

Major milestones are summarized below. Please refer to [change log][changelog] for details.

- v0.5.1 (Jun 9 2023): Model versioning implemented.
- v0.5.0 (Jun 8 2023): Simplified saving and loading of models. Now models can be loaded with one line of code!
- v0.4.0 (Jun 7 2023): Near feature parity with original TF implementations. Re-trained M3Gnet universal potential now
  available.
- v0.1.0 (Feb 16 2023): Initial implementations of M3GNet and MEGNet architectures have been completed. Expect
  bugs!

## Architectures

<img src="https://github.com/materialsvirtuallab/matgl/blob/main/assets/MxGNet.png?raw=true" alt="m3gnet_schematic" width="50%">

## MEGNet

The [MatErials Graph Network (MEGNet)][megnet] is an implementation of DeepMind's [graph networks][graphnetwork] for
machine learning in materials science. We have demonstrated its success in achieving low prediction errors in a broad
array of properties in both [molecules and crystals][megnet]. New releases have included our recent work on
[multi-fidelity materials property modeling][mfimegnet]. Figure 1 shows the sequential update steps of the graph
network, whereby bonds, atoms, and global state attributes are updated using information from each other, generating an output graph.

## M3GNet

[M3GNet][m3gnet] is a new materials graph neural network architecture that incorporates 3-body interactions in MEGNet. An additional difference is the addition of the coordinates for atoms and
the 3×3 lattice matrix in crystals, which are necessary for obtaining tensorial quantities such as forces and
stresses via auto-differentiation. As a framework, M3GNet has diverse applications, including:

- **Interatomic potential development.** With the same training data, M3GNet performs similarly to state-of-the-art
  machine learning interatomic potentials (MLIPs). However, a key feature of a graph representation is its
  flexibility to scale to diverse chemical spaces. One of the key accomplishments of M3GNet is the development of a
  *universal IP* that can work across the entire periodic table of the elements by training on relaxations performed
  in the [Materials Project][mp].
- **Surrogate models for property predictions.** Like the previous MEGNet architecture, M3GNet can be used to develop
  surrogate models for property predictions, achieving in many cases accuracies that are better or similar to other
  state-of-the-art ML models.

For detailed performance benchmarks, please refer to the publications in the [References](#references) section.

## Installation

Matgl can be installed via pip for the latest stable version:

```bash
pip install matgl
```

For the latest dev version, please clone this repo and install using:

```bash
python setup.py -e .
```

## Usage

Pre-trained M3GNet universal potential and MEGNet models for the Materials Project formation energy and
multi-fidelity band gap are now available. Users who just want to use the models out of the box should use the newly
implemented `matgl.load_model` convenience method. The following is an example of a prediction of the formation
energy for CsCl.

```python
from pymatgen.core import Lattice, Structure
import matgl

model = matgl.load_model("MEGNet-MP-2018.6.1-Eform")

# This is the structure obtained from the Materials Project.
struct = Structure.from_spacegroup("Pm-3m", Lattice.cubic(4.1437), ["Cs", "Cl"], [[0, 0, 0], [0.5, 0.5, 0.5]])
eform = model.predict_structure(struct)
print(f"The predicted formation energy for CsCl is {float(eform.numpy()):.3f} eV/atom.")
```

To obtain a listing of available pre-trained models,

```python
import matgl
print(matgl.get_available_pretrained_models())
```

### Jupyter Tutorials

We have written several [Jupyter notebooks](examples) on the use of MatGL. These notebooks can be run on [Google
Colab][colab]. This will be the primary form of tutorials.

## API Docs

The Sphinx-generated API docs are available [here][apidocs].

## Developer's Guide

A basic [developer's guide](developer.md) has been written to outline the key design elements of matgl. This serves
as a guiding documentation for developers wishing to train and contribute matgl models.

## References

A MatGL publication is currently being written. For now, pls refer to the CITATION.cff file for the citation
information. If you are using any of the pretrained models, please cite the relevant works below:

> ### MEGNet
>
> Chen, C.; Ye, W.; Zuo, Y.; Zheng, C.; Ong, S. P. _Graph Networks as a Universal Machine Learning Framework for
> Molecules and Crystals._ Chem. Mater. 2019, 31 (9), 3564–3572. DOI: [10.1021/acs.chemmater.9b01294][megnet].

> ### Multi-fidelity MEGNet
>
> Chen, C.; Zuo, Y.; Ye, W.; Li, X.; Ong, S. P. _Learning Properties of Ordered and Disordered Materials from
> Multi-Fidelity Data._ Nature Computational Science, 2021, 1, 46–53. DOI: [10.1038/s43588-020-00002-x][mfimegnet].

> ### M3GNet
>
> Chen, C., Ong, S.P. _A universal graph deep learning interatomic potential for the periodic table._ Nature
> Computational Science, 2023, 2, 718–728. DOI: [10.1038/s43588-022-00349-3][m3gnet].

## FAQs

1. The `M3GNet-MP-2021.2.8-PES` differs from the original tensorflow (TF) implementation!

   Answer: `M3GNet-MP-2021.2.8-PES` is a refitted model with some data improvements and minor architectural changes.
   Porting over the weights from the TF version to DGL/PyTorch is non-trivial. We have performed reasonable benchmarking
   to ensure that the new implementation reproduces the broad error characteristics of the original TF implementation
   (see [examples](examples)). However, it is not expected to reproduce the TF version exactly. This refitted model
   serves as a baseline for future model improvements. We do not believe there is value in expending the resources
   to reproduce the TF version exactly.

2. I am getting errors with `matgl.load_model()`!

   Answer: The most likely reason is that you have a cached older version of the model. We often refactor models to
   ensure the best implementation. This can usually be solved by updating your matgl to the latest version
   and clearing your cache using:

   ```bash
   pip install matgl --upgrade
   python -c "import matgl; matgl.clear_cache()"
   ```

   On the next run, the latest model will be downloaded. With effect from v0.5.2, we have implemented a model
   versioning scheme that will detect code vs model version conflicts and alert the user of such problems.

## Acknowledgments

This work was primarily supported by the [Materials Project][mp], funded by the U.S. Department of Energy, Office of
Science, Office of Basic Energy Sciences, Materials Sciences and Engineering Division under contract no.
DE-AC02-05-CH11231: Materials Project program KC23MP. This work used the Expanse supercomputing cluster at the Extreme
Science and Engineering Discovery Environment (XSEDE), which is supported by National Science Foundation grant number
ACI-1548562.

[m3gnetrepo]: https://github.com/materialsvirtuallab/m3gnet "M3GNet repo"
[megnetrepo]: https://github.com/materialsvirtuallab/megnet "MEGNet repo"
[dgl]: https://www.dgl.ai "DGL website"
[mavrl]: http://materialsvirtuallab.org "MAVRL website"
[changelog]: https://matgl.ai/changes "Changelog"
[graphnetwork]: https://arxiv.org/abs/1806.01261 "Deepmind's paper"
[megnet]: https://pubs.acs.org/doi/10.1021/acs.chemmater.9b01294 "MEGNet paper"
[mfimegnet]: https://www.nature.com/articles/s43588-020-00002-x "mfi MEGNet paper"
[m3gnet]: https://www.nature.com/articles/s43588-022-00349-3 "M3GNet paper"
[mp]: http://materialsproject.org "Materials Project"
[apidocs]: https://materialsvirtuallab.github.io/matgl/matgl.html "MatGL API docs"
[doc]: https://matgl.ai "MatGL Documentation"
[colab]: http://colab.google.com "Google Colab"