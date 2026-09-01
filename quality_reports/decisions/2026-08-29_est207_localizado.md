# EST-207: localizado, y por qué se descargó el fichero equivocado

**Fecha:** 29 de agosto de 2026
**Estado:** LOCALIZADO — falta obtener el texto

## El artículo

Según PubMed:

> Exarchos V, Tkhilaishvili T, Potapov E, Starck C, Trampuz A, Schoenrath F.
> **Successful bacteriophage treatment of infection involving cardiac
> implantable electronic device and aortic graft: a Trojan horse concept.**
> *Europace* 2020 Apr 1;22(4):**597**.

- DOI: [10.1093/europace/euz319](https://doi.org/10.1093/europace/euz319)
- PMID: 31740948
- **Sin PMCID**: no hay texto libre en PubMed Central. Está de pago en Oxford.
- Términos MeSH: Bacteriophages, Phage Therapy, Prosthesis-Related Infections,
  Defibrillators Implantable, Pacemaker Artificial, Device Removal.
  **Ninguno menciona *Pseudomonas*.**

## Por qué salió el fichero equivocado

El artículo ocupa **una sola página: la 597** del volumen 22, número 4. El PDF
que hay guardado es también la página 597 de *Europace*, pero de otro artículo
—«The SPRM in Japanese HF patients»—, y trae su lista de referencias.

La descarga fue por número de página y acertó la página, no el artículo. Es un
fallo reproducible: cualquier recuperación de este tipo, en una revista donde
un número de página puede corresponder a más de un artículo o a otro volumen,
puede traer el documento contiguo sin que nada avise.

## Qué hace falta

1. Pedirlo por préstamo interbibliotecario con el DOI, no con la página.
2. Al recibirlo, **comprobar que el título del PDF coincide con el de S5**
   antes de extraer. Es la comprobación que faltó.
3. Cuando esté, decidir si el caso es de *P. aeruginosa*: los términos MeSH no
   lo indican, y el título tampoco.

## Comprobación que conviene añadir al canal

Ningún script comprueba hoy que el PDF guardado bajo `EST-nnn.pdf` sea el
artículo que S5 dice. Con el título de S5 y el texto del PDF se puede
contrastar automáticamente, y habría cazado este caso el día que se descargó.
