# Vision

## BindingMT's scientific identity

BindingMT is the molecular binding modelling and characterization layer of
MolSysSuite. It provides one canonical scientific component, repository and Python API. The maintainer
accepts this identity and domain expansion under
[#108](https://github.com/uibcdf/bindingmt/issues/108) on 2026-11-11.

Its mission is to make molecular binding questions reproducible, inspectable and
usable through scientifically explicit public operations and replaceable
providers. The domain includes:

- docking molecular partners and exploring candidate bound configurations;
- predicting complete complexes for declared, fixed molecular identities;
- refining declared complexes through explicit physical or model-based methods;
- calculating and predicting binding free energies;
- characterizing binding interfaces and their structural/physicochemical context.

These are distinct scientific operations, not interchangeable names for a score.
The [scope](SCIENTIFIC_SCOPE.md) separates the accepted domain, current received
profiles and future implementations. Existing docking concepts remain useful
within the wider component; the name change does not require a universal problem
or result class.

## Scientific continuity

A researcher should be able to follow an explicit scientific chain:

```text
question + molecular identities + conditions + allowed information
    -> operation-specific inputs and applicability assessment
    -> provider-owned molecular preparation / representation
    -> selected docking, prediction, refinement or evaluation method
    -> native artifacts + faithful molecular correspondence
    -> separately interpreted structure, energetics and interface evidence
    -> inspected and preserved results, alternatives and unsuccessful outcomes
```

Not every workflow needs every operation. A saved result remains inspectable
without its original engine, model weights, accelerator or agent. Original,
completed and refined structures retain distinct identities and evidence.

The existing physical-docking direction remains valuable: **from box-based
docking to molecular-landscape-aware binding models**. Topographic pockets,
pharmacophoric guidance, flexibility information, conformational ensembles,
waters/cofactors and explicit constraints can inform appropriate protocols.
Their presence does not establish universal support or predictive accuracy.

## User experience and public API

Common workflows should be short, clear and dependable: specify an admitted
scientific question, select an appropriate operation/provider and understand
its result or refusal. Defaults with scientific consequences belong to the
resolved protocol and stay inspectable.

Advanced users control the same workflow through documented inputs, states,
protocols, molecular maps, quantities, provider settings, original artifacts,
evaluations and limitations. Direct expert use remains possible without
PeptideMT, Praxis, Nextia or an agent. Convenience and expert routes share
scientific contracts; neither hides changed chemistry, method substitution,
disclosure or resource use.

Power, robustness and performance develop through concrete workflows and
measured evidence. Do not add empty architecture or a catalogue of adapters as
a substitute for useful, qualified scientific operations.

## Ownership and scientific posture

BindingMT owns binding-specific scientific operations, protocol composition,
provider adaptation and interpretation of their outputs. MolSysMT owns general
molecular identity, chemistry, preparation, transformations, formats and reusable
interaction analysis. TopoMT owns topography; PharmacophoreMT and ElastNetMT keep
their specialized methods; MolSysViewer owns generic visualization. BindingMT
composes their public capabilities for binding/interface questions.

PeptideMT owns peptide design intent, constraints, eligibility, selection and
interpretation. Praxis owns cross-platform methodology/applicability and method
selection; Nextia, Recorda, Ackredit and Sabueso retain their project, recording,
attribution and knowledge responsibilities. Optional Moli and MolSys-AI agents
do not own these scientific computations or become runtime prerequisites.

A docking score, neural confidence, interface descriptor, predicted affinity and
binding free-energy estimate answer different questions. Report their definition,
units or scale, conditions, applicability and uncertainty when available. Preserve
disagreements and missing evidence. Computational success, chemical validity,
scientific generalization and experimental confirmation remain separate judgments.
