# DOI repair -- screening corpus

The `doi` column was populated from the wrong node of the PubMed XML.
`art.iter("ArticleId")` walks the whole subtree, including
`PubmedData/ReferenceList/Reference/ArticleIdList`, so the stored value was
the DOI of the article's **last cited reference**. Re-read from
`PubmedData/ArticleIdList` only.

| | n |
|---|---|
| Records in corpus | 9561 |
| DOIs corrected | 4817 |
| DOIs recovered where the field was empty | 0 |
| Records PubMed no longer returns (left untouched) | 0 |
| DOIs still shared by more than one record | 0 |

Any DOI still shared is a genuine collision (erratum, reprint, multipart
article) and is listed below for inspection.

## Every correction

| PMID | stored (wrong) | actual | title |
|---|---|---|---|
| 26406987 | 10.1007/BF00228148 | 10.1080/19420862.2015.1099774 | Molecular basis of in vitro affinity maturation and functional evolution of a ne |
| 26475103 | 10.1016/j.colsurfb.2004.10.033 | 10.1128/AEM.02581-15 | Combination Therapy of LysGH15 and Apigenin as a New Strategy for Treating Pneum |
| 26491176 | 10.1128/JCM.02594-05 | 10.1128/JCM.02257-15 | Development of a TaqMan Array Card for Acute-Febrile-Illness Outbreak Investigat |
| 26496237 | 10.1182/blood-2004-04-1482 | 10.1080/19420862.2015.1110660 | Calcium-dependent antigen binding as a novel modality for antibody recycling by  |
| 26497451 | 10.1016/j.watres.2010.01.025 | 10.1128/AEM.02897-15 | Solar Disinfection of Viruses in Polyethylene Terephthalate Bottles. |
| 26497465 | 10.1016/j.ijfoodmicro.2007.11.072 | 10.1128/AEM.01827-15 | A Novel Bacteriophage Targeting Cronobacter sakazakii Is a Potential Biocontrol  |
| 26519290 | 10.1124/jpet.114.217653 | 10.1099/jgv.0.000330 | Novel human anti-claudin 1 mAbs inhibit hepatitis C virus infection and may syne |
| 26563652 | 10.1016/j.jim.2006.07.009 | 10.1080/19420862.2015.1115166 | Development and characterization of human monoclonal antibodies that neutralize  |
| 26574007 | 10.1128/AAC.45.3.649-659.2001 | 10.1128/AAC.01426-15 | Antipseudomonal Bacteriophage Reduces Infective Burden and Inflammatory Response |
| 26582830 | 10.1128/JCM.03235-14 | 10.1128/JCM.02200-15 | Usefulness of High-Quality Core Genome Single-Nucleotide Variant Analysis for Su |
| 26589824 | 10.1007/s00259-010-1700-1 | 10.1007/s11307-015-0909-6 | Hypoxia-Targeting Fluorescent Nanobodies for Optical Molecular Imaging of Pre-In |
| 26590277 | 10.1016/S0043-1354(02)00029-5 | 10.1128/AEM.02382-15 | Isolation of Polyvalent Bacteriophages by Sequential Multiple-Host Approaches. |
| 26590286 | 10.1128/AEM.06969-11 | 10.1128/AEM.02440-15 | Determination of Evolutionary Relationships of Outbreak-Associated Listeria mono |
| 26621622 | 10.1128/MMBR.64.2.412-434.2000 | 10.1128/AAC.01907-15 | Comparative RNA-seq-Based Transcriptome Analysis of the Virulence Characteristic |
| 26651396 | 10.2174/1874306400802010060 | 10.1080/19420862.2015.1119352 | CSL311, a novel, potent, therapeutic monoclonal antibody for the treatment of di |
| 26652308 | 10.1016/j.ab.2008.08.017 | 10.1080/19420862.2015.1118596 | Assessing kinetic and epitopic diversity across orthogonal monoclonal antibody g |
| 26725946 | 10.1016/S0022-2836(02)00241-3 | 10.1038/srep18644 | Structural characterization of eRF1 mutants indicate a complex mechanism of stop |
| 26731115 | 10.1126/science.1165480 | 10.1371/journal.pone.0145872 | Directed Evolution of a Highly Specific FN3 Monobody to the SH3 Domain of Human  |
| 26741979 | 10.1073/pnas.1104144108 | 10.1371/journal.ppat.1005282 | Phages Fight Back: Inactivation of the CRISPR-Cas Bacterial Immune System by Ant |
| 26745374 | 10.1371/journal.pntd.0001930 | 10.1371/journal.pntd.0004292 | A Recombinant Positive Control for Serology Diagnostic Tests Supporting Eliminat |
| 26747455 | 10.1099/mic.0.26905-0 | 10.1099/mic.0.000238 | Comparison of Lactobacillus crispatus isolates from Lactobacillus-dominated vagi |
| 26750429 | 10.1371/journal.pcbi.1000117 | 10.1038/srep19237 | Global Transcriptomic Analysis of Interactions between Pseudomonas aeruginosa an |
| 26765322 | 10.1186/1477-3155-9-45 | 10.1371/journal.pone.0146244 | Spatially Resolved Quantification of Chromatin Condensation through Differential |
| 26765929 | 10.1016/j.molcel.2009.07.026 | 10.1371/journal.pgen.1005797 | P1 Ref Endonuclease: A Molecular Mechanism for Phage-Enhanced Antibiotic Lethali |
| 26781591 | 10.1056/NEJMoa1411627 | 10.1038/srep19234 | Plug-and-Display: decoration of Virus-Like Particles via isopeptide bonds for mo |
| 26784030 | 10.1128/AEM.02670-14 | 10.1371/journal.pone.0146623 | Persistence of F-Specific RNA Coliphages in Surface Waters from a Produce Produc |
| 26785354 | 10.1155/2012/158547 | 10.1371/journal.pone.0146856 | A Human Anti-Toll Like Receptor 4 Fab Fragment Inhibits Lipopolysaccharide-Induc |
| 26785809 | 10.1016/j.jmb.2004.05.051 | 10.1080/19420862.2015.1125067 | Generation, characterization and preclinical studies of a human anti-L1CAM monoc |
| 26786672 | 10.1038/srep10881 | 10.1186/s12929-016-0223-x | Advancement and applications of peptide phage display technology in biomedical s |
| 26798420 | 10.1111/1462-2920.12232 | 10.1155/2016/3578368 | Oxidative Stress in Shiga Toxin Production by Enterohemorrhagic Escherichia coli |
| 26819321 | 10.2217/nnm.15.37 | 10.1128/MMBR.00056-15 | Biological Nanomotors with a Revolution, Linear, or Rotation Motion Mechanism. |
| 26824182 | 10.18632/genesandcancer.2 | 10.18632/oncotarget.7003 | MiR-129 triggers autophagic flux by regulating a novel Notch-1/ E2F7/Beclin-1 ax |
| 26824472 | 10.1128/IAI.05470-11 | 10.1371/journal.pone.0147270 | Protozoan Predation of Escherichia coli O157:H7 Is Unaffected by the Carriage of |
| 26826153 | 10.3201/eid2004.131782 | 10.1136/bmjopen-2015-009933 | Disease severity of Shiga toxin-producing E. coli O157 and factors influencing t |
| 26826235 | 10.1016/j.resmic.2014.10.006 | 10.1128/AEM.03463-15 | Heterogeneity in Induction Level, Infection Ability, and Morphology of Shiga Tox |
| 26833148 | 10.1093/jac/dkv325 | 10.1128/AAC.02859-15 | The Recombinant Bacteriophage Endolysin HY-133 Exhibits In Vitro Activity agains |
| 26840229 | 10.1016/j.jbiotec.2012.05.019 | 10.1371/journal.pone.0147470 | Competitive Mirror Image Phage Display Derived Peptide Modulates Amyloid Beta Ag |
| 26841043 | 10.1016/j.ygeno.2012.06.009 | 10.1371/journal.pone.0148367 | A Site-Specific Integrative Plasmid Found in Pseudomonas aeruginosa Clinical Iso |
| 26848672 | 10.7554/eLife.03497 | 10.3390/ijerph13020187 | Mapping to Support Fine Scale Epidemiological Cholera Investigations: A Case Stu |
| 26851519 | 10.1016/j.nbt.2015.11.005 | 10.1016/j.jim.2016.02.003 | pMINERVA: A donor-acceptor system for the in vivo recombineering of scFv into Ig |
| 26861018 | 10.1101/gr.092759.109 | 10.1128/mBio.01948-15 | Resolving the Complexity of Human Skin Metagenomes Using Single-Molecule Sequenc |
| 26861297 | 10.1016/j.clml.2014.09.007 | 10.3390/ijms17020214 | Generation of Potent Anti-Vascular Endothelial Growth Factor Neutralizing Antibo |
| 26863535 | 10.1002/pro.256 | 10.1371/journal.pone.0148266 | Simvastatin Sodium Salt and Fluvastatin Interact with Human Gap Junction Gamma-3 |
| 26876365 | 10.12703/P6-9 | 10.1292/jvms.15-0310 | Bacteriophage can lyse antibiotic-resistant Pseudomonas aeruginosa isolated from |
| 26888694 | 10.1038/nature13777 | 10.1038/srep21240 | Inhibition of preS1-hepatocyte interaction by an array of recombinant human anti |
| 26890996 | 10.1128/AEM.00025-11 | 10.1080/21655979.2015.1134066 | Novel application of bacteriophage for controlling foaming in wastewater treatme |
| 26893434 | 10.1089/omi.2008.0017 | 10.1128/genomeA.01761-15 | Complete Genome Sequence of Pseudomonas aeruginosa Phage-Resistant Variant PA1RG |
| 26894679 | 10.1002/bab.1080 | 10.1371/journal.pone.0148366 | The Development of a Recombinant scFv Monoclonal Antibody Targeting Canine CD20  |
| 26895405 | 10.1021/ac300864j | 10.1371/journal.pone.0149393 | Next-Generation Sequencing of a Single Domain Antibody Repertoire Reveals Qualit |
| 26897358 | 10.1016/S0161-5890(98)00105-9 | 10.1186/s12885-016-2168-6 | A novel anti-p21Ras scFv antibody reacting specifically with human tumour cell l |
| 26900709 | 10.1039/b908978k | 10.1021/acsnano.5b07338 | Reading Out Single-Molecule Digital RNA and DNA Isothermal Amplification in Nano |
| 26902886 | 10.1078/0171-9335-00256 | 10.1038/srep21661 | Isolation of a recombinant antibody specific for a surface marker of the corneal |
| 26910291 | 10.1016/B978-0-12-416039-2.00006-9 | 10.1080/19420862.2016.1155014 | Differential killing of CD56-expressing cells by drug-conjugated human antibodie |
| 26941153 | 10.1186/1471-2105-11-119 | 10.1128/genomeA.01543-15 | Complete Genome Sequence of PM105, a New Pseudomonas aeruginosa B3-Like Transpos |
| 26950154 | 10.3390/toxins7114817 | 10.3390/toxins8030064 | Isolation of Anti-Ricin Protective Antibodies Exhibiting High Affinity from Immu |
| 26955368 | 10.1128/JB.186.14.4808-4812.2004 | 10.3389/fmicb.2016.00208 | Structural and Enzymatic Characterization of ABgp46, a Novel Phage Endolysin wit |
| 26963639 | 10.4161/mabs.29889 | 10.1080/19420862.2016.1160180 | Improving the CH1-CK heterodimerization and pharmacokinetics of 4Dm2m, a novel p |
| 26964063 | 10.1016/j.watres.2010.12.026 | 10.1371/journal.pone.0151184 | The Formulation of Bacteriophage in a Semi Solid Preparation for Control of Prop |
| 26971047 | 10.1128/AEM.00237-14 | 10.1186/s12866-016-0653-3 | Comparative genomic analysis of toxin-negative strains of Clostridium difficile  |
| 26973628 | 10.1074/jbc.M004191200 | 10.3389/fmicb.2016.00252 | Genetic Evidence for O-Specific Antigen as Receptor of Pseudomonas aeruginosa Ph |
| 26976860 | 10.1099/jmm.0.05149-0 | 10.1128/AAC.03016-15 | Rapid Whole-Cell Assay of Antitubercular Drugs Using Second-Generation Fluoromyc |
| 26982243 | 10.1017/S0950268805003687 | 10.3201/eid2204.151485 | Shiga Toxin-Producing Escherichia coli O157, England and Wales, 1983-2012. |
| 26982594 | 10.1128/mBio.00143-12 | 10.3201/eid2204.150531 | Microevolution of Monophasic Salmonella Typhimurium during Epidemic, United King |
| 26990554 | 10.1002/eji.200535101 | 10.1371/journal.pone.0150320 | Streptococcus pneumoniae Cell-Wall-Localized Phosphoenolpyruvate Protein Phospho |
| 26992211 | 10.18632/oncotarget.6387 | 10.18632/oncotarget.8115 | Armored long non-coding RNA MEG3 targeting EGFR based on recombinant MS2 bacteri |
| 27000701 | 10.1093/bioinformatics/btr039 | 10.1186/s12985-016-0490-x | Genetic characterization of ØVC8 lytic phage for Vibrio cholerae O1. |
| 27013045 | 10.1099/ijs.0.038075-0 | 10.1128/genomeA.00162-16 | Draft Genome Sequence of a Clinically Isolated Extensively Drug-Resistant Pseudo |
| 27014207 | 10.1111/j.1749-4486.2009.01973.x | 10.3389/fmicb.2016.00282 | Small Colony Variants and Single Nucleotide Variations in Pf1 Region of PB1 Phag |
| 27015541 | 10.1002/anie.201505964 | 10.1371/journal.pone.0152522 | Anti-Human VEGF Repebody Effectively Suppresses Choroidal Neovascularization and |
| 27021321 | 10.1038/nature01026 | 10.1128/AAC.00285-16 | Efficacy of Artilysin Art-175 against Resistant and Persistent Acinetobacter bau |
| 27025251 | 10.1186/s13059-015-0611-7 | 10.1128/mBio.00322-16 | Transfer of Viral Communities between Human Individuals during Fecal Microbiota  |
| 27025826 | 10.1007/s00005-016-0387-9 | 10.1093/cid/ciw200 | Beyond Antibiotics: New Therapeutic Approaches for Bacterial Infections. |
| 27029347 | 10.1016/j.neuron.2013.10.061 | 10.1042/BCJ20160114 | High-affinity Anticalins with aggregation-blocking activity directed against the |
| 27035230 | 10.1371/journal.pone.0066943 | 10.3892/mmr.2016.5031 | Profiling lethal factor interacting proteins from human stomach using T7 phage d |
| 27039071 | 10.1093/nar/gkq427 | 10.1186/s12859-016-1001-1 | PAT: predictor for structured units and its application for the optimization of  |
| 27040947 | 10.1016/j.biomaterials.2015.02.002 | 10.1016/j.addr.2016.03.008 | Tumor penetrating peptides for improved drug delivery. |
| 27044623 | 10.1016/j.ajpath.2011.12.037 | 10.1128/JB.01019-15 | Genomic Characterization of a Pattern D Streptococcus pyogenes emm53 Isolate Rev |
| 27053324 | 10.1002/bip.20949 | 10.1021/acscombsci.5b00194 | Rapid Discovery of Functional Small Molecule Ligands against Proteomic Targets t |
| 27061586 | 10.1099/00221287-39-3-321 | 10.1007/s00284-016-1033-9 | Poultry-Like pA+ Biotype of Staphylococcus aureus CC346/084 Clone in Human Popul |
| 27065964 | 10.1007/s00253-014-5552-7 | 10.3389/fmicb.2016.00393 | A Bacteriophage-Acquired O-Antigen Polymerase (Wzyβ) from P. aeruginosa Serotype |
| 27067385 | 10.1101/gr.092759.109 | 10.1038/srep24157 | Monocyte-derived macrophages exhibit distinct and more restricted HIV-1 integrat |
| 27089359 | 10.3855/jidc.3573 | 10.3390/v8040099 | Chlamydiaphage φCPG1 Capsid Protein Vp1 Inhibits Chlamydia trachomatis Growth vi |
| 27099623 | 10.1016/j.tim.2015.12.011 | 10.1111/eva.12364 | Long-term effects of single and combined introductions of antibiotics and bacter |
| 27100289 | 10.1371/journal.pone.0017297 | 10.1371/journal.ppat.1005554 | Antigenic Fingerprinting following Primary RSV Infection in Young Children Ident |
| 27102907 | 10.1093/nar/gkq1019 | 10.1186/s12859-016-1052-3 | Empirical estimation of sequencing error rates using smoothing splines. |
| 27113766 | 10.1074/jbc.M109.096172 | 10.1007/s00294-016-0603-5 | Use of bacteriophage to target bacterial surface structures required for virulen |
| 27120707 | 10.7554/eLife.13152 | 10.7554/eLife.16111 | A lysin to kill. |
| 27129873 | 10.1016/j.pep.2005.01.016 | 10.1186/s12865-016-0146-z | Development and identification of fully human scFv-Fcs against Staphylococcus au |
| 27144083 | 10.1111/j.1749-4486.2009.01973.x | 10.1080/21597081.2015.1096995 | Development of expanded host range phage active on biofilms of multi-drug resist |
| 27151780 | 10.1093/nar/gkl791 | 10.1128/genomeA.00041-16 | Complete Genome Sequences of Broad-Host-Range Pseudomonas aeruginosa Bacteriopha |
| 27158095 | 10.1038/nbt840 | 10.1016/j.addr.2016.04.032 | Microbiome therapeutics - Advances and challenges. |
| 27170747 | 10.3390/v4113090 | 10.1128/JVI.00093-16 | Association between Hemagglutinin Stem-Reactive Antibodies and Influenza A/H1N1  |
| 27171169 | 10.1016/j.jmarsys.2006.03.026 | 10.1371/journal.pone.0155003 | Enumerating Virus-Like Particles and Bacterial Populations in the Sinuses of Chr |
| 27180244 | 10.1186/s13742-015-0051-z | 10.1007/s10096-016-2644-6 | Deep sequencing approach for investigating infectious agents causing fever. |
| 27184415 | 10.1107/S0907444911007281 | 10.1038/srep26071 | Inhibiting complex IL-17A and IL-17RA interactions with a linear peptide. |
| 27185291 | 10.1016/S0145-305X(02)00039-3 | 10.1080/19420862.2016.1186320 | Development and characterization of synthetic antibodies binding to the cystic f |
| 27203546 | 10.18632/oncotarget.2991 | 10.18632/oncotarget.9460 | Phage display library selection of a hypoxia-binding scFv antibody for liver can |
| 27208109 | 10.1099/13500872-142-2-299 | 10.1128/AEM.00090-16 | Analyses of Short-Term Antagonistic Evolution of Pseudomonas aeruginosa Strain P |
| 27210583 | 10.2174/1389557516666160219121836 | 10.1016/j.addr.2016.05.009 | Tumor-targeting peptides from combinatorial libraries. |
| 27210805 | 10.1107/S0907444910045749 | 10.1080/19420862.2016.1190060 | Structural diversity in a human antibody germline library. |
| 27211075 | 10.1128/JB.187.13.4531-4541.2005 | 10.1080/19420862.2016.1189050 | DNA immunization combined with scFv phage display identifies antagonistic GCGR s |
| 27221614 | 10.1111/cbdd.12055 | 10.3892/or.2016.4829 | A new non-muscle-invasive bladder tumor-homing peptide identified by phage displ |
| 27225966 | 10.1111/j.1749-6632.2011.06254.x. | 10.1038/srep26717 | Phage selection restores antibiotic sensitivity in MDR Pseudomonas aeruginosa. |
| 27236552 | 10.1128/JVI.80.2.891-899.2006 | 10.1007/978-3-319-32805-8_4 | Generation of Recombinant Antibodies Against Toxins and Viruses by Phage Display |
| 27258388 | 10.1128/JVI.01943-14 | 10.1371/journal.pone.0156798 | Discovery and Characterization of Phage Display-Derived Human Monoclonal Antibod |
| 27280590 | 10.1128/aem.02850-14 | 10.1371/journal.pone.0156773 | Three New Escherichia coli Phages from the Human Gut Show Promising Potential fo |
| 27303392 | 10.1093/nar/gkv1227 | 10.3389/fmicb.2016.00811 | Genomic Rearrangements and Functional Diversification of lecA and lecB Lectin-Co |
| 27303696 | 10.1016/0378-1119(85)90120-9 | 10.1128/mSphere.00104-15 | Pf Filamentous Phage Requires UvrD for Replication in Pseudomonas aeruginosa. |
| 27304671 | 10.1038/jid.2013.85 | 10.1371/journal.pone.0156800 | Pathogenicity and Epitope Characteristics Do Not Differ in IgG Subclass-Switched |
| 27307569 | 10.1016/j.virol.2008.06.041 | 10.1128/JVI.01023-16 | Characterization of a Novel Conformational GII.4 Norovirus Epitope: Implications |
| 27312006 | 10.1371/journal.pone.0008646 | 10.1111/imm.12635 | Generation and characterization of CD1d-specific single-domain antibodies with d |
| 27313312 | 10.1371/journal.pone.0134512 | 10.1128/genomeA.01515-15 | Genome Sequences of Pseudomonas oryzihabitans Phage POR1 and Pseudomonas aerugin |
| 27320081 | 10.1038/srep21943 | 10.1038/srep28338 | Isolation and characterization of a bacteriophage phiEap-2 infecting multidrug r |
| 27322433 | 10.1016/S1473-3099(14)70854-0 | 10.1371/journal.pone.0157981 | Importance of Multifaceted Approaches in Infection Control: A Practical Experien |
| 27337144 | 10.2217/17460913.2.5.485 | 10.1371/journal.ppat.1005634 | The Janus-Face of Bacteriophages across Human Body Habitats. |
| 27342557 | 10.1016/j.ijmm.2015.07.001 | 10.1128/AEM.01594-16 | Yersinia enterocolitica-Specific Infection by Bacteriophages TG1 and ϕR1-RT Is D |
| 27342558 | 10.3389/fmicb.2014.00542 | 10.1128/AEM.01166-16 | Phage Therapy Is Effective in a Mouse Model of Bacterial Equine Keratitis. |
| 27380413 | 10.1021/ac401555n | 10.1371/journal.pgen.1006134 | Next-Generation "-omics" Approaches Reveal a Massive Alteration of Host RNA Meta |
| 27387381 | 10.1016/j.micinf.2014.02.011 | 10.1371/journal.pone.0158213 | Experimental Phage Therapy for Burkholderia pseudomallei Infection. |
| 27416017 | 10.1002/prca.201600002 | 10.1080/19420862.2016.1212149 | Phage display-derived human antibodies in clinical development and therapy. |
| 27422833 | 10.1016/j.watres.2012.02.020 | 10.1128/AEM.01528-16 | Relevance of F-Specific RNA Bacteriophages in Assessing Human Norovirus Risk in  |
| 27434673 | 10.1074/mcp.M700548-MCP200 | 10.7554/eLife.16228 | NaLi-H1: A universal synthetic library of humanized nanobodies providing highly  |
| 27437775 | 10.18632/oncotarget.3312 | 10.18632/oncotarget.10662 | The natural dietary genistein boosts bacteriophage-mediated cancer cell killing  |
| 27447594 | 10.1128/JB.00344-09 | 10.7554/eLife.16413 | Structural elucidation of a novel mechanism for the bacteriophage-based inhibiti |
| 27449085 | 10.18632/oncotarget.8115 | 10.18632/oncotarget.10681 | Novel miR-122 delivery system based on MS2 virus like particle surface displayin |
| 27454285 | 10.1093/bioinformatics/btu590 | 10.1038/nmeth.3930 | Real-time selective sequencing using nanopore technology. |
| 27457717 | 10.1093/nar/gkh562 | 10.1128/JB.00489-16 | F-Type Bacteriocins of Listeria monocytogenes: a New Class of Phage Tail-Like St |
| 27464652 | 10.1158/1535-7163.MCT-05-0181 | 10.1038/srep30591 | Engineering Salmonella as intracellular factory for effective killing of tumour  |
| 27472381 | 10.1016/S0076-6879(00)23372-7 | 10.1080/19420862.2016.1216742 | High affinity nanobodies against human epidermal growth factor receptor selected |
| 27474712 | 10.1073/pnas.0909285106 | 10.1128/AEM.01496-16 | Transmission of Staphylococcus aureus from Humans to Green Monkeys in The Gambia |
| 27512055 | 10.1128/JVI.01677-12 | 10.1128/JVI.01408-16 | Antigenic Fingerprinting of Antibody Response in Humans following Exposure to Hi |
| 27539157 | 10.5772/20492 | 10.1002/bip.22934 | Protein catalyzed capture agents with tailored performance for in vitro and in v |
| 27548261 | 10.1016/j.copbio.2011.04.020 | 10.1371/journal.pone.0161290 | Selection of Novel Peptides Homing the 4T1 CELL Line: Exploring Alternative Targ |
| 27548264 | 10.1007/s00203-010-0592-6 | 10.1371/journal.pone.0161528 | The Genetic Analysis of an Acinetobacter johnsonii Clinical Strain Evidenced the |
| 27551151 | 10.1016/j.cell.2014.10.053 | 10.1084/jem.20160059 | Identification of GAPDH on the surface of Plasmodium sporozoites as a new candid |
| 27558933 | 10.1074/jbc.M110.153890 | 10.1098/rsob.160120 | The sclerostin-neutralizing antibody AbD09097 recognizes an epitope adjacent to  |
| 27563032 | 10.1093/nar/gki366 | 10.1128/genomeA.00165-16 | Complete Genome Sequence of Pseudomonas aeruginosa Phage AAT-1. |
| 27564098 | 10.18632/oncotarget.2713 | 10.18632/oncotarget.11562 | An anti-ErbB2 fully human antibody circumvents trastuzumab resistance. |
| 27573013 | 10.1038/nature10172 | 10.1128/JB.00458-16 | Requirements for Pseudomonas aeruginosa Type I-F CRISPR-Cas Adaptation Determine |
| 27578501 | 10.1006/abio.1997.2378 | 10.1038/srep32454 | Continuous microfluidic assortment of interactive ligands (CMAIL). |
| 27581884 | 10.1111/j.1462-2920.2008.01784.x | 10.1098/rspb.2016.0721 | Immigration of susceptible hosts triggers the evolution of alternative parasite  |
| 27584691 | 10.1371/journal.pone.0086076 | 10.3201/eid2212.160017 | Whole-Genome Characterization and Strain Comparison of VT2f-Producing Escherichi |
| 27590812 | 10.1371/journal.pone.0085806 | 10.1128/AEM.01415-16 | Genomic and Transcriptional Mapping of PaMx41, Archetype of a New Lineage of Bac |
| 27603936 | 10.1016/j.resmic.2008.03.005 | 10.1371/journal.pone.0162060 | Genomic Characterization of the Novel Aeromonas hydrophila Phage Ahp1 Suggests t |
| 27605673 | 10.1016/j.gene.2004.03.017 | 10.1128/JVI.01492-16 | Identification of Essential Genes in the Salmonella Phage SPN3US Reveals Novel I |
| 27613688 | 10.1038/ng.3219 | 10.1128/AEM.01660-16 | Genomic Analysis of Salmonella enterica Serovar Typhimurium from Wild Passerines |
| 27617744 | 10.1002/dvdy.22344 | 10.1371/journal.pone.0162771 | Enterovirus A71 DNA-Launched Infectious Clone as a Robust Reverse Genetic Tool. |
| 27618915 | 10.1016/j.expneurol.2007.05.019 | 10.1186/s12974-016-0713-5 | Antibody profiling identifies novel antigenic targets in spinal cord injury pati |
| 27626445 | 10.4161/hv.26769 | 10.3390/toxins8090266 | Tetanus Neurotoxin Neutralizing Antibodies Screened from a Human Immune scFv Ant |
| 27631621 | 10.1371/journal.pgen.1002220 | 10.1371/journal.pgen.1006312 | A Recombination Directionality Factor Controls the Cell Type-Specific Activation |
| 27636991 | 10.18632/oncotarget.4198 | 10.18632/oncotarget.11970 | Oxidized macrophage migration inhibitory factor is a potential new tissue marker |
| 27656173 | 10.1093/jac/dkr069 | 10.3389/fmicb.2016.01402 | Enhanced Antibacterial Activity of Acinetobacter baumannii Bacteriophage ØABP-01 |
| 27659070 | 10.1186/1756-0500-2-168 | 10.1038/srep34067 | Characterization and Comparative Genomic Analyses of Pseudomonas aeruginosa Phag |
| 27659529 | 10.18632/oncotarget.6673 | 10.18632/oncotarget.12167 | Induction of anti-EGFR immune response with mimotopes identified from a phage di |
| 27659535 | 10.1158/0008-5472.CAN-06-2887 | 10.18632/oncotarget.12174 | Generation of affibody molecules specific for HPV16 E7 recognition. |
| 27669301 | 10.1016/0192-0561(91)90112-K | 10.3390/toxins8100274 | Glypican-3 Targeting Immunotoxins for the Treatment of Liver Cancer. |
| 27671066 | 10.1093/nar/gkn179 | 10.1128/AAC.01649-16 | Whole-Genome Sequencing Identifies In Vivo Acquisition of a blaCTX-M-27-Carrying |
| 27681597 | 10.1093/protein/gzw050 | 10.1074/jbc.M116.748681 | Deep Mutational Scans as a Guide to Engineering High Affinity T Cell Receptor In |
| 27695058 | 10.1128/AEM.05151-11 | 10.1371/journal.pone.0163966 | Monitoring in Real Time the Formation and Removal of Biofilms from Clinical Rela |
| 27699445 | 10.1038/gt.2015.2 | 10.1007/s00005-016-0427-5 | CRISPR/Cas9 Immune System as a Tool for Genome Engineering. |
| 27716771 | 10.3109/00365521.2015.1033454 | 10.1371/journal.pone.0163648 | Identification and Tumour-Binding Properties of a Peptide with High Affinity to  |
| 27725812 | 10.1128/IAI.00509-07 | 10.3389/fmicb.2016.01519 | Transcriptomic and Metabolomic Analysis Revealed Multifaceted Effects of Phage P |
| 27729062 | 10.1084/jem.186.2.325 | 10.1186/s13075-016-1133-8 | Screening for peptides targeted to IL-7Rα for molecular imaging of rheumatoid ar |
| 27736755 | 10.1126/science.1066869 | 10.1128/AAC.01872-16 | Antibiofilm Activities of a Novel Chimeolysin against Streptococcus mutans under |
| 27749902 | 10.1517/14656566.9.11.1981 | 10.1371/journal.pone.0163184 | High-Throughput Analysis of Global DNA Methylation Using Methyl-Sensitive Digest |
| 27749918 | 10.1074/jbc.M303172200 | 10.1371/journal.pone.0164834 | Voltage-Dependent Anion Channel-1, a Possible Ligand of Plasminogen Kringle 5. |
| 27756316 | 10.1016/S0163-7258(98)00028-X | 10.1186/s12985-016-0619-y | Integrins are not essential for entry of coxsackievirus A9 into SW480 human colo |
| 27770178 | 10.1016/0378-1119(90)90334-N | 10.1007/s00253-016-7924-7 | The temperate Burkholderia phage AP3 of the Peduovirinae shows efficient antimic |
| 27786601 | 10.4161/mabs.28677 | 10.1080/19420862.2016.1249078 | 'In-Format' screening of a novel bispecific antibody format reveals significant  |
| 27790211 | 10.1089/humc.2014.154 | 10.3389/fmicb.2016.01631 | Modular Approach to Select Bacteriophages Targeting Pseudomonas aeruginosa for T |
| 27795361 | 10.1016/j.jaci.2013.08.052 | 10.1128/IAI.00648-16 | Filamentous Bacteriophage Produced by Pseudomonas aeruginosa Alters the Inflamma |
| 27795387 | 10.1128/JCM.01175-08 | 10.1128/mBio.01023-16 | Dual-Reporter Mycobacteriophages (Φ2DRMs) Reveal Preexisting Mycobacterium tuber |
| 27798611 | 10.1073/pnas.1307002110 | 10.1038/nmeth.4038 | Directed evolution using dCas9-targeted somatic hypermutation in mammalian cells |
| 27799208 | 10.1038/305709a0 | 10.1128/AAC.01655-16 | A Novel erm(44) Gene Variant from a Human Staphylococcus saprophyticus Isolate C |
| 27814687 | 10.1371/journal.pone.0067509 | 10.1186/s12866-016-0876-3 | Bacterial genome engineering and synthetic biology: combating pathogens. |
| 27815276 | 10.1093/nar/gkj014 | 10.1128/AEM.02305-16 | Genome Dynamics and Molecular Infection Epidemiology of Multidrug-Resistant Heli |
| 27829980 | 10.1038/nature11723 | 10.1080/19420889.2016.1216740 | Exploring the ecological function of CRISPR-Cas virus defense. |
| 27834591 | 10.1261/rna.1858010 | 10.1080/15476286.2016.1251003 | Viral interference of the bacterial RNA metabolism machinery. |
| 27834817 | 10.1016/j.bbrc.2009.04.039 | 10.3390/ijms17111862 | Classification of 27 Tumor-Associated Antigens by Histochemical Analysis of 36 F |
| 27842517 | 10.1021/cb400619v | 10.1186/s12885-016-2937-2 | Screening and characterization of novel specific peptides targeting MDA-MB-231 c |
| 27842538 | 10.1128/AAC.48.4.1416-1418.2004 | 10.1186/s12906-016-1431-3 | The modified Gingyo-san, a Chinese herbal medicine, has direct antibacterial eff |
| 27845395 | 10.1128/jcm.39.1.362-364.2001 | 10.1038/srep37015 | Slow reduction of IP-10 Levels predicts HBeAg seroconversion in chronic hepatiti |
| 27849134 | 10.3233/HAB-150287 | 10.1080/21655979.2016.1255383 | Developing and characterization of single chain variable fragment (scFv) antibod |
| 27855079 | 10.1016/S0378-1097(03)00577-9 | 10.1128/AAC.01697-16 | Chromosomal Amplification of the blaOXA-58 Carbapenemase Gene in a Proteus mirab |
| 27861551 | 10.1093/bioinformatics/btn235 | 10.1371/journal.pone.0166757 | Genomes of Gardnerella Strains Reveal an Abundance of Prophages within the Bladd |
| 27863402 | 10.18632/oncotarget.4275 | 10.18632/oncotarget.13349 | A fully human anti-CD47 blocking antibody with therapeutic potential for cancer. |
| 27879679 | 10.1016/j.toxicon.2004.11.004 | 10.3390/ijms17111940 | Hydrostatin-TL1, an Anti-Inflammatory Active Peptide from the Venom Gland of Hyd |
| 27881076 | 10.1111/j.1399-3011.1990.tb00976.x | 10.1186/s12859-016-1350-9 | Clustering of disulfide-rich peptides provides scaffolds for hit discovery by ph |
| 27888174 | 10.1099/00221287-16-3-721 | 10.1136/bmjopen-2016-012638 | Phenotypic and antibiogram pattern of V. cholerae isolates from a tertiary care  |
| 27912729 | 10.1002/j.1538-7305.1950.tb00463.x | 10.1186/s12864-016-3340-8 | Genomic insights from whole genome sequencing of four clonal outbreak Campylobac |
| 27912785 | 10.1038/nmeth.f.303 | 10.1186/s40168-016-0212-z | Transmission of viruses via our microbiomes. |
| 27929733 | 10.1016/j.vaccine.2012.09.047 | 10.1080/21645515.2017.1264786 | Antibody repertoire profiling with mimotope arrays. |
| 27929745 | 10.1016/0167-7799(96)10029-9 | 10.1080/19420862.2016.1267086 | An elaborate landscape of the human antibody repertoire against enterovirus 71 i |
| 27934909 | 10.1186/s13062-016-0106-9 | 10.1038/srep38795 | Characterization of the first double-stranded RNA bacteriophage infecting Pseudo |
| 27935413 | 10.3389/fmicb.2015.00224 | 10.1080/19490976.2016.1265196 | Stable core virome despite variable microbiome after fecal transfer. |
| 27978847 | 10.1126/science.1259595 | 10.1186/s13054-016-1549-1 | Non-antibiotic treatments for bacterial diseases in an era of progressive antibi |
| 27992494 | 10.1128/AAC.01513-06 | 10.1371/journal.pone.0168380 | Application of Bacteriophage-containing Aerosol against Nosocomial Transmission  |
| 28000703 | 10.1073/pnas.111551898 | 10.1038/srep39130 | Characterization of Pseudomonas aeruginosa Phage C11 and Identification of Host  |
| 28000755 | 10.1128/mBio.01926-14 | 10.1038/srep39491 | The balance of metagenomic elements shapes the skin microbiome in acne and healt |
| 28006031 | 10.1089/rej.2009.0924 | 10.1371/journal.pone.0167432 | Selection and Characterization of Tau Binding ᴅ-Enantiomeric Peptides with Poten |
| 28008969 | 10.1073/pnas.1108617109 | 10.1038/srep39774 | Determination of equilibrium dissociation constants for recombinant antibodies b |
| 28025997 | 10.1172/JCI58765 | 10.3892/ijmm.2016.2762 | A novel Chk1-binding peptide that enhances genotoxic sensitivity through the cel |
| 28029647 | 10.18632/oncotarget.7879 | 10.18632/oncotarget.14121 | Peptide-guided targeting of GPR55 for anti-cancer therapy. |
| 28056789 | 10.18637/jss.v045.i02 | 10.1186/s12866-016-0916-z | Evolutionary diversification of Pseudomonas aeruginosa in an artificial sputum m |
| 28056857 | 10.1073/pnas.0801053105 | 10.1186/s12885-016-2987-5 | Upregulation of Mrps18a in breast cancer identified by selecting phage antibody  |
| 28060819 | 10.1172/JCI119442 | 10.1371/journal.pone.0167860 | An Anti-Human Lutheran Glycoprotein Phage Antibody Inhibits Cell Migration on La |
| 28060939 | 10.1371/journal.pone.0151409 | 10.1371/journal.pone.0169684 | Large Preferred Region for Packaging of Bacterial DNA by phiC725A, a Novel Pseud |
| 28067844 | 10.1016/j.dnarep.2014.07.008 | 10.3390/genes8010018 | Error-Free Bypass of 7,8-dihydro-8-oxo-2'-deoxyguanosineby DNA Polymerase of Pse |
| 28076361 | 10.4103/0253-7613.83103 | 10.1371/journal.pone.0168615 | Synergy and Order Effects of Antibiotics and Phages in Killing Pseudomonas aerug |
| 28081123 | 10.1146/annurev.genet.34.1.359 | 10.1371/journal.pntd.0005216 | Yersinia enterocolitica, a Neglected Cause of Human Enteric Infections in Côte d |
| 28081707 | 10.1038/nbt.1673 | 10.1186/s12896-016-0322-5 | Antigen-specific single B cell sorting and expression-cloning from immunoglobuli |
| 28090384 | 10.1186/1471-2164-12-402 | 10.1080/21597081.2016.1251379 | Phagebiotics in treatment and prophylaxis of healthcare-associated infections. |
| 28095447 | 10.1128/JCM.00908-12 | 10.1371/journal.pone.0170162 | Identification and Characterization of Single-Chain Antibodies that Specifically |
| 28096486 | 10.1097/QAD.0000000000000415 | 10.1128/mBio.01984-16 | Phage-Derived Protein Induces Increased Platelet Activation and Is Associated wi |
| 28099518 | 10.1016/j.vaccine.2015.12.020 | 10.1371/journal.pone.0170199 | Evaluation of Methods for the Concentration and Extraction of Viruses from Sewag |
| 28114378 | 10.1016/j.ijheh.2011.10.003 | 10.1371/journal.pone.0170399 | FRNA Bacteriophages as Viral Indicators of Faecal Contamination in Mexican Tropi |
| 28122516 | 10.1073/pnas.95.11.6157 | 10.1186/s12868-017-0334-7 | TDP-43 protein variants as biomarkers in amyotrophic lateral sclerosis. |
| 28122648 | 10.1002/aur.237 | 10.1186/s40168-016-0225-7 | Microbiota Transfer Therapy alters gut ecosystem and improves gastrointestinal a |
| 28125612 | 10.1271/bbb.64.2138 | 10.1371/journal.pone.0170305 | A Recombinant Human Anti-Platelet scFv Antibody Produced in Pichia pastoris for  |
| 28152075 | 10.1016/j.jmb.2008.04.049 | 10.1371/journal.pone.0171511 | Pathogen-specific deep sequence-coupled biopanning: A method for surveying human |
| 28166293 | 10.1128/JCM.00202-15 | 10.1371/journal.pone.0171389 | Assessing the genome level diversity of Listeria monocytogenes from contaminated |
| 28166723 | 10.1111/j.1469-0691.2009.03003.x | 10.1186/s12864-017-3516-x | Prophages and adaptation of Staphylococcus aureus ST398 to the human clinic. |
| 28179010 | 10.1093/molbev/msr121 | 10.1186/s12985-017-0701-0 | Characterization and complete genome of the virulent Myoviridae phage JD007 acti |
| 28186116 | 10.1006/abio.1999.4309 | 10.1038/srep42230 | Targeting of phage particles towards endothelial cells by antibodies selected th |
| 28192413 | 10.7554/eLife.10606 | 10.1038/nchembio.2299 | Evolution of a split RNA polymerase as a versatile biosensor platform. |
| 28193211 | 10.1186/1472-6750-9-6 | 10.1186/s12951-016-0240-7 | Display of single-chain variable fragments on bacteriophage MS2 virus-like parti |
| 28207864 | 10.1093/nar/gkn188 | 10.1371/journal.pone.0172303 | Characterisation and genome sequence of the lytic Acinetobacter baumannii bacter |
| 28218671 | 10.1093/bioinformatics/bts139 | 10.3390/toxins9020050 | Human scFvs That Counteract Bioactivities of Staphylococcus aureus TSST-1. |
| 28224117 | 10.1128/AEM.00507-15 | 10.3389/fcimb.2017.00032 | PerC Manipulates Metabolism and Surface Antigens in Enteropathogenic Escherichia |
| 28230780 | 10.1007/s00430-006-0011-4 | 10.3390/v9020036 | A3R Phage and Staphylococcus aureus Lysate Do Not Induce Neutrophil Degranulatio |
| 28231311 | 10.1371/journal.pone.0167378 | 10.1371/journal.pone.0172734 | Handwashing and Ebola virus disease outbreaks: A randomized comparison of soap,  |
| 28257056 | 10.1073/pnas.120163297 | 10.3390/toxins9030077 | Interaction of Type IV Toxin/Antitoxin Systems in Cryptic Prophages of Escherich |
| 28258146 | 10.1128/JB.01230-08 | 10.1128/AEM.03414-16 | A Broad-Host-Range Tailocin from Burkholderia cenocepacia. |
| 28270110 | 10.1073/pnas.1422108112 | 10.1186/s12866-017-0962-1 | Comparative genomics of Enterococcus spp. isolated from bovine feces. |
| 28271446 | 10.1096/fj.02-1044fje | 10.1007/s13238-017-0386-6 | In vitro-engineered non-antibody protein therapeutics. |
| 28272300 | 10.1016/j.jim.2016.06.001 | 10.3390/ijms18030566 | A Human Antibody That Binds to the Sixth Ig-Like Domain of VCAM-1 Blocks Lung Ca |
| 28273830 | 10.3390/genes8010018 | 10.3390/genes8030091 | Erratum: Gu, S. et al. Error-Free Bypass of 7,8-dihydro-8-oxo-2'-deoxyguanosine  |
| 28283023 | 10.1093/jac/dkw093 | 10.1186/s12864-017-3603-z | Genome analysis following a national increase in Scarlet Fever in England 2014. |
| 28287337 | 10.1073/pnas.94.26.14764 | 10.1080/19420862.2017.1299848 | Generation and characterization of protective antibodies to Marburg virus. |
| 28289407 | 10.1126/science.aad6791 | 10.3389/fmicb.2017.00293 | A Novel Antimicrobial Endolysin, LysPA26, against Pseudomonas aeruginosa. |
| 28322317 | 10.1128/iai.01358-06 | 10.1038/srep44929 | Genetic engineering of a temperate phage-based delivery system for CRISPR/Cas9 a |
| 28332627 | 10.1093/nar/gkt382 | 10.1038/srep45163 | Cross-neutralizing anti-HIV-1 human single chain variable fragments(scFvs) again |
| 28335451 | 10.1126/science.352.6293.1506 | 10.3390/v9030050 | A Review of Phage Therapy against Bacterial Pathogens of Aquatic and Terrestrial |
| 28337580 | 10.1128/JVI.02262-13 | 10.1007/s00253-017-8224-6 | Bacteriophage-encoded virion-associated enzymes to overcome the carbohydrate bar |
| 28346467 | 10.1007/s13238-016-0264-7 | 10.1371/journal.pone.0174429 | Characterization and interstrain transfer of prophage pp3 of Pseudomonas aerugin |
| 28348152 | 10.1111/1440-1681.12613 | 10.1128/AAC.02629-16 | Pharmacokinetics and Tolerance of the Phage Endolysin-Based Candidate Drug SAL20 |
| 28348836 | 10.1093/nar/gkr485 | 10.1099/mgen.0.000096 | Evolution of a zoonotic pathogen: investigating prophage diversity in enterohaem |
| 28348855 | 10.1101/gr.074492.107 | 10.1099/mgen.0.000059 | Emergence of a novel lineage containing a prophage in emm/M3 group A Streptococc |
| 28348865 | 10.1371/currents.outbreaks.aa5372d90826e6cb0136ff66bb7a62fc | 10.1099/mgen.0.000070 | Phylogenetic structure of European Salmonella Enteritidis outbreak correlates wi |
| 28348875 | 10.1093/nar/gkr485 | 10.1099/mgen.0.000084 | Short-term evolution of Shiga toxin-producing Escherichia coli O157:H7 between t |
| 28352996 | 10.1093/bioinformatics/btm050 | 10.1007/s00018-017-2509-x | Mechanisms and consequences of intestinal dysbiosis. |
| 28353419 | 10.1371/journal.pone.0013622 | 10.1080/19420862.2017.1288770 | A new anti-mesothelin antibody targets selectively the membrane-associated form. |
| 28367456 | 10.1093/infdis/173.3.758 | 10.1155/2017/5871043 | Synthetic Peptides as Potential Antigens for Cutaneous Leishmaniosis Diagnosis. |
| 28367777 | 10.1371/journal.pone.0077836 | 10.1017/S0950268817000619 | Molecular characterisation of Salmonella strains isolated from outbreaks and spo |
| 28369144 | 10.1371/journal.pone.0121301 | 10.1371/journal.pone.0174909 | ANKRD54 preferentially selects Bruton's Tyrosine Kinase (BTK) from a Human Src-H |
| 28373671 | 10.1016/j.ymeth.2012.12.010 | 10.1038/s41598-017-00728-1 | Targeted rescue of cancer-associated IDH1 mutant activity using an engineered sy |
| 28377527 | 10.1038/srep07649 | 10.1128/mBio.00240-17 | Phage Inhibit Pathogen Dissemination by Targeting Bacterial Migrants in a Chroni |
| 28388565 | 10.18632/oncotarget.10697 | 10.18632/oncotarget.16590 | Prokaryotic expression of MLAA-34 and generation of a novel human ScFv against M |
| 28395597 | 10.1590/0074-02760150423 | 10.1080/20477724.2017.1314069 | Genome sequencing and comparative analysis of an NDM-1-producing Klebsiella pneu |
| 28401893 | 10.4161/bact.24219 | 10.1038/srep46151 | Bacteriophages from ExPEC Reservoirs Kill Pandemic Multidrug-Resistant Strains o |
| 28421049 | 10.1038/srep19237 | 10.3389/fmicb.2017.00548 | Transcriptomic and Metabolomics Profiling of Phage-Host Interactions between Pha |
| 28421882 | 10.1016/j.jbiotec.2010.09.945 | 10.1080/19420862.2017.1319023 | Inhibition of HER3 activation and tumor growth with a human antibody binding to  |
| 28426952 | 10.1016/j.eurpolymj.2016.10.041 | 10.1016/j.cbpa.2017.03.013 | Plant viruses and bacteriophages for drug delivery in medicine and biotechnology |
| 28444417 | 10.1128/jb.176.4.1184-1187.1994 | 10.1007/s00203-017-1381-2 | Identification of proteins differentially expressed by Chlamydia trachomatis tre |
| 28459299 | 10.1128/JCM.02155-08 | 10.1080/21505594.2017.1325070 | Enhanced nasopharyngeal infection and shedding associated with an epidemic linea |
| 28462431 | 10.2166/wh.2016.144 | 10.1007/s11356-017-9050-1 | Total staphylococci as performance surrogate for greywater treatment. |
| 28469136 | 10.1182/blood-2012-04-420943 | 10.1038/s41598-017-01456-2 | Identification of a nanobody specific to human pulmonary surfactant protein A. |
| 28472930 | 10.1038/nmeth.1923 | 10.1186/s12864-017-3729-z | Three novel Pseudomonas phages isolated from composting provide insights into th |
| 28475474 | 10.4049/jimmunol.1500888 | 10.1080/19420862.2017.1325052 | Antibodies targeting G protein-coupled receptors: Recent advances and therapeuti |
| 28484722 | 10.5858/arpa.2012-0422-OA | 10.1155/2017/3780697 | Bacteriophages and Their Immunological Applications against Infectious Threats. |
| 28498803 | 10.1093/nar/gkv070 | 10.18632/oncotarget.17390 | Differentially expressed proteins in glioblastoma multiforme identified with a n |
| 28508219 | 10.1006/viro.2000.0618 | 10.1007/978-1-4939-6964-7_10 | Reverse Genetics of Newcastle Disease Virus. |
| 28512627 | 10.1007/s10096-009-0706-8 | 10.3389/fcimb.2017.00152 | Laboratory Mice Are Frequently Colonized with Staphylococcus aureus and Mount a  |
| 28526816 | 10.1093/nar/gkw458 | 10.1038/s41598-017-01987-8 | Delineation of B-cell Epitopes of Salmonella enterica serovar Typhi Hemolysin E: |
| 28531182 | 10.1186/1471-2334-6-130 | 10.1371/journal.pone.0177943 | Selection of a Biosafety Level 1 (BSL-1) surrogate to evaluate surface disinfect |
| 28539351 | 10.1038/nrmicro2235 | 10.1136/gutjnl-2017-313952 | Bacteriophage transfer during faecal microbiota transplantation in Clostridium d |
| 28542609 | 10.1107/S1399004713031040 | 10.1371/journal.ppat.1006372 | Potent and selective inhibition of pathogenic viruses by engineered ubiquitin va |
| 28559263 | 10.1128/AAC.00824-07 | 10.1128/AAC.00457-17 | Efficient Killing of Planktonic and Biofilm-Embedded Coagulase-Negative Staphylo |
| 28561803 | 10.1016/S0021-9673(01)01021-4 | 10.3390/ijms18061169 | Utilization of Multi-Immunization and Multiple Selection Strategies for Isolatio |
| 28572662 | 10.2174/157016408785909622 | 10.1038/s41598-017-02891-x | Discovery of a polystyrene binding peptide isolated from phage display library a |
| 28583189 | 10.1093/femsle/fnv242 | 10.1186/s13054-017-1709-y | Use of bacteriophages in the treatment of colistin-only-sensitive Pseudomonas ae |
| 28584144 | 10.1107/S0907444909047337 | 10.1128/AAC.00186-17 | Peptide Inhibitors Targeting the Neisseria gonorrhoeae Pivotal Anaerobic Respira |
| 28586008 | 10.2174/1381612819666140110114902 | 10.3892/mmr.2017.6677 | A nanobody targeting carcinoembryonic antigen as a promising molecular probe for |
| 28590540 | 10.1038/scibx.2014.1397 | 10.1002/chem.201702117 | Bicyclic Peptides as Next-Generation Therapeutics. |
| 28592501 | 10.1093/cid/cix188 | 10.1534/genetics.117.201517 | A Physicist's Quest in Biology: Max Delbrück and "Complementarity". |
| 28594392 | 10.1186/2049-2618-1-3 | 10.3390/v9060141 | The Human Gut Phage Community and Its Implications for Health and Disease. |
| 28604602 | 10.1128/genomeA.01250-13 | 10.3390/v9060144 | Highly Sensitive Bacteriophage-Based Detection of Brucella abortus in Mixed Cult |
| 28606056 | 10.1093/bioinformatics/btt656 | 10.1186/s12864-017-3842-z | Comparative genome and transcriptome analysis reveals distinctive surface charac |
| 28611496 | 10.1128/AAC.49.12.4853-4859.2005 | 10.1007/s12088-017-0640-x | A Bacteriophage Mediated Gold Nanoparticles Synthesis and Their Anti-biofilm Act |
| 28611956 | 10.1093/nar/gkr485 | 10.3389/fcimb.2017.00229 | Comparative Genomic and Phylogenetic Analysis of a Shiga Toxin Producing Shigell |
| 28613272 | 10.1172/JCI119096 | 10.3390/v9060150 | Phage-Phagocyte Interactions and Their Implications for Phage Application as The |
| 28617221 | 10.1080/01621459.1952.10483441 | 10.1186/s12859-017-1661-5 | Identification of cancer-specific motifs in mimotope profiles of serum antibody  |
| 28619007 | 10.1016/S0168-1605(00)00501-8 | 10.1186/s12866-017-1043-1 | Whole genome sequencing analyses of Listeria monocytogenes that persisted in a m |
| 28620205 | 10.1016/j.freeradbiomed.2015.10.405 | 10.1038/s41598-017-03799-2 | An anti vimentin antibody promotes tube formation. |
| 28622385 | 10.1073/pnas.0908760106 | 10.1371/journal.pone.0179659 | Effect of acute predation with bacteriophage on intermicrobial aggression by Pse |
| 28628648 | 10.1016/j.chom.2011.08.010 | 10.1371/journal.ppat.1006455 | The adenovirus major core protein VII is dispensable for virion assembly but is  |
| 28630311 | 10.1007/82_2017_3 | 10.1073/pnas.1706110114 | A prokaryotic viral sequence is expressed and conserved in mammalian brain. |
| 28651630 | 10.1038/nature11550 | 10.1186/s40168-017-0282-6 | Maternal inheritance of bifidobacterial communities and bifidophages in infants  |
| 28652618 | 10.1038/nmeth.2019 | 10.1038/s41598-017-03470-w | Intracellular targeting of annexin A2 inhibits tumor cell adhesion, migration, a |
| 28654001 | 10.4168/aair.2014.6.6.558 | 10.3390/ijms18071373 | Profiling the Extended Cleavage Specificity of the House Dust Mite Protease Alle |
| 28663444 | 10.1107/S0907444909052925 | 10.1126/science.aam6892 | Atomic structure of the human cytomegalovirus capsid with its securing tegument  |
| 28666016 | 10.1002/ibd.20118 | 10.1371/journal.pone.0180509 | Detection of colonic dysplasia in patients with ulcerative colitis using a targe |
| 28669053 | 10.4103/0973-1482.138007 | 10.1007/s00432-017-2468-5 | Efficient targeting of CD13 on cancer cells by the immunotoxin scFv13-ETA' and t |
| 28672882 | 10.1089/ars.2007.1693 | 10.3390/md15070200 | A Novel Benzoquinone Compound Isolated from Deep-Sea Hydrothermal Vent Triggers  |
| 28676857 | 10.3390/ijms17050796 | 10.1155/2017/4101653 | Salinomycin Exerts Anticancer Effects on PC-3 Cells and PC-3-Derived Cancer Stem |
| 28692019 | 10.1093/bioinformatics/btq315 | 10.1038/nmicrobiol.2017.112 | Bacteriophage evolution differs by host, lifestyle and genome. |
| 28696303 | 10.1111/pedi.12468 | 10.1073/pnas.1706359114 | Intestinal virome changes precede autoimmunity in type I diabetes-susceptible ch |
| 28700235 | 10.1371/journal.pone.0042342 | 10.1021/acs.est.7b02703 | Quantitative CrAssphage PCR Assays for Human Fecal Pollution Measurement. |
| 28704436 | 10.1016/j.addr.2005.01.027 | 10.1371/journal.pone.0180798 | Platinum nanoparticles induce damage to DNA and inhibit DNA replication. |
| 28704569 | 10.1006/abio.2000.4753 | 10.1371/journal.ppat.1006495 | A virulence-associated filamentous bacteriophage of Neisseria meningitidis incre |
| 28710848 | 10.1038/ncomms16085 | 10.1128/microbiolspec.MTBP-0001-2016 | Breaking Transmission with Vaccines: The Case of Tuberculosis. |
| 28713356 | 10.1007/978-1-4939-0473-0_9 | 10.3389/fmicb.2017.01229 | A Genotypic Analysis of Five P. aeruginosa Strains after Biofilm Infection by Ph |
| 28714913 | 10.1093/glycob/cwv168 | 10.3390/v9070188 | Novel Fri1-like Viruses Infecting Acinetobacter baumannii-vB_AbaP_AS11 and vB_Ab |
| 28719653 | 10.1182/blood-2011-06-362053 | 10.1371/journal.pone.0179039 | Isolation of a monoclonal antibody from a phage display library binding the rhes |
| 28719657 | 10.1128/AAC.45.3.649-659.2001 | 10.1371/journal.pone.0179245 | Isolation and in vitro evaluation of bacteriophages against MDR-bacterial isolat |
| 28740223 | 10.1097/QAD.0b013e328322ffac | 10.1038/s41598-017-06594-1 | Dual functional Phi29 DNA polymerase-triggered exponential rolling circle amplif |
| 28750102 | 10.1371/journal.pone.0024418 | 10.1371/journal.pone.0182121 | Stability of bacteriophages in burn wound care products. |
| 28797098 | 10.1186/1471-2164-8-121 | 10.1371/journal.pone.0182940 | Comparative genomics of two super-shedder isolates of Escherichia coli O157:H7. |
| 28797124 | 10.1002/mds.26377 | 10.1371/journal.pone.0181844 | Preclinical development of a vaccine against oligomeric alpha-synuclein based on |
| 28807909 | 10.7717/peerj.2261 | 10.1128/AAC.00954-17 | Development and Use of Personalized Bacteriophage-Based Therapeutic Cocktails To |
| 28808331 | 10.1111/j.1462-2920.2009.02030.x | 10.1038/s41598-017-08336-9 | Pro- and anti-inflammatory responses of peripheral blood mononuclear cells induc |
| 28827559 | 10.1107/S0907444911001314 | 10.1038/s41598-017-08273-7 | Selection of nanobodies with broad neutralizing potential against primary HIV-1  |
| 28830351 | 10.1093/nar/gkj014 | 10.1186/s12866-017-1094-3 | Genome sequencing and comparative genomics of enterohemorrhagic Escherichia coli |
| 28840811 | 10.1097/00000637-198105000-00008 | 10.1128/microbiolspec.BAD-0003-2016 | Bacteriophage Clinical Use as Antibacterial "Drugs": Utility and Precedent. |
| 28840820 | 10.4049/jimmunol.179.10.7021 | 10.1128/microbiolspec.BAD-0006-2016 | Ecological Therapeutic Opportunities for Oral Diseases. |
| 28851366 | 10.1099/mic.0.030486-0 | 10.1186/s12915-017-0415-1 | A widespread family of polymorphic toxins encoded by temperate phages. |
| 28852111 | 10.1128/JCM.01779-15 | 10.1038/s41598-017-10083-w | Development of an Affimer-antibody combined immunological diagnosis kit for glyp |
| 28854224 | 10.1371/journal.ppat.1005288 | 10.1371/journal.ppat.1006602 | The 5'-poly(A) leader of poxvirus mRNA confers a translational advantage that ca |
| 28859690 | 10.1111/bjd.14773 | 10.1186/s13063-017-2118-x | Targeted anti-staphylococcal therapy with endolysins in atopic dermatitis and th |
| 28860505 | 10.1093/nar/gkh340 | 10.1038/s41598-017-10755-7 | Endolysin LysEF-P10 shows potential as an alternative treatment strategy for mul |
| 28869283 | 10.1136/gutjnl-2017-313952 | 10.1111/apt.14280 | Review article: the human intestinal virome in health and disease. |
| 28870171 | 10.1093/ve/vew007 | 10.1186/s12864-017-4065-z | Evolution of mobile genetic element composition in an epidemic methicillin-resis |
| 28881167 | 10.1080/20002297.2017.1334504 | 10.1080/21505594.2017.1376147 | Meeting report: The 12th European oral microbiology workshop (EOMW) in Stockholm |
| 28887415 | 10.4269/ajtmh.2011.10-0389 | 10.1128/AEM.01457-17 | Inactivation of Human Norovirus Genogroups I and II and Surrogates by Free Chlor |
| 28892521 | 10.1124/pr.114.009217 | 10.1371/journal.pone.0183969 | A systems medicine approach for finding target proteins affecting treatment outc |
| 28902178 | 10.1007/s10059-009-0028-9 | 10.3390/ijms18091968 | Tumor Inhibitory Effect of IRCR201, a Novel Cross-Reactive c-Met Antibody Target |
| 28904355 | 10.1007/s00253-008-1839-x | 10.1038/s41598-017-11832-7 | Highly potent antimicrobial modified peptides derived from the Acinetobacter bau |
| 28906479 | 10.1371/journal.pone.0004944 | 10.3390/v9090258 | Characterization of vB_SauM-fRuSau02, a Twort-Like Bacteriophage Isolated from a |
| 28912771 | 10.1126/science.aad6791 | 10.3389/fmicb.2017.01669 | Selection of Functional Quorum Sensing Systems by Lysogenic Bacteriophages in Ps |
| 28916756 | 10.1371/journal.pone.0055116 | 10.1038/s41467-017-00488-6 | Identification of the S100 fused-type protein hornerin as a regulator of tumor v |
| 28933630 | 10.4161/mabs.23049 | 10.1080/19420862.2017.1381812 | Going native: Direct high throughput screening of secreted full-length IgG antib |
| 28935111 | 10.1007/s12033-012-9598-4 | 10.1016/bs.mie.2017.06.030 | Evaluation of Virus-Like Particle-Based Tumor-Associated Carbohydrate Immunogen  |
| 28939600 | 10.1080/02786826.2010.501351 | 10.1128/AEM.01270-17 | Evaluation of Chlorine Treatment Levels for Inactivation of Human Norovirus and  |
| 28939601 | 10.1128/JVI.02763-12 | 10.1128/AEM.01567-17 | A Lytic Providencia rettgeri Virus of Potential Therapeutic Value Is a Deep-Bran |
| 28950849 | 10.1016/S0022-5347(17)36966-5 | 10.1186/s12894-017-0283-6 | Bacteriophages for treating urinary tract infections in patients undergoing tran |
| 28951481 | 10.1073/pnas.1503141112 | 10.1128/mBio.01490-17 | Bacterial Whack-a-Mole: Reconsidering the Public Health Relevance of Using Carba |
| 28953230 | 10.1038/356083a0 | 10.3390/ijms18102064 | A Novel Fully Human Agonistic Single Chain Fragment Variable Antibody Targeting  |
| 28963461 | 10.1515/hsz-2012-0184 | 10.1038/s41598-017-12572-4 | The identification of molecular target of (20S) ginsenoside Rh2 for its anti-can |
| 28967893 | 10.1016/j.cub.2016.02.056 | 10.1038/nnano.2017.188 | A synthetic intrabody-based selective and generic inhibitor of GPCR endocytosis. |
| 28974033 | 10.1007/s12033-013-9669-1 | 10.3390/toxins9100309 | The European AntibotABE Framework Program and Its Update: Development of Innovat |
| 28985502 | 10.1038/nchembio.2410 | 10.1016/j.molcel.2017.09.007 | The Revolution Continues: Newly Discovered Systems Expand the CRISPR-Cas Toolkit |
| 29018773 | 10.1111/j.1749-4486.2009.01973.x | 10.3389/fcimb.2017.00418 | Activity of Bacteriophages in Removing Biofilms of Pseudomonas aeruginosa Isolat |
| 29023522 | 10.1111/j.1365-2036.2006.02861.x | 10.1371/journal.pone.0186239 | Microencapsulation of Clostridium difficile specific bacteriophages using microf |
| 29026171 | 10.1021/ac950914h | 10.1038/s41598-017-13363-7 | Characterization and genomic study of "phiKMV-Like" phage PAXYB1 infecting Pseud |
| 29026949 | 10.1006/smim.1996.0035 | 10.1007/s00262-017-2076-x | A filamentous bacteriophage targeted to carcinoembryonic antigen induces tumor r |
| 29029605 | 10.1038/ni.2647 | 10.1186/s12943-017-0730-8 | Monitoring multiple myeloma by idiotype-specific peptide binders of tumor-derive |
| 29038472 | 10.1007/978-1-60761-723-5_13 | 10.1038/s41467-017-01055-9 | Phage-assisted continuous evolution of proteases with altered substrate specific |
| 29040265 | 10.1016/j.molimm.2014.01.002 | 10.1371/journal.pone.0185976 | Analysis of peripheral B cells and autoantibodies against the anti-nicotinic ace |
| 29051051 | 10.1080/19420862.2017.1281504 | 10.1016/j.virusres.2017.10.011 | Brief introduction of current technologies in isolation of broadly neutralizing  |
| 29066548 | 10.1128/IAI.68.8.4673-4680.2000 | 10.1128/mBio.01558-17 | Genome-Wide Discovery of Genes Required for Capsule Production by Uropathogenic  |
| 29077053 | 10.1016/j.tim.2013.06.002 | 10.3390/v9110315 | Differential Effect of Newly Isolated Phages Belonging to PB1-Like, phiKZ-Like a |
| 29079627 | 10.1111/j.1365-2672.1984.tb01372.x | 10.1128/AEM.01866-17 | F-Specific RNA Bacteriophages, Especially Members of Subgroup II, Should Be Reco |
| 29084989 | 10.1016/j.jmb.2005.03.072 | 10.1038/s41598-017-14112-6 | Nanobodies effectively modulate the enzymatic activity of CD38 and allow specifi |
| 29089428 | 10.1007/s10260-010-0142-z | 10.1128/mBio.01341-17 | Associations among Antibiotic and Phage Resistance Phenotypes in Natural and Cli |
| 29089574 | 10.1538/expanim.14-0059 | 10.1038/s41598-017-14823-w | High throughput discovery of influenza virus neutralizing antibodies from phage- |
| 29099783 | 10.1128/JVI.01308-09 | 10.3390/v9110328 | Metagenomic Analysis of Therapeutic PYO Phage Cocktails from 1997 to 2014. |
| 29109173 | 10.1016/j.bbrc.2012.09.066 | 10.1128/IAI.00784-17 | The Homolog of the Gene bstA of the BTP1 Phage from Salmonella enterica Serovar  |
| 29109551 | 10.1107/S0907444909042073 | 10.1038/s41598-017-14797-9 | Modular endolysin of Burkholderia AP3 phage has the largest lysozyme-like cataly |
| 29115982 | 10.1017/S0950268815001636 | 10.1186/s13104-017-2878-0 | Phage typing or CRISPR typing for epidemiological surveillance of Salmonella Typ |
| 29116500 | 10.1073/pnas.0909775106 | 10.1007/978-1-4939-7447-4_4 | Modular Construction of Large Non-Immune Human Antibody Phage-Display Libraries  |
| 29116514 | 10.1016/j.biomaterials.2010.11.073 | 10.1007/978-1-4939-7447-4_18 | Combine Phage Antibody Display Library Selection on Patient Tissue Specimens wit |
| 29117225 | 10.1016/j.jinf.2015.11.002 | 10.1371/journal.pone.0187288 | Genomic comparison between Staphylococcus aureus GN strains clinically isolated  |
| 29118372 | 10.1002/prot.24403 | 10.1038/s41598-017-14886-9 | Human single chain-transbodies that bound to domain-I of non-structural protein  |
| 29119245 | 10.2337/dcS13-2032 | 10.1007/s00125-017-4491-0 | Development and characterisation of a novel glucagon like peptide-1 receptor ant |
| 29123083 | 10.1073/pnas.1114518108 | 10.1038/s41467-017-01096-0 | Identification of a peptide recognizing cerebrovascular changes in mouse models  |
| 29123253 | 10.1128/IAI.00021-12 | 10.1038/s41598-017-15618-9 | The gene fmt, encoding tRNAfMet-formyl transferase, is essential for normal grow |
| 29132246 | 10.1016/j.jbiotec.2010.01.012 | 10.1080/1061186X.2017.1405424 | Phage-derived protein-mediated targeted chemotherapy of pancreatic cancer. |
| 29132309 | 10.1111/j.1096-0031.1989.tb00562.x | 10.1186/s12864-017-4248-7 | Significant differences in terms of codon usage bias between bacteriophage early |
| 29133882 | 10.1093/nar/gkm265 | 10.1038/s41564-017-0053-y | Discovery of an expansive bacteriophage family that includes the most abundant v |
| 29142290 | 10.1016/0263-7855(96)00018-5 | 10.1038/s41598-017-15930-4 | Characterizing the conformational landscape of MDM2-binding p53 peptides using M |
| 29146960 | 10.1111/j.1462-2920.2009.02058.x | 10.1038/s41467-017-01544-x | Assessing species biomass contributions in microbial communities via metaproteom |
| 29147662 | 10.1002/jobm.201200710 | 10.1155/2017/9351017 | Effectiveness of a Lytic Phage SRG1 against Vancomycin-Resistant Enterococcus fa |
| 29148397 | 10.1073/pnas.1304978110 | 10.3201/eid2312.170628 | Evolutionary Context of Non-Sorbitol-Fermenting Shiga Toxin-Producing Escherichi |
| 29150513 | 10.1186/1471-2105-12-395 | 10.1128/AEM.02164-17 | High Prevalence and Genetic Diversity of Large phiCD211 (phiCDIF1296T)-Like Prop |
| 29158280 | 10.1007/s12275-011-1512-4 | 10.1128/AAC.01714-17 | Proof-of-Principle Study in a Murine Lung Infection Model of Antipseudomonal Act |
| 29159596 | 10.2174/1389201017666160823144032 | 10.1007/s11684-017-0596-6 | Human monoclonal antibodies as candidate therapeutics against emerging viruses. |
| 29162715 | 10.1371/journal.pbio.1002128 | 10.1128/mBio.01874-17 | Bacteriophage Transcytosis Provides a Mechanism To Cross Epithelial Cell Layers. |
| 29162919 | 10.1021/ac0341261 | 10.1038/s41598-017-16290-9 | Production of recombinant human procollagen type I C-terminal propeptide and est |
| 29164271 | 10.1371/journal.pone.0186239 | 10.1007/s00018-017-2715-6 | Bacteriophages targeting intestinal epithelial cells: a potential novel form of  |
| 29165352 | 10.2174/157016461202150903114319 | 10.3390/ijms18112376 | Antibody-Based Protective Immunity against Helminth Infections: Antibody Phage D |
| 29176754 | 10.1007/s00253-015-6492-6 | 10.1038/s41598-017-16411-4 | The O-specific polysaccharide lyase from the phage LKA1 tailspike reduces Pseudo |
| 29180523 | 10.1186/1756-0500-5-280 | 10.1128/AAC.01358-17 | Efficacy of Novel Antistaphylococcal Ectolysin P128 in a Rat Model of Methicilli |
| 29180782 | 10.1128/JVI.01084-10 | 10.1038/s41598-017-16451-w | Alpha-helicoidal HEAT-like Repeat Proteins (αRep) Selected as Interactors of HIV |
| 29182455 | 10.1177/108705719900400407 | 10.1080/19420862.2017.1409320 | Isolation of blood-brain barrier-crossing antibodies from a phage display librar |
| 29201902 | 10.3389/fmicb.2016.01112 | 10.1155/2017/3612015 | In Vivo Studies on the Influence of Bacteriophage Preparations on the Autoimmune |
| 29203765 | 10.1016/j.jim.2004.10.006 | 10.1038/s41467-017-02057-3 | Internalization of a polysialic acid-binding Escherichia coli bacteriophage into |
| 29207071 | 10.1158/0008-5472.CAN-10-2277 | 10.3892/ijo.2017.4205 | Hepatocellular carcinoma-targeted nanoparticles for cancer therapy. |
| 29207143 | 10.1158/1535-7163.MCT-11-0891 | 10.3892/or.2017.6131 | Screening and antitumor effect of an anti‑CTLA‑4 nanobody. |
| 29208163 | 10.1016/S1473-3099(15)00424-7 | 10.1099/mgen.0.000141 | Population structure of Escherichia coli O26 : H11 with recent and repeated stx2 |
| 29233140 | 10.1107/S2053230X17005969 | 10.1186/s12934-017-0837-z | Selection, characterization, and thermal stabilization of llama single domain an |
| 29233895 | 10.1128/AEM.01369-08 | 10.1128/mBio.01751-17 | Disabling a Type I-E CRISPR-Cas Nuclease with a Bacteriophage-Encoded Anti-CRISP |
| 29255267 | 10.1093/nar/30.4.e15 | 10.1038/s41598-017-18041-2 | Detection of Cystic Fibrosis Serological Biomarkers Using a T7 Phage Display Lib |
| 29258650 | 10.2807/ese.16.15.19840-en | 10.2807/1560-7917.ES.2017.22.50.17-00196 | Re-evaluation of a 2014 multi-country European outbreak of Salmonella Enteritidi |
| 29259289 | 10.4161/gmic.1.6.14087 | 10.1038/s41396-017-0015-7 | Resolution of habitat-associated ecogenomic signatures in bacteriophage genomes  |
| 29266197 | 10.1038/nrmicro.2017.30 | 10.1111/bph.14106 | Phages of life - the path to pharma. |
| 29266228 | 10.1007/s00018-017-2715-6 | 10.1111/cei.13092 | Therapeutic potential of phages in autoimmune liver diseases. |
| 29268793 | 10.1155/2012/631460 | 10.1186/s13071-017-2576-8 | Selection strategy of phage-displayed immunogens based on an in vitro evaluation |
| 29273737 | 10.1128/JB.186.20.6891-6901.2004 | 10.1038/s41598-017-18096-1 | Hydrolytic activity determination of Tail Tubular Protein A of Klebsiella pneumo |
| 29283291 | 10.1107/S0021889892009944 | 10.1080/19420862.2017.1412026 | Structural insights into humanization of anti-tissue factor antibody 10H10. |
| 29284038 | 10.1093/nar/gkh271 | 10.1371/journal.pone.0190062 | Comparative analysis of the end-joining activity of several DNA ligases. |
| 29293692 | 10.2217/fmb.09.44 | 10.1371/journal.pone.0190836 | Comparison of genomes and proteomes of four whole genome-sequenced Campylobacter |
| 29301020 | 10.1016/j.jmb.2010.09.006 | 10.1093/protein/gzx063 | Discovery of internalizing antibodies to basal breast cancer cells. |
| 29306353 | 10.3389/fmicb.2015.01120 | 10.1099/mgen.0.000142 | Vibrio cholerae genomic diversity within and between patients. |
| 29311716 | 10.1109/TVCG.2014.2346248 | 10.1038/s41598-017-18341-7 | Discovering viral genomes in human metagenomic data by predicting unknown protei |
| 29318984 | 10.1101/cshperspect.a016717 | 10.1128/ecosalplus.ESP-0006-2017 | A Brief History of Shigella. |
| 29324905 | 10.1038/nrg3114 | 10.1371/journal.ppat.1006726 | Strains of bacterial species induce a greatly varied acute adaptive immune respo |
| 29329326 | 10.1038/srep30859 | 10.1371/journal.pone.0190850 | Utilization of peptide phage display to investigate hotspots on IL-17A and what  |
| 29330364 | 10.1021/jm070861j | 10.1038/s41598-017-18494-5 | Polypharmacy through Phage Display: Selection of Glucagon and GLP-1 Receptor Co- |
| 29331148 | 10.1016/0003-2697(76)90527-3 | 10.1186/s12934-017-0856-9 | Isolation of anti-extra-cellular vesicle single-domain antibodies by direct pann |
| 29348170 | 10.1107/S0907444909042073 | 10.1074/jbc.RA117.001611 | CRISPR RNA and anti-CRISPR protein binding to the Xanthomonas albilineans Csy1-C |
| 29359149 | 10.1007/s00705-015-2680-z | 10.1155/2017/3723254 | Isolation of Potential Phages against Multidrug-Resistant Bacterial Isolates: Pr |
| 29362234 | 10.1128/AEM.07621-11 | 10.1128/mBio.01923-17 | Are Phage Lytic Proteins the Secret Weapon To Kill Staphylococcus aureus? |
| 29374036 | 10.1021/es103488e | 10.1128/AEM.02374-17 | Fate of the Urinary Tract Virus BK Human Polyomavirus in Source-Separated Urine. |
| 29378882 | 10.1007/978-1-60327-164-6_12 | 10.1128/JB.00738-17 | Bacteriophages of the Urinary Microbiome. |
| 29381715 | 10.1371/journal.pone.0166883 | 10.1371/journal.pone.0191834 | Enterohemorrhagic Escherichia coli O157 subclade 8b strains in Chiba Prefecture, |
| 29391057 | 10.4049/jimmunol.0800224 | 10.1186/s40168-018-0410-y | A human gut phage catalog correlates the gut phageome with type 2 diabetes. |
| 29402927 | 10.1111/j.1365-2907.1985.tb00383.x | 10.1038/s41598-017-18667-2 | Salmonella Enteritidis ST183: emerging and endemic biotypes affecting western Eu |
| 29408864 | 10.1038/nprot.2010.5 | 10.1371/journal.pone.0192507 | In vitro characterization of PlyE146, a novel phage lysin that targets Gram-nega |
| 29410443 | 10.1007/978-1-60327-164-6_15 | 10.1038/s41598-018-20847-7 | Evolution of the Quorum network and the mobilome (plasmids and bacteriophages) i |
| 29414776 | 10.1016/j.micinf.2004.12.014 | 10.1074/jbc.RA117.000599 | Identification of a staphylococcal complement inhibitor with broad host specific |
| 29414851 | 10.1016/j.jsb.2014.02.016 | 10.3390/v10020067 | Breaking Symmetry in Viral Icosahedral Capsids as Seen through the Lenses of X-r |
| 29415431 | 10.15252/embr.201643250 | 10.3390/v10020064 | The Magistral Phage. |
| 29416528 | 10.1128/JB.00157-09 | 10.3389/fmicb.2018.00030 | Substrate Binding Protein DppA1 of ABC Transporter DppBCDF Increases Biofilm For |
| 29420566 | 10.18632/oncotarget.2121 | 10.1371/journal.pone.0191872 | A novel monoclonal antibody targeting carboxymethyllysine, an advanced glycation |
| 29420662 | 10.1158/0008-5472.CAN-16-0180 | 10.1371/journal.pone.0192194 | Generation of high-affinity, internalizing anti-FGFR2 single-chain variable anti |
| 29433534 | 10.1126/science.279.5355.1344 | 10.1186/s13075-017-1508-5 | Identification of a novel autoantibody against self-vimentin specific in seconda |
| 29434246 | 10.1038/nmeth1109-786 | 10.1038/s41598-018-21021-9 | High throughput protease profiling comprehensively defines active site specifici |
| 29435721 | 10.1016/S0958-1669(98)80017-7 | 10.1007/s00726-018-2539-1 | Selection and identification of novel peptides specifically targeting human cerv |
| 29437962 | 10.1016/j.jsb.2006.06.010 | 10.1128/JVI.02117-17 | Shigella Phages Isolated during a Dysentery Outbreak Reveal Uncommon Structures  |
| 29438273 | 10.1038/nm894 | 10.3390/toxins10020080 | Novel Phage Display-Derived Anti-Abrin Antibodies Confer Post-Exposure Protectio |
| 29439039 | 10.1093/nar/29.12.2607 | 10.1128/genomeA.01395-17 | Complete Genome Sequence of the Myoviral Bacteriophage YS35, Which Causes the Ly |
| 29442169 | 10.1038/srep29344 | 10.1007/s00253-018-8811-1 | Applications of bacteriophages versus phage enzymes to combat and cure bacterial |
| 29447223 | 10.1371/journal.ppat.1003057 | 10.1371/journal.pone.0192878 | Virome and bacteriome characterization of children with pneumonia and asthma in  |
| 29451376 | 10.1007/s11095014-1617-7 | *(none)* | [Phage therapy, an alternative to antibiotic therapy?)]. |
| 29463260 | 10.1124/dmd.30.7.757 | 10.1186/s12951-018-0345-2 | Multifunctionalized biocatalytic P22 nanoreactor for combinatory treatment of ER |
| 29467315 | 10.1177/002215540104900507 | 10.1128/JVI.02170-17 | Plasmid Partitioning by Human Tumor Viruses. |
| 29467338 | 10.1002/art.30424 | 10.1172/jci.insight.97805 | TCR-mimic bispecific antibodies targeting LMP2A show potent activity against EBV |
| 29472918 | 10.1016/j.jmb.2014.09.020 | 10.3389/fimmu.2018.00118 | Next-Generation Sequencing of Antibody Display Repertoires. |
| 29485998 | 10.1093/nar/gku531 | 10.1371/journal.pone.0191052 | Identification and characterization of highly versatile peptide-vectors that bin |
| 29495568 | 10.1371/journal.pone.0107307 | 10.3390/v10030103 | Study of the Interactions Between Bacteriophage phiIPLA-RODI and Four Chemical D |
| 29497090 | 10.1016/j.ejpb.2014.05.016 | 10.1038/s41598-018-21910-z | Application of Bld-1-Embedded Elastin-Like Polypeptides in Tumor Targeting. |
| 29503640 | 10.1016/0042-6822(71)90147-4 | 10.3389/fmicb.2018.00247 | A Pilin Region Affecting Host Range of the Pseudomonas aeruginosa RNA Phage, PP7 |
| 29509721 | 10.1126/science.1243457 | 10.3390/v10030113 | Deciphering the Human Virome with Single-Virus Genomics and Metagenomics. |
| 29512652 | 10.1101/gr.849004 | 10.1038/nature26155 | Evolved Cas9 variants with broad PAM compatibility and high DNA specificity. |
| 29515197 | 10.4056/sigs.531120 | 10.1038/s41598-018-22526-z | Mycobacterium ahvazicum sp. nov., the nineteenth species of the Mycobacterium si |
| 29517960 | 10.1080/21597081.2015.1088124 | 10.1080/19490976.2018.1447291 | A bacteriophage cocktail targeting Escherichia coli reduces E. coli in simulated |
| 29521625 | 10.1186/gb-2013-14-4-r40 | 10.7554/eLife.32035 | CRISPR-based herd immunity can limit phage epidemics in bacterial populations. |
| 29523751 | 10.1073/pnas.1514285112 | 10.1042/CS20171330 | Does the microbiome and virome contribute to myalgic encephalomyelitis/chronic f |
| 29545792 | 10.1073/pnas.1120059109 | 10.3389/fimmu.2018.00329 | Coupling of Single Molecule, Long Read Sequencing with IMGT/HighV-QUEST Analysis |
| 29549634 | 10.1038/nature16057 | 10.1007/978-3-319-72077-7_3 | Naïve Human Antibody Libraries for Infectious Diseases. |
| 29549637 | 10.1128/IAI.74.1.362-369.2006 | 10.1007/978-3-319-72077-7_6 | Monoclonal Antibodies and Antibody Like Fragments Derived from Immunised Phage D |
| 29555626 | 10.1111/2049-632X.12184 | 10.1128/AAC.02573-17 | Design of a Broad-Range Bacteriophage Cocktail That Reduces Pseudomonas aerugino |
| 29555908 | 10.1074/jbc.272.17.11057 | 10.1038/s41598-018-22744-5 | High yield bacterial expression, purification and characterisation of bioactive  |
| 29558962 | 10.1074/jbc.272.25.16010 | 10.1186/s12985-018-0955-1 | Engineering T7 bacteriophage as a potential DNA vaccine targeting delivery vecto |
| 29563204 | 10.15585/mmwr.mm6502a3 | 10.1128/JCM.00225-18 | Frequency of Instrument, Environment, and Laboratory Technologist Contamination  |
| 29568066 | 10.1093/nar/gki088 | 10.1038/s41426-018-0031-3 | Human transbodies that interfere with the functions of Ebola virus VP35 protein  |
| 29572482 | 10.1099/jmm.0.043687-0 | 10.1038/s41598-018-23418-y | Bacteriophages are more virulent to bacteria with human cells than they are in b |
| 29577680 | 10.1007/s10911-011-9236-y | 10.1002/mbo3.623 | Streptococcus dysgalactiae subsp. dysgalactiae isolated from milk of the bovine  |
| 29581113 | 10.1371/journal.ppat.1005500 | 10.1128/AAC.02212-17 | Chemotherapy with Phage Lysins Reduces Pneumococcal Colonization of the Respirat |
| 29583113 | 10.1017/S0950268814000260 | 10.1099/mgen.0.000170 | Whole-genome sequencing revealed concurrent outbreaks of shigellosis in the Engl |
| 29588404 | 10.1093/bioinformatics/bti770 | 10.1128/mBio.00467-18 | The Typhoid Toxin Produced by the Nontyphoidal Salmonella enterica Serotype Javi |
| 29593241 | 10.1016/S0022-5320(73)80038-3 | 10.1038/s41598-018-23708-5 | Identification and DNA annotation of a plasmid isolated from Chromobacterium vio |
| 29594068 | 10.1099/jmm.0.05245-0 | 10.3389/fcimb.2018.00075 | Construction of a New Phage Integration Vector pFIV-Val for Use in Different Fra |
| 29596346 | 10.1111/mec.14542 | 10.3390/v10040158 | 1st German Phage Symposium-Conference Report. |
| 29601536 | 10.1371/journal.pone.0000799 | 10.3390/v10040163 | In Vitro Characteristics of Phages to Guide 'Real Life' Phage Therapy Suitabilit |
| 29602308 | 10.3390/biomedicines4020011 | 10.1186/s12951-018-0362-1 | Gold nanoparticles stabilize peptide-drug-conjugates for sustained targeted drug |
| 29614013 | 10.1371/journal.pone.0068797 | 10.3390/v10040172 | Selection of Potential Therapeutic Bacteriophages that Lyse a CTX-M-15 Extended  |
| 29614052 | 10.1128/JB.00831-06 | 10.3390/v10040174 | Genomic Characterization of Sixteen Yersinia enterocolitica-Infecting Podoviruse |
| 29615108 | 10.1371/journal.pone.0044328 | 10.1186/s40168-018-0452-1 | Phages infecting Faecalibacterium prausnitzii belong to novel viral genera that  |
| 29615700 | 10.1006/bbrc.1996.0122 | 10.1038/s41598-018-23796-3 | Affinity maturation of humanized anti-epidermal growth factor receptor antibody  |
| 29617332 | 10.3389/fmicb.2017.00467 | 10.3390/v10040176 | Rapid Identification of Intact Staphylococcal Bacteriophages Using Matrix-Assist |
| 29620505 | 10.1002/wrna.1110 | 10.1099/jmm.0.000728 | Influence of RNase E deficiency on the production of stx2-bearing phages and Shi |
| 29621149 | 10.1016/S1473-3099(04)01127-2 | 10.3390/v10040177 | Criteria for Selecting Suitable Infectious Diseases for Phage Therapy. |
| 29621199 | 10.1128/JVI.01347-14 | 10.3390/v10040178 | Expert Opinion on Three Phage Therapy Related Topics: Bacterial Phage Resistance |
| 29622628 | 10.1016/j.jsb.2012.09.006 | 10.1126/science.aao7298 | Structure of the herpes simplex virus 1 capsid with associated tegument protein  |
| 29631623 | 10.1186/s40168-017-0237-y | 10.1186/s40168-018-0446-z | Reproducible protocols for metagenomic analysis of human faecal phageomes. |
| 29642449 | 10.1186/s12941-015-0106-0 | 10.3390/v10040182 | Characterization of a New Staphylococcus aureus Kayvirus Harboring a Lysin Activ |
| 29642590 | 10.1038/s41598-017-03996-z | 10.3390/v10040188 | Characterizing Phage Genomes for Therapeutic Applications. |
| 29643197 | 10.2807/ese.15.05.19477-en | 10.1128/JCM.00119-18 | Whole-Genome Sequencing of Recent Listeria monocytogenes Isolates from Germany R |
| 29652924 | 10.1074/jbc.M110356200 | 10.1371/journal.pone.0195077 | Extended cleavage specificity of human neutrophil cathepsin G: A low activity pr |
| 29658818 | 10.1002/pmic.201200303 | 10.1080/19420862.2018.1463945 | A long non-coding SINEUP RNA boosts semi-stable production of fully human monocl |
| 29668682 | 10.1038/nmeth.3176 | 10.1371/journal.pcbi.1006099 | Biogeography and environmental conditions shape bacteriophage-bacteria networks  |
| 29670863 | 10.1136/gutjnl-2017-313952 | 10.3389/fcimb.2018.00104 | Commentary: Bacteriophage transfer during faecal microbiota transplantation in C |
| 29671403 | 10.1002/ajmg.a.36740 | 10.1186/s12918-018-0531-8 | KDiamend: a package for detecting key drivers in a molecular ecological network  |
| 29671810 | 10.4161/21597081.2014.979662 | 10.3390/v10040205 | Bacteriophage Applications for Food Production and Processing. |
| 29677137 | 10.1126/science.352.6293.1506 | 10.3390/v10040209 | Phages Make for Jolly Good Stories. |
| 29693561 | 10.4315/0362-028X.JFP-17-098 | 10.3390/v10050218 | Framing the Future with Bacteriophages in Agriculture. |
| 29708991 | 10.1128/JCM.02262-12 | 10.1371/journal.pone.0196490 | DNA microarray-based assessment of virulence potential of Shiga toxin gene-carry |
| 29718957 | 10.1002/sim.4780090710 | 10.1371/journal.pone.0196271 | Sulfamethoxazole - Trimethoprim represses csgD but maintains virulence genes at  |
| 29720567 | 10.1093/protein/gzu032 | 10.1172/jci.insight.98305 | Selection of phage-displayed accessible recombinant targeted antibodies (SPARTA) |
| 29723982 | 10.1038/nprot.2014.037 | 10.3390/ijms19051334 | ScFvs as Allosteric Inhibitors of VEGFR-2: Novel Tools to Harness VEGF Signaling |
| 29735560 | 10.1074/jbc.M112.395962 | 10.1128/AAC.00385-18 | The Novel Phage-Derived Antimicrobial Agent HY-133 Is Active against Livestock-A |
| 29735891 | 10.1371/journal.pone.0172790 | 10.3390/v10050245 | Transposition Behavior Revealed by High-Resolution Description of Pseudomonas Ae |
| 29736607 | 10.1097/MCG.0b013e318266f6cf | 10.1007/s00018-018-2827-7 | Engineering microbes for targeted strikes against human pathogens. |
| 29739319 | 10.1128/JB.186.14.4486-4491.2004 | 10.1186/s12866-018-1182-z | Characterization of biofilm-forming capacity and resistance to sanitizers of a r |
| 29740542 | 10.1002/bies.201600262 | 10.3389/fcimb.2018.00121 | The Francisella Type VI Secretion System. |
| 29746832 | 10.1128/microbiolspec.EHEC-0028-2014. | 10.1016/j.chom.2018.04.007 | Bacteriophage Transcription Factor Cro Regulates Virulence Gene Expression in En |
| 29748239 | 10.1126/science.aaq0180 | 10.1042/BSR20170788 | Shooting the messenger: RNA-targetting CRISPR-Cas systems. |
| 29748556 | 10.1186/1471-2180-10-131 | 10.1038/s41467-018-04232-6 | Regulatory protein SrpA controls phage infection and core cellular processes in  |
| 29755481 | 10.1126/science.358.6366.982 | 10.3389/fimmu.2018.00941 | "Phage Transplantation in Allotransplantation": Possible Treatment in Graft-Vers |
| 29765367 | 10.1186/1471-2164-13-331 | 10.3389/fmicb.2018.00856 | Detection of Bacteriophage Particles Containing Antibiotic Resistance Genes in t |
| 29770130 | 10.1002/bit.24630 | 10.3389/fmicb.2018.00875 | Bacteriophage Infectivity Against Pseudomonas aeruginosa in Saline Conditions. |
| 29772002 | 10.1016/j.bbamcr.2014.03.018 | 10.1371/journal.ppat.1006971 | Lessons from bacteriophages part 1: Deriving utility from protein structure, fun |
| 29772006 | 10.1371/journal.pgen.1006838 | 10.1371/journal.ppat.1006970 | Lessons from bacteriophages part 2: A saga of scientific breakthroughs and prosp |
| 29776929 | 10.1186/1465-9921-7-98 | 10.1128/AEM.00886-18 | Antibacterial Effects of Phage Lysin LysGH15 on Planktonic Cells and Biofilms of |
| 29780361 | 10.1586/14787210.2.4.611 | 10.3389/fmicb.2018.00775 | Challenges and Promises for Planning Future Clinical Research Into Bacteriophage |
| 29792401 | 10.1038/nmeth1003 | 10.7554/eLife.34317 | Synthetic single domain antibodies for the conformational trapping of membrane p |
| 29802323 | 10.1371/journal.ppat.1000958 | 10.1038/s41598-018-26516-z | The antiviral protein Viperin suppresses T7 promoter dependent RNA synthesis-pos |
| 29843391 | 10.3389/fmed.2018.00146 | 10.3390/v10060288 | Phage Therapy: What Have We Learned? |
| 29844267 | 10.1111/j.1365-2591.2007.01211.x | 10.3390/v10060290 | Effects of a Chimeric Lysin against Planktonic and Sessile Enterococcus faecalis |
| 29844287 | 10.7554/eLife.13152 | 10.3390/v10060292 | Phage-Derived Peptidoglycan Degrading Enzymes: Challenges and Future Prospects f |
| 29849110 | 10.1371/journal.pcbi.1000191 | 10.1038/s41598-018-26683-z | Identification of a peptide for folate receptor alpha by phage display and its t |
| 29854845 | 10.1371/journal.ppat.1003150 | 10.1155/2018/7251793 | Three Types of Broadly Reacting Antibodies against Influenza B Viruses Induced b |
| 29855618 | 10.1007/s00284-012-0284-3 | 10.1038/s41598-018-26749-y | Targeted Delivery of Cell Penetrating Peptide Virus-like Nanoparticles to Skin C |
| 29856874 | 10.1016/j.dnarep.2015.02.001 | 10.1371/journal.pone.0198480 | Variable termination sites of DNA polymerases encountering a DNA-protein cross-l |
| 29857552 | 10.1073/pnas.0403302101 | 10.3390/v10060297 | Burkholderia cenocepacia Prophages-Prevalence, Chromosome Location and Major Gen |
| 29857590 | 10.3390/v10040174 | 10.3390/v10060299 | Analysis of 19 Highly Conserved Vibrio cholerae Bacteriophages Isolated from Env |
| 29875339 | 10.1128/AAC.02526-12 | 10.3390/v10060310 | Development of Phage Lysins as Novel Therapeutics: A Historical Perspective. |
| 29879998 | 10.1086/662677 | 10.1186/s12976-018-0079-8 | Outside-host phage therapy as a biological control against environmental infecti |
| 29880747 | 10.1006/jmbi.1998.1860 | 10.3390/v10060311 | Landscape Phage: Evolution from Phage Display to Nanobiotechnology. |
| 29882754 | 10.4161/21597073.2014.961869 | 10.3390/v10060307 | Nanomedicine and Phage Capsids. |
| 29889019 | 10.1007/s705-002-8299-4 | 10.1099/jgv.0.001097 | Detecting viral genomes in the female urinary microbiome. |
| 29890762 | 10.1016/j.toxicon.2018.03.004 | 10.3390/toxins10060236 | Basics of Antibody Phage Display Technology. |
| 29895791 | 10.1016/j.tim.2012.11.003 | 10.3390/v10060323 | Phage Therapy Faces Evolutionary Challenges. |
| 29895866 | 10.2967/jnumed.115.162339 | 10.1038/s41598-018-27355-8 | Development of a radionuclide-labeled monoclonal anti-CD55 antibody with therano |
| 29909042 | 10.1126/science.aar4120 | 10.1016/j.tim.2018.05.009 | Close Encounters of Three Kinds: Bacteriophages, Commensal Bacteria, and Host Im |
| 29910791 | 10.1111/j.1752-4571.2011.00236.x | 10.3389/fmicb.2018.01170 | Adaptation of Pseudomonas aeruginosa to Phage PaP1 Predation via O-Antigen Polym |
| 29913091 | 10.1038/nature08480 | 10.1080/19490976.2018.1474322 | "I will survive": A tale of bacteriophage-bacteria coevolution in the gut. |
| 29914064 | 10.1016/j.chom.2017.06.018 | 10.3390/v10060327 | The Diversity of Bacterial Lifestyles Hampers Bacteriophage Tenacity. |
| 29915075 | 10.1146/annurev-biochem-062917-012550 | 10.1073/pnas.1806718115 | Antibody selection using clonal cocultivation of Escherichia coli and eukaryotic |
| 29915115 | 10.1038/srep34067 | 10.1128/AEM.01263-18 | A Linear Plasmid-Like Prophage of Actinomyces odontolyticus Promotes Biofilm Ass |
| 29925793 | 10.1038/srep26717 | 10.3390/v10060338 | Identification and Characterization of Type IV Pili as the Cellular Receptor of  |
| 29927113 | 10.1002/0471140864.ps2809s79 | 10.1002/cpch.39 | Generating FN3-Based Affinity Reagents Through Phage Display. |
| 29933614 | 10.1007/s00284-016-1166-x | 10.3390/ijms19071831 | Relating Phage Genomes to Helicobacter pylori Population Structure: General Step |
| 29939993 | 10.1126/science.1138140 | 10.1371/journal.pntd.0006579 | Genetic diversity and spatial-temporal distribution of Yersinia pestis in Qingha |
| 29943298 | 10.1016/j.chom.2016.04.013 | 10.1007/978-981-13-0502-3_8 | Therapeutic Antibody Discovery in Infectious Diseases Using Single-Cell Analysis |
| 29950382 | 10.1016/j.jinf.2016.08.010 | 10.1128/mSphereDirect.00312-18 | Transcriptome Analysis of Neisseria gonorrhoeae during Natural Infection Reveals |
| 29954053 | 10.2217/fmb.13.47 | 10.3390/v10070345 | Delivering Phage Products to Combat Antibiotic Resistance in Developing Countrie |
| 29954402 | 10.1158/1940-6207.CAPR-10-0328 | 10.1186/s12967-018-1546-z | Identification of anti-SF3B1 autoantibody as a diagnostic marker in patients wit |
| 29955037 | 10.1261/rna.7255805 | 10.1038/s41467-018-04729-0 | Global pairwise RNA interaction landscapes reveal core features of protein recog |
| 29963501 | 10.1089/wound.2012.0381 | 10.3389/fcimb.2018.00196 | Development of a High-Throughput ex-Vivo Burn Wound Model Using Porcine Skin, an |
| 29966329 | 10.1159/000473872 | 10.3390/v10070351 | Resistance Development to Bacteriophages Occurring during Bacteriophage Therapy. |
| 29976589 | 10.1016/j.vetmic.2015.11.013 | 10.1128/JCM.00140-18 | Prevalence and Genomic Structure of Bacteriophage phi3 in Human-Derived Livestoc |
| 29980598 | 10.1107/S0021889892009944 | 10.1074/jbc.RA117.000262 | Identification of two distinct peptide-binding pockets in the SH3 domain of huma |
| 29985410 | 10.1021/ja808255d | 10.1038/s41598-018-28493-9 | Optimization of a MT1-MMP-targeting Peptide and Its Application in Near-infrared |
| 29990379 | 10.1016/j.jconrel.2009.06.008 | 10.1371/journal.pone.0200444 | CD177-mediated nanoparticle targeting of human and mouse neutrophils. |
| 29992156 | 10.1097/01.mbc.0000198990.16598.85 | 10.1155/2018/6232091 | The Use of Phage Display and Yeast Based Expression System for the Development o |
| 29993044 | 10.1016/S0022-2836(05)80360-2 | 10.1038/s41598-018-28844-6 | Changing of the Genomic Pattern of Salmonella Enteritidis Strains Isolated in Br |
| 29995563 | 10.1080/19420862.2018.1463945 | 10.1080/19420862.2018.1496772 | Massive parallel screening of phage libraries for the generation of repertoires  |
| 30005571 | 10.1183/09031936.00158414 | 10.1021/acs.jproteome.8b00414 | Affimers as an Alternative to Antibodies in an Affinity LC-MS Assay for Quantifi |
| 30029479 | 10.1073/pnas.1121072109 | 10.3390/v10070375 | Novel T7 Phage Display Library Detects Classifiers for Active Mycobacterium Tube |
| 30038902 | 10.1084/jem.20051681 | 10.3389/fcimb.2018.00235 | The Staphylococcus aureus Extracellular Adherence Protein Eap Is a DNA Binding P |
| 30039318 | 10.1038/nmicrobiol.2015.24 | 10.1007/s00705-018-3938-z | Virus classification - where do you draw the line? |
| 30044093 | 10.1016/j.semcdb.2018.03.017 | 10.1021/acs.langmuir.8b01812 | Assessing Protein Dynamics on Low-Complexity Single-Stranded DNA Curtains. |
| 30046034 | 10.1038/nature16526 | 10.1038/s41467-018-05092-w | Widespread anti-CRISPR proteins in virulent bacteriophages inhibit a range of Ca |
| 30051426 | 10.3791/3064 | 10.1007/978-1-4939-8661-3_7 | Exploiting Phage Display for Development of Novel Cellular Targeting Strategies. |
| 30065291 | 10.1093/nar/gkw992 | 10.1038/s41598-018-29272-2 | Investigation of recombination-intense viral groups and their genes in the Earth |
| 30065309 | 10.1007/BF00330613 | 10.1038/s41396-018-0244-4 | Acquisition of MACPF domain-encoding genes is the main contributor to LPS glycan |
| 30068548 | 10.1016/S0076-6879(06)08001-3 | 10.1074/jbc.RA118.004676 | Cytotoxic and mutagenic properties of O6-alkyl-2'-deoxyguanosine lesions in Esch |
| 30075254 | 10.1093/molbev/msy027 | 10.1016/j.meegid.2018.07.038 | Distribution and characterization of Shiga toxin converting temperate phages car |
| 30087270 | 10.1111/apt.14201 | 10.3390/ijerph15081679 | Rebuilding the Gut Microbiota Ecosystem. |
| 30087425 | 10.1080/17425247.2016.1220364 | 10.1038/s41598-018-30031-6 | Active Transport of Peptides Across the Intact Human Tympanic Membrane. |
| 30092023 | 10.1194/jlr.M073171 | 10.1371/journal.pone.0200298 | The antigenicity and cholesteroid nature of mycolic acids determined by recombin |
| 30096336 | 10.2217/fmb-2016-0156 | 10.1016/j.addr.2018.08.001 | Phage therapy for respiratory infections. |
| 30101693 | 10.3389/fgene.2017.00072 | 10.1080/21505594.2018.1509666 | An ancient family of mobile genomic islands introducing cephalosporinase and car |
| 30108574 | 10.1128/JB.01655-07 | 10.3389/fmicb.2018.01725 | Chestnut Honey and Bacteriophage Application to Control Pseudomonas aeruginosa a |
| 30110337 | 10.1073/pnas.0606179103 | 10.1371/journal.pone.0200955 | Herpes ICP8 protein stimulates homologous recombination in human cells. |
| 30110933 | 10.1111/j.1365-2958.2008.06311.x | 10.3390/v10080427 | Structure and Analysis of R1 and R2 Pyocin Receptor-Binding Fibers. |
| 30115980 | 10.1073/pnas.1420588112 | 10.1038/s41598-018-30705-1 | Novel phages of healthy skin metaviromes from South Africa. |
| 30126456 | 10.1073/pnas.1305956110 | 10.1186/s40168-018-0527-z | Tracing mother-infant transmission of bacteriophages by means of a novel analyti |
| 30127773 | 10.3201/eid1406.071447 | 10.3389/fmicb.2018.01750 | Crystal Structures of R-Type Bacteriocin Sheath and Tube Proteins CD1363 and CD1 |
| 30127777 | 10.1128/genomeA.00449-14 | 10.3389/fmicb.2018.01778 | Antibacterial Activity of a Lytic Enzyme Encoded by Pseudomonas aeruginosa Doubl |
| 30131795 | 10.1016/S0749-0690(18)30446-4 | 10.3389/fmicb.2018.01832 | Adapted Bacteriophages for Treating Urinary Tract Infections. |
| 30134556 | 10.1021/ja051306e | 10.3390/ijms19092470 | Specific Antibody Fragment Ligand Traps Blocking FGF1 Activity. |
| 30135446 | 10.1038/sj.mt.6300245 | 10.1038/s41598-018-30790-2 | A platform for discovery of functional cell-penetrating peptides for efficient m |
| 30137359 | 10.5524/100470 | 10.1093/gigascience/giy100 | Establishment of a Macaca fascicularis gut microbiome gene catalog and compariso |
| 30142227 | 10.1099/vir.0.80131-0 | 10.1371/journal.ppat.1007262 | Protective antigenic sites in respiratory syncytial virus G attachment protein o |
| 30143740 | 10.1093/molbev/msp259 | 10.1038/s41598-018-31181-3 | Characterization and induction of prophages in human gut-associated Bifidobacter |
| 30150232 | 10.1128/JB.00943-09 | 10.1128/JB.00189-18 | Phage Morons Play an Important Role in Pseudomonas aeruginosa Phenotypes. |
| 30170539 | 10.1073/pnas.0903585106 | 10.1186/s12864-018-5045-7 | Attack of the clones: whole genome-based characterization of two closely related |
| 30183492 | 10.3791/186 | 10.1080/19420862.2018.1515565 | A synthetic anti-Frizzled antibody engineered for broadened specificity exhibits |
| 30185663 | 10.1016/j.canlet.2016.06.017 | 10.1172/jci.insight.121497 | Targeting CD46 for both adenocarcinoma and neuroendocrine prostate cancer. |
| 30205462 | 10.1038/s41564-017-0053-y | 10.3390/v10090479 | Insights into the Human Virome Using CRISPR Spacers from Microbiomes. |
| 30211956 | 10.1099/mgen.0.000142. | 10.1111/1348-0421.12648 | Comparative analyses of CTX prophage region of Vibrio cholerae seventh pandemic  |
| 30217840 | 10.1023/A:1011904921318 | 10.1128/AEM.01809-18 | Transfer of Enteric Viruses Adenovirus and Coxsackievirus and Bacteriophage MS2  |
| 30232199 | 10.1111/1471-0528.15299 | 10.1101/gr.236000.118 | Metagenomic analysis with strain-level resolution reveals fine-scale variation i |
| 30248089 | 10.1128/JB.01184-12 | 10.1371/journal.pbio.2006738 | Evolutionary emergence of infectious diseases in heterogeneous host populations. |
| 30249752 | 10.1371/journal.pone.0199250 | 10.1042/BSR20181113 | Biopanning of allergens from wasp sting patients. |
| 30262856 | 10.3324/haematol.2013.086207 | 10.1038/s41598-018-32832-1 | Identification of Peptide Mimotope Ligands for Natalizumab. |
| 30264928 | 10.1128/mBio.00246-11 | 10.1111/mmi.14141 | Two pKM101-encoded proteins, the pilus-tip protein TraC and Pep, assemble on the |
| 30281587 | 10.18637/jss.v082.i13 | 10.1371/journal.pbio.2006057 | Cross-resistance is modular in bacteria-phage interactions. |
| 30282659 | 10.1038/nature11233 | 10.1098/rsob.180104 | Intracellular RNA-tracking methods. |
| 30291704 | 10.1038/s41598-017-16303-7 | 10.1128/microbiolspec.GPP3-0026-2018 | Mycobacteriophages. |
| 30302018 | 10.1186/s13100-017-0095-y | 10.1038/s41426-018-0169-z | The disparate effects of bacteriophages on antibiotic-resistant bacteria. |
| 30302027 | 10.1016/j.yjmcc.2013.10.015 | 10.1038/s41598-018-33382-2 | An innovative flow cytometry method to screen human scFv-phages selected by in v |
| 30308048 | 10.1128/AEM.00767-14 | 10.1371/journal.pone.0205728 | Comparative analysis of different preservation techniques for the storage of Sta |
| 30308933 | 10.1111/bph.14106 | 10.3390/v10100552 | Potential Application of Bacteriophages in Enrichment Culture for Improved Prena |
| 30309013 | 10.1016/j.vaccine.2017.09.025 | 10.3390/ijerph15102211 | A Metagenomic Approach to Evaluating Surface Water Quality in Haiti. |
| 30323035 | 10.1128/AAC.01288-13 | 10.1128/AAC.01110-18 | New Treatment Options against Carbapenem-Resistant Acinetobacter baumannii Infec |
| 30344303 | 10.1016/j.anai.2011.09.014 | 10.3390/medicina54050072 | Lower Airway Virology in Health and Disease-From Invaders to Symbionts. |
| 30344632 | 10.1111/j.1752-4571.2011.00236.x | 10.1111/eva.12653 | Rapid evolution of generalized resistance mechanisms can constrain the efficacy  |
| 30352623 | 10.1109/MCSE.2014.80 | 10.1186/s40168-018-0573-6 | A diversity-generating retroelement encoded by a globally ubiquitous Bacteroides |
| 30355958 | 10.1016/j.molcel.2008.05.013 | 10.3390/ijms19113305 | A Recombinant Affinity Reagent Specific for a Phosphoepitope of Akt1. |
| 30356736 | 10.1098/rstb.2017.0359 | 10.3389/fimmu.2018.02240 | Immunological Tolerance and Function: Associations Between Intestinal Bacteria,  |
| 30359456 | 10.1128/IAI.00648-16 | 10.1371/journal.ppat.1007310 | Bacteriophages shift the focus of the mammalian microbiota. |
| 30371236 | 10.1161/JAHA.115.002856 | 10.1161/JAHA.118.008737 | Engineered Exosomes With Ischemic Myocardium-Targeting Peptide for Targeted Ther |
| 30373771 | 10.1007/978-1-62703-646-7_17 | 10.1074/jbc.RA118.004469 | Discovery of peptide ligands targeting a specific ubiquitin-like domain-binding  |
| 30374457 | 10.1093/nar/30.7.1575 | 10.1128/mSystems.00075-18 | Metapopulation Structure of CRISPR-Cas Immunity in Pseudomonas aeruginosa and It |
| 30384416 | 10.3389/fmicb.2015.01313 | 10.3390/v10110595 | Comparative Genomics and Characterization of the Late Promoter pR' from Shiga To |
| 30395707 | 10.1073/pnas.71.9.3363 | 10.1021/acs.est.8b02191 | Biological Weighting Functions for Evaluating the Role of Sunlight-Induced Inact |
| 30397357 | 10.1080/STA-200066418 | 10.1038/s41591-018-0211-7 | Expanded skin virome in DOCK8-deficient patients. |
| 30406049 | 10.3389/fmicb.2018.00850 | 10.3389/fcimb.2018.00376 | Bacteriophage Therapy: Clinical Trials and Regulatory Hurdles. |
| 30410478 | 10.1007/s00705-018-3866-y | 10.3389/fmicb.2018.02561 | Characterization and Genomic Analyses of Pseudomonas aeruginosa Podovirus TC6: E |
| 30411529 | 10.1021/bi991611a | 10.1002/wnan.1545 | Physical, chemical, and synthetic virology: Reprogramming viruses as controllabl |
| 30413044 | 10.1186/s12967-014-0358-z | 10.3390/v10110617 | Effects of Staphylococcus aureus Bacteriophage K on Expression of Cytokines and  |
| 30417018 | 10.3389/fimmu.2017.01780 | 10.1155/2018/4089459 | Anti-ICOSL New Antigen Receptor Domains Inhibit T Cell Proliferation and Reduce  |
| 30421127 | 10.1016/j.bbrc.2009.08.059 | 10.1007/s11033-018-4467-2 | Development of drug-loaded protein nanoparticles displaying enzymatically-conjug |
| 30424942 | 10.1371/journal.pntd.0003776 | 10.1016/j.ijheh.2018.07.002 | A bioassay-based protocol for chemical neutralization of human faecal wastes tre |
| 30425154 | 10.1073/pnas.0503005102 | 10.1128/mBio.02184-18 | Temperature, by Controlling Growth Rate, Regulates CRISPR-Cas Activity in Pseudo |
| 30425253 | 10.1128/AEM.70.11.6887-6891.2004 | 10.1038/s41598-018-34918-2 | Mobilisation Mechanism of Pathogenicity Islands by Endogenous Phages in Staphylo |
| 30429469 | 10.1073/pnas.1605883113 | 10.1038/s41467-018-07225-7 | ΦCrAss001 represents the most abundant bacteriophage family in the human gut and |
| 30451861 | 10.1093/nar/gkw880 | 10.1038/s41467-018-07321-8 | Translation of non-standard codon nucleotides reveals minimal requirements for c |
| 30452949 | 10.1128/JB.00738-00717 | 10.1016/j.addr.2018.11.004 | Bacteriophage-based biomaterials for tissue regeneration. |
| 30457532 | 10.1099/jmm.0.062380-0 | 10.3201/eid2412.180409 | Highly Pathogenic Clone of Shiga Toxin-Producing Escherichia coli O157:H7, Engla |
| 30459201 | 10.1186/1471-2105-10-421 | 10.1128/mBio.02248-18 | Diagnostic Potential and Interactive Dynamics of the Colorectal Cancer Virome. |
| 30459750 | 10.1007/s00253-018-8811-1 | 10.3389/fimmu.2018.02252 | Phage Lysins for Fighting Bacterial Respiratory Infections: A New Generation of  |
| 30459762 | 10.1016/S0006-291X(67)80055-X | 10.3389/fimmu.2018.02387 | Extended Cleavage Specificity of Human Neutrophil Elastase, Human Proteinase 3,  |
| 30462638 | 10.1101/gr.849004 | 10.1371/journal.pgen.1007792 | Bacterial group II introns generate genetic diversity by circularization and tra |
| 30463964 | 10.1016/j.carres.2015.05.003 | 10.1128/JVI.01163-18 | Functional Analysis and Antivirulence Properties of a New Depolymerase from a My |
| 30509943 | 10.1128/AEM.03657-12 | 10.1128/AAC.01439-18 | Antibiotics Stimulate Formation of Vesicles in Staphylococcus aureus in both Pha |
| 30510202 | 10.1038/ncb2036 | 10.1038/s41598-018-35859-6 | Engineered K1F bacteriophages kill intracellular Escherichia coli K1 in human ep |
| 30513883 | 10.1038/nprot.2016.169 | 10.3390/toxins10120509 | Human Monoclonal scFvs that Neutralize Fribrinogenolytic Activity of Kaouthiagin |
| 30514786 | 10.1186/1758-907X-3-9 | 10.1128/mBio.02321-18 | Potent Cas9 Inhibition in Bacterial and Human Cells by AcrIIC4 and AcrIIC5 Anti- |
| 30516449 | 10.1074/jbc.M303164200 | 10.1080/19420862.2018.1538723 | Generation by phage display and characterization of drug-target complex-specific |
| 30518317 | 10.1093/nar/gkw290 | 10.1186/s12866-018-1336-z | USA300 Staphylococcus aureus persists on multiple body sites following an infect |
| 30518413 | 10.1021/acs.molpharmaceut.7b00985 | 10.1186/s13104-018-3955-8 | Isolation and characterization of camelid single-domain antibodies against HER2. |
| 30518855 | 10.1007/s002030100345 | 10.1038/s41586-018-0767-x | A chemical defence against phage infection. |
| 30521603 | 10.1101/gr.849004 | 10.1371/journal.pone.0207826 | Extended cleavage specificities of mast cell proteases 1 and 2 from golden hamst |
| 30526270 | 10.3389/fimmu.2018.01716 | 10.1080/19420862.2018.1550320 | Effective binding to protein antigens by antibodies from antibody libraries desi |
| 30526504 | 10.1128/IAI.00261-07 | 10.1186/s12879-018-3542-6 | Human monoclonal anti-protective antigen antibody for the low-dose post-exposure |
| 30526683 | 10.1186/1471-2105-11-119 | 10.1186/s40168-018-0598-x | Long-term colonisation with donor bacteriophages following successful faecal mic |
| 30533722 | 10.1093/nar/gkh152 | 10.1128/MRA.01034-18 | Draft Genome Sequence of Escherichia coli Phage CMSTMSU, Isolated from Shrimp Fa |
| 30541839 | 10.1073/pnas.0400444101 | 10.1128/JVI.01833-18 | Global Proteomic Profiling of Salmonella Infection by a Giant Phage. |
| 30546305 | 10.1128/IAI.00815-10 | 10.3389/fphar.2018.01330 | Use of a Primary Epithelial Cell Screening Tool to Investigate Phage Therapy in  |
| 30547858 | 10.4161/19420862.2014.985132 | 10.1128/microbiolspec.GPP3-0047-2018 | Nonconventional Therapeutics against Staphylococcus aureus. |
| 30551565 | 10.3390/toxins10100380 | 10.3390/toxins10120534 | Biosynthetic Oligoclonal Antivenom (BOA) for Snakebite and Next-Generation Treat |
| 30552174 | 10.1002/jor.22794 | 10.1136/annrheumdis-2018-214294 | Targeting early changes in the synovial microenvironment: a new class of immunom |
| 30555486 | 10.1038/ni.3858 | 10.3389/fimmu.2018.02822 | A Single-Domain Antibody Targeting Complement Component C5 Acts as a Selective I |
| 30558657 | 10.1093/nar/gkn176 | 10.1186/s13104-018-4010-5 | Whole-genome of Mexican-crAssphage isolated from the human gut microbiome. |
| 30558669 | 10.1159/000448733 | 10.1186/s40168-018-0611-4 | Signatures within the esophageal microbiome are associated with host genetics, a |
| 30559407 | 10.1038/nmeth.1923 | 10.1038/s41564-018-0321-5 | Genomic variation and strain-specific functional adaptation in the human gut mic |
| 30560894 | 10.1371/journal.pone.0099733 | 10.1038/s41598-018-35938-8 | HAI Peptide and Backbone Analogs-Validation and Enhancement of Biostability and  |
| 30563034 | 10.15252/embr.201643250 | 10.3390/v10120688 | A Wake-Up Call: We Need Phage Therapy Now. |
| 30567291 | 10.1128/AEM.02821-16 | 10.3390/v10120722 | "FAGOMA: Spanish Network of Bacteriophages and Transducer Elements"-V Meeting Re |
| 30569818 | 10.1038/nbt1126 | 10.1080/19420862.2018.1537580 | De novo generation of specific human IgGs by in vitro immunization using autolog |
| 30571788 | 10.1371/journal.pntd.0003031 | 10.1371/journal.pone.0209357 | Phenotypic and genomic analyses of bacteriophages targeting environmental and cl |
| 30585199 | 10.1007/s00262-006-0227-6 | 10.3390/v11010010 | Interactions between Bacteriophage, Bacteria, and the Mammalian Immune System. |
| 30586498 | 10.1371/journal.pone.0164097 | 10.1021/acsnano.8b06395 | Rapid Colorimetric Detection of Bacterial Species through the Capture of Gold Na |
| 30591706 | 10.1093/nar/16.22.10881 | 10.1038/s41598-018-35923-1 | Selection and Characterization of Anti-Dengue NS1 Single Domain Antibodies. |
| 30597868 | 10.1053/j.gastro.2016.11.010 | 10.3390/v11010018 | Clinical Indications and Compassionate Use of Phage Therapy: Personal Experience |
| 30621339 | 10.1002/cam4.35 | 10.3390/ijms20010183 | Bacteriocins and Bacteriophages: Therapeutic Weapons for Gastrointestinal Diseas |
| 30622259 | 10.1038/nmeth.3176 | 10.1038/s41467-018-07992-3 | Fecal pollution can explain antibiotic resistance gene abundances in anthropogen |
| 30622532 | 10.1002/hep.510280333 | 10.3389/fimmu.2018.03004 | Antibody Repertoire Analysis of Hepatitis C Virus Infections Identifies Immune S |
| 30626617 | 10.1038/nrmicro3096 | 10.1128/MMBR.00044-18 | Cross-Domain and Viral Interactions in the Microbiome. |
| 30628877 | 10.1111/j.1365-2958.2006.05249.x | 10.1099/jmm.0.000908 | Bacteriophage-associated genes responsible for the widely divergent phenotypes o |
| 30635442 | 10.1038/s41467-018-03028-y | 10.1074/jbc.H118.006803 | Putting phage to work in deubiquitinase ligand discovery. |
| 30643127 | 10.1016/j.stem.2016.01.022 | 10.1038/s41467-018-08158-x | Anti-CRISPR-mediated control of gene editing and synthetic circuits in eukaryoti |
| 30643154 | 10.1080/00031305.1998.10480550 | 10.1038/s41598-018-33804-1 | Development of a high sensitivity TaqMan-based PCR assay for the specific detect |
| 30648944 | 10.1128/CMR.00001-16 | 10.1099/mgen.0.000237 | Shared genome analyses of notable listeriosis outbreaks, highlighting the critic |
| 30650088 | 10.1128/CMR.00034-09 | 10.1371/journal.pone.0209390 | Adjunct phage treatment enhances the effectiveness of low antibiotic concentrati |
| 30651225 | 10.4161/bact.1.3.16591 | 10.1128/CMR.00066-18 | Phage Therapy in the Postantibiotic Era. |
| 30658491 | 10.1080/19420862.2015.1093266 | 10.3390/toxins11010053 | Toxin Neutralization Using Alternative Binding Proteins. |
| 30663541 | 10.1126/science.1246135 | 10.1080/19420862.2019.1571879 | ALTHEA Gold Libraries™: antibody libraries for therapeutic antibody discovery. |
| 30670422 | 10.1371/journal.ppat.1005257 | 10.1128/AAC.01834-18 | Early Detection of Emergent Extensively Drug-Resistant Tuberculosis by Flow Cyto |
| 30670427 | 10.1093/jac/dkw249 | 10.1128/AAC.02291-18 | The Antistaphylococcal Lysin, CF-301, Activates Key Host Factors in Human Blood  |
| 30670618 | 10.1016/j.chom.2016.02.010 | 10.1128/mBio.02626-18 | Going Viral: a Novel Role for Bacteriophage in Colorectal Cancer. |
| 30677033 | 10.1371/journal.pntd.0000228 | 10.1371/journal.pntd.0007131 | Discovery of Leptospira spp. seroreactive peptides using ORFeome phage display. |
| 30678377 | 10.1016/j.surg.2005.02.012 | 10.3390/v11020096 | The Preclinical and Clinical Progress of Bacteriophages and Their Lytic Enzymes: |
| 30691529 | 10.1101/gr.074492.107 | 10.1186/s40168-019-0626-5 | Choice of assembly software has a critical impact on virome characterisation. |
| 30692603 | 10.1016/j.bpj.2010.01.051 | 10.1038/s41598-018-37280-5 | Directed evolution of super-secreted variants from phage-displayed human Interle |
| 30692672 | 10.1093/bioinformatics/btw006 | 10.1038/s41564-018-0338-9 | Megaphages infect Prevotella and variants are widespread in gut microbiomes. |
| 30696740 | 10.1128/AEM.00141-08 | 10.1128/mBio.01828-18 | Competition in Biofilms between Cystic Fibrosis Isolates of Pseudomonas aerugino |
| 30705359 | 10.1186/1472-6750-4-21 | 10.1038/s41598-018-37685-2 | Identification and characterization of synthetic chondroitin-4-sulfate binding p |
| 30707748 | 10.1016/j.ttbdis.2018.03.030 | 10.1371/journal.ppat.1007375 | An anti-Gn glycoprotein antibody from a convalescent patient potently inhibits t |
| 30728389 | 10.1038/nprot.2007.514 | 10.1038/s41598-018-37636-x | Phage therapy against Pseudomonas aeruginosa infections in a cystic fibrosis zeb |
| 30733972 | 10.1111/fcp.12071 | 10.1155/2019/3017360 | A Novel Anti-EGFR mAb Ame55 with Lower Toxicity and Better Efficacy than Cetuxim |
| 30735524 | 10.18637/jss.v012.i06 | 10.1371/journal.pone.0211827 | A new approach to measure the resistance of fabric to liquid and viral penetrati |
| 30735956 | 10.1007/s11356-018-1881-x | 10.1016/j.watres.2018.12.058 | Occurrence of coliphage in raw wastewater and in ambient water: A meta-analysis. |
| 30736446 | 10.1128/IAI.70.10.5428-5437.2002 | 10.3390/ijms20030716 | In Vitro Activity of the Bacteriophage Endolysin HY-133 against Staphylococcus a |
| 30736742 | 10.1093/nar/gkr485 | 10.1186/s12864-018-5394-2 | Virulence factor landscape of a Staphylococcus aureus sequence type 45 strain, M |
| 30758724 | 10.1002/clen.201400235 | 10.1007/s12560-019-09369-1 | Critical Evaluation of CrAssphage as a Molecular Marker for Human-Derived Wastew |
| 30765740 | 10.1007/978-1-60327-164-6_14 | 10.1038/s41598-018-38318-4 | Fibrin glue as a local drug-delivery system for bacteriophage PA5. |
| 30778090 | 10.1016/j.tibtech.2006.03.003 | 10.1038/s41598-018-38371-z | Lambda bacteriophage nanoparticles displaying GP2, a HER2/neu derived peptide, i |
| 30779811 | 10.1016/j.virol.2009.11.032 | 10.1371/journal.ppat.1007572 | Identification of HIV gp41-specific antibodies that mediate killing of infected  |
| 30787460 | 10.1007/s00705-018-04136-2 | 10.1038/d41586-019-00599-8 | Classify viruses - the gain is worth the pain. |
| 30793400 | 10.1016/j.str.2019.01.002 | 10.1002/pro.3593 | Dimerization of a ubiquitin variant leads to high affinity interactions with a u |
| 30810520 | 10.1126/science.aao2136 | 10.1099/mgen.0.000256 | Wave 2 strains of atypical Vibrio cholerae El Tor caused the 2009-2011 cholera o |
| 30816246 | 10.1007/s10682-012-9594-y | 10.1038/s41598-019-39773-3 | Environmental structure drives resistance to phages and antibiotics during phage |
| 30824445 | 10.1099/jmm.0.060004-0 | 10.1128/AEM.02900-18 | Two Novel Bacteriophages Improve Survival in Galleria mellonella Infection and M |
| 30825301 | 10.1038/nbt.2942 | 10.1128/microbiolspec.PSIB-0009-2018 | Type VI Secretion Systems and the Gut Microbiota. |
| 30834237 | 10.1111/j.1752-4571.2011.00236.x | 10.3389/fcimb.2019.00022 | Fighting Pathogenic Bacteria on Two Fronts: Phages and Antibiotics as Combined S |
| 30840689 | 10.1155/2017/5482768 | 10.1371/journal.pone.0213184 | Swainsonine, an alpha-mannosidase inhibitor, may worsen cervical cancer progress |
| 30842211 | 10.1038/nmeth.1923 | 10.1136/gutjnl-2018-318131 | Gut mucosal virome alterations in ulcerative colitis. |
| 30848235 | 10.1128/mBio.00318-11 | 10.1128/microbiolspec.GPP3-0055-2018 | Enterococcal Genetics. |
| 30850705 | 10.1021/ci200227u | 10.1038/s41598-019-40562-1 | Rational Identification of a Colorectal Cancer Targeting Peptide through Phage D |
| 30850736 | 10.1016/j.cell.2015.02.011 | 10.1038/s41375-019-0434-8 | A fully human anti-IL-7Rα antibody promotes antitumor activity against T-cell ac |
| 30851297 | 10.1016/j.str.2019.01.002 | 10.1016/j.pharmthera.2019.03.003 | Emerging drug development technologies targeting ubiquitination for cancer thera |
| 30862096 | 10.2165/00003088-200342040-00002 | 10.3390/v11030241 | Directed in Vitro Evolution of Therapeutic Bacteriophages: The Appelmans Protoco |
| 30866714 | 10.1093/bioinformatics/btu616 | 10.1080/19490976.2019.1586037 | The success of fecal microbial transplantation in Clostridium difficile infectio |
| 30867296 | 10.1007/s00248-018-1228-7 | 10.1073/pnas.1900141116 | Genomic plasticity associated with antimicrobial resistance in Vibrio cholerae. |
| 30867462 | 10.1016/j.str.2011.09.022 | 10.1038/s41598-019-39732-y | B1.12: a novel peptide interacting with the extracellular loop of the EBV oncopr |
| 30884879 | 10.1371/journal.pone.0051017 | 10.3390/v11030265 | Processing Phage Therapy Requests in a Brussels Military Hospital: Lessons Ident |
| 30889807 | 10.3389/fmicb.2018.00247 | 10.3390/v11030268 | Phage-Derived Antibacterials: Harnessing the Simplicity, Plasticity, and Diversi |
| 30890181 | 10.1038/ismej.2016.89 | 10.1186/s40168-019-0657-y | Mining, analyzing, and integrating viral signals from metagenomic data. |
| 30894414 | 10.1093/bioinformatics/btn392 | 10.1074/jbc.RA118.006968 | A small mycobacteriophage-derived peptide and its improved isomer restrict mycob |
| 30897686 | 10.2337/db06-1491 | 10.3390/nu11030666 | PHAGE Study: Effects of Supplemental Bacteriophage Intake on Inflammation and Gu |
| 30900543 | 10.1001/archinte.163.4.402 | 10.1128/microbiolspec.GPP3-0057-2018 | Antibiotic Resistance and the MRSA Problem. |
| 30901901 | 10.1042/BCJ20170633 | 10.3390/v11030284 | Broad Bactericidal Activity of the Myoviridae Bacteriophage Lysins LysAm24, LysE |
| 30905286 | 10.1016/j.bbapap.2013.12.008 | 10.1098/rstb.2018.0384 | Genome-wide correlation analysis suggests different roles of CRISPR-Cas systems  |
| 30909579 | 10.1093/femsle/fnv225 | 10.3390/v11030295 | Towards Inhaled Phage Therapy in Western Europe. |
| 30923196 | 10.1038/ni1207 | 10.1126/science.aat9691 | Bacteriophage trigger antiviral immunity and prevent clearance of bacterial infe |
| 30934000 | 10.1186/1471-2164-9-539 | 10.1371/journal.pone.0214641 | Characterization of Listeria prophages in lysogenic isolates from foods and food |
| 30936157 | 10.1128/JB.00592-09 | 10.1128/IAI.00085-19 | Bacteriophage Resistance Alters Antibiotic-Mediated Intestinal Expansion of Ente |
| 30939832 | 10.3390/v9110315 | 10.3390/v11040318 | Characterization of Two Pseudomonas aeruginosa Viruses vB_PaeM_SCUT-S1 and vB_Pa |
| 30949157 | 10.3389/fmicb.2018.00011 | 10.3389/fmicb.2019.00572 | A Phage-Like Plasmid Carrying bla KPC-2 Gene in Carbapenem-Resistant Pseudomonas |
| 30952698 | 10.1016/j.jim.2004.11.016 | 10.1074/jbc.RA119.008315 | Novel MASP-2 inhibitors developed via directed evolution of human TFPI1 are pote |
| 30962344 | 10.1016/j.bbagen.2013.02.002 | 10.1128/AAC.00342-19 | Lysocins: Bioengineered Antimicrobials That Deliver Lysins across the Outer Memb |
| 30962356 | 10.1128/AEM.00136-13 | 10.1128/JB.00766-18 | ϕSa3mw Prophage as a Molecular Regulatory Switch of Staphylococcus aureus β-Toxi |
| 30975220 | 10.1016/0027-5107(92)90106-C | 10.1186/s13104-019-4251-y | Zero-valent iron sand filtration reduces concentrations of virus-like particles  |
| 30978194 | 10.1128/AAC.02243-12 | 10.1371/journal.pmed.1002780 | Lipoarabinomannan in sputum to detect bacterial load and treatment response in p |
| 30986237 | 10.1128/AAC.49.5.1857-1864.2005 | 10.1371/journal.pone.0215038 | Accessory genome of the multi-drug resistant ocular isolate of Pseudomonas aerug |
| 30986243 | 10.1371/journal.pcbi.1003537 | 10.1371/journal.pgen.1008114 | Distinct evolutionary dynamics of horizontal gene transfer in drug resistant and |
| 30988390 | 10.1038/srep26240 | 10.1038/s41598-019-42628-6 | Development of a Phage Display Panning Strategy Utilizing Crude Antigens: Isolat |
| 30988669 | 10.1038/srep15082 | 10.3389/fmicb.2019.00539 | Emerging Strategies to Combat ESKAPE Pathogens in the Era of Antimicrobial Resis |
| 30990839 | 10.1098/rspb.2013.2563 | 10.1371/journal.pone.0215456 | Investigation of Pseudomonas aeruginosa strain PcyII-10 variants resisting infec |
| 30991723 | 10.1186/1471-2407-6-41 | 10.3390/ijms20081861 | Cognizance of Molecular Methods for the Generation of Mutagenic Phage Display An |
| 30992351 | 10.1128/mBio.02790-18 | 10.1128/mBio.00446-19 | Evolutionary and Genomic Insights into Clostridioides difficile Sequence Type 11 |
| 30992664 | 10.1101/pdb.rec8111. | 10.2147/IJN.S190188 | Biomimetic hydroxyapatite nanocrystals are an active carrier for Salmonella bact |
| 30996083 | 10.1099/mgen.0.000167 | 10.1126/scitranslmed.aau9748 | Filamentous bacteriophages are associated with chronic Pseudomonas lung infectio |
| 30999559 | 10.3389/fmicb.2016.00882 | 10.3390/v11040352 | Phage Therapy Regulation: From Night to Dawn. |
| 31000791 | 10.1093/infdis/jiu059 | 10.1038/s41598-019-42681-1 | Isolation and characterisation of pVa-21, a giant bacteriophage with anti-biofil |
| 31010053 | 10.1128/AEM.01540-10 | 10.3390/v11040366 | Evaluation of Phage Therapy in the Context of Enterococcus faecalis and Its Asso |
| 31010201 | 10.1371/journal.pone.0096360 | 10.3390/v11040360 | First Evidence of Antibodies Against Lloviu Virus in Schreiber's Bent-Winged Ins |
| 31010858 | 10.3791/50318 | 10.1128/AAC.00024-19 | Isolation of Phage Lysins That Effectively Kill Pseudomonas aeruginosa in Mouse  |
| 31013713 | 10.1186/s13071-017-2576-8 | 10.3390/ijms20081812 | Leishmania infantum β-Tubulin Identified by Reverse Engineering Technology throu |
| 31013833 | 10.1016/S1473-3099(18)30605-4 | 10.3390/v11040343 | Current State of Compassionate Phage Therapy. |
| 31015204 | 10.1038/nphoton.2008.291 | 10.1074/jbc.RA119.008213 | Engineering nanomolar peptide ligands that differentially modulate EphA2 recepto |
| 31020041 | 10.1016/j.ijid.2014.09.010 | 10.1128/mSystems.00068-19 | Global Transcriptomic Analysis of the Interactions between Phage φAbp1 and Exten |
| 31028263 | 10.1186/1743-422X-10-58 | 10.1038/s41467-019-09914-3 | Differential human antibody repertoires following Zika infection and the implica |
| 31035322 | 10.4049/jimmunol.1500888 | 10.3390/ijms20092088 | Single-Domain Antibodies Represent Novel Alternatives to Monoclonal Antibodies a |
| 31039174 | 10.1371/journal.pone.0072070 | 10.1371/journal.pone.0216002 | The bacteriocin from the prophylactic candidate Streptococcus suis 90-1330 is wi |
| 31040333 | 10.1083/jcb.17.2.299 | 10.1038/s41598-019-43115-8 | Efficacy and safety assessment of two enterococci phages in an in vitro biofilm  |
| 31042470 | 10.1101/285916 | 10.1016/j.celrep.2019.03.097 | Comprehensive Profiling of HIV Antibody Evolution. |
| 31060321 | 10.1038/srep39505 | 10.3390/v11050420 | The Third Annual Meeting of the European Virus Bioinformatics Center. |
| 31069064 | 10.1038/srep45011 | 10.12688/f1000research.18093.1 | Combating Cholera. |
| 31089181 | 10.1107/S0907444909042073 | 10.1038/s41598-019-43748-9 | Structure and tailspike glycosidase machinery of ORF212 from E. coli O157:H7 pha |
| 31092596 | 10.1016/S1473-3099(18)30482-1 | 10.1128/JCM.00229-19 | Implications of Bacteriophage- and Bacteriophage Component-Based Therapies for t |
| 31093881 | 10.4238/2015.January.16.2 | 10.1007/s12250-019-00125-0 | Specific and Selective Bacteriophages in the Fight against Multidrug-resistant A |
| 31109012 | 10.1186/1471-2164-7-8 | 10.3390/v11050454 | Still Something to Discover: Novel Insights intoEscherichia coli Phage Diversity |
| 31111814 | 10.1128/jb.179.7.2459-2463.1997 | 10.1128/microbiolspec.GPP3-0025-2018 | Genomics and Genetics of Streptococcus pneumoniae. |
| 31111820 | 10.1016/j.ajpath.2011.12.037 | 10.1128/microbiolspec.GPP3-0059-2018 | The Bacteriophages of Streptococcus pyogenes. |
| 31120240 | 10.1021/acsinfecdis.6b00209 | 10.1021/acsinfecdis.9b00091 | Inhibition of Marburg Virus RNA Synthesis by a Synthetic Anti-VP35 Antibody. |
| 31123265 | 10.1038/s41467-018-06502-9 | 10.1038/s41467-019-10294-x | Altered respiratory virome and serum cytokine profile associated with recurrent  |
| 31126089 | 10.3390/v11030265 | 10.3390/v11050470 | "French Phage Network" Annual Conference 2018-Fourth Meeting Report. |
| 31130731 | 10.1016/j.ccr.2007.08.029 | 10.1038/s41417-019-0101-2 | Targeted AAVP-based therapy in a mouse model of human glioblastoma: a comparison |
| 31138130 | 10.1128/JB.01804-08 | 10.1186/s12866-019-1484-9 | Genomic analyses of two novel biofilm-degrading methicillin-resistant Staphyloco |
| 31164451 | 10.1093/nar/gkt1226 | 10.1128/mSystems.00191-18 | Temperate Bacteriophages from Chronic Pseudomonas aeruginosa Lung Infections Sho |
| 31164603 | 10.1126/science.277.5331.1453 | 10.3390/mps2010022 | Reverse Genetic Systems for Pseudomonas aeruginosa Leviphages. |
| 31167044 | 10.1074/mcp.M113.029538 | 10.1111/cmi.13063 | Molecular interactions between Neisseria meningitidis and its human host. |
| 31167904 | 10.1111/1574-6976.12074 | 10.1128/MMBR.00007-19 | Gut Microbiota and Colonization Resistance against Bacterial Enteric Infection. |
| 31172913 | 10.1038/srep09784 | 10.1128/microbiolspec.GPP3-0062-2019 | Pathogenicity Islands and Their Role in Staphylococcal Biology. |
| 31177014 | 10.1097/ppo.0000000000000045 | 10.1016/j.coviro.2019.05.007 | Virome and bacteriome: two sides of the same coin. |
| 31177333 | 10.1210/en.2011-1501 | 10.1007/s00216-019-01952-6 | Development of anti-immunocomplex specific antibodies and non-competitive time-r |
| 31190084 | 10.1126/science.298.5593.621 | 10.1007/s00018-019-03159-5 | Open reading frame mining identifies a TLR4 binding domain in the primary sequen |
| 31192160 | 10.1016/j.dnarep.2011.03.007 | 10.3389/fcimb.2019.00166 | phiD12-Like Livestock-Associated Prophages Are Associated With Novel Subpopulati |
| 31197251 | 10.1038/s41586-019-1257-5 | 10.1038/s41579-019-0226-1 | Playing dead during phage infection. |
| 31201356 | 10.1016/j.resmic.2017.11.002 | 10.1038/s41396-019-0450-8 | Diversity patterns of bacteriophages infecting Aggregatibacter and Haemophilus s |
| 31208333 | 10.1093/bioinformatics/btq413 | 10.1186/s12866-019-1481-z | Characterization of a bacteriophage with broad host range against strains of Pse |
| 31212699 | 10.1046/j.1472-765x.2000.00815.x | 10.3390/molecules24112193 | Microbiological Evaluation of 5 L- and 20 L-Transparent Polypropylene Buckets fo |
| 31212885 | 10.1128/MMBR.64.1.69-114.2000 | 10.3390/v11060557 | Hurdles for Phage Therapy to Become a Reality-An Editorial Comment. |
| 31212961 | 10.1021/bp070345m | 10.3390/toxins11060346 | Recombinant Antibodies against Mycolactone. |
| 31213694 | 10.1016/j.chom.2017.09.012 | 10.1038/d41586-019-01880-6 | The secret social lives of viruses. |
| 31219660 | 10.1074/jbc.M109.096172 | 10.1111/cmi.13072 | The C-type lectin receptor MGL senses N-acetylgalactosamine on the unique Staphy |
| 31231326 | 10.1016/j.cell.2015.09.027 | 10.3389/fmicb.2019.01218 | A Type VI Secretion System Trans-Kingdom Effector Is Required for the Delivery o |
| 31231616 | 10.1186/s40793-015-0098-6 | 10.3389/fcimb.2019.00167 | Comparative Genome Analysis of Uropathogenic Morganella morganii Strains. |
| 31235961 | 10.1093/femsle/fnw047 | 10.1038/s41591-019-0506-3 | Genetically engineered phages for therapeutics: proceed with caution. |
| 31239501 | 10.1016/S0168-583X(01)01211-3 | 10.1038/s41598-019-45775-y | Aptness of Escherichia coli host strain CB390 to detect total coliphages in Colo |
| 31241898 | 10.1107/S0021889892009944 | 10.1021/acschembio.9b00290 | Folding Then Binding vs Folding Through Binding in Macrocyclic Peptide Inhibitor |
| 31242068 | 10.1080/19420862.2016.1155014 | 10.1080/19420862.2019.1629239 | Characterization of a novel anti-human lymphocyte activation gene 3 (LAG-3) anti |
| 31242267 | 10.1038/s41426-018-0197-8 | 10.1371/journal.pone.0219091 | Development of two antigen-binding fragments to a conserved linear epitope of hu |
| 31243315 | 10.1093/nar/22.22.4673 | 10.1038/s41598-019-41039-x | Chloramphenicol inhibits eukaryotic Ser/Thr phosphatase and infection-specific c |
| 31243996 | 10.1038/s41598-017-14823-w | 10.1021/acs.biochem.9b00184 | Rapid Discovery and Characterization of Synthetic Neutralizing Antibodies agains |
| 31247001 | 10.1007/s12272-014-0503-5 | 10.1371/journal.pone.0218252 | The oral microbiome of early stage Parkinson's disease and its relationship with |
| 31252683 | 10.1073/pnas.96.5.2192 | 10.3390/v11070587 | Phages and Human Health: More Than Idle Hitchhikers. |
| 31261372 | 10.1093/nar/gkw419 | 10.1038/s41390-019-0491-8 | Experimental support for multidrug resistance transfer potential in the preterm  |
| 31263188 | 10.1016/j.jmb.2015.11.006 | 10.1038/s41598-019-45760-5 | SMRT sequencing reveals differential patterns of methylation in two O111:H- STEC |
| 31266884 | 10.1534/genetics.113.159541 | 10.26508/lsa.201900366 | Systematic identification of recognition motifs for the hub protein LC8. |
| 31273267 | 10.1371/journal.pone.0037557 | 10.1038/s41598-019-46087-x | Type 1 Diabetes: an Association Between Autoimmunity, the Dynamics of Gut Amyloi |
| 31276485 | 10.1111/j.1365-2958.2005.04584.x | 10.1371/journal.ppat.1007888 | Bacteriophages benefit from generalized transduction. |
| 31277396 | 10.1128/JVI.01492-16 | 10.3390/mi10070450 | Analysis of Bacteriophages with Insulator-Based Dielectrophoresis. |
| 31278366 | 10.1016/0076-6879(86)30013-2 | 10.1038/s41598-019-46224-6 | Selective cytotoxicity and antifungal properties of copper(II) and cobalt(II) co |
| 31285240 | 10.1186/s12864-016-3346-2 | 10.1128/JB.00370-19 | Methylation Warfare: Interaction of Pneumococcal Bacteriophages with Their Host. |
| 31285584 | 10.5281/zenodo.1230436 | 10.1038/s41564-019-0494-6 | Global phylogeography and ancient evolution of the widespread human gut virus cr |
| 31291645 | 10.3390/medsci6040086 | 10.1371/journal.pone.0219599 | Phages in a thermoreversible sustained-release formulation targeting E. faecalis |
| 31295925 | 10.1073/pnas.110147297 | 10.3390/ijms20143391 | A Method for Improving the Accuracy and Efficiency of Bacteriophage Genome Annot |
| 31316751 | 10.1038/ismej.2015.183 | 10.12688/f1000research.18480.1 | A theoretical model of temperate phages as mediators of gut microbiome dysbiosis |
| 31323792 | 10.1128/AEM.05741-11 | 10.3390/v11070656 | Human Virome and Disease: High-Throughput Sequencing for Virus Discovery, Identi |
| 31323845 | 10.1128/CMR.00030-10 | 10.3390/v11070657 | Ts2631 Endolysin from the Extremophilic Thermus scotoductus Bacteriophage vB_Tsc |
| 31324156 | 10.1186/1471-2105-10-421 | 10.1186/s12864-019-5951-3 | Discovery and characterization of the evolution, variation and functions of dive |
| 31330855 | 10.1093/bioinformatics/btx383 | 10.3390/v11070667 | A Protocol for Extraction of Infective Viromes Suitable for Metagenomics Sequenc |
| 31332326 | 10.1002/0471250953.bi0508s52 | 10.1038/s41587-019-0193-0 | Continuous evolution of base editors with expanded target compatibility and impr |
| 31344144 | 10.1126/science.1134426 | 10.1371/journal.pone.0219842 | A system for site-specific integration of transgenes in mammalian cells. |
| 31349628 | 10.1186/1756-0500-5-244 | 10.3390/antibiotics8030103 | Synergistic Action of Phage and Antibiotics: Parameters to Enhance the Killing E |
| 31354735 | 10.1016/j.toxicon.2019.06.005 | 10.3389/fimmu.2019.01598 | History of Envenoming Therapy and Current Perspectives. |
| 31361781 | 10.1093/bioinformatics/bti054 | 10.1371/journal.pone.0220494 | Nanopore sequencing for fast determination of plasmids, phages, virulence marker |
| 31371773 | 10.1172/JCI8978 | 10.1038/s41598-019-47413-z | Promotion of angiogenesis by M13 phage and RGD peptide in vitro and in vivo. |
| 31375703 | 10.1016/j.jmb.2010.10.030 | 10.1038/s41598-019-47600-y | A Novel Cell-Penetrating Antibody Fragment Inhibits the DNA Repair Protein RAD51 |
| 31379775 | 10.1074/jbc.M113.499772 | 10.3389/fmicb.2019.01615 | Baseplate Component TssK and Spatio-Temporal Assembly of T6SS in Pseudomonas aer |
| 31383878 | 10.1038/nature12352 | 10.1038/s41598-019-47656-w | A simple, reproducible and cost-effective procedure to analyse gut phageome: fro |
| 31383901 | 10.1159/000239371 | 10.1038/s41598-019-47742-z | Defining a Core Genome for the Herpesvirales and Exploring their Evolutionary Re |
| 31388083 | 10.1128/IAI.72.9.5340-5348.2004 | 10.1038/s41598-019-47931-w | Inhibition of Francisella tularensis phagocytosis using a novel anti-LPS scFv an |
| 31391493 | 10.1016/b978-0-12-801185-0.00001-5 | 10.1038/s41598-019-47857-3 | Real-Time Selective Sequencing with RUBRIC: Read Until with Basecall and Referen |
| 31394847 | 10.1093/nar/19.15.4133 | 10.3390/toxins11080464 | Camelid VHHs Fused to Human Fc Fragments Provide Long Term Protection Against Bo |
| 31399594 | 10.1021/bi962514+ | 10.1038/s41467-019-11604-z | Virus lasers for biological detection. |
| 31402174 | 10.1101/027607 | 10.1016/j.cell.2019.07.016 | Large-Scale Analyses of Human Microbiomes Reveal Thousands of Small, Novel Genes |
| 31405109 | 10.3390/v11010050 | 10.3390/v11080737 | Bacteriophage-Based Biotechnological Applications. |
| 31409682 | 10.1073/pnas.0832438100 | 10.1128/mBio.01698-19 | Pseudomonas aeruginosa Interstrain Dynamics and Selection of Hyperbiofilm Mutant |
| 31409688 | 10.1128/CVI.00115-14 | 10.1128/mBio.01869-19 | Development of a Gold Nanoparticle Vaccine against Enterohemorrhagic Escherichia |
| 31412645 | 10.1186/1471-2180-10-301 | 10.3390/v11080749 | Selection of Bacteriophages to Control In Vitro 24 h Old Biofilm of Pseudomonas  |
| 31413262 | 10.1051/medsci/20031989840 | 10.1038/s41598-019-47891-1 | Intrabody against prolyl hydroxylase 2 promotes angiogenesis by stabilizing hypo |
| 31416880 | 10.1128/mSystems.00191-18 | 10.1128/MRA.00853-19 | Genome Sequence of Pseudomonas Phage UMP151, Isolated from the Female Bladder Mi |
| 31417879 | 10.7150/jca.17712 | 10.3389/fcimb.2019.00275 | Preparation and Evaluation of the Fully Humanized Monoclonal Antibody GD-mAb Aga |
| 31427601 | 10.1002/1522-2683(200208)23:15<2373::AID-ELPS2373>3.0.CO;2-W | 10.1038/s41467-019-11695-8 | High-throughput screen reveals sRNAs regulating crRNA biogenesis by targeting CR |
| 31434316 | 10.1155/2016/9582430 | 10.3390/biom9080386 | Proinflammatory Action of a New Electronegative Low-Density Lipoprotein Epitope. |
| 31443115 | 10.1126/sciadv.aaw1228 | 10.1002/jbm.a.36790 | Bacteriophage delivering hydrogels reduce biofilm formation in vitro and infecti |
| 31443379 | 10.1111/pde.12766 | 10.3390/v11090769 | Therapeutic Potential of an Endolysin Derived from Kayvirus S25-3 for Staphyloco |
| 31447177 | 10.1101/420604 | 10.1016/j.cell.2019.07.035 | DNA-Packing Portal and Capsid-Associated Tegument Complexes in the Tumor Herpesv |
| 31448090 | 10.1038/s41591-019-0437-z | 10.12688/f1000research.19509.1 | Emerging therapies against infections with Pseudomonas aeruginosa. |
| 31451543 | 10.1073/pnas.1415712111 | 10.1128/JB.00383-19 | PQS Produced by the Pseudomonas aeruginosa Stress Response Repels Swarms Away fr |
| 31454976 | 10.1016/j.pbiomolbio.2014.02.003 | 10.3390/v11090785 | Combinatorial Avidity Selection of Mosaic Landscape Phages Targeted at Breast Ca |
| 31461177 | 10.1101/333625 | 10.1002/ana.25588 | Chronic Dengue Virus Panencephalitis in a Patient with Progressive Dementia with |
| 31461846 | 10.1093/nar/gkv623 | 10.3390/ijms20174187 | Homology Modeling-Based in Silico Affinity Maturation Improves the Affinity of a |
| 31462656 | 10.1186/s12864-016-2611-8 | 10.1038/s41598-019-48993-6 | Discovery of HSPG2 (Perlecan) as a Therapeutic Target in Triple Negative Breast  |
| 31467087 | 10.1038/s41586-018-0291-z | 10.1101/gad.329508.119 | Control of homologous recombination by the HROB-MCM8-MCM9 pathway. |
| 31482502 | 10.1038/srep29344 | 10.1007/978-981-13-7709-9_11 | Enzybiotics: Enzyme-Based Antibacterials as Therapeutics. |
| 31488062 | 10.1038/nmeth.1923 | 10.1186/s12866-019-1586-4 | Improved single-swab sample preparation for recovering bacterial and phage DNA f |
| 31488108 | 10.1038/s41426-018-0031-3 | 10.1186/s12896-019-0554-2 | Intracellular human antibody fragments recognizing the VP35 protein of Zaire Ebo |
| 31488912 | 10.1038/s41568-019-0155-3 | 10.1038/s41568-019-0203-z | Phage warriors. |
| 31492910 | 10.1038/emboj.2013.79 | 10.1038/s41598-019-49233-7 | Integrating SpyCatcher/SpyTag covalent fusion technology into phage display work |
| 31502535 | 10.1371/journal.pone.0126264 | 10.7554/eLife.46540 | Functional metagenomics-guided discovery of potent Cas9 inhibitors in the human  |
| 31526274 | 10.1111/j.1365-2249.2009.04011.x | 10.1080/10408363.2019.1660303 | Complex interactions between the microbiome and cancer immune therapy. |
| 31527029 | 10.3389/fmicb.2014.00051 | 10.1128/AAC.00924-19 | Bacteriophages as Adjuvant to Antibiotics for the Treatment of Periprosthetic Jo |
| 31527112 | 10.1101/248849 | 10.1128/JB.00568-19 | PQS Signaling for More than a Quorum: the Collective Stress Response Protects He |
| 31530875 | 10.1016/0003-2697(84)90553-0 | 10.1038/s41598-019-50030-5 | Identification and characterization of phage protein and its activity against tw |
| 31533281 | 10.1128/AAC.00300-10 | 10.3390/v11090869 | Bacterial Virus Lambda Gpd-Fusions to Cathelicidins, α- and β-Defensins, and Dis |
| 31537684 | 10.7717/peerj.985 | 10.1128/MRA.01073-19 | Complete Genome Sequence of a Pseudomonas aeruginosa Isolate from a Kidney Stone |
| 31548497 | 10.1007/s00113-017-0374-6 | 10.3390/v11100891 | Bacteriophage Application for Difficult-to-treat Musculoskeletal Infections: Dev |
| 31548657 | 10.1371/journal.pone.0079798 | 10.1038/s41417-019-0137-3 | Specific driving of the suicide E gene by the CEA promoter enhances the effects  |
| 31551330 | 10.1038/nbt.1754 | 10.1128/mBio.01652-19 | Resistance Evolution against Phage Combinations Depends on the Timing and Order  |
| 31551983 | 10.1111/j.1749-4486.2009.01973.x | 10.3389/fmicb.2019.02049 | Quorum Quenching Lactonase Strengthens Bacteriophage and Antibiotic Arsenal Agai |
| 31553300 | 10.1128/JCM.01275-06 | 10.1099/mgen.0.000297 | Phylogenomic analysis of gastroenteritis-associated Clostridium perfringens in E |
| 31562736 | 10.1126/science.aat5867 | 10.1128/microbiolspec.GPP3-0058-2018 | Temperate Phages of Staphylococcus aureus. |
| 31564196 | 10.1007/s12033-012-9601-0 | 10.1080/15384047.2019.1665953 | Identification of anti-CD16a single domain antibodies and their application in b |
| 31570731 | 10.1038/nprot.2006.73 | 10.1038/s41467-019-12449-2 | High levels of AAV vector integration into CRISPR-induced DNA breaks. |
| 31575664 | 10.3354/meps072205 | 10.1128/mSystems.00221-19 | Lying in Wait: Modeling the Control of Bacterial Infections via Antibiotic-Induc |
| 31578217 | 10.1128/AEM.00448-09 | 10.1128/MMBR.00005-19 | Persistence and Decay of Fecal Microbiota in Aquatic Habitats. |
| 31578263 | 10.3390/v10110638 | 10.1128/JCM.01006-19 | Methicillin-Resistant Staphylococcus aureus in Hospitals: Latest Trends and Trea |
| 31582898 | 10.1128/jvi.02043-14 | 10.1155/2019/3730519 | Bacteriophages: Uncharacterized and Dynamic Regulators of the Immune System. |
| 31587298 | 10.1101/619999 | 10.5694/mja2.50355 | Phage therapy for severe bacterial infections: a narrative review. |
| 31589660 | 10.1128/iai.70.2.938-944.2002 | 10.1371/journal.ppat.1008032 | Phage resistance at the cost of virulence: Listeria monocytogenes serovar 4b req |
| 31590369 | 10.18388/abp.2015_1114 | 10.3390/antibiotics8040175 | Exacerbations of Chronic Rhinosinusitis-Microbiology and Perspectives of Phage T |
| 31594506 | 10.1164/rccm.201009-1430OC | 10.1098/rspb.2019.1794 | Transposable temperate phages promote the evolution of divergent social strategi |
| 31594997 | 10.1038/nprot.2016.070 | 10.1038/s41598-019-51016-z | Modulation of PTH1R signaling by an ECD binding antibody results in inhibition o |
| 31600502 | 10.1111/j.1365-2958.2007.06027.x | 10.1016/j.chom.2019.09.006 | Viral Satellites Exploit Phage Proteins to Escape Degradation of the Bacterial H |
| 31611357 | 10.3389/fmicb.2018.01832 | 10.1128/AAC.01281-19 | A Dutch Case Report of Successful Treatment of Chronic Relapsing Urinary Tract I |
| 31619676 | 10.1021/acs.biochem.7b00311 | 10.1038/s41467-019-12681-w | Super-resolution imaging of fluorescent dipoles via polarized structured illumin |
| 31623599 | 10.1016/j.virol.2009.09.012 | 10.1186/s12896-019-0559-x | Development of a novel human phage display-derived anti-LAG3 scFv antibody targe |
| 31624289 | 10.1038/nprot.2016.169 | 10.1038/s41598-019-51089-w | Human single-chain antibodies that neutralize Pseudomonas aeruginosa-exotoxin A- |
| 31634471 | 10.1016/j.str.2019.06.008 | 10.1016/j.jmb.2019.09.024 | Structural and Functional Analysis of Ubiquitin-based Inhibitors That Target the |
| 31635282 | 10.1056/NEJMra0902814 | 10.3390/toxins11100607 | Contribution and Interaction of Shiga Toxin Genes to Escherichia coli O157:H7 Vi |
| 31639052 | 10.4103/abr.abr_243_15 | 10.1186/s13104-019-4711-4 | Genotyping and characterization of prophage patterns in clinical isolates of Sta |
| 31640814 | 10.3389/fimmu.2017.01287 | 10.1186/s40425-019-0705-y | Discovery of low-molecular weight anti-PD-L1 peptides for cancer immunotherapy. |
| 31641028 | 10.3390/ph4030494 | 10.1261/rna.067835.118 | Live-cell imaging of single mRNA dynamics using split superfolder green fluoresc |
| 31645642 | 10.1371/journal.pone.0206278 | 10.1038/s41598-019-51742-4 | Improved lyophilization conditions for long-term storage of bacteriophages. |
| 31653906 | 10.1099/00221287-136-7-1343 | 10.1038/s41598-019-51628-5 | Clostridium difficile clade 3 (RT023) have a modified cell surface and contain a |
| 31656180 | 10.1186/1756-3305-6-3 | 10.1186/s12887-019-1731-0 | Prevalence and factors associated with intestinal parasitic infection among unde |
| 31660953 | 10.1016/j.chom.2019.01.017 | 10.1186/s12915-019-0704-y | Studying the gut virome in the metagenomic era: challenges and perspectives. |
| 31666296 | 10.1007/978-1-4939-7343-9_15 | 10.1128/MMBR.00012-19 | Pharmacologically Aware Phage Therapy: Pharmacodynamic and Pharmacokinetic Obsta |
| 31669042 | 10.1016/j.tips.2019.04.001 | 10.1016/j.str.2019.10.004 | Development of "Plug and Play" Fiducial Marks for Structural Studies of GPCR Sig |
| 31676478 | 10.1038/nmeth.1318 | 10.1128/AEM.01922-19 | Prophages in Lactobacillus reuteri Are Associated with Fitness Trade-Offs but Ca |
| 31681623 | 10.1128/IAI.69.9.5385-5394.2001 | 10.3389/fcimb.2019.00343 | Editorial: Beyond Antimicrobials: Non-traditional Approaches to Combating Multid |
| 31683810 | 10.1517/14728222.2011.648617 | 10.3390/biom9110681 | Antibody-Based Targeting of Cell Surface GRP94 Specifically Inhibits Cetuximab-R |
| 31685458 | 10.1016/S1473-3099(18)30482-1 | 10.1128/AAC.01987-19 | What's Old Is New Again: Bacteriophage Therapy in the 21st Century. |
| 31687381 | 10.1002/jmv.25193 | 10.1155/2019/2560401 | External Control Viral-Like Particle Construction for Detection of Emergent Arbo |
| 31690625 | 10.1016/j.jmb.2007.05.022 | 10.1074/jbc.RA119.010251 | An engineered antibody fragment targeting mutant β-catenin via major histocompat |
| 31696062 | 10.1093/nar/gkr485 | 10.3389/fcimb.2019.00363 | Staphylococcus aureus Small Colony Variants (SCVs): News From a Chronic Prosthet |
| 31701033 | 10.1007/s11263-006-0002-3 | 10.1038/s42003-019-0633-x | Spatial structure affects phage efficacy in infecting dual-strain biofilms of Ps |
| 31717800 | 10.1021/acs.bioconjchem.8b00285 | 10.3390/v11110988 | Evolution of a Landscape Phage Library in a Mouse Xenograft Model of Human Breas |
| 31723265 | 10.1002/hep.30832 | 10.1038/s41586-019-1742-x | Bacteriophage targeting of gut bacterium attenuates alcoholic liver disease. |
| 31727099 | 10.1016/j.virol.2012.09.002 | 10.1186/s12967-019-2120-z | Exploring the whole standard operating procedure for phage therapy in clinical p |
| 31730461 | 10.1093/bioinformatics/btp352 | 10.1186/s12864-019-6260-6 | WGS based study of the population structure of Salmonella enterica serovar Infan |
| 31740838 | 10.1101/471219 | 10.1038/s41587-019-0299-4 | In situ readout of DNA barcodes and single base edits facilitated by in vitro tr |
| 31741097 | 10.1093/cid/cix596 | 10.1007/s00705-019-04466-9 | In-depth serum virome analysis in patients with acute liver failure with indeter |
| 31742539 | 10.1128/JB.01430-08 | 10.3201/eid2512.190267 | Genomic Analysis of Fluoroquinolone- and Tetracycline-Resistant Campylobacter je |
| 31743332 | 10.1016/S0923-2508(97)85244-8 | 10.1371/journal.pone.0220584 | Characterization of the diverse plasmid pool harbored by the blaNDM-1-containing |
| 31744662 | 10.1099/mic.0.000220 | 10.1016/j.tim.2019.10.007 | Steering Phages to Combat Bacterial Pathogens. |
| 31745353 | 10.3389/fmicb.2019.00566 | 10.1038/d41586-019-03417-3 | Microbial clues to a liver disease. |
| 31752386 | 10.3389/fmicb.2017.01460 | 10.3390/v11111080 | Characterization of Klebsiella pneumoniae ST11 Isolates and Their Interactions w |
| 31754272 | 10.1101/214213 | 10.1038/s41564-019-0616-1 | Dyeing to connect. |
| 31766537 | 10.1016/j.surg.2005.02.012 | 10.3390/v11121083 | Promises and Pitfalls of In Vivo Evolution to Improve Phage Therapy. |
| 31766550 | 10.1016/j.jmb.2006.03.043 | 10.3390/v11121085 | Evolution of BACON Domain Tandem Repeats in crAssphage and Novel Gut Bacteriopha |
| 31766758 | 10.1128/AAC.02440-16 | 10.3390/ijms20235868 | Mycobacterium abscessus, an Emerging and Worrisome Pathogen among Cystic Fibrosi |
| 31771160 | 10.1002/med.21572 | 10.3390/v11121089 | Pseudomonas aeruginosa PA5oct Jumbo Phage Impacts Planktonic and Biofilm Populat |
| 31774589 | 10.1182/blood.2019000481 | 10.1002/pro.3794 | Engineering the serpin α1 -antitrypsin: A diversity of goals and techniques. |
| 31774847 | 10.1073/pnas.0604891103 | 10.1371/journal.pone.0225057 | Analysis of virulence potential of Escherichia coli O145 isolated from cattle fe |
| 31781060 | 10.1101/gr.074492.107 | 10.3389/fmicb.2019.02537 | Constructing and Characterizing Bacteriophage Libraries for Phage Therapy of Hum |
| 31784537 | 10.1038/ncomms7884 | 10.1038/s41467-019-13517-3 | DNA origami cryptography for secure communication. |
| 31784706 | 10.1038/s41575-018-0099-1 | 10.1038/s41575-019-0246-3 | Manipulating the gut microbiota to combat alcoholic hepatitis. |
| 31789928 | 10.3390/molecules23092392 | 10.1097/MOO.0000000000000598 | Latest developments on topical therapies in chronic rhinosinusitis. |
| 31795231 | 10.1146/annurev.micro.55.1.437 | 10.3390/v11121105 | Yersinia Phages and Food Safety. |
| 31795802 | 10.1021/bi100978r | 10.1080/19420862.2019.1689027 | An engineered human IgG1 CH2 domain with decreased aggregation and nonspecific b |
| 31804537 | 10.1080/14653240902783268 | 10.1038/s41598-019-54686-x | Upregulation of tropomyosin alpha-4 chain in patients' saliva with oral squamous |
| 31804848 | 10.1128/microbiolspec.PFS-0023-2018 | 10.1089/fpd.2019.2706 | Source Attribution of Salmonella in Macadamia Nuts to Animal and Environmental R |
| 31805175 | 10.4172/2155-9899.1000402 | 10.1371/journal.pone.0226162 | Identification of novel non-myelin biomarkers in multiple sclerosis using an imp |
| 31817243 | 10.1016/j.fm.2007.07.007 | 10.3390/genes10121007 | Genomic Diversity of Common Sequence Types of Listeria monocytogenes Isolated fr |
| 31823811 | 10.7717/peerj.985 | 10.1186/s40168-019-0766-7 | Discordant transmission of bacteria and viruses from mothers to babies at birth. |
| 31827120 | 10.1111/j.1365-2958.1990.tb00671.x | 10.1038/s41598-019-54895-4 | Diversity of P1 phage-like elements in multidrug resistant Escherichia coli. |
| 31829073 | 10.1038/nbt785 | 10.1080/19420862.2019.1701792 | Exploiting next-generation sequencing in antibody selections - a simple PCR meth |
| 31831017 | 10.1080/03079450400013162 | 10.1186/s12985-019-1260-3 | Veterinary use of bacteriophage therapy in intensively-reared livestock. |
| 31842457 | 10.1093/bioinformatics/btm404 | 10.3390/biom9120868 | Generation of Lamprey Monoclonal Antibodies (Lampribodies) Using the Phage Displ |
| 31848274 | 10.1093/nar/gki029 | 10.1128/mBio.02451-19 | Mining the Methylome Reveals Extensive Diversity in Staphylococcus epidermidis R |
| 31849908 | 10.3389/fmicb.2017.00403 | 10.3389/fmicb.2019.02772 | vB_PaeM_MIJ3, a Novel Jumbo Phage Infecting Pseudomonas aeruginosa, Possesses Un |
| 31849974 | 10.1101/308973 | 10.3389/fimmu.2019.02796 | Diagnostic Profiling of the Human Public IgM Repertoire With Scalable Mimotope L |
| 31858443 | 10.12688/wellcomeopenres.13373.1 | 10.1007/s42770-019-00214-y | Genomic information on Stenotrophomonas maltophilia ST264 isolated from a cystic |
| 31866964 | 10.3390/molecules18078607 | 10.3389/fmicb.2019.02771 | Dendronized Silver Nanoparticles as Bacterial Membrane Permeabilizers and Their  |
| 31867291 | 10.1099/vir.0.81515-0 | 10.3389/fcimb.2019.00417 | A Murine Monoclonal Antibody With Potent Neutralization Ability Against Human Ad |
| 31870137 | 10.4166/kjg.2017.69.4.226 | 10.4166/kjg.2019.74.6.314 | Role of Gut Microbiota in Type 2 Diabetes Mellitus and Its Complications: Novel  |
| 31877142 | 10.1086/653482 | 10.1371/journal.pntd.0007884 | Development of RT-qPCR and semi-nested RT-PCR assays for molecular diagnosis of  |
| 31883087 | 10.1007/978-1-60761-652-8_30 | 10.1007/978-1-0716-0211-9_5 | Bacterial Artificial Chromosome-Based Lambda Red Recombination with the I-SceI H |
| 31888202 | 10.1093/intimm/dxs081 | 10.3390/ijms20246340 | Extended Cleavage Specificities of Rabbit and Guinea Pig Mast Cell Chymases: Two |
| 31888239 | 10.1016/j.idcr.2018.e00439 | 10.3390/v11121163 | Genomic and Proteomic Characterization of Bacteriophage BH1 Spontaneously Releas |
| 31894001 | 10.1038/nbt.2782 | 10.1186/s12929-019-0592-z | Development of therapeutic antibodies for the treatment of diseases. |
| 31896785 | 10.1098/rstb.2018.0094 | 10.1038/s41396-019-0577-7 | The effect of phage genetic diversity on bacterial resistance evolution. |
| 31905218 | 10.1016/j.pep.2005.04.004 | 10.1371/journal.ppat.1008223 | Novel EBV LMP-2-affibody and affitoxin in molecular imaging and targeted therapy |
| 31905631 | 10.1093/jnci/djy134 | 10.3390/biom10010051 | Development of Human Monoclonal Antibody for Claudin-3 Overexpressing Carcinoma  |
| 31907420 | 10.1038/s41586-019-1742-x | 10.1038/d41573-019-00198-2 | Phages fight alcoholic hepatitis. |
| 31913346 | 10.1093/nar/gkz239 | 10.1038/s41598-019-56763-7 | Meta-analysis of Pandemic Escherichia coli ST131 Plasmidome Proves Restricted Pl |
| 31928310 | 10.4161/mabs.27230 | 10.1080/19420862.2020.1714371 | A novel human monoclonal antibody specific to the A33 glycoprotein recognizes co |
| 31931655 | 10.1093/bioinformatics/btx184 | 10.1080/19490976.2019.1701353 | Dietary prophage inducers and antimicrobials: toward landscaping the human gut m |
| 31936552 | 10.1093/molbev/msu300 | 10.3390/ijms21020425 | Isolation of Four Lytic Phages Infecting Klebsiella pneumoniae K22 Clinical Isol |
| 31940321 | 10.1093/bioinformatics/btu033 | 10.1371/journal.pone.0226930 | Biogeographic study of human gut-associated crAssphage suggests impacts from ind |
| 31941900 | 10.1016/j.chemolab.2015.02.019 | 10.1038/s41467-019-14103-3 | Acquisition, transmission and strain diversity of human gut-colonizing crAss-lik |
| 31941901 | 10.1021/ja508416e | 10.1038/s41467-019-13948-y | Targeting the tumor vasculature with engineered cystine-knot miniproteins. |
| 31942051 | 10.1016/j.chom.2018.12.014 | 10.1038/s41586-019-1894-8 | The arms race between bacteria and their phage foes. |
| 31942057 | 10.1038/s41598-019-49975-4 | 10.1038/d41586-020-00053-0 | The kill-switch for CRISPR that could make gene-editing safer. |
| 31947597 | 10.1089/hum.2018.145 | 10.3390/ijms21020515 | Finding the Keys to the CAR: Identifying Novel Target Antigens for T Cell Redire |
| 31953385 | 10.1093/bioinformatics/btr039 | 10.1038/s41467-019-14042-z | Virulent coliphages in 1-year-old children fecal samples are fewer, but more inf |
| 31953428 | 10.1002/pro.5560030911 | 10.1038/s41598-019-57103-5 | Human antibodies neutralizing diphtheria toxin in vitro and in vivo. |
| 31971941 | 10.1101/gr.210641.116 | 10.1371/journal.pcbi.1007314 | An educational guide for nanopore sequencing in the classroom. |
| 31974622 | 10.3390/biomedicines7010018 | 10.3892/mmr.2019.10880 | Affinity improvement of the fully human anti‑TSLP recombinant antibody. |
| 31976323 | 10.21037/jtd.2018.01.111 | 10.1155/2019/6051870 | Rapid Affinity Maturation of Novel Anti-PD-L1 Antibodies by a Fast Drop of the A |
| 31976857 | 10.1093/bioinformatics/btx157 | 10.1099/jmm.0.001141 | Bacteriophages of Klebsiella spp., their diversity and potential therapeutic use |
| 31980006 | 10.1186/gb-2011-12-11-r112 | 10.1080/19420862.2020.1717265 | In situ antibody phage display yields optimal inhibitors of integrin α11/β1. |
| 31988343 | 10.1186/1472-6750-13-52 | 10.1038/s41598-019-57279-w | Affinity-matured variants derived from nimotuzumab keep the original fine specif |
| 31992617 | 10.1093/nar/gky379 | 10.1128/mBio.02530-19 | Phage Resistance in Multidrug-Resistant Klebsiella pneumoniae ST258 Evolves via  |
| 31996833 | 10.1038/s41591-018-0238-9 | 10.1038/d41586-020-00199-x | Fighting cancer with microbes. |
| 32001704 | 10.1016/S0378-1119(01)00824-1 | 10.1038/s41467-020-14397-8 | Rewiring of endogenous signaling pathways to genomic targets for therapeutic cel |
| 32011231 | 10.1016/0022-2836(76)90119-4 | 10.1099/jmm.0.001162 | Myoviridae phage PDX kills enteroaggregative Escherichia coli without human micr |
| 32019835 | 10.1128/JB.172.4.1899-1904.1990 | 10.1128/mSystems.00756-19 | Quantitative Models of Phage-Antibiotic Combination Therapy. |
| 32033406 | 10.1128/IAI.00711-18 | 10.3390/toxins12020103 | Bacteriocins of Listeria monocytogenes and Their Potential as a Virulence Factor |
| 32033477 | 10.1038/s41575-019-0242-7 | 10.3390/ijms21031061 | Defeating Antibiotic-Resistant Bacteria: Exploring Alternative Therapies for a P |
| 32036540 | 10.1128/AEM.00732-10 | 10.1007/s11262-020-01735-7 | Approaches to optimize therapeutic bacteriophage and bacteriophage-derived produ |
| 32047137 | 10.1093/nar/gkw1004 | 10.1128/mBio.03339-19 | Genome Dynamics of Vibrio cholerae Isolates Linked to Seasonal Outbreaks of Chol |
| 32053790 | 10.1056/NEJMoa1414216 | 10.1016/j.chom.2020.01.001 | Longitudinal Human Antibody Repertoire against Complete Viral Proteome from Ebol |
| 32059512 | 10.1021/acssynbio.7b00179 | 10.3390/v12020205 | Isolation and Characterization of AbTJ, an Acinetobacter baumannii Phage, and Fu |
| 32066959 | 10.1164/rccm.201904-0839LE | 10.1038/s41564-019-0634-z | Safety of bacteriophage therapy in severe Staphylococcus aureus infection. |
| 32069281 | 10.1016/j.str.2014.11.010 | 10.1371/journal.pcbi.1007636 | Structural diversity of B-cell receptor repertoires along the B-cell differentia |
| 32069326 | 10.1038/nmeth.3541 | 10.1371/journal.ppat.1008314 | Structure of the host cell recognition and penetration machinery of a Staphyloco |
| 32069856 | 10.1038/nature07814 | 10.3390/molecules25040808 | Targeting Tumors Using Peptides. |
| 32073830 | 10.1080/15459624.2015.1043058 | 10.1021/acs.est.9b06034 | Evaluating the Environmental Persistence and Inactivation of MS2 Bacteriophage a |
| 32075083 | 10.2220/biomedres.35.105 | 10.3390/molecules25040843 | Phage Display-Based Nanotechnology Applications in Cancer Immunotherapy. |
| 32075512 | 10.1002/0471143030.cb0322s30. | 10.1177/0022034520905792 | Insights Obtained by Culturing Saccharibacteria With Their Bacterial Hosts. |
| 32076016 | 10.1038/nprot.2017.126 | 10.1038/s41598-020-59745-2 | Golden Gate assembly with a bi-directional promoter (GBid): A simple, scalable m |
| 32076029 | 10.1177/1087057108327329 | 10.1038/s41598-020-59818-2 | A novel anti-HER2 antibody GB235 reverses Trastuzumab resistance in HER2-express |
| 32079185 | 10.1002/anie.201508445 | 10.3390/molecules25040874 | Novel Blood-Brain Barrier Shuttle Peptides Discovered through the Phage Display  |
| 32080807 | 10.15252/emmm.201607156 | 10.1007/s11033-020-05313-w | A high affinity nanobody against endothelin receptor type B: a new approach to t |
| 32084151 | 10.1002/ana.24088 | 10.1371/journal.pone.0228883 | Oligoclonal IgG antibodies in multiple sclerosis target patient-specific peptide |
| 32086379 | 10.1038/nmeth.1802 | 10.1074/jbc.RA119.011025 | Conformation-specific inhibitors of activated Ras GTPases reveal limited Ras dep |
| 32090123 | 10.1136/bmj.317.7155.371 | 10.1155/2020/8152640 | Sexual Differences in response to Mid- or Low-Premixed Insulin Analogue in Patie |
| 32093349 | 10.3390/ph10020043 | 10.3390/v12020235 | Bacteriophages for Chronic Wound Treatment: from Traditional to Novel Delivery S |
| 32094257 | 10.1128/AAC.00871-19 | 10.1128/IAI.00926-19 | Fitness Trade-Offs Resulting from Bacteriophage Resistance Potentiate Synergisti |
| 32099077 | 10.1038/nrmicro.2017.61 | 10.1038/s41579-020-0347-6 | Phage liquid crystals protect Pseudomonas. |
| 32102684 | 10.1101/gr.129684.111 | 10.1186/s13059-020-01956-x | Allosteric inhibition of CRISPR-Cas9 by bacteriophage-derived peptides. |
| 32103171 | 10.1038/71577 | 10.1038/s41564-019-0666-4 | Treat phage like living antibiotics. |
| 32125643 | 10.2106/JBJS.K.01135 | 10.1007/s12250-019-00192-3 | Bacteriophages and Lysins in Biofilm Control. |
| 32153575 | 10.1038/srep14802 | 10.3389/fimmu.2020.00244 | Pf Bacteriophage and Their Impact on Pseudomonas Virulence, Mammalian Immunity,  |
| 32156804 | 10.1073/pnas.1800650115 | 10.1128/mBio.00041-20 | More than Simple Parasites: the Sociobiology of Bacteriophages and Their Bacteri |
| 32164202 | 10.3201/eid2008.131399 | 10.3390/ijms21051883 | Bacteriophage-Insensitive Mutants of Antimicrobial-Resistant Salmonella Enterica |
| 32170178 | 10.1063/1.2018637 | 10.1038/s41467-020-15057-7 | An amber obligate active site-directed ligand evolution technique for phage disp |
| 32175286 | 10.1086/315239 | 10.3389/fcimb.2020.00062 | The Virulence of Escherichia coli O157:H7 Isolates in Mice Depends on Shiga Toxi |
| 32176482 | 10.1111/j.1600-079X.2007.00492.x | 10.1021/acschemneuro.9b00549 | Innovative IgG Biomarkers Based on Phage Display Microbial Amyloid Mimotope for  |
| 32178740 | 10.1086/423182 | 10.1186/s13756-020-00708-7 | Development of amoxicillin resistance in Escherichia coli after exposure to remn |
| 32185503 | 10.1186/s40945-017-0033-9.Using | 10.1007/164_2020_356 | Microbiome and Cardiovascular Disease. |
| 32190660 | 10.1002/cam4.1518 | 10.1155/2020/3415471 | Astragalus membranaceus-Derived Anti-Programmed Death-1 Monoclonal Antibodies wi |
| 32194532 | 10.1016/j.jcf.2018.03.007 | 10.3389/fmicb.2020.00327 | Development of a Bacteriophage Cocktail to Constrain the Emergence of Phage-Resi |
| 32203410 | 10.1093/nar/gkv094 | 10.1038/s41564-020-0691-3 | Bacterial alginate regulators and phage homologs repress CRISPR-Cas immunity. |
| 32212918 | 10.1128/mBio.02530-19 | 10.1080/22221751.2020.1747950 | Non-active antibiotic and bacteriophage synergism to successfully treat recurren |
| 32214384 | 10.1126/science.aat9691 | 10.1371/journal.ppat.1008318 | 5 challenges in understanding the role of the virome in health and disease. |
| 32218510 | 10.1002/ame2.12069 | 10.1038/s41564-020-0692-2 | Broad-spectrum anti-CRISPR proteins facilitate horizontal gene transfer. |
| 32218528 | 10.1073/pnas.1806660115 | 10.1038/s42003-020-0867-7 | Function-based high-throughput screening for antibody antagonists and agonists a |
| 32221310 | 10.7554/eLife.01456 | 10.1038/s41467-020-15363-0 | Synthetic antibodies against BRIL as universal fiducial marks for single-particl |
| 32222943 | 10.1038/ismej.2011.27 | 10.1007/s12275-020-9605-6 | Cryptic prophages in a blaNDM-1-bearing plasmid increase bacterial survival agai |
| 32227286 | 10.1038/ncomms4043 | 10.1007/s13770-020-00244-w | Engineered M13 Peptide Carrier Promotes Angiogenic Potential of Patient-Derived  |
| 32231271 | 10.1002/bit.25571 | 10.1038/s41565-020-0660-2 | Phage capsid nanoparticles with defined ligand arrangement block influenza virus |
| 32235304 | 10.1016/j.sbi.2016.06.003 | 10.3390/biom10040517 | A High-Throughput Single-Clone Phage Fluorescence Microwell Immunoassay and Lase |
| 32244369 | 10.1007/s00253-015-6867-8 | 10.3390/s20071953 | A Syringe-Based Biosensor to Rapidly Detect Low Levels of Escherichia Coli (ECOR |
| 32246126 | 10.1007/s00284-009-9430-y | 10.1038/s41598-020-62691-8 | Identification of a newly isolated lytic bacteriophage against K24 capsular type |
| 32249837 | 10.3389/fcimb.2012.00113 | 10.1038/s41598-020-63167-5 | Massive analysis of 64,628 bacterial genomes to decipher water reservoir and ori |
| 32252524 | 10.1016/S0022-0728(84)80324-1 | 10.1021/acs.analchem.0c00534 | Virus Bioresistor (VBR) for Detection of Bladder Cancer Marker DJ-1 in Urine at  |
| 32272740 | 10.1099/mic.0.000344 | 10.3390/v12040407 | The Application of Impedance Spectroscopy for Pseudomonas Biofilm Monitoring dur |
| 32280214 | 10.1002/cpt.v101.6 | 10.2147/IJN.S235058 | Preparation and Characterization of Anti-GPC3 Nanobody Against Hepatocellular Ca |
| 32285973 | 10.3109/17453679108994503 | 10.1002/jor.24689 | Therapeutics and delivery vehicles for local treatment of osteomyelitis. |
| 32286226 | 10.1038/s41467-019-10272-3 | 10.7554/eLife.55517 | Cryo-EM structure in situ reveals a molecular switch that safeguards virus again |
| 32290520 | 10.1371/journal.pone.0102600 | 10.3390/v12040435 | Phage-Mediated Molecular Detection (PMMD): A Novel Rapid Method for Phage-Specif |
| 32291303 | 10.1016/S0263-7855(97)00009-X | 10.1128/mBio.00603-20 | Global Trends in Proteome Remodeling of the Outer Membrane Modulate Antimicrobia |
| 32293244 | 10.1101/gr.229202 | 10.1186/s12864-020-6650-9 | Exploring the success of Brazilian endemic clone Pseudomonas aeruginosa ST277 an |
| 32295276 | 10.1074/jbc.M204467200 | 10.3390/v12040446 | "French Phage Network" Annual Conference-Fifth Meeting Report. |
| 32295868 | 10.1093/nar/gkw387 | 10.1128/mSphere.00056-20 | Emergence of a Novel Salmonella enterica Serotype Reading Clonal Group Is Linked |
| 32300857 | 10.1126/scitranslmed.3004916 | 10.1007/s00262-020-02564-1 | Characterization of an HLA-restricted and human cytomegalovirus-specific antibod |
| 32310742 | 10.1016/j.ijmm.2017.02.002 | 10.1099/jgv.0.001407 | Characterization and spontaneous induction of urinary tract Streptococcus angino |
| 32310947 | 10.1371/journal.pntd.0002049 | 10.1371/journal.pntd.0007642 | Genomic analysis of pathogenic isolates of Vibrio cholerae from eastern Democrat |
| 32314570 | 10.1021/nn305930e | 10.1021/acssensors.0c00654 | Chimeric Phage Nanoparticles for Rapid Characterization of Bacterial Pathogens:  |
| 32317653 | 10.1111/j.1365-2672.2010.04664.x | 10.1038/s41598-020-63432-7 | Unravelling the consequences of the bacteriophages in human samples. |
| 32325677 | 10.1186/1742-4690-6-90 | 10.3390/biom10040628 | Diverse Functions of Polyamines in Virus Infection. |
| 32325706 | 10.12968/jowc.2009.18.6.42801 | 10.3390/cells9041013 | Phages and Their Role in Gastrointestinal Disease: Focus on Inflammatory Bowel D |
| 32325896 | 10.1007/BF02756201 | 10.3390/v12040461 | Survival of Human Norovirus Surrogates in Water upon Exposure to Thermal and Non |
| 32328467 | 10.1016/j.jaut.2016.03.001 | 10.3389/fcimb.2020.00131 | Dysbiosis in Peripheral Blood Mononuclear Cell Virome Associated With Systemic L |
| 32328641 | 10.1242/jcs.220814 | 10.1083/jcb.201909178 | A direct role for SNX9 in the biogenesis of filopodia. |
| 32339190 | 10.1134/S0006297915020042 | 10.1371/journal.pone.0230090 | Structure and conformational cycle of a bacteriophage-encoded chaperonin. |
| 32350467 | 10.1128/aac.01479-07 | 10.1038/s41586-020-2186-z | Action of a minimal contractile bactericidal nanomachine. |
| 32351494 | 10.1093/jac/33.5.959 | 10.3389/fmicb.2020.00695 | Using Bacteriophages as a Trojan Horse to the Killing of Dual-Species Biofilm Fo |
| 32353007 | 10.1016/j.watres.2018.06.057 | 10.1371/journal.pone.0232289 | Prevalence and seasonal dynamics of blaCTX-M antibiotic resistance genes and fec |
| 32357999 | 10.1084/jem.20030857 | 10.1128/AEM.00073-20 | A Tailspike with Exopolysaccharide Depolymerase Activity from a New Providencia  |
| 32358533 | 10.1111/mmi.13006 | 10.1038/s41396-020-0664-9 | Hitchhiking, collapse, and contingency in phage infections of migrating bacteria |
| 32375972 | 10.1128/AEM.02229-13 | 10.1099/mgen.0.000369 | Genomic analysis of 40 prophages located in the genomes of 16 carbapenemase-prod |
| 32376832 | 10.1016/j.ygeno.2018.08.008 | 10.1038/s41598-020-63048-x | Isolation, Characterization and Genomic Analysis of a Novel Bacteriophage VB_Eco |
| 32377714 | 10.1016/j.bmc.2017.06.052 | 10.3892/mmr.2020.11128 | Heptapeptide HP3 acts as a potent inhibitor of experimental imiquimod‑induced mu |
| 32380649 | 10.1371/journal.pcbi.1000138 | 10.3390/biom10050714 | Phage Display Selection, Identification, and Characterization of Novel Pancreati |
| 32380650 | 10.1074/jbc.M111.323311 | 10.3390/ijms21093258 | Novel Antibodies Targeting MUC1-C Showed Anti-Metastasis and Growth-Inhibitory E |
| 32380707 | 10.1080/21597081.2016.1251379 | 10.3390/antibiotics9050232 | Bacteriophage Therapy for Critical Infections Related to Cardiothoracic Surgery. |
| 32392794 | 10.1016/j.bbagen.2018.07.029 | 10.3390/s20092667 | Advanced Methods for Detection of Bacillus cereus and Its Pathogenic Factors. |
| 32393490 | 10.1186/1471-2180-11-258 | 10.1128/AAC.00461-20 | Bacteriophage-Antibiotic Combination Strategy: an Alternative against Methicilli |
| 32393891 | 10.1016/j.ymeth.2012.12.008 | 10.1038/s41551-020-0556-3 | De novo development of proteolytically resistant therapeutic peptides for oral a |
| 32410729 | 10.1007/BF02048548 | 10.7554/eLife.55053 | Identification of novel, clinically correlated autoantigens in the monogenic aut |
| 32413276 | 10.1126/science.abb7269 | 10.1016/j.chom.2020.04.023 | Identification of Human Single-Domain Antibodies against SARS-CoV-2. |
| 32418663 | 10.1002/ppap.201900269 | 10.1016/j.tibtech.2020.04.003 | Cold Plasma, a New Hope in the Field of Virus Inactivation. |
| 32422119 | 10.3390/v10010005 | 10.1016/j.bjid.2020.04.010 | Clinical utilization of bacteriophages: a new perspective to combat the antimicr |
| 32442222 | 10.1111/1751-7915.12334 | 10.1371/journal.pone.0233557 | The intestinal virome in children with cystic fibrosis differs from healthy cont |
| 32443619 | 10.1111/j.1365-2672.2005.02659.x | 10.3390/v12050559 | Efficacy of Lytic Phage Cocktails on Staphylococcus aureus and Pseudomonas aerug |
| 32454153 | 10.1103/physrevlett.78.2477 | 10.1016/j.jmb.2020.05.016 | Phage G Structure at 6.1 Å Resolution, Condensed DNA, and Host Identity Revision |
| 32456083 | 10.1093/nar/gkn179 | 10.3390/v12050573 | First crAss-Like Phage Genome Encoding the Diversity-Generating Retroelement (DG |
| 32459982 | 10.1016/j.cell.2019.01.001 | 10.1080/19490976.2020.1752605 | Metagenomics reveals impact of geography and acute diarrheal disease on the Cent |
| 32461312 | 10.1016/j.gde.2005.09.006 | 10.1128/JVI.00953-20 | The Concerted Action of Two B3-Like Prophage Genes Excludes Superinfecting Bacte |
| 32461640 | 10.1186/1742-4690-9-23 | 10.1038/s41586-020-2192-1 | The stepwise assembly of the neonatal virome is modulated by breastfeeding. |
| 32466194 | 10.3390/v10110622 | 10.3390/ijms21103715 | Animal Models to Translate Phage Therapy to Human Medicine. |
| 32467564 | 10.1038/nm.2554 | 10.1038/s41392-020-0183-1 | Identification and characterization of mammaglobin-A epitope in heterogenous bre |
| 32471182 | 10.1002/path.1999 | 10.3390/biom10060820 | An Isoform of the Oncogenic Splice Variant AIMP2-DX2 Detected by a Novel Monoclo |
| 32476604 | 10.1016/j.bbrc.2020.01.057 | 10.1080/15476286.2020.1761639 | The large family of PC4-like domains - similar folds and functions throughout al |
| 32483301 | 10.1016/j.tips.2018.12.005 | 10.1038/s41375-020-0885-y | Detection of chronic lymphocytic leukemia subpopulations in peripheral blood by  |
| 32486377 | 10.1093/molbev/mss279 | 10.3390/v12060601 | A Novel Inducible Prophage from Burkholderia Vietnamiensis G4 is Widely Distribu |
| 32487750 | 10.1146/annurev.ge.14.120180.002151 | 10.1074/jbc.RA120.014465 | Spontaneous and photosensitization-induced mutations in primary mouse cells tran |
| 32496181 | 10.1038/s41588-018-0184-y | 10.1099/mgen.0.000376 | Assessing the genomic relatedness and evolutionary rates of persistent verotoxig |
| 32511090 | 10.1017/S095026881600176X | 10.3201/eid2608.200346 | CrAssphage as a Novel Tool to Detect Human Fecal Contamination on Environmental  |
| 32512271 | 10.1016/j.jviromet.2005.04.015 | 10.1016/j.intimp.2020.106654 | An approach towards development of monoclonal IgY antibodies against SARS CoV-2  |
| 32522236 | 10.3389/fgene.2018.00304/full | 10.1186/s40168-020-00867-0 | VIBRANT: automated recovery, annotation and curation of microbial viruses, and e |
| 32522608 | 10.1093/infdis/jiaa114 | 10.1016/j.ajic.2020.06.002 | Evaluation of an electrostatic spray disinfectant technology for rapid decontami |
| 32523333 | 10.1016/S0022-5193(03)00262-5 | 10.2147/DDDT.S251171 | Bacteriophages, a New Therapeutic Solution for Inhibiting Multidrug-Resistant Ba |
| 32525961 | 10.1073/pnas.061038398 | 10.1371/journal.pone.0234159 | Introducing Lu-1, a Novel Lactobacillus jensenii Phage Abundant in the Urogenita |
| 32533007 | 10.1093/nar/gkv1290 | 10.1038/s41598-020-66214-3 | Increasing incidence of group B streptococcus neonatal infections in the Netherl |
| 32533350 | 10.1007/s12591-016-0303-0 | 10.1007/s11538-020-00751-w | Optimizing the Timing and Composition of Therapeutic Phage Cocktails: A Control- |
| 32545159 | 10.1128/CMR.00109-13 | 10.3390/v12060631 | Development and Evaluation of a Sensitive Bacteriophage-Based MRSA Diagnostic Sc |
| 32546616 | 10.1136/annrheumdis-2018-214856 | 10.1128/mBio.00460-20 | Convergent Evolution of Neutralizing Antibodies to Staphylococcus aureus γ-Hemol |
| 32570896 | 10.1128/AAC.45.3.649-659.2001 | 10.3390/antibiotics9060339 | The Basis for Natural Multiresistance to Phage in Pseudomonas aeruginosa. |
| 32571816 | 10.1093/jac/dku113 | 10.1128/AAC.00993-20 | Bacteriophage-Antibiotic Combinations for Enterococcus faecium with Varying Bact |
| 32574158 | 10.1016/S2214-109X(18)30351-6 | 10.1371/journal.pntd.0008387 | Growth velocity in children with Environmental Enteric Dysfunction is associated |
| 32574197 | 10.3390/antibiotics7010013 | 10.1371/journal.pone.0235002 | Host range, morphological and genomic characterisation of bacteriophages with ac |
| 32575645 | 10.1093/bioinformatics/btq484 | 10.3390/ijms21124390 | Antibiotics Act with vB_AbaP_AGC01 Phage against Acinetobacter baumannii in Huma |
| 32578012 | 10.1021/es3028764 | 10.1007/s12560-020-09431-3 | Evaluation of Viral Recovery Methodologies from Solid Waste Landfill Leachate. |
| 32579599 | 10.1038/sj.mt.6300399 | 10.1371/journal.pone.0235127 | Repeat induces not only gene silencing, but also gene activation in mammalian ce |
| 32587063 | 10.15585/mmwr.mm6915e6 | 10.1128/mBio.00997-20 | Microwave-Generated Steam Decontamination of N95 Respirators Utilizing Universal |
| 32591388 | 10.1155/2011/734690 | 10.1128/AEM.01482-20 | Persistence of Bacteriophage Phi 6 on Porous and Nonporous Surfaces and the Pote |
| 32601452 | 10.1093/bioinformatics/btp616 | 10.1038/s41564-020-0746-5 | Phase-variable capsular polysaccharides and lipoproteins modify bacteriophage su |
| 32611695 | 10.1128/mSphere.00612-17 | 10.1128/mSphere.00226-20 | Evolution and Population Dynamics of Clonal Complex 152 Community-Associated Met |
| 32611794 | 10.1016/S2589-7500(20)30062-5 | 10.1128/JCM.00412-20 | Gold Standard Cholera Diagnostics Are Tarnished by Lytic Bacteriophage and Antib |
| 32612183 | 10.3109/1547691X.2012.703253 | 10.1038/s41598-020-67654-7 | An in vitro methodology for discovering broadly-neutralizing monoclonal antibodi |
| 32612960 | 10.1038/s41598-017-08530-9 | 10.3389/fcimb.2020.00276 | Differences in Compositions of Gut Bacterial Populations and Bacteriophages in 5 |
| 32629918 | 10.1016/j.ijfoodmicro.2014.09.011 | 10.3390/ijms21134653 | Metabolic Shift of an Isogenic Strain of Enterococcus faecalis 14, Deficient in  |
| 32630402 | 10.1016/S0169-409X(00)00131-9 | 10.3390/biom10060955 | Rapid Evaluation of Antibody Fragment Endocytosis for Antibody Fragment-Drug Con |
| 32630442 | 10.1177/1087057114560123 | 10.3390/v12060684 | BLI-Based Functional Assay in Phage Display Benefits the Development of a PD-L1- |
| 32635178 | 10.1016/j.virol.2009.11.043 | 10.3390/v12070721 | Pseudomonas Phage PaBG-A Jumbo Member of an Old Parasite Family. |
| 32636253 | 10.1038/35054089 | 10.1128/mBio.01470-20 | Probiotic Properties of Escherichia coli Nissle in Human Intestinal Organoids. |
| 32640188 | 10.1101/2020.03.12.988782 | 10.1016/j.chembiol.2020.06.010 | Illuminating RNA Biology: Tools for Imaging RNA in Live Mammalian Cells. |
| 32652063 | 10.1186/1471-2105-14-19 | 10.1016/j.chom.2020.06.011 | Bacteroides thetaiotaomicron-Infecting Bacteriophage Isolates Inform Sequence-Ba |
| 32652484 | 10.1038/s41564-019-0634-z | 10.1016/j.mib.2020.06.003 | Molecular mechanisms of enterococcal-bacteriophage interactions and implications |
| 32654263 | 10.1002/hep.31178 | 10.1002/hep.31459 | Intestinal Virome in Patients With Alcoholic Hepatitis. |
| 32655502 | 10.2217/fmb.15.48 | 10.3389/fmicb.2020.00947 | Molecular Characterization and Comparative Genomic Analysis of vB_PaeP_YA3, a No |
| 32657966 | 10.1128/aac.00954-17 | 10.1097/QCO.0000000000000658 | Bacteriophage therapy as a treatment option for transplant infections. |
| 32658245 | 10.1128/ecosalplus.ESP-0003 | 10.1093/gbe/evaa146 | Two Lineages of Pseudomonas aeruginosa Filamentous Phages: Structural Uniformity |
| 32664292 | 10.3390/v10020064 | 10.3390/v12070743 | Phages Needed against Resistant Bacteria. |
| 32668759 | 10.1186/1756-0500-5-63 | 10.3390/ijms21144943 | Development of a Single Construct System for Site-Directed RNA Editing Using MS2 |
| 32678145 | 10.1186/1471-2105-9-376 | 10.1038/s41598-020-68462-9 | Global distribution of epidemic-related Shiga toxin 2 encoding phages among ente |
| 32694655 | 10.1093/bioinformatics/btp033 | 10.1038/s41598-020-68983-3 | Exploiting phage receptor binding proteins to enable endolysins to kill Gram-neg |
| 32699879 | 10.1093/cid/ciy947 | 10.1093/cid/ciaa705 | Phage Therapy for Limb-threatening Prosthetic Knee Klebsiella pneumoniae Infecti |
| 32708112 | 10.3389/fimmu.2018.03004 | 10.3390/ijms21145145 | COVID-19: A Review on Diagnosis, Treatment, and Prophylaxis. |
| 32709718 | 10.1016/j.mimet.2015.09.022 | 10.1128/AEM.01311-20 | Lysin LysMK34 of Acinetobacter baumannii Bacteriophage PMK34 Has a Turgor Pressu |
| 32710406 | 10.1186/gb-2006-7-10-r100 | 10.1007/978-1-0716-0712-1_7 | New Generations of MS2 Variants and MCP Fusions to Detect Single mRNAs in Living |
| 32727031 | 10.1093/nar/gkt1113 | 10.3390/cells9081786 | AcrIIA5 Suppresses Base Editors and Reduces Their Off-Target Effects. |
| 32727845 | 10.1177/1010428317695924 | 10.1074/jbc.AC120.014918 | Identification of an anti-SARS-CoV-2 receptor-binding domain-directed human mono |
| 32727858 | 10.1186/1471-2105-11-595 | 10.1128/mSphere.00404-20 | Acinetobacter baumannii NCIMB8209: a Rare Environmental Strain Displaying Extens |
| 32728257 | 10.3389/fmicb.2019.02537 | 10.1038/d41586-020-02109-7 | Bacteria-eating viruses could provide a route to stability in cystic fibrosis. |
| 32737386 | 10.1080/07391102.2019.1677504 | 10.1038/s41598-020-69515-9 | Peptides targeting dengue viral nonstructural protein 1 inhibit dengue virus pro |
| 32753497 | 10.1006/jmcc.1998.0655 | 10.1128/mBio.01462-20 | Phage-Antibiotic Synergy Is Driven by a Unique Combination of Antibacterial Mech |
| 32753678 | 10.1080/2162402X.2016.1165376 | 10.1038/s41416-020-1017-1 | Development of an artificial antibody specific for HLA/peptide complex derived f |
| 32756438 | 10.1007/s13201-019-0959-z | 10.3390/v12080845 | Recent Progress in the Detection of Bacteria Using Bacteriophages: A Review. |
| 32770098 | 10.1080/10618600.1996.10474713 | 10.1038/s41598-020-70135-6 | A panel of anti-influenza virus nucleoprotein antibodies selected from phage-dis |
| 32776637 | 10.1212/WNL.0000000000009183 | 10.15252/emmm.202012739 | Protective anti-prion antibodies in human immunoglobulin repertoires. |
| 32778162 | 10.1021/acs.chemrev.6b00799 | 10.1186/s13756-020-00795-6 | CRISPR-Cas system: a potential alternative tool to cope antibiotic resistance. |
| 32788409 | 10.12688/wellcomeopenres.14826.1 | 10.1128/mSystems.00659-20 | Computational Basis for On-Demand Production of Diversified Therapeutic Phage Co |
| 32792334 | 10.3389/fmicb.2019.02162 | 10.1128/MMBR.00026-19 | Staphylococcal Biofilm Development: Structure, Regulation, and Treatment Strateg |
| 32792590 | 10.1101/310961 | 10.1038/s41598-020-70581-2 | Transcriptomic determinants of the response of ST-111 Pseudomonas aeruginosa AG1 |
| 32798603 | 10.1093/nar/gkv367 | 10.1016/j.antiviral.2020.104916 | Enzymatically synthesized 2'-fluoro-modified Dicer-substrate siRNA swarms agains |
| 32807206 | 10.2200/S00240ED1V01Y200912DMK002 | 10.1186/s12985-020-01394-y | Characterization of integrated prophages within diverse species of clinical nont |
| 32808238 | 10.1016/j.brainres.2015.05.011 | 10.1007/s11481-020-09948-1 | Antibodies from Multiple Sclerosis Brain Identified Epstein-Barr Virus Nuclear A |
| 32814789 | 10.1109/MCSE.2007.55 | 10.1038/s41598-020-70841-1 | Optimizing bacteriophage engineering through an accelerated evolution platform. |
| 32817337 | 10.1093/nar/gky1106 | 10.1074/jbc.RA120.012893 | Generation and validation of recombinant antibodies to study human aminoacyl-tRN |
| 32824480 | 10.1016/j.lwt.2018.01.033 | 10.3390/nu12082474 | PHAGE-2 Study: Supplemental Bacteriophages Extend Bifidobacterium animalis subsp |
| 32825391 | 10.3109/03008207.2014.923868 | 10.3390/ijms21175994 | Phage Display to Augment Biomaterial Function. |
| 32839842 | 10.1007/s00198-010-1501-1 | 10.1007/s00223-020-00746-8 | Recombinant Antibodies with Unique Specificities Allow for Sensitive and Specifi |
| 32841606 | 10.2307/1943563 | 10.1016/j.chom.2020.08.003 | The Gut Virome Database Reveals Age-Dependent Patterns of Virome Diversity in th |
| 32848007 | 10.1016/j.mimet.2008.06.010 | 10.1128/mSphere.00748-20 | Antibiotic Resistance in Vibrio cholerae: Mechanistic Insights from IncC Plasmid |
| 32855401 | 10.1016/j.jviromet.2005.05.027 | 10.1038/s41467-020-18159-4 | A panel of human neutralizing mAbs targeting SARS-CoV-2 spike at multiple epitop |
| 32864566 | 10.1111/evo.12652 | 10.1099/acmi.0.000002 | Characterization of the ϕCTX-like Pseudomonas aeruginosa phage Dobby isolated fr |
| 32866189 | 10.1038/s41586-019-0934-8 | 10.1371/journal.ppat.1008793 | Distinct disease features in chimpanzees infected with a precore HBV mutant asso |
| 32872428 | 10.1007/s10517-016-3434-y | 10.3390/ijms21176258 | Exhaustive Search of the Receptor Ligands by the CyCLOPS (Cytometry Cell-Labelin |
| 32876069 | 10.1016/j.bbadis.2003.08.004 | 10.4014/jmb.2005.05046 | Generation and Characterization of Monoclonal Antibodies to the Ogawa Lipopolysa |
| 32880207 | 10.1021/jm050540c | 10.1080/19420862.2020.1801230 | Structural and functional characterization of C0021158, a high-affinity monoclon |
| 32882851 | 10.1101/gr.1239303 | 10.3390/ijms21176338 | Isolation and Characterization of the Novel Bacteriophage AXL3 against Stenotrop |
| 32883029 | 10.1038/s41388-018-0391-0 | 10.3390/ijms21176354 | Selection and Characterization of YKL-40-Targeting Monoclonal Antibodies from Hu |
| 32886694 | 10.1186/1475-2859-13-S1-S3 | 10.1371/journal.pone.0238390 | Whole-genome sequence of multi-drug resistant Pseudomonas aeruginosa strains UY1 |
| 32887488 | 10.1038/s41594-019-0206-1 | 10.3390/v12090976 | The Phage-Encoded N-Acetyltransferase Rac Mediates Inactivation of Pseudomonas a |
| 32887544 | 10.1016/j.celrep.2013.06.007 | 10.1186/s12868-020-00586-0 | Isolation and characterization of antibody fragments selective for human FTD bra |
| 32899396 | 10.1017/S0950268810001093 | 10.3390/genes11091042 | Newly Emerged Serotype 1c of Shigella flexneri: Multiple Origins and Changing Dr |
| 32900827 | 10.1111/j.1365-2958.1990.tb02040.x | 10.1128/JB.00411-20 | Nanoluciferase Reporter Mycobacteriophage for Sensitive and Rapid Detection of M |
| 32901128 | 10.1101/020891v1.full | 10.1038/s41423-020-00532-4 | Phages and their potential to modulate the microbiome and immunity. |
| 32901894 | 10.5483/BMBRep.2017.50.2.011 | 10.3892/mmr.2020.11500 | Human monoclonal anti‑TLR4 antibody negatively regulates lipopolysaccharide‑indu |
| 32914796 | 10.1039/B207853H | 10.1039/d0bm01219j | The unique potency of Cowpea mosaic virus (CPMV) in situ cancer vaccine. |
| 32923408 | 10.1111/j.1574-695X.2000.tb01516.x | 10.3389/fcimb.2020.00414 | Proteus mirabilis Biofilm: Development and Therapeutic Strategies. |
| 32927825 | 10.3390/molecules25040843 | 10.3390/molecules25184148 | Special Issue "Recent Advances in Precision Nanomedicine for Cancer". |
| 32941607 | 10.1101/094672 | 10.1093/nar/gkaa735 | Detection of preQ0 deazaguanine modifications in bacteriophage CAjan DNA using N |
| 32941803 | 10.1101/2020.04.10.036418 | 10.1016/j.cell.2020.09.007 | High Potency of a Bivalent Human VH Domain in SARS-CoV-2 Animal Models. |
| 32948001 | 10.1128/AAC.00954-17 | 10.3390/ijms21186793 | Alternative and Experimental Therapies of Mycobacterium abscessus Infections. |
| 32954791 | 10.1128/mBio.00722-20 | 10.5144/0256-4947.2020.373 | Automated SARS-COV-2 RNA extraction from patient nasopharyngeal samples using a  |
| 32957679 | 10.1038/s41467-018-07225-7 | 10.3390/v12091035 | Evolutionary Study of the Crassphage Virus at Gene Level. |
| 32958861 | 10.1371/journal.pone.0202054 | 10.1038/s41598-020-71791-4 | Metagenomic sequencing of stool samples in Bangladeshi infants: virome associati |
| 32966645 | 10.1056/NEJMoa2001191 | 10.1002/jmv.26540 | One-step quantitative RT-PCR assay with armored RNA controls for detection of SA |
| 32968007 | 10.1017/S0950268818002704 | 10.1128/mSphere.00654-20 | Antibodies to Variable Domain 4 Linear Epitopes of the Chlamydia trachomatis Maj |
| 32969787 | 10.1186/s12864-019-5674-5 | 10.1099/mgen.0.000440 | Exploration into the origins and mobilization of di-hydrofolate reductase genes  |
| 32971846 | 10.1016/j.jmb.2015.09.014 | 10.3390/ijms21186953 | Blocking of the IL-33/ST2 Signaling Axis by a Single-Chain Antibody Variable Fra |
| 32973096 | 10.1101/502187 | 10.1073/pnas.2009279117 | Deep profiling of protease substrate specificity enabled by dual random and scan |
| 32980676 | 10.1128/JVI.75.22.10892-10905 | 10.1016/j.virol.2020.06.016 | Selection and immune recognition of HIV-1 MPER mimotopes. |
| 32983005 | 10.1128/iai.73.11.7151-7160.2005 | 10.3389/fmicb.2020.01947 | Combined Bacteriophage and Antibiotic Treatment Prevents Pseudomonas aeruginosa  |
| 32983137 | 10.1186/s12929-019-0592-z | 10.3389/fimmu.2020.01986 | Phage Display Derived Monoclonal Antibodies: From Bench to Bedside. |
| 32983155 | 10.3390/antib9020012 | 10.3389/fimmu.2020.02067 | Structural Aspects of the Allergen-Antibody Interaction. |
| 32985020 | 10.1128/mSystems.00190-16 | 10.1111/mmi.14614 | A recently isolated human commensal Escherichia coli ST10 clone member mediates  |
| 32985336 | 10.1007/s00253-013-5128-y | 10.1080/19490976.2020.1813533 | Bacteriophage endolysins as a potential weapon to combat Clostridioides difficil |
| 32989087 | 10.1128/IAI.48.1.124-129.1985 | 10.1128/JB.00363-20 | Influence of Shigella flexneri 2a O Antigen Acetylation on Its Bacteriophage Sf6 |
| 32993643 | 10.1016/j.jviromet.2017.02.003 | 10.1186/s12917-020-02572-4 | Development of a double-recombinant antibody sandwich ELISA for quantitative det |
| 32993724 | 10.1007/s00705-014-2114-3 | 10.1186/s12985-020-01410-1 | Viruses of protozoan parasites and viral therapy: Is the time now right? |
| 32994538 | 10.1128/AEM.03242-13 | 10.1038/s10038-020-00841-6 | Identification of ancient viruses from metagenomic data of the Jomon people. |
| 32995758 | 10.1101/285916 | 10.1016/j.xcrm.2020.100123 | ReScan, a Multiplex Diagnostic Pipeline, Pans Human Sera for SARS-CoV-2 Antigens |
| 32995957 | 10.1111/cas.12167 | 10.1007/s00430-020-00694-y | Elevated plasma phage load as a marker for intestinal permeability in leukemic p |
| 32998720 | 10.1128/mBio.00362-12 | 10.1186/s12941-020-00389-5 | Bacteriophage therapy against Pseudomonas aeruginosa biofilms: a review. |
| 33008118 | 10.1371/journal.pntd.0002451 | 10.3390/v12101114 | Expansion and Refinement of Deep Sequence-Coupled Biopanning Technology for Epit |
| 33011743 | 10.1101/2020.02.05.935965v2 | 10.1038/s41396-020-00794-w | Phage gene expression and host responses lead to infection-dependent costs of CR |
| 33014897 | 10.1136/gutjnl-2018-318131 | 10.3389/fcimb.2020.00481 | Shining Light on Human Gut Bacteriophages. |
| 33020240 | 10.1038/nrclinonc.2016.211 | 10.1136/jitc-2020-000905 | CD47/SIRPα blocking peptide identification and synergistic effect with irradiati |
| 33022253 | 10.1101/2020.02.15.951020 | 10.1016/j.cub.2020.07.036 | Trading-off and trading-up in the world of bacteria-phage evolution. |
| 33024089 | 10.1111/j.1462-5822.2005.00525.x | 10.1038/s41467-020-18700-5 | Prophage exotoxins enhance colonization fitness in epidemic scarlet fever-causin |
| 33040749 | 10.1101/2020.04.07.20057224 | 10.1017/ice.2020.1257 | Scalable in-hospital decontamination of N95 filtering face-piece respirator with |
| 33049935 | 10.3390/v11030295 | 10.3390/v12101138 | Characterization of Novel Lytic Bacteriophages of Achromobacter marplantensis Is |
| 33050261 | 10.3390/v11070587 | 10.3390/v12101143 | Characterization of the Vaginal DNA Virome in Health and Dysbiosis. |
| 33050521 | 10.1128/AAC.01106-08 | 10.3390/ph13100299 | The Principles, Mechanisms, and Benefits of Unconventional Agents in the Treatme |
| 33055250 | 10.1016/S1359-0278(98)00044-3 | 10.1128/JVI.01495-20 | High-Resolution Mapping of Human Norovirus Antigens via Genomic Phage Display Li |
| 33064268 | 10.1016/j.ygeno.2010.06.001 | 10.1007/s12223-020-00775-8 | Biological characteristics and genome analysis of a novel phage vB_KpnP_IME279 i |
| 33072116 | 10.1002/ijc.10514 | 10.3389/fimmu.2020.573823 | Intercellular Adhesion Molecule-1 as Target for CAR-T-Cell Therapy of Triple-Neg |
| 33077648 | 10.1128/AAC.00461-20 | 10.1128/AAC.01863-20 | Bacteriophage AB-SA01 Cocktail in Combination with Antibiotics against MRSA-VISA |
| 33077657 | 10.3791/61469 | 10.1128/AAC.01470-20 | Pharmacokinetics and Time-Kill Study of Inhaled Antipseudomonal Bacteriophage Th |
| 33079052 | 10.1093/infdis/jiy597 | 10.3201/eid2611.201442 | Phage-Mediated Immune Evasion and Transmission of Livestock-Associated Methicill |
| 33081350 | 10.1073/pnas.1208507109 | 10.3390/v12101172 | Viral Related Tools against SARS-CoV-2. |
| 33082473 | 10.1080/19420862.2018.1553476 | 10.1038/s41598-020-74761-y | Development of humanized tri-specific nanobodies with potent neutralization for  |
| 33082574 | 10.1101/2019.12.15.877092 | 10.1038/s41589-020-00679-1 | Bi-paratopic and multivalent VH domains block ACE2 binding and neutralize SARS-C |
| 33084973 | 10.1002/anie.201506225 | 10.1007/s00280-020-04167-0 | The biologically functional identification of a novel TIM3-binding peptide P26 i |
| 33087392 | 10.1093/annhyg/mev005 | 10.1136/bmjgh-2020-003110 | Reusability of filtering facepiece respirators after decontamination through dry |
| 33096802 | 10.1038/21918 | 10.3390/v12101197 | Maturation of Pseudo-Nucleus Compartment in P. aeruginosa, Infected with Giant p |
| 33101229 | 10.1093/nar/gkr485 | 10.3389/fmicb.2020.556706 | Temperate Bacteriophages (Prophages) in Pseudomonas aeruginosa Isolates Belongin |
| 33109704 | 10.26434/chemrxiv.12116943.v12116941 | 10.1074/mcp.RA120.002314 | Antibody Binding Epitope Mapping (AbMap) of Hundred Antibodies in a Single Run. |
| 33114050 | 10.1158/0008-5472.CAN-05-4441 | 10.3390/ijms21217867 | Doxorubicin Improves Cancer Cell Targeting by Filamentous Phage Gene Delivery Ve |
| 33117380 | 10.1126/science.1099191 | 10.3389/fimmu.2020.577815 | Selection of a Single Domain Antibody, Specific for an HLA-Bound Epitope of the  |
| 33118486 | 10.1007/s00253-004-1585-7 | 10.1128/ecosalplus.ESP-0029-2019 | Bacteriophage Infections of Biofilms of Health Care-Associated Pathogens: Klebsi |
| 33122703 | 10.1371/journal.pone.0127606 | 10.1038/s41598-020-75637-x | Contribution of Podoviridae and Myoviridae bacteriophages to the effectiveness o |
| 33123112 | 10.1001/jamainternmed.2013.9763 | 10.3389/fmicb.2020.580779 | Identification and Characterization of New Bacteriophages to Control Multidrug-R |
| 33125119 | 10.1016/j.humpath.2008.11.001 | 10.3892/or.2020.7792 | Diverse molecular functions of aspartate β‑hydroxylase in cancer (Review). |
| 33126265 | 10.3389/fmicb.2018.01832 | 10.1007/s12223-020-00835-z | Anti-phage serum antibody responses and the outcome of phage therapy. |
| 33131851 | 10.1021/acs.est.6b00876 | 10.1016/j.scitotenv.2020.143067 | Applicability of polyethylene glycol precipitation followed by acid guanidinium  |
| 33136526 | 10.1158/1078-0432.CCR-17-1766 | 10.1080/19420862.2020.1836713 | Novel human monoclonal antibodies specific to the alternatively spliced domain D |
| 33139482 | 10.1111/mmi.12451 | 10.1128/JB.00406-20 | Phage Proteins Required for Tail Fiber Assembly Also Bind Specifically to the Su |
| 33139569 | 10.1101/2020.05.06.081497 | 10.1073/pnas.2010197117 | Rapid identification of a human antibody with high prophylactic and therapeutic  |
| 33143386 | 10.1016/j.femsle.2005.09.029 | 10.3390/microorganisms8111700 | Activation of the Cell Wall Stress Response in Pseudomonas aeruginosa Infected b |
| 33161737 | 10.1002/bip.22705 | 10.3920/BM2020.0039 | Bacillus subtilis DE111 intake may improve blood lipids and endothelial function |
| 33162982 | 10.1002/prot.25215 | 10.3389/fimmu.2020.566710 | A Direct Role for the CD1b Endogenous Spacer in the Recognition of a Mycobacteri |
| 33164326 | 10.1016/s0140-6736(20)31208-3 | 10.1002/wnan.1681 | Advancements in protein nanoparticle vaccine platforms to combat infectious dise |
| 33166282 | 10.3390/toxins11060350 | 10.1371/journal.pone.0236538 | Sites of vulnerability on ricin B chain revealed through epitope mapping of toxi |
| 33170117 | 10.1016/j.mimet.2005.03.018 | 10.1099/mgen.0.000474 | Epigenomics, genomics, resistome, mobilome, virulome and evolutionary phylogenom |
| 33174903 | 10.1186/s12864-016-2883-z | 10.1590/0074-02760200370 | Detection of Bacillus anthracis and Bacillus anthracis-like spores in soil from  |
| 33177196 | 10.1016/j.mimet.2005.06.001 | 10.1128/JVI.01643-20 | cDNA-Derived RNA Phage Assembly Reveals Critical Residues in the Maturation Prot |
| 33194818 | 10.1136/gutjnl-2017-313952 | 10.3389/fcimb.2020.582187 | Virome Sequencing of the Human Intestinal Mucosal-Luminal Interface. |
| 33198306 | 10.3389/fimmu.2018.02315 | 10.3390/ijms21228527 | Emerging Strategies to Combat β-Lactamase Producing ESKAPE Pathogens. |
| 33198413 | 10.1002/elps.1150090603 | 10.3390/ijms21228546 | Extended Cleavage Specificity of the Rat Vascular Chymase, a Potential Blood Pre |
| 33206590 | 10.1093/oxfordjournals.aje.a118408 | 10.1080/19420862.2020.1843754 | Selection and verification of antibodies against the cytoplasmic domain of M2 of |
| 33217933 | 10.1128/JCM.01949-17 | 10.3390/v12111323 | Characterization of Clinical and Carrier Streptococcus agalactiae and Prophage C |
| 33218076 | 10.1038/nrmicro2577 | 10.3390/genes11111365 | CRISPR-Cas Diversity in Clinical Salmonella enterica Serovar Typhi Isolates from |
| 33238548 | 10.1128/AEM.01311-20 | 10.3390/v12111340 | LysSAP26, a New Recombinant Phage Endolysin with a Broad Spectrum Antibacterial  |
| 33246946 | 10.1038/ni.1864 | 10.1126/sciimmunol.abc0217 | Shiga toxin suppresses noncanonical inflammasome responses to cytosolic LPS. |
| 33260527 | 10.1016/j.tig.2017.07.011 | 10.3390/cells9122555 | A Singular and Widespread Group of Mobile Genetic Elements: RNA Circles with Aut |
| 33261041 | 10.1093/nar/gkv1100 | 10.3390/v12121360 | Application of Next Generation Sequencing (NGS) in Phage Displayed Peptide Selec |
| 33262768 | 10.1016/j.bcp.2011.09.024 | 10.3389/fimmu.2020.587825 | Discovery of a Recombinant Human Monoclonal Immunoglobulin G Antibody Against α- |
| 33281824 | 10.1002/biot.201500458 | 10.3389/fimmu.2020.595970 | Development of Patient-Derived Human Monoclonal Antibodies Against Nucleocapsid  |
| 33291078 | 10.1161/RES.0000000000000104 | 10.18632/aging.104130 | Multiwalled carbon nanotubes inhibit cell migration and invasion by destroying a |
| 33291831 | 10.1371/journal.pgen.1002414 | 10.3390/v12121393 | The State of the Art in Biodefense Related Bacterial Pathogen Detection Using Ba |
| 33298522 | 10.1002/alz.12213 | 10.1074/jbc.RA120.015501 | An "epitomic" analysis of the specificity of conformation-dependent, anti-Aß amy |
| 33299101 | 10.1038/s41598-018-25411-x | 10.1038/s41598-020-78622-6 | Phage lysin that specifically eliminates Clostridium botulinum Group I cells. |
| 33301112 | 10.1016/j.jsb.2018.03.004 | 10.1007/978-1-0716-1126-5_4 | Validation of the Production of Antibodies in Different Formats in the HEK 293 T |
| 33301114 | 10.1126/scisignal.aan0868 | 10.1007/978-1-0716-1126-5_6 | Isolation of Artificial Binding Proteins (Affimer Reagents) for Use in Molecular |
| 33303866 | 10.1097/00000539-200010000-00009 | 10.1038/s41598-020-78600-y | MRI-based molecular imaging of epicardium-derived stromal cells (EpiSC) by pepti |
| 33315926 | 10.1111/j.1749-4486.2009.01973.x | 10.1371/journal.pone.0243947 | Patient perceptions of phage therapy for diabetic foot infection. |
| 33317184 | 10.4269/ajtmh.12-0023 | 10.3390/biom10121652 | Highly Sensitive Detection of Zika Virus Nonstructural Protein 1 in Serum Sample |
| 33321823 | 10.1007/978-1-4939-7395-8_9 | 10.3390/v12121418 | Characterization of Salmonella Isolates from Various Geographical Regions of the |
| 33323672 | 10.3389/fchem.2019.00824 | 10.4014/jmb.2010.10021 | Mechanisms and Control Strategies of Antibiotic Resistance in Pathological Biofi |
| 33324585 | 10.1128/genomeA.00258-16 | 10.3389/fcimb.2020.620703 | Editorial: Recent Advances in Understanding the Pathogenesis of Shiga Toxin-Prod |
| 33328654 | 10.1016/j.molcel.2020.03.033 | 10.1038/s41589-020-00700-7 | Controlling and enhancing CRISPR systems. |
| 33349652 | 10.1101/2020.03.02.973784v1 | 10.1038/s41396-020-00860-3 | CRISPR-Cas systems restrict horizontal gene transfer in Pseudomonas aeruginosa. |
| 33352791 | 10.1128/IAI.73.12.8039-8049.2005 | 10.3390/v12121470 | In Vitro Evaluation of a Phage Cocktail Controlling Infections with Escherichia  |
| 33353123 | 10.1128/CVI.00333-08 | 10.3390/biom10121694 | Yersinia Outer Membrane Vesicles as Potential Vaccine Candidates in Protecting a |
| 33353489 | 10.5772/intechopen.86324 | 10.1080/01652176.2020.1868616 | Bovine brucellosis - a comprehensive review. |
| 33356871 | 10.1007/s00217-007-0632-x | 10.1080/21505594.2020.1868841 | The Superior Adherence Phenotype of E. coli O104:H4 is Directly Mediated by the  |
| 33357309 | 10.1021/acs.molpharmaceut.9b00633 | 10.3779/j.issn.1009-3419.2020.103.17 | [Screening and Identification of the Peptides Specifically Binding to Human Non- |
| 33357462 | 10.1002/wrna.1379 | 10.1016/j.chembiol.2020.12.003 | Discovery of cellular substrates of human RNA-decapping enzyme DCP2 using a stap |
| 33358997 | 10.1074/mcp.T600035-MCP200 | 10.1016/j.jim.2020.112952 | Multiplex bead binding assays using off-the-shelf components and common flow cyt |
| 33363055 | 10.3389/fmicb.2020.01453 | 10.3389/fcimb.2020.595709 | Prophage-Related Gene VpaChn25_0724 Contributes to Cell Membrane Integrity and G |
| 33370781 | 10.1163/156856107780684567 | 10.1371/journal.pone.0244518 | Surface texture limits transfer of S. aureus, T4 bacteriophage, influenza B viru |
| 33371447 | 10.1038/s41592-020-0746-7 | 10.3390/biom10121701 | Nanobodies Right in the Middle: Intrabodies as Toolbox to Visualize and Modulate |
| 33375201 | 10.1007/s00203-014-1013-z | 10.3390/v13010007 | Staphylococcal Phage in Combination with Staphylococcus Epidermidis as a Potenti |
| 33376251 | 10.1016/j.ajpath.2020.07.001 | 10.1038/s41598-020-79625-z | Survival of the enveloped bacteriophage Phi6 (a surrogate for SARS-CoV-2) in eva |
| 33382949 | 10.1016/j.jim.2007.09.017 | 10.1080/19420862.2020.1864084 | Combining phage display with SMRTbell next-generation sequencing for the rapid d |
| 33395313 | 10.1007/s00018-019-03048-x | 10.1021/acs.nanolett.0c04833 | Bifunctional Janus Particles as Multivalent Synthetic Nanoparticle Antibodies (S |
| 33396774 | 10.1016/j.bmc.2017.06.052 | 10.3390/ijms22010314 | Tumor-Targeting Peptides Search Strategy for the Delivery of Therapeutic and Dia |
| 33396965 | 10.1111/1462-2920.13284 | 10.3390/v13010051 | Bacteriophage Treatment: Critical Evaluation of Its Application on World Health  |
| 33397904 | 10.1186/1471-2105-10-421 | 10.1038/s41467-020-20199-9 | Long-read metagenomics using PromethION uncovers oral bacteriophages and their i |
| 33406073 | 10.4049/jimmunol.1500146 | 10.1371/journal.pone.0239792 | Comprehensive genomic analysis reveals virulence factors and antibiotic resistan |
| 33406123 | 10.1021/acs.bioconjchem.5b00283 | 10.1371/journal.pone.0241157 | Development of an orally-administrable tumor vasculature-targeting therapeutic u |
| 33408174 | 10.1099/mic.0.035055-0 | 10.1128/JVI.02245-20 | A PolyQ Membrane Protein of Vibrio cholerae Acts as the Receptor for Phage Infec |
| 33411815 | 10.1006/jmbi.2000.4315 | 10.1371/journal.pgen.1009204 | Phage infection and sub-lethal antibiotic exposure mediate Enterococcus faecalis |
| 33413427 | 10.2174/187152508785909528 | 10.1186/s12951-020-00758-4 | Development of targeted therapy therapeutics to sensitize triple-negative breast |
| 33416098 | 10.1016/j.numecd.2019.09.012 | 10.3892/ijmm.2020.4822 | Construction and application of a human scFv phage display library based on Cre‑ |
| 33418559 | 10.4292/wjgpt.v8.i3.162 | 10.1371/journal.pone.0245354 | Klebsiella virus UPM2146 lyses multiple drug-resistant Klebsiella pneumoniae in  |
| 33420898 | 10.1080/15384101.2020.1820697 | 10.1007/s11010-020-04046-5 | DMP-1 promoter-associated antisense strand non-coding RNA, panRNA-DMP-1, physica |
| 33426055 | 10.4014/jmb.1908.08021 | 10.1155/2020/5463801 | Isolation of a Novel Lytic Bacteriophage against a Nosocomial Methicillin-Resist |
| 33429117 | 10.1021/acs.est.6b00876 | 10.1016/j.scitotenv.2020.144786 | Evaluation of two rapid ultrafiltration-based methods for SARS-CoV-2 concentrati |
| 33430886 | 10.1038/nature13777 | 10.1186/s12936-020-03548-3 | Isolation and light chain shuffling of a Plasmodium falciparum AMA1-specific hum |
| 33432151 | 10.1038/nprot.2007.521 | 10.1038/s41564-020-00830-7 | Bacteriophage-resistant Acinetobacter baumannii are resensitized to antimicrobia |
| 33436625 | 10.1038/s41586-019-1786-y | 10.1038/s41467-020-20575-5 | Viral speciation through subcellular genetic isolation and virogenesis incompati |
| 33436632 | 10.1096/fj.14-255992 | 10.1038/s41467-020-20577-3 | Targeting adaptor protein SLP76 of RAGE as a therapeutic approach for lethal sep |
| 33436756 | 10.1128/AEM.00641-19 | 10.1038/s41598-020-80076-9 | CrAssphage and its bacterial host in cat feces. |
| 33436840 | 10.1016/j.trac.2017.01.009 | 10.1038/s41598-020-80354-6 | Selection and characterisation of Affimers specific for CEA recognition. |
| 33440682 | 10.1099/mic.0.2007/006213-0 | 10.3390/v13010089 | Characterization of Yersinia pestis Phage Lytic Activity in Human Whole Blood fo |
| 33440735 | 10.1006/meth.2001.1262 | 10.3390/ijms22020649 | The Acquisition of Colistin Resistance Is Associated to the Amplification of a L |
| 33441405 | 10.1128/AEM.02272-07 | 10.1128/mSphere.01215-20 | A Novel N4-Like Bacteriophage Isolated from a Wastewater Source in South India w |
| 33441407 | 10.1101/2020.07.24.218685 | 10.1128/mSphere.01263-20 | Genes Influencing Phage Host Range in Staphylococcus aureus on a Species-Wide Sc |
| 33445453 | 10.1111/j.1752-4571.2011.00236.x | 10.3390/microorganisms9010152 | Aztreonam Lysine Increases the Activity of Phages E79 and phiKZ against Pseudomo |
| 33446140 | 10.3892/ijo.2017.4109 | 10.1186/s12885-020-07761-w | Development of an engineered peptide antagonist against periostin to overcome do |
| 33446406 | 10.1126/scitranslmed.abf1555 | 10.1016/j.tim.2020.12.006 | Slaying SARS-CoV-2 One (Single-domain) Antibody at a Time. |
| 33446856 | 10.1145/355984.355989 | 10.1038/s41598-021-81063-4 | Predicting bacteriophage hosts based on sequences of annotated receptor-binding  |
| 33450990 | 10.1038/s41596-020-0346-0 | 10.3390/ijms22020735 | Mycobacteriophages as Potential Therapeutic Agents against Drug-Resistant Tuberc |
| 33458528 | 10.1016/j.mimet.2011.07.021 | 10.1021/acsomega.0c05340 | Human Hexa-Histidine-Tagged Single-Chain Variable Fragments for Bioimaging of Ba |
| 33459147 | 10.1016/s0022-1759(96)00215-3 | 10.1080/19420862.2020.1850395 | Discovery and optimization of a novel anti-GUCY2c x CD3 bispecific antibody for  |
| 33466377 | 10.1128/AAC.06330-11 | 10.3390/v13010060 | A Case of Phage Therapy against Pandrug-Resistant Achromobacter xylosoxidans in  |
| 33466546 | 10.3390/antibiotics8030103 | 10.3390/ph14010034 | Bacteriophage Therapy of Bacterial Infections: The Rediscovered Frontier. |
| 33467089 | 10.1002/pssa.201900825 | 10.3390/ijms22020859 | Pulling the Brakes on Fast and Furious Multiple Drug-Resistant (MDR) Bacteria. |
| 33467484 | 10.1016/j.jmb.2012.08.008 | 10.3390/cells10010160 | Structural Insights into Membrane Fusion Mediated by Convergent Small Fusogens. |
| 33467548 | 10.1080/1040841X.2020.1729695 | 10.3390/antibiotics10010078 | Bacteriophage Cocktail-Mediated Inhibition of Pseudomonas aeruginosa Biofilm on  |
| 33472935 | 10.3791/53964 | 10.1128/JVI.01832-20 | Novel Lytic Phages Protect Cells and Mice against Pseudomonas aeruginosa Infecti |
| 33474609 | 10.1111/j.1749-4486.2009.01973.x | 10.1007/s00203-020-02167-5 | Phage therapy as strategy to face post-antibiotic era: a guide to beginners and  |
| 33483508 | 10.1016/j.jaci.2017.11.010 | 10.1038/s41467-020-20622-1 | Profiling serum antibodies with a pan allergen phage library identifies key whea |
| 33484405 | 10.1093/nar/gkr485 | 10.1007/s12560-021-09460-6 | Bi- and Multi-directional Gene Transfer in the Natural Populations of Polyvalent |
| 33489934 | 10.1016/j.chom.2020.08.005 | 10.3389/fcimb.2020.601573 | The Viral Janus: Viruses as Aetiological Agents and Treatment Options in Colorec |
| 33495501 | 10.1111/j.1574-6968.2011.02476.x | 10.1038/s41598-021-81580-2 | Designing P. aeruginosa synthetic phages with reduced genomes. |
| 33497357 | 10.1093/nar/gkz452 | 10.1172/jci.insight.144499 | Distinct antibody repertoires against endemic human coronaviruses in children an |
| 33498243 | 10.3390/ijerph17093278 | 10.3390/microorganisms9020206 | Animal Models in the Evaluation of the Effectiveness of Phage Therapy for Infect |
| 33498475 | 10.1371/journal.pone.0036991 | 10.3390/v13020149 | Phage phiKZ-The First of Giants. |
| 33500260 | 10.1016/j.ccell.2020.10.019 | 10.1136/jitc-2020-001762 | Anticancer immunity induced by a synthetic tumor-targeted CD137 agonist. |
| 33504115 | 10.2183/pjab.92.156 | 10.3390/v13020178 | Phage Display Technology as a Powerful Platform for Antibody Drug Discovery. |
| 33505366 | 10.1172/JCI118253 | 10.3389/fmicb.2020.593988 | Overcoming Challenges to Make Bacteriophage Therapy Standard Clinical Treatment  |
| 33509087 | 10.1111/j.2517-6161.1995.tb02031.x | 10.1186/s12866-021-02090-9 | Higher genome variability within metabolism genes associates with recurrent Clos |
| 33521848 | 10.1158/1078-0432 | 10.1007/s00253-021-11128-x | Generation of a novel affibody molecule targeting Chlamydia trachomatis MOMP. |
| 33529170 | 10.1002/prot.25674 | 10.1172/jci.insight.145785 | Dromedary camels as a natural source of neutralizing nanobodies against SARS-CoV |
| 33531388 | 10.1111/mmi.12018 | 10.1128/mBio.03384-20 | Pseudomonas aeruginosa Uses c-di-GMP Phosphodiesterases RmcA and MorA To Regulat |
| 33540528 | 10.1073/pnas.1714812115 | 10.3390/antibiotics10020145 | Pseudomonas aeruginosa Resistance to Bacteriophages and Its Prevention by Strate |
| 33542282 | 10.1073/pnas.120163297 | 10.1038/s41598-021-82422-x | O antigen restricts lysogenization of non-O157 Escherichia coli strains by Stx-c |
| 33543454 | 10.1155/2019/9367845 | 10.1007/978-3-030-58174-9_2 | Homing Peptides for Cancer Therapy. |
| 33544853 | 10.1101/137067 | 10.1093/nar/gkab006 | Mobile element warfare via CRISPR and anti-CRISPR in Pseudomonas aeruginosa. |
| 33552999 | 10.1016/j.chom.2020.08.005 | 10.3389/fcimb.2020.575084 | Enteric Phageome Alterations in Patients With Type 2 Diabetes. |
| 33556628 | 10.1101/2020.04.16.045419 | 10.1016/j.nbt.2021.01.010 | FN3-based monobodies selective for the receptor binding domain of the SARS-CoV-2 |
| 33557673 | 10.1093/nar/gki387 | 10.1080/19420862.2021.1883239 | Combining random mutagenesis, structure-guided design and next-generation sequen |
| 33557979 | 10.1001/jama.2020.9843 | 10.1017/ice.2021.48 | Hydrogen peroxide vapor decontamination of N95 respirators for reuse. |
| 33559027 | 10.1111/febs.14376 | 10.1007/s11686-021-00339-x | Phage Display Screening for Alba Superfamily Proteins from the Human Malaria Par |
| 33563827 | 10.1093/nar/gkg595 | 10.1128/mBio.03454-20 | A Grad-seq View of RNA and Protein Complexes in Pseudomonas aeruginosa under Sta |
| 33563833 | 10.1093/bioinformatics/btu808 | 10.1128/mBio.03474-20 | Targeting of Mammalian Glycans Enhances Phage Predation in the Gastrointestinal  |
| 33567764 | 10.1016/0022-1759(89)90397-9 | 10.3390/ijms22041709 | A Novel Artificially Humanized Anti-Cripto-1 Antibody Suppressing Cancer Cell Gr |
| 33569355 | 10.1101/gr.074492.107 | 10.3389/fcimb.2020.608402 | Heterogeneous Klebsiella pneumoniae Co-infections Complicate Personalized Bacter |
| 33576446 | 10.1080/15476286.2017.1367888 | 10.3892/mmr.2021.11897 | Comparison and optimisation of microRNA extraction from the plasma of healthy pr |
| 33577875 | 10.1053/j.gastro.2021.01.010 | 10.1053/j.gastro.2021.02.013 | Functional Restoration of Bacteriomes and Viromes by Fecal Microbiota Transplant |
| 33590592 | 10.1038/mtm.2013.9 | 10.1002/anie.202100872 | Quantitative Assessment of the Physical Virus Titer and Purity by Ultrasensitive |
| 33594055 | 10.1038/nbt.3988 | 10.1038/s41467-021-21350-w | Analysis of metagenome-assembled viral genomes from the human gut reveals divers |
| 33602058 | 10.1038/nmeth.3176 | 10.1080/19490976.2021.1887719 | The gut virome in Irritable Bowel Syndrome differs from that of controls. |
| 33606979 | 10.1101/2020.05.06.081778 | 10.1016/j.cell.2021.01.029 | Massive expansion of human gut bacteriophage diversity. |
| 33607132 | 10.1007/s00018-020-03580-1 | 10.1016/j.ijbiomac.2021.02.090 | Underscoring the immense potential of chitosan in fighting a wide spectrum of vi |
| 33619540 | 10.1016/j.ymthe.2020.10.006 | 10.1093/nar/gkaa1264 | Microbial single-strand annealing proteins enable CRISPR gene-editing tools with |
| 33620651 | 10.1016/j.foodcont.2016.10.033 | 10.1007/978-3-030-65481-8_6 | Phage Biocontrol of Campylobacter: A One Health Approach. |
| 33620655 | 10.1128/aem.00346-15 | 10.1007/978-3-030-65481-8_10 | Natural Competence and Horizontal Gene Transfer in Campylobacter. |
| 33622723 | 10.1128/JB.187.12.4005-4014.2005 | 10.1128/mBio.03608-20 | Toward a Comprehensive Analysis of Posttranscriptional Regulatory Networks: a Ne |
| 33630870 | 10.1159/000485455 | 10.1371/journal.pone.0247045 | A "ligand-targeting" peptide-drug conjugate: Targeted intracellular drug deliver |
| 33633363 | 10.1158/0008-5472.CAN-11-1620 | 10.1038/s41401-020-00574-4 | Development of a nanobody-based immunoassay for the sensitive detection of fibri |
| 33634788 | 10.1038/s41564-017-0053-y | 10.7554/eLife.60608 | MetaHiC phage-bacteria infection network reveals active cycling phages of the he |
| 33638001 | 10.1111/jdv.12079 | 10.1007/s00284-021-02395-y | Isolation and Characterization of a Novel Phage SaGU1 that Infects Staphylococcu |
| 33642937 | 10.1016/j.micres.2014.12.001 | 10.1016/j.cej.2021.129071 | Antimicrobial TiO2 nanocomposite coatings for surfaces, dental and orthopaedic i |
| 33643301 | 10.1016/s0167-5699(98)01368-1 | 10.3389/fimmu.2020.619896 | Domain-Scan: Combinatorial Sero-Diagnosis of Infectious Diseases Using Machine L |
| 33649949 | 10.1101/gr.2289704 | 10.1007/978-1-0716-1274-3_7 | Phageome Analysis of Bifidobacteria-Rich Samples. |
| 33657424 | 10.1093/cid/ciaa1275 | 10.1016/j.chom.2021.02.019 | Robust SARS-CoV-2 infection in nasal turbinates after treatment with systemic ne |
| 33666135 | 10.1074/mcp.O115.052209 | 10.1080/19420862.2021.1893426 | Bispecific VH/Fab antibodies targeting neutralizing and non-neutralizing Spike e |
| 33668889 | 10.3390/microorganisms9010152 | 10.3390/microorganisms9030478 | In Vitro Newly Isolated Environmental Phage Activity against Biofilms Preformed  |
| 33668899 | 10.1093/bioinformatics/btu153 | 10.3390/ph14030184 | Synergistic Killing and Re-Sensitization of Pseudomonas aeruginosa to Antibiotic |
| 33668971 | 10.1107/S0907444910007493 | 10.3390/molecules26051225 | Phage-Display Based Discovery and Characterization of Peptide Ligands against WD |
| 33669238 | 10.1126/sciadv.aax0064 | 10.3390/ijms22041934 | The Versatile Manipulations of Self-Assembled Proteins in Vaccine Design. |
| 33669643 | 10.4274/balkanmedj.2016.1853 | 10.3390/v13020318 | Phage-Bacteria Interactions in Potential Applications of Bacteriophage vB_EfaS-2 |
| 33670028 | 10.1007/s00018-014-1612-5 | 10.3390/v13020334 | Improving the Inhibitory Effect of Phages against Pseudomonas aeruginosa Isolate |
| 33670076 | 10.1016/j.celrep.2020.107956 | 10.3390/v13020336 | An Efficient, Counter-Selection-Based Method for Prophage Curing in Pseudomonas  |
| 33671516 | 10.1002/14651858.CD009528.pub4 | 10.3390/ijms22042155 | Approaches to Targeting Bacterial Biofilms in Cystic Fibrosis Airways. |
| 33671574 | 10.1371/journal.pone.0228676 | 10.3390/v13020337 | Examination of Staphylococcus aureus Prophages Circulating in Egypt. |
| 33671877 | 10.1126/science.abc7520 | 10.3390/ijms22041913 | Neutralizing Human Antibodies against Severe Acute Respiratory Syndrome Coronavi |
| 33673397 | 10.1128/IAI.70.8.3985-3993.2002 | 10.3390/microorganisms9030490 | Comparative Genomic Analysis of Three Pseudomonas Species Isolated from the East |
| 33683192 | 10.3389/fmicb.2020.577658 | 10.1099/mgen.0.000545 | Analysis of a small outbreak of Shiga toxin-producing Escherichia coli O157:H7 u |
| 33683473 | 10.1016/j.jviromet.2018.10.002 | 10.1007/s00705-021-05024-y | Diversity of β-lactamase-encoding genes in wastewater: bacteriophages as reporte |
| 33687511 | 10.1186/1743-422X-7-254 | 10.1007/s00284-021-02398-9 | Phage Display Technique as a Tool for Diagnosis and Antibody Selection for Coron |
| 33690097 | 10.1016/j.ebiom.2021.103250 | 10.1016/j.ebiom.2021.103267 | Phage display for targeting PCSK9. |
| 33692375 | 10.1021/bi0609624 | 10.1038/s41598-021-84618-7 | Identification of an alpha-1 antitrypsin variant with enhanced specificity for f |
| 33692485 | 10.1126/science.280.5361.295 | 10.1038/s41396-021-00946-6 | The effect of Quorum sensing inhibitors on the evolution of CRISPR-based phage i |
| 33703996 | 10.1128/MMBR.05015-11 | 10.1080/22221751.2021.1902754 | Pre-optimized phage therapy on secondary Acinetobacter baumannii infection in fo |
| 33707427 | 10.4161/mabs.24218 | 10.1038/s41467-021-21609-2 | SARS-CoV-2 neutralizing human recombinant antibodies selected from pre-pandemic  |
| 33707432 | 10.1038/nbt.3300 | 10.1038/s41467-021-21578-6 | Overcoming the design, build, test bottleneck for synthesis of nonrepetitive pro |
| 33712669 | 10.1162/089976600300015015 | 10.1038/s41598-021-85274-7 | Antibody design using LSTM based deep generative model from phage display librar |
| 33721106 | 10.1093/eurheartj/ehx218 | 10.1007/s00395-021-00849-9 | A DARPin targeting activated Mac-1 is a novel diagnostic tool and potential anti |
| 33727555 | 10.1128/IAI.00096-09 | 10.1038/s41522-021-00194-8 | Impact of temperature-dependent phage expression on Pseudomonas aeruginosa biofi |
| 33738267 | 10.1111/1751-7915.13594 | 10.3389/fcimb.2021.637313 | A Novel Acinetobacter baumannii Bacteriophage Endolysin LysAB54 With High Antiba |
| 33751147 | 10.1371/journal.pcbi.1005595 | 10.1007/s00294-021-01173-4 | Genetic characteristics and phylogenetic analysis of Brazilian clinical strains  |
| 33757423 | 10.1093/nar/gkw257 | 10.1186/s12864-021-07535-z | Hybrid genome de novo assembly with methylome analysis of the anaerobic thermoph |
| 33761869 | 10.1007/s12010-018-2762-y | 10.1186/s12879-021-05969-0 | Isolation and characterizations of a novel recombinant scFv antibody against exo |
| 33765014 | 10.1093/nar/18.20.6097 | 10.1371/journal.pcbi.1008751 | Parameters and determinants of responses to selection in antibody libraries. |
| 33767189 | 10.1287/mksc.12.1.1 | 10.1038/s41467-021-22055-w | Engineering and characterization of gymnosperm sapwood toward enabling the desig |
| 33777836 | 10.1128/JB.01919-07 | 10.3389/fcimb.2021.622487 | The M. tuberculosis Rv1523 Methyltransferase Promotes Drug Resistance Through Me |
| 33779498 | 10.1186/s13059-016-0997-x | 10.1080/19490976.2021.1900995 | Expansion and persistence of antibiotic-specific resistance genes following anti |
| 33781338 | 10.1038/nrmicro3552 | 10.1186/s40168-021-01017-w | Thousands of previously unknown phages discovered in whole-community human gut m |
| 33785625 | 10.1371/journal.pone.0003957 | 10.1128/mBio.03431-20 | Mycobacterium abscessus Strain Morphotype Determines Phage Susceptibility, the R |
| 33785627 | 10.1128/mBio.01069-17 | 10.1128/mBio.03441-20 | The Prophage and Plasmid Mobilome as a Likely Driver of Mycobacterium abscessus  |
| 33785903 | 10.1093/nar/gkw387 | 10.1038/s41579-021-00536-5 | The human virome: assembly, composition and host interactions. |
| 33788112 | 10.3389/fmicb.2018.01033 | 10.1007/s10517-021-05122-6 | Determination of Bactericidal Activity Spectrum of Recombinant Endolysins of ECD |
| 33791236 | 10.1038/s41587-018-0008-8 | 10.3389/fcimb.2021.616918 | Probing the "Dark Matter" of the Human Gut Phageome: Culture Assisted Metagenomi |
| 33792875 | 10.1128/MCB.00582-06 | 10.1007/978-1-0716-1386-3_10 | Purification of RiboNucleoProtein Particles by MS2-MBP Affinity Chromatography. |
| 33794724 | 10.1093/bioinformatics/bts199 | 10.1080/19490976.2021.1897217 | Gut bacteriophage dynamics during fecal microbial transplantation in subjects wi |
| 33799646 | 10.1016/j.tim.2012.10.005 | 10.3390/v13030455 | Common Oral Medications Lead to Prophage Induction in Bacterial Isolates from th |
| 33801971 | 10.1186/s12941-020-00389-5 | 10.3390/microorganisms9030569 | Parallel Evolution of Enhanced Biofilm Formation and Phage-Resistance in Pseudom |
| 33804216 | 10.3389/fmicb.2016.00882 | 10.3390/v13030478 | Isolation and Characterisation of Bacteriophages with Activity against Invasive  |
| 33804519 | 10.1186/s13073-020-00811-9 | 10.3390/v13030391 | Isolation and Characterization of Cross-Reactive Human Monoclonal Antibodies Tha |
| 33807121 | 10.1016/j.ijid.2020.04.059 | 10.3390/biom11030484 | Neisseria gonorrhoeae Multivalent Maxibody with a Broad Spectrum of Strain Speci |
| 33810202 | 10.1164/rccm.201609-1954OC | 10.3390/microorganisms9030660 | Variability in Bacteriophage and Antibiotic Sensitivity in Serial Pseudomonas ae |
| 33811022 | 10.3390/v9070168 | 10.1128/AEM.03019-20 | Rapid Clinical Screening of Burkholderia pseudomallei Colonies by a Bacteriophag |
| 33813257 | 10.1038/s41564-020-0694-0 | 10.1016/j.coviro.2021.03.004 | Assembly of the virome in newborn human infants. |
| 33813641 | 10.1002/bies.201700112 | 10.1007/s00284-021-02472-2 | Genome-Wide Identification and Analysis of Chromosomally Integrated Putative Pro |
| 33829687 | 10.1016/S1473-3099(20)30330-3 | 10.12182/20210360207 | [Bacteriophage Therapy: Retrospective Review and Future Prospects]. |
| 33841345 | 10.1038/ncomms11274 | 10.3389/fmicb.2021.613450 | Experimental Evolution of Interference Competition. |
| 33841816 | 10.1016/j.ijfoodmicro.2003.08.018 | 10.1002/fsn3.2164 | Microbiological quality assessment (including antibiogram and threat assessment) |
| 33845877 | 10.1093/bioinformatics/btu393 | 10.1186/s40168-021-01036-7 | Isolation and characterisation of ΦcrAss002, a crAss-like phage from the human g |
| 33849822 | 10.1002/hep.31220 | 10.12122/j.issn.1673-4254.2021.03.03 | [LIM-domain binding protein 2 regulated by m6A modification inhibits lung adenoc |
| 33852569 | 10.1016/j.chom.2019.10.009 | 10.1371/journal.pone.0240958 | The gut virome of healthy children during the first year of life is diverse and  |
| 33853672 | 10.2290/v11010088 | 10.1186/s40168-021-01026-9 | Assessment of the microbiome during bacteriophage therapy in combination with sy |
| 33853691 | 10.3389/fmicb.2018.00749 | 10.1186/s40168-021-01008-x | Temporal landscape of human gut RNA and DNA virome in SARS-CoV-2 infection and s |
| 33856343 | 10.1016/j.cell.2019.09.015 | 10.7554/eLife.68277 | ORACLE reveals a bright future to fight bacteria. |
| 33859250 | 10.1093/nar/gkr366 | 10.1038/s41598-021-87501-7 | The VH framework region 1 as a target of efficient mutagenesis for generating a  |
| 33862490 | 10.1016/j.isci.2021.102287 | 10.1016/j.copbio.2021.03.002 | Preclinical data and safety assessment of phage therapy in humans. |
| 33870869 | 10.1016/S1473-3099(17)30325-0 | 10.1080/19490976.2021.1911279 | The role of the human gut microbiota in colonization and infection with multidru |
| 33871329 | 10.1038/nmeth.2019 | 10.1099/mic.0.001021 | Bacteriophage infection of Escherichia coli leads to the formation of membrane v |
| 33875544 | 10.1371/journal.ppat.1002917 | 10.1128/JB.00141-21 | A Tail Fiber Protein and a Receptor-Binding Protein Mediate ICP2 Bacteriophage I |
| 33875547 | 10.1006/abio.1999.4085 | 10.1128/JB.00027-21 | Mutations in Ehrlichia chaffeensis Genes ECH_0660 and ECH_0665 Cause Transcripti |
| 33877574 | 10.1073/pnas.1222743110 | 10.1007/s12275-021-1085-9 | Gain and loss of antibiotic resistant genes in multidrug resistant bacteria: One |
| 33879590 | 10.1128/JB.00268-18 | 10.1128/mBio.00039-21 | Peptidoglycan Contribution to the B Cell Superantigen Activity of Staphylococcal |
| 33881767 | 10.1016/j.tim.2020.10.014 | 10.1007/s40259-021-00480-z | Engineered Bacteriophage Therapeutics: Rationale, Challenges and Future. |
| 33886531 | 10.3201/eid2705.210514 | 10.15585/mmwr.mm7016e1 | Laboratory Modeling of SARS-CoV-2 Exposure Reduction Through Physically Distance |
| 33899674 | 10.1007/978-1-4939-7447-4_19 | 10.1080/19420862.2021.1904546 | A platform-agnostic, function first-based antibody discovery strategy using plas |
| 33902596 | 10.2174/1568026618666180522075258 | 10.1186/s12964-021-00727-w | Peptide targeting of lysophosphatidylinositol-sensing GPR55 for osteoclastogenes |
| 33902597 | 10.12659/MSM.881844 | 10.1186/s12941-021-00433-y | Bacteriophage therapy for inhibition of multi drug-resistant uropathogenic bacte |
| 33906920 | 10.1016/j.str.2011.03.019 | 10.1128/mBio.00211-21 | Antiviral Resistance and Phage Counter Adaptation to Antibiotic-Resistant Extrai |
| 33910982 | 10.1086/318514 | 10.1128/MMBR.00031-20 | Incompatibility Group I1 (IncI1) Plasmids: Their Genetics, Biology, and Public H |
| 33910993 | 10.1002/prot.25792 | 10.1128/mSphere.00203-21 | Predicting COVID-19 Severity with a Specific Nucleocapsid Antibody plus Disease  |
| 33918836 | 10.3390/ijms13045254 | 10.3390/v13040649 | Phage-Displayed Peptides for Targeting Tyrosine Kinase Membrane Receptors in Can |
| 33920965 | 10.1159/000473872 | 10.3390/v13040680 | The Advantages and Challenges of Using Endolysins in a Clinical Setting. |
| 33921071 | 10.1111/j.1365-2672.2004.02422.x | 10.3390/bios11040124 | Bacteriophage-Based Biosensing of Pseudomonas aeruginosa: An Integrated Approach |
| 33921405 | 10.1016/j.jmb.2013.07.040 | 10.3390/v13040663 | Structural Characterization of a Minimal Antibody against Human APOBEC3B. |
| 33923360 | 10.1016/S0021-9258(18)47069-X | 10.3390/v13050750 | Screening of Bacteriophage Encoded Toxic Proteins with a Next Generation Sequenc |
| 33923551 | 10.1073/pnas.2010197117 | 10.3390/ijms22084123 | Antibody Libraries as Tools to Discover Functional Antibodies and Receptor Pleio |
| 33923724 | 10.1016/0019-2791(71)90454-X | 10.3390/ijms22084146 | In Vitro Characterization of Neutralizing Hen Antibodies to Coxsackievirus A16. |
| 33926375 | 10.1038/srep17507 | 10.1186/s12879-021-06069-9 | Five-year microevolution of a multidrug-resistant Mycobacterium tuberculosis str |
| 33931013 | 10.1016/j.tim.2020.05.021 | 10.1186/s12866-021-02197-z | Sewage and sewage-contaminated environments are the most prominent sources to is |
| 33937105 | 10.1128/AEM.00886-18 | 10.3389/fcimb.2021.668430 | Phage Endolysin LysP108 Showed Promising Antibacterial Potential Against Methici |
| 33937418 | 10.1038/nbt0616-577 | 10.1155/2021/6659960 | Epitope-Based Chicken-Derived Novel Anti-PAD2 Monoclonal Antibodies Inhibit Citr |
| 33938175 | 10.1126/science.280.5367.1265 | 10.1515/hsz-2020-0185 | Phage-display reveals interaction of lipocalin allergen Can f 1 with a peptide r |
| 33945146 | 10.3945/ajcn.110.010132 | 10.1007/s13679-021-00438-w | Do Antibiotics Cause Obesity Through Long-term Alterations in the Gut Microbiome |
| 33946948 | 10.5281/zenodo.4089225 | 10.3390/ijms22094725 | Screening for Interacting Proteins with Peptide Biomarker of Blood-Brain Barrier |
| 33946994 | 10.3389/fncel.2020.00229 | 10.3390/ijms22094734 | Gut Susceptibility to Viral Invasion: Contributing Roles of Diet, Microbiota and |
| 33947755 | 10.2174/138920207780833810 | 10.1128/mBio.00458-21 | Heterogenous Susceptibility to R-Pyocins in Populations of Pseudomonas aeruginos |
| 33949378 | 10.1016/j.jmoldx.2020.04.211 | 10.1039/d0an02483j | HIV detection from human serum with paper-based isotachophoretic RNA extraction  |
| 33952321 | 10.1111/rssc.12206 | 10.1186/s13059-021-02355-6 | geneshot: gene-level metagenomics identifies genome islands associated with immu |
| 33962011 | 10.1111/1751-7915.13698 | 10.1016/j.ymeth.2021.04.026 | Therapeutic approaches for SARS-CoV-2 infection. |
| 33963272 | 10.1038/s41467-019-12554-2 | 10.1038/s41393-021-00636-2 | Bacteriophages: what role may they play in life after spinal cord injury? |
| 33966671 | 10.1016/j.ajic.2020.11.010 | 10.1017/ice.2021.218 | A simulation study to evaluate contamination during reuse of N95 respirators and |
| 33968805 | 10.1128/JB.01370-08 | 10.3389/fcimb.2021.662344 | The Type II Secretory System Mediates Phage Infection in Vibrio cholerae. |
| 33974910 | 10.1101/2020.06.06.137513 | 10.1016/j.cell.2021.04.033 | Structural insight into SARS-CoV-2 neutralizing antibodies and modulation of syn |
| 33978401 | 10.1128/JB.01188-09 | 10.1021/jacs.1c01275 | A Metabolite of Pseudomonas Triggers Prophage-Selective Lysogenic to Lytic Conve |
| 33980677 | 10.1128/genomeA.00004-17 | 10.1128/mSphere.00223-21 | Staphylococcus epidermidis Phages Transduce Antimicrobial Resistance Plasmids an |
| 33980972 | 10.1093/nar/27.1.209 | 10.1038/s42003-021-02066-5 | CellectSeq: In silico discovery of antibodies targeting integral membrane protei |
| 33983947 | 10.1126/science.2992081 | 10.1371/journal.pone.0250318 | Identification of recombinant Fabs for structural and functional characterizatio |
| 33984699 | 10.1021/acs.est.6b00876 | 10.1016/j.scitotenv.2021.147534 | Detection of SARS-CoV-2 RNA in bivalve mollusks and marine sediments. |
| 33989511 | 10.1016/j.ijbiomac.2020.03.229 | 10.1080/21645515.2021.1913960 | The potential applications of T cell receptor (TCR)-like antibody in cervical ca |
| 33991511 | 10.1126/science.abh2644 | 10.1016/j.celrep.2021.109164 | Epitope profiling reveals binding signatures of SARS-CoV-2 immune response in na |
| 33993461 | 10.7150/ijbs.31957 | 10.1007/s12539-021-00436-5 | TUPDB: Target-Unrelated Peptide Data Bank. |
| 34001258 | 10.3389/fmicb.2020.612367 | 10.1186/s13104-021-05602-y | Blue light inactivation of the enveloped RNA virus Phi6. |
| 34001868 | 10.1016/j.jviromet.2013.08.035 | 10.1038/s41392-021-00615-2 | Gut Phage Database: phage mining in the cave of wonders. |
| 34008466 | 10.1038/s41429-020-0344-z | 10.1080/21505594.2021.1926411 | A phage protein-derived antipathogenic peptide that targets type IV pilus assemb |
| 34010620 | 10.1038/s41586-020-2008-3 | 10.1016/j.cell.2021.04.045 | High-resolution profiling of pathways of escape for SARS-CoV-2 spike-binding ant |
| 34011948 | 10.1073/pnas.2002589117 | 10.1038/s42003-021-02128-8 | Multivalent nanoparticle-based vaccines protect hamsters against SARS-CoV-2 afte |
| 34014515 | 10.1007/978-1-0716-0524-0_27 | 10.1007/978-1-0716-1166-1_3 | Identification of PDZ Interactions by Proteomic Peptide Phage Display. |
| 34016711 | 10.1186/1471-2105-12-395 | 10.1128/mBio.00973-21 | Toward a Phage Cocktail for Tuberculosis: Susceptibility and Tuberculocidal Acti |
| 34024246 | 10.1107/S2059798319011471 | 10.1080/19420862.2021.1922134 | Potent SARS-CoV-2 binding and neutralization through maturation of iconic SARS-C |
| 34026768 | 10.1007/s15010-017-1077-1 | 10.3389/fmed.2021.569159 | Case Report: Arthroscopic "Debridement Antibiotics and Implant Retention" With L |
| 34030968 | 10.1159/000473872 | 10.1016/j.tim.2021.04.008 | The phages of staphylococci: critical catalysts in health and disease. |
| 34040046 | 10.3390/cancers11091268 | 10.1038/s41598-021-90348-7 | Novel human neutralizing mAbs specific for Spike-RBD of SARS-CoV-2. |
| 34045567 | 10.1039/c2an35371g | 10.1038/s41598-021-90619-3 | Specific and rapid reverse assaying protocol for detection and antimicrobial sus |
| 34046704 | 10.1089/jam.2007.0610 | 10.1007/s00203-021-02382-8 | Bacteriophages as surrogates for the study of viral dispersion in open air. |
| 34050782 | 10.1128/aem.01729-15 | 10.1007/s00203-021-02402-7 | Characterization of a novel group I F-specific RNA bacteriophage isolated from h |
| 34052285 | 10.3389/FIMMU.2020.619896 | 10.1016/j.jmb.2021.167071 | Motifier: An IgOme Profiler Based on Peptide Motifs Using Machine Learning. |
| 34059940 | 10.1016/j.brainres.2016.01.028 | 10.1007/s00253-021-11363-2 | A screened PirB antagonist peptide antagonizes Aβ42-mediated inhibition of neuri |
| 34060472 | 10.1098/rsif.2018.0243 | 10.7554/eLife.65145 | Targeting a cell surface vitamin D receptor on tumor-associated macrophages in t |
| 34063251 | 10.1016/b978-0-12-394805-2.00001-4 | 10.3390/v13050825 | Isolation and Characterization of Streptococcus mutans Phage as a Possible Treat |
| 34064648 | 10.4292/wjgpt.v8.i3.162 | 10.3390/antibiotics10050556 | Clinical Pharmacology of Bacteriophage Therapy: A Focus on Multidrug-Resistant P |
| 34065940 | 10.1093/infdis/jiw290 | 10.3390/biom11050724 | Antibiotic Therapy of Plague: A Review. |
| 34066356 | 10.1002/1096-9888(200007)35:7<763::AID-JMS16>3.0.CO;2-# | 10.3390/ijerph18094934 | A Simple Electrostatic Precipitator for Trapping Virus Particles Spread via Drop |
| 34066841 | 10.1128/JVI.14.4.1008-1012.1974 | 10.3390/v13050865 | Evaluation of the Stability of Bacteriophages in Different Solutions Suitable fo |
| 34067885 | 10.3390/v10030103 | 10.3390/v13050928 | Phage Biocontrol of Pseudomonas aeruginosa in Water. |
| 34068736 | 10.1016/j.tim.2018.10.008 | 10.3390/v13050875 | Viruses with U-DNA: New Avenues for Biotechnology. |
| 34070537 | 10.1007/s40336-016-0178-7 | 10.3390/molecules26113159 | Radiotracers for Bone Marrow Infection Imaging. |
| 34071061 | 10.15698/mic2019.09.689 | 10.3390/nu13061779 | Human Milk Virome Analysis: Changing Pattern Regarding Mode of Delivery, Birth W |
| 34071422 | 10.1146/annurev-virology-091919-074551 | 10.3390/v13061013 | Temperate Bacteriophages-The Powerful Indirect Modulators of Eukaryotic Cells an |
| 34072209 | 10.1128/CMR.13.4.559 | 10.3390/ijms22115743 | Detection of SARS-CoV-2 RNA by a Multiplex Reverse-Transcription Loop-Mediated I |
| 34073633 | 10.1128/AAC.01611-12 | 10.3390/ijms22115690 | Characterization of an Endolysin Targeting Clostridioides difficile That Affects |
| 34079028 | 10.1016/j.chroma.2009.09.047 | 10.1038/s41598-021-91208-0 | Focused peptide library screening as a route to a superior affinity ligand for a |
| 34080897 | 10.1093/nar/gkz935 | 10.1128/MRA.00076-21 | Isolation and Genomic Analysis of the Phage vB_PaeP_fHoPae04 Infecting Pseudomon |
| 34086281 | 10.1093/nar/gkg563 | 10.1007/978-1-0716-1499-0_13 | FRET Analysis of RNA -Protein Interactions Using Spinach Aptamers. |
| 34098950 | 10.1038/s41590-020-00826-9 | 10.1186/s12929-021-00740-8 | Identification of COVID-19 B-cell epitopes with phage-displayed peptide library. |
| 34106768 | 10.1093/bioinformatics/btv249 | 10.1128/mSphere.00337-21 | Recent Vibrio cholerae O1 Epidemic Strains Are Unable To Replicate CTXΦ Prophage |
| 34111729 | 10.1080/22221751.2020.1729071 | 10.1016/j.watres.2021.117090 | Decay of infectious SARS-CoV-2 and surrogates in aquatic environments. |
| 34113327 | 10.1016/0003-2697(88)90134-0 | 10.3389/fmicb.2021.660403 | Mining of Gram-Negative Surface-Active Enzybiotic Candidates by Sequence-Based C |
| 34115350 | 10.1021/acs.analchem.6b03526 | 10.1007/978-1-0716-1562-1_3 | Phage Microarrays for Screening of Humoral Immune Responses. |
| 34122456 | 10.1371/journal.pcbi.1006112 | 10.3389/fimmu.2021.690742 | Prospects of Neutralizing Nanobodies Against SARS-CoV-2. |
| 34125841 | 10.1038/nature06350 | 10.1371/journal.pcbi.1009067 | How does feedback from phage infections influence the evolution of phase variati |
| 34126767 | 10.4161/rna.8.1.13346 | 10.1128/mBio.01049-21 | Genome-Wide Essentiality Analysis of Mycobacterium abscessus by Saturated Transp |
| 34130621 | 10.1093/gbe/evaa023 | 10.1186/s12859-021-04242-0 | Simulation study and comparative evaluation of viral contiguous sequence identif |
| 34132590 | 10.1007/978-1-4939-3578-9_16 | 10.1128/AEM.00467-21 | Legionella pneumophila CRISPR-Cas Suggests Recurrent Encounters with One or More |
| 34136415 | 10.1016/j.synbio.2020.09.003 | 10.3389/fcimb.2021.635597 | Rekindling of a Masterful Precedent; Bacteriophage: Reappraisal and Future Pursu |
| 34150671 | 10.1136/gutjnl-2017-313952 | 10.3389/fcimb.2021.643214 | The Human Gut Phageome: Origins and Roles in the Human Gut Microbiome. |
| 34154404 | 10.3892/ijmm_00000491 | 10.1128/mBio.00746-21 | Inhibition of Fibrinolysis by Streptococcal Phage LysinSM1. |
| 34154528 | 10.1128/AAC.01123-10 | 10.1186/s12866-021-02251-w | Isolation and characterization of lytic phage TUN1 specific for Klebsiella pneum |
| 34156288 | 10.3354/meps072205 | 10.1128/mSystems.00193-21 | Filamentous Bacteriophages and the Competitive Interaction between Pseudomonas a |
| 34156584 | 10.1007/s00253-018-8811-1 | 10.1007/s11262-021-01847-8 | Identification of a phage-derived depolymerase specific for KL64 capsule of Kleb |
| 34160257 | 10.3390/v9090255 | 10.1128/JVI.00485-21 | Potent Human Single-Domain Antibodies Specific for a Novel Prefusion Epitope of  |
| 34165717 | 10.1016/j.stem.2015.02.001 | 10.1007/978-1-0716-1503-4_13 | Chromatin Regulation at Parental Gene Promoters by Pseudogene Sense lncRNAs. |
| 34169446 | 10.1093/cid/ciaa803 | 10.1007/s10096-021-04296-1 | Treatment for carbapenem-resistant Enterobacterales infections: recent advances  |
| 34177601 | 10.1097/qco.0000000000000024 | 10.3389/fphar.2021.692614 | Case Report: Chronic Bacterial Prostatitis Treated With Phage Therapy After Mult |
| 34178726 | 10.1093/femsle/fnw186 | 10.3389/fcimb.2021.689770 | Phage vB_PaeS-PAJD-1 Rescues Murine Mastitis Infected With Multidrug-Resistant P |
| 34194425 | 10.1128/mBio.01874-17 | 10.3389/fimmu.2021.639570 | Immune Response to Therapeutic Staphylococcal Bacteriophages in Mammals: Kinetic |
| 34198741 | 10.3390/v11020096 | 10.3390/antibiotics10060675 | The Potential Role of Bacteriophages in the Treatment of Recalcitrant Chronic Rh |
| 34199889 | 10.3390/v11040352 | 10.3390/antibiotics10060672 | Advances in Bacteriophage Therapy against Relevant MultiDrug-Resistant Pathogens |
| 34200458 | 10.1016/S2468-1253(20)30048-0 | 10.3390/v13061089 | Bacteriophages as Fecal Pollution Indicators. |
| 34200586 | 10.1093/infdis/jis733 | 10.3390/v13061113 | Mixed Bacteriophage MS2-L2 VLPs Elicit Long-Lasting Protective Antibodies agains |
| 34200959 | 10.1007/s12026-020-09159-z | 10.3390/v13061120 | Discovery of Antivirals Using Phage Display. |
| 34202166 | 10.1111/jpi.12502 | 10.3390/ijms22136842 | A Novel Cu(II)-Binding Peptide Identified by Phage Display Inhibits Cu2+-Mediate |
| 34204417 | 10.1186/1742-4682-11-30 | 10.3390/pathogens10060765 | Human Single-Chain Antibodies That Neutralize Elastolytic Activity of Pseudomona |
| 34204897 | 10.1038/d41586-020-02418-x | 10.3390/v13061057 | The Potential of Phage Therapy against the Emerging Opportunistic Pathogen Steno |
| 34205687 | 10.1089/vim.2013.0128 | 10.3390/v13061182 | Successful Treatment of Staphylococcus aureus Prosthetic Joint Infection with Ba |
| 34206009 | 10.1093/nar/gky300 | 10.3390/ijms22115989 | Computational-Driven Epitope Verification and Affinity Maturation of TLR4-Target |
| 34206124 | 10.1039/D0SC01699C | 10.3390/molecules26113338 | Biosynthetic Strategies for Macrocyclic Peptides. |
| 34207911 | 10.1038/srep26240 | 10.3390/ijms22126240 | Semi-Automated Cell Panning for Efficient Isolation of FGFR3-Targeting Antibody. |
| 34208170 | 10.1128/jb.134.1.84-91.1978 | 10.3390/toxins13060416 | Escherichia coli Shiga Toxins and Gut Microbiota Interactions. |
| 34209474 | 10.1093/nar/gku1223 | 10.3390/genes12070990 | Revealing the Viral Community in the Hadal Sediment of the New Britain Trench. |
| 34209836 | 10.3389/fmicb.2016.01209 | 10.3390/v13071268 | The Safety and Toxicity of Phage Therapy: A Review of Animal and Clinical Studie |
| 34209998 | 10.3390/biom10071001 | 10.3390/ijms22137031 | Therapeutic Effect of a Newly Isolated Lytic Bacteriophage against Multi-Drug-Re |
| 34211469 | 10.1038/nmeth.1607 | 10.3389/fimmu.2021.678570 | Cross-Reactive SARS-CoV-2 Neutralizing Antibodies From Deep Mining of Early Pati |
| 34222050 | 10.1101/gr.074492.107 | 10.3389/fcimb.2021.686090 | Characterisation of Bacteriophage-Encoded Depolymerases Selective for Key Klebsi |
| 34222051 | 10.3390/antibiotics9060304 | 10.3389/fcimb.2021.690377 | Bacteriophage Cocktails Protect Dairy Cows Against Mastitis Caused By Drug Resis |
| 34223815 | 10.1016/j.meegid.2013.04.030 | 10.1099/mgen.0.000601 | Exploring the evolution and epidemiology of European CC1-MRSA-IV: tracking a mul |
| 34224110 | 10.1101/2020.06.12.148726 | 10.1007/s12250-021-00409-4 | Antibody Cocktail Exhibits Broad Neutralization Activity Against SARS-CoV-2 and  |
| 34224345 | 10.1126/science.1106469 | 10.1099/mic.0.001066 | Phase-variable bacteria simultaneously express multiple capsules. |
| 34228538 | 10.1128/AAC.01533-08 | 10.1128/AAC.00900-21 | Enhanced Antibacterial Activity of Repurposed Mitomycin C and Imipenem in Combin |
| 34232073 | 10.1093/bioinformatics/btr039 | 10.1128/mSphere.00452-21 | Distribution of Antimicrobial Resistance and Virulence Genes within the Prophage |
| 34233201 | 10.1101/767376 | 10.1016/j.str.2021.06.010 | Selection and structural characterization of anti-TREM2 scFvs that reduce levels |
| 34234269 | 10.1038/ncomms10501 | 10.1038/s41401-021-00707-3 | A novel and effective approach to generate germline-like monoclonal antibodies b |
| 34238738 | 10.1136/gutjnl-2020-323263 | 10.12122/j.issn.1673-4254.2021.06.08 | [Characteristics of gut virome and microbiome in patients with stroke]. |
| 34251609 | 10.3390/v11020096 | 10.1007/s42770-021-00566-4 | Overview of the risks of Staphylococcus aureus infections and their control by b |
| 34254028 | 10.1101/586115:586115 | 10.1093/emph/eoaa026 | Phage steering of antibiotic-resistance evolution in the bacterial pathogen, Pse |
| 34254156 | 10.3389/fmicb.2019.00420 | 10.1007/s00253-021-11432-6 | |Isolation and characterization of novel bacteriophages as a potential therapeut |
| 34254979 | 10.7554/eLife.58823 | 10.1085/jgp.202112873 | Zinc binding alters the conformational dynamics and drives the transport cycle o |
| 34259504 | 10.1097/ftd.0b013e318166eba0 | 10.1021/acs.analchem.1c02109 | Recombinant Peptide Mimetic NanoLuc Tracer for Sensitive Immunodetection of Myco |
| 34260404 | 10.5281/zenodo.4379347 | 10.1073/pnas.2104242118 | A conserved epitope III on hepatitis C virus E2 protein has alternate conformati |
| 34261128 | 10.15252/embr.202051252 | 10.1038/s41586-021-03800-z | Two cGAS-like receptors induce antiviral immunity in Drosophila. |
| 34261503 | 10.1093/bioinformatics/btq033 | 10.1186/s13059-021-02427-7 | Genomic diversity and ecology of human-associated Akkermansia species in the gut |
| 34261793 | 10.1101/2021.04.01.437943 | 10.1073/pnas.2106203118 | In vitro affinity maturation of broader and more-potent variants of the HIV-1-ne |
| 34273271 | 10.1101/2021.03.03.21252812 | 10.1016/j.celrep.2021.109433 | A SARS-CoV-2 neutralizing antibody selected from COVID-19 patients binds to the  |
| 34280017 | 10.1093/bioinformatics/btx162 | 10.1128/AAC.00659-21 | Exploration of Synergistic Action of Cell Wall-Degrading Enzymes against Mycobac |
| 34281490 | 10.1080/19420862.2021.1924347 | 10.1080/19420862.2021.1950265 | Animal- versus in vitro-derived antibodies: avoiding the extremes. |
| 34282933 | 10.1007/s00705-018-3811-0 | 10.1128/mSystems.00218-21 | The Future of Bacteriophage Therapy Will Promote Antimicrobial Susceptibility. |
| 34290683 | 10.1128/AAC.00635-06 | 10.3389/fmicb.2021.682255 | The Efficacy of Phage Therapy in a Murine Model of Pseudomonas aeruginosa Pneumo |
| 34292970 | 10.1093/nar/gku734 | 10.1371/journal.pone.0254382 | Genomic insights into methicillin-resistant Staphylococcus pseudintermedius isol |
| 34295840 | 10.1016/j.meegid.2013.04.022 | 10.3389/fcimb.2021.698909 | Phenotypic and Genotypic Characterization of Novel Polyvalent Bacteriophages Wit |
| 34299376 | 10.1093/nar/gkab125 | 10.3390/ijms22147758 | Mutational Analysis of Redβ Single Strand Annealing Protein: Roles of the 14 Lys |
| 34307189 | 10.1136/gutjnl-2017-313952 | 10.3389/fcimb.2021.657867 | Alterations, Interactions, and Diagnostic Potential of Gut Bacteria and Viruses  |
| 34307196 | 10.1016/j.ibmb.2015.02.002 | 10.3389/fcimb.2021.697876 | Developing Recombinant Antibodies by Phage Display Against Infectious Diseases a |
| 34309796 | 10.1016/S0140-6736(05)70155-0 | 10.1007/s12033-021-00371-2 | Alternatives to Conventional Antibiotic Therapy: Potential Therapeutic Strategie |
| 34321079 | 10.1155/2016/2987140 | 10.1186/s13287-021-02506-3 | Mkx mediates tenogenic differentiation but incompletely inhibits the proliferati |
| 34323607 | 10.1016/j.virusres.2013.01.021 | 10.1128/MRA.00489-21 | Complete Genome Sequence of Pseudomonas Phage Zikora. |
| 34326184 | 10.1101/2020.09.01.20182220 | 10.1126/sciimmunol.abe9950 | Cross-reactive antibodies against human coronaviruses and the animal coronavirom |
| 34326207 | 10.1098/rstb.2018.0089 | 10.1126/science.abg2166 | Temporal shifts in antibiotic resistance elements govern phage-pathogen conflict |
| 34328615 | 10.1016/j.arth.2013.08.017 | 10.1007/s15010-021-01675-w | Observed transaminitis with a unique bacteriophage therapy protocol to treat rec |
| 34328665 | 10.1038/s41467-017-02057-3 | 10.1002/1878-0261.13070 | Metagenomic analysis of primary colorectal carcinomas and their metastases ident |
| 34336189 | 10.2139/ssrn.3582780 | 10.12688/f1000research.52540.3 | Increase of SARS-CoV-2 RNA load in faecal samples prompts for rethinking of SARS |
| 34336721 | 10.1016/j.isci.2020.101437 | 10.3389/fcimb.2021.698807 | Characterization of an Enterococcus faecalis Bacteriophage vB_EfaM_LG1 and Its S |
| 34338580 | 10.1101/2020.04.16.20067835. | 10.1177/00220345211032885 | Dental Mitigation Strategies to Reduce Aerosolization of SARS-CoV-2. |
| 34338634 | 10.1038/s41586-020-2951-z | 10.7554/eLife.64815 | The development of Nanosota-1 as anti-SARS-CoV-2 nanobody drug candidates. |
| 34339765 | 10.1053/j.gastro.2020.02.055 | 10.1016/j.jviromet.2021.114249 | Evaluation of low-cost viral concentration methods in wastewaters: Implications  |
| 34346352 | 10.1053/j.gastro.2020.03.020 | 10.1016/j.scitotenv.2021.149112 | Somatic coliphages are conservative indicators of SARS-CoV-2 inactivation during |
| 34347517 | 10.1016/j.jtbi.2006.08.017 | 10.1128/AEM.00980-21 | Bacteriophage Treatment before Chemical Disinfection Can Enhance Removal of Plas |
| 34348076 | 10.1158/0008-5472.CAN-17-0337 | 10.1080/19420862.2021.1958663 | Development of potent and effective synthetic SARS-CoV-2 neutralizing nanobodies |
| 34356798 | 10.1007/978-1-4939-0473-0_8 | 10.3390/antibiotics10070877 | Pseudomonas aeruginosa PAO 1 In Vitro Time-Kill Kinetics Using Single Phages and |
| 34361054 | 10.1016/0022-2836(70)90057-4 | 10.3390/ijms22158288 | Anti-Idiotype scFv Localizes an Autoepitope in the Globular Domain of C1q. |
| 34370558 | 10.1098/rstb.2015.0021 | 10.1128/JB.00104-21 | Investigating the Process of Sheath Maturation in Antifeeding Prophage: a Phage  |
| 34372537 | 10.1128/IAI.01249-07 | 10.3390/v13071331 | Advances in Phage Therapy: Targeting the Burkholderia cepacia Complex. |
| 34372538 | 10.1128/IAI.66.9.4244-4253.1998 | 10.3390/v13071332 | Emerging Phage Resistance in Pseudomonas aeruginosa PAO1 Is Accompanied by an En |
| 34372554 | 10.1089/mdr.2020.0083 | 10.3390/v13071348 | Characterization of Anti-Bacterial Effect of the Two New Phages against Uropatho |
| 34372580 | 10.1128/JB.00058-17 | 10.3390/v13071376 | Aerobic Conditions and Endogenous Reactive Oxygen Species Reduce the Production  |
| 34372584 | 10.1111/j.1574-6976.2007.00088.x | 10.3390/v13071377 | The Mycobacteriophage Ms6 LysB N-Terminus Displays Peptidoglycan Binding Affinit |
| 34372595 | 10.3390/v11100951 | 10.3390/v13071389 | Ecological Approach to Understanding Superinfection Inhibition in Bacteriophage. |
| 34373446 | 10.1038/s41422-020-0282-0 | 10.1038/s41467-021-25153-x | Identification of potent human neutralizing antibodies against SARS-CoV-2 implic |
| 34373631 | 10.1128/mBio.00362-12 | 10.1038/s41579-021-00602-y | Interactions between bacterial and phage communities in natural environments. |
| 34378963 | 10.1038/s41467-019-10656-5 | 10.1128/Spectrum.00077-21 | Use of Recombinant Endolysin to Improve Accuracy of Group B Streptococcus Tests. |
| 34378967 | 10.1128/AEM.00062-07 | 10.1128/Spectrum.00599-21 | Bacteriophage: A Useful Tool for Studying Gut Bacteria Function of Housefly Larv |
| 34379161 | 10.1016/j.cub.2011.11.055 | 10.1007/s00203-021-02511-3 | Novel PhoH-encoding vibriophages with lytic activity against environmental Vibri |
| 34400725 | 10.1111/j.1744-7917.1995.tb00045.x | 10.1038/s41598-021-96133-w | Comparative genome analysis of Bacillus thuringiensis strain HD521 and HS18-1. |
| 34403037 | 10.1186/1743-422X-10-266 | 10.1007/s12250-021-00436-1 | Generation and Characterization of a Nanobody Against SARS-CoV. |
| 34407825 | 10.1038/nature09199 | 10.1186/s12915-021-01084-3 | Long-term persistence of crAss-like phage crAss001 is associated with phase vari |
| 34411388 | 10.1155/2016/1548326 | 10.1111/jam.15262 | Direct and quantitative capture of viable bacteriophages from experimentally con |
| 34417258 | 10.1371/journal.pone.0017433 | 10.1126/sciimmunol.abg4925 | A high-affinity human TCR-like antibody detects celiac disease gluten peptide-MH |
| 34417565 | 10.1101/2021.06.25.449885v1 | 10.1038/s41396-021-01090-x | Phages in the infant gut: a framework for virome development during early life. |
| 34427831 | 10.1126/sciimmunol.aax7965 | 10.1007/s10875-021-01115-2 | A Novel STK4 Mutation Impairs T Cell Immunity Through Dysregulation of Cytokine- |
| 34431719 | 10.18637/jss.v069.i01 | 10.1128/Spectrum.00497-21 | Prophylactic Administration of a Bacteriophage Cocktail Is Safe and Effective in |
| 34438996 | 10.1093/femsec/fiy107 | 10.3390/antibiotics10080946 | Successful Intratracheal Treatment of Phage and Antibiotic Combination Therapy o |
| 34445373 | 10.1038/s41564-021-00932-w | 10.3390/ijms22168660 | SARS-CoV-2: Understanding the Transcriptional Regulation of ACE2 and TMPRSS2 and |
| 34445637 | 10.1016/j.clim.2014.04.003 | 10.3390/ijms22168931 | The Binding of Monoclonal and Polyclonal Anti-Z-DNA Antibodies to DNA of Various |
| 34445641 | 10.1016/j.cels.2020.02.006 | 10.3390/ijms22168937 | Interactions of Bacteriophages with Animal and Human Organisms-Safety Issues in  |
| 34452284 | 10.1093/nar/13.20.7473 | 10.3390/v13081418 | Novel Viruses That Lyse Plant and Human Strains of Kosakonia cowanii. |
| 34452328 | 10.1111/j.1472-765X.2008.02542.x | 10.3390/v13081462 | Enzyme-Linked Phage Receptor Binding Protein Assays (ELPRA) Enable Identificatio |
| 34452408 | 10.1038/nrmicro.2017.61 | 10.3390/v13081543 | Bacteriophage Therapy for Difficult-to-Treat Infections: The Implementation of a |
| 34452479 | 10.15252/embr.201847427 | 10.3390/v13081614 | The Repressor C Protein, Pf4r, Controls Superinfection of Pseudomonas aeruginosa |
| 34452490 | 10.3390/v7082847 | 10.3390/v13081626 | Characterization and Application of a Lytic Phage D10 against Multidrug-Resistan |
| 34460060 | 10.1186/s12866-019-1443-5 | 10.1007/s11033-021-06690-6 | Multidrug-resistant Acinetobacter baumannii as an emerging concern in hospitals. |
| 34465897 | 10.1093/bioinformatics/bts480 | 10.1038/s41396-021-01096-5 | Genome-driven elucidation of phage-host interplay and impact of phage resistance |
| 34467445 | 10.1007/s12560-021-09460-6 | 10.1007/s00248-021-01846-0 | Bacteriophage-Mediated Risk Pathways Underlying the Emergence of Antimicrobial R |
| 34468190 | 10.1128/AAC.02471-16 | 10.1128/Spectrum.00217-21 | Complete Genetic Analysis of Plasmids Carried by Two Nonclonal blaNDM-5- and mcr |
| 34468308 | 10.1128/mBio.03431-20 | 10.1099/mic.0.001094 | Wildy Prize Lecture, 2020-2021: Who wouldn't want to discover a new virus? |
| 34469200 | 10.5014/ajot.49.4.318 | 10.1128/AEM.01215-21 | Transfer Rate of Enveloped and Nonenveloped Viruses between Fingerpads and Surfa |
| 34481243 | 10.3899/jrheum.140767 | 10.1016/j.ebiom.2021.103506 | Citrullination of a phage-displayed human peptidome library reveals the fine spe |
| 34487189 | 10.1128/Jcm.42.11.4947-4955.2004 | 10.1007/s00203-021-02564-4 | The evaluation of five commercial bacteriophage cocktails against methicillin-re |
| 34490477 | 10.1007/978-1-62703-541-5_3 | 10.3892/mmr.2021.12407 | Parallel evaluation of cell‑based phage display panning strategies: Optimized se |
| 34491998 | 10.1093/bioinformatics/btr261 | 10.1371/journal.pgen.1009761 | The CovR regulatory network drives the evolution of Group B Streptococcus virule |
| 34495736 | 10.1061/(ASCE)0733-9372(1997)123:11(1142) | 10.1128/AEM.01532-21 | UV Inactivation of SARS-CoV-2 across the UVC Spectrum: KrCl* Excimer, Mercury-Va |
| 34498685 | 10.5524/100918 | 10.1093/gigascience/giab056 | DeePhage: distinguishing virulent and temperate phage-derived sequences in metav |
| 34499212 | 10.1056/NEJMra040181 | 10.1007/s00132-021-04148-y | [Treatment of bone and periprosthetic infections with bacteriophages : A systema |
| 34500572 | 10.3390/v10040205 | 10.3390/molecules26175138 | Phages and Enzybiotics in Food Biopreservation. |
| 34502431 | 10.7326/0003-4819-96-1-1 | 10.3390/ijms22179518 | Antimicrobial Face Shield: Next Generation of Facial Protective Equipment agains |
| 34502483 | 10.1177/0300985813485099 | 10.3390/ijms22179579 | Anti-Cancer Effects of Cyclic Peptide ALOS4 in a Human Melanoma Mouse Model. |
| 34511602 | 10.1038/nature21671 | 10.1038/s41419-021-04140-6 | EMP3 negatively modulates breast cancer cell DNA replication, DNA damage repair, |
| 34512672 | 10.1084/jem.20052319 | 10.3389/fimmu.2021.740395 | HIV Antibody Profiles in HIV Controllers and Persons With Treatment-Induced Vira |
| 34523959 | 10.1038/s41564-021-00930-y | 10.1128/MMBR.00091-21 | DNA Repair in Staphylococcus aureus. |
| 34524200 | 10.1089/fpd.2020.2833 | 10.1097/QCO.0000000000000772 | Bacteriophages against enteropathogens: rediscovery and refinement of novel anti |
| 34530447 | 10.1128/IAI.00743-09 | 10.1242/dmm.049159 | Mycobacteriophage-antibiotic therapy promotes enhanced clearance of drug-resista |
| 34539634 | 10.1182/blood-2006-12-061812 | 10.3389/fimmu.2021.703574 | Mouse CD38-Specific Heavy Chain Antibodies Inhibit CD38 GDPR-Cyclase Activity an |
| 34552126 | 10.1021/bi000290w | 10.1038/s41598-021-97871-7 | Deep mutational scanning of the plasminogen activator inhibitor-1 functional lan |
| 34556764 | 10.1099/vir.0.80320-0 | 10.1038/s41598-021-98432-8 | Comparative analysis of prophages carried by human and animal-associated Staphyl |
| 34559314 | 10.1016/j.tplants.2020.01.013 | 10.1007/s00705-021-05241-5 | Efficacy of three lytic bacteriophages for eradicating biofilms of multidrug-res |
| 34566987 | 10.1007/s00262-013-1443-5 | 10.3389/fimmu.2021.729336 | Filamentous Bacteriophage-A Powerful Carrier for Glioma Therapy. |
| 34566992 | 10.1084/jem.20210281 | 10.3389/fimmu.2021.730471 | Engineering an Antibody V Gene-Selective Vaccine. |
| 34569248 | 10.1161/CIRCRESAHA.118.312804 | 10.1161/JAHA.120.016287 | In Vivo Human Single-Chain Fragment Variable Phage Display-Assisted Identificati |
| 34571955 | 10.1038/sj.embor.7400290 | 10.3390/cells10092307 | Identification and Characterization of an Affimer Affinity Reagent for the Detec |
| 34575870 | 10.2217/pgs-2019-0184 | 10.3390/ijms22189712 | Building Personalized Cancer Therapeutics through Multi-Omics Assays and Bacteri |
| 34575991 | 10.1016/0076-6879(94)35170-8 | 10.3390/ijms22189830 | The In Vitro Anti-Pseudomonal Activity of Cu2+, Strawberry Furanone, Gentamicin, |
| 34576896 | 10.1111/j.1365-2672.2011.05043.x | 10.3390/microorganisms9092001 | Preclinical Development of a Bacteriophage Cocktail for Treating Multidrug Resis |
| 34578208 | 10.1038/s41467-021-21718-y | 10.3390/pathogens10091177 | Staphylococcus aureus and Cystic Fibrosis-A Close Relationship. What Can We Lear |
| 34578303 | 10.3390/v13040605 | 10.3390/v13091723 | Dual Promoters Improve the Rescue of Recombinant Measles Virus in Human Cells. |
| 34578313 | 10.1186/s40168-019-0779-2 | 10.3390/v13091734 | Examining the Effects of an Anti-Salmonella Bacteriophage Preparation, BAFASAL®, |
| 34578333 | 10.3390/cancers6010333 | 10.3390/v13091754 | Bacteriophages M13 and T4 Increase the Expression of Anchorage-Dependent Surviva |
| 34578366 | 10.1016/j.addr.2019.01.003 | 10.3390/v13091785 | Bacteriophage Rescue Therapy of a Vancomycin-Resistant Enterococcus faecium Infe |
| 34578390 | 10.3390/v10040178 | 10.3390/v13091809 | Phage Therapy for Multi-Drug Resistant Respiratory Tract Infections. |
| 34578429 | 10.1111/1751-7915.13594 | 10.3390/v13091848 | Characterization of a Novel Phage ΦAb1656-2 and Its Endolysin with Higher Antimi |
| 34579784 | 10.1183/13993003.00582-2017 | 10.1186/s13104-021-05796-1 | Searching for synergy: combining systemic daptomycin treatment with localised ph |
| 34582688 | 10.1016/j.chroma.2021.462506 | 10.1021/acs.analchem.1c02807 | Enrichment and Liquid Chromatography-Mass Spectrometry Analysis of Trastuzumab a |
| 34583680 | 10.1002/adfm.201700995 | 10.1186/s12951-021-01047-4 | An atherosclerotic plaque-targeted single-chain antibody for MR/NIR-II imaging o |
| 34588479 | 10.1371/journal.pone.0205728 | 10.1038/s41598-021-98457-z | Isolation and characterization of a lytic bacteriophage against Pseudomonas aeru |
| 34588569 | 10.1093/nar/gki366 | 10.1038/s41598-021-98910-z | Morphological, biological, and genomic characterization of a newly isolated lyti |
| 34588605 | 10.1126/science.1150609 | 10.1038/s12276-021-00678-9 | A human antibody against human endothelin receptor type A that exhibits antitumo |
| 34590284 | 10.1016/0076-6879(87)54085-x | 10.1007/978-1-0716-1740-3_17 | Generation of Protein Inhibitors for Validation of Cancer Drug Targets Identifie |
| 34605137 | 10.1021/cb300709g | 10.1002/cbic.202100450 | Chemical Modification of Phage-Displayed Helix-Loop-Helix Peptides to Construct  |
| 34606423 | 10.1093/nar/gkab521 | 10.1080/15476286.2021.1985347 | Structural insights into the inactivation of the type I-F CRISPR-Cas system by a |
| 34606796 | 10.1016/j.buildenv.2019.05.005 | 10.1016/j.jviromet.2021.114307 | Phi 6 recovery from inoculated fingerpads based on elution buffer and methodolog |
| 34610400 | 10.1016/j.scitotenv.2021.145124 | 10.1016/j.scitotenv.2021.150722 | Comparison of five polyethylene glycol precipitation procedures for the RT-qPCR  |
| 34615923 | 10.1089/nat.2016.0660 | 10.1038/s41598-021-98706-1 | Optimizing the synthesis and purification of MS2 virus like particles. |
| 34630431 | 10.1093/nar/gkv1267 | 10.3389/fimmu.2021.752898 | The SARM1 TIR NADase: Mechanistic Similarities to Bacterial Phage Defense and To |
| 34631490 | 10.4161/bact.1.2.15845 | 10.34172/bi.2021.10 | Evaluation of in-situ gel-forming eye drop containing bacteriophage against Pseu |
| 34632543 | 10.1038/nature18615 | 10.1007/s12250-021-00454-z | Identification and Characterization of a Novel Single Domain Antibody Against Eb |
| 34635758 | 10.1016/j.ijpharm.2012.01.051 | 10.1038/s41598-021-99696-w | Development of peptides targeting receptor binding site of the envelope glycopro |
| 34637549 | 10.1101/2021.01.25.427948 | 10.1096/fj.202100986RR | Single domain shark VNAR antibodies neutralize SARS-CoV-2 infection in vitro. |
| 34638603 | 10.1038/nprot.2009.22 | 10.3390/ijms221910263 | Tagging and Capturing of Lentiviral Vectors Using Short RNAs. |
| 34638776 | 10.4014/jmb.2005.05040 | 10.3390/ijms221910436 | Phage Therapy as a Focused Management Strategy in Aquaculture. |
| 34638896 | 10.1002/0471142727.mb2314s95 | 10.3390/ijms221910558 | Optimization of a Lambda-RED Recombination Method for Rapid Gene Deletion in Hum |
| 34662188 | 10.3390/antibiotics9050241 | 10.1128/AAC.00824-21 | Critically Ill Patient with Multidrug-Resistant Acinetobacter baumannii Respirat |
| 34662191 | 10.1093/jac/dkt374 | 10.1128/AAC.01879-21 | Phage Activity against Planktonic and Biofilm Staphylococcus aureus Periprosthet |
| 34668031 | 10.1016/j.micpath.2017.02.045 | 10.1007/s00203-021-02595-x | Correlation between type IIIA CRISPR-Cas system and SCCmec in Staphylococcus epi |
| 34668728 | 10.1371/journal.ppat.1007572 | 10.1128/Spectrum.01298-21 | SARS-CoV-2 Antibody Binding and Neutralization in Dried Blood Spot Eluates and P |
| 34668734 | 10.1016/j.chom.2021.02.001 | 10.1128/CMR.00136-21 | Intestinal Bacteriophage Therapy: Looking for Optimal Efficacy. |
| 34668746 | 10.2105/SMWW.2882.195 | 10.1128/Spectrum.00537-21 | Robust Evaluation of Ultraviolet-C Sensitivity for SARS-CoV-2 and Surrogate Coro |
| 34669452 | 10.3389/fmicb.2016.00577 | 10.1128/AEM.01515-21 | Engineering a Lysin with Intrinsic Antibacterial Activity (LysMK34) by Cecropin  |
| 34672917 | 10.1073/pnas.1506279112 | 10.1099/mic.0.001115 | Microbial Musings - September 2021. |
| 34673779 | 10.1371/journal.pcbi.1005944 | 10.1371/journal.pcbi.1009428 | Comprehensive discovery of CRISPR-targeted terminally redundant sequences in the |
| 34675140 | 10.1007/s002390010140 | 10.4014/jmb.2110.10003 | Applicability Evaluation of Male-Specific Coliphage-Based Detection Methods for  |
| 34678315 | 10.1101/2021.03.18.436013 | 10.1016/j.jbc.2021.101290 | Development of a highly specific and sensitive VHH-based sandwich immunoassay fo |
| 34680793 | 10.1101/pdb.prot095505 | 10.3390/antibiotics10101212 | Antibacterial, Antifungal and Anticancer Activities of Compounds Produced by New |
| 34681646 | 10.1093/cvr/cvv205 | 10.3390/ijms222010985 | Recent Advances in CRISPR/Cas9-Based Genome Editing Tools for Cardiac Diseases. |
| 34681796 | 10.1093/nar/gky427 | 10.3390/ijms222011136 | Human Antibody Domains and Fragments Targeting Neutrophil Elastase as Candidate  |
| 34683360 | 10.1016/j.jmb.2006.03.043 | 10.3390/microorganisms9102040 | The Characterization of a Novel Phage, pPa_SNUABM_DT01, Infecting Pseudomonas ae |
| 34688274 | 10.1093/bioinformatics/btx157 | 10.1186/s12864-021-08080-5 | Long-read sequencing-based in silico phage typing of vancomycin-resistant Entero |
| 34694874 | 10.1128/AAC.00824-21 | 10.1128/AAC.01996-21 | Case Commentary: Novel Therapy for Multidrug-Resistant Acinetobacter baumannii I |
| 34696328 | 10.3389/fmicb.2018.00127 | 10.3390/v13101898 | A Case of In Situ Phage Therapy against Staphylococcus aureus in a Bone Allograf |
| 34696331 | 10.1186/s13073-018-0525-6 | 10.3390/v13101901 | Phage Therapy Experience at the Eliava Phage Therapy Center: Three Cases of Bact |
| 34696356 | 10.3389/fmicb.2016.00882 | 10.3390/v13101926 | A Design of Experiment Approach to Optimize Spray-Dried Powders Containing Pseud |
| 34696396 | 10.1038/s41564-019-0634-z | 10.3390/v13101965 | Phages from Genus Bruynoghevirus and Phage Therapy: Pseudomonas Phage Delta Case |
| 34696475 | 10.1016/j.it.2017.01.006 | 10.3390/v13102044 | In Vitro Evaluation of the Therapeutic Potential of Phage VA7 against Enterotoxi |
| 34696479 | 10.1007/s11095-010-0313-5 | 10.3390/v13102049 | Phage Therapy Related Microbial Succession Associated with Successful Clinical O |
| 34696523 | 10.1186/1471-2180-11-168 | 10.3390/v13102093 | Comparison of PCR versus PCR-Free DNA Library Preparation for Characterising the |
| 34697726 | 10.1002/btm2.10159 | 10.1007/s11095-021-03111-y | Manufacturing Stable Bacteriophage Powders by Including Buffer System in Formula |
| 34699013 | 10.1128/JB.00975-12 | 10.1007/s12602-021-09868-3 | Distribution of Genes Related to Probiotic Effects Across Lacticaseibacillus rha |
| 34710374 | 10.1038/s41391-021-00394-5 | 10.1016/j.jbc.2021.101342 | The development of a high-affinity conformation-sensitive antibody mimetic using |
| 34712234 | 10.1002/jps.22267 | 10.3389/fimmu.2021.745625 | Bacteriophage T4 Vaccine Platform for Next-Generation Influenza Vaccine Developm |
| 34713608 | 10.1086/315239 | 10.1002/mbo3.1245 | Characterization of the genetic switch from phage ɸ13 important for Staphylococc |
| 34717584 | 10.1111/j.1537-2995.2012.03960.x | 10.1186/s12879-021-06717-0 | Isolation and characterization of high affinity and highly stable anti-Chikungun |
| 34721353 | 10.1038/srep29344 | 10.3389/fmicb.2021.748718 | Discovering the Potentials of Four Phage Endolysins to Combat Gram-Negative Infe |
| 34736365 | 10.1007/978-1-4939-0554-6_12 | 10.1080/22221751.2021.2002671 | Colistin-phage combinations decrease antibiotic resistance in Acinetobacter baum |
| 34737586 | 10.1038/s41598-018-37636-x | 10.2147/IDR.S326230 | Evaluation of Phage Therapy for Pulmonary Infection of Mouse by Liquid Aerosol-E |
| 34747690 | 10.1007/s00705-020-04752-x | 10.1099/mgen.0.000686 | Leviviricetes: expanding and restructuring the taxonomy of bacteria-infecting si |
| 34766210 | 10.1038/ismej.2008.110 | 10.1007/s00248-021-01914-5 | Metagenomics Analysis to Investigate the Microbial Communities and Their Functio |
| 34768992 | 10.1093/bioinformatics/btu830 | 10.3390/ijms222111562 | The Mutation in wbaP cps Gene Cluster Selected by Phage-Borne Depolymerase Aboli |
| 34769055 | 10.3201/eid2005.130953 | 10.3390/ijms222111626 | Clustered Regularly Interspaced Short Palindromic Repeat Analysis of Clonal Comp |
| 34770973 | 10.1007/s12032-014-0110-9 | 10.3390/molecules26216564 | Modification of a Tumor-Targeting Bacteriophage for Potential Diagnostic Applica |
| 34773197 | 10.1073/pnas.1415191111 | 10.1007/s11357-021-00469-0 | Diabetes mellitus correlates with increased biological age as indicated by clini |
| 34782783 | 10.1093/cid/ciz782 | 10.1038/s41575-021-00536-z | Bacteriophages and their potential for treatment of gastrointestinal diseases. |
| 34787444 | 10.1093/nar/gku1046 | 10.1128/mSphere.00799-21 | Characterization of the Type I Restriction Modification System Broadly Conserved |
| 34787450 | 10.1002/wics.147 | 10.1128/mSphere.00725-21 | Deciphering Multidrug-Resistant Acinetobacter baumannii from a Pediatric Cancer  |
| 34788068 | 10.1128/iai.48.1.124-129.1985 | 10.1128/AEM.01514-21 | Selection for Phage Resistance Reduces Virulence of Shigella flexneri. |
| 34795985 | 10.1016/s1473-3099(18)30482-1 | 10.17691/stm2020.12.3.12 | Application of Phagotherapy in the Treatment of Burn Patients (Review). |
| 34799567 | 10.1002/biot.200900035 | 10.1038/s41467-021-27109-7 | Plasmodium sporozoite phospholipid scramblase interacts with mammalian carbamoyl |
| 34800892 | 10.1101/2021.10.12.464088 | 10.1016/j.coviro.2021.10.010 | The female reproductive tract virome: understanding the dynamic role of viruses  |
| 34803517 | 10.3748/wjg.v26.i20.2498 | 10.1155/2021/6926082 | Microbiota, Bacterial Carbonic Anhydrases, and Modulators of Their Activity: Lin |
| 34809462 | 10.1038/nmicrobiol.2016.77 | 10.1128/mBio.02893-21 | SOS-Independent Pyocin Production in P. aeruginosa Is Induced by XerC Recombinas |
| 34818102 | 10.1128/mSphereDirect.00331-17 | 10.1128/AEM.01486-21 | Cross-Genus "Boot-Up" of Synthetic Bacteriophage in Staphylococcus aureus by Usi |
| 34821965 | 10.1016/j.mib.2013.08.008 | 10.1007/s00253-021-11695-z | Phage therapeutics: from promises to practices and prospectives. |
| 34822608 | 10.3390/toxins4090729 | 10.3390/toxins13110825 | The Deleterious Effects of Shiga Toxin Type 2 Are Neutralized In Vitro by FabF8: |
| 34828356 | 10.1016/j.ijfoodmicro.2020.108510 | 10.3390/genes12111752 | The Staphylococcus aureus CC398 Lineage: An Evolution Driven by the Acquisition  |
| 34830219 | 10.1002/ijc.31092 | 10.3390/ijms222212335 | Intrabody Targeting HIF-1α Mediates Transcriptional Downregulation of Target Gen |
| 34830335 | 10.1093/nar/gkz935 | 10.3390/ijms222212460 | Characterization and Genome Study of Novel Lytic Bacteriophages against Prevaili |
| 34830420 | 10.1021/cb400060x | 10.3390/ijms222212538 | Chemoenzymatic Synthesis and Antibody Binding of HIV-1 V1/V2 Glycopeptide-Bacter |
| 34832944 | 10.1128/AAC.00306-13 | 10.3390/ph14111162 | Friends or Foes? Rapid Determination of Dissimilar Colistin and Ciprofloxacin An |
| 34835009 | 10.1038/s41392-021-00718-w | 10.3390/v13112201 | Monoclonal Human Antibodies That Recognise the Exposed N and C Terminal Regions  |
| 34846863 | 10.1016/j.cryobiol.2006.01.003 | 10.1021/acs.biomac.1c01187 | Polymer-Mediated Cryopreservation of Bacteriophages. |
| 34847492 | 10.1038/s41598-018-20698-2 | 10.1016/j.jss.2021.10.010 | Identifying Causative Microorganisms in Left Ventricular Assist Device Infection |
| 34850665 | 10.1016/j.ijbiomac.2018.06.105 | 10.1080/19420862.2021.1980942 | Drug-like antibodies with high affinity, diversity and developability directly f |
| 34850676 | 10.1126/science.aar4120 | 10.1099/mic.0.001110 | Functional diversity increases the efficacy of phage combinations. |
| 34855624 | 10.1101/2020.11.28.402297 | 10.1172/jci.insight.151518 | Pharmacokinetics of high-titer anti-SARS-CoV-2 human convalescent plasma in high |
| 34856888 | 10.1186/s40168-018-0450-3 | 10.1080/19420862.2021.2004638 | Development of a fully canine anti-canine CTLA4 monoclonal antibody for comparat |
| 34872344 | 10.1128/AAC.50.1.171-177.2006 | 10.1128/mBio.02259-21 | Staphylococcal Phages Adapt to New Hosts by Extensive Attachment Site Variabilit |
| 34874249 | 10.1371/journal.pgen.1002252 | 10.1099/mgen.0.000706 | Genome reorganization during emergence of host-associated Mycobacterium abscessu |
| 34878337 | 10.3390/v11070657 | 10.1128/Spectrum.00546-21 | Design SMAP29-LysPA26 as a Highly Efficient Artilysin against Pseudomonas aerugi |
| 34878971 | 10.1016/s0966-842x(01)02173-4 | 10.1099/mgen.0.000716 | The global population structure and evolutionary history of the acquisition of m |
| 34880054 | 10.3389/fmicb.2016.00185 | 10.1136/annrheumdis-2021-221267 | Whole gut virome analysis of 476 Japanese revealed a link between phage and auto |
| 34882085 | 10.2215/CJN.08140718 | 10.1099/mgen.0.000710 | Comparative genomics of Chinese and international isolates of Escherichia albert |
| 34884521 | 10.1895/wormbook.1.101.1 | 10.3390/ijms222312719 | Non-Woven Infection Prevention Fabrics Coated with Biobased Cranberry Extracts I |
| 34884975 | 10.3390/molecules26133926 | 10.3390/ijms222313170 | (20S) Ginsenoside Rh2 Exerts Its Anti-Tumor Effect by Disrupting the HSP90A-Cdc3 |
| 34900751 | 10.3389/fmicb.2018.02247 | 10.3389/fcimb.2021.755650 | Roles of Gut Bacteriophages in the Pathogenesis and Treatment of Inflammatory Bo |
| 34900762 | 10.1053/j.gastro.2020.05.048 | 10.3389/fcimb.2021.790422 | Alterations in the Composition of Intestinal DNA Virome in Patients With COVID-1 |
| 34904653 | 10.1101/2020.06.22.160242 | 10.1093/nar/gkab1207 | Identification and classification of reverse transcriptases in bacterial genomes |
| 34907894 | 10.1186/1471-2164-15-893 | 10.1099/mgen.0.000726 | Prophages encoding human immune evasion cluster genes are enriched in Staphyloco |
| 34908451 | 10.1016/0003-2697(85)90442-7 | 10.1128/Spectrum.02094-21 | Application of Recombinant Human scFv Antibody as a Powerful Tool to Monitor Nit |
| 34908504 | 10.1016/j.gpb.2017.01.001 | 10.1128/Spectrum.00769-21 | Cerebrospinal Fluid from Healthy Pregnant Women Does Not Harbor a Detectable Mic |
| 34914049 | 10.1128/JVI.01630-20 | 10.1007/978-1-0716-1884-4_10 | CRISPR Engineering of Bacteriophage T4 to Design Vaccines Against SARS-CoV-2 and |
| 34921062 | 10.1016/j.bpj.2009.07.028 | 10.1136/gutjnl-2021-325180 | Reversal of pancreatic desmoplasia by a tumour stroma-targeted nitric oxide nano |
| 34921120 | 10.1212/NXI.0000000000001014 | 10.1136/jnnp-2021-326656 | Characterisation of TRIM46 autoantibody-associated paraneoplastic neurological s |
| 34922324 | 10.1007/BF02200721 | 10.1016/j.ebiom.2021.103747 | Deconvoluting virome-wide antibody epitope reactivity profiles. |
| 34923908 | 10.1128/jb.154.1.269-277.1983 | 10.1080/19420862.2021.2006123 | Phenotypic whole-cell screening identifies a protective carbohydrate epitope on  |
| 34925289 | 10.12688/f1000research.15931.1 | 10.3389/fmicb.2021.783722 | Survival Comes at a Cost: A Coevolution of Phage and Its Host Leads to Phage Res |
| 34926329 | 10.1016/S1473-3099(17)30628-X | 10.3389/fcimb.2021.792305 | Isolation and Characterization of Novel Phages Targeting Pathogenic Klebsiella p |
| 34935421 | 10.1007/s13238-020-00724-8 | 10.1128/Spectrum.00090-21 | Expanding the Colorectal Cancer Biomarkers Based on the Human Gut Phageome. |
| 34937862 | 10.1371/journal.pcbi.1005595 | 10.1038/s41598-021-03823-6 | Staphylococcus aureus isolates from Eurasian Beavers (Castor fiber) carry a nove |
| 34938668 | 10.1016/j.cocis.2021.101497 | 10.3389/fcimb.2021.758392 | Prospects of Inhaled Phage Therapy for Combatting Pulmonary Infections. |
| 34943709 | 10.3390/molecules14093754 | 10.3390/antibiotics10121497 | Treating Bacterial Infections with Bacteriophage-Based Enzybiotics: In Vitro, In |
| 34944435 | 10.1016/j.tibtech.2015.03.012 | 10.3390/biom11121791 | Non-Antibody-Based Binders for the Enrichment of Proteins for Analysis by Mass S |
| 34944462 | 10.1038/srep01339 | 10.3390/biom11121818 | Development of a Low-Molecular-Weight Aβ42 Detection System Using a Enzyme-Linke |
| 34946736 | 10.1016/j.biomaterials.2016.05.015 | 10.3390/molecules26247652 | Mimotopes for Mycotoxins Diagnosis Based on Random Peptides or Recombinant Antib |
| 34948232 | 10.1016/j.jviromet.2020.113856 | 10.3390/ijms222413438 | Polyethylene Films Containing Plant Extracts in the Polymer Matrix as Antibacter |
| 34948244 | 10.1371/journal.pcbi.1008214 | 10.3390/ijms222413434 | Transposable Prophages in Leptospira: An Ancient, Now Diverse, Group Predominant |
| 34949838 | 10.1038/nbt.3481 | 10.1038/s41589-021-00927-y | Precise genome editing across kingdoms of life using retron-derived DNA. |
| 34957709 | 10.1038/s41578-021-00362-4 | 10.1002/adhm.202102539 | Bacteriophage-Loaded Poly(lactic-co-glycolic acid) Microparticles Mitigate Staph |
| 34960611 | 10.1136/sti.75.5.352 | 10.3390/v13122341 | Presence and Persistence of Putative Lytic and Temperate Bacteriophages in Vagin |
| 34960616 | 10.1016/j.chembiol.2015.07.011 | 10.3390/v13122343 | Targeting Human Osteoarthritic Chondrocytes with Ligand Directed Bacteriophage-B |
| 34960634 | 10.1016/j.humimm.2021.07.009 | 10.3390/v13122365 | Composition of Eukaryotic Viruses and Bacteriophages in Individuals with Acute G |
| 34960683 | 10.3389/fmed.2021.550853 | 10.3390/v13122414 | Past and Future of Phage Therapy and Phage-Derived Proteins in Patients with Bon |
| 34960737 | 10.3390/md12074260 | 10.3390/v13122468 | Bacteriophage-Resistant Salmonella rissen: An In Vitro Mitigated Inflammatory Re |
| 34965410 | 10.1002/0471142727 | 10.1016/j.celrep.2021.110164 | Mobilization of vitamin B12 transporters alters competitive dynamics in a human  |
| 34970529 | 10.1128/AEM.00767-14 | 10.3389/fpubh.2021.783832 | Essential Oil Disinfectant Efficacy Against SARS-CoV-2 Microbial Surrogates. |
| 34981814 | 10.1080/19420862.2019.1703531 | 10.3892/ijo.2022.5302 | Retrospective analysis of the preparation and application of immunotherapy in ca |
| 34985567 | 10.1128/MRA.01035-18 | 10.1007/s00253-021-11752-7 | Characterization of a novel broad-spectrum endolysin PlyD4 encoded by a highly c |
| 34986742 | 10.1093/jn/136.6.1706s | 10.1080/21655979.2021.2014387 | DNA methylation across the tree of life, from micro to macro-organism. |
| 34993937 | 10.18632/oncotarget.13712 | 10.1007/978-1-0716-2014-4_3 | Discovery of Targets for Cancer Immunoprevention. |
| 34996449 | 10.1016/j.stemcr.2019.12.004 | 10.1186/s12915-021-01214-x | CRISPR/Cas9-mediated gene knockout and interallelic gene conversion in human ind |
| 35007129 | 10.1111/1440-1681.12613 | 10.1128/AAC.01842-21 | A Phase 1 Study To Evaluate Safety and Pharmacokinetics following Administration |
| 35008761 | 10.1016/j.intimp.2014.06.015 | 10.3390/ijms23010334 | Single-Chain Fragment Variables Targeting Leukocidin ED Can Alleviate the Inflam |
| 35008840 | 10.1002/jgm.1617 | 10.3390/ijms23010402 | Bacteriophages as Solid Tumor Theragnostic Agents. |
| 35012330 | 10.1002/jcc.20084 | 10.1128/mbio.02697-21 | Elevated Levels of an Enzyme Involved in Coenzyme B12 Biosynthesis Kills Escheri |
| 35013136 | 10.1093/nar/gkz239 | 10.1038/s41467-021-26583-3 | Crystal structure and functional implication of bacterial STING. |
| 35020473 | 10.1038/s41598-020-58335-6 | 10.1128/JVI.01769-21 | Expression of a Phage-Encoded Gp21 Protein Protects Pseudomonas aeruginosa again |
| 35027600 | 10.1128/JVI.75.21.10118-10131.2001 | 10.1038/s41598-021-04434-x | Bivalent single domain antibody constructs for effective neutralization of Venez |
| 35030192 | 10.1136/bmj.l231 | 10.1371/journal.pone.0262108 | Viral dysbiosis in children with new-onset celiac disease. |
| 35031652 | 10.1038/s41467-018-02879-9 | 10.1038/s41598-021-04627-4 | Targeting of Pseudomonas aeruginosa cell surface via GP12, an Escherichia coli s |
| 35038901 | 10.1016/j.ab.2004.12.001 | 10.1128/mbio.03174-21 | Quorum Sensing Promotes Phage Infection in Pseudomonas aeruginosa PAO1. |
| 35038902 | 10.1038/srep26717 | 10.1128/mbio.02441-21 | A Filamentous Bacteriophage Protein Inhibits Type IV Pili To Prevent Superinfect |
| 35040700 | 10.1093/nar/gky1080 | 10.1128/msystems.01083-21 | Species-Scale Genomic Analysis of Staphylococcus aureus Genes Influencing Phage  |
| 35041503 | 10.1371/journal.pone.0118557 | 10.1128/AAC.01923-21 | Development of an Anti-Acinetobacter baumannii Biofilm Phage Cocktail: Genomic A |
| 35041506 | 10.1093/cid/ciy947 | 10.1128/AAC.02071-21 | Considerations for the Use of Phage Therapy in Clinical Practice. |
| 35042848 | 10.1038/s41586-021-03819-2 | 10.1038/s41467-021-27656-z | Combination of pre-adapted bacteriophage therapy and antibiotics for treatment o |
| 35044719 | 10.1038/s41467-018-05928-5 | 10.15252/msb.202110584 | Proteome-scale mapping of binding sites in the unstructured regions of the human |
| 35045655 | 10.1016/j.bbrc.2017.05.031 | 10.3760/cma.j.issn.0253-2727.2021.11.008 | [Effects of L-asparaginase on proliferation, cell cycle and apoptosis of Burkitt |
| 35053205 | 10.1016/j.semcancer.2021.05.008 | 10.3390/biom12010056 | Understanding the Role of the Gut Microbiome and Microbial Metabolites in Non-Al |
| 35054861 | 10.1002/pro.3731 | 10.3390/ijms23020676 | Self-Assembling Lectin Nano-Block Oligomers Enhance Binding Avidity to Glycans. |
| 35059329 | 10.3389/fmicb.2020.01472 | 10.3389/fcimb.2021.822562 | Phages in the Gut Ecosystem. |
| 35061133 | 10.1016/S0966-842X(00)01705-4 | 10.1007/s10123-022-00237-w | Phage therapy for urinary tract infections: does it really work? |
| 35062209 | 10.1038/s41396-021-01096-5 | 10.3390/v14010006 | Phenotypic and Genomic Comparison of Klebsiella pneumoniae Lytic Phages: vB_KpnM |
| 35062236 | 10.1038/s41598-017-08336-9 | 10.3390/v14010033 | Preclinical Assessment of Bacteriophage Therapy against Experimental Acinetobact |
| 35062325 | 10.1128/AEM.02794-09 | 10.3390/v14010121 | Outer Membrane Vesicles (OMVs) of Pseudomonas aeruginosa Provide Passive Resista |
| 35062329 | 10.3389/fmicb.2021.667084 | 10.3390/v14010125 | Novel Neutralizing Epitope of PEDV S1 Protein Identified by IgM Monoclonal Antib |
| 35063014 | 10.1016/j.neurobiolaging.2018.11.026 | 10.1186/s13195-022-00959-z | A novel D-amino acid peptide with therapeutic potential (ISAD1) inhibits aggrega |
| 35064802 | 10.1007/s00253-020-10359-8 | 10.1007/s00294-022-01229-z | Prophage-encoded gene VpaChn25_0734 amplifies ecological persistence of Vibrio p |
| 35067170 | 10.1186/s40168-017-0283-5 | 10.1080/19490976.2021.2021790 | Hybrid, ultra-deep metagenomic sequencing enables genomic and functional charact |
| 35072628 | 10.1016/j.cell.2021.02.026 | 10.7554/eLife.73490 | Comprehensive characterization of the antibody responses to SARS-CoV-2 Spike pro |
| 35075126 | 10.1021/bi00367a013 | 10.1038/s41467-021-27799-z | A pandemic-enabled comparison of discovery platforms demonstrates a naïve antibo |
| 35075514 | 10.1016/j.tim.2018.09.006 | 10.1007/s00705-021-05345-y | Characterization and genome analysis of two new Aeromonas hydrophila phages, PZL |
| 35076284 | 10.1126/science.2466332 | 10.1089/crispr.2021.0065 | Bacterial Retrons Enable Precise Gene Editing in Human Cells. |
| 35077138 | 10.1098/rsif.2014.0950 | 10.1021/acssynbio.1c00576 | Combating Infectious Diseases with Synthetic Biology. |
| 35082445 | 10.1038/s41586-018-0043-0 | 10.1038/s41586-021-04332-2 | Petabase-scale sequence alignment catalyses viral discovery. |
| 35084299 | 10.1186/1471-2105-4-41 | 10.1099/mgen.0.000749 | Genome diversity of domesticated Acinetobacter baumannii ATCC 19606T strains. |
| 35089052 | 10.1128/AEM.67.2.608-616.2001 | 10.1128/mbio.03334-21 | Needle in a Whey-Stack: PhRACS as a Discovery Tool for Unknown Phage-Host Combin |
| 35092364 | 10.1016/j.celrep.2021.109930 | 10.1002/btpr.3241 | Proceedings from the 3rd International Conference on Microbiome Engineering. |
| 35094358 | 10.3109/09553002.2014.892229 | 10.1007/978-1-0716-1811-0_41 | Selection of Cancer Stem Cell-Targeting Agents Using Bacteriophage Display. |
| 35095778 | 10.3389/fmicb.2020.01056 | 10.3389/fmicb.2021.707815 | Optimized Method for Pseudomonas aeruginosa Integrative Filamentous Bacteriophag |
| 35104206 | 10.1093/bioinformatics/btr039 | 10.1099/mgen.0.000752 | Diversity of carbapenem-resistant Acinetobacter baumannii and bacteriophage-medi |
| 35107319 | 10.1128/AEM.02525-09 | 10.1128/spectrum.02295-21 | A Novel Bacteriophage with Broad Host Range against Clostridioides difficile Rib |
| 35107633 | 10.13005/bpj/1414 | 10.1007/s00253-022-11794-5 | Site-specific integration as an efficient method for production of recombinant h |
| 35107752 | 10.1093/protein/gzu032 | 10.1007/s12033-021-00442-4 | A Simple Whole-Plasmid PCR Method to Construct High-Diversity Synthetic Phage Di |
| 35128603 | 10.1093/nar/gkr485 | 10.1007/s11274-022-03239-y | Engineering laboratory/factory-specific phage-resistant strains of Escherichia c |
| 35143386 | 10.1128/AAC.04669-14 | 10.1099/mgen.0.000786 | Genomic analysis reveals high intra-species diversity of Shewanella algae. |
| 35149955 | 10.1111/joim.12233 | 10.1007/s12223-022-00954-9 | The crafty opponent: the defense systems of Staphylococcus aureus and response m |
| 35150435 | 10.1038/srep26717 | 10.1007/s40121-022-00591-2 | Therapeutic Strategies for Emerging Multidrug-Resistant Pseudomonas aeruginosa. |
| 35151823 | 10.1016/j.chom.2021.05.010 | 10.1016/j.micpath.2022.105442 | Clinical and experimental bacteriophage studies: Recommendations for possible ap |
| 35156836 | 10.1016/j.gpb.2021.04.001 | 10.1128/jb.00593-21 | Genetic Signatures from Adaptation of Bacteria to Lytic Phage Identify Potential |
| 35157271 | 10.1074/jbc.RA118.001752 | 10.1007/978-1-0716-2075-5_6 | A Transgenic Heavy Chain IgG Mouse Platform as a Source of High Affinity Fully H |
| 35163794 | 10.3390/v11121089 | 10.3390/ijms23031873 | The Antibacterial Effect of PEGylated Carbosilane Dendrimers on P. aeruginosa Al |
| 35164562 | 10.1128/JB.00747-15 | 10.1128/mbio.03088-21 | Evolutionary Sweeps of Subviral Parasites and Their Phage Host Bring Unique Para |
| 35165329 | 10.3390/jpm11070664 | 10.1038/s41598-022-06433-y | Detecting disease associated biomarkers by luminescence modulating phages. |
| 35165352 | 10.1093/bioinformatics/btab070 | 10.1038/s41598-022-06422-1 | Systematic analysis of putative phage-phage interactions on minimum-sized phage  |
| 35166238 | 10.1073/pnas.1920561117 | 10.1172/JCI154604 | Targeting a proteolytic neoepitope on CUB domain containing protein 1 (CDCP1) fo |
| 35166655 | 10.5740/jaoacint.18-0014 | 10.1099/mgen.0.000742 | Identification of novel, cryptic Clostridioides species isolates from environmen |
| 35167974 | 10.1101/2021.04.12.439201 | 10.1016/j.ymthe.2022.02.013 | Human inhalable antibody fragments neutralizing SARS-CoV-2 variants for COVID-19 |
| 35171008 | 10.1038/s41598-020-65619-4 | 10.1128/spectrum.01393-21 | A Multiwell-Plate Caenorhabditis elegans Assay for Assessing the Therapeutic Pot |
| 35171030 | 10.1016/0022-1759(90)90018-q | 10.1128/spectrum.01678-21 | Isolation and Characterization of Novel Lytic Phages Infecting Multidrug-Resista |
| 35175568 | 10.1016/S1473-3099(04)00976-4 | 10.1007/s40268-022-00383-6 | Exebacase: A Novel Approach to the Treatment of Staphylococcal Infections. |
| 35188102 | 10.3389/fmed.2017.00094 | 10.7554/eLife.73679 | Parallel evolution of Pseudomonas aeruginosa phage resistance and virulence loss |
| 35188577 | 10.1101/2021.08.21.457204 | 10.1093/nar/gkac099 | Discovery of potent and versatile CRISPR-Cas9 inhibitors engineered for chemical |
| 35190846 | 10.1016/j.joen.2015.04.008 | 10.1007/s00253-022-11810-8 | Phage therapy for refractory periapical periodontitis caused by Enterococcus fae |
| 35195442 | 10.1126/science.172.3990.1303 | 10.1128/jcm.02291-21 | Reoccurring Bovine Anthrax in Germany on the Same Pasture after 12 Years. |
| 35196122 | 10.1186/1471-2105-9-386 | 10.1128/msphere.01015-21 | Diversity of Pseudomonas aeruginosa Temperate Phages. |
| 35196336 | 10.1039/c2an15780b | 10.1371/journal.pone.0263887 | Decay and damage of therapeutic phage OMKO1 by environmental stressors. |
| 35196798 | 10.1038/s41598-019-52982-0 | 10.1128/spectrum.01466-21 | Targeted Antimicrobial Photodynamic Therapy of Biofilm-Embedded and Intracellula |
| 35197516 | 10.3390/toxins10060236 | 10.1038/s41598-022-06921-1 | Enhancing neutralization of Plasmodium falciparum using a novel monoclonal antib |
| 35199035 | 10.1038/nmeth.2019 | 10.1016/j.xpro.2022.101170 | Protocol for the isolation, sequencing, and analysis of the gut phageome from hu |
| 35203767 | 10.1093/nar/29.9.e45 | 10.3390/antibiotics11020164 | Phage-Host Interaction Analysis by Flow Cytometry Allows for Rapid and Efficient |
| 35204656 | 10.1007/s13311-013-0184-7 | 10.3390/biom12020157 | Inhibition of Polyglutamine Misfolding with D-Enantiomeric Peptides Identified b |
| 35208664 | 10.1038/nrmicro.2017.120 | 10.3390/microorganisms10020210 | Novel Bacteriophages Show Activity against Selected Australian Clinical Strains  |
| 35215782 | 10.3389/fmicb.2019.01984 | 10.3390/v14020190 | A Bacteriophage Cocktail Significantly Reduces Listeria monocytogenes without De |
| 35215788 | 10.3390/v10070351 | 10.3390/v14020194 | Isolation and Characterization of a Novel Autographiviridae Phage and Its Combin |
| 35215934 | 10.1038/s41586-021-03819-2 | 10.3390/v14020342 | PhageLeads: Rapid Assessment of Phage Therapeutic Suitability Using an Ensemble  |
| 35215976 | 10.1158/1078-0432.CCR-14-3212 | 10.3390/v14020384 | Phage-Displayed Mimotopes of SARS-CoV-2 Spike Protein Targeted to Authentic and  |
| 35216013 | 10.1126/science.aad3312 | 10.3390/v14020420 | A Conserved Receptor-Binding Domain in the VP1u of Primate Erythroparvoviruses D |
| 35216023 | 10.1155/S1064744997000094 | 10.3390/v14020430 | Transkingdom Analysis of the Female Reproductive Tract Reveals Bacteriophages fo |
| 35220702 | 10.1016/j.clinthera.2020.07.014 | 10.3760/cma.j.cn501120-20211130-00400 | [Analysis of genomic information and biological characteristics of a bacteriopha |
| 35237274 | 10.3390/microorganisms9040762 | 10.3389/fimmu.2022.835417 | Fighting MDR-Klebsiella pneumoniae Infections by a Combined Host- and Pathogen-D |
| 35238483 | 10.1128/AEM.00091-16 | 10.1111/tbed.14500 | Survey of Staphylococcus aureus carriage by free-living red deer (Cervus elaphus |
| 35239330 | 10.3109/10520293309116112 | 10.1021/acsnano.2c00048 | Treatment of Wound Infections in a Mouse Model Using Zn2+-Releasing Phage Bound  |
| 35239730 | 10.1016/j.yexcr.2021.112567 | 10.1371/journal.pone.0264822 | Selection of human single domain antibodies (sdAb) against thymidine kinase 1 an |
| 35258339 | 10.3389/fmicb.2021.748718 | 10.1128/mra.00092-22 | Complete Genome Sequence of Pseudomonas aeruginosa Bacteriophage PASA16, Used in |
| 35259067 | 10.21203/rs.3.rs-850585/v1 | 10.1080/22221751.2022.2051752 | Effective phage cocktail to combat the rising incidence of extensively drug-resi |
| 35265532 | 10.1128/AAC.43.11.2813 | 10.3389/fcimb.2022.817841 | Comparative Genomic Reveals Clonal Heterogeneity in Persistent Staphylococcus au |
| 35272105 | 10.1038/s41586-020-2012-7 | 10.1016/j.molimm.2022.03.006 | Functional reconstitution of the MERS CoV receptor binding motif. |
| 35277541 | 10.1134/S0026365619060089 | 10.1038/s41598-022-07763-7 | Genetic analysis of the cold-sensitive growth phenotype of Burkholderia pseudoma |
| 35277777 | 10.3390/v13060959 | 10.1007/s00705-022-05391-0 | Nettle manure: an unsuspected source of bacteriophages active against various ph |
| 35285676 | 10.1007/BF00328721 | 10.1128/aac.01957-21 | Monoclonal Antibodies Targeting Surface-Exposed Epitopes of Candida albicans Cel |
| 35285710 | 10.1128/AEM.00233-18 | 10.1128/aem.02552-21 | Factors Impacting Persistence of Phi6 Bacteriophage, an Enveloped Virus Surrogat |
| 35298559 | 10.1038/leu.2016.373 | 10.1371/journal.pone.0265534 | A TCR mimic monoclonal antibody for the HPV-16 E7-epitope p11-19/HLA-A*02:01 com |
| 35298699 | 10.4161/mabs.25234 | 10.1007/s00280-022-04415-5 | Discovery and pharmacological characterization of cetrelimab (JNJ-63723283), an  |
| 35301980 | 10.1038/s41541-020-00249-5 | 10.2807/1560-7917.ES.2022.27.11.2100119 | Large-scale decontamination of disposable FFP2 and FFP3 respirators by hydrogen  |
| 35306645 | 10.1016/j.ajic.2016.03.018 | 10.1007/s12560-022-09519-y | Use of a Hydrogen Peroxide Nebulizer for Viral Disinfection of Emergency Ambulan |
| 35311639 | 10.1128/mBio.02481-18 | 10.1099/mgen.0.000800 | Kaptive 2.0: updated capsule and lipopolysaccharide locus typing for the Klebsie |
| 35313913 | 10.3390/pharmaceutics12040308 | 10.1186/s12987-022-00321-3 | Exploring ITM2A as a new potential target for brain delivery. |
| 35315699 | 10.1186/1471-2164-12-402 | 10.1128/spectrum.00391-22 | Genomic Characteristics of Recently Recognized Vibrio cholerae El Tor Lineages A |
| 35316421 | 10.1086/315239 | 10.1007/s11538-022-01006-6 | Phage-Antibiotic Synergy Inhibited by Temperate and Chronic Virus Competition. |
| 35320047 | 10.17504/protocols.io.gwebxbe | 10.1073/pnas.2114619119 | The virota and its transkingdom interactions in the healthy infant gut. |
| 35320327 | 10.1128/JCM.00197-18 | 10.1371/journal.pone.0265884 | Whole genome sequencing of Klebsiella pneumoniae clinical isolates sequence type |
| 35323045 | 10.1109/MCSE.2007.55 | 10.1128/msystems.00084-22 | Deciphering Active Prophages from Metagenomes. |
| 35328933 | 10.1086/661222 | 10.3390/ijerph19063246 | UV-C Light-Based Surface Disinfection: Analysis of Its Virucidal Efficacy Using  |
| 35333580 | 10.1101/2021.04.11.439360v1 | 10.1126/sciadv.abm0220 | Multivariate mining of an alpaca immune repertoire identifies potent cross-neutr |
| 35335222 | 10.3389/fmicb.2016.01515 | 10.3390/molecules27061857 | Limitations of Phage Therapy and Corresponding Optimization Strategies: A Review |
| 35336974 | 10.1128/JB.01804-08 | 10.3390/v14030567 | Global Transcriptomic Response of Staphylococcus aureus to Virulent Bacteriophag |
| 35337023 | 10.1089/jam.2007.0610 | 10.3390/v14030616 | Environmental Effects on Viable Virus Transport and Resuspension in Ventilation  |
| 35337027 | 10.1161/ATVBAHA.110.213850 | 10.3390/v14030620 | Efficacy Assessment of Phage Therapy in Treating Staphylococcus aureus-Induced M |
| 35337034 | 10.1186/s13059-014-0550-8 | 10.3390/v14030626 | Insights into Gene Transcriptional Regulation of Kayvirus Bacteriophages Obtaine |
| 35338087 | 10.1038/ncomms8458 | 10.1136/jitc-2021-004035 | Development of a TCR-like antibody and chimeric antigen receptor against NY-ESO- |
| 35343798 | 10.1093/bioinformatics/btu033 | 10.1128/msystems.00064-22 | Cervicovaginal DNA Virome Alterations Are Associated with Genital Inflammation a |
| 35344565 | 10.1093/bioinformatics/btr509 | 10.1371/journal.ppat.1010420 | Engineering selectivity of Cutibacterium acnes phages by epigenetic imprinting. |
| 35348270 | 10.5761/atcs.oa.20-00294 | 10.1111/cas.15350 | Novel cancer-specific epidermal growth factor receptor antibody obtained from th |
| 35348363 | 10.1093/molbev/msw054 | 10.1128/jvi.00197-22 | RetS Regulates Phage Infection in Pseudomonas aeruginosa via Modulating the GacS |
| 35348372 | 10.1186/1471-2105-9-386 | 10.1128/spectrum.00561-22 | Clarification of the Dynamic Autothermal Thermophilic Aerobic Digestion Process  |
| 35352244 | 10.1186/s12985-020-01485-w | 10.1007/s10517-022-05424-3 | Molecular Epidemiology of Hypervirulent K. pneumoniae and Problems of Health-Car |
| 35354477 | 10.1080/22221751.2020.1747950 | 10.1186/s12929-022-00806-1 | Bacteriophages and antibiotic interactions in clinical practice: what we have le |
| 35358257 | 10.1007/s00705-015-2625-6 | 10.1371/journal.pone.0266220 | Characterization of an intracellular humanized single-chain antibody to matrix p |
| 35360104 | 10.1073/pnas.1706359114 | 10.3389/fcimb.2022.836706 | Gut Virome: Role and Distribution in Health and Gastrointestinal Diseases. |
| 35360502 | 10.3934/microbiol.2020014 | 10.1016/j.sjbs.2022.03.019 | Isolation and characterization of lytic bacteriophages from sewage at an egyptia |
| 35368814 | 10.1056/NEJMoa2001017 | 10.34067/KID.0006102020 | SARS-CoV-2 in Spent Dialysate from Chronic Peritoneal Dialysis Patients with COV |
| 35369520 | 10.1093/infdis/jit842 | 10.3389/fmicb.2022.817228 | PaP1, a Broad-Spectrum Lysin-Derived Cationic Peptide to Treat Polymicrobial Ski |
| 35372200 | 10.1016/j.cmi.2018.08.022 | 10.3389/fpubh.2022.712657 | Phage Display-Derived Monoclonal Antibodies Against Internalins A and B Allow Sp |
| 35378038 | 10.1371/journal.ppat.1008232 | 10.1021/acschembio.2c00114 | Directed Evolution-Driven Increase of Structural Plasticity Is a Prerequisite fo |
| 35379961 | 10.1093/bib/bbx129 | 10.1038/s41587-022-01256-8 | CRISPR-free base editors with enhanced activity and expanded targeting scope in  |
| 35388062 | 10.1186/1471-2105-7-439 | 10.1038/s41598-022-09733-5 | Phenotypic characterization and genome analysis of a novel Salmonella Typhimuriu |
| 35388218 | 10.1111/1462-2920.15224 | 10.1038/s41586-022-04546-y | Two defence systems eliminate plasmids from seventh pandemic Vibrio cholerae. |
| 35389255 | 10.1073/pnas.1814023115 | 10.1128/jb.00557-21 | Phage Infection Restores PQS Signaling and Enhances Growth of a Pseudomonas aeru |
| 35392977 | 10.1038/nri.2017.49 | 10.1186/s13046-022-02307-3 | Adaptive antitumor immune response stimulated by bio-nanoparticle based vaccine  |
| 35394418 | 10.1111/zph.12467 | 10.1099/mgen.0.000796 | Pathogenomes and variations in Shiga toxin production among geographically disti |
| 35398093 | 10.3791/62395 | 10.1016/j.jbc.2022.101907 | Solution structure ensemble of human obesity-associated protein FTO reveals drug |
| 35404959 | 10.1093/bioinformatics/btp163 | 10.1371/journal.ppat.1010155 | Detailed analysis of antibody responses to SARS-CoV-2 vaccination and infection  |
| 35404965 | 10.1073/pnas.1806005115 | 10.1371/journal.pone.0261482 | Modelling of filamentous phage-induced antibiotic tolerance of P. aeruginosa. |
| 35415924 | 10.1007/bf00172827 | 10.1111/1462-2920.16010 | The power of unbiased phenotypic screens - cellulose as a first receptor for the |
| 35416546 | 10.1007/s12560-021-09460-6 | 10.1007/s00284-022-02834-4 | Characterization and Genomic Analysis of Bacteriophage vB_KpnM_IME346 Targeting  |
| 35416713 | 10.1016/j.clim.2020.108511 | 10.1128/aac.02273-21 | Linker-Improved Chimeric Endolysin Selectively Kills Staphylococcus aureus In Vi |
| 35417303 | 10.3390/ijms22041749 | 10.1080/21645515.2022.2055373 | Binding and neutralizing abilities of antibodies towards SARS-CoV-2 S2 domain. |
| 35418239 | 10.1089/crispr.2020.0059 | 10.1128/msystems.00083-22 | Prediction of Prophages and Their Host Ranges in Pathogenic and Commensal Neisse |
| 35423325 | 10.3389/fmicb.2015.01216 | 10.1039/d0ra10156g | Regenerating heavily biofouled dissolved oxygen sensors using bacterial viruses. |
| 35426058 | 10.3389/fpubh.2018.00235 | 10.1007/s10661-022-09918-5 | Evaluation of crAssphage as a human-specific microbial source-tracking marker in |
| 35434949 | 10.1038/s41578-021-00362-4 | 10.1002/advs.202105668 | Photocatalytic Quantum Dot-Armed Bacteriophage for Combating Drug-Resistant Bact |
| 35435739 | 10.1128/JB.185.11.3325-3332.2003 | 10.1128/spectrum.02777-21 | The Chronic Wound Phageome: Phage Diversity and Associations with Wounds and Hea |
| 35435752 | 10.1093/bioinformatics/btp101 | 10.1128/spectrum.00123-22 | Global Transcriptomic Analysis of Bacteriophage-Host Interactions between a Kayv |
| 35444660 | 10.1038/nbt1217-1115 | 10.3389/fimmu.2022.838966 | Discovery of Anti-PD-L1 Human Domain Antibodies for Cancer Immunotherapy. |
| 35457098 | 10.1038/mtm.2015.43 | 10.3390/ijms23084282 | Structural Requirements for the Binding of a Peptide to Prohibitins on the Cell  |
| 35458417 | 10.1128/AAC.04548-14 | 10.3390/v14040688 | Phage Therapy Potentiates Second-Line Antibiotic Treatment against Pneumonic Pla |
| 35464476 | 10.1016/j.compbiolchem.2020.107322 | 10.3389/fimmu.2022.869825 | Construction of a Large Size Human Immunoglobulin Heavy Chain Variable (VH) Doma |
| 35465015 | 10.1093/bioinformatics/9.3.355 | 10.1155/2022/9470683 | Phage_UniR_LGBM: Phage Virion Proteins Classification with UniRep Features and L |
| 35466441 | 10.1016/s0378-1119(03)00509-2 | 10.1002/ana.26380 | ZSCAN1 Autoantibodies Are Associated with Pediatric Paraneoplastic ROHHAD. |
| 35468972 | 10.1016/j.jim.2006.07.024 | 10.1038/s41598-022-10657-3 | Immunoreactivity of humanized single-chain variable fragment against its functio |
| 35469831 | 10.1074/mcp.M113.031591 | 10.1016/j.jmb.2022.167602 | Synthetic Antibodies Detect Distinct Cellular States of Chromosome Passenger Com |
| 35475638 | 10.1371/journal.pone.0070329 | 10.1128/spectrum.01503-21 | Involvement of a Phage-Encoded Wzy Protein in the Polymerization of K127 Units T |
| 35478284 | 10.1093/bioinformatics/btv383 | 10.1002/mbo3.1273 | Genetically distant bacteriophages select for unique genomic changes in Enteroco |
| 35481650 | 10.1016/j.jmb.2012.11.037 | 10.1002/pro.4296 | Synthetic antibodies block receptor binding and current-inhibiting effects of α- |
| 35491833 | 10.1038/s41586-021-03819-2 | 10.1128/mbio.00588-22 | Organizing the Global Diversity of Microviruses. |
| 35493489 | 10.3389/fimmu.2020.00610 | 10.3389/fimmu.2022.865232 | Restriction of the Global IgM Repertoire in Antiphospholipid Syndrome. |
| 35493727 | 10.3389/fmicb.2018.02247 | 10.3389/fcimb.2022.846063 | More Positive or More Negative? Metagenomic Analysis Reveals Roles of Virome in  |
| 35501488 | 10.1371/journal.pone.0033578 | 10.1007/s00253-022-11932-z | Phage nanoparticle as a carrier for controlling fungal infection. |
| 35504908 | 10.1146/annurev-med-080219-122208 | 10.1038/s41467-022-29689-4 | Bacteriophage treatment of disseminated cutaneous Mycobacterium chelonae infecti |
| 35534543 | 10.21769/BioProtoc.2124 | 10.1038/s41598-022-11774-9 | Determination of a distinguished interferon gamma epitope recognized by monoclon |
| 35535021 | 10.1017/ice.2021.284 | 10.1093/infdis/jiac195 | Fit-Tested N95 Masks Combined With Portable High-Efficiency Particulate Air Filt |
| 35537278 | 10.1128/mBio.01652-19 | 10.1016/j.ebiom.2022.104045 | Phage-antibiotic combination is a superior treatment against Acinetobacter bauma |
| 35547216 | 10.3389/fmed.2020.00342 | 10.3389/fmed.2022.851310 | Use of Phage Cocktail BFC 1.10 in Combination With Ceftazidime-Avibactam in the  |
| 35548089 | 10.1046/j.1365-2958.1996.6311351.x | 10.3389/fpubh.2022.869886 | Viral Metagenomics Reveals Widely Diverse Viral Community of Freshwater Amazonia |
| 35562968 | 10.1093/emph/eoy005 | 10.3390/ijms23094577 | Phage Therapy in the Era of Multidrug Resistance in Bacteria: A Systematic Revie |
| 35563247 | 10.1080/01919512.2020.1795614 | 10.3390/ijms23094856 | Inactivation of E. coli, S. aureus, and Bacteriophages in Biofilms by Humidified |
| 35572557 | 10.1136/annrheumdis-2011-200413 | 10.3389/fimmu.2022.851096 | Ferritin Light Chain: A Candidate Autoantigen in Immuno-Related Pancytopenia. |
| 35575497 | 10.1093/nar/gkw387 | 10.1128/spectrum.01182-22 | PrrT/A, a Pseudomonas aeruginosa Bacterial Encoded Toxin-Antitoxin System Involv |
| 35576225 | 10.1016/j.ttbdis.2016.09.017 | 10.1371/journal.ppat.1010540 | Targeted mutagenesis in Anaplasma marginale to define virulence and vaccine deve |
| 35579384 | 10.1371/journal.pcbi.1005752 | 10.1128/msystems.00129-22 | Gut Microbial Stability is Associated with Greater Endurance Performance in Athl |
| 35579468 | 10.1093/nar/gkn179 | 10.1128/spectrum.02158-21 | Co-Occurrence of Multidrug Resistant Klebsiella pneumoniae Pathogenic Clones of  |
| 35579473 | 10.1093/bioinformatics/btu153 | 10.1128/spectrum.00185-22 | Dissecting Listeria monocytogenes Persistent Contamination in a Retail Market Us |
| 35580120 | 10.1093/nar/gkw781 | 10.1371/journal.pone.0259480 | Apoptosis like symptoms associated with abortive infection of Mycobacterium smeg |
| 35580187 | 10.5061/dryad.4f4qrfjf6 | 10.1073/pnas.2121966119 | An aggregation inhibitor specific to oligomeric intermediates of Aβ42 derived fr |
| 35583733 | 10.1093/nar/16.13.6127 | 10.1007/978-1-0716-2233-9_6 | Plant Gene Modification by BAC Recombineering. |
| 35586934 | 10.2217/fmb.15.8 | 10.4014/jmb.2205.05009 | Bactericidal Effect of Cecropin A Fused Endolysin on Drug-Resistant Gram-Negativ |
| 35589780 | 10.1021/acs.jctc.0c01132 | 10.1038/s41598-022-12242-0 | Structure-guided affinity maturation of a novel human antibody targeting the SAR |
| 35596819 | 10.1021/acschemneuro.0c00518 | 10.1007/s10571-022-01230-7 | Tau Aggregation Inhibiting Peptides as Potential Therapeutics for Alzheimer Dise |
| 35599623 | 10.1101/2020.05.19.20107144 | 10.1080/21655979.2022.2076390 | Healthy humans can be a source of antibodies countering COVID-19. |
| 35604129 | 10.1093/gbe/evaa023 | 10.1128/spectrum.02654-21 | The Neisseria gonorrhoeae Accessory Genome and Its Association with the Core Gen |
| 35612629 | 10.1186/s12967-014-0352-5 | 10.1007/s00253-022-11981-4 | HRP-conjugated-nanobody-based cELISA for rapid and sensitive clinical detection  |
| 35613073 | 10.1016/j.cub.2022.01.052 | 10.1371/journal.pbio.3001644 | Perplexing dynamics of Wolbachia proteins for cytoplasmic incompatibility. |
| 35614180 | 10.1038/s41598-016-0001-8 | 10.1038/s41598-022-12818-w | Longer amplicons provide better sensitivity for electrochemical sensing of viral |
| 35617160 | 10.1038/s41467-020-19096-y | 10.1371/journal.pone.0266136 | Cross-reactive antibodies targeting surface-exposed non-structural protein 1 (NS |
| 35617195 | 10.1146/annurev-virology-031413-085500 | 10.1371/journal.pone.0268596 | Unconstrained coevolution of bacterial size and the latent period of plastic pha |
| 35620101 | 10.3390/md17040211 | 10.3389/fmicb.2022.892021 | Antitoxin CrlA of CrlTA Toxin-Antitoxin System in a Clinical Isolate Pseudomonas |
| 35620437 | 10.1016/j.freeradbiomed.2014.08.011 | 10.1016/j.isci.2022.104372 | Genomic characterization of lytic bacteriophages targeting genetically diverse P |
| 35625199 | 10.2807/1560-7917.ES.2018.23.46.1800516 | 10.3390/antibiotics11050555 | Bacteriophage Tail Proteins as a Tool for Bacterial Pathogen Recognition-A Liter |
| 35628148 | 10.1371/journal.pone.0212332 | 10.3390/ijms23105335 | Antiviral Characterization of Advanced Materials: Use of Bacteriophage Phi 6 as  |
| 35628365 | 10.3390/diagnostics11020288 | 10.3390/ijms23105556 | A Novel Human Neutralizing mAb Recognizes Delta, Gamma and Omicron Variants of S |
| 35632644 | 10.1007/s00216-017-0808-6 | 10.3390/v14050902 | Targeting of Silver Cations, Silver-Cystine Complexes, Ag Nanoclusters, and Nano |
| 35632706 | 10.1016/j.ijpharm.2021.120850 | 10.3390/v14050964 | Antibiofilm Efficacy of the Pseudomonas aeruginosa Pbunavirus vB_PaeM-SMS29 Load |
| 35632757 | 10.1371/journal.pone.0142504 | 10.3390/v14051016 | Characterization of Three Novel Virulent Aeromonas Phages Provides Insights into |
| 35632803 | 10.3389/fmicb.2018.00127 | 10.3390/v14051061 | Understanding the Mechanisms That Drive Phage Resistance in Staphylococci to Pre |
| 35632820 | 10.1016/j.mimet.2010.09.004 | 10.3390/v14051079 | In Vitro and In Vivo Assessments of Two Newly Isolated Bacteriophages against an |
| 35637399 | 10.1186/s13756-019-0590-7 | 10.1007/s00203-022-02962-2 | Metagenomic analysis of wastewater phageome from a University Hospital in Turkey |
| 35638779 | 10.1093/nar/gkn879 | 10.1128/spectrum.01135-22 | Bacteriophage-Mediated Perturbation of Defined Bacterial Communities in an In Vi |
| 35638845 | 10.1128/AEM.01369-08 | 10.1128/aem.00039-22 | The c-di-GMP Phosphodiesterase PipA (PA0285) Regulates Autoaggregation and Pf4 B |
| 35638894 | 10.1016/j.virol.2010.06.011 | 10.1128/mra.00239-22 | Complete Genome Sequence of the N4-like Pseudomonas aeruginosa Bacteriophage vB_ |
| 35649416 | 10.1126/science.aaa0698 | 10.1016/j.immuni.2022.05.002 | Phage display of environmental protein toxins and virulence factors reveals the  |
| 35650235 | 10.3390/polym13091367 | 10.1038/s41598-022-13316-9 | Novel sustainable filter for virus filtration and inactivation. |
| 35654045 | 10.1136/gutjnl-2017-313952 | 10.1016/j.chom.2022.05.005 | Gut bacterial isoamylamine promotes age-related cognitive dysfunction by promoti |
| 35658414 | 10.1073/pnas.1703255114 | 10.1021/acsinfecdis.2c00201 | Chimeric Ligands of Pili and Lectin A Inhibit Tolerance, Persistence, and Virule |
| 35663462 | 10.1186/s12916-018-1215-3 | 10.3389/fcimb.2022.871293 | The Microbiome in Pancreatic Cancer-Implications for Diagnosis and Precision Bac |
| 35668859 | 10.1128/AEM.00980-21 | 10.2147/IDR.S367460 | Assessment of Phage-Mediated Inhibition and Removal of Multidrug-Resistant Pseud |
| 35669812 | 10.1590/0104-1169.0266.2611 | 10.1007/s40201-021-00770-2 | Potential of lytic bacteriophages as disinfectant to control of Pseudomonas aeru |
| 35670674 | 10.1101/600890 | 10.1093/nar/gkac462 | CRISPR-Cas12a targeting of ssDNA plays no detectable role in immunity. |
| 35672689 | 10.1089/bsp.2009.0057 | 10.1186/s12879-022-07493-1 | Evaluation of a direct phage DNA detection-based Taqman qPCR methodology for qua |
| 35682794 | 10.3389/fmicb.2021.627897 | 10.3390/ijms23116116 | APTC-C-SA01: A Novel Bacteriophage Cocktail Targeting Staphylococcus aureus and  |
| 35689701 | 10.1016/j.chom.2019.01.008 | 10.1007/s00535-022-01882-8 | Features of the gut prokaryotic virome of Japanese patients with Crohn's disease |
| 35694384 | 10.1186/s12864-020-6527-y | 10.7717/peerj.13479 | Genomic insights into Lactobacillus gasseri and Lactobacillus paragasseri. |
| 35696017 | 10.1038/s41586-020-2548-6 | 10.1007/s11427-021-2095-0 | Structural and functional analysis of a potent human neutralizing antibody again |
| 35696196 | 10.1001/jamaneurol.2020.2231 | 10.1001/jamaneurol.2022.1357 | Identification of Caveolae-Associated Protein 4 Autoantibodies as a Biomarker of |
| 35699339 | 10.1128/IAI.00939-15 | 10.1128/msystems.00092-22 | Nutrient Availability and Phage Exposure Alter the Quorum-Sensing and CRISPR-Cas |
| 35699567 | 10.1038/nn.2908 | 10.1080/19420862.2022.2085536 | In vitro discovery of a human monoclonal antibody that neutralizes lethality of  |
| 35700129 | 10.3389/fphys.2016.00156 | 10.1093/femsre/fuac027 | The role of virome in the gastrointestinal tract and beyond. |
| 35701436 | 10.1080/01621459.1977.10479905 | 10.1038/s41598-022-13269-z | The human "contaminome": bacterial, viral, and computational contamination in wh |
| 35705576 | 10.1186/s12864-019-5647-8 | 10.1038/s41598-022-13584-5 | TSP, a virulent Podovirus, can control the growth of Staphylococcus aureus for 1 |
| 35708333 | 10.1371/journal.pone.0077122 | 10.1128/aac.02247-21 | Antibiotic Exposure Leads to Reduced Phage Susceptibility in Vancomycin Intermed |
| 35710371 | 10.1093/nar/gkaa913 | 10.1186/s12915-022-01347-7 | To kill or to be killed: pangenome analysis of Escherichia coli strains reveals  |
| 35713790 | 10.1371/journal.pbio.0040003 | 10.1007/s12560-022-09525-0 | Infectious Pepper Mild Mottle Virus and Human Adenoviruses as Viral Indices in S |
| 35716268 | 10.1371/journal.pone.0192507 | 10.1007/s00705-022-05472-0 | Characterization and genome analysis of Pseudomonas aeruginosa phage vB_PaeP_Lx1 |
| 35717537 | 10.1093/nar/gkh340 | 10.1038/s41598-022-14025-z | Characterization of Stenotrophomonas maltophilia phage AXL1 as a member of the g |
| 35726228 | 10.1093/abt/tbaa022 | 10.1155/2022/2929605 | Development and Characterization of a Nanobody against Human T-Cell Immunoglobul |
| 35727730 | 10.17226/24622 | 10.1093/g3journal/jkac141 | Publishing student-led discoveries in genetics. |
| 35731716 | 10.1016/j.ijbiomac.2018.05.007 | 10.1021/acs.biochem.2c00010 | Phage-Related Ribosomal Protease (Prp) of Staphylococcus aureus: In Vitro Michae |
| 35732145 | 10.1007/978-1-61779-207-6_2 | 10.1016/j.xcrm.2022.100656 | Filamentous bacteriophage delays healing of Pseudomonas-infected wounds. |
| 35739117 | 10.1038/nmeth.3176 | 10.1038/s41467-022-31390-5 | Gut virome profiling identifies a widespread bacteriophage family associated wit |
| 35743031 | 10.1016/j.bbrc.2021.12.079 | 10.3390/ijms23126587 | Human Superantibodies to 3CLpro Inhibit Replication of SARS-CoV-2 across Variant |
| 35746642 | 10.1038/d41586-022-00228-x | 10.3390/v14061170 | A Thorough Synthesis of Phage Therapy Unit Activity in Poland-Its History, Miles |
| 35746731 | 10.1016/S0022-2836(02)01246-9 | 10.3390/v14061261 | Filamentous Pseudomonas Phage Pf4 in the Context of Therapy-Inducibility, Infect |
| 35746779 | 10.1016/j.meegid.2021.104881 | 10.3390/v14061309 | Isolation and Characterization of Lytic Proteus Virus 309. |
| 35746797 | 10.1021/acs.analchem.0c03173 | 10.3390/v14061326 | ORFeome Phage Display Reveals a Major Immunogenic Epitope on the S2 Subdomain of |
| 35746811 | 10.7150/ijbs.60551 | 10.3390/v14061340 | Novel Bacteriophage Specific against Staphylococcus epidermidis and with Antibio |
| 35752612 | 10.1111/2049-632X.12074 | 10.1038/s41392-022-01056-1 | Pseudomonas aeruginosa: pathogenesis, virulence factors, antibiotic resistance,  |
| 35753005 | 10.1016/j.virusres.2020.198274 | 10.1007/s00203-022-03055-w | Gene sequencing analysis of tailed phages identified diverse (Kayfunavirus and B |
| 35753153 | 10.1146/annurev-micro-090817-062535 | 10.1016/j.ebiom.2022.104113 | The gut virome: A new microbiome component in health and disease. |
| 35759354 | 10.1021/acsnano.6b07071 | 10.1021/acs.bioconjchem.2c00166 | Design and Functional Analysis of Heterobifunctional Multivalent Phage Capsid In |
| 35762793 | 10.1128/mBio.00277-20 | 10.1128/msystems.00019-22 | Phage Cocktails Constrain the Growth of Enterococcus. |
| 35771408 | 10.1007/s11427-020-1740-8 | 10.1007/s10529-022-03263-w | Selection and identification of a specific peptide binding to ovarian cancer cel |
| 35773283 | 10.1093/nar/gkw387 | 10.1038/s41467-022-31455-5 | Comparative genomics of Acinetobacter baumannii and therapeutic bacteriophages f |
| 35773472 | 10.3390/v13030455 | 10.1038/s41579-022-00755-4 | Mutualistic interplay between bacteriophages and bacteria in the human gut. |
| 35778844 | 10.1038/nsmb.1727 | 10.1016/j.bpj.2022.06.028 | Labeling of a mutant estrogen receptor with an Affimer in a breast cancer cell l |
| 35782108 | 10.1038/nrcardio.2014.40 | 10.3389/fcimb.2022.890817 | Abnormal Blood Bacteriome, Gut Dysbiosis, and Progression to Severe Dengue Disea |
| 35782128 | 10.1038/s41598-022-07995-7 | 10.3389/fcimb.2022.918010 | Metagenomic Analyses of Multiple Gut Datasets Revealed the Association of Phage  |
| 35796308 | 10.1038/s41598-020-76603-3 | 10.1021/acschembio.2c00256 | A Designer Nanoparticle Platform for Controlled Intracellular Delivery of Bioact |
| 35797343 | 10.3390/microorganisms9122414 | 10.1371/journal.ppat.1010602 | Mycobacteriophages: From Petri dish to patient. |
| 35805896 | 10.1038/onc.2013.156 | 10.3390/ijms23136895 | A Fully-Human Antibody Specifically Targeting a Membrane-Bound Fragment of CADM1 |
| 35806089 | 10.1128/jb.157.2.649-654.1984 | 10.3390/ijms23137084 | Flagellotropic Bacteriophages: Opportunities and Challenges for Antimicrobial Ap |
| 35806205 | 10.1093/neuonc/nov170 | 10.3390/ijms23137200 | Glioblastoma Extracellular Vesicle-Specific Peptides Inhibit EV-Induced Neuronal |
| 35806393 | 10.3390/ijms20102383 | 10.3390/ijms23137388 | Multipotential Role of Growth Factor Mimetic Peptides for Osteochondral Tissue E |
| 35817890 | 10.1093/bioinformatics/btz795 | 10.1038/s41564-022-01162-4 | Phage defence by deaminase-mediated depletion of deoxynucleotides in bacteria. |
| 35817891 | 10.1093/nar/gkz239 | 10.1038/s41564-022-01158-0 | Bacteria deplete deoxynucleotides to defend against bacteriophage infection. |
| 35831579 | 10.1038/nm.3950 | 10.1002/jmv.27998 | Dynamics of nasopharyngeal tract phageome and association with disease severity  |
| 35833243 | 10.1128/mr.56.3.430-481.1992 | 10.1111/omi.12378 | Increased sensitivity of Aggregatibacter actinomycetemcomitans to human serum is |
| 35837391 | 10.1038/srep19211 | 10.3389/fimmu.2022.885424 | Development of a Humanized VHH Based Recombinant Antibody Targeting Claudin 18.2 |
| 35842473 | 10.1093/bioinformatics/btu170 | 10.1038/s41598-022-16453-3 | Development and characterization of a camelid derived antibody targeting a linea |
| 35847060 | 10.1128/jb.176.17.5262-5269.1994 | 10.3389/fmicb.2022.907958 | Characterization of Pseudomonas aeruginosa Bacteriophage L5 Which Requires Type  |
| 35851408 | 10.1006/jmbi.1996.0628 | 10.1038/s41598-022-16293-1 | Eosinophilic esophagitis auxiliary diagnosis based on a peptide ligand to eosino |
| 35851946 | 10.1007/s11356-022-18514-6 | 10.1007/s12560-022-09526-z | Assessment of Surface Disinfection Effectiveness of Decontamination System COUNT |
| 35857150 | 10.1093/bioinformatics/btr039 | 10.1007/s00705-022-05542-3 | Genome sequence of the novel freshwater Microcystis cyanophage Mwe-Yong1112-1. |
| 35859168 | 10.1093/nar/gku486 | 10.1038/s41586-022-04999-1 | Cryo-EM structure of an active bacterial TIR-STING filament complex. |
| 35862704 | 10.1080/15366367.2019.1565254 | 10.1128/iai.00161-22 | Development of a Monoclonal Antibody to a Vibriophage as a Proxy for Vibrio chol |
| 35862755 | 10.1073/pnas.1311066110 | 10.1128/aac.00239-22 | Increased Innate Immune Susceptibility in Hyperpigmented Bacteriophage-Resistant |
| 35862916 | 10.1016/j.celrep.2021.109567 | 10.1128/mra.00463-22 | Complete Genome Sequence of Pseudomonas aeruginosa Bacteriophage vB_PaeP_PaCe. |
| 35869081 | 10.3389/fphar.2020.578823 | 10.1038/s41467-022-31837-9 | Personalized bacteriophage therapy to treat pandrug-resistant spinal Pseudomonas |
| 35869245 | 10.1038/s41598-021-94902-1 | 10.1038/s41598-022-16841-9 | Antibody CDR amino acids underlying the functionality of antibody repertoires in |
| 35871543 | 10.1101/2022.04.20.488972 | 10.1093/protein/gzac005 | Affinity maturation of TCR-like antibodies using phage display guided by structu |
| 35873140 | 10.1146/annurev-earth-060313-054942 | 10.3389/fcimb.2022.912427 | Comparative Genomic Analysis of the Human Pathogen Wohlfahrtiimonas Chitiniclast |
| 35873174 | 10.1002/dmrr.3043 | 10.3389/fcimb.2022.892291 | Does the Gut Microbiome Play a Role in Obesity in Type 1 Diabetes? Unanswered Qu |
| 35874759 | 10.1016/j.jhepr.2021.100299 | 10.3389/fimmu.2022.932228 | The Impact of Human Microbiotas in Hematopoietic Stem Cell and Organ Transplanta |
| 35876591 | 10.1093/nar/gkab951 | 10.1128/spectrum.01271-22 | An Engineered λ Phage Enables Enhanced and Strain-Specific Killing of Enterohemo |
| 35880080 | 10.3390/antibiotics9040155 | 10.3389/fcimb.2022.909731 | What Is New in the Anti-Pseudomonas aeruginosa Clinical Development Pipeline Sin |
| 35880893 | 10.1093/bioinformatics/btr039 | 10.1128/spectrum.00334-22 | Bioinformatic Analysis of a Set of 14 Temperate Bacteriophages Isolated from Sta |
| 35881358 | 10.1126/science.1254417 | 10.1007/978-1-0716-2189-9_26 | Protocol for Differential Biopanning of P. falciparum Phage Display cDNA Library |
| 35883584 | 10.1093/nar/gnf089 | 10.3390/cells11142141 | A Novel Cre/lox71-Based System for Inducible Expression of Recombinant Proteins  |
| 35884306 | 10.1038/s41598-021-00241-6 | 10.3390/bios12070503 | Recent Advances in Electrochemical Sensing Strategies for Food Allergen Detectio |
| 35886935 | 10.1111/tbed.14196 | 10.3390/ijms23147589 | A Novel Nanobody-Horseradish Peroxidase Fusion Based-Competitive ELISA to Rapidl |
| 35887026 | 10.1002/biot.201800637 | 10.3390/ijms23147678 | Fusion Tag Design Influences Soluble Recombinant Protein Production in Escherich |
| 35887153 | 10.3390/ijms22094541 | 10.3390/ijms23147805 | New Anti-Flavivirus Fusion Loop Human Antibodies with Zika Virus-Neutralizing Po |
| 35887200 | 10.1016/j.jmb.2008.10.012 | 10.3390/ijms23147854 | A Perspective on Studies of Phage DNA Packaging Dynamics. |
| 35887231 | 10.1007/s00253-016-7858-0 | 10.3390/ijms23147885 | Characterization and Genomic Analysis of a New Phage Infecting Helicobacter pylo |
| 35891477 | 10.3390/ijerph17228553 | 10.3390/v14071497 | Impact of Chemical Properties of Human Respiratory Droplets and Aerosol Particle |
| 35891499 | 10.3390/v13102049 | 10.3390/v14071518 | Two Newly Isolated Enterobacter-Specific Bacteriophages: Biological Properties a |
| 35891522 | 10.1186/s12929-022-00806-1 | 10.3390/v14071542 | An Optimized Checkerboard Method for Phage-Antibiotic Synergy Detection. |
| 35893664 | 10.1093/nar/gkz380 | 10.3390/v14081598 | Morphological and Genetic Characterization of Eggerthella lenta Bacteriophage PM |
| 35894699 | 10.7554/eLife.06416 | 10.1093/g3journal/jkac188 | Characterization of the cluster MabR prophages of Mycobacterium abscessus and My |
| 35895271 | 10.3389/fgene.2020.00409 | 10.1007/978-1-0716-2521-7_17 | Tethered Function Assays to Elucidate the Role of RNA-Binding Proteins. |
| 35898510 | 10.1128/IAI.00924-15 | 10.3389/fimmu.2022.931052 | Development of Live Attenuated Salmonella Typhimurium Vaccine Strain Using Radia |
| 35900097 | 10.1073/pnas.1909653116 | 10.1128/mbio.01822-22 | A Bacteriophage-Based, Highly Efficacious, Needle- and Adjuvant-Free, Mucosal CO |
| 35901898 | 10.1016/J.COLSURFB.2018.12.007 | 10.1016/j.scitotenv.2022.157613 | Development of a magnetic nanoparticle-based method for concentrating SARS-CoV-2 |
| 35908075 | 10.1001/jamapediatrics.2021.1929 | 10.1038/s41467-022-32188-1 | Evaluation of transplacental transfer of mRNA vaccine products and functional an |
| 35909125 | 10.1128/AAC.01123-10 | 10.1186/s12866-022-02603-0 | Antibacterial efficacy of lytic phages against multidrug-resistant Pseudomonas a |
| 35918338 | 10.1038/s41467-019-10600-7 | 10.1038/s41467-022-31934-9 | Systematic strategies for developing phage resistant Escherichia coli strains. |
| 35918375 | 10.1038/s41598-019-45549-6 | 10.1038/s41598-022-16939-0 | Isolation, characterization and complete genome analysis of a novel bacteriophag |
| 35918747 | 10.3389/fgene.2022.793884 | 10.1186/s12943-022-01621-w | BTApep-TAT peptide inhibits ADP-ribosylation of BORIS to induce DNA damage in ca |
| 35920561 | 10.1093/nar/gkn179 | 10.1128/msphere.00345-22 | Phage Resistance Accompanies Reduced Fitness of Uropathogenic Escherichia coli i |
| 35920671 | 10.1016/j.mib.2005.06.003 | 10.1128/mra.00478-22 | Genome Sequence of SN1, a Bacteriophage That Infects Sphaerotilus natans and Pse |
| 35920769 | 10.48550/arXiv.1511.08458 | 10.1093/bioinformatics/btac509 | Identification of bacteriophage genome sequences with representation learning. |
| 35925286 | 10.1016/j.ymthe.2019.07.015 | 10.1007/s00262-022-03238-w | Anti-mesothelin CAR-T immunotherapy in patients with ovarian cancer. |
| 35927325 | 10.1093/nar/gkh340 | 10.1038/s41598-022-17678-y | Isolation and characterization of phage display-derived scFv antibodies against  |
| 35931928 | 10.3389/fmicb.2018.01778 | 10.1007/s12223-022-00990-5 | Current knowledge in the use of bacteriophages to combat infections caused by Ps |
| 35934298 | 10.1006/bbrc.1996.6009 | 10.1016/j.bbapap.2022.140831 | Arg236 in human chymotrypsin B2 (CTRB2) is a key determinant of high enzyme acti |
| 35935197 | 10.3389/fmicb.2017.00957 | 10.3389/fmicb.2022.946251 | Isolation and characterization of two homolog phages infecting Pseudomonas aerug |
| 35947606 | 10.1080/19420862.2020.1778435 | 10.1371/journal.pone.0272364 | A humanized nanobody phage display library yields potent binders of SARS CoV-2 s |
| 35948266 | 10.1016/B978-0-12-819265-8.00072-3 | 10.1016/j.micpath.2022.105704 | Gut bacteria, bacteriophages, and probiotics: Tripartite mutualism to quench the |
| 35950843 | 10.1186/1471-2180-14-116 | 10.1128/aac.00506-22 | A Lysozyme Murein Hydrolase with Broad-Spectrum Antibacterial Activity from Ente |
| 35950856 | 10.1111/j.2517-6161.1964.tb00553.x | 10.1128/spectrum.01102-22 | Comparative Assessment of Filtration- and Precipitation-Based Methods for the Co |
| 35955526 | 10.1111/j.1472-765X.2005.01702.x | 10.3390/ijms23158391 | Specific Isolation of Clostridium botulinum Group I Cells by Phage Lysin Cell Wa |
| 35959988 | 10.18129/B9.bioc.BiocParallel | 10.1093/bioinformatics/btac555 | Detecting and quantifying antibody reactivity in PhIP-Seq data with BEER. |
| 35960657 | 10.1111/j.1574-6976.2012.00347.x | 10.1099/mgen.0.000858 | Shooting hoops: globetrotting plasmids spreading more than just antimicrobial re |
| 35970899 | 10.1016/j.cell.2022.07.003 | 10.1038/s41575-022-00677-9 | Phage therapy in IBD. |
| 35972150 | 10.1186/s40168-020-00936-4 | 10.1128/msystems.01522-21 | Genomes from Uncultivated Pelagiphages Reveal Multiple Phylogenetic Clades Exhib |
| 35972246 | 10.1111/imm.13108 | 10.1128/spectrum.01602-22 | Engineered Bacteriophages Containing Anti-CRISPR Suppress Infection of Antibioti |
| 35972274 | 10.1093/nar/gkab951 | 10.1128/spectrum.01356-22 | Phage Resistance Evolution Induces the Sensitivity of Specific Antibiotics in Ps |
| 35976695 | 10.1038/s41589-022-01019-1 | 10.1021/jacs.2c07375 | Lysine-Targeted Reversible Covalent Ligand Discovery for Proteins via Phage Disp |
| 35979493 | 10.1016/j.mib.2013.08.008 | 10.3389/fmicb.2022.905343 | Hypoxia Increases the Tempo of Phage Resistance and Mutational Bottlenecking of  |
| 35980993 | 10.1128/AEM.02847-10 | 10.1371/journal.pone.0273343 | Novel findings in context of molecular diversity and abundance of bacteriophages |
| 35982165 | 10.1016/j.cell.2022.07.003 | 10.1038/s41579-022-00792-z | A phage cocktail for IBD? |
| 35985693 | 10.1038/nmeth.1923 | 10.18632/aging.204222 | Alterations of gut viral signals in atrial fibrillation: complex linkage with gu |
| 35996120 | 10.1080/1547691X.2016.1251512 | 10.1186/s12896-022-00752-8 | Development of a human phage display-derived anti-PD-1 scFv antibody: an attract |
| 35999405 | 10.1097/CMR.0b013e32835312fd | 10.1007/s12032-022-01757-1 | Isolation and characterization of human anti-CD20 single-chain variable fragment |
| 36000841 | 10.1016/j.isci.2020.101437 | 10.1128/jvi.01063-22 | Exploitation of a Bacterium-Encoded Lytic Transglycosylase by a Human Oral Lytic |
| 36001178 | 10.1186/s12934-015-0402-6 | 10.1007/s00203-022-03193-1 | In silico and in vitro analysis of a rational mutation in gIII signal peptide an |
| 36003377 | 10.1089/bio.2019.0067 | 10.3389/fimmu.2022.856497 | Human leukocyte antigen class II gene diversity tunes antibody repertoires to co |
| 36008132 | 10.1172/JCI150201 | 10.1136/ard-2022-222441 | Coexisting autoantibodies against transcription factor Sp4 are associated with d |
| 36012174 | 10.1038/s41467-022-30269-9 | 10.3390/ijms23168917 | Genetic Mining of Newly Isolated Salmophages for Phage Therapy. |
| 36016269 | 10.1038/s41467-019-11306-6 | 10.3390/v14081647 | Comparative Genomics of Closely-Related Gordonia Cluster DR Bacteriophages. |
| 36016303 | 10.1038/sj.onc.1206562 | 10.3390/v14081681 | CIGB-300 Peptide Targets the CK2 Phospho-Acceptor Domain on Human Papillomavirus |
| 36016331 | 10.1021/acsinfecdis.1c00222 | 10.3390/v14081709 | Isolation and Characterization of the Lytic Pseudoxanthomonas kaohsiungensi Phag |
| 36016370 | 10.1128/jvi.14.2.198-202.1974 | 10.3390/v14081748 | Bacteriophage-Based Detection of Staphylococcus aureus in Human Serum. |
| 36016410 | 10.1038/s41598-018-20698-2 | 10.3390/v14081788 | Salmonella Enteritidis Bacteriophages Isolated from Kenyan Poultry Farms Demonst |
| 36026491 | 10.1128/jb.92.3.787-788.1966 | 10.1371/journal.pgen.1010250 | The Vibrio cholerae Seventh Pandemic Islands act in tandem to defend against a c |
| 36036571 | 10.1111/1462-2920.14595 | 10.1128/spectrum.01548-22 | Pf4 Phage Variant Infection Reduces Virulence-Associated Traits in Pseudomonas a |
| 36040048 | 10.1093/oxfordjournals.aje.a118408 | 10.1128/msphere.00303-22 | Aerosolized Hydrogen Peroxide Decontamination of N95 Respirators, with Fit-Testi |
| 36040159 | 10.1101/gr.1239303 | 10.1128/spectrum.00348-22 | Dysbiotic Oral and Gut Viromes in Untreated and Treated Rheumatoid Arthritis Pat |
| 36045380 | 10.1146/annurev-virology-101416-041742 | 10.1186/s12985-022-01847-6 | Metagenomic analysis of viral diversity and a novel astroviruse of forest rodent |
| 36045680 | 10.1016/j.ijid.2022.07.013 | 10.3389/fimmu.2022.941923 | Antibodies against the SARS-CoV-2 S1-RBD cross-react with dengue virus and hinde |
| 36059507 | 10.1371/journal.pone.0161446 | 10.3389/fimmu.2022.942317 | Centaur antibodies: Engineered chimeric equine-human recombinant antibodies. |
| 36066758 | 10.1016/S1473-3099(21)00612-5 | 10.1007/s10096-022-04490-9 | Safety and efficacy of phage therapy in difficult-to-treat infections: studies i |
| 36067253 | 10.1038/s41586-021-03990-6 | 10.1371/journal.ppat.1010799 | Biosynthetic proteins targeting the SARS-CoV-2 spike as anti-virals. |
| 36068216 | 10.1093/bioinformatics/bty560 | 10.1038/s41467-022-32832-w | Extensive gut virome variation and its associations with host and environmental  |
| 36069436 | 10.1016/S1473-3099(17)30489-9 | 10.1128/msphere.00271-22 | The Molecular Epidemiology of Prevalent Klebsiella pneumoniae Strains and Humora |
| 36069454 | 10.1093/bioinformatics/btw354 | 10.1128/msystems.00741-22 | MetaPhage: an Automated Pipeline for Analyzing, Annotating, and Classifying Bact |
| 36069758 | 10.1016/S0002-9610(35)90928-X | 10.1128/cmr.00062-22 | Reassessment of Historical Clinical Trials Supports the Effectiveness of Phage T |
| 36070465 | 10.1093/nar/gkw408 | 10.1021/acschembio.2c00538 | Identification of a Phage Display-Derived Peptide Interacting with the N-Termina |
| 36070530 | 10.1002/0471142727.mb0114s13 | 10.1089/crispr.2022.0058 | Efficient Homology-Directed Repair with Circular Single-Stranded DNA Donors. |
| 36073944 | 10.1007/978-1-4939-0473-0_52 | 10.1128/aem.01068-22 | RecT Affects Prophage Lifestyle and Host Core Cellular Processes in Pseudomonas  |
| 36076084 | 10.1038/s41587-020-0491-6 | 10.1038/s41587-022-01410-2 | High-throughput continuous evolution of compact Cas9 variants targeting single-n |
| 36077327 | 10.3389/fmicb.2018.01854 | 10.3390/ijms23179931 | Glycan-Adhering Lectins and Experimental Evaluation of a Lectin FimH Inhibitor i |
| 36077542 | 10.1038/srep14333 | 10.3390/ijms231710143 | Liposomal Delivery of Newly Identified Prophage Lysins in a Pseudomonas aerugino |
| 36078188 | 10.1007/s12560-015-9216-2 | 10.3390/ijerph191710472 | Application of an Ultrasonic Nebulizer Closet in the Disinfection of Textiles an |
| 36080167 | 10.1007/s12602-017-9336-0 | 10.3390/molecules27175399 | Functional Annotation of Lactiplantibacillus plantarum 13-3 as a Potential Start |
| 36080431 | 10.1128/JB.00359-21 | 10.3390/molecules27175665 | Whole-Genome Analysis of Acinetobacter baumannii Strain AB43 Containing a Type I |
| 36081500 | 10.1371/journal.pone.0096409 | 10.3389/fimmu.2022.972930 | Application of recombinant antibodies for treatment of Clostridioides difficile  |
| 36090087 | 10.1128/AEM.02175-18 | 10.3389/fmicb.2022.955286 | Treatment of Pseudomonas aeruginosa infectious biofilms: Challenges and strategi |
| 36094333 | 10.1101/2020.05.13.093773 | 10.1093/g3journal/jkac244 | Phylogenomic analyses and host range prediction of cluster P mycobacteriophages. |
| 36094767 | 10.1016/j.ijpharm.2018.09.024 | 10.1186/s43141-022-00409-1 | Bacteriophage as a potential therapy to control antibiotic-resistant Pseudomonas |
| 36099883 | 10.1126/scitranslmed.3005661 | 10.1016/j.ccell.2022.07.005 | A covalent inhibitor of K-Ras(G12C) induces MHC class I presentation of haptenat |
| 36104101 | 10.1016/j.ejca.2021.03.038 | 10.1136/jitc-2022-005282 | Generation and in vivo validation of an IL-12 fusion protein based on a novel an |
| 36109427 | 10.1002/0471250953.bi0301s42 | 10.1007/s12033-022-00558-1 | Phylogenetic Analysis of Anti-CRISPR and Member Addition in the Families. |
| 36109550 | 10.1021/acschemneuro.0c00649 | 10.1038/s41598-022-19780-7 | Unbiased approach to identify and assess efficacy of human SARS-CoV-2 neutralizi |
| 36109569 | 10.1006/jmbi.1994.0062 | 10.1038/s41598-022-19699-z | Isolation of a human SARS-CoV-2 neutralizing antibody from a synthetic phage lib |
| 36111782 | 10.1038/nrmicro1614 | 10.7554/eLife.81196 | Mobilome-driven segregation of the resistome in biological wastewater treatment. |
| 36114220 | 10.1038/nmeth.2089 | 10.1038/s41598-022-19471-3 | Reconstituted TAD-size chromatin fibers feature heterogeneous nucleosome cluster |
| 36121163 | 10.7717/peerj.4227 | 10.1128/msystems.00651-22 | A Metagenomic Investigation of Spatial and Temporal Changes in Sewage Microbiome |
| 36129287 | 10.1128/AEM.00518-15 | 10.1128/spectrum.02072-22 | Characterization of Phage Resistance and Their Impacts on Bacterial Fitness in P |
| 36129288 | 10.1002/jbio.202000232 | 10.1128/aem.01221-22 | Effects of UV-C Disinfection on N95 and KN95 Filtering Facepiece Respirator Reus |
| 36133139 | 10.1016/S0969-2126(01)00167-8 | 10.1039/c9na00461k | Phage-mimicking antibacterial core-shell nanoparticles. |
| 36135376 | 10.1371/journal.pone.0117163 | 10.1128/spectrum.02874-22 | The Selection of Antibiotic- and Bacteriophage-Resistant Pseudomonas aeruginosa  |
| 36136541 | 10.1128/JCM.01269-20 | 10.3390/toxins14090603 | Genomic Analysis of Shiga Toxin-Producing E. coli O157 Cattle and Clinical Isola |
| 36137152 | 10.1136/gutjnl-2013-306155 | 10.1371/journal.pone.0274283 | Patient-derived monoclonal antibody neutralizes HCV infection in vitro and vivo  |
| 36138514 | 10.3390/microorganisms9061143 | 10.1080/19490976.2022.2122667 | Apyrase decreases phage induction and Shiga toxin release from E. coli O157:H7 a |
| 36140695 | 10.1016/0304-4165(65)90096-6 | 10.3390/genes13091527 | Transcriptome Analyses of Prophage in Mediating Persistent Methicillin-Resistant |
| 36146653 | 10.1128/mr.51.4.381-395.1987 | 10.3390/v14091842 | Varidnaviruses in the Human Gut: A Major Expansion of the Order Vinavirales. |
| 36146802 | 10.1128/AEM.02195-08 | 10.3390/v14091996 | From Farm to Fork: Streptococcus suis as a Model for the Development of Novel Ph |
| 36148618 | 10.1128/mBio.01462-20 | 10.2340/17453674.2022.4579 | Salphage: salvage bacteriophage therapy for a recalcitrant Klebsiella pneumoniae |
| 36149952 | 10.1145/2939672.2939785 | 10.1126/sciadv.abq2422 | Systemic antibody responses against human microbiota flagellins are overrepresen |
| 36154277 | 10.1093/nar/gky1080 | 10.1128/spectrum.00502-22 | Microbial Interdomain Interactions Delineate the Disruptive Intestinal Homeostas |
| 36155858 | 10.3390/molecules22060871 | 10.1007/s00284-022-03029-7 | Emerging Non-Traditional Approaches to Combat Antibiotic Resistance. |
| 36160186 | 10.1128/AAC.02242-19 | 10.3389/fmicb.2022.988725 | Expert workshop summary: Advancing toward a standardized murine model to evaluat |
| 36163386 | 10.1038/s41586-021-03819-2 | 10.1038/s41589-022-01137-w | Structural basis of AcrIF24 as an anti-CRISPR protein and transcriptional suppre |
| 36163472 | 10.1093/bioinformatics/btu638 | 10.1038/s41522-022-00334-8 | An in vitro fermentation model to study the impact of bacteriophages targeting S |
| 36165045 | 10.1186/s40168-017-0282-6 | 10.1097/MOG.0000000000000885 | The gut virome in health and disease: new insights and associations. |
| 36165773 | 10.1371/journal.pone.0225671 | 10.1128/spectrum.02358-22 | Bacteriophage Effectively Rescues Pneumonia Caused by Prevalent Multidrug-Resist |
| 36167817 | 10.1016/j.micpath.2020.104200 | 10.1038/s41390-022-02318-y | Multi-omic factors associated with future wheezing in infants. |
| 36171633 | 10.1016/j.cell.2019.11.031 | 10.1186/s13046-022-02483-2 | Peptide-based PROTAC degrader of FOXM1 suppresses cancer and decreases GLUT1 and |
| 36174018 | 10.1007/978-l-4939-2272-7_5 | 10.1021/acschembio.2c00565 | Novel Regioselective Approach to Cyclize Phage-Displayed Peptides in Combination |
| 36175406 | 10.1093/nar/gkx343 | 10.1038/s41467-022-33294-w | Bacteriophage-antibiotic combination therapy against extensively drug-resistant  |
| 36175428 | 10.1038/s41592-018-0260-3 | 10.1038/s41467-022-32979-6 | Experimental validation that human microbiome phages use alternative genetic cod |
| 36175701 | 10.1182/blood-2015-11-680546 | 10.1007/s12032-022-01806-9 | Targeting acute myeloid cell surface using a recombinant antibody isolated from  |
| 36177589 | 10.1038/srep26717 | 10.3760/cma.j.cn501120-20210929-00338 | [Research advances on the interaction between Pseudomonas aeruginosa bacteriopha |
| 36178514 | 10.1038/s41396-020-00860-3 | 10.1007/s00253-022-12144-1 | Novel PCR detection of CRISPR/Cas systems in Pseudomonas aeruginosa and its corr |
| 36183106 | 10.1007/s12015-022-10344-w | 10.1186/s12951-022-01636-x | Huc-MSC-derived exosomes modified with the targeting peptide of aHSCs for liver  |
| 36188006 | 10.1152/ajplung.00355.2002 | 10.3389/fmicb.2022.979610 | Evaluation of phages and liposomes as combination therapy to counteract Pseudomo |
| 36189209 | 10.1038/s41586-021-04385-3 | 10.3389/fimmu.2022.930975 | SARS-CoV-2 neutralizing camelid heavy-chain-only antibodies as powerful tools fo |
| 36189235 | 10.3390/molecules27072198 | 10.3389/fimmu.2022.965446 | Isolation of an escape-resistant SARS-CoV-2 neutralizing nanobody from a novel s |
| 36190827 | 10.3945/ajcn.117.158816 | 10.1099/mgen.0.000874 | Luminal and mucosa-associated caecal microbiota of chickens after experimental C |
| 36192374 | 10.1016/j.cell.2020.05.042 | 10.1038/s41467-022-33030-4 | IgG-like bispecific antibodies with potent and synergistic neutralization agains |
| 36192747 | 10.1002/bit.22135 | 10.1186/s12987-022-00374-4 | VHHs as tools for therapeutic protein delivery to the central nervous system. |
| 36194307 | 10.1016/j.jmb.2017.12.007 | 10.1007/s00705-022-05617-1 | Escherichia coli phage phi2013: genomic analysis and receptor identification. |
| 36198417 | 10.1128/mSystems.00756-19 | 10.1183/16000617.0121-2022 | Phage therapy for pulmonary infections: lessons from clinical experiences and ke |
| 36199029 | 10.1128/jb.179.10.3239-3243.1997 | 10.1186/s12864-022-08909-7 | Global diversity and distribution of prophages are lineage-specific within the R |
| 36204777 | 10.1021/acs.bioconjchem.9b00713 | 10.1021/acs.jmedchem.2c00065 | Discovery of BT8009: A Nectin-4 Targeting Bicycle Toxin Conjugate for the Treatm |
| 36207326 | 10.1126/science.abd0831 | 10.1038/s41598-022-20849-6 | Differential patterns of cross-reactive antibody response against SARS-CoV-2 spi |
| 36211408 | 10.3390/cancers13205250 | 10.3389/fimmu.2022.977235 | Proline metabolism reprogramming of trained macrophages induced by early respira |
| 36222703 | 10.1101/2020.07.11.198606v1 | 10.1128/mra.00740-22 | Complete Genome Sequence of Pseudomonas Phage Motto. |
| 36222821 | 10.1016/j.healun.2019.01.001 | 10.1097/MOT.0000000000001029 | Role of bacteriophage therapy for resistant infections in transplant recipients. |
| 36226992 | 10.1371/journal.pcbi.1002195 | 10.1128/aem.01146-22 | Genomic Characterization and Antimicrobial Susceptibility of Dromedary-Associate |
| 36229661 | 10.1002/jbio.201500150 | 10.1038/s41551-022-00948-5 | Collagen-binding peptides for the enhanced imaging, lubrication and regeneration |
| 36239354 | 10.1002/ijc.10212 | 10.3724/abbs.2022141 | Identification and characterization of blocking nanobodies against human CD70. |
| 36243697 | 10.1093/nar/gkz239 | 10.1186/s12864-022-08927-5 | Comparative genome analysis of mycobacteria focusing on tRNA and non-coding RNA. |
| 36246261 | 10.1111/mmi.12614 | 10.3389/fmicb.2022.987656 | The virulence factor regulator and quorum sensing regulate the type I-F CRISPR-C |
| 36250060 | 10.1186/s12859-017-1512-4 | 10.3389/fcimb.2022.933516 | Revealing bacteria-phage interactions in human microbiome through the CRISPR-Cas |
| 36253000 | 10.1172/JCI96061 | 10.1136/jitc-2022-004590 | PD-L1/TLR7 dual-targeting nanobody-drug conjugate mediates potent tumor regressi |
| 36257408 | 10.1101/2022.07.19.500692 | 10.1016/j.jbc.2022.102608 | Deep mutational scanning and massively parallel kinetics of plasminogen activato |
| 36258079 | 10.1039/c3cc40869h | 10.1007/978-3-031-08491-1_13 | Pseudomonas aeruginosa in the Cystic Fibrosis Lung. |
| 36263241 | 10.1016/j.chom.2019.01.019 | 10.1155/2022/4913146 | Current Status of Phage Therapy against Infectious Diseases and Potential Applic |
| 36274728 | 10.1038/s41598-017-13363-7 | 10.3389/fmicb.2022.1004733 | Phage-resistant Pseudomonas aeruginosa against a novel lytic phage JJ01 exhibits |
| 36279314 | 10.1371/journal.pgen.1005556 | 10.1371/journal.pgen.1010467 | Activation of the integrative and conjugative element Tn916 causes growth arrest |
| 36283250 | 10.3390/vaccines8040621 | 10.1016/j.bmc.2022.117066 | Development of carbohydrate based next-generation anti-pertussis vaccines. |
| 36287952 | 10.1016/j.jpba.2012.10.008 | 10.3390/toxins14100683 | Construction, Characterization, and Application of a Nonpathogenic Virus-like Mo |
| 36289234 | 10.7554/eLife.20352 | 10.1038/s41597-022-01779-4 | A dataset comprised of binding interactions for 104,972 antibodies against a SAR |
| 36289309 | 10.1093/jac/dkaa311 | 10.1038/s41396-022-01338-0 | Dominance of phage particles carrying antibiotic resistance genes in the viromes |
| 36290106 | 10.1385/1-59259-584-7:531 | 10.3390/antibiotics11101448 | Improvement of the Antibacterial Activity of Phage Lysin-Derived Peptide P87 thr |
| 36291042 | 10.3390/v10080397 | 10.3390/bios12100905 | Bacteriophage-Based Biosensors: A Platform for Detection of Foodborne Bacterial  |
| 36293124 | 10.1371/journal.pone.0063906 | 10.3390/ijms232012267 | Neutralizing Ability of a Single Domain VNAR Antibody: In Vitro Neutralization o |
| 36293532 | 10.1007/978-3-642-01144-3_50 | 10.3390/ijms232012677 | Development of Anti-LRRC15 Small Fragments for Imaging Purposes Using a Phage-Di |
| 36298860 | 10.1210/er.2010-0027 | 10.3390/v14102305 | Diversity and Ecology of Caudoviricetes Phages with Genome Terminal Repeats in F |
| 36299622 | 10.1186/s13059-021-02463-3 | 10.3389/fcimb.2022.1043256 | Editorial: Gut virome and human health. |
| 36300623 | 10.1073/pnas.1906251116 | 10.7554/eLife.78550 | Autoantibody discovery across monogenic, acquired, and COVID-19-associated autoi |
| 36301743 | 10.3390/gels7020041 | 10.1021/acsbiomaterials.2c00777 | Modulation of Biofilm Mechanics by DNA Structure and Cell Type. |
| 36303134 | 10.1002/9780470559277.ch110148 | 10.1186/s12951-022-01665-6 | Towards preventing exfoliation glaucoma by targeting and removing fibrillar aggr |
| 36307814 | 10.1016/j.biopha.2019.108905 | 10.1186/s12896-022-00760-8 | Identification of a novel fully human anti-toxic shock syndrome toxin (TSST)-1 s |
| 36312416 | 10.1016/j.ab.2007.10.015 | 10.1021/acsomega.2c05539 | Isolation of a Peptide That Binds to Pseudomonas aeruginosa Lytic Bacteriophage. |
| 36313802 | 10.1093/bioinformatics/btv053 | 10.1016/j.crmeth.2022.100318 | CasPlay provides a gRNA-barcoded CRISPR-based display platform for antibody repe |
| 36314797 | 10.7554/eLife.19706 | 10.1128/mbio.02171-22 | Mobile Element Integration Reveals a Chromosome Dimer Resolution System in Legio |
| 36314905 | 10.1016/j.scitotenv.2019.04.435 | 10.1128/spectrum.01720-22 | Quantitative Assessment of Microbial Pathogens and Indicators of Wastewater Trea |
| 36316452 | 10.1101/2022.03.25.485874 | 10.1038/s41564-022-01243-4 | Bacteriophage genome engineering with CRISPR-Cas13a. |
| 36320594 | 10.1172/JCI136577 | 10.20411/pai.v7i2.516 | Therapeutic Bacteriophages for Gram-Negative Bacterial Infections in Animals and |
| 36322255 | 10.1038/ncomms10937 | 10.1007/s10096-022-04512-6 | Coexistence of tet(A) and blaKPC-2 in the ST11 hypervirulent tigecycline- and ca |
| 36322762 | 10.1099/MIC.0.001093 | 10.1073/pnas.2210299119 | Control of resistance against bacteriophage killing by a metabolic regulator in  |
| 36326506 | 10.3390/v12111268 | 10.1128/spectrum.02960-22 | Comparative Analysis of Novel Lytic Phages for Biological Control of Phytopathog |
| 36329839 | 10.1016/j.addr.2022.114378 | 10.3389/fmicb.2022.1031101 | Topically applied bacteriophage to control multi-drug resistant Pseudomonas aeru |
| 36335167 | 10.2147/ijn.s50070 | 10.1038/s41598-022-23465-6 | Antiviral efficacy of cerium oxide nanoparticles. |
| 36336729 | 10.1186/s12985-020-01485-w | 10.1007/s10123-022-00292-3 | Characteristics of a novel temperate bacteriophage against Staphylococcus arlett |
| 36336785 | 10.4103/1673-5374.226380 | 10.1002/ctm2.1100 | Comprehensive profiling of the human viral exposome in households containing an  |
| 36343978 | 10.1002/hep.32571 | 10.1136/gutjnl-2022-328403 | Longitudinal transkingdom gut microbial approach towards decompensation in outpa |
| 36350341 | 10.1016/S0022-5347(05)65965-4 | 10.1007/s00216-022-04361-4 | Quantitative detection of urinary bladder cancer antigen via peptide-immobilized |
| 36350460 | 10.1007/s10552-019-01242-7 | 10.1007/s10123-022-00293-2 | Bacteriophage therapy as an alternative technique for treatment of multidrug-res |
| 36353213 | 10.1016/j.gpb.2022.02.003 | 10.3389/fbinf.2022.932319 | Bacteriophage Genetic Edition Using LSTM. |
| 36357719 | 10.1038/s41587-019-0032-3 | 10.1038/s41587-022-01533-6 | Evolution of an adenine base editor into a small, efficient cytosine base editor |
| 36357763 | 10.1093/genetics/148.4.1539 | 10.1007/s11262-022-01954-0 | Isolation, characterization, and genomic analysis of vB_PaeS_TUMS_P81, a lytic b |
| 36359751 | 10.1002/jev2.12057 | 10.3390/cells11213355 | Screening, Expression, and Identification of Nanobody against SARS-CoV-2 Spike P |
| 36360258 | 10.1128/CMR.00046-08 | 10.3390/genes13112024 | Multi-Omic Profiles in Infants at Risk for Food Reactions. |
| 36361776 | 10.1093/nar/gkh340 | 10.3390/ijms232112988 | Isolation and Characterization of Two Novel Siphoviruses Novomoskovsk and Bolokh |
| 36362137 | 10.1038/sj.emboj.7600158 | 10.3390/ijms232113353 | Recognition of a Clickable Abasic Site Analog by DNA Polymerases and DNA Repair  |
| 36364436 | 10.1038/s41568-021-00400-x | 10.3390/molecules27217609 | Identification of an IGF2BP2-Targeted Peptide for Near-Infrared Imaging of Esoph |
| 36366441 | 10.3390/v10020064 | 10.3390/v14112339 | Isolation and Characterization of Lytic Pseudomonas aeruginosa Bacteriophages Is |
| 36366454 | 10.21775/cimb.040.267 | 10.3390/v14112356 | Isolation, Characterization, and Genome Analysis of a Novel Bacteriophage, Esche |
| 36366479 | 10.1371/journal.pone.0205728 | 10.3390/v14112381 | Isolation and Characterization of Lytic Bacteriophages Active against Clinical S |
| 36366569 | 10.1086/381502 | 10.3390/v14112471 | Influence of Staphylococcus aureus Strain Background on Sa3int Phage Life Cycle  |
| 36371482 | 10.1016/S2542-5196(21)00051-6 | 10.1038/s41598-022-24134-4 | Escherichia coli ST155 as a production-host of three different polyvalent phages |
| 36374021 | 10.1371/journal.pone.0246020 | 10.1128/spectrum.01994-22 | Characterization of Novel Klebsiella Phage PG14 and Its Antibiofilm Efficacy. |
| 36376440 | 10.1002/ijc.31274 | 10.1038/s42003-022-04191-1 | Anti-tumor effects of P-LPK-CPT, a peptide-camptothecin conjugate, in colorectal |
| 36377945 | 10.1093/bioinformatics/btu153 | 10.1128/spectrum.02641-22 | SourceFinder: a Machine-Learning-Based Tool for Identification of Chromosomal, P |
| 36379931 | 10.1093/bioinformatics/btr174 | 10.1038/s41467-022-34269-7 | High-affinity chromodomains engineered for improved detection of histone methyla |
| 36382789 | 10.3389/fmicb.2016.00680 | 10.1099/mgen.0.000897 | Increased phage resistance through lysogenic conversion accompanying emergence o |
| 36388368 | 10.1016/j.ajic.2020.12.007 | 10.3389/fpubh.2022.1010802 | Assessment of potential for viral contamination of user and environment via aero |
| 36389774 | 10.1016/j.cell.2022.07.003 | 10.3389/fimmu.2022.1057892 | Phage therapy for Clostridioides difficile infection. |
| 36399439 | 10.3390/genes11090999 | 10.1371/journal.pone.0271847 | Gene co-expression network analysis of the human gut commensal bacterium Faecali |
| 36399504 | 10.1093/bioinformatics/btq010 | 10.1371/journal.ppat.1010991 | Dissecting the invasion of Galleria mellonella by Yersinia enterocolitica reveal |
| 36402800 | 10.1088/0022-3727/47/47/475203 | 10.1038/s41598-022-23660-5 | Plasma-generated reactive water mist for disinfection of N95 respirators laden w |
| 36413017 | 10.1093/nar/gkw290 | 10.1128/msystems.00817-22 | AcaFinder: Genome Mining for Anti-CRISPR-Associated Genes. |
| 36413074 | 10.1136/gut.2003.032805 | 10.1093/g3journal/jkac293 | Impact of antibiotic perturbation on fecal viral communities in mice. |
| 36417939 | 10.3390/v10070351 | 10.3201/eid2812.220572 | Emergence and Evolutionary Response of Vibrio cholerae to Novel Bacteriophage, D |
| 36418461 | 10.1109/TED.2019.2898455 | 10.1038/s41598-022-24658-9 | Bio-inspired electronic fingerprint PUF device with single-walled carbon nanotub |
| 36422769 | 10.1021/acs.est.6b00876 | 10.1007/s10123-022-00300-6 | Antiviral activity of nano-monocaprin against Phi6 as a surrogate for SARS-CoV-2 |
| 36422842 | 10.1371/journal.ppat.1002946 | 10.1007/s12275-022-2476-2 | Construction of high-density transposon mutant library of Staphylococcus aureus  |
| 36423170 | 10.1073/pnas.1305923110 | 10.3390/v14112561 | Isolation and Characterization of a Phapecoctavirus Infecting Multidrug-Resistan |
| 36423191 | 10.1164/rccm.201904-0839LE | 10.3390/v14112582 | Effects of Klebsiella pneumoniae Bacteriophages on IRAK3 Knockdown/Knockout THP- |
| 36423198 | 10.1038/s41467-020-19619-7 | 10.3390/v14112589 | Heterologous RNA Recombination in the Cystoviruses φ6 and φ8: A Mechanism of Vir |
| 36424464 | 10.1074/jbc.M704524200 | 10.1038/s41551-022-00956-5 | An anti-CD98 antibody displaying pH-dependent Fc-mediated tumour-specific activi |
| 36434275 | 10.1093/nar/gkaa1038 | 10.1038/s42003-022-04238-3 | A small bacteriophage protein determines the hierarchy over co-residential jumbo |
| 36439110 | 10.1038/s41467-017-02312-7 | 10.3389/fimmu.2022.1022418 | Generation of high affinity ICAM-1-specific nanobodies and evaluation of their s |
| 36443683 | 10.1371/journal.pcbi.1005595 | 10.1186/s12864-022-09023-4 | Tyroviruses are a new group of temperate phages that infect Bacillus species in  |
| 36443864 | 10.1097/SMJ.0b013e31817a8b3f | 10.1186/s12985-022-01924-w | Dermatological manifestations of tick-borne viral infections found in the United |
| 36445133 | 10.1016/bs.mie.2018.12.034 | 10.1128/spectrum.03511-22 | A Novel XRE-Type Regulator Mediates Phage Lytic Development and Multiple Host Me |
| 36445388 | 10.1074/jbc.RA118.006968 | 10.1007/s00253-022-12306-1 | Production, characterization, and application of phage-derived PK34 recombinant  |
| 36445603 | 10.1128/IAI.71.10.5750-5755.2003 | 10.1007/s11259-022-10043-4 | Selection of Brucella abortus mimetic epitopes for fast diagnostic purposes in c |
| 36445694 | 10.1016/j.btre.2015.08.003 | 10.1128/mbio.03017-22 | Phage Therapy for Mosquito Larval Control: a Proof-of-Principle Study. |
| 36446974 | 10.1006/jmbi.1999.3471 | 10.1007/978-1-0716-2859-1_12 | The Lambda Display Technology: A Useful Tool for the Identification of Ubiquitin |
| 36450725 | 10.1128/JB.187.17.5977-5983.2005 | 10.1038/s41467-022-34876-4 | Polyploidy, regular patterning of genome copies, and unusual control of DNA part |
| 36453020 | 10.1172/JCI122216 | 10.1002/1878-0261.13352 | Screening of an annexin-A2-targeted heptapeptide for pancreatic adenocarcinoma l |
| 36456600 | 10.1093/nar/gkw329 | 10.1038/s41598-022-25257-4 | Identification of a novel peptide ligand for the cancer-specific receptor mutati |
| 36459997 | 10.1093/bioinformatics/btq033 | 10.1016/j.chom.2022.11.002 | Widespread, human-associated redondoviruses infect the commensal protozoan Entam |
| 36467721 | 10.1002/bit.24630 | 10.3389/fcimb.2022.1060825 | Bacteriophage-based decontamination to control environmental colonization by Sta |
| 36470427 | 10.1101/2021.10.04.463034 | 10.1016/j.jbc.2022.102769 | Identification, binding, and structural characterization of single domain anti-P |
| 36473906 | 10.1093/bioinformatics/btm039 | 10.1038/s41598-022-25636-x | Broad host range may be a key to long-term persistence of bacteriophages infecti |
| 36475872 | 10.1093/bioinformatics/btq413 | 10.1128/msystems.00564-22 | High Level of Interaction between Phages and Bacteria in an Artisanal Raw Milk C |
| 36476652 | 10.1093/bib/bbx108 | 10.1038/s41598-022-25576-6 | A novel virulent Litunavirus phage possesses therapeutic value against multidrug |
| 36497081 | 10.1007/s40263-022-00930-4 | 10.3390/cells11233822 | A Single Chain Fragment Variant Binding Misfolded Alpha-Synuclein Exhibits Neuro |
| 36499634 | 10.1017/S0031182000024768 | 10.3390/ijms232315307 | Construction of scFv Antibodies against the Outer Loops of the Microsporidium No |
| 36500236 | 10.1016/j.actbio.2014.07.031 | 10.3390/molecules27238144 | Targeted Nanoparticles for the Binding of Injured Vascular Endothelium after Per |
| 36503913 | 10.1101/cshperspect.a000414 | 10.1038/s41598-022-25122-4 | Antimicrobial properties of a multi-component alloy. |
| 36504140 | 10.1159/000437426 | 10.1007/s10123-022-00310-4 | Diverse infective and lytic machineries identified in genome analysis of tailed  |
| 36504499 | 10.1038/nprot.2006.24 | 10.1016/j.mex.2022.101941 | Determination of Acr-mediated immunosuppression in Pseudomonas aeruginosa. |
| 36506027 | 10.1038/s41598-017-17641-2 | 10.3389/fcimb.2022.952491 | Deciphering the genetic network and programmed regulation of antimicrobial resis |
| 36508095 | 10.1038/ncomms14187 | 10.1007/s11356-022-24637-7 | Bacteriophages diversity in India's major river Ganga: a repository to regulate  |
| 36511681 | 10.1038/nprot.2016.169 | 10.1128/spectrum.03562-22 | Novel Affibody Molecules Specifically Bind to SARS-CoV-2 Spike Protein and Effic |
| 36513793 | 10.1093/nar/gky427 | 10.1038/s41598-022-26097-y | Differential critical residues on the overlapped region of the non-structural pr |
| 36517572 | 10.1093/bioinformatics/btt086 | 10.1038/s41598-022-26198-8 | Impact of Shiga-toxin encoding gene transduction from O80:H2 Shiga toxigenic Esc |
| 36522388 | 10.1007/s10461-007-9229-4 | 10.1038/s41598-022-25979-5 | Impact of HIV infection and integrase strand transfer inhibitors-based treatment |
| 36527491 | 10.1128/JB.183.1.358-366.2001 | 10.1007/s00705-022-05663-9 | Characterization and genomic analysis of JC01, a novel bacteriophage infecting C |
| 36528171 | 10.1111/j.1751-7915.2008.00058.x | 10.1016/j.virusres.2022.199025 | Characterization and the host specificity of Pet-CM3-4, a new phage infecting Cr |
| 36533913 | 10.1093/nar/gkz239 | 10.1128/spectrum.03617-22 | Genomic and Evolutionary Insights into Australian Toxigenic Vibrio cholerae O1 S |
| 36534288 | 10.3851/IMP2125 | 10.1007/978-1-0716-2895-9_12 | The Rhizopus Holobiont: A Model to Decipher Fungal-Bacterial-Viral Symbioses. |
| 36534707 | 10.1371/journal.ppat.0020116 | 10.1371/journal.ppat.1011033 | Antibody epitope profiling of the KSHV LANA protein using VirScan. |
| 36539881 | 10.1073/pnas.1909374116 | 10.1186/s13073-022-01147-2 | Post-vaccine epidemiology of serotype 3 pneumococci identifies transformation in |
| 36541762 | 10.1093/bib/bbx088 | 10.1128/msystems.00342-22 | Compendium-Wide Analysis of Pseudomonas aeruginosa Core and Accessory Genes Reve |
| 36541779 | 10.1016/0022-2836(76)90119-4 | 10.1128/spectrum.02663-21 | Single-Cell Approach Reveals Intercellular Heterogeneity in Phage-Producing Capa |
| 36546891 | 10.1111/1751-7915.13535 | 10.1002/cpz1.605 | Recombineering in Non-Model Bacteria. |
| 36548304 | 10.1016/j.cell.2020.06.011 | 10.1371/journal.ppat.1011065 | Ubiquitin variants potently inhibit SARS-CoV-2 PLpro and viral replication via a |
| 36548718 | 10.1038/s41598-017-14519-1 | 10.3390/toxins14120821 | A Novel Cost-Effective Nanobody against Fumonisin B1 Contaminations: Efficacy Te |
| 36550315 | 10.1038/s41564-021-00928-6 | 10.1038/s41564-022-01280-z | A database to identify the human gut virome. |
| 36550570 | 10.1126/scitranslmed.abi9215 | 10.1186/s12929-022-00891-2 | Monoclonal antibodies against S2 subunit of spike protein exhibit broad reactivi |
| 36551303 | 10.1016/j.nano.2019.102145 | 10.3390/biom12121875 | Effect of the Biopolymer Carrier on Staphylococcus aureus Bacteriophage Lytic Ac |
| 36553341 | 10.1002/ppul.25712 | 10.3390/children9121898 | Inflammation and Infection in Cystic Fibrosis: Update for the Clinician. |
| 36554950 | 10.1016/j.jhin.2021.04.007 | 10.3390/ijerph192417074 | Infectivity of SARS-CoV-2 on Inanimate Surfaces: Don't Trust Ct Value. |
| 36555373 | 10.1093/bioinformatics/bts091 | 10.3390/ijms232415731 | Comprehensive Genome Analysis of Neisseria meningitidis from South America Revea |
| 36557761 | 10.1007/s00281-007-0078-z | 10.3390/microorganisms10122508 | Genome-Based Analysis of Virulence Factors and Biofilm Formation in Novel P. aer |
| 36560618 | 10.1186/1477-7525-1-62 | 10.3390/v14122614 | Bacteriophage Cocktails in the Post-COVID Rehabilitation. |
| 36560621 | 10.1016/j.jgar.2022.01.019 | 10.3390/v14122617 | How Interest in Phages Has Bloomed into a Leading Medical Research Activity in P |
| 36560636 | 10.1038/s41596-020-00424-x | 10.3390/v14122632 | Comparing In Vitro Faecal Fermentation Methods as Surrogates for Phage Therapy A |
| 36560651 | 10.1111/1750-3841.15042 | 10.3390/v14122647 | Broad-Spectrum Salmonella Phages PSE-D1 and PST-H1 Controls Salmonella in Foods. |
| 36560673 | 10.3390/v10080427 | 10.3390/v14122669 | Recombination Events in Putative Tail Fibre Gene in Litunavirus Phages Infecting |
| 36560706 | 10.1089/phage.2020.0036 | 10.3390/v14122704 | Advancements in the Use of Bacteriophages to Combat the Kiwifruit Canker Phytopa |
| 36560744 | 10.1371/journal.pone.0168985 | 10.3390/v14122740 | Two Novel Yersinia pestis Bacteriophages with a Broad Host Range: Potential as B |
| 36560763 | 10.3390/ijms21144952 | 10.3390/v14122760 | In Vitro and Pre-Clinical Evaluation of Locally Isolated Phages, vB_Pae_SMP1 and |
| 36560776 | 10.3389/fphar.2021.699054 | 10.3390/v14122772 | Diversity, Dynamics and Therapeutic Application of Clostridioides difficile Bact |
| 36562822 | 10.3390/v13030506 | 10.1007/s00284-022-03152-5 | Isolation, Characterization, and Comparative Genomic Analysis of vB_Pd_C23, a No |
| 36565337 | 10.1093/genetics/148.4.1539 | 10.1007/s00705-022-05692-4 | Isolation, characterization, and genomic analysis of vB_PaeP_TUMS_P121, a new ly |
| 36568830 | 10.1080/21597081.2016.1270090 | *(none)* | Inhaled Bacteriophage Therapy for Multi-Drug Resistant Achromobacter. |
| 36569196 | 10.3390/antibiotics9060304 | 10.3389/fcimb.2022.1032052 | Rapid hydrogel-based phage susceptibility test for pathogenic bacteria. |
| 36578069 | 10.1016/S1473-3099(20)30330-3 | 10.1186/s13063-022-07047-5 | Safety and microbiological activity of phage therapy in persons with cystic fibr |
| 36584356 | 10.1016/j.cca.2016.05.013 | 10.1021/acssensors.2c02001 | Multiarray Biosensor for Diagnosing Lung Cancer Based on Gap Plasmonic Color Fil |
| 36585418 | 10.1371/journal.pone.0158634 | 10.1038/s41598-022-27161-3 | Nanobodies targeting ABCC3 for immunotargeted applications in glioblastoma. |
| 36591313 | 10.1038/nrmicro1130 | 10.3389/fimmu.2022.1058905 | Pasteurella multocida toxin - lessons learned from a mitogenic toxin. |
| 36591314 | 10.1371/journal.pone.0051813 | 10.3389/fimmu.2022.957233 | EGFR-targeted bacteriophage lambda penetrates model stromal and colorectal carci |
| 36596342 | 10.1038/s41565-019-0539-2 | 10.1016/j.jconrel.2022.12.057 | TAxI-peptide targeted Cas12a ribonuclease protein nanoformulations increase geno |
| 36596850 | 10.1007/978-1-60327-164-6_3 | 10.1038/s41598-022-27341-1 | Study of 32 new phage tail-like bacteriocins (pyocins) from a clinical collectio |
| 36598587 | 10.1002/art.41511 | 10.1007/s10067-022-06451-1 | The composition and function profile of the gut microbiota of patients with prim |
| 36600213 | 10.3389/fmicb.2019.03090 | 10.1186/s12866-022-02738-0 | Phage-antibiotic synergy reduces Burkholderia cenocepacia population. |
| 36600337 | 10.1016/j.cell.2022.04.024 | 10.1136/bmjopen-2022-065401 | Standardised treatment and monitoring protocol to assess safety and tolerability |
| 36602321 | 10.1007/978-1-4939-0473-0_9 | 10.1128/spectrum.03911-22 | Pseudomonas aeruginosa Resists Phage Infection via Eavesdropping on Indole Signa |
| 36602353 | 10.1007/s00003-006-0020-7 | 10.1128/aem.01596-22 | A Flexible and Efficient Microfluidics Platform for the Characterization and Iso |
| 36604462 | 10.3389/fimmu.2022.843183 | 10.1038/s41598-022-26696-9 | Characterisation and sequencing of the novel phage Abp95, which is effective aga |
| 36608168 | 10.1186/1471-2334-13-568 | 10.1371/journal.pntd.0011019 | Anti-Trypanosoma cruzi antibody profiling in patients with Chagas disease treate |
| 36610752 | 10.1128/microbiolspec.MTBP-0016-2017 | 10.1093/nar/gkac1220 | The ESKAPE mobilome contributes to the spread of antimicrobial resistance and CR |
| 36613917 | 10.1007/s10928-007-9065-1 | 10.3390/ijms24010475 | Half-Life Extension and Biodistribution Modulation of Biotherapeutics via Red Bl |
| 36619993 | 10.1371/journal.pone.0000564 | 10.3389/fmicb.2022.1093670 | Motility increase of adherent invasive Escherichia coli (AIEC) induced by a sub- |
| 36622155 | 10.57873/T34W2R | 10.1128/msystems.00701-22 | Longitudinal, Multi-Platform Metagenomics Yields a High-Quality Genomic Catalog  |
| 36622213 | 10.1186/1471-2105-15-7 | 10.1128/spectrum.03232-22 | The Bacteriophage-Phage-Inducible Chromosomal Island Arms Race Designs an Interk |
| 36625915 | 10.3389/fmed.2017.00094 | 10.1007/s00253-022-12349-4 | The impact of agarose immobilization on the activity of lytic Pseudomonas aerugi |
| 36635459 | 10.5740/jaoacint.11-482 | 10.1007/s13258-022-01348-4 | Genomic insights of Leclercia adecarboxylata strains linked to an outbreak in pu |
| 36645771 | 10.1042/BST20130129 | 10.7554/eLife.81692 | Dynamics of immune memory and learning in bacterial communities. |
| 36646746 | 10.1093/nar/gkt263 | 10.1038/s41598-023-27734-w | Monitoring phage-induced lysis of gram-negatives in real time using a fluorescen |
| 36647580 | 10.1002/(SICI)1521-3773(19990115)38:1/2<236::AID-ANIE236>3.0.CO;2-M | 10.1021/acschembio.2c00735 | Discovery of All-d-Peptide Inhibitors of SARS-CoV-2 3C-like Protease. |
| 36651770 | 10.3758/bf03193146 | 10.1128/spectrum.03377-22 | Discovery of Novel Transketolase Epitopes and the Development of IgG-Based Tuber |
| 36669116 | 10.1038/s41579-019-0299-x | 10.1073/pnas.2216084120 | Antibiotics that affect translation can antagonize phage infectivity by interfer |
| 36671367 | 10.1093/nar/gkab301 | 10.3390/antibiotics12010165 | Antimicrobial Susceptibility and Molecular Features of Colonizing Isolates of Ps |
| 36671975 | 10.1039/c4cc03011g | 10.3390/bios13010138 | CRISPR/Cas12a-Assisted Dual Visualized Detection of SARS-CoV-2 on Frozen Shrimps |
| 36672880 | 10.1111/pedi.12468 | 10.3390/genes14010139 | The Two-Faced Role of crAssphage Subfamilies in Obesity and Metabolic Syndrome:  |
| 36674462 | 10.21449/ijate.661803 | 10.3390/ijms24020934 | Multi-Omic Factors Associated with Frequency of Upper Respiratory Infections in  |
| 36675046 | 10.1002/bit.26890 | 10.3390/ijms24021536 | The Breadth of Bacteriophages Contributing to the Development of the Phage-Based |
| 36675109 | 10.1093/bioinformatics/8.3.275 | 10.3390/ijms24021594 | Comparative Evaluation of Reproducibility of Phage-Displayed Peptide Selections  |
| 36675201 | 10.1007/978-1-60327-164-6_9 | 10.3390/ijms24021686 | Antimicrobial and Virucidal Potential of Morpholinium-Based Ionic Liquids. |
| 36680055 | 10.1101/619999 | 10.3390/v15010014 | Microcalorimetry: A Novel Application to Measure In Vitro Phage Susceptibility o |
| 36680060 | 10.1016/S0021-9258(19)67936-6 | 10.3390/v15010017 | Phage K gp102 Drives Temperature-Sensitive Antibacterial Activity on USA300 MRSA |
| 36680213 | 10.1186/s12916-021-02103-4 | 10.3390/v15010174 | Development and Characterization of Phage Display-Derived Monoclonal Antibodies  |
| 36680214 | 10.1053/j.gastro.2011.06.057 | 10.3390/v15010173 | The Emerging Role of the Gut Virome in Health and Inflammatory Bowel Disease: Ch |
| 36680219 | 10.3389/fmicb.2020.00110 | 10.3390/v15010179 | Enterococcus faecium Bacteriophage vB_EfaH_163, a New Member of the Herellevirid |
| 36680256 | 10.3389/fmicb.2017.01754 | 10.3390/v15010216 | A Genome of Temperate Enterococcus Bacteriophage Placed in a Space of Pooled Vir |
| 36682626 | 10.1016/j.ajic.2007.10.006 | 10.1016/j.jhin.2023.01.004 | A methodology for using Lambda phages as a proxy for pathogen transmission in ho |
| 36683075 | 10.1016/j.coviro.2021.10.011 | 10.1007/s00705-022-05694-2 | Abolishment of morphology-based taxa and change to binomial species names: 2022  |
| 36685519 | 10.1080/19420862.2019.1616506 | 10.3389/fimmu.2022.1039969 | Bispecific killer cell engager with high affinity and specificity toward CD16a o |
| 36687584 | 10.3389/fcimb.2022.945000 | 10.3389/fmicb.2022.1032520 | Temperature-specific adaptations and genetic requirements in a biofilm formed by |
| 36688638 | 10.1099/mic.0.2006/000117-0 | 10.1128/spectrum.02631-22 | Clinical and Environmental Vibrio cholerae Non-O1, Non-O139 Strains from Austral |
| 36689552 | 10.1093/sysbio/syy060 | 10.1371/journal.pbio.3001972 | Phylogenomic analysis of Wolbachia genomes from the Darwin Tree of Life biodiver |
| 36690941 | 10.4236/aim.2013.32028 | 10.1186/s12866-023-02766-4 | Assessment of the influence of selected stress factors on the growth and surviva |
| 36696011 | 10.1093/bioinformatics/btp033 | 10.1007/s12033-023-00664-8 | Extract-Shaped Immune Repertoires as Source for Nanobody-Based Human IgE in Gras |
| 36700149 | 10.1038/s41589-022-01140-1 | 10.2147/IJN.S387160 | A Multivalent and Thermostable Nanobody Neutralizing SARS-CoV-2 Omicron (B.1.1.5 |
| 36700630 | 10.3390/v13102005 | 10.1128/spectrum.04030-22 | Efficacy in Galleria mellonella Larvae and Application Potential Assessment of a |
| 36709744 | 10.1021/acs.nanolett.0c03331 | 10.1016/j.ijheh.2023.114120 | Estimating the restraint of SARS-CoV-2 spread using a conventional medical air-c |
| 36717719 | 10.1006/jsbi.1996.0013 | 10.1038/s41564-022-01317-3 | L-form conversion in Gram-positive bacteria enables escape from phage infection. |
| 36719711 | 10.1515/labmed-2014-0004 | 10.1021/acssensors.2c01822 | Recombinant Reporter Phage rTUN1::nLuc Enables Rapid Detection and Real-Time Ant |
| 36726844 | 10.3201/eid1106.050167 | 10.1155/2023/5250040 | Recent Approaches for Downplaying Antibiotic Resistance: Molecular Mechanisms. |
| 36729226 | 10.3390/ijms12010001 | 10.1007/s00253-023-12395-6 | Production and applications of fluorobody from redox-engineered Escherichia coli |
| 36730457 | 10.1007/978-1-4939-7098-8_17 | 10.1371/journal.ppat.1011127 | Phage production is blocked in the adherent-invasive Escherichia coli LF82 upon  |
| 36731126 | 10.4161/bact.20092 | 10.1021/acssynbio.2c00615 | Tail-Engineered Phage P2 Enables Delivery of Antimicrobials into Multiple Gut Pa |
| 36747030 | 10.1073/pnas.90.15.7089 | 10.1038/s41598-023-29365-7 | Recombinant anti-HIV MAP30, a ribosome inactivating protein: against plant virus |
| 36747166 | 10.1093/nar/gkaa946 | 10.1186/s12915-022-01509-7 | A nontuberculous mycobacterium could solve the mystery of the lady from the Fran |
| 36748528 | 10.1371/journal.pone.0021323 | 10.1099/mgen.0.000902 | Genetic diversity of Staphylococcus aureus wall teichoic acid glycosyltransferas |
| 36750095 | 10.1016/j.jmb.2017.12.007 | 10.1016/j.cell.2022.12.041 | Bacteriophages inhibit and evade cGAS-like immune function in bacteria. |
| 36753420 | 10.1186/s12866-020-02007-y | 10.1016/j.celrep.2023.112048 | Genetic determinants of host tropism in Klebsiella phages. |
| 36755092 | 10.1101/2021.10.04.463034 | 10.1038/s41586-022-05647-4 | An E1-E2 fusion protein primes antiviral immune signalling in bacteria. |
| 36756618 | 10.1093/jac/dkx217 | 10.3389/fcimb.2023.1077995 | Characterization and comprehensive genome analysis of novel bacteriophage, vB_Kp |
| 36758519 | 10.32614/RJ-2017-066 | 10.1016/j.chom.2023.01.003 | Longitudinal comparison of the developing gut virome in infants and their mother |
| 36758766 | 10.1016/j.carbpol.2013.10.002 | 10.1016/j.ijbiomac.2023.123587 | Antibacterial and antiviral chitosan oligosaccharide modified cellulosic fibers  |
| 36761762 | 10.1038/cdd.2014.12 | 10.3389/fimmu.2023.1070492 | Human antibodies targeting ENPP1 as candidate therapeutics for cancers. |
| 36766686 | 10.1016/j.resmic.2022.103954 | 10.3390/cells12030344 | Accessing the In Vivo Efficiency of Clinically Isolated Phages against Uropathog |
| 36768143 | 10.1101/gr.361602 | 10.3390/ijms24031820 | Three Phages One Host: Isolation and Characterization of Pantoea agglomerans Pha |
| 36768328 | 10.1002/btm2.10302 | 10.3390/ijms24032007 | Targeting Agents in Biomaterial-Mediated Bone Regeneration. |
| 36768484 | 10.3791/50934 | 10.3390/ijms24032161 | Stabilization of Monomeric Tau Protein by All D-Enantiomeric Peptide Ligands as  |
| 36769020 | 10.3389/fmicb.2020.00327 | 10.3390/ijms24032695 | Bacteriophages and the Microbiome in Dermatology: The Role of the Phageome and a |
| 36769055 | 10.1016/j.envpol.2022.119603 | 10.3390/ijms24032733 | The Burden of Survivors: How Can Phage Infection Impact Non-Infected Bacteria? |
| 36775818 | 10.1186/ar3798 | 10.1038/s41392-022-01263-w | MiR146a-loaded engineered exosomes released from silk fibroin patch promote diab |
| 36779712 | 10.1016/j.femsle.2004.11.005 | 10.1128/spectrum.03099-22 | Identification of Potential Antimicrobial Targets of Pseudomonas aeruginosa Biof |
| 36779715 | 10.1073/pnas.2023202118 | 10.1128/mra.00004-23 | Complete Genome Sequence of the Lysogenic Pseudomonas Bacteriophage Fyn8. |
| 36779718 | 10.1111/j.1432-1033.1992.tb16740.x | 10.1128/mbio.02490-22 | Staphylococcus aureus Prophage-Encoded Protein Causes Abortive Infection and Pro |
| 36779782 | 10.1093/nar/gni059 | 10.1002/cpz1.656 | Recombineering: Genetic Engineering in Escherichia coli Using Homologous Recombi |
| 36780326 | 10.1021/acs.estlett.0c00437 | 10.1021/acsabm.2c00901 | Virus Inactivation Based on Optimal Surfactant Reservoir of Mesoporous Silica. |
| 36780432 | 10.1128/mBio.01360-14 | 10.1371/journal.pbio.3001922 | Four principles to establish a universal virus taxonomy. |
| 36781732 | 10.1038/nbt.1754 | 10.1007/978-1-0716-2996-3_16 | Genomic Epidemiological Analysis of Antimicrobial-Resistant Bacteria with Nanopo |
| 36790168 | 10.1016/j.xcrm.2020.100123 | 10.7554/eLife.81401 | Antibodies to repeat-containing antigens in Plasmodium falciparum are exposure-d |
| 36793881 | 10.1586/eri.13.12 | 10.1089/phage.2021.0016 | vHULK, a New Tool for Bacteriophage Host Prediction Based on Annotated Genomic F |
| 36794936 | 10.1371/journal.pone.0199432 | 10.1128/msystems.01189-22 | Transcriptomics-Driven Characterization of LUZ100, a T7-like Pseudomonas Phage w |
| 36795728 | 10.1093/nar/gkh152 | 10.1371/journal.pone.0281769 | Unusual prophages in Mycobacterium abscessus genomes and strain variations in ph |
| 36800087 | 10.1016/j.envint.2019.105452 | 10.1007/s11356-023-25824-w | Applicability of crAssphage as a performance indicator for viral reduction durin |
| 36800381 | 10.1242/jcs.01403 | 10.1371/journal.ppat.1010925 | Tripartite interactions between filamentous Pf4 bacteriophage, Pseudomonas aerug |
| 36802441 | 10.1128/mbio.02441-21 | 10.1073/pnas.2216430120 | Polyamines and linear DNA mediate bacterial threat assessment of bacteriophage i |
| 36805702 | 10.1128/mBio.00306-15 | 10.1038/s41589-023-01269-7 | Multicopy suppressor screens reveal convergent evolution of single-gene lysis pr |
| 36807264 | 10.1002/pro.3280 | 10.1038/s41467-023-36526-9 | The ϕPA3 phage nucleus is enclosed by a self-assembling 2D crystalline lattice. |
| 36808524 | 10.1074/jbc.M113.466433 | 10.1007/s10549-023-06866-7 | A specific anti-cyclin D1 intrabody represses breast cancer cell proliferation b |
| 36809931 | 10.1128/IAI.00205-19 | 10.1080/21505594.2023.2180228 | Identification of an immunodominant region on a group A Streptococcus T-antigen  |
| 36819063 | 10.3389/fmicb.2020.00377 | 10.3389/fmicb.2023.1027380 | Transcriptional analysis in bacteriophage Fc02 of Pseudomonas aeruginosa reveale |
| 36820898 | 10.1371/journal.pone.0178634 | 10.1007/s00253-023-12433-3 | Monoclonal antibody targeting a novel linear epitope on nucleoprotein confers pa |
| 36823020 | 10.1371/journal.pone.0061217 | 10.1080/19490976.2023.2177488 | Multiomic spatial analysis reveals a distinct mucosa-associated virome. |
| 36829156 | 10.1128/Spectrum.01023-21 | 10.1186/s12941-023-00567-1 | Isolation, characterization, therapeutic potency, and genomic analysis of a nove |
| 36830196 | 10.1111/j.1469-0691.2011.03570.x | 10.3390/antibiotics12020286 | Phage Therapy as an Alternative Treatment Modality for Resistant Staphylococcus  |
| 36833250 | 10.1038/ismej.2013.241 | 10.3390/genes14020323 | Diversity and Distribution Characteristics of Viruses from Soda Lakes. |
| 36834622 | 10.3390/toxins14100683 | 10.3390/ijms24043209 | Identify the Virus-like Models for COVID-19 as Bio-Threats: Combining Phage Disp |
| 36835084 | 10.4161/bact.27943 | 10.3390/ijms24043678 | Phenotypic Characterization and Comparative Genomic Analysis of Novel Salmonella |
| 36835304 | 10.1016/j.jaut.2022.102899 | 10.3390/ijms24043897 | The Human Virome and Its Crosslink with Glomerulonephritis and IgA Nephropathy. |
| 36835341 | 10.1002/rcm.7270 | 10.3390/ijms24043929 | Analysis of Bacteriophage Behavior of a Human RNA Virus, SARS-CoV-2, through the |
| 36838874 | 10.1111/pai.13141 | 10.3390/molecules28041880 | Identification and Structure of Epitopes on Cashew Allergens Ana o 2 and Ana o 3 |
| 36839335 | 10.1016/j.jpsychires.2016.07.019 | 10.3390/nu15040977 | The Human Gut Virome and Its Relationship with Nontransmissible Chronic Diseases |
| 36845148 | 10.1016/j.micpath.2017.06.020 | 10.3389/fimmu.2023.1112894 | Immunoproteomics and phage display in the context of leishmaniasis complexity. |
| 36845160 | 10.1021/acsomega.1c05213 | 10.3389/fimmu.2023.1065274 | Screening and epitope characterization of diagnostic nanobody against total and  |
| 36847856 | 10.1002/ame2.12227 | 10.1007/s00253-023-12439-x | Bacteriophage-based techniques for elucidating the function of zebrafish gut mic |
| 36851545 | 10.1371/journal.pone.0144802 | 10.3390/v15020333 | A Glimpse at the Anti-Phage Defenses Landscape in the Foodborne Pathogen Salmone |
| 36851601 | 10.1111/bph.15526 | 10.3390/v15020387 | Repetitive Exposure to Bacteriophage Cocktails against Pseudomonas aeruginosa or |
| 36851640 | 10.2217/fmb.12.76 | 10.3390/v15020427 | Development and Evaluation of Bacteriophage Cocktail to Eradicate Biofilms Forme |
| 36851674 | 10.2106/JBJS.K.01135 | 10.3390/v15020460 | Phage and Antibiotic Combinations Reduce Staphylococcus aureus in Static and Dyn |
| 36851708 | 10.1371/journal.pbio.3001424 | 10.3390/v15020495 | "French Phage Network" Annual Conference-Seventh Meeting Report. |
| 36851713 | 10.1016/j.jtcvs.2010.06.037 | 10.3390/v15020499 | Short-Term Outcomes of Phage-Antibiotic Combination Treatment in Adult Patients  |
| 36851734 | 10.32473/edis-fs269-2017 | 10.3390/v15020520 | Pseudomonas Phage ZCPS1 Endolysin as a Potential Therapeutic Agent. |
| 36851802 | 10.3390/v10020064 | 10.3390/v15020588 | Phage Therapy in Germany-Update 2023. |
| 36853925 | 10.1093/infdis/jiac394 | 10.1021/acs.est.2c08632 | Efficacy of Grignard Pure to Inactivate Airborne Phage MS2, a Common SARS-CoV-2  |
| 36856430 | 10.1073/pnas.2109750119 | 10.1128/aem.01545-22 | Viral Preservation with Protein-Supplemented Nebulizing Media in Aerosols. |
| 36856438 | 10.1016/j.jhin.2020.08.013 | 10.1128/aem.01744-22 | Laboratory Evaluation of a Quaternary Ammonium Compound-Based Antimicrobial Coat |
| 36866633 | 10.1093/bioinformatics/btr703 | 10.1002/bmb.21720 | A bacterial genome assembly and annotation laboratory using a virtual machine. |
| 36869086 | 10.1093/nar/gkw385 | 10.1038/s41598-023-30623-x | First pan-specific vNAR against human TGF-β as a potential therapeutic applicati |
| 36869335 | 10.1038/nmeth.2089 | 10.1186/s12896-023-00776-8 | A fully human connective tissue growth factor blocking monoclonal antibody ameli |
| 36869962 | 10.1128/AEM.02581-15 | 10.1007/s00203-023-03434-x | Novel recombinant endolysin ointment with broad antimicrobial activity against m |
| 36883860 | 10.1016/s0022-1759(03)00223-0 | 10.1128/jvi.00062-23 | Isolation of an Ecotropic Porcine Endogenous Retrovirus PERV-C from a Yucatan SL |
| 36897342 | 10.1128/jb.00275-16 | 10.1007/s00253-023-12452-0 | CYP broth: a tool for Yersinia pestis isolation in ancient culture collections a |
| 36899044 | 10.1007/978-1-4939-7447-4_22 | 10.1038/s41598-023-31173-y | Development of an inhibiting antibody against equine interleukin 5 to treat inse |
| 36899059 | 10.1038/s41587-020-0631-z | 10.1038/s41598-023-30690-0 | Inactivation and spike protein denaturation of novel coronavirus variants by Cux |
| 36902040 | 10.1016/j.jchromb.2019.121885 | 10.3390/ijms24054609 | Discovery and Optimization of Neutralizing SARS-CoV-2 Antibodies Using ALTHEA Go |
| 36902066 | 10.7717/peerj.12391 | 10.3390/ijms24054635 | Mycobacterium abscessus Infections in Cystic Fibrosis Individuals: A Review on T |
| 36903484 | 10.1186/s12859-019-3317-0 | 10.3390/molecules28052238 | Prediction of Phage Virion Proteins Using Machine Learning Methods. |
| 36913409 | 10.1136/jech.53.4.235 | 10.1371/journal.pntd.0011179 | Seasonal variation of diarrhoeal pathogens among Guinea-Bissauan children under  |
| 36914753 | 10.1038/s41571-019-0184-6 | 10.1007/s00259-023-06183-7 | Identification of a CEACAM5 targeted nanobody for positron emission tomography i |
| 36918067 | 10.1128/MRA.01535-18 | 10.1016/j.jhin.2023.03.004 | Establishment and application of test methodology demonstrating the functionalit |
| 36933045 | 10.1177/23800844221123751 | 10.1007/s00784-023-04937-z | Tracing ΦX174 bacteriophage spreading during aerosol-generating procedures in a  |
| 36935353 | 10.1128/spectrum.01393-21 | 10.1080/21645515.2023.2175519 | The applications of animal models in phage therapy: An update. |
| 36947007 | 10.1038/s41598-022-15768-5 | 10.1021/acsami.3c01400 | Durability and Surface Oxidation States of Antiviral Nano-Columnar Copper Thin F |
| 36949545 | 10.1093/jac/dkh197 | 10.1186/s12985-023-02012-3 | The persistence and stabilization of auxiliary genes in the human skin virome. |
| 36951916 | 10.1099/13500872-142-7-1833 | 10.1099/mgen.0.000959 | Global population structure, genomic diversity and carbohydrate fermentation cha |
| 36959476 | 10.3389/fmicb.2020.589640 | 10.1007/s11274-023-03584-6 | Biofilm control strategies in the light of biofilm-forming microorganisms. |
| 36963724 | 10.1038/s41598-020-63048-x | 10.1016/j.virusres.2023.199102 | Characterization and comparative genomic analysis of novel lytic bacteriophages  |
| 36964164 | 10.1017/dmp.2020.255 | 10.1038/s41598-023-32082-w | Evaluation of aerosols in a simulated orthodontic debanding procedure. |
| 36964198 | 10.1002/jcc.20084 | 10.1038/s41598-023-31568-x | Rabbit derived VL single-domains as promising scaffolds to generate antibody-dru |
| 36966151 | 10.1371/journal.pone.0122630 | 10.1038/s41467-023-37396-x | The genomic landscape of reference genomes of cultivated human gut bacteria. |
| 36969497 | 10.1038/nbt1126 | 10.1155/2023/7612566 | Development of a Novel Recombinant Full-Length IgY Monoclonal Antibody against H |
| 36973327 | 10.1084/jem.160.6.1767 | 10.1038/s41598-023-32111-8 | Dynamic changes in Shiga toxin (Stx) 1 transducing phage throughout the evolutio |
| 36973710 | 10.1101/gr.122705.111 | 10.1186/s12985-023-02013-2 | Comparison of gut viral communities in children under 5 years old and newborns. |
| 36975787 | 10.1038/s41591-021-01403-9 | 10.1128/aac.00037-23 | Therapeutic Potential of Intravenous Phage as Standalone Therapy for Recurrent D |
| 36978364 | 10.3390/antibiotics9110732 | 10.3390/antibiotics12030497 | Isolation and Characterization of a Novel Lytic Phage, vB_PseuP-SA22, and Its Ef |
| 36978460 | 10.1101/2020.04.24.060335 | 10.3390/antibiotics12030593 | Lytic Bacteriophage Is a Promising Adjunct to Common Antibiotics across Cystic F |
| 36979394 | 10.1038/s41423-021-00655-2 | 10.3390/biom13030459 | Novel scFv against Notch Ligand JAG1 Suitable for Development of Cell Therapies  |
| 36979401 | 10.1111/cbdd.12325 | 10.3390/biom13030466 | Development of a Novel Antibacterial Peptide, PAM-5, via Combination of Phage Di |
| 36979613 | 10.1007/s00604-022-05560-7 | 10.3390/bios13030401 | Dual-Mode Biosensor for Simultaneous and Rapid Detection of Live and Whole Salmo |
| 36982770 | 10.3390/antibiotics10060710 | 10.3390/ijms24065696 | Characterization and Comparative Genomic Analysis of Three Virulent E. coli Bact |
| 36983034 | 10.1038/s41598-017-18947-x | 10.3390/ijms24065961 | The Influence of Bacteriophages on the Metabolic Condition of Human Fibroblasts  |
| 36983085 | 10.1007/978-1-62703-245-2_22 | 10.3390/ijms24066011 | Generation and Next-Generation Sequencing-Based Characterization of a Large Huma |
| 36985593 | 10.3390/cancers14051325 | 10.3390/molecules28062621 | Phage Display-Derived Peptides and Antibodies for Bacterial Infectious Diseases  |
| 36991500 | 10.1016/j.fm.2012.02.003 | 10.1186/s40168-023-01496-z | Gut commensal Enterocloster species host inoviruses that are secreted in vitro a |
| 36992312 | 10.3389/fcimb.2022.1000721 | 10.3390/v15030602 | Administration of Bacteriophages via Nebulization during Mechanical Ventilation: |
| 36992345 | 10.3390/microorganisms7030081 | 10.3390/v15030637 | Twenty Years of Collaboration to Sort out Phage Mu Replication and Its Dependenc |
| 36992352 | 10.3390/v13030506 | 10.3390/v15030643 | Genomic Analysis of Two Novel Bacteriophages Infecting Acinetobacter beijerincki |
| 36992381 | 10.1093/femsle/fnv242 | 10.3390/v15030672 | Co-Delivery of the Human NY-ESO-1 Tumor-Associated Antigen and Alpha-GalactosylC |
| 36992387 | 10.1021/acsami.1c01643 | 10.3390/v15030679 | Characterization of Three Different Endolysins Effective against Gram-Negative B |
| 36992428 | 10.1371/journal.pone.0116465 | 10.3390/v15030719 | Impact Assessment of vB_KpnP_K1-ULIP33 Bacteriophage on the Human Gut Microbiota |
| 36992430 | 10.1016/j.trsl.2020.03.010 | 10.3390/v15030721 | The Future of Clinical Phage Therapy in the United Kingdom. |
| 36992511 | 10.1016/j.ijpharm.2018.09.024 | 10.3390/v15030803 | Design of Phage-Cocktail-Containing Hydrogel for the Treatment of Pseudomonas ae |
| 36994608 | 10.1128/IAI.01513-13 | 10.1080/19490976.2023.2194794 | Temperate bacteriophages infecting the mucin-degrading bacterium Ruminococcus gn |
| 36995238 | 10.1371/journal.pone.0009490 | 10.1128/spectrum.04340-22 | Enrichment Culture but Not Metagenomic Sequencing Identified a Highly Prevalent  |
| 36998407 | 10.1128/AAC.43.2.287 | 10.3389/fmicb.2023.1093668 | Characterization of a lytic Pseudomonas aeruginosa phage vB_PaeP_ASP23 and funct |
| 37004108 | 10.1146/annurev.immunol.16.1.225 | 10.1186/s13293-023-00501-2 | Effects of 5α-dihydrotestosterone on the modulation of monocyte/macrophage respo |
| 37004601 | 10.1128/MRA.00765-19 | 10.1007/s11262-023-01990-4 | Characterization of Phietavirus Henu 2 in the virome of individuals with acute g |
| 37019943 | 10.1038/nbt.3988 | 10.1038/s42003-023-04718-0 | New carbohydrate binding domains identified by phage display based functional me |
| 37022175 | 10.1093/nar/gkv332 | 10.1128/jb.00023-23 | All DACs in a Row: Domain Architectures of Bacterial and Archaeal Diadenylate Cy |
| 37022197 | 10.1006/abio.1993.1098 | 10.1128/spectrum.04384-22 | Resistance of Klebsiella pneumoniae to Phage hvKpP3 Due to High-Molecular Weight |
| 37026514 | 10.1042/BCJ20210071 | 10.3892/ijmm.2023.5244 | Overexpression of salusin‑α upregulates AdipoR2 and activates the PPARα/ApoA5/SR |
| 37030644 | 10.1016/j.apsb.2020.08.014 | 10.1016/j.pep.2023.106267 | Preparation and characterization of nanobodies targeting SARS-CoV-2 papain-like  |
| 37036343 | 10.1128/mBio.02527-21 | 10.1128/mbio.03452-22 | Environmental Stability of Enveloped Viruses Is Impacted by Initial Volume and E |
| 37036571 | 10.1016/j.virusres.2021.198348 | 10.1007/s12223-023-01046-y | Phage therapy of antibiotic-resistant strains of Klebsiella pneumoniae, opportun |
| 37037943 | 10.1101/gr.092759.109 | 10.1038/s41564-023-01345-7 | Expanding known viral diversity in the healthy infant gut. |
| 37039641 | 10.1128/mbio.02441-21 | 10.1128/mbio.00472-23 | Engineered Superinfective Pf Phage Prevents Dissemination of Pseudomonas aerugin |
| 37042412 | 10.1007/s00404-022-06817-5 | 10.1111/1751-7915.14261 | Fighting polymicrobial biofilms in bacterial vaginosis. |
| 37042671 | 10.1046/j.1365-2958.2000.02134.x | 10.1128/mbio.00182-23 | Human-Gut Phages Harbor Sporulation Genes. |
| 37047510 | 10.1007/s00128-021-03137-3 | 10.3390/ijms24076535 | Potential Use of a Combined Bacteriophage-Probiotic Sanitation System to Control |
| 37048151 | 10.1038/s41586-019-1730-1 | 10.3390/cells12071078 | Development of Cyclic Peptides Targeting the Epidermal Growth Factor Receptor in |
| 37049457 | 10.1128/JB.184.1.152-164.2002 | 10.3390/nu15071616 | Metagenomic Sequencing Identified Specific Bacteriophage Signature Discriminatin |
| 37052201 | 10.1080/0036552120161216587 | 10.1093/ecco-jcc/jjad061 | Community Types of the Human Gut Virome are Associated with Endoscopic Outcome i |
| 37053131 | 10.1186/s12941-021-00433-y | 10.1371/journal.pone.0283930 | Coliphages of the human urinary microbiota. |
| 37060711 | 10.1016/J.ULTSONCH.2022.106053 | 10.1016/j.ultsonch.2023.106400 | Inactivation of the enveloped virus phi6 with hydrodynamic cavitation. |
| 37063837 | 10.1038/s41586-019-0916-x | 10.3389/fimmu.2023.1144774 | LRPPRC facilitates tumor progression and immune evasion through upregulation of  |
| 37063855 | 10.1371/journal.pone.0054504 | 10.3389/fimmu.2023.1154380 | Alterations in the gut virome in patients with ankylosing spondylitis. |
| 37065190 | 10.1007/s11262-017-1445-z | 10.3389/fcimb.2023.1149848 | Statistical optimization of a podoviral anti-MRSA phage CCASU-L10 generated from |
| 37067377 | 10.1038/s41591-019-0440-4 | 10.1021/acs.molpharmaceut.3c00173 | Human Antibody VH Domains Targeting GPNMB and VCAM-1 as Candidate Therapeutics f |
| 37067443 | 10.3201/eid2608.200346 | 10.1128/spectrum.05149-22 | Targeted Single-Phage Isolation Reveals Phage-Dependent Heterogeneous Infection  |
| 37069161 | 10.1371/journal.pcbi.1009442 | 10.1038/s41467-023-37975-y | Altered human gut virome in patients undergoing antibiotics therapy for Helicoba |
| 37073274 | 10.4269/ajtmh.20-0755 | 10.7717/peerj.15202 | Enveloped and non-enveloped virus survival on microfiber towels. |
| 37074184 | 10.1093/nar/gkab301 | 10.1128/aem.00421-23 | Longitudinal Study of Lactococcus Phages in a Canadian Cheese Factory. |
| 37074450 | 10.1038/nm1167 | 10.1007/s00284-023-03294-0 | Identification of Heterophilic Epitopes of H1N1 Influenza Virus Hemagglutinin. |
| 37077532 | 10.1128/JB.01517-10 | 10.3389/fcimb.2023.1162617 | Targeted proteomics links virulence factor expression with clinical severity in  |
| 37079526 | 10.3390/ijms20061283 | 10.1371/journal.pone.0284708 | A novel anti-membrane CD30 single-chain variable fragment discovered from the hu |
| 37083687 | 10.1002/pro.3943 | 10.1371/journal.pbio.3002072 | Distribution and molecular evolution of the anti-CRISPR family AcrIF7. |
| 37094126 | 10.1016/j.molcel.2021.12.03 | 10.1073/pnas.2215098120 | Mechanistic insights into DNA binding and cleavage by a compact type I-F CRISPR- |
| 37094788 | 10.1111/j.1476-5381.2010.00872.x | 10.4269/ajtmh.22-0303 | Isolation and Characterization of Pseudomonas aeruginosa Phages with a Broad Hos |
| 37098917 | 10.1002/bab.1910 | 10.1128/spectrum.00920-23 | Targeted Killing of Staphylococcus aureus Using Specific Peptides Displayed on Y |
| 37098944 | 10.1128/AAC.01625-09 | 10.1128/aac.01519-22 | PlyKp104, a Novel Phage Lysin for the Treatment of Klebsiella pneumoniae, Pseudo |
| 37098979 | 10.1002/pmic.201800236 | 10.1128/jb.00466-22 | Regulatory Role of Anti-Sigma Factor RsbW in Clostridioides difficile Stress Res |
| 37101118 | 10.1080/10934529.2022.2036551 | 10.1186/s12866-023-02847-4 | Biocontrol of multi-drug resistant pathogenic bacteria in drainage water by loca |
| 37101261 | 10.1021/acsinfecdis.1c00108 | 10.1186/s12929-023-00919-1 | Therapeutic potential of bacteriophage endolysins for infections caused by Gram- |
| 37102658 | 10.1177/17534259211051069 | 10.1002/iid3.803 | Downregulation of ROR2 attenuates LPS-induced A549 cell injury through JNK and E |
| 37103716 | 10.1371/journal.pone.0111788 | 10.1007/s10096-023-04600-1 | Genome-wide association study of hemolytic uremic syndrome causing Shiga toxin-p |
| 37105971 | 10.1093/bioinformatics/btv372 | 10.1038/s41467-023-38098-0 | Automated design of protein-binding riboswitches for sensing human biomarkers in |
| 37107097 | 10.1038/s41522-021-00214-7 | 10.3390/antibiotics12040735 | A Novel Zinc (II) Porphyrin Is Synergistic with PEV2 Bacteriophage against Pseud |
| 37108047 | 10.1084/jem.185.7.1307 | 10.3390/ijms24086883 | The Utility of Peptide Ligand-Functionalized Liposomes for Subcutaneous Drug Del |
| 37108460 | 10.1371/journal.ppat.1011033 | 10.3390/ijms24087292 | Longitudinal Variations in Antibody Responses against SARS-CoV-2 Spike Epitopes  |
| 37112892 | 10.1007/s10068-018-0351-z | 10.3390/v15040912 | The Lytic Activity of Bacteriophage ZCSE9 against Salmonella enterica and Its Sy |
| 37113000 | 10.1016/j.virusres.2022.198997 | 10.3390/v15041020 | Current Clinical Landscape and Global Potential of Bacteriophage Therapy. |
| 37115804 | 10.1099/mgen.0.000670 | 10.1371/journal.ppat.1010650 | Genomic analysis unveils genome degradation events and gene flux in the emergenc |
| 37120837 | 10.1093/nar/gkw1154 | 10.1021/acsnano.3c01102 | Bioengineered Bacteriophage-Like Nanoparticles as RNAi Therapeutics to Enhance R |
| 37125933 | 10.1093/bioinformatics/btr039 | 10.1128/spectrum.04636-22 | Isolation and Characterization of Three Pseudomonas aeruginosa Viruses with Ther |
| 37125939 | 10.1128/AAC.02043-18 | 10.1128/spectrum.05050-22 | Exploiting Broad-Spectrum Chimeric Lysin to Cooperate with Mupirocin against Sta |
| 37129715 | 10.3389/fmicb.2020.01245 | 10.1007/s00203-023-03550-8 | The metastable associations of bacteriophages and Erwinia amylovora. |
| 37137974 | 10.1101/gr.092759.109 | 10.1038/s42003-023-04877-0 | Leaky barriers to gene sharing between locally co-existing coagulase-negative St |
| 37145987 | 10.1007/BF02540223 | 10.1371/journal.pone.0285274 | The ecological consequences and evolution of retron-mediated suicide as a way to |
| 37153161 | 10.1513/AnnalsATS.201408-395OC | 10.3389/fcimb.2023.1151594 | Genomic features, antimicrobial susceptibility, and epidemiological insights int |
| 37154766 | 10.3390/v13102049 | 10.1128/aac.00449-23 | Case Commentary: Unlocking the Potential of Bacteriophage to Prevent Recurrent U |
| 37154774 | 10.1016/j.jgg.2019.07.006 | 10.1128/spectrum.05015-22 | Identification of Toxic Proteins Encoded by Mycobacteriophage TM4 Using a Next-G |
| 37156803 | 10.1089/mdr.2016.0248 | 10.1038/s41598-023-33822-8 | Antibacterial activity of vB_AbaM_PhT2 phage hydrophobic amino acid fusion endol |
| 37160116 | 10.1016/j.mib.2014.12.007 | 10.1016/j.cell.2023.04.015 | Bacterial NLR-related proteins protect against phage. |
| 37160359 | 10.1016/j.resmic.2018.05.001 | 10.1136/bmjresp-2022-001360 | Single-arm, open-labelled, safety and tolerability of intrabronchial and nebulis |
| 37163048 | 10.3791/3916 | 10.1101/2023.04.26.538445 | High prevalence of lipopolysaccharide mutants and R2-Pyocin susceptible variants |
| 37164013 | 10.7554/eLife.65088 | 10.1016/j.immuni.2023.04.003 | Phage display sequencing reveals that genetic, environmental, and intrinsic fact |
| 37165188 | 10.1093/nar/gkab1038 | 10.1038/s41586-023-05989-7 | Profiling the human intestinal environment under physiological conditions. |
| 37166313 | 10.1186/s12864-015-1848-y | 10.1128/mra.00139-23 | Complete Genome Sequencing of the Novel Pseudomonas aeruginosa Phage UF_RH1. |
| 37169795 | 10.1093/nar/gkac1062 | 10.1038/s41467-023-37915-w | Cryo-electron microscopy of the f1 filamentous phage reveals insights into viral |
| 37175929 | 10.1016/0042-6822(76)90024-6 | 10.3390/ijms24098222 | Potential Applications of Thermophilic Bacteriophages in One Health. |
| 37180155 | 10.1136/jitc-2020-000911 | 10.3389/fimmu.2023.1089395 | Highly reliable GIGA-sized synthetic human therapeutic antibody library construc |
| 37184385 | 10.1128/jb.134.3.1141-1156.1978 | 10.1128/aem.00036-23 | Regulation and Functionality of a Holin/Endolysin Pair Involved in Killing of Ga |
| 37188814 | 10.1371/journal.pcbi.1009442 | 10.1038/s41564-023-01370-6 | Centenarians have a diverse gut virome with the potential to modulate metabolism |
| 37189332 | 10.1128/mBio.00978-16 | 10.3390/biom13040584 | Bacteriophages of the Order Crassvirales: What Do We Currently Know about This K |
| 37195168 | 10.1038/protex.2010.212 | 10.1128/spectrum.04430-22 | Synergistic Interactions among Burkholderia cepacia Complex-Targeting Phages Rev |
| 37198182 | 10.1016/S1044-0305(99)00085-9 | 10.1038/s41467-023-38075-7 | High-affinity peptides developed against calprotectin and their application as s |
| 37199616 | 10.1111/1469-0691.12651 | 10.1128/spectrum.04918-22 | Optimization of Phage-Antibiotic Combinations against Staphylococcus aureus Biof |
| 37200291 | 10.1186/s13073-016-0294-z | 10.1371/journal.pone.0285824 | Phage therapy and the public: Increasing awareness essential to widespread use. |
| 37201587 | 10.1101/2020.09.03.282103 | 10.1016/j.jbc.2023.104831 | Identification of SARS-CoV-2 PLpro and 3CLpro human proteome substrates using su |
| 37208714 | 10.1038/s41564-019-0416-7 | 10.1186/s40168-023-01541-x | Chromosome folding and prophage activation reveal specific genomic architecture  |
| 37221194 | 10.1038/nmeth.2019 | 10.1038/s41598-023-35364-5 | Bacteriophage-loaded functional nanofibers for treatment of P. aeruginosa and S. |
| 37221274 | 10.1093/bioinformatics/btp595 | 10.1038/s41598-023-34730-7 | Respiratory eukaryotic virome expansion and bacteriophage deficiency characteriz |
| 37221517 | 10.1016/j.micpath.2021.105135 | 10.1186/s12866-023-02881-2 | Synergistic action of phages and lytic proteins with antibiotics: a combination  |
| 37222232 | 10.1007/s40259-020-00412-3 | 10.1080/19420862.2023.2213793 | Evolution of phage display libraries for therapeutic antibody discovery. |
| 37224425 | 10.1016/j.cell.2010.01.029 | 10.1021/acs.biochem.3c00096 | Elucidation of Short Linear Motif-Based Interactions of the FERM Domains of Ezri |
| 37226433 | 10.3389/fmicb.2015.01242 | 10.1080/15476286.2023.2216065 | Impact of phage predation on P. aeruginosa adhered to human airway epithelium: m |
| 37226834 | 10.1186/1471-2180-11-38 | 10.1099/mic.0.001334 | Removal of AMR plasmids using a mobile, broad host-range CRISPR-Cas9 delivery to |
| 37237003 | 10.1186/1471-2105-11-119 | 10.1038/s41598-023-35823-z | Occurrence and genetic diversity of prophage sequences identified in the genomes |
| 37239505 | 10.1016/j.atmosenv.2023.119598 | 10.3390/ijerph20105776 | Ozone Efficacy for the Disinfection of Ambulances Used to Transport Patients dur |
| 37239874 | 10.1016/0003-2697(88)90134-0 | 10.3390/ijms24108523 | Characterization and Engineering Studies of a New Endolysin from the Propionibac |
| 37243121 | 10.1038/jid.2013.521 | 10.3390/v15051034 | Construction of a Hantaan Virus Phage Antibody Library and Screening for Potenti |
| 37243129 | 10.1074/jbc.270.24.14389 | 10.3390/v15051042 | Characterization of a Bacteriophage GEC_vB_Bfr_UZM3 Active against Bacteroides f |
| 37243293 | 10.1038/s41467-021-22814-9 | 10.3390/v15051210 | Successful Bacteriophage-Antibiotic Combination Therapy against Multidrug-Resist |
| 37243294 | 10.3390/v13071268 | 10.3390/v15051208 | Virulent Phage vB_EfaS_WH1 Removes Enterococcus faecalis Biofilm and Inhibits It |
| 37243574 | 10.1002/j.1460-2075.1995.tb00142.x | 10.1080/19420862.2023.2217964 | Generation and in vivo characterization of a novel high-affinity human antibody  |
| 37247008 | 10.1099/mic.0.067116-0 | 10.1007/s00438-023-02037-x | Characterization of a novel phage vB_Pae_HB2107-3I that infects Pseudomonas aeru |
| 37247084 | 10.3390/v13030506 | 10.1007/s10123-023-00381-x | Characterization and synergy studies of Caudoviricete Escherichia phage FS2B inf |
| 37249420 | 10.1093/nar/gkn656 | 10.1128/mra.00206-23 | Complete Genome Sequence of Pseudomonas aeruginosa Phage UF_RH6, Isolated from H |
| 37250708 | 10.1016/j.addr.2018.07.009 | 10.7717/peerj.15078 | Determination of the affinity constants for phage display albumin-binding peptid |
| 37251411 | 10.1093/bioinformatics/btz022 | 10.3389/fimmu.2023.1170357 | Serum albumin binding knob domains engineered within a VH framework III bispecif |
| 37253769 | 10.1038/mt.2009.128 | 10.1038/s41467-023-38364-1 | Design of bacteriophage T4-based artificial viral vectors for human genome remod |
| 37255423 | 10.1038/nprot.2008.73 | 10.1128/aem.00520-23 | Characterization of a Filamentous Phage, Vaf1, from Vibrio alginolyticus AP-1. |
| 37260386 | 10.1016/j.jmb.2013.06.040 | 10.1128/jb.00029-23 | F-Type Pyocins Are Diverse Noncontractile Phage Tail-Like Weapons for Killing Ps |
| 37261715 | 10.1093/ve/vev017 | 10.1007/s12275-023-00052-6 | Searching for a Reliable Viral Indicator of Faecal Pollution in Aquatic Environm |
| 37264114 | 10.1093/nar/gkab301 | 10.1038/s41598-023-36034-2 | Combination of genetically diverse Pseudomonas phages enhances the cocktail effi |
| 37267422 | 10.1186/s40168-020-00867-0 | 10.1371/journal.ppat.1011424 | Targeted IS-element sequencing uncovers transposition dynamics during selective  |
| 37273201 | 10.1073/pnas.061038398 | 10.1128/msphere.00044-23 | Therapeutic potential of Bacillus phage lysin PlyB in ocular infections. |
| 37274310 | 10.1039/D0MO00027B | 10.3389/fcimb.2023.1200478 | Conceptual model to inform Legionella-amoebae control, including the roles of ex |
| 37274318 | 10.1016/j.foodcont.2019.106830 | 10.3389/fcimb.2023.1178248 | Complete genome analysis of Tequatrovirus ufvareg1, a Tequatrovirus species inhi |
| 37275366 | 10.1007/978-1-60327-164-6_7 | 10.3389/fmed.2023.1199657 | Case report: Analysis of phage therapy failure in a patient with a Pseudomonas a |
| 37280108 | 10.1046/j.1469-7580.2002.00065.x | 10.1093/stmcls/sxad045 | Glioblastoma Stem Cell Targeting Peptide Isolated Through Phage Display Binds Ca |
| 37288661 | 10.1172/JCI163669 | 10.1172/jci.insight.169515 | Autoantigen profiling reveals a shared post-COVID signature in fully recovered a |
| 37288872 | 10.1016/s0076-6879(00)26071-0 | 10.1080/19420862.2023.2220839 | Generation of a novel fully human non-superagonistic anti-CD28 antibody with eff |
| 37293203 | 10.1111/JOIM.12233 | 10.3389/fcimb.2023.1169135 | Isolation and in vitro characterization of novel S. epidermidis phages for thera |
| 37294811 | 10.1111/mmi.14229 | 10.1371/journal.pone.0284022 | Distinctive microbial community and genome structure in coastal seawater from a  |
| 37296574 | 10.3389/fimmu.2022.864868 | 10.3390/cells12111453 | Generation of Chimeric Antigen Receptors against Tetraspanin 7. |
| 37298067 | 10.1093/nar/gkz935 | 10.3390/ijms24119116 | Characterization and Diversity of Klebsiella pneumoniae Prophages. |
| 37298457 | 10.1093/molbev/msab120 | 10.3390/ijms24119506 | Isolation, Characterization, and Comparative Genomic Analysis of Bacteriophage E |
| 37304279 | 10.1016/j.sleep.2022.02.003 | 10.3389/fimmu.2023.1133358 | Sex-dependent differences in behavioral and immunological responses to antibioti |
| 37305418 | 10.1099/vir.0.026328-0 | 10.3389/fcimb.2023.1174510 | Interplays of mutations in waaA, cmk, and ail contribute to phage resistance in  |
| 37305419 | 10.1074/jbc.M804555200 | 10.3389/fcimb.2023.1183681 | Alkyl-quinolone-dependent quorum sensing controls prophage-mediated autolysis in |
| 37308590 | 10.1101/854182 | 10.1038/s41564-023-01406-x | Phage diversity in cell-free DNA identifies bacterial pathogens in human sepsis  |
| 37308748 | 10.1007/978-1-4939-8682-8_4 | 10.1038/s41598-023-36749-2 | Potential of bacteriophage therapy in managing Staphylococcus aureus infections  |
| 37310294 | 10.1128/mra.01221-21 | 10.1128/jvi.00667-23 | Characterization of the Attachment of Three New Coliphages onto the Ferrichrome  |
| 37318278 | 10.1016/0042-6822(70)90218-7 | 10.1021/acssynbio.3c00135 | Genetic Engineering of Bacteriophage K1F with Human Epidermal Growth Factor to E |
| 37323567 | 10.1038/nature11003 | 10.1016/j.crmeth.2023.100475 | Sequence enrichment profiles enable target-agnostic antibody generation for a br |
| 37330608 | 10.1101/gr.2289704 | 10.1038/s41598-023-37065-5 | Characterization of bacteriophage vB_KleM_KB2 possessing high control ability to |
| 37332116 | 10.1002/imt2.12 | 10.1080/19490976.2023.2221778 | L-Arabinose inhibits Shiga toxin type 2-converting bacteriophage induction in Es |
| 37338211 | 10.18637/jss.v067.i01 | 10.1128/msphere.00132-23 | Longitudinal and quantitative fecal shedding dynamics of SARS-CoV-2, pepper mild |
| 37338346 | 10.3390/molecules21091194 | 10.1128/aem.00581-23 | Design, Screening, and Characterization of Engineered Phage Endolysins with Extr |
| 37338375 | 10.1128/AEM.70.6.3417-3424.2004 | 10.1128/spectrum.00340-23 | Phage-Antibiotic Cocktail Rescues Daptomycin and Phage Susceptibility against Da |
| 37338376 | 10.18637/jss.v069.i01 | 10.1128/spectrum.04812-22 | Phages against Noncapsulated Klebsiella pneumoniae: Broader Host range, Slower R |
| 37338387 | 10.1016/B978-0-12-394621-8.00017-0 | 10.1128/mra.00396-23 | Complete Genome Sequencing of a Novel Pseudomonas aeruginosa Phage, UF_RH5. |
| 37340022 | 10.1186/1471-2105-7-439 | 10.1038/s41598-023-37176-z | Characterization of two novel lytic bacteriophages having lysis potential agains |
| 37340046 | 10.1111/imr.12565 | 10.1038/s41564-023-01422-x | Bacteriophage DNA in blood provides species-level insight into bacterial infecti |
| 37344099 | 10.1038/nri1498 | 10.1136/jitc-2023-007068 | Discovery of a novel dual-targeting D-peptide to block CD24/Siglec-10 and PD-1/P |
| 37347160 | 10.1007/978-1-61779-974-7_8 | 10.1128/spectrum.03607-22 | Development and Application of a Nanobody-Based Competitive ELISA for Detecting  |
| 37347328 | 10.3390/microorganisms9071527 | 10.1007/s11356-023-28081-z | Isolation and characterization of novel lytic bacteriophages that infect multi d |
| 37349979 | 10.1186/s13073-016-0271-6 | 10.1080/19490976.2023.2226925 | Alterations in the gut virome are associated with type 2 diabetes and diabetic n |
| 37358420 | 10.1371/journal.pone.0009321 | 10.1128/spectrum.00937-23 | Bacterial Swarm-Mediated Phage Transportation Disrupts a Biofilm Inherently Prot |
| 37358448 | 10.1086/595738 | 10.1128/spectrum.00600-23 | Gp05, a Prophage-Encoded Virulence Factor, Contributes to Persistent Methicillin |
| 37364635 | 10.1128/JCM.01547-21 | 10.1016/j.cmi.2023.06.026 | The problem of Mycobacterium abscessus complex: multi-drug resistance, bacteriop |
| 37366636 | 10.1093/gbe/evx243 | 10.1128/msphere.00128-23 | Prophage identification and molecular analysis in the genomes of Pseudomonas aer |
| 37367005 | 10.1021/acssensors.7b00069 | 10.3390/bios13060640 | Antibody Phage Display Technology for Sensor-Based Virus Detection: Current Stat |
| 37369702 | 10.1093/jac/dkr198 | 10.1038/s41467-023-39370-z | Personalized aerosolised bacteriophage treatment of a chronic lung infection due |
| 37369735 | 10.1038/s41467-023-39028-w | 10.1038/s41575-023-00810-2 | Phage therapy alleviates NAFLD in mice. |
| 37373012 | 10.1002/prot.21949 | 10.3390/ijms24129865 | Isolation and Characterization of scFv Antibody against Internal Ribosomal Entry |
| 37373494 | 10.1016/j.carres.2019.107857 | 10.3390/ijms241210348 | StackTHPred: Identifying Tumor-Homing Peptides through GBDT-Based Feature Select |
| 37374958 | 10.3390/ijms221910350 | 10.3390/microorganisms11061456 | Identification, Characterization, and Genome Analysis of Two Novel Temperate Pse |
| 37376552 | 10.1016/j.celrep.2020.108666 | 10.3390/v15061252 | Neutralizing and Enhancing Epitopes of the SARS-CoV-2 Receptor-Binding Domain (R |
| 37376571 | 10.1016/j.lwt.2019.108316 | 10.3390/v15061271 | Bacteriophage Delivery Systems for Food Applications: Opportunities and Perspect |
| 37376592 | 10.1128/JVI.00212-17 | 10.3390/v15061293 | Metavirome Profiling and Dynamics of the DNA Viral Community in Seawater in Chuu |
| 37377167 | 10.3390/antibiotics11060712 | 10.1002/jcla.24932 | Bacteriophages: The promising therapeutic approach for enhancing ciprofloxacin e |
| 37382405 | 10.1101/2022.07.03.498593 | 10.1002/advs.202302159 | Long-Read Sequencing Reveals Extensive DNA Methylations in Human Gut Phagenome C |
| 37388728 | 10.1002/cmdc.202100135 | 10.3389/fimmu.2023.1200652 | Rapid nanobody-based imaging of mesothelin expressing malignancies compatible wi |
| 37389722 | 10.1136/jitc-2020-000905 | 10.1007/s12539-023-00575-x | CD47Binder: Identify CD47 Binding Peptides by Combining Next-Generation Phage Di |
| 37392288 | 10.1039/d0en00962h | 10.1007/s11033-023-08557-4 | Bacteriophage genome engineering for phage therapy to combat bacterial antimicro |
| 37397737 | 10.1093/clinchem/hvac067 | 10.3389/fpubh.2023.1177069 | Metagenomic-based pathogen surveillance for children with severe pneumonia in pe |
| 37398644 | 10.1080/19420862.2021.1883239 | 10.3389/fimmu.2023.1127849 | Human-murine chimeric autoantibodies with high affinity and specificity for syst |
| 37402176 | 10.1016/j.cell.2022.07.003 | 10.1099/mgen.0.001053 | CRISPR dynamics during the interaction between bacteria and phage in the first y |
| 37404143 | 10.1128/spectrum.02423-21 | 10.1128/spectrum.01277-23 | An Endogenous Staphylococcus aureus CRISPR-Cas System Limits Phage Proliferation |
| 37404162 | 10.1016/j.micpath.2017.09.046 | 10.1128/iai.00065-23 | Class-Driven Synergy and Antagonism between a Pseudomonas Phage and Antibiotics. |
| 37404190 | 10.1093/nar/18.20.6097 | 10.1128/aem.00177-23 | Horizontal Gene Transfer and CRISPR Targeting Drive Phage-Bacterial Host Interac |
| 37405643 | 10.1007/978-3-662-04605-0_2 | 10.1007/978-1-0716-3279-6_5 | Identification of New Antibodies Targeting Tumor Cell Surface Antigens by Phage  |
| 37406030 | 10.1511/2022.110.3.162 | 10.1371/journal.pone.0283914 | Horizontal transfer of probable chicken-pathogenicity chromosomal islands betwee |
| 37407800 | 10.1016/j.bioflm.2019.100010 | 10.1007/s10096-023-04638-1 | A systematic review of the use of bacteriophages for in vitro biofilm control. |
| 37409241 | 10.1111/bph.15526 | 10.2147/IDR.S413900 | Refractory Pseudomonas aeruginosa Bronchopulmonary Infection After Lung Transpla |
| 37409956 | 10.1093/nar/gkw387 | 10.1128/spectrum.01309-23 | Urinary Plasmids Reduce Permissivity to Coliphage Infection. |
| 37418300 | 10.1128/mBio.01470-20 | 10.1099/mic.0.001352 | Decolonizing drug-resistant E. coli with phage and probiotics: breaking the freq |
| 37418366 | 10.1016/j.cub.2021.06.021 | 10.1371/journal.pone.0280070 | Bacterial cytological profiling reveals interactions between jumbo phage φKZ inf |
| 37422479 | 10.1128/JB.01546-07 | 10.1038/s41467-023-39756-z | High-resolution cryo-EM structure of the Pseudomonas bacteriophage E217. |
| 37422898 | 10.3390/antibiotics11091175 | 10.1007/s11262-023-02016-9 | Isolation and characterization of a novel lytic bacteriophage vB_Efm_LG62 infect |
| 37427929 | 10.1111/j.1365-2958.1993.tb01628.x | 10.1128/mbio.00798-23 | Methylome-dependent transformation of emm1 group A streptococci. |
| 37428387 | 10.1016/j.carres.2007.12.012 | 10.1007/s12010-023-04639-y | Role of Virus on Oral Biofilm: Inducer or Eradicator? |
| 37428714 | 10.1080/21505594.2017.1279374 | 10.1371/journal.pone.0283583 | Comparative genomics and virulome analysis reveal unique features associated wit |
| 37429841 | 10.1371/journal.pone.0163962 | 10.1038/s41467-023-39892-6 | Roving methyltransferases generate a mosaic epigenetic landscape and influence e |
| 37443756 | 10.1128/spectrum.00820-22 | 10.3390/cells12131720 | Phage Interactions with the Nervous System in Health and Disease. |
| 37445758 | 10.1016/j.ejmech.2020.112777 | 10.3390/ijms241310580 | Phage Targeting Neonatal Meningitis E. coli K1 In Vitro in the Intestinal Microb |
| 37448101 | 10.1101/gr.5969107 | 10.1080/19490976.2023.2234653 | Viral metagenomics of the gut virome of diarrheal children with Rotavirus A infe |
| 37450468 | 10.1111/j.1472-765X.2012.03221.x | 10.1371/journal.pone.0288454 | Applicability of F-specific bacteriophage subgroups, PMMoV and crAssphage as ind |
| 37458918 | 10.3390/v13030506 | 10.1007/s11262-023-02021-y | Jojan: a novel virus that lyses Stenotrophomonas maltophilia from dog. |
| 37464199 | 10.1038/nprot.2014.039 | 10.1007/s10517-023-05839-6 | The Search for Single-Domain Antibodies Interacting with the Receptor-Binding Do |
| 37464758 | 10.6084/m9.figshare.c.6723841 | 10.1098/rspb.2023.0622 | Ancient Yersinia pestis genomes lack the virulence-associated YpfΦ prophage pres |
| 37468551 | 10.1093/nar/gkw419 | 10.1038/s41598-023-38873-5 | Viruses participate in the organomineralization of travertines. |
| 37468662 | 10.1016/j.jcv.2016.08.298 | 10.1007/s10096-023-04642-5 | Epidemiology of gastrointestinal infections: lessons learned from syndromic test |
| 37468842 | 10.1093/sysbio/syq010 | 10.1186/s12864-023-09511-1 | Genomic analysis of Enterococcus faecium strain RAOG174 associated with acute ch |
| 37474516 | 10.1007/978-1-4939-9173-0_1 | 10.1038/s41467-023-39612-0 | Enhancing bacteriophage therapeutics through in situ production and release of h |
| 37474554 | 10.1128/JCM.01098-10 | 10.1038/s41467-023-39863-x | Engineered reporter phages for detection of Escherichia coli, Enterococcus, and  |
| 37483601 | 10.1016/j.ymgmr.2021.100837 | 10.3389/fimmu.2023.1142634 | Primary oxidative phosphorylation defects lead to perturbations in the human B c |
| 37490161 | 10.1016/B978-0-12-394438-2.00007-4 | 10.1007/s10930-023-10139-z | Bacteriophage Endolysin: A Powerful Weapon to Control Bacterial Biofilms. |
| 37491224 | 10.1038/srep11757 | 10.1186/s12929-023-00950-2 | A structure and knowledge-based combinatorial approach to engineering universal  |
| 37491415 | 10.1089/phage.2021.0007 | 10.1186/s40168-023-01607-w | Phages are unrecognized players in the ecology of the oral pathogen Porphyromona |
| 37495819 | 10.1007/s40259-013-0081-y | 10.1186/s13568-023-01582-3 | Isolation of a bacteriophage targeting Pseudomonas aeruginosa and exhibits a pro |
| 37497217 | 10.3389/fimmu.2022.867189 | 10.3389/fimmu.2023.1211295 | Extended cleavage specificities of human granzymes A and K, two closely related  |
| 37503841 | 10.1101/094672 | 10.1093/nar/gkad622 | A novel Queuovirinae lineage of Pseudomonas aeruginosa phages encode dPreQ0 DNA  |
| 37508185 | 10.1093/jacamr/dlac046 | 10.3390/antibiotics12071089 | Bacteriophage-Antibiotic Combination Therapy against Pseudomonas aeruginosa. |
| 37515114 | 10.3390/microorganisms8040480 | 10.3390/v15071427 | Transcriptional Landscapes of Herelleviridae Bacteriophages and Staphylococcus a |
| 37515203 | 10.1016/j.mib.2007.05.018 | 10.3390/v15071517 | Structure and Function of Hoc-A Novel Environment Sensing Device Encoded by T4 a |
| 37515541 | 10.1101/2023.01.23.22283996 | 10.1177/23247096231188243 | Bacteriophage Therapy for Pan-Drug-Resistant Pseudomonas aeruginosa in Two Perso |
| 37523325 | 10.1021/mp4001734 | 10.1021/acs.jcim.3c00752 | Computational Peptide Design Cotargeting Glucagon and Glucagon-like Peptide-1 Re |
| 37528343 | 10.1093/bioinformatics/btv033 | 10.1186/s12866-023-02949-z | Common antibiotics, azithromycin and amoxicillin, affect gut metagenomics within |
| 37532140 | 10.1007/s00705-023-05797-4 | 10.1016/j.virusres.2023.199184 | Characterization and genomic analysis of a broad-spectrum lytic phage HZ2201 and |
| 37535697 | 10.1016/j.micpath.2023.106130 | 10.1371/journal.pone.0289609 | Defeating a superbug: A breakthrough in vaccine design against multidrug-resista |
| 37543585 | 10.1080/03079457.2018.1475724 | 10.1186/s12866-023-02963-1 | Bacteriophage cocktail application for Campylobacter mitigation - from in vitro  |
| 37545056 | 10.1039/D2CC01677J | 10.1021/acs.analchem.3c02284 | Standardizing In Vitro β-Lactam Antibiotic Allergy Testing with Synthetic IgE. |
| 37545854 | 10.1016/S2213-2600(15)00063-6 | 10.3389/fcimb.2023.1173894 | Isolation and characterization of a novel mycobacteriophage Kashi-VT1 infecting  |
| 37550073 | 10.1083/jcb.200105003 | 10.1212/NXI.0000000000200145 | Utility of Protein Microarrays for Detection of Classified and Novel Antibodies  |
| 37550759 | 10.1016/j.cell.2019.09.015 | 10.1186/s12985-023-02138-4 | Phage tailspike modularity and horizontal gene transfer reveals specificity towa |
| 37553527 | 10.1128/mSphere.00454-19 | 10.1111/cns.14398 | Abnormalities in Clostridioides and related metabolites before ACTH treatment ma |
| 37558752 | 10.1093/nar/gky328 | 10.1038/s42003-023-05188-0 | Molecular reshaping of phage-displayed Interleukin-2 at beta chain receptor inte |
| 37561410 | 10.1080/19420862.2021.2002236 | 10.1093/protein/gzad008 | The variable conversion of neutralizing anti-SARS-CoV-2 single-chain antibodies  |
| 37566076 | 10.1016/S0022-2836(03)00185-2 | 10.3390/cells12151997 | New Phage-Derived Antibacterial Enzyme PolaR Targeting Rothia spp. |
| 37567926 | 10.1093/nar/25.5.955 | 10.1038/s41598-023-40228-z | Comparative analysis of effectiveness for phage cocktail development against mul |
| 37569397 | 10.3390/ijms22179518 | 10.3390/ijms241512018 | Tiger Nut Milk's Antiviral Properties against Enveloped and Non-Enveloped Viruse |
| 37569404 | 10.1371/journal.pone.0212819 | 10.3390/ijms241512028 | Biocompatible Chitosan Films Containing Acetic Acid Manifested Potent Antiviral  |
| 37574509 | 10.1016/S0140-6736(21)02724-0 | 10.1007/s00705-023-05845-z | Isolation and characterization of three novel Acinetobacter baumannii phages fro |
| 37575224 | 10.1016/j.cell.2023.02.029 | 10.3389/fimmu.2023.1224341 | The arms race between bacteria CBASS and bacteriophages. |
| 37577374 | 10.1016/j.chom.2020.08.005 | 10.3389/fcimb.2023.1241058 | The gut virome and the relevance of temperate phages in human health. |
| 37577460 | 10.1021/ci200227u | 10.1101/2023.08.01.551527 | Chaperone-assisted cryo-EM structure of P. aeruginosa PhuR reveals molecular bas |
| 37579172 | 10.1172/jci.insight.16986 | 10.1073/pnas.2220269120 | Ceramide as an endothelial cell surface receptor and a lung-specific lipid vascu |
| 37584323 | 10.1038/ni.2888 | 10.1042/BST20221395 | SMC-based immunity against extrachromosomal DNA elements. |
| 37587248 | 10.1186/s12864-020-6527-y | 10.1007/s11274-023-03722-0 | Population genomics of Lacticaseibacillus paracasei: pan-genome, integrated prop |
| 37594262 | 10.1371/journal.pone.0100448 | 10.1128/msystems.00646-23 | Engineered phage with cell-penetrating peptides for intracellular bacterial infe |
| 37594274 | 10.1007/978-1-4939-0554-6_12 | 10.1128/iai.00026-23 | Vibrio cholerae phage ICP3 requires O1 antigen for infection. |
| 37594644 | 10.1007/s00216-021-03847-x | 10.1007/s00604-023-05924-7 | A magnetic nanoparticle-based microfluidic device fabricated using a 3D-printed  |
| 37603558 | 10.1038/s41467-020-16366-7 | 10.1371/journal.ppat.1011600 | Bacteriophages targeting protective commensals impair resistance against Salmone |
| 37604733 | 10.1016/j.pan.2023.05.013 | 10.1016/j.pan.2023.08.004 | Substrate specificity of human chymotrypsin-like protease (CTRL) characterized b |
| 37604859 | 10.1016/j.toxicon.2016.04.032 | 10.1038/s41598-023-40630-7 | Subtractive panning for the isolation of monoclonal PEPITEM peptide antibody by  |
| 37608098 | 10.1038/s41467-021-25576-6 | 10.1007/978-1-0716-3358-8_1 | Digital PCR: A Partitioning-Based Application for Detection and Surveillance of  |
| 37608144 | 10.1016/S1473-3099(18)30482-1 | 10.1007/s10096-023-04649-y | A novel lytic phage exhibiting a remarkable in vivo therapeutic potential and hi |
| 37608325 | 10.1007/978-981-19-0120-1_22 | 10.1186/s13195-023-01285-8 | A metagenomic study of gut viral markers in amyloid-positive Alzheimer's disease |
| 37624247 | 10.4331/wjbc.v1.i5.188 | 10.3390/toxins15080490 | In Silico-Ex Vitro Iteration Strategy for Affinity Maturation of Anti-Ricin Pept |
| 37624267 | 10.1016/j.toxcx.2020.100049 | 10.3390/toxins15080510 | The Need for Next-Generation Antivenom for Snakebite Envenomation in India. |
| 37626867 | 10.1038/nrd2153 | 10.3390/cells12162057 | Stability Considerations for Bacteriophages in Liquid Formulations Designed for  |
| 37627283 | 10.1074/jbc.M116.769703 | 10.3390/biom13081218 | The Impact of Viral Infection on the Chemistries of the Earth's Most Abundant Ph |
| 37628582 | 10.3389/fmicb.2021.701414 | 10.3390/genes14081529 | Deep Isolated Aquifer Brines Harbor Atypical Halophilic Microbial Communities in |
| 37628911 | 10.12688/wellcomeopenres.14694.1 | 10.3390/ijms241612729 | Molecular and Genomic Analysis of the Virulence Factors and Potential Transmissi |
| 37630448 | 10.1016/j.ijantimicag.2019.11.001 | 10.3390/microorganisms11081888 | Peptidoglycan Endopeptidase from Novel Adaiavirus Bacteriophage Lyses Pseudomona |
| 37632008 | 10.7717/peerj.2261 | 10.3390/v15081665 | Compounding Achromobacter Phages for Therapeutic Applications. |
| 37632043 | 10.1128/MRA.01143-18 | 10.3390/v15081701 | A Temperate Sinorhizobium Phage, AP-16-3, Closely Related to Phage 16-3: Mosaic  |
| 37632068 | 10.1016/j.cell.2021.01.029 | 10.3390/v15081726 | Human Neutrophil Response to Pseudomonas Bacteriophage PAK_P1, a Therapeutic Can |
| 37632288 | 10.1007/s00401-017-1802-y | 10.1002/ana.26776 | Detection of High-Risk Paraneoplastic Antibodies against TRIM9 and TRIM67 Protei |
| 37632545 | 10.2353/ajpath.2006.050479 | 10.1007/s00005-023-00685-w | Improved Production of Anti-FGF-2 Nanobody Using Pichia pastoris and Its Effect  |
| 37632647 | 10.1096/fj.10-180331 | 10.1007/s12026-023-09418-9 | A high affinity and specificity anti-HER2 single-domain antibody (VHH) that targ |
| 37634214 | 10.3390/ijms140918488 | 10.1007/s10930-023-10145-1 | Staphylococcus aureus Bacteriophage 52 Endolysin Exhibits Anti-Biofilm and Broad |
| 37635262 | 10.1371/journal.pone.0061217 | 10.1186/s40168-023-01632-9 | The impact of storage buffer and storage conditions on fecal samples for bacteri |
| 37638647 | 10.1021/acsinfecdis.2c00006 | 10.1021/acschemneuro.3c00248 | Synergistic Screening of Peptide-Based Biotechnological Drug Candidates for Neur |
| 37642487 | 10.1016/S0140-6736(20)30566-3 | 10.1002/mbo3.1371 | Isolation and functional analysis of phage-displayed antibody fragments targetin |
| 37644177 | 10.1007/s40265-020-01257-4 | 10.1007/s00108-023-01567-1 | [New developments in the fight against bacterial infections : Update on antiobio |
| 37647137 | 10.1021/acs.estlett.2c00350 | 10.1021/acs.est.3c03376 | Adsorption of Respiratory Syncytial Virus, Rhinovirus, SARS-CoV-2, and F+ Bacter |
| 37656816 | 10.1007/s40572-018-0195-y | 10.1021/acs.est.3c03814 | The Protective Effect of Virus Capsids on RNA and DNA Virus Genomes in Wastewate |
| 37657419 | 10.1093/nar/gkt053 | 10.1016/j.cell.2023.07.039 | Phage-assisted evolution and protein engineering yield compact, efficient prime  |
| 37658299 | 10.1093/bioinformatics/btab007 | 10.1186/s12863-023-01153-2 | Complete genome sequences of Providencia bacteriophages PibeRecoleta, Stilesk an |
| 37660314 | 10.3390/antibiotics7030066 | 10.1007/s00705-023-05862-y | Genome characterization of the novel lytic phage vB_AbaAut_ChT04 and the antimic |
| 37661761 | 10.1038/s41392-020-00222-7 | 10.1080/21655979.2023.2252667 | Impaired proliferation and migration of HUVEC and melanoma cells by human anti-F |
| 37662248 | 10.1038/s41564-019-0510-x | 10.1101/2023.08.25.554831 | Inhibition of PQS signaling by the Pf bacteriophage protein PfsE enhances viral  |
| 37662851 | 10.1093/nar/gkab688 | 10.1016/j.bioflm.2023.100147 | Combining phages and antibiotic to enhance antibiofilm efficacy against an in vi |
| 37665209 | 10.1111/mmi.14683 | 10.1099/mgen.0.001100 | Host interactions of novel Crassvirales species belonging to multiple families i |
| 37668982 | 10.1021/acschembio.6b00555 | 10.1007/978-1-0716-3393-9_17 | Engineering SH2 Domains with Tailored Specificities and Affinities. |
| 37669381 | 10.1007/978-981-15-2651-0_13 | 10.1073/pnas.2309647120 | Picobirnaviruses encode proteins that are functional bacterial lysins. |
| 37672388 | 10.1017/S0950268820001582 | 10.1099/mgen.0.001090 | Analysis of Escherichia coli O157 strains in cattle and humans between Scotland  |
| 37676871 | 10.1002/1873-3468.13771 | 10.1371/journal.pone.0291109 | Genetic diversity of Salmonella enterica isolated over 13 years from raw Califor |
| 37679422 | 10.1002/jor.25432 | 10.1007/s00590-023-03720-w | The stability of Staphylococcal bacteriophage in presence of local vancomycin co |
| 37679612 | 10.4161/mabs.24218 | 10.1007/978-1-0716-3381-6_1 | Antibody Phage Display. |
| 37679613 | 10.1007/978-1-4939-7447-4_1 | 10.1007/978-1-0716-3381-6_2 | Construction of Human Immune and Naive scFv Phage Display Libraries. |
| 37679614 | 10.1038/s42003-021-01881-0 | 10.1007/978-1-0716-3381-6_3 | Construction of Naïve and Immune Human Fab Phage Display Library. |
| 37679615 | 10.1007/978-1-62703-992-5_8 | 10.1007/978-1-0716-3381-6_4 | Construction of Synthetic Antibody Phage Display Libraries. |
| 37679619 | 10.1093/intimm/dxaa078 | 10.1007/978-1-0716-3381-6_8 | Phagekines: Directed Evolution and Characterization of Functional Cytokines Disp |
| 37679621 | 10.1016/j.nbt.2021.01.010 | 10.1007/978-1-0716-3381-6_10 | Construction of an Ultra-Large Phage Display Library by Kunkel Mutagenesis and R |
| 37679623 | 10.1371/journal.pone.0027756 | 10.1007/978-1-0716-3381-6_12 | Antibody Selection via Phage Display in Microtiter Plates. |
| 37679626 | 10.1007/978-3-642-01144-3_18 | 10.1007/978-1-0716-3381-6_15 | Magnetic Nanoparticle-Based Semi-automated Panning for High-Throughput Antibody  |
| 37679629 | 10.1021/nl0607636 | 10.1007/978-1-0716-3381-6_18 | Antibody Isolation from Human Synthetic Libraries of Single-Chain Antibodies and |
| 37679631 | 10.1016/S0022-1759(98)00144-6 | 10.1007/978-1-0716-3381-6_20 | Antibody Affinity and Stability Maturation by Error-Prone PCR. |
| 37679634 | 10.1186/1472-6750-12-62 | 10.1007/978-1-0716-3381-6_23 | High-Throughput IgG Reformatting and Expression Using Hybrid Secretion Signals a |
| 37679636 | 10.1073/pnas.1111218108 | 10.1007/978-1-0716-3381-6_25 | Mapping Polyclonal Antibody Responses to Infection Using Next-Generation Phage D |
| 37697078 | 10.1038/s41598-019-39929-1 | 10.1007/s10096-023-04658-x | Bacteriophage therapy: are we running before we have learned to walk? |
| 37702234 | 10.1016/j.ijbiomac.2023.125660 | 10.2174/1389201025666230912123849 | Postbiotic as Novel Alternative Agent or Adjuvant for the Common Antibiotic Util |
| 37704798 | 10.3390/v10070351 | 10.1038/s41598-023-42505-3 | Bacteriophages with depolymerase activity in the control of antibiotic resistant |
| 37704976 | 10.1371/journal.pone.0025486 | 10.1186/s12866-023-02976-w | Study of Combined Effect of Bacteriophage vB3530 and Chlorhexidine on the Inacti |
| 37725261 | 10.1080/2162402X.2020.1846915 | 10.1007/s42770-023-01118-8 | From antimicrobial to anticancer: the pioneering works of Prof. Luiz Rodolpho Tr |
| 37728456 | 10.3389/fmicb.2019.00574 | 10.5114/pedm.2023.125363 | Potential bacteriophages to overcome bacterial infection of Alcaligenes faecalis |
| 37730888 | 10.1063/5.0031150 | 10.1038/s41598-023-42403-8 | Evaluation of face shields used during aerosol generating procedures. |
| 37736037 | 10.1074/JBC.270.19.11181 | 10.1016/j.isci.2023.107745 | The phage-encoded protein PIT2 impacts Pseudomonas aeruginosa quorum sensing by  |
| 37737980 | 10.2174/1386207013331237 | 10.1007/978-1-0716-3453-0_7 | Phage Immunoprecipitation Sequencing (PhIP-Seq) for Analyzing Antibody Epitope R |
| 37738590 | 10.1101/2022.05.15.492003 | 10.1093/bioinformatics/btad586 | Phables: from fragmented assemblies to high-quality bacteriophage genomes. |
| 37741937 | 10.1186/s42523-022-00177-w | 10.1007/s00253-023-12743-6 | Genomic and proteomic characterization of vB_SauM-UFV_DC4, a novel Staphylococcu |
| 37742917 | 10.1002/pmic.201600391 | 10.1016/j.jbc.2023.105278 | Sequence tolerance of immunoglobulin variable domain framework regions to noncan |
| 37753068 | 10.1111/j.1478-3231.2008.01826.x | 10.2147/IJN.S428430 | Identification and Characterization of a Novel Nanobody Against Human CTGF to Re |
| 37753081 | 10.3389/fimmu.2022.953917 | 10.3389/fimmu.2023.1257042 | Unleashing the power of shark variable single domains (VNARs): broadly neutraliz |
| 37758823 | 10.1002/lpor.202200814 | 10.1038/s41598-023-43480-5 | Highly sensitive label-free biosensor: graphene/CaF2 multilayer for gas, cancer, |
| 37764074 | 10.1371/journal.pone.0168615 | 10.3390/microorganisms11092230 | Comparison of Antibiofilm Activity of Pseudomonas aeruginosa Phages on Isolates  |
| 37765038 | 10.1016/S1473-3099(18)30482-1 | 10.3390/ph16091230 | Age of Antibiotic Resistance in MDR/XDR Clinical Pathogen of Pseudomonas aerugin |
| 37766190 | 10.1099/ijsem.0.005288 | 10.3390/v15091781 | Characterisation of the Novel Filamentous Phage PMBT54 Infecting the Milk Spoila |
| 37766228 | 10.1128/IAI.00840-10 | 10.3390/v15091821 | Characterization of Diverse Anelloviruses, Cressdnaviruses, and Bacteriophages i |
| 37766240 | 10.1080/10934520903217054 | 10.3390/v15091833 | Inactivation of Bacteriophage ɸ6 and SARS-CoV-2 in Antimicrobial Surface Tests. |
| 37766309 | 10.1038/s41416-018-0325-1 | 10.3390/v15091903 | Progress on Phage Display Technology: Tailoring Antibodies for Cancer Immunother |
| 37768041 | 10.1073/pnas.2014920118 | 10.1128/mbio.01830-23 | Systemic application of bone-targeting peptidoglycan hydrolases as a novel treat |
| 37775657 | 10.1016/j.celrep.2020.108065 | 10.1007/978-1-0716-3469-1_4 | An Approach for Antigen-Agnostic Identification of Virus-Like Particle-Displayed |
| 37775669 | 10.1146/annurev.iy.11.040193.001555 | 10.1007/978-1-0716-3469-1_16 | Melt Processing Virus-Like Particle-Based Vaccine Candidates into Biodegradable  |
| 37777575 | 10.1016/j.jbiotec.2021.02.010 | 10.1038/s41598-023-43559-z | Expression of a recombinant endolysin from bacteriophage CAP 10-3 with lytic act |
| 37781379 | 10.1007/s00253-012-4518-x | 10.3389/fimmu.2023.1224397 | Advances in phage display based nano immunosensors for cholera toxin. |
| 37781858 | 10.71371/journal.pone.0076571 | 10.1002/anie.202309744 | Stereoselective Synthesis of Sialyl Lewisa Antigen and the Effective Anticancer  |
| 37789281 | 10.1093/ofid/ofad221 | 10.1186/s12879-023-08621-1 | Reviewing the journey to the clinical application of bacteriophages to treat mul |
| 37789862 | 10.1038/srep29344 | 10.3389/fmicb.2023.1170418 | Beyond antibiotics: phage-encoded lysins against Gram-negative pathogens. |
| 37790805 | 10.1038/aja.2012.40 | 10.3389/fphar.2023.1243824 | Case report: Successful treatment of recurrent E. coli infection with bacterioph |
| 37791751 | 10.1099/mic.0.2007/013714-0 | 10.1128/jb.00196-23 | Bacteriophage steering of Burkholderia cenocepacia toward reduced virulence and  |
| 37791767 | 10.1002/pro.4519 | 10.1128/msystems.00446-23 | The heterogenous and diverse population of prophages in Mycobacterium genomes. |
| 37795104 | 10.1038/3315 | 10.3389/fimmu.2023.1243946 | Identification of SKOR2 IgG as a novel biomarker of paraneoplastic neurologic sy |
| 37800970 | 10.2217/pgs.13.12 | 10.1128/spectrum.04597-22 | Mycobacteriophage D29 Lysin B exhibits promising anti-mycobacterial activity aga |
| 37803295 | 10.1016/j.micpath.2019.04.016 | 10.1186/s12917-023-03743-9 | Preparation of Escherichia coli ghost of anchoring bovine Pasteurella multocida  |
| 37808693 | 10.21105/joss.01686 | 10.1101/2023.09.26.559468 | The impact of phage and phage resistance on microbial community dynamics. |
| 37808979 | 10.1099/vir.0.016378-0 | 10.3389/fpubh.2023.1212018 | Applications of VirScan to broad serological profiling of bat reservoirs for eme |
| 37819122 | 10.3389/fmicb.2020.602444 | 10.1128/spectrum.02907-23 | Stability of magistral phage preparations before therapeutic application in pati |
| 37819980 | 10.1038/s41589-023-01422-2 | 10.1073/pnas.2303690120 | Phage display uncovers a sequence motif that drives polypeptide binding to a con |
| 37822360 | 10.1093/cid/ciy802 | 10.3389/fcimb.2023.1220943 | Metagenomic next-generation sequencing of bronchoalveolar lavage fluid assists i |
| 37822941 | 10.1016/j.cell.2020.05.025 | 10.3389/fimmu.2023.1271508 | A novel bispecific antibody dual-targeting approach for enhanced neutralization  |
| 37824011 | 10.1002/smll.202200059 | 10.1007/978-1-0716-3377-9_15 | Atomic Force Microscopy of Viruses: Stability, Disassembly, and Genome Release. |
| 37828992 | 10.1093/nar/16.22.10881 | 10.3389/fimmu.2023.1221108 | Antibodies to coagulase of Staphylococcus aureus crossreact to Efb and reveal di |
| 37834144 | 10.1021/acs.analchem.7b01247 | 10.3390/ijms241914698 | The Generation of a Nanobody-Based ELISA for Human Microsomal Epoxide Hydrolase. |
| 37834237 | 10.1093/glycob/cwv018 | 10.3390/ijms241914787 | An Intrabody against B-Cell Receptor-Associated Protein 31 (BAP31) Suppresses th |
| 37843121 | 10.1128/AAC.00464-18 | 10.1093/cid/ciad475 | The Antibacterial Resistance Leadership Group: Scientific Advancements and Futur |
| 37843655 | 10.1016/S0966-842X(01)02198-9 | 10.1007/s00248-023-02301-y | An Eco-evolutionary Model on Surviving Lysogeny Through Grounding and Accumulati |
| 37843806 | 10.3390/MICROORGANISMS8040480 | 10.1007/978-3-031-41741-2_4 | Chemical-Biology and Metabolomics Studies in Phage-Host Interactions. |
| 37844250 | 10.1039/d2tb02355e | 10.1073/pnas.2221859120 | Viral nanoparticle vaccines against S100A9 reduce lung tumor seeding and metasta |
| 37845226 | 10.1007/s00284-019-01751-3 | 10.1038/s41467-023-42114-8 | Distantly related Alteromonas bacteriophages share tail fibers exhibiting proper |
| 37853918 | 10.1111/eos.12784 | 10.1111/1751-7915.14339 | Development of engineered endolysins with in vitro intracellular activity agains |
| 37855339 | 10.5384/sjovs.v14i2.130 | 10.2174/0109298673255220231010073215 | Beyond the Dusty Fog: Local Eye Drop Therapy and Potentially New Treatment Alter |
| 37855638 | 10.1002/pro.3235 | 10.1128/jvi.01448-23 | Discovery of Nanosota-2, -3, and -4 as super potent and broad-spectrum therapeut |
| 37855639 | 10.1056/evidoa2200131 | 10.1128/aac.00578-23 | Phage-antibiotic combinations against multidrug-resistant Pseudomonas aeruginosa |
| 37857919 | 10.1056/NEJMoa054765 | 10.1007/s10096-023-04682-x | Country-wide expansion of a VIM-1 carbapenemase-producing Klebsiella oxytoca ST1 |
| 37869063 | 10.1080/19420862.2022.2047144 | 10.2147/IJN.S427990 | A Naïve Phage Display Library-Derived Nanobody Neutralizes SARS-CoV-2 and Three  |
| 37872768 | 10.1007/s15010-021-01643-4 | 10.1080/21505594.2023.2273567 | Potential of phage depolymerase for the treatment of bacterial biofilms. |
| 37874326 | 10.1093/infdis/jiac430 | 10.1099/mgen.0.001124 | Genetic variants linked to the phenotypic outcome of invasive disease and carria |
| 37875544 | 10.3390/v11030241 | 10.1038/s41598-023-45405-8 | Phage activity against Staphylococcus aureus is impaired in plasma and synovial  |
| 37876041 | 10.18637/jss.v070.i10 | 10.1017/S0950268823001723 | Using SNP addresses for Salmonella Typhimurium DT104 in routine veterinary outbr |
| 37877697 | 10.3390/v11010088 | 10.1128/aac.00728-23 | Ciprofloxacin in combination with bacteriophage cocktails against multi-drug res |
| 37882540 | 10.1093/nar/gkaa1113 | 10.1128/mbio.01985-23 | Adaptation to bile and anaerobicity limits Vibrio cholerae phage adsorption. |
| 37882584 | 10.1038/s41592-022-01488-1 | 10.1128/spectrum.04298-22 | Broad-range capsule-dependent lytic Sugarlandvirus against Klebsiella sp. |
| 37883333 | 10.1016/0022-1759(83)90303-4 | 10.1371/journal.pbio.3002341 | Mammalian cells internalize bacteriophages and use them as a resource to enhance |
| 37891627 | 10.1039/C4MB00438H | 10.1186/s40168-023-01666-z | Virus diversity and activity is driven by snowmelt and host dynamics in a high-a |
| 37894788 | 10.1002/bit.25571 | 10.3390/ijms242015108 | IRAK3 Knockout and Wildtype THP-1 Monocytes as Models for Endotoxin Detection As |
| 37894982 | 10.1093/nar/gky427 | 10.3390/ijms242015302 | Genomes of a Novel Group of Phages That Use Alternative Genetic Code Found in Hu |
| 37896809 | 10.1038/nbt.3820 | 10.3390/v15102031 | The International Virus Bioinformatics Meeting 2023. |
| 37896872 | 10.1099/mic.0.28265-0 | 10.3390/v15102096 | The Dynamics of Synthesis and Localization of Jumbo Phage RNA Polymerases inside |
| 37896873 | 10.1128/jb.174.5.1462-1477.1992 | 10.3390/v15102095 | The Isolation and Characterization of Bacteriophages Infecting Avian Pathogenic  |
| 37897520 | 10.1038/s41564-020-00830-7 | 10.1007/s10096-023-04677-8 | Co-regulation of biofilm formation and antimicrobial resistance in Acinetobacter |
| 37902315 | 10.1016/j.scitotenv.2021.146191 | 10.1128/aem.01219-23 | Persistence of SARS-CoV-2 and its surrogate, bacteriophage Phi6, on surfaces and |
| 37904586 | 10.1128/ecosalplus.ESP-0003-2013 | 10.1093/nar/gkad977 | PacBio sequencing of human fecal samples uncovers the DNA methylation landscape  |
| 37909043 | 10.1038/nmeth.4169 | 10.1016/j.str.2023.10.007 | Cryo-EM structure of a Shigella podophage reveals a hybrid tail and novel decora |
| 37914863 | 10.1021/ac301924f | 10.1007/s12033-023-00926-5 | Principles, Methods, and Real-Time Applications of Bacteriophage-Based Pathogen  |
| 37922210 | 10.18637/jss.v021.i12 | 10.1021/acssynbio.3c00355 | Mammalian Genomic Manipulation with Orthogonal Bxb1 DNA Recombinase Sites for th |
| 37923729 | 10.1186/1471-2105-10-421 | 10.1038/s41467-023-42694-5 | Diagnostic and commensal Staphylococcus pseudintermedius genomes reveal niche ad |
| 37923820 | 10.1128/AAC.02573-17 | 10.1038/s41598-023-45313-x | Two novel phages PSPa and APPa inhibit planktonic, sessile and persister populat |
| 37929884 | 10.1016/j.canlet.2013.05.022 | 10.1111/jcmm.18030 | Acetylshikonin induces apoptosis through the endoplasmic reticulum stress-activa |
| 37931230 | 10.21105/joss.03167 | 10.1128/aac.00654-23 | Jumbo phages are active against extensively drug-resistant eyedrop-associated Ps |
| 37932119 | 10.1101/2023.04.19.537516 | 10.1093/cid/ciad539 | Knowing and Naming: Phage Annotation and Nomenclature for Phage Therapy. |
| 37932511 | 10.1056/NEJMoa063842 | 10.1038/s41577-023-00951-0 | Role of the microbiota in response to and recovery from cancer therapy. |
| 37934865 | 10.1093/bioinformatics/btr064 | 10.1172/jci.insight.174976 | Validation of a murine proteome-wide phage display library for identification of |
| 37943040 | 10.2174/138920110790725311 | 10.1128/jvi.00850-23 | Phage Milagro: a platform for engineering a broad host range virulent phage for  |
| 37945533 | 10.7554/eLife.46134.001 | 10.1002/pro.4824 | Engineered antigen-binding fragments for enhanced crystallization of antibody:an |
| 37949857 | 10.1128/AEM.71.11.6856-6862.2005 | 10.1038/s41467-023-43145-x | A closed translocation channel in the substrate-free AAA+ ClpXP protease diminis |
| 37954588 | 10.3389/fmicb.2022.886252 | 10.3389/fimmu.2023.1258136 | Glycosylation of bacterial antigens changes epitope patterns. |
| 37956142 | 10.1371/journal.pone.0221944 | 10.1371/journal.pone.0294190 | Phage therapy: Awareness and demand among clinicians in the United Kingdom. |
| 37957846 | 10.1016/j.plipres.2009.07.003 | 10.2174/0118715303257321231024094904 | Exploring the Interplay between Nutrients, Bacteriophages, and Bacterial Lipases |
| 37958578 | 10.1016/j.ijantimicag.2013.11.001 | 10.3390/ijms242115594 | Genetic and Phenotypic Analysis of Phage-Resistant Mutant Fitness Triggered by P |
| 37958612 | 10.3390/cells12030344 | 10.3390/ijms242115628 | Fitness Trade-Offs between Phage and Antibiotic Sensitivity in Phage-Resistant V |
| 37958944 | 10.3389/fendo.2015.00130 | 10.3390/ijms242115961 | Combined Multiplexed Phage Display, High-Throughput Sequencing, and Functional A |
| 37962408 | 10.3390/molecules22061024 | 10.1128/spectrum.02372-23 | The phage-encoded PIT4 protein affects multiple two-component systems of Pseudom |
| 37962552 | 10.3389/fmicb.2017.00559 | 10.1128/jcm.00614-23 | Interlaboratory comparison of Pseudomonas aeruginosa phage susceptibility testin |
| 37962644 | 10.3390/ijms23031873 | 10.1007/s00449-023-02938-6 | Engineered phage enzymes against drug-resistant pathogens: a review on advances  |
| 37963142 | 10.3390/pharmaceutics11110592 | 10.1371/journal.pone.0289183 | An intravenous pancreatic cancer therapeutic: Characterization of CRISPR/Cas9n-m |
| 37965262 | 10.1016/j.mimet.2016.11.020 | 10.3389/fcimb.2023.1250339 | Bacterial outer membrane vesicles bound to bacteriophages modulate neutrophil re |
| 37965326 | 10.1038/s41392-020-00348-8 | 10.3389/fimmu.2023.1227572 | Novel NKG2D-directed bispecific antibodies enhance antibody-mediated killing of  |
| 37966242 | 10.1371/journal.ppat.1001270 | 10.1128/spectrum.01477-23 | Identification and impact on Pseudomonas aeruginosa virulence of mutations confe |
| 37966590 | 10.3389/fbioe.2019.00144 | 10.1007/978-1-0716-3549-0_2 | The Diversity of Bacteriophages in the Human Gut. |
| 37966592 | 10.33073/pjm-2014-019 | 10.1007/978-1-0716-3549-0_4 | The Diversity of Bacteriophages in Hot Springs. |
| 37966594 | 10.3390/v12101143 | 10.1007/978-1-0716-3549-0_6 | Purification and Up-Concentration of Bacteriophages and Viruses from Fecal Sampl |
| 37966595 | 10.1007/978-1-60327-164-6_17 | 10.1007/978-1-0716-3549-0_7 | Isolation of Enterococcus Bacteriophages from Municipal Wastewater Samples Using |
| 37966598 | 10.1016/S0166-0934(02)00163-5 | 10.1007/978-1-0716-3549-0_10 | Detection and Quantification of Bacteriophages in Wastewater Samples by Culture  |
| 37966601 | 10.1093/bioinformatics/btu031 | 10.1007/978-1-0716-3549-0_13 | Bioinformatic Analysis of Staphylococcus Phages: A Key Step for Safe Cocktail De |
| 37966605 | 10.1007/7651_2014_186 | 10.1007/978-1-0716-3549-0_17 | Phage Transduction of Staphylococcus aureus. |
| 37966609 | 10.1128/jb.98.2.519-527.1969 | 10.1007/978-1-0716-3549-0_21 | The Application of Bacteriophage and Photoacoustic Flow Cytometry in Bacterial I |
| 37966610 | 10.1007/978-1-60327-164-6_23 | 10.1007/978-1-0716-3549-0_22 | Propagation, Purification, and Characterization of Bacteriophages for Phage Ther |
| 37966612 | 10.1016/S0140-6736(10)61030-6 | 10.1007/978-1-0716-3549-0_24 | Bacteriophage Virus-Like Particles: Platforms for Vaccine Design. |
| 37971191 | 10.1128/CMR.00111-13 | 10.1002/jor.25731 | The stability of Staphylococcal bacteriophages with commonly used prosthetic joi |
| 37971248 | 10.1016/j.mimet.2015.09.022 | 10.1128/spectrum.01813-23 | Distinct mode of action of a highly stable, engineered phage lysin killing Gram- |
| 37975684 | 10.1093/nar/gky448 | 10.1128/spectrum.03025-23 | The Acinetobacter baumannii K70 and K9 capsular polysaccharides consist of relat |
| 37977224 | 10.33140/JCEI | 10.1016/j.jbc.2023.105460 | Mapping immunological and host receptor binding determinants of SARS-CoV spike p |
| 37982612 | 10.1128/JCM.01113-19 | 10.1128/spectrum.01139-23 | Pathogen quantitative efficacy of different spike-in internal controls and clini |
| 38001360 | 10.1016/j.nucmedbio.2013.10.010 | 10.1038/s41598-023-47891-2 | Selection, characterization and in vivo evaluation of novel CD44v6-targeting ant |
| 38003392 | 10.1093/molbev/msw054 | 10.3390/ijms242216202 | Characterization of a Vibriophage Infecting Pathogenic Vibrio harveyi. |
| 38003626 | 10.1101/pdb.prot3468 | 10.3390/ijms242216437 | Utilizing Extraepitopic Amino Acid Substitutions to Define Changes in the Access |
| 38004732 | 10.1038/nrmicro3185 | 10.3390/microorganisms11112718 | T6SS: A Key to Pseudomonas's Success in Biocontrol? |
| 38005888 | 10.1016/j.coviro.2021.12.004 | 10.3390/v15112211 | Human Complement Inhibits Myophages against Pseudomonas aeruginosa. |
| 38005892 | 10.1128/MMBR.68.3.560-602.2004 | 10.3390/v15112215 | Analysis of Pseudomonas aeruginosa Isolates from Patients with Cystic Fibrosis R |
| 38006423 | 10.3389/fimmu.2021.759253 | 10.1007/s00284-023-03537-0 | Exploring the Human Virome: Composition, Dynamics, and Implications for Health a |
| 38009957 | 10.1093/bioinformatics/btaa213 | 10.1128/mbio.01766-23 | Host translation machinery is not a barrier to phages that interact with both CP |
| 38011181 | 10.1111/j.1469-0691.2011.03715.x | 10.1371/journal.pone.0294782 | A multiplex Taqman PCR assay for MRSA detection from whole blood. |
| 38014954 | 10.1093/nar/gki866 | 10.1128/msystems.00796-23 | Insights into virulence: structure classification of the Vibrio parahaemolyticus |
| 38014983 | 10.3389/fmicb.2019.02337 | 10.1128/spectrum.01882-23 | Pharmacokinetics and safety evaluation of intravenously administered Pseudomonas |
| 38018211 | 10.1177/0192623315625859 | 10.2174/0113892037269645231031095145 | Reduced Tumor Volume and Increased Necrosis of Human Breast Tumor Xenograft in M |
| 38038061 | 10.1038/s41564-019-0510-x | 10.1111/mmi.15202 | Inhibition of PQS signaling by the Pf bacteriophage protein PfsE enhances viral  |
| 38038764 | 10.1007/s00103-023-03711-6 | 10.1007/s00108-023-01620-z | [Precision medicine in infectious diseases]. |
| 38041113 | 10.1021/acsinfecdis.6b00006 | 10.1186/s12985-023-02230-9 | Development of a neutralization monoclonal antibody with a broad neutralizing ef |
| 38045026 | 10.15252/emmm.202012435 | 10.3389/fmicb.2023.1292618 | A mechanism-based pathway toward administering highly active N-phage cocktails. |
| 38047502 | 10.1016/S1470-2045(15)00083-2 | 10.1080/19420862.2023.2287250 | Development and pharmacokinetic assessment of a fully canine anti-PD-1 monoclona |
| 38049683 | 10.1128/jvi.01464-21 | 10.1007/s00436-023-08049-1 | A metatranscriptomic evaluation of viruses in field-collected bed bugs. |
| 38051037 | 10.21105/joss.03167 | 10.1128/msystems.00697-23 | Comparative genomics reveals the correlations of stress response genes and bacte |
| 38051048 | 10.1080/19490976.2021.1887719 | 10.1128/spectrum.01050-23 | Structural changes in the gut virome of patients with atherosclerotic cardiovasc |
| 38054715 | 10.1007/978-3-540-75418-3_6 | 10.1128/spectrum.03388-23 | Toxin/antitoxin systems induce persistence and work in concert with restriction/ |
| 38059609 | 10.1126/sciadv.abq2005 | 10.1128/mbio.02924-23 | Bacteriophage infection and killing of intracellular Mycobacterium abscessus. |
| 38062354 | 10.1093/bioinformatics/btq461 | 10.1186/s12864-023-09818-z | Comparative genomic analysis of clinical Enterococcus faecalis distinguishes str |
| 38063386 | 10.1186/1471-2148-15-S1-S1 | 10.1128/spectrum.02537-23 | Isolation and characterization of novel plasmid-dependent phages infecting bacte |
| 38063398 | 10.1099/mgen.0.000166 | 10.1128/aac.01192-23 | Emergence of cefiderocol resistance during ceftazidime/avibactam treatment cause |
| 38064533 | 10.1007/978-1-4939-9170-9_3 | 10.1371/journal.pbio.3002431 | Cas9 degradation in human cells using phage anti-CRISPR proteins. |
| 38066363 | 10.1128/MMBR.67.2.238-276.2003 | 10.1007/978-1-0716-3523-0_5 | Rapid Bench to Bedside Therapeutic Bacteriophage Production. |
| 38066368 | 10.3389/fmicb.2022.979610 | 10.1007/978-1-0716-3523-0_10 | Studying Bacteriophage Efficacy Using a Zebrafish Model. |
| 38066371 | 10.1128/AAC.01646-08 | 10.1007/978-1-0716-3523-0_13 | Bacteriophage Treatment of Infected Diabetic Foot Ulcers. |
| 38066372 | 10.1093/cid/ciac694 | 10.1007/978-1-0716-3523-0_14 | A Review of Phage Therapy for Bone and Joint Infections. |
| 38066373 | 10.1007/978-1-60327-164-6_14 | 10.1007/978-1-0716-3523-0_15 | Successful Use of Phage and Antibiotics Therapy for the Eradication of Two Bacte |
| 38066374 | 10.1371/journal.pone.0154925 | 10.1007/978-1-0716-3523-0_16 | Genetic Engineering and Rebooting of Bacteriophages in L-Form Bacteria. |
| 38068990 | 10.1038/s41598-017-10755-7 | 10.3390/ijms242316670 | Aerococcus viridans Phage Lysin AVPL Had Lytic Activity against Streptococcus su |
| 38076734 | 10.1016/j.virol.2008.04.003 | 10.2147/IJN.S431619 | Screening, Expression and Identification of Nanobody Against Monkeypox Virus A35 |
| 38079005 | 10.1093/molbev/msy096 | 10.1007/s00705-023-05940-1 | Genomic and biological characteristics of a novel lytic phage, vB_MscM-PMS3, inf |
| 38079060 | 10.1155/2014/382539 | 10.1007/s11262-023-02037-4 | Enhancement of bactericidal effects of bacteriophage and gentamicin combination  |
| 38084959 | 10.3389/fcimb.2021.684704 | 10.1128/jvi.01359-23 | Evaluation of the impact of repeated intravenous phage doses on mammalian host-p |
| 38084971 | 10.1128/spectrum.04671-22 | 10.1128/spectrum.03219-23 | Exploiting phage-antibiotic synergies to disrupt Pseudomonas aeruginosa PAO1 bio |
| 38094745 | 10.1016/j.arr.2022.101818 | 10.3389/fcimb.2023.1238543 | One-plasmid double-expression system for preparation of MS2 virus-like particles |
| 38096814 | 10.1093/nar/gkz991 | 10.1016/j.chom.2023.11.015 | Infant gut DNA bacteriophage strain persistence during the first 3 years of life |
| 38102298 | 10.18637/jss.v059.i05 | 10.1038/s41591-023-02685-x | The infant gut virome is associated with preschool asthma risk independently of  |
| 38103556 | 10.1093/nar/gkab301 | 10.1016/j.molcel.2023.11.026 | Phage anti-CBASS protein simultaneously sequesters cyclic trinucleotides and din |
| 38114502 | 10.1002/jcc.21787 | 10.1038/s41467-023-44160-8 | Biophysical basis of filamentous phage tactoid-mediated antibiotic tolerance in  |
| 38117559 | 10.1093/bioinformatics/btr039 | 10.1099/mgen.0.001172 | Genomic characterization of a unique Panton-Valentine leucocidin-positive commun |
| 38131664 | 10.1186/s12936-016-1625-7 | 10.1128/mbio.03142-23 | Plasmodium female gamete surface HSP90 is a key determinant for fertilization. |
| 38139096 | 10.1093/bioinformatics/btz848 | 10.3390/ijms242417267 | Investigating the Human Intestinal DNA Virome and Predicting Disease-Associated  |
| 38139119 | 10.1093/nar/gkab301 | 10.3390/ijms242417288 | Depolymerisation of the Klebsiella pneumoniae Capsular Polysaccharide K21 by Kle |
| 38139153 | 10.3390/v12111268 | 10.3390/ijms242417324 | Tentaclins-A Novel Family of Phage Receptor-Binding Proteins That Can Be Hypermu |
| 38140529 | 10.1128/JB.00983-15 | 10.3390/v15122287 | Isolation and Characterization of New Bacteriophages against Staphylococcal Clin |
| 38140531 | 10.3389/fphar.2019.01196 | 10.3390/v15122290 | Alginate-Encapsulated Mycobacteriophage: A Potential Approach for the Management |
| 38140696 | 10.1128/mSystems.00218-21 | 10.3390/v15122455 | StM171, a Stenotrophomonas maltophilia Bacteriophage That Affects Sensitivity to |
| 38143746 | 10.1186/s13045-020-00983-2 | 10.3389/fimmu.2023.1282176 | The role of macrophages in gastric cancer. |
| 38146311 | 10.3389/bjbs.2023.11387 | 10.3389/fcimb.2023.1334273 | Editorial: Phage therapy in infectious diseases of animals and humans. |
| 38147466 | 10.1073/pnas.98.3.974 | 10.1002/pro.4885 | Structural and functional validation of a highly specific Smurf2 inhibitor. |
| 38152664 | 10.1016/j.cmi.2021.05.049 | 10.3389/fpubh.2023.1258981 | Exploring the microbial landscape: uncovering the pathogens associated with comm |
| 38155176 | 10.1006/meth.2001.1262 | 10.1038/s41598-023-49880-x | Genome analysis of triple phages that curtails MDR E. coli with ML based host re |
| 38158479 | 10.3390/ph14010034 | 10.1007/s11845-023-03599-w | Phage-antibiotic synergism against Salmonella typhi isolated from stool samples  |
| 38160131 | 10.1038/s41541-020-0161-1 | 10.1016/j.vaccine.2023.12.077 | A bacteriophage virus-like particle vaccine against oxycodone elicits high-titer |
| 38165478 | 10.1039/D0RA05692H | 10.1007/s00253-023-12838-0 | Chitosan-based matrix as a carrier for bacteriophages. |
| 38165618 | 10.3389/fmicb.2018.00835 | 10.1007/978-1-0716-3561-2_8 | Use of Specific Borrelia Phages as a New Strategy for Improved Diagnostic Tests. |
| 38167452 | 10.1038/s41419-018-0818-0 | 10.1186/s13046-023-02910-y | A novel PDPN antagonist peptide CY12-RP2 inhibits melanoma growth via Wnt/β-cate |
| 38168031 | 10.1128/JB.186.10.3270-3273.2004 | 10.1038/s41467-023-44157-3 | Phage Paride can kill dormant, antibiotic-tolerant cells of Pseudomonas aerugino |
| 38172339 | 10.1111/j.2517-6161.1995.tb02031.x | 10.1038/s43018-023-00669-x | Bacteria and bacteriophage consortia are associated with protective intestinal m |
| 38178369 | 10.1093/bioinformatics/btv688 | 10.1080/19490976.2023.2298254 | Isolation and characterization of a novel lytic Parabacteroides distasonis bacte |
| 38181755 | 10.1093/nar/gkab301 | 10.1016/j.molcel.2023.12.005 | cGAS goes viral: A conserved immune defense system from bacteria to humans. |
| 38183010 | 10.1093/cvr/cvaa128 | 10.1186/s12866-023-03166-4 | Microbiome as a biomarker and therapeutic target in pancreatic cancer. |
| 38184487 | 10.1126/sciadv.aax0064 | 10.1007/s10529-023-03455-y | Construction of a bacteriophage-derived vector with potential applications in ta |
| 38184672 | 10.1371/journal.pgen.1002764 | 10.1038/s41598-023-50450-4 | Studying SARS-CoV-2 interactions using phage-displayed receptor binding domain a |
| 38194144 | 10.1016/j.mib.2016.05.006 | 10.1007/s00253-023-12839-z | New bacteriophage-derived lysins, LysJ and LysF, with the potential to control B |
| 38198031 | 10.2166/wh.2011.117 | 10.1007/s12560-023-09578-9 | Foodborne Viruses and Somatic Coliphages Occurrence in Fresh Produce at Retail f |
| 38203173 | 10.1038/srep08365 | 10.3390/ijms25010002 | Prophage Carriage and Genetic Diversity within Environmental Isolates of Clostri |
| 38203372 | 10.1016/j.xphs.2023.09.012 | 10.3390/ijms25010201 | Medical Device-Associated Healthcare Infections: Sterilization and the Potential |
| 38206055 | 10.3389/fmicb.2017.00840 | 10.1128/spectrum.03471-23 | Single-cell analysis reveals that cryptic prophage protease LfgB protects Escher |
| 38215547 | 10.1007/978-3-031-22997-8 | 10.1016/j.mib.2023.102421 | The intersection between host-pathogen interactions and metabolism during Vibrio |
| 38217826 | 10.1158/0008-5472.CAN-14-3000 | 10.1007/s12033-023-01021-5 | Preclinical Evaluation of virus-like particle Vaccine Against Carbonic Anhydrase |
| 38224841 | 10.1111/1462-2920.14504 | 10.1016/j.virusres.2024.199320 | Characterization and genomic analysis of a broad-spectrum lytic phage PG288: A p |
| 38225366 | 10.1038/s41564-023-01345-7 | 10.1038/s41591-023-02747-0 | Beyond bacteria: early-life gut virome link with childhood asthma development. |
| 38228619 | 10.1016/0041-0101(86)90089-9 | 10.1038/s41467-023-42624-5 | Antibody-dependent enhancement of toxicity of myotoxin II from Bothrops asper. |
| 38233948 | 10.1002/jobm.200510585 | 10.1186/s13071-023-06082-8 | Application of bacteria and bacteriophage cocktails for biological control of ho |
| 38234712 | 10.3390/antibiotics9050268 | 10.1016/j.bioflm.2023.100170 | Controlling of foodborne pathogen biofilms on stainless steel by bacteriophages: |
| 38236051 | 10.1186/s13059-014-0550-8 | 10.1128/mbio.02169-23 | Bacteriophage P22 SieA-mediated superinfection exclusion. |
| 38237058 | 10.1101/2023.07.29.550271 | 10.1021/acsnano.3c10339 | Surface Cross-Linking by Macromolecular Tethers Enhances Virus-like Particles' R |
| 38238612 | 10.1101/2021.06.21.449206 | 10.1007/s11262-024-02052-z | Two novel phages, Klebsiella phage GADU21 and Escherichia phage GADU22, from the |
| 38247783 | 10.1111/j.1600-0463.2007.apm_630.x | 10.3390/gels10010060 | Alginate Gel Encapsulated with Enzybiotics Cocktail Is Effective against Multisp |
| 38254012 | 10.1128/jcm.00831-18 | 10.1186/s12866-024-03185-9 | Genetic approach toward linkage of Iran 2012-2016 cholera outbreaks with 7th pan |
| 38254241 | 10.1038/s42003-021-02586-0 | 10.1186/s40779-024-00510-1 | Antimicrobial resistance crisis: could artificial intelligence be the solution? |
| 38257758 | 10.1002/jmv.28323 | 10.3390/v16010058 | Experimental Identification of Cross-Reacting IgG Hotspots to Predict Existing I |
| 38257809 | 10.1186/s12985-022-01918-8 | 10.3390/v16010109 | Metagenomic Analysis of Viromes of Aedes Mosquitoes across India. |
| 38257834 | 10.1128/AEM.03108-13 | 10.3390/v16010134 | Structural and Functional Disparities within the Human Gut Virome in Terms of Ge |
| 38258777 | 10.1128/AAC.00461-20 | 10.2174/0109298665181166231212051621 | Molecular Machinery of the Triad Holin, Endolysin, and Spanin: Key Players Orche |
| 38262441 | 10.1128/spectrum.00076-23 | 10.1055/s-0043-1778017 | Exploring Immunome and Microbiome Interplay in Reproductive Health: Current Know |
| 38263187 | 10.1128/AEM.02900-18 | 10.1038/s41598-023-50916-5 | Genomic analysis of vB_PaS-HSN4 bacteriophage and its antibacterial activity (in |
| 38263343 | 10.1074/jbc.M706230200 | 10.1038/s41598-024-51260-y | Antirepressor specificity is shaped by highly efficient dimerization of the stap |
| 38263397 | 10.1093/nar/gkv1189 | 10.1038/s41467-023-44370-0 | Ultraconserved bacteriophage genome sequence identified in 1300-year-old human p |
| 38264887 | 10.1038/ismej.2015.99 | 10.1099/mgen.0.001166 | Prophages: an integral but understudied component of the human microbiome. |
| 38275913 | 10.1038/nmeth.2019 | 10.1128/mbio.02540-23 | MEndoB, a chimeric lysin featuring a novel domain architecture and superior acti |
| 38275975 | 10.1165/rcmb.2007-0325OC | 10.3390/v16010165 | The Inovirus Pf4 Triggers Antiviral Responses and Disrupts the Proliferation of  |
| 38277241 | 10.1007/s00259-020-05097-y | 10.1158/1078-0432.CCR-23-3647 | Development of a [89Zr]Zr-labeled Human Antibody using a Novel Phage-displayed H |
| 38280942 | 10.1038/nmeth.2089 | 10.1038/s42003-024-05806-5 | M13 phage grafted with peptide motifs as a tool to detect amyloid-β oligomers in |
| 38284691 | 10.3390/ph15121498 | 10.2174/0118715265276529231214105423 | Strategies to Overcome Antimicrobial Resistance in Nosocomial Infections, A Revi |
| 38289080 | 10.1099/mgen.0.000206 | 10.1128/aac.01128-23 | Type I BREX system defends against antibiotic-resistant plasmids in Escherichia  |
| 38293203 | 10.1214/14-EJS890 | 10.1101/2024.01.16.575879 | Macrophage-induced reduction of bacteriophage density limits the efficacy of in  |
| 38294230 | 10.1093/bib/bbs017 | 10.1128/spectrum.02897-23 | A synthetic biology approach to assemble and reboot clinically relevant Pseudomo |
| 38298921 | 10.1128/msphere.00345-22 | 10.3389/fcimb.2023.1280265 | Resistance against two lytic phage variants attenuates virulence and antibiotic  |
| 38299825 | 10.1128/spectrum.00184-22 | 10.1128/msphere.00553-23 | Resistance, mechanism, and fitness cost of specific bacteriophages for Pseudomon |
| 38300409 | 10.1128/mr.52.1.1-28.1988 | 10.1007/s12275-024-00107-2 | Use of Cas9 Targeting and Red Recombination for Designer Phage Engineering. |
| 38300802 | 10.1111/PRD.12385 | 10.1016/j.celrep.2024.113728 | Bacteriophages, gut bacteria, and microbial pathways interplay in cardiometaboli |
| 38302537 | 10.1002/pro.3280 | 10.1038/s41598-024-52996-3 | The NMR structure of the Ea22 lysogenic developmental protein from lambda bacter |
| 38302552 | 10.1016/j.chembiol.2022.06.003 | 10.1038/s41598-024-52192-3 | Optimized preparation pipeline for emergency phage therapy against Pseudomonas a |
| 38307030 | 10.1101/655910 | 10.1016/j.xcrm.2024.101409 | Alterations in fecal virome and bacteriome virome interplay in children with aut |
| 38308075 | 10.1016/j.idcr.2023.e01854 | 10.1007/s15010-024-02178-0 | Phage therapy as a glimmer of hope in the fight against the recurrence or emerge |
| 38308169 | 10.1111/php.13805 | 10.1007/s43630-023-00521-2 | Germicidal efficacy of continuous and pulsed ultraviolet-C radiation on pathogen |
| 38315006 | 10.3389/fmicb.2017.02221 | 10.1128/aem.01062-23 | Degradation of Listeria monocytogenes biofilm by phages belonging to the genus P |
| 38319074 | 10.1128/IAI.69.4.2448-2455.2001 | 10.1128/spectrum.02927-23 | Coordination of prophage and global regulator leads to high enterotoxin producti |
| 38322011 | 10.1186/s13045-021-01095-1 | 10.3389/fimmu.2023.1303353 | Nanobodies: a promising approach to treatment of viral diseases. |
| 38323591 | 10.1542/peds.2005-0566 | 10.1080/22221751.2024.2316809 | Epidemiology and clinical features of Skin and Soft Tissue Infections Caused by  |
| 38325368 | 10.1021/ci200227u | 10.1016/j.str.2024.01.007 | Chaperone-assisted cryo-EM structure of P. aeruginosa PhuR reveals molecular bas |
| 38326411 | 10.1093/ps/80.3.278 | 10.1038/s41598-024-53365-w | Investigating bacteriophages as a novel multiple-hurdle measure against Campylob |
| 38326819 | 10.1021/acssynbio.7b00203 | 10.1186/s12934-024-02302-7 | Discovery of a high-performance phage-derived promoter/repressor system for prob |
| 38329337 | 10.3201/eid1908.130482 | 10.1128/jcm.01545-23 | Multicenter evaluation of BioCode GPP for syndromic molecular detection of gastr |
| 38329937 | 10.1073/pnas.0408992102 | 10.1371/journal.pntd.0011912 | Detection of Salmonella Typhi bacteriophages in surface waters as a scalable app |
| 38334630 | 10.1186/1465-9921-14-43 | 10.3390/cells13030238 | Pro-Fibrotic Effects of CCL18 on Human Lung Fibroblasts Are Mediated via CCR6. |
| 38338671 | 10.1093/nar/gkq179 | 10.3390/ijms25031393 | Biological Function of Prophage-Related Gene Cluster ΔVpaChn25_RS25055~ΔVpaChn25 |
| 38338703 | 10.1128/AEM.01209-19 | 10.3390/ijms25031424 | Correlation of Pseudomonas aeruginosa Phage Resistance with the Numbers and Type |
| 38341278 | 10.3390/v12040461 | 10.1093/jambio/lxae033 | Heat inactivation of aqueous viable norovirus and MS2 bacteriophage. |
| 38342498 | 10.1093/med/9780199609147.001.0001 | 10.1136/jme-2023-109423 | Ethical argument for establishing good manufacturing practice for phage therapy  |
| 38343039 | 10.3390/polym13234234 | 10.1021/acsami.3c15125 | Polypropylene-Rendered Antiviral by Three-Dimensionally Surface-Grafted Poly(N-b |
| 38345389 | 10.1016/0042-6822(66)90317-5 | 10.1128/spectrum.03719-23 | Characterization of a new Pseudomonas aeruginosa Queuovirinae bacteriophage. |
| 38345396 | 10.1093/milmed/usad385 | 10.1097/MCP.0000000000001050 | Bacteriophages for bronchiectasis: treatment of the future? |
| 38347019 | 10.1016/S0923-2508(98)80003-X | 10.1038/s41598-024-53317-4 | Lytic activity of phages against bacterial pathogens infecting diabetic foot ulc |
| 38349137 | 10.1021/ac60147a030 | 10.1128/mbio.03519-23 | Klebsiella pneumoniae K2 capsular polysaccharide degradation by a bacteriophage  |
| 38350843 | 10.2174/138161212799436412 | 10.1186/s12879-024-09022-8 | Single-domain antibodies against SARS-CoV-2 RBD from a two-stage phage screening |
| 38353560 | 10.1016/j.cell.2022.04.024 | 10.1128/mbio.03396-23 | Bacteriophage and antibiotic combination therapy for recurrent Enterococcus faec |
| 38353831 | 10.1007/978-1-4419-6084-9_5/TABLES/1 | 10.1007/s00203-023-03826-z | Biofilm-mediated infections by multidrug-resistant microbes: a comprehensive exp |
| 38357445 | 10.1002/med.21879 | 10.3389/fcimb.2024.1336821 | Bacteriophage therapy for drug-resistant Staphylococcus aureus infections. |
| 38357944 | 10.1136/bmj.320.7249.1574 | 10.2174/0113862073267755240126111628 | Phage Therapy in Bacterial Pneumonia Models: A Systematic Review and Meta-Analys |
| 38358956 | 10.1016/j.epidem.2020.100391 | 10.1371/journal.pntd.0011822 | Old tools, new applications: Use of environmental bacteriophages for typhoid sur |
| 38360595 | 10.3390/v14122760 | 10.1186/s12941-024-00678-3 | Genomic characterization, in vitro, and preclinical evaluation of two microencap |
| 38365227 | 10.1128/JB.01272-12 | 10.1093/ismejo/wrad003 | Rhizoviticin is an alphaproteobacterial tailocin that mediates biocontrol of gra |
| 38365255 | 10.1016/j.cell.2016.08.023 | 10.1093/ismejo/wrad025 | Filamentous prophage Pf4 promotes genetic exchange in Pseudomonas aeruginosa. |
| 38365702 | 10.1128/AAC.43.6.1523 | 10.1186/s12985-024-02306-0 | Phage vB_Ec_ZCEC14 to treat antibiotic-resistant Escherichia coli isolated from  |
| 38366022 | 10.1007/978-1-4939-0554-6_12 | 10.1093/ismejo/wrad039 | CRISPR-Cas in Pseudomonas aeruginosa provides transient population-level immunit |
| 38366192 | 10.3390/ijms232416195 | 10.1093/ismejo/wrae005 | Escherichia coli CRISPR arrays from early life fecal samples preferentially targ |
| 38372457 | 10.1021/acschemneuro.0c00518 | 10.1002/cpz1.957 | Mirror-Image Phage Display for the Selection of D-Amino Acid Peptide Ligands as  |
| 38372795 | 10.2147/ott.S104142 | 10.1007/s00253-024-13058-w | Advanced detection of cervical cancer biomarkers using engineered filamentous ph |
| 38376991 | 10.1007/s00253-003-1438-9 | 10.1128/jvi.01476-23 | Collateral sensitivity increases the efficacy of a rationally designed bacteriop |
| 38378698 | 10.1128/spectrum.00813-22 | 10.1038/s41467-024-45785-z | Exploiting lung adaptation and phage steering to clear pan-resistant Pseudomonas |
| 38381773 | 10.1038/nmeth.1923 | 10.1371/journal.ppat.1012023 | Antibody profiling and predictive modeling discriminate between Kaposi sarcoma a |
| 38383452 | 10.1093/bioinformatics/btp616 | 10.1038/s41467-024-45601-8 | Efficient encoding of large antigenic spaces by epitope prioritization with Dolp |
| 38383718 | 10.3390/antibiotics10030279 | 10.1038/s41598-024-54469-z | Stability study in selected conditions and biofilm-reducing activity of phages a |
| 38391505 | 10.1038/srep26717 | 10.3390/antibiotics13020119 | Advances in Development of Novel Therapeutic Strategies against Multi-Drug Resis |
| 38392890 | 10.1039/C9EW00190E | 10.3390/pathogens13020152 | Bacteriophage Challenges in Industrial Processes: A Historical Unveiling and Fut |
| 38393330 | 10.1093/nar/gkaa735 | 10.1128/mra.01174-23 | Complete genome sequence of Pseudomonas aeruginosa phage Knedl. |
| 38394193 | 10.1101/2020.07.11.198606 | 10.1126/sciadv.adj0341 | Accumulation of defense systems in phage-resistant strains of Pseudomonas aerugi |
| 38396784 | 10.2147/JMDH.S362994 | 10.3390/ijms25042107 | Bacteriophages-Dangerous Viruses Acting Incognito or Underestimated Saviors in t |
| 38396974 | 10.1093/protein/gzq002 | 10.3390/ijms25042297 | Generation of Endotoxin-Specific Monoclonal Antibodies by Phage and Yeast Displa |
| 38399370 | 10.1007/s00253-010-2777-y | 10.3390/ph17020155 | Antibacterial and Anti-Biofilm Efficacy of Endolysin LysAB1245 against a Panel o |
| 38400052 | 10.1016/j.microc.2023.108740 | 10.3390/v16020277 | Phage Display's Prospects for Early Diagnosis of Prostate Cancer. |
| 38400074 | 10.1021/acssynbio.3c00101 | 10.3390/v16020299 | Meeting Report of the Second Symposium of the Belgian Society for Viruses of Mic |
| 38400099 | 10.1093/gbe/evaa146 | 10.3390/vaccines12020115 | Adjuvanted Vaccine Induces Functional Antibodies against Pseudomonas aeruginosa  |
| 38402281 | 10.1093/nar/gkq810 | 10.1038/s41467-024-45969-7 | Phage-assisted evolution of highly active cytosine base editors with enhanced se |
| 38411110 | 10.4103/ejd.ejd_401_17 | 10.1128/spectrum.03212-23 | Synergistic bactericidal effects of phage-enhanced antibiotic therapy against MR |
| 38413544 | 10.1016/j.watres.2020.115670 | 10.1007/s12560-024-09584-5 | CrAss-Like Phages: From Discovery in Human Fecal Metagenome to Application as a  |
| 38415011 | 10.3390/microorganisms8010047 | 10.3389/fcimb.2024.1327969 | Cytokine expression in subjects with Mycobacterium avium ssp. paratuberculosis p |
| 38415633 | 10.4081/ejh.2021.3337 | 10.1128/msphere.00702-23 | Liver sinusoidal cells eliminate blood-borne phage K1F. |
| 38418927 | 10.1101/2023.07.24.550367 | 10.1038/s41579-024-01017-1 | Conservation and similarity of bacterial and eukaryotic innate immunity. |
| 38426733 | 10.1038/s41467-018-07641-9 | 10.1128/mra.01171-23 | The genome sequences of lytic Pseudomonas aeruginosa bacteriophages BL1, BL2, an |
| 38427766 | 10.5152/jemcr.2018.2238 | 10.4103/ijpm.ijpm_833_23 | Staphylococcal scalded skin syndrome in neonate: Another face of CA-MRSA. |
| 38431663 | 10.1002/imt2.56 | 10.1038/s41467-024-45257-4 | Transmission and dynamics of mother-infant gut viruses during pregnancy and earl |
| 38441061 | 10.1093/molbev/msx281 | 10.1128/aac.01459-23 | Inter-phylum circulation of a beta-lactamase-encoding gene: a rare but observabl |
| 38442093 | 10.1093/brain/awab455 | 10.1371/journal.pone.0297625 | Absence of specific autoantibodies in patients with narcolepsy type 1 as indicat |
| 38443577 | 10.1093/nar/gkad1019 | 10.1038/s41564-024-01616-x | Phage proteins target and co-opt host ribosomes immediately upon infection. |
| 38444699 | 10.1038/s41467-018-05997-6 | 10.1093/femsml/uqae002 | Refining the transcriptional landscapes for distinct clades of virulent phages i |
| 38448490 | 10.1093/bioinformatics/bty121 | 10.1038/s41598-024-56402-w | A long-read sequencing strategy with overlapping linkers on adjacent fragments ( |
| 38449296 | 10.1101/2021.10.04.463034 | 10.1093/bioinformatics/btae112 | Graph-theoretical prediction of biological modules in quaternary structures of l |
| 38459466 | 10.1128/aem.00991-22 | 10.1186/s12864-024-10110-x | Genome mining of Escherichia coli WG5D from drinking water source: unraveling an |
| 38459523 | 10.1038/srep27572 | 10.1186/s12917-024-03945-9 | Characteristics of intestinal bacteriophages and their relationship with Bacteri |
| 38461188 | 10.1093/bioinformatics/btp666 | 10.1038/s41598-024-54662-0 | Re-analysis of an outbreak of Shiga toxin-producing Escherichia coli O157:H7 ass |
| 38461214 | 10.1089/vim.2013.0128 | 10.1038/s42003-024-06006-x | Bacteriophage therapy for the treatment of Mycobacterium tuberculosis infections |
| 38468305 | 10.1016/j.jchromb.2012.05.015 | 10.1186/s40168-023-01746-0 | Perturbation and resilience of the gut microbiome up to 3 months after β-lactams |
| 38469347 | 10.3390/antiox10091498 | 10.3389/fcimb.2024.1296777 | PqsA mutation-mediated enhancement of phage-mediated combat against Pseudomonas  |
| 38470054 | 10.1021/ac60119a033 | 10.1128/mbio.01990-23 | Wall teichoic acid substitution with glucose governs phage susceptibility of Sta |
| 38470113 | 10.1007/978-1-4939-7383-5_15 | 10.1128/iai.00084-24 | Single-domain antibodies reveal unique borrelicidal epitopes on the Lyme disease |
| 38470133 | 10.1128/mbio.02441-21 | 10.1128/aac.01728-23 | Pseudomonas aeruginosa ventricular assist device infections: findings from ineff |
| 38470366 | 10.1073/pnas.1615288113 | 10.1039/d3nr05660k | Bacteriophage-based particles carrying the TNF-related apoptosis-inducing ligand |
| 38470611 | 10.1158/1078-0432.Ccr-19-1659 | 10.1021/acs.bioconjchem.4c00019 | Development of an Engineered Single-Domain Antibody for Targeting MET in Non-Sma |
| 38471546 | 10.6084/m9.figshare.c.7075454 | 10.1098/rspb.2023.1529 | Building pyramids against the evolutionary emergence of pathogens. |
| 38472239 | 10.4149/av_2019_412 | 10.1038/s41598-024-55776-1 | Phage-layer interferometry: a companion diagnostic for phage therapy and a bacte |
| 38473932 | 10.1002/jcc.21367 | 10.3390/ijms25052686 | Screening Peptide-Binding Partners for GenX via Phage Display. |
| 38474392 | 10.3390/v12060601 | 10.3390/cells13050428 | Harnessing the Diversity of Burkholderia spp. Prophages for Therapeutic Potentia |
| 38480650 | 10.1182/blood.V128.22.5630.5630 | 10.1007/s11307-024-01901-5 | Development of New CD38 Targeted Peptides for Cancer Imaging. |
| 38480702 | 10.1016/j.xpro.2022.102033 | 10.1038/s41467-024-46555-7 | Bacteriophage DNA induces an interrupted immune response during phage therapy in |
| 38483476 | 10.3389/fmicb.2021.705020 | 10.1128/spectrum.03919-23 | Complete sequence of carbapenem-resistant Ralstonia mannitolilytica clinical iso |
| 38483478 | 10.1016/j.jhin.2014.09.008 | 10.1128/spectrum.03797-23 | Effective elimination of bacteria on hard surfaces by the combined use of bacter |
| 38483683 | 10.1007/s00253-021-11384-x | 10.1007/s11033-024-09362-3 | Characterization and genome-informatic analysis of a novel lytic mendocina phage |
| 38484051 | 10.5281/ZENODO.10637358 | 10.1126/science.adk4422 | Continuous evolution of compact protein degradation tags regulated by selective  |
| 38486152 | 10.3390/v11110991 | 10.1186/s12879-024-09152-z | Isolation and characterization of lytic bacteriophages from various sources in A |
| 38493441 | 10.1016/j.joen.2010.08.053 | 10.1007/s00203-024-03897-6 | Isolation of phages against Streptococcus species in the oral cavity for potenti |
| 38494579 | 10.1002/med.21572 | 10.1007/s00018-024-05174-7 | Molecular engineering of a spheroid-penetrating phage nanovector for photodynami |
| 38497939 | 10.1084/jem.20220650 | 10.1001/jamaneurol.2024.0272 | Serologic Response to the Epstein-Barr Virus Peptidome and the Risk for Multiple |
| 38517165 | 10.1099/0022-1317-67-9-1759 | 10.1128/jvi.00603-23 | Mutagenesis and functional analysis of the varicella-zoster virus portal protein |
| 38517357 | 10.1136/gutjnl-2013-306651 | 10.1080/19490976.2024.2331520 | Using a human colonoid-derived monolayer to study bacteriophage translocation. |
| 38517580 | 10.3389/fmicb.2019.00420 | 10.1007/s10123-024-00508-8 | Preclinical characterization and in silico safety assessment of three virulent b |
| 38519791 | 10.1016/j.chom.2024.02.003 | 10.1038/s41575-024-00925-0 | Bacteriophages and host inflammation in IBD. |
| 38524182 | 10.1016/j.ajic.2012.11.004 | 10.3389/fcimb.2024.1351993 | Characterization of a Straboviridae phage vB_AbaM-SHI and its inhibition effect  |
| 38526142 | 10.1080/14787210.2019.1694905 | 10.1128/spectrum.03221-23 | A simple solid media assay for detection of synergy between bacteriophages and a |
| 38526721 | 10.1016/j.ijbiomac.2020.12.062 | 10.1007/978-1-0716-3798-2_2 | Generation of a Naïve Human scFv Phage Display Library and Panning Selection. |
| 38526726 | 10.1021/acsnano.1c03935 | 10.1007/978-1-0716-3798-2_7 | Single-Cell Proteomics by Barcoded Phage-Displayed Screening via an Integrated M |
| 38526727 | 10.1016/j.mimet.2005.06.001 | 10.1007/978-1-0716-3798-2_8 | Targeted Genome Editing of Virulent Pseudomonas Phages Using CRISPR-Cas3. |
| 38531981 | 10.1186/1472-6750-9-6 | 10.1038/s41598-024-57355-w | Transient expression of anti-HrpE scFv antibody reduces the hypersensitive respo |
| 38534149 | 10.1007/978-1-4939-2450-9 | 10.1128/spectrum.03534-23 | Targeting intracellular nontuberculous mycobacteria and M. tuberculosis with a b |
| 38539119 | 10.1038/s41551-021-00801-1 | 10.1186/s12866-024-03243-2 | Promiscuous, persistent and problematic: insights into current enterococcal geno |
| 38541227 | 10.3920/BM2020.0132 | 10.3390/medicina60030501 | Fully Characterized Effective Bacteriophages Specific against Antibiotic-Resista |
| 38542452 | 10.1038/s12276-023-00971-9 | 10.3390/ijms25063479 | Alzheimer's Disease: A Molecular Model and Implied Path to Improved Therapy. |
| 38543740 | 10.1016/j.cell.2020.09.018 | 10.3390/v16030374 | Evolution of Virology: Science History through Milestones and Technological Adva |
| 38543751 | 10.1186/s12929-023-00919-1 | 10.3390/v16030385 | Bacteriophage vB_SepP_134 and Endolysin LysSte_134_1 as Potential Staphylococcus |
| 38543787 | 10.1016/j.molcel.2021.12.021 | 10.3390/v16030422 | CRISPR RNA-Guided Transposases Facilitate Dispensable Gene Study in Phage. |
| 38543808 | 10.2903/j.efsa.2009.1076 | 10.3390/v16030443 | The Medicinal Phage-Regulatory Roadmap for Phage Therapy under EU Pharmaceutical |
| 38543814 | 10.1172/JCI145157 | 10.3390/v16030448 | Viral Epitope Scanning Reveals Correlation between Seasonal HCoVs and SARS-CoV-2 |
| 38543840 | 10.1038/s41467-019-11433-0 | 10.3390/v16030475 | A New Inovirus from the Human Blood Encodes Proteins with Nuclear Subcellular Lo |
| 38543843 | 10.1021/acs.analchem.2c00682 | 10.3390/v16030478 | Bacteriophage-Host Interactions and the Therapeutic Potential of Bacteriophages. |
| 38547072 | 10.1021/acs.jmedchem.2c00094 | 10.1371/journal.pone.0299804 | A phage-displayed disulfide constrained peptide discovery platform yields novel  |
| 38553443 | 10.1016/j.ymeth.2009.04.005 | 10.1038/s41467-024-47119-5 | Structural basis of Acinetobacter type IV pili targeting by an RNA virus. |
| 38555551 | 10.4315/0362-028X.JFP-16-457 | 10.1007/s00203-024-03923-7 | Isolation and characterization of a relatively broad-spectrum phage against Esch |
| 38558079 | 10.5281/zenodo.7768343 | 10.1371/journal.ppat.1012122 | Characterization and genomic analysis of the Lyme disease spirochete bacteriopha |
| 38559352 | 10.1080/22221751.2021.2002671 | 10.3389/fmicb.2024.1344962 | In vitro and in vivo evaluation of the biofilm-degrading Pseudomonas phage Motto |
| 38560569 | 10.3181/00379727-186-42590a | 10.32604/or.2023.044276 | Dual ligand-targeted Pluronic P123 polymeric micelles enhance the therapeutic ef |
| 38561651 | 10.1186/s12864-019-5677-2 | 10.1186/s12866-024-03241-4 | Transcriptional dynamics during Rhodococcus erythropolis infection with phage WC |
| 38564677 | 10.1039/c4an00826j | 10.1128/jb.00095-24 | Alkyl quinolones mediate heterogeneous colony biofilm architecture that improves |
| 38565143 | 10.1093/nar/28.1.33 | 10.1016/j.chom.2024.03.005 | A metagenomics pipeline reveals insertion sequence-driven evolution of the micro |
| 38565243 | 10.1093/nar/gkg595 | 10.1261/rna.079980.124 | Robo-Therm, a pipeline to RNA thermometer discovery and validation. |
| 38568909 | 10.1111/lam.12204 | 10.1371/journal.pone.0299691 | Development of a latex agglutination test based on VH antibody fragment for dete |
| 38572320 | 10.3389/fmicb.2022.1032186 | 10.3389/fcimb.2024.1361045 | Isolation and identification of a novel phage targeting clinical multidrug-resis |
| 38574067 | 10.1038/s41467-019-10097-0 | 10.1371/journal.pone.0301175 | Selection, engineering, and in vivo testing of a human leukocyte antigen-indepen |
| 38574145 | 10.5281/zenodo.10845966 | 10.1126/science.adl0635 | Removal of Pseudomonas type IV pili by a small RNA virus. |
| 38582763 | 10.1093/bioinformatics/btz265 | 10.1038/s41467-024-47192-w | Phage-specific immunity impairs efficacy of bacteriophage targeting Vancomycin R |
| 38582870 | 10.1107/S0907444909042073 | 10.1038/s41467-024-47213-8 | Potent human neutralizing antibodies against Nipah virus derived from two ancest |
| 38589670 | 10.1186/s40168-014-0064-3 | 10.1038/s41598-024-59065-9 | Bacteriophages from human skin infecting coagulase-negative Staphylococcus: dive |
| 38591854 | 10.3389/fmicb.2018.03192 | 10.1128/aac.01439-23 | The virtue of training: extending phage host spectra against vancomycin-resistan |
| 38607024 | 10.1016/j.virol.2009.12.002 | 10.3390/cells13070585 | Controlling Recombination to Evolve Bacteriophages. |
| 38607601 | 10.2217/fmb.12.24 | 10.1007/s10529-024-03476-1 | Neutralizing anti-diphtheria toxin scFv produced by phage display. |
| 38608728 | 10.1101/2023.03.16.531341 | 10.1016/j.jbc.2024.107283 | Utility of protein-protein binding surfaces composed of anti-parallel alpha-heli |
| 38610029 | 10.1038/s41408-022-00629-1 | 10.1186/s12967-024-05159-x | Development of nanobodies targeting hepatocellular carcinoma and application of  |
| 38610253 | 10.1016/j.celrep.2023.112672 | 10.3390/s24072042 | Tracking of Bacteriophage Predation on Pseudomonas aeruginosa Using a New Radiof |
| 38611711 | 10.1128/AAC.01703-15 | 10.3390/molecules29071431 | Camel-Derived Nanobodies as Potent Inhibitors of New Delhi Metallo-β-Lactamase-1 |
| 38612860 | 10.3390/antibiotics11081079 | 10.3390/ijms25074051 | Microbiota and Immunity during Respiratory Infections: Lung and Gut Affair. |
| 38616221 | 10.3892/etm.2013.946 | 10.1007/s00203-024-03938-0 | Biofilm inhibition/eradication: exploring strategies and confronting challenges  |
| 38619619 | 10.1093/nar/gkr485 | 10.1007/s00253-024-13129-y | Isolation and characterization of novel Staphylococcus aureus bacteriophage Hesa |
| 38619733 | 10.1016/j.drup.2019.07.002 | 10.1007/s42770-024-01311-3 | Genetic determinants of antimicrobial resistance in polymyxin B resistant Pseudo |
| 38624196 | 10.1146/annurev-virology-091919-071712 | 10.1128/aem.00286-24 | Warming alters life-history traits and competition in a phage community. |
| 38630615 | 10.1186/s40168-023-01644-5 | 10.1099/mgen.0.001240 | Genome sequences of the first Autographiviridae phages infecting marine Roseobac |
| 38632127 | 10.1111/mmi.14470 | 10.1007/s00284-024-03680-2 | Genomic Approach of Listeria monocytogenes Strains Isolated from Deli-Meats in M |
| 38639792 | 10.3390/vaccines11071176 | 10.1007/s00216-024-05294-w | Breaking barriers in electrochemical biosensing using bioinspired peptide and ph |
| 38646632 | 10.1186/1465-9921-13-35 | 10.3389/fmicb.2024.1374466 | Antimicrobial resistance of Pseudomonas aeruginosa: navigating clinical impacts, |
| 38648198 | 10.21105/joss.01686 | 10.1371/journal.pbio.3002346 | The impact of phage and phage resistance on microbial community dynamics. |
| 38649411 | 10.1093/nar/gkab1081 | 10.1038/s41564-024-01684-z | Phage defence system CBASS is regulated by a prokaryotic E2 enzyme that imitates |
| 38649443 | 10.1093/bib/bbx108 | 10.1038/s41598-024-59903-w | Isolation and characterisation of a novel Silviavirus bacteriophage promising an |
| 38649748 | 10.1126/science.adl0635 | 10.1038/s41579-024-01050-0 | Phages get snappy. |
| 38651885 | 10.1128/mbio.01851-22 | 10.1128/spectrum.00382-24 | First report of the chromosomal integration of carbapenemase gene blaIMP-19 in A |
| 38652717 | 10.1093/bioinformatics/btt703 | 10.1371/journal.pbio.3002566 | Lytic bacteriophages induce the secretion of antiviral and proinflammatory cytok |
| 38653744 | 10.1186/s12929-022-00806-1 | 10.1038/s41598-024-59444-2 | Phage-antibiotic combinations to control Pseudomonas aeruginosa-Candida two-spec |
| 38658531 | 10.1128/AEM.01541-09 | 10.1038/s41467-024-47457-4 | A comprehensive synthetic library of poly-N-acetyl glucosamines enabled vaccine  |
| 38674401 | 10.1038/sj.gt.3303019 | 10.3390/genes15040467 | Redirect Tropism of Fowl Adenovirus 4 Vector by Modifying Fiber2 with Variable D |
| 38675877 | 10.1128/JB.00120-20 | 10.3390/v16040535 | A Metagenomic Investigation of Potential Health Risks and Element Cycling Functi |
| 38675913 | 10.1016/j.heliyon.2020.e04162 | 10.3390/v16040570 | Improving Pharmacokinetics of Peptides Using Phage Display. |
| 38675937 | 10.1080/19420862.2016.1212149 | 10.3390/v16040596 | Combining Cellular Immunization and Phage Display Screening Results in Novel, Fc |
| 38675985 | 10.1016/j.jtbi.2006.01.027 | 10.3390/v16040645 | Lysis Physiology of Pseudomonas aeruginosa Infected with ssRNA Phage PRR1. |
| 38683990 | 10.1002/bip.360221211 | 10.1073/pnas.2317307121 | A general approach for selection of epitope-directed binders to proteins. |
| 38687034 | 10.1038/s41467-022-30269-9 | 10.1128/jb.00402-23 | Targeted deletion of Pf prophages from diverse Pseudomonas aeruginosa isolates h |
| 38687079 | 10.1099/jgv.0.000381 | 10.1128/spectrum.00758-24 | In vitro enhancement of Zika virus infection by preexisting West Nile virus anti |
| 38691464 | 10.1093/cid/ciz222 | 10.1016/j.xpro.2024.102949 | Protocol for phage matching, treatment, and monitoring for compassionate bacteri |
| 38694516 | 10.1099/jmm.0.000913 | 10.3389/fcimb.2024.1368923 | The complete genome sequence of unculturable Mycoplasma faucium obtained through |
| 38695573 | 10.3390/antibiotics10080999 | 10.1128/spectrum.00427-23 | Selective bacteriophages reduce the emergence of resistant bacteria in bacteriop |
| 38697296 | 10.1128/jvi.00837-18 | 10.1016/j.virusres.2024.199383 | A dual-targeting approach using a human bispecific antibody against the receptor |
| 38698002 | 10.1093/bioinformatics/btu033 | 10.1038/s41598-024-59148-7 | Genome plasticity shapes the ecology and evolution of Phocaeicola dorei and Phoc |
| 38698845 | 10.1038/nbt.2782 | 10.3389/fimmu.2024.1341389 | Rapid generation of human recombinant monoclonal antibodies from antibody-secret |
| 38710842 | 10.1371/journal.pone.0110726 | 10.1038/s42003-024-06247-w | Synthetic phage-based approach for sensitive and specific detection of Escherich |
| 38713013 | 10.1007/BF02789105 | 10.1042/BCJ20240019 | Efficient overexpression and purification of severe acute respiratory syndrome c |
| 38713338 | 10.22038/IJBMS.2022.62032.13760 | 10.1007/s12010-024-04943-1 | Developmental Formulation Principles of Food Preservatives by Nanoencapsulation- |
| 38713691 | 10.1073/pnas.1416587112 | 10.1371/journal.pone.0303056 | Factors of prescribing phage therapy among UK healthcare professionals: Evidence |
| 38716972 | 10.1093/nar/gkab092 | 10.1042/BST20231289 | Making the leap from technique to treatment - genetic engineering is paving the  |
| 38717818 | 10.1101/gr.251678.119 | 10.1099/mgen.0.001247 | Presence of phage-plasmids in multiple serovars of Salmonella enterica. |
| 38719911 | 10.3390/molecules16021776 | 10.1038/s41598-024-61230-z | Development of a new affinity maturation protocol for the construction of an int |
| 38726795 | 10.1016/j.clinthera.2023.06.009 | 10.1080/01652176.2024.2350661 | Successful phage-antibiotic therapy of P. aeruginosa implant-associated infectio |
| 38727217 | 10.1038/s41598-023-27734-w | 10.1128/msystems.01036-23 | What makes a temperate phage an effective bacterial weapon? |
| 38732011 | 10.3390/v15010174 | 10.3390/ijms25094791 | Development, High-Throughput Profiling, and Biopanning of a Large Phage Display  |
| 38732145 | 10.1073/pnas.2018181118 | 10.3390/ijms25094929 | Knowing Our Enemy in the Antimicrobial Resistance Era: Dissecting the Molecular  |
| 38733291 | 10.3390/vaccines4010003 | 10.1002/adhm.202302755 | Inducing Long Lasting B Cell and T Cell Immunity Against Multiple Variants of SA |
| 38736039 | 10.1016/S1473-3099(19)30427-X | 10.1080/21505594.2024.2349768 | Genetic, virulence, and antimicrobial resistance characteristics associated with |
| 38739436 | 10.1016/j.jmb.2012.07.019 | 10.1099/mic.0.001462 | Combined effect of SAR-endolysin LysKpV475 with polymyxin B and Salmonella bacte |
| 38742847 | 10.1016/j.amsu.2022.104895 | 10.1097/JS9.0000000000001605 | Antiseptic management of critical wounds: differential bacterial response upon e |
| 38745661 | 10.1158/2326-6066.CIR-13-0216 | 10.3389/fimmu.2024.1367040 | PD-L1 targeted peptide demonstrates potent antitumor and immunomodulatory activi |
| 38748218 | 10.1097/PRS.0000000000009472 | 10.1007/s00113-024-01439-9 | [Reconstruction options for infection-related defects : Plastic surgery armament |
| 38750067 | 10.1093/bioinformatics/btp163 | 10.1038/s41467-023-42104-w | Microbial adaptation to spaceflight is correlated with bacteriophage-encoded fun |
| 38753445 | 10.1172/jci.insight.163150 | 10.1172/JCI180012 | Unveiling the proteome-wide autoreactome enables enhanced evaluation of emerging |
| 38755613 | 10.1186/s12943-020-01185-7 | 10.1186/s12951-024-02521-5 | A humanized trivalent Nectin-4-targeting nanobody drug conjugate displays potent |
| 38765034 | 10.1016/j.watres.2023.119686 | 10.1016/j.heliyon.2024.e30738 | Kinetics of inactivation of bacteria responsible for infections in hospitals usi |
| 38766200 | 10.1038/s41467-024-53994-9 | 10.1101/2024.05.07.593005 | Dosing and Delivery of Bacteriophage Therapy In a Murine Wound Infection Model. |
| 38768614 | 10.26434/chemrxiv-2022-rdk8m | 10.1146/annurev-virology-111821-111145 | Bacteriophage T4 as a Protein-Based, Adjuvant- and Needle-Free, Mucosal Pandemic |
| 38771013 | 10.1099/jmm.0.001707 | 10.1099/mgen.0.001243 | Genomic analysis of an outbreak of Shiga toxin-producing Escherichia coli O183:H |
| 38772946 | 10.1172/JCI167957 | 10.1007/s00408-024-00700-7 | Phage Therapy for Respiratory Infections: Opportunities and Challenges. |
| 38773507 | 10.7554/eLife.69951 | 10.1186/s12951-024-02553-x | Outer membrane vesicles generated by an exogenous bacteriophage lysin and protec |
| 38776874 | 10.1038/s41592-019-0575-8 | 10.1016/j.xcrm.2024.101573 | Potent human monoclonal antibodies targeting Epstein-Barr virus gp42 reveal vuln |
| 38777835 | 10.1093/nar/gkac1052 | 10.1038/s41467-024-48655-w | Cystine-knot peptide inhibitors of HTRA1 bind to a cryptic pocket within the act |
| 38779661 | 10.1089/mab.2015.0053 | 10.3389/fimmu.2024.1382576 | Comparative characterization of two monoclonal antibodies targeting canine PD-1. |
| 38779673 | 10.1186/1559-0275-11-16 | 10.3389/fimmu.2024.1392456 | BacScan: a novel genome-wide strategy for uncovering broadly immunogenic protein |
| 38779676 | 10.1007/BF01886751 | 10.3389/fimmu.2024.1380694 | Isolation and characterization of Hc-targeting chimeric heavy chain antibodies n |
| 38779682 | 10.1016/j.ijpharm.2021.121206 | 10.3389/fimmu.2024.1398652 | Advances and optimization strategies in bacteriophage therapy for treating infla |
| 38779807 | 10.1002/adma.202102703 | 10.37201/req/039.2024 | New materials and complications of prostheses in humans: situation in Spain. |
| 38783333 | 10.1038/s41551-021-00730-z | 10.1186/s12951-024-02512-6 | BCMA/CD47-directed universal CAR-T cells exhibit excellent antitumor activity in |
| 38784808 | 10.1016/j.jgar.2020.03.023 | 10.3389/fmicb.2024.1397830 | Engineered endolysin of Klebsiella pneumoniae phage is a potent and broad-spectr |
| 38785444 | 10.1371/journal.pcbi.1009442 | 10.1128/spectrum.04287-23 | Gut virome alterations in patients with chronic obstructive pulmonary disease. |
| 38786114 | 10.1038/s41467-021-27656-z | 10.3390/antibiotics13050385 | Use of the Naturally Occurring Bacteriophage Grouping Model for the Design of Po |
| 38787276 | 10.1128/mBio.01462-20 | 10.3390/pathogens13050424 | Phage Therapy for Cardiac Implantable Electronic Devices and Vascular Grafts: A  |
| 38787890 | 10.1186/s13059-014-0550-8 | 10.1371/journal.pone.0298746 | Transcriptomic and proteomic analysis of the virulence inducing effect of ciprof |
| 38791502 | 10.1016/j.cmi.2023.01.021 | 10.3390/ijms25105465 | Current Knowledge and Perspectives of Phage Therapy for Combating Refractory Wou |
| 38792972 | 10.3390/v11040343 | 10.3390/medicina60050790 | How Effective Is Phage Therapy for Prosthetic Joint Infections? A Preliminary Sy |
| 38793567 | 10.1111/j.1365-2249.1990.tb05232.x | 10.3390/v16050686 | Unraveling the Properties of Phage Display Fab Libraries and Their Use in the Se |
| 38793624 | 10.1128/AEM.03817-12 | 10.3390/v16050743 | Phage-Bacterial Interaction Alters Phenotypes Associated with Virulence in Acine |
| 38794310 | 10.3390/pharmaceutics10030158 | 10.3390/pharmaceutics16050648 | Ciprofloxacin-Loaded Inhalable Formulations against Lower Respiratory Tract Infe |
| 38806609 | 10.32614/RJ-2016-025 | 10.1038/s41598-024-62953-9 | In vivo phage display identifies novel peptides for cardiac targeting. |
| 38807208 | 10.1038/nmeth.2727 | 10.1186/s12929-024-01045-2 | Development of a highly effective combination monoclonal antibody therapy agains |
| 38808067 | 10.3389/fmicb.2020.01134 | 10.3389/fcimb.2024.1373052 | Identification and characterization of the capsule depolymerase Dpo27 from phage |
| 38808279 | 10.1128/AAC.43.2.287 | 10.3389/fmicb.2024.1396774 | Characterization of Pseudomonas aeruginosa bacteriophages and control hemorrhagi |
| 38808710 | 10.1016/j.biopha.2022.113122 | 10.2174/0115665232305905240521081553 | Theranostic Potential of Bacteriophages against Oral Squamous Cell Carcinoma. |
| 38812675 | 10.3390/antibiotics11101432 | 10.3389/fmicb.2024.1401234 | Using phage to drive selections toward restoring antibiotic sensitivity in Pseud |
| 38814706 | 10.3390/v15041007 | 10.1099/jgv.0.001997 | Decoding huge phage diversity: a taxonomic classification of Lak megaphages. |
| 38816486 | 10.1038/nmeth.3176 | 10.1038/s42003-024-06337-9 | A metagenomic analysis of the phase 2 Anopheles gambiae 1000 genomes dataset rev |
| 38822912 | 10.2174/1389201023378490 | 10.1007/s12033-024-01195-6 | Phage Display as a Medium for Target Therapy Based Drug Discovery, Review and Up |
| 38829455 | 10.3390/idr13020051 | 10.1007/s10482-024-01984-8 | Insights into the genomic traits of Yersinia frederiksenii, Yersinia intermedia  |
| 38830864 | 10.1101/pdb.top115 | 10.1038/s41467-024-48735-x | Generation of nanobodies from transgenic 'LamaMice' lacking an endogenous immuno |
| 38834561 | 10.1128/AEM.65.2.868-872.1999 | 10.1038/s41467-024-48560-2 | Bacteriophage defends murine gut from Escherichia coli invasion via mucosal adhe |
| 38834776 | 10.32614/RJ-2013-014 | 10.1038/s41564-024-01705-x | Personalized bacteriophage therapy outcomes for 100 consecutive cases: a multice |
| 38834777 | 10.1093/cid/ciac453 | 10.1038/s41564-024-01712-y | Personalized bacteriophage therapy for difficult-to-treat infections. |
| 38835241 | 10.6084/m9.figshare.c.7214505 | 10.1098/rsob.230252 | Structural and functional characterization of nanobodies that neutralize Omicron |
| 38837964 | 10.1002/iid3.826 | 10.1371/journal.pone.0301223 | Discovery of a potent, selective, and tumor-suppressing antibody antagonist of a |
| 38839974 | 10.3390/v10020064 | 10.1038/s41564-024-01733-7 | Advocating for phage therapy. |
| 38842649 | 10.7554/eLife.42166 | 10.1007/s11427-024-2607-8 | Inhibition mechanisms of CRISPR-Cas9 by AcrIIA25.1 and AcrIIA32. |
| 38846353 | 10.3389/fmicb.2023.1280026 | 10.3389/fcimb.2024.1385562 | Deciphering the microbial landscape of lower respiratory tract infections: insig |
| 38849989 | 10.1136/jitc-2021-004225 | 10.1080/19420862.2024.2362432 | Structural analysis of light chain-driven bispecific antibodies targeting CD47 a |
| 38850320 | 10.1186/1471-2180-12-297 | 10.1007/s00253-024-13194-3 | Lysins as a powerful alternative to combat Bacillus anthracis. |
| 38851653 | 10.3389/fmicb.2019.02537 | 10.1007/s00705-024-06063-x | Characterization of bacteriophages infecting multidrug-resistant uropathogenic E |
| 38858494 | 10.1038/s41573-018-0007-y | 10.1038/s41401-024-01316-6 | T cell-redirecting antibody for treatment of solid tumors via targeting mesothel |
| 38858586 | 10.1016/j.stemcr.2017.03.012 | 10.1038/s41551-024-01227-1 | Efficient site-specific integration of large genes in mammalian cells via contin |
| 38858621 | 10.1128/aac.01384-09 | 10.1186/s12866-024-03349-7 | Quorum sensing gene lasR promotes phage vB_Pae_PLY infection in Pseudomonas aeru |
| 38862601 | 10.1016/j.mex.2022.101846 | 10.1038/s41598-024-64405-w | Discovery of a new class of cell-penetrating peptides by novel phage display pla |
| 38862604 | 10.18637/jss.v021.i12 | 10.1038/s41564-024-01635-8 | Longitudinal multi-omics analysis of host microbiome architecture and immune res |
| 38863706 | 10.3390/microorganisms10091782 | 10.3389/fimmu.2024.1402862 | Advancements in ovarian cancer immunodiagnostics and therapeutics via phage disp |
| 38870941 | 10.1038/nbt.2839 | 10.1016/j.chom.2024.05.016 | Characterization of a lipid-based jumbo phage compartment as a hub for early pha |
| 38884473 | 10.1016/j.bbamcr.2014.08.008 | 10.1128/iai.00215-24 | Identification of Babesia microti immunoreactive antigens by phage display cDNA  |
| 38886215 | 10.1016/j.molcel.2022.04.006 | 10.1038/s41576-024-00740-y | DNA packaging by molecular motors: from bacteriophage to human chromosomes. |
| 38886583 | 10.1093/nar/gkab1081 | 10.1038/s41564-024-01719-5 | Bacteriophage protein Dap1 regulates evasion of antiphage immunity and Pseudomon |
| 38891850 | 10.3389/fmicb.2018.01701 | 10.3390/ijms25115662 | Insight into the Mechanism of Lysogeny Control of phiCDKH01 Bacteriophage Infect |
| 38892193 | 10.1002/jcc.540040211 | 10.3390/ijms25116006 | Probing the Conformational Restraints of DNA Damage Recognition with β-L-Nucleot |
| 38896642 | 10.1038/sj.onc.1209203 | 10.1590/1414-431X2024e13190 | Rho GTPase activating protein 21-mediated regulation of prostate cancer associat |
| 38896653 | 10.1371/journal.pbio.3001514 | 10.1093/ismejo/wrae108 | Conditions for the spread of CRISPR-Cas immune systems into bacterial population |
| 38902231 | 10.1016/j.copbio.2020.11.011 | 10.1038/s41467-024-49603-4 | Guiding antibiotics towards their target using bacteriophage proteins. |
| 38909125 | 10.1186/1471-2180-9-169 | 10.1038/s41598-024-65143-9 | Bacteriophage ISP eliminates Staphylococcus aureus in planktonic phase, but not  |
| 38912817 | 10.1128/mBio.02184-18 | 10.1128/spectrum.03520-23 | Relevance of the bacteriophage adherence to mucus model for Pseudomonas aerugino |
| 38913264 | 10.1101/gr.251678.119 | 10.1007/s11356-024-33875-w | Genetic features of BEL-1-producing and KPC-2-producing E. coli from hospital wa |
| 38914878 | 10.1016/S0740-5472(03)00118-1 | 10.1007/7854_2024_478 | Role of the Microbiome and the Gut-Brain Axis in Alcohol Use Disorder: Potential |
| 38917809 | 10.1038/s41586-021-03819-2 | 10.1016/j.chom.2024.05.021 | A large-scale type I CBASS antiphage screen identifies the phage prohead proteas |
| 38918467 | 10.1109/JSTARS.2015.2403257 | 10.1038/s41564-024-01735-5 | Spatial mapping of mobile genetic elements and their bacterial hosts in complex  |
| 38918839 | 10.1016/j.copbio.2020.11.012 | 10.1186/s12951-024-02576-4 | Phage-based delivery systems: engineering, applications, and challenges in nanom |
| 38920383 | 10.1021/ac502040v | 10.1128/msphere.00011-24 | Nucleoid-associated proteins shape the global protein occupancy and transcriptio |
| 38920649 | 10.1111/cmi.13090 | 10.3390/cells13121019 | Mycobacterium tuberculosis FadD18 Promotes Proinflammatory Cytokine Secretion to |
| 38921819 | 10.1038/s41598-024-59444-2 | 10.3390/pathogens13060522 | Does Phage Therapy Need a Pan-Phage? |
| 38924428 | 10.5061/dryad.6djh9w18j | 10.1126/scitranslmed.adl3758 | Transcobalamin receptor antibodies in autoimmune vitamin B12 central deficiency. |
| 38924648 | 10.7554/eLife.46134.001 | 10.1002/pro.5081 | Antigen-binding fragments with improved crystal lattice packing and enhanced con |
| 38925791 | 10.1128/AAC.02071-21 | 10.1183/16000617.0029-2024 | Phage therapy: breathing new tactics into lower respiratory tract infection trea |
| 38926510 | 10.1007/s00439-007-0460-x | 10.1038/s41598-024-64782-2 | Functional analysis of two mutation sites in the OCA2 gene. |
| 38927189 | 10.1128/AEM.01434-14 | 10.3390/antibiotics13060523 | A Novel Bacteriophage Infecting Multi-Drug- and Extended-Drug-Resistant Pseudomo |
| 38932109 | 10.1111/risa.13426 | 10.3390/v16060816 | Capsid Integrity Detection of Enteric Viruses in Reclaimed Waters. |
| 38932188 | 10.3389/fmicb.2020.631161 | 10.3390/v16060897 | Bacteriophages and Green Synthesized Zinc Oxide Nanoparticles in Combination Are |
| 38932245 | 10.1371/journal.pone.0058404 | 10.3390/v16060953 | Exploring the Complexity of the Human Respiratory Virome through an In Silico An |
| 38932260 | 10.3390/v15030807 | 10.3390/v16060968 | Phage Display in Cancer Research: Special Issue Editorial. |
| 38932268 | 10.1016/j.sbi.2009.08.003 | 10.3390/v16060977 | Experimental Evolution Studies in Φ6 Cystovirus. |
| 38933276 | 10.1007/978-1-59745-554-1_16 | 10.3389/fimmu.2024.1407398 | Human antibodies neutralizing the alpha-latrotoxin of the European black widow. |
| 38934499 | 10.1016/j.toxcx.2019.100006 | 10.1080/21645515.2024.2366641 | Characterization of neutralizing chimeric heavy-chain antibodies against tetanus |
| 38934592 | 10.1016/j.jgg.2023.03.010 | 10.1128/msphere.00707-23 | Optimizing bacteriophage treatment of resistant Pseudomonas. |
| 38934605 | 10.1093/nar/gkaa351 | 10.1128/spectrum.04157-23 | Comparative genomic analysis of an emerging Pseudomonadaceae member, Thiopseudom |
| 38934645 | 10.1007/978-1-4939-9173-0_1 | 10.1128/msystems.00538-24 | Extremely halophilic brine community manipulation shows higher robustness of mic |
| 38935316 | 10.1017/ice.2016.174 | 10.1007/s12275-024-00150-z | Enterococcus Phage vB_EfaS_HEf13 as an Anti-Biofilm Agent Against Enterococcus f |
| 38937990 | 10.1128/jvi.02457-16 | 10.1002/advs.202309972 | Data-Driven Engineering of Phages with Tunable Capsule Tropism for Klebsiella pn |
| 38939995 | 10.1038/srep44929 | 10.2174/0109298673306699240614112615 | Antimicrobial Resistance and New Antimicrobial Agents, A Review of the Literatur |
| 38940542 | 10.1084/jem.20120033 | 10.1128/spectrum.00400-24 | Characterization of mAbs against Klebsiella pneumoniae type 3 fimbriae isolated  |
| 38943594 | 10.1371/journal.pone.0266136 | 10.1021/acsinfecdis.4c00058 | An Engineered N-Glycosylated Dengue Envelope Protein Domain III Facilitates Epit |
| 38945452 | 10.1101/2023.07.04.547721 | 10.1016/j.jbc.2024.107502 | Identification and biophysical characterization of a novel domain-swapped cameli |
| 38949386 | 10.1093/bioinformatics/btv421 | 10.1128/spectrum.03875-23 | The uncharacterized PA3040-3042 operon is part of the cell envelope stress respo |
| 38951925 | 10.1186/s40168-015-0124-3 | 10.1186/s40168-024-01820-1 | Overcoming donor variability and risks associated with fecal microbiota transpla |
| 38953006 | 10.3389/fmicb.2019.02761 | 10.3389/fcimb.2024.1397935 | Phage endolysins as new therapeutic options for multidrug resistant Staphylococc |
| 38953167 | 10.1128/microbiolspec.mdna3-0059-2014 | 10.1093/nar/gkae534 | Directed evolution of hyperactive integrases for site specific insertion of tran |
| 38954982 | 10.1111/febs.16356 | 10.1016/j.bbrc.2024.150321 | A method for rapid and reliable quantification of VEGF-cell binding activity. |
| 38960003 | 10.1128/msystems.00019-22 | 10.1016/j.virusres.2024.199426 | A diverse set of Enterococcus-infecting phage provides insight into phage host-r |
| 38960407 | 10.1093/nar/gkw458 | 10.1093/bib/bbae304 | AttABseq: an attention-based deep learning prediction method for antigen-antibod |
| 38962879 | 10.1128/mbio.01379-14 | 10.1111/1751-7915.14513 | You get what you test for: The killing effect of phage lysins is highly dependen |
| 38963841 | 10.5281/zenodo.10140769 | 10.1126/science.adl1356 | An intron endonuclease facilitates interference competition between coinfecting  |
| 38964787 | 10.3390/children7020014 | 10.1136/jitc-2024-008888 | Off-the-shelf CAR-NK cells targeting immunogenic cell death marker ERp57 execute |
| 38967872 | 10.1128/JCM.40.10.3613-3619.2002 | 10.1007/s00705-024-06081-9 | Three novel Enterobacter cloacae bacteriophages for therapeutic use from Ghanaia |
| 38969094 | 10.1002/jcp.28229 | 10.1016/j.jare.2024.07.002 | The role of gut microbiota, exosomes, and their interaction in the pathogenesis  |
| 38970126 | 10.3389/fimmu.2022.1005107 | 10.1186/s40168-024-01833-w | Fecal microbiota transplantation alters gut phage communities in a clinical tria |
| 38976078 | 10.1073/pnas.1706359114 | 10.1007/s00203-024-04068-3 | Gut virome and diabetes: discovering links, exploring therapies. |
| 38980574 | 10.1177/0022034509359125 | 10.1007/s13346-024-01660-4 | Dual phage-incorporated electrospun polyvinyl alcohol-eudragit nanofiber matrix  |
| 38987383 | 10.3390/v12050513 | 10.1038/s42003-024-06500-2 | Two-dimensional high-throughput on-cell screening of immunoglobulins against bro |
| 38987432 | 10.21769/BioProtoc.170 | 10.1038/s41598-024-67147-x | Efficient generation of a stable CHO-K1 cell line overexpressing the human water |
| 38992001 | 10.1002/smll.201402619 | 10.1038/s41467-024-50064-y | Harnessing virus flexibility to selectively capture and profile rare circulating |
| 38992033 | 10.1016/S1473-3099(20)30491-6 | 10.1038/s41467-024-49461-0 | Precision arbovirus serology with a pan-arbovirus peptidome. |
| 38992046 | 10.1016/j.tim.2023.05.002 | 10.1038/s41467-024-49710-2 | High throughput platform technology for rapid target identification in personali |
| 38998954 | 10.1080/19420862.2023.2168470 | 10.3390/molecules29133002 | Phage Display Technology in Biomarker Identification with Emphasis on Non-Cancer |
| 38999924 | 10.1016/J.PRP.2023.154362 | 10.3390/ijms25136814 | Unveiling the Secrets of Acinetobacter baumannii: Resistance, Current Treatments |
| 39000118 | 10.1128/jb.142.3.836-842.1980 | 10.3390/ijms25137009 | Screening of the PA14NR Transposon Mutant Library Identifies Genes Involved in R |
| 39005118 | 10.3390/molecules25122905 | 10.2174/0113892010307146240626080746 | Cancer Antibody Engineering: Comparison of Mammalian, Yeast, Bacterial, Plants,  |
| 39009827 | 10.1126/science.abf3067 | 10.1038/s44320-024-00055-4 | Proteome-scale characterisation of motif-based interactome rewiring by disease m |
| 39012113 | 10.1093/nar/gkab1107 | 10.1128/spectrum.00915-24 | Distinct prophage gene profiles of Staphylococcus aureus strains from atopic der |
| 39012882 | 10.1038/s41598-024-52192-3 | 10.1371/journal.pone.0307079 | Bacteriophages isolated from mouse feces attenuates pneumonia mice caused by Pse |
| 39023219 | 10.1038/s41396-021-01178-4 | 10.1093/ismejo/wrae134 | Dynamics of CRISPR-mediated virus-host interactions in the human gut microbiome. |
| 39026313 | 10.1136/gutjnl-2021-325413 | 10.1186/s40168-024-01832-x | Gut virome-wide association analysis identifies cross-population viral signature |
| 39028612 | 10.1056/NEJMc1902336 | 10.1093/cei/uxae060 | Screening and anti-angiogenesis activity of Chiloscyllium plagiosum anti-human V |
| 39029281 | 10.1038/s41551-024-01227-1 | 10.1016/j.sbi.2024.102878 | Dynamics in Cre-loxP site-specific recombination. |
| 39029888 | 10.1038/nmeth.4193 | 10.1016/j.jmb.2024.168713 | Structure of the Bacteriophage PhiKZ Non-virion RNA Polymerase Transcribing from |
| 39037053 | 10.1074/jbc.M510026200 | 10.1021/acs.biochem.4c00225 | Exploring the Effects of Intersubunit Interface Mutations on Virus-Like Particle |
| 39037231 | 10.1002/pro.3235 | 10.1128/mbio.01804-24 | Exploiting the Affimer platform against influenza A virus. |
| 39037288 | 10.1101/2023.04.30.538883 | 10.1128/mbio.01536-24 | A natural ANI gap that can define intra-species units of bacteriophages and othe |
| 39039289 | 10.1016/j.omtn.2022.07.024 | 10.1038/s44318-024-00158-6 | T4 DNA polymerase prevents deleterious on-target DNA damage and enhances precise |
| 39039580 | 10.1093/femsle/fnw002 | 10.1186/s13104-024-06864-y | Isolation of lytic bacteriophages and their relationships with the adherence gen |
| 39045774 | 10.1038/s41426-018-0169-z | 10.1089/fpd.2024.0023 | Therapeutic Phage Candidates for Targeting Prevalent Sequence Types of Carbapene |
| 39046960 | 10.1128/IAI.00593-10 | 10.1371/journal.pone.0302243 | Mosaic and cocktail capsid-virus-like particle vaccines for induction of antibod |
| 39047021 | 10.1371/journal.ppat.1009606 | 10.1371/journal.ppat.1012378 | Bacteriophage-driven emergence and expansion of Staphylococcus aureus in rodent  |
| 39052320 | 10.1038/s41522-019-0113-6 | 10.1093/ismejo/wrae135 | Divergent molecular strategies drive evolutionary adaptation to competitive fitn |
| 39055914 | 10.1139/cjm-2017-0740 | 10.1016/j.isci.2024.110210 | Development of the CRISPR-Cas12a system for editing of Pseudomonas aeruginosa ph |
| 39056544 | 10.7554/eLife.78633 | 10.1002/iid3.1353 | Development and characterization of a multimeric recombinant protein using the s |
| 39060226 | 10.1093/bioinformatics/bti553 | 10.1038/s41467-024-50484-w | Genomic insights into the 2022-2023Vibrio cholerae outbreak in Malawi. |
| 39063099 | 10.1111/srt.12436 | 10.3390/ijms25147860 | Wrinkle-Improving Effect of Novel Peptide That Binds to Nicotinic Acetylcholine  |
| 39066163 | 10.3390/v15020427 | 10.3390/v16071000 | Combinations of Bacteriophage Are Efficacious against Multidrug-Resistant Pseudo |
| 39066209 | 10.1038/s42003-023-04710-8 | 10.3390/v16071047 | Phage-Mediated Digestive Decolonization in a Gut-On-A-Chip Model: A Tale of Gut- |
| 39066214 | 10.1038/s41551-018-0263-5 | 10.3390/v16071051 | Pseudomonas aeruginosa Bacteriophages and Their Clinical Applications. |
| 39066242 | 10.1016/j.chom.2017.06.018 | 10.3390/v16071080 | Phage Therapy in a Burn Patient Colonized with Extensively Drug-Resistant Pseudo |
| 39068184 | 10.7717/peerj.9460 | 10.1038/s41467-024-50777-0 | Phylogeny and disease associations of a widespread and ancient intestinal bacter |
| 39068518 | 10.1093/cid/ciad475 | 10.1080/19490976.2024.2380747 | Bacteriophages from treatment-naïve type 2 diabetes individuals drive an inflamm |
| 39072625 | 10.1128/msphere.00080-22 | 10.1128/jcm.00743-24 | A single-layer spot assay for easy, fast, and high-throughput quantitation of ph |
| 39072666 | 10.7554/eLife.73679 | 10.1128/cmr.00044-24 | Pharmacokinetics and pharmacodynamics of bacteriophage therapy: a review with a  |
| 39074617 | 10.1128/cmr.00138-00118 | 10.1016/j.virusres.2024.199442 | Safety and tolerability of bronchoscopic and nebulised administration of bacteri |
| 39076360 | 10.6084/m9.figshare.c.7320460 | 10.1098/rsos.240108 | Metagenomic profiling of nasopharyngeal samples from adults with acute respirato |
| 39079958 | 10.1016/j.jconrel.2016.09.019 | 10.1038/s41419-024-06927-9 | Anti-tau single domain antibodies clear pathological tau and attenuate its toxic |
| 39082827 | 10.1007/978-1-4939-7343-9_3 | 10.1128/spectrum.00427-24 | Exploring synergistic and antagonistic interactions in phage-antibiotic combinat |
| 39085444 | 10.1007/s10059-009-0028-9 | 10.1038/s41598-024-68680-5 | A single-domain antibody library based on a stability-engineered human VH3 scaff |
| 39087354 | 10.13188/2377-9292.1000009 | 10.1002/cac2.12597 | Beyond the Gut: The intratumoral microbiome's influence on tumorigenesis and tre |
| 39091310 | 10.3390/v14020264 | 10.3389/fmicb.2024.1386830 | Characterization of the novel broad-spectrum lytic phage Phage_Pae01 and its ant |
| 39095371 | 10.1002/pro.3943 | 10.1038/s41467-024-50811-1 | Capsid structure of bacteriophage ΦKZ provides insights into assembly and stabil |
| 39096350 | 10.1128/mbio.01371-01318 | 10.1111/1751-7915.14543 | Phages produce persisters. |
| 39104636 | 10.1007/s00289-016-1840-y | 10.1002/ski2.399 | Understanding and treating diabetic foot ulcers: Insights into the role of cutan |
| 39106212 | 10.1038/s41598-023-34586-x | 10.1080/19490976.2024.2387144 | Phage lysins for intestinal microbiome modulation: current challenges and enabli |
| 39110680 | 10.1093/bioinformatics/btaa250 | 10.1371/journal.pbio.3002746 | Comprehensive blueprint of Salmonella genomic plasticity identifies hotspots for |
| 39113562 | 10.1007/s002800050995 | 10.1080/19420862.2024.2387240 | Discovery of a novel highly specific, fully human PSCA antibody and its applicat |
| 39119204 | 10.1073/pnas.2018329118 | 10.1089/phage.2023.0022 | Tradeoffs Between Evolved Phage Resistance and Antibiotic Susceptibility in a Hi |
| 39120285 | 10.1016/j.bbamem.2013.03.016 | 10.3390/cells13151254 | Globoside Is an Essential Intracellular Factor Required for Parvovirus B19 Endos |
| 39125718 | 10.1001/jama.2019.0510 | 10.3390/ijms25158148 | Advanced Vibrational Spectroscopy and Bacteriophages Team Up: Dynamic Synergy fo |
| 39125890 | 10.1164/ajrccm-conference.2024.209.1_MeetingAbstracts.A6808 | 10.3390/ijms25158321 | Phage Therapy: An Alternative Approach to Combating Multidrug-Resistant Bacteria |
| 39132840 | 10.1093/bioinformatics/btab007 | 10.1080/19490976.2024.2379440 | Gene content, phage cycle regulation model and prophage inactivation disclosed b |
| 39136463 | 10.1128/iai.00605-19 | 10.1128/aac.00650-24 | Bacteriophage therapy reduces Staphylococcus aureus in a porcine and human ex vi |
| 39141729 | 10.1101/2022.07.26.501571 | 10.1126/sciadv.adn3316 | Long-read sequencing reveals extensive gut phageome structural variations driven |
| 39143239 | 10.7554/eLife.42166 | 10.1038/s44318-024-00195-1 | Structure and replication of Pseudomonas aeruginosa phage JBD30. |
| 39143367 | 10.3389/fmicb.2018.00850 | 10.1007/s00203-024-04106-0 | Characterization of a novel phage against multidrug-resistant Klebsiella pneumon |
| 39146931 | 10.1021/acs.bioconjchem.2c00220 | 10.1016/j.str.2024.07.014 | Engineering of pH-dependent antigen binding properties for toxin-targeting IgG1  |
| 39157733 | 10.1080/07388551.2020.1785385 | 10.2147/IJN.S472038 | Strategies for Targeting Peptide-Modified Exosomes and Their Applications in the |
| 39158623 | 10.1128/msystems.00084-22 | 10.1007/s12033-024-01249-9 | Deeper Exploration of Gut Microbiome: Profile of Resistome, Virome and Viral Aux |
| 39158799 | 10.3389/fmicb.2017.00227 | 10.1007/s10096-024-04920-w | An insight on the powerful of bacterial quorum sensing inhibition. |
| 39160380 | 10.1016/j.watres.2013.03.025 | 10.1007/s12560-024-09609-z | Comparative Removal of Poliovirus, Rotavirus SA11 and MS2 Coliphage by Point-of- |
| 39160541 | 10.1371/journal.pone.0243947 | 10.1186/s12985-024-02450-7 | The potential use of bacteriophages as antibacterial agents against Klebsiella p |
| 39160615 | 10.1016/j.jbi.2019.103208 | 10.1186/s40168-024-01870-5 | Defining Vaginal Community Dynamics: daily microbiome transitions, the role of m |
| 39163262 | 10.1128/JVI.00165-21 | 10.1093/protein/gzae013 | An engineered NKp46 antibody for construction of multi-specific NK cell engagers |
| 39164718 | 10.1021/acs.biochem.8b00341 | 10.1186/s12941-024-00734-y | Proteomic analysis of carbapenem-resistant Klebsiella pneumoniae outer membrane  |
| 39166873 | 10.1038/s41591-021-01552-x | 10.1128/msystems.00434-24 | Gut phageome in Mexican Americans: a population at high risk for metabolic dysfu |
| 39166874 | 10.1126/science.288.5469.1251 | 10.1128/msystems.00801-24 | Phage-mediated resolution of genetic conflict alters the evolutionary trajectory |
| 39167154 | 10.1177/1534734619881076 | 10.1007/s11033-024-09870-2 | Antimicrobial resistance: use of phage therapy in the management of resistant in |
| 39167701 | 10.1128/jb.188.7.2711-2714.2006 | 10.1080/19490976.2024.2390720 | Role of bacteriophages in shaping gut microbial community. |
| 39168282 | 10.1101/2023.08.21.23294253 | 10.1016/j.mcpro.2024.100831 | Phage Immunoprecipitation and Sequencing-a Versatile Technique for Mapping the A |
| 39169307 | 10.1158/1078-0432.CCR-21-1888 | 10.1186/s12865-024-00636-w | Antagonist anti-LIF antibody derived from naive human scFv phage library inhibit |
| 39171268 | 10.1093/cid/ciad514 | 10.3389/fmicb.2024.1386245 | A comparison of phage susceptibility testing with two liquid high-throughput met |
| 39172643 | 10.1128/JVI.05217-11 | 10.1080/19490976.2024.2392876 | Fecal virus-like particles are sufficient to reduce necrotizing enterocolitis. |
| 39174532 | 10.1093/nar/gkab1038 | 10.1038/s41467-024-51617-x | Control of lysogeny and antiphage defense by a prophage-encoded kinase-phosphata |
| 39181880 | 10.1002/ddr.20265 | 10.1038/s41467-024-51610-4 | Proximity-driven site-specific cyclization of phage-displayed peptides. |
| 39185427 | 10.1021/acs.jmedchem.1c00943 | 10.3389/fimmu.2024.1437886 | An anti-sortilin affibody-peptide fusion inhibits sortilin-mediated progranulin  |
| 39187718 | 10.1186/s12859-019-3019-7 | 10.1038/s41586-024-07809-y | Birth of protein folds and functions in the virome. |
| 39189763 | 10.1016/0378-1119(94)90227-5 | 10.1128/spectrum.01054-24 | Evaluation of human antibodies from vaccinated volunteers for protection against |
| 39192463 | 10.1080/19420862.2021.1980942 | 10.1080/19420862.2024.2394230 | A next-generation Fab library platform directly yielding drug-like antibodies wi |
| 39194291 | 10.7717/peerj.3243 | 10.1128/spectrum.00254-24 | Targeted phage hunting to specific Klebsiella pneumoniae clinical isolates is an |
| 39194631 | 10.1111/jam.15274 | 10.3390/bios14080402 | A Bacteriophage Protein-Based Impedimetric Electrochemical Biosensor for the Det |
| 39194910 | 10.1126/sciadv.aay9634 | 10.3390/jof10080585 | The Expanding Mycovirome of Aspergilli. |
| 39195859 | 10.1038/s41596-018-0025-6 | 10.1038/s44161-024-00525-w | An engineered human cardiac tissue model reveals contributions of systemic lupus |
| 39196527 | 10.1074/jbc.M109.029843 | 10.1134/S1607672924600416 | Error-Prone DNA Synthesis on Click-Ligated Templates. |
| 39197447 | 10.1038/s41564-022-01258-x | 10.1016/j.cell.2024.07.057 | Animal and bacterial viruses share conserved mechanisms of immune evasion. |
| 39201374 | 10.1101/2021.06.14.448389 | 10.3390/ijms25168690 | Dietary Effects on the Gut Phageome. |
| 39204211 | 10.1111/j.1365-2958.2005.04956.x | 10.3390/pathogens13080610 | Comparative Genomic Analysis of Prophages in Human Vaginal Isolates of Streptoco |
| 39204419 | 10.1016/j.clae.2023.101819 | 10.3390/pharmaceutics16081074 | The Role of Pseudomonas aeruginosa in the Pathogenesis of Corneal Ulcer, Its Ass |
| 39205249 | 10.3389/fmicb.2022.825828 | 10.3390/v16081275 | Characterization and Anti-Biofilm Activity of Lytic Enterococcus Phage vB_Efs8_K |
| 39209859 | 10.1111/tpj.12316 | 10.1038/s41467-024-51912-7 | Bacterial cell surface characterization by phage display coupled to high-through |
| 39209878 | 10.1021/acs.biomac.7b00979 | 10.1038/s41522-024-00552-2 | Combination of bacteriophages and vancomycin in a co-delivery hydrogel for local |
| 39210957 | 10.1002/imt2.186 | 10.21769/BioProtoc.5050 | Extraction of Bacterial Membrane Vesicle and Phage Complex by Density Gradient U |
| 39215044 | 10.1093/nar/gkab1038 | 10.1038/s41467-024-51781-0 | Tumor-agnostic cancer therapy using antibodies targeting oncofetal chondroitin s |
| 39224703 | 10.1016/j.drup.2024.101083 | 10.3389/fcimb.2024.1442062 | Evaluation of phage-based decontamination in respiratory intensive care unit env |
| 39224822 | 10.1016/j.bbrc.2020.09.131 | 10.7717/peerj.17846 | Screening and affinity optimization of single domain antibody targeting the SARS |
| 39227770 | 10.1038/s41591-021-01403-9 | 10.1186/s12866-024-03474-3 | Antibacterial efficacy of mycobacteriophages against virulent Mycobacterium tube |
| 39228894 | 10.3389/fcimb.2019.00146 | 10.3389/fcimb.2024.1455259 | Development of a novel sandwich immunoassay based on targeting recombinant Franc |
| 39230264 | 10.1101/2024.01.16.575879 | 10.1128/msystems.00171-24 | Metapopulation model of phage therapy of an acute Pseudomonas aeruginosa lung in |
| 39230289 | 10.1016/S0022-2836(05)80360-2 | 10.1128/mbio.03206-23 | Improving viral annotation with artificial intelligence. |
| 39237829 | 10.1016/j.jpba.2020.113415 | 10.1038/s41596-024-01040-9 | Construction and utilization of a new generation of bacteriophage-based particle |
| 39237903 | 10.3390/v13122414 | 10.1186/s12879-024-09814-y | Proportion of patients with prosthetic joint infection eligible for adjuvant pha |
| 39240286 | 10.1152/physrev.00030.2013 | 10.1007/s00284-024-03875-7 | Immunomodulation in Non-traditional Therapies for Methicillin-resistant Staphylo |
| 39248470 | 10.1093/nar/gkac1003 | 10.1128/msystems.00850-24 | Potential of training of anti-Staphylococcus aureus therapeutic phages against S |
| 39248472 | 10.1182/blood-2007-06-095398 | 10.1128/aac.00829-24 | Zebrafish as an effective model for evaluating phage therapy in bacterial infect |
| 39253479 | 10.1128/jb.186.21.7262-7272.2004 | 10.1101/2024.08.26.609590 | AcrIF11 is a potent CRISPR-specific ADP-ribosyltransferase encoded by phage and  |
| 39253689 | 10.1016/S0923-2508(03)00071-8 | 10.1016/j.ijregi.2024.100415 | Simultaneous clonal spread of NDM-1-producing Pseudomonas aeruginosa ST773 from  |
| 39254035 | 10.1093/bioinformatics/btr039 | 10.1128/msystems.00941-24 | Characterization of the carbapenem-resistant Acinetobacter baumannii clinical re |
| 39254211 | 10.3389/fmicb.2023.1172635 | 10.1042/EBC20240024 | Phage-specific antibodies: are they a hurdle for the success of phage therapy? |
| 39254722 | 10.1038/s41564-022-01207-8 | 10.1007/s00264-024-06295-1 | Bacteriophage therapy as an innovative strategy for the treatment of Periprosthe |
| 39256307 | 10.1186/s12929-022-00806-1 | 10.1007/s11262-024-02103-5 | Isolation, characterization, and potential application of Acinetobacter baumanni |
| 39263065 | 10.1128/jb.188.3.1184-1187.2006 | 10.1016/j.heliyon.2024.e36243 | Characterization and genomic analysis of PA-56 Pseudomonas phage from Istanbul,  |
| 39264563 | 10.14202/vetworld.2022.2856-2869 | 10.1007/s10517-024-06209-6 | Isolation and Characterization of Salmonella Bacteriophages as Potential Agents  |
| 39268483 | 10.3390/v14020342 | 10.3389/fcimb.2024.1421724 | Isolation and characterization of two novel bacteriophages against carbapenem-re |
| 39268487 | 10.3389/froh.2021.774115 | 10.3389/fcimb.2024.1397675 | Delivery mode and maternal gestational diabetes are important factors in shaping |
| 39273250 | 10.1093/infdis/jiac389 | 10.3390/ijms25179301 | The Biological Characteristics of Mycobacterium Phage Henu3 and the Fitness Cost |
| 39273419 | 10.1021/acsbiomaterials.4c00972 | 10.3390/ijms25179472 | Insights into the Preparation of and Evaluation of the Bactericidal Effects of P |
| 39274911 | 10.1056/NEJM197408012910507 | 10.3390/molecules29174065 | Agents Targeting the Bacterial Cell Wall as Tools to Combat Gram-Positive Pathog |
| 39276365 | 10.1016/j.xpro.2021.101101 | 10.1093/protein/gzae014 | Engineered FHA domains can bind to a variety of Phosphothreonine-containing pept |
| 39282405 | 10.1128/mbio.01304-16 | 10.1101/2024.09.07.611814 | Multi-strain phage induced clearance of bacterial infections. |
| 39287442 | 10.1002/0471250953.bi1112s47 | 10.1128/mbio.02359-24 | Deciphering transcript architectural complexity in bacteria and archaea. |
| 39287445 | 10.1093/nar/gkab301 | 10.1128/mbio.00111-24 | Sporadic phage defense in epidemic Vibrio cholerae mediated by the toxin-antitox |
| 39289529 | 10.1007/978-1-60327-164-6_7 | 10.1038/s41587-024-02384-z | An experimental census of retrons for DNA production and genome editing. |
| 39290977 | 10.1128/aem.00468-21 | 10.3389/fcimb.2024.1434397 | Optimization of bacteriophage therapy for difficult-to-treat musculoskeletal inf |
| 39296778 | 10.1126/science.1258096 | 10.1093/ismeco/ycae105 | A nanoluciferase-encoded bacteriophage illuminates viral infection dynamics of P |
| 39300324 | 10.1002/jcc.20084 | 10.1038/s41564-024-01793-9 | Specialized Listeria monocytogenes produce tailocins to provide a population-lev |
| 39301510 | 10.1126/scitranslmed.aau9748 | 10.1093/pnasnexus/pgae390 | The lysogenic filamentous Pseudomonas bacteriophage phage Pf slows mucociliary t |
| 39306818 | 10.3390/pharmaceutics14020427 | 10.1007/s00284-024-03896-2 | The Hydrophobic Stabilization of Pseudomonas aeruginosa Bacteriophage F8 and the |
| 39307422 | 10.1002/0471140864.ps1210s64 | 10.1016/j.mcpro.2024.100844 | Insights Into Glycobiology and the Protein-Glycan Interactome Using Glycan Micro |
| 39311906 | 10.1038/srep30257 | 10.1007/s00204-024-03869-1 | Neutralizing chimeric heavy-chain antibody targeting the L-HN domain of Clostrid |
| 39313510 | 10.1002/pro.3280 | 10.1038/s41467-024-52238-0 | Core and accessory genomic traits of Vibrio cholerae O1 drive lineage transmissi |
| 39315811 | 10.1016/j.jmb.2022.167505 | 10.1128/msphere.00454-24 | Preexisting cell state rather than stochastic noise confers high or low infectio |
| 39316269 | 10.11654/jaes.2017-0549 | 10.1007/s10653-024-02239-1 | Characteristics of tetracycline antibiotic resistance gene enrichment and migrat |
| 39320361 | 10.1371/journal.pone.0243947 | 10.1099/jmm.0.001895 | Current status of clinical trials for phage therapy. |
| 39322758 | 10.1038/s41564-022-01239-0 | 10.1038/s44318-024-00248-5 | Toxin-mediated depletion of NAD and NADP drives persister formation in a human p |
| 39325139 | 10.1016/j.bpj.2023.11.1743 | 10.1007/s00216-024-05552-x | Biosensing strategies using recombinant luminescent proteins and their use for f |
| 39325826 | 10.1002/pro.3235 | 10.1371/journal.ppat.1012600 | Structure-guided in vitro evolution of nanobodies targeting new viral variants. |
| 39332682 | 10.1128/aac.45.4.1151-1161.2001 | 10.1016/j.virusres.2024.199473 | Isolation and characterization of lytic bacteriophage vB_KpnP_23: A promising an |
| 39333115 | 10.1093/bioinformatics/bty053 | 10.1038/s41467-024-52450-y | Prophage-encoded antibiotic resistance genes are enriched in human-impacted envi |
| 39334975 | 10.1213/ANE.0000000000002864 | 10.3390/antibiotics13090800 | Bacteriophage Therapy on an In Vitro Wound Model and Synergistic Effects in Comb |
| 39336556 | 10.1093/ecco-jcc/jjac064 | 10.3390/medicina60091515 | Insights into the Two Most Common Cancers of Primitive Gut-Derived Structures an |
| 39337427 | 10.3389/fmicb.2023.1250848 | 10.3390/ijms25189938 | Recent Advances and Mechanisms of Phage-Based Therapies in Cancer Treatment. |
| 39338470 | 10.1073/pnas.1919888117 | 10.3390/microorganisms12091795 | The Potential of Phage Treatment to Inactivate Planktonic and Biofilm-Forming Ps |
| 39338555 | 10.3389/fmed.2023.1199657 | 10.3390/microorganisms12091880 | Diversification of Pseudomonas aeruginosa Biofilm Populations under Repeated Pha |
| 39339825 | 10.1038/srep26717 | 10.3390/v16091348 | Phage against the Machine: The SIE-ence of Superinfection Exclusion. |
| 39343973 | 10.1017/ice.2020.11 | 10.1186/s13756-024-01473-7 | Evaluation of an automated far ultraviolet-C light technology for decontaminatio |
| 39345202 | 10.1016/j.scitotenv.2023.168461 | 10.1128/aem.01353-24 | Challenges and opportunities of phage therapy for Klebsiella pneumoniae infectio |
| 39351325 | 10.1016/j.phymed.2022.154346 | *(none)* | Intricate Crosstalk Between Food Allergens, Phages, Bacteria, and Eukaryotic Hos |
| 39353939 | 10.1021/acs.nanolett.9b04446 | 10.1038/s41467-024-52752-1 | Integrative structural analysis of Pseudomonas phage DEV reveals a genome ejecti |
| 39355265 | 10.1371/journal.pcbi.1005595 | 10.3389/fcimb.2024.1354681 | Case report: Personalized triple phage-antibiotic combination therapy to rescue  |
| 39361673 | 10.1002/jcc.21334 | 10.1371/journal.pone.0297338 | Phage libraries screening on P53: Yield improvement by zinc and a new parasites- |
| 39361891 | 10.1038/ncomms15892 | 10.1093/ismejo/wrae192 | Recruitment of complete crAss-like phage genomes reveals their presence in chick |
| 39362854 | 10.1128/JCM.05556-11 | 10.1038/s41467-024-52595-w | Targeting Pseudomonas aeruginosa biofilm with an evolutionary trained bacterioph |
| 39363262 | 10.1109/TNNLS.2017.2676130 | 10.1186/s12951-024-02881-y | Truncated M13 phage for smart detection of E. coli under dark field. |
| 39367826 | 10.1001/jama.2020.4806 | 10.1177/21650799241273972 | Wipe Disinfection of Reusable Elastomeric Half-Mask Respirators for Health Care  |
| 39368473 | 10.1128/iai.00207-11 | 10.1016/j.chom.2024.09.004 | Rapid design of bacteriophage cocktails to suppress the burden and virulence of  |
| 39369022 | 10.1101/gr.6649807 | 10.1038/s41392-024-01995-x | The phage anti-restriction induced system: new insights into bacterial immunity  |
| 39370451 | 10.1038/s41598-022-11382-7 | 10.1038/s42003-024-06985-x | Cryo-EM analysis of Pseudomonas phage Pa193 structural components. |
| 39373478 | 10.1021/acs.bioconjchem.6b00638 | 10.1128/spectrum.04269-23 | The development of single-domain VHH nanobodies that target the Candida albicans |
| 39377596 | 10.3390/v9040070 | 10.1128/mra.00684-24 | Complete genome sequences of three Pseudomonas aeruginosa jumbo bacteriophages d |
| 39377811 | 10.1158/1535-7163.mct-16-0825 | 10.1007/s00259-024-06941-1 | Preclinical evaluation and pilot clinical study of [68Ga]Ga-NOTA-H006 for non-in |
| 39379324 | 10.1093/nar/gkz822 | 10.1080/19420862.2024.2408344 | Seq2scFv: a toolkit for the comprehensive analysis of display libraries from lon |
| 39379373 | 10.1002/pro.3943 | 10.1038/s41467-024-52732-5 | PlzR regulates type IV pili assembly in Pseudomonas aeruginosa via PilZ binding. |
| 39382702 | 10.1128/IAI.68.10.5679-5689.2000 | 10.1007/s00253-024-13317-w | Campycins are novel broad-spectrum antibacterials killing Campylobacter jejuni. |
| 39401247 | 10.1101/2024.03.14.585103 | 10.1371/journal.pcbi.1012522 | Inference and design of antibody specificity: From experiments to models and bac |
| 39402718 | 10.1038/nmeth.1492 | 10.1080/19420862.2024.2410316 | CD200R1 immune checkpoint blockade by the first-in-human anti-CD200R1 antibody 2 |
| 39408641 | 10.1021/ct300203w | 10.3390/ijms251910311 | Phage Display Revealed the Complex Structure of the Epitope of the Monoclonal An |
| 39412263 | 10.1126/science.aba0372 | 10.1128/msphere.00398-24 | mSphere of Influence: Revisiting the central dogma, again! |
| 39412595 | 10.1073/pnas.061038398 | 10.1007/s12602-024-10374-5 | Characterization of a Peptidoglycan-Degrading Protein: Biochemical and Antimicro |
| 39414952 | 10.3389/fimmu.2021.631226 | 10.1038/s41598-024-76163-w | A self-adjuvanted VLPs-based Covid-19 vaccine proven versatile, safe, and highly |
| 39415074 | 10.1038/s41598-018-19439-2 | 10.1038/s41596-024-01070-3 | Measuring carbohydrate recognition profile of lectins on live cells using liquid |
| 39417290 | 10.1038/s41564-019-0666-4 | 10.1042/EBC20240020 | Translational research priorities for bacteriophage therapeutics. |
| 39418095 | 10.1038/s41467-019-12825-y | 10.1099/mgen.0.001297 | Revisiting typing systems for group B Streptococcus prophages: an application in |
| 39420033 | 10.1093/nar/gkw253 | 10.1038/s41467-024-53454-4 | The phageome of patients with ulcerative colitis treated with donor fecal microb |
| 39420423 | 10.1371/journal.pmed.0030484 | 10.1186/s40168-024-01925-7 | Alterations of the gut microbiome in HIV infection highlight human anelloviruses |
| 39421627 | 10.1016/j.trsl.2020.03.010 | 10.17691/stm2024.16.1.05 | Evaluation of the Feasibility of Using Commercial Wound Coatings as a Carrier Ma |
| 39421990 | 10.3389/fmicb.2019.00438 | 10.2174/0109298673316661241002060518 | Resilience Against Resistance: Exploring Cutting-edge Therapies for Methicillin- |
| 39424745 | 10.1080/10717544.2016.1189625 | 10.1007/s11030-024-11007-3 | Design and investigation of novel iridoid-based peptide conjugates for targeting |
| 39425223 | 10.1002/med.21572 | 10.1186/s12985-024-02510-y | The potential use of bacteriophages as antibacterial agents in dental infection. |
| 39425798 | 10.3390/v10040174 | 10.1007/s00705-024-06149-6 | Isolation and characterization of Yersinia phage fMtkYen3-01. |
| 39428565 | 10.1038/srep15877 | 10.3201/eid3011.241068 | Invasive Group A Streptococcus Hypervirulent M1UK Clone, Canada, 2018-2023. |
| 39431820 | 10.1016/j.cell.2021.02.030 | 10.1128/jvi.01102-24 | Comprehensive phage display viral antibody profiling using VirScan: potential ap |
| 39433212 | 10.26434/chemrxiv-2024-wnx5w | 10.1016/j.mcpro.2024.100865 | Nanobodies: From High-Throughput Identification to Therapeutic Development. |
| 39435185 | 10.1038/s41598-023-42505-3 | 10.3389/fcimb.2024.1428637 | Bacteriophage-mediated approaches for biofilm control. |
| 39435664 | 10.1007/978-1-62703-050-2_16 | 10.1172/jci.insight.181309 | The contribution of neutrophils to bacteriophage clearance and pharmacokinetics  |
| 39439944 | 10.1016/j.diagmicrobio.2023.115955 | 10.3389/fmicb.2024.1454618 | The antibacterial activity of a novel highly thermostable endolysin, LysKP213, a |
| 39440986 | 10.1097/CCM.0000000000001271 | 10.1128/spectrum.01781-24 | Effects of the combination of anti-PcrV antibody and bacteriophage therapy in a  |
| 39443305 | 10.1007/s12223-021-00946-1 | 10.1007/s00203-024-04168-0 | Bacteriophage entrapment strategies for the treatment of chronic wound infection |
| 39445393 | 10.1038/s41392-023-01579-1 | 10.1021/acs.analchem.4c04162 | Exploring the Impact of In Vitro-Transcribed mRNA Impurities on Cellular Respons |
| 39449043 | 10.1093/bioinformatics/btaa213 | 10.1186/s40168-024-01935-5 | A single-stranded based library preparation method for virome characterization. |
| 39450991 | 10.1038/s41467-024-45757-3 | 10.1093/ismejo/wrae218 | Chronic exposure to polycyclic aromatic hydrocarbons alters skin virome composit |
| 39451702 | 10.3390/bios14100458 | 10.3390/bios14100489 | Non-Invasive On-Off Fluorescent Biosensor for Endothelial Cell Detection. |
| 39452183 | 10.3389/fmicb.2019.01674 | 10.3390/antibiotics13100916 | Phage-Antibiotic Combination Therapy against Recurrent Pseudomonas Septicaemia i |
| 39452768 | 10.3389/fmicb.2022.845500 | 10.3390/pathogens13100896 | Phage-Based Therapy in Combination with Antibiotics: A Promising Alternative aga |
| 39455687 | 10.1111/j.1467-8276.2006.00913.x | 10.1038/s41598-024-75721-6 | Consumer acceptance of bacteriophage technology for microbial control. |
| 39455951 | 10.1038/s41598-024-54469-z | 10.1186/s12879-024-10081-0 | Synergistic effects of bacteriophage cocktail and antibiotics combinations again |
| 39456772 | 10.2307/2529826 | 10.3390/ijms252010988 | Metagenomic Study Reveals Phage-Bacterial Interactome Dynamics in Gut and Oral M |
| 39457603 | 10.1016/j.chom.2019.05.001 | 10.3390/biomedicines12102291 | Biofilm Prevention and Removal in Non-Target Pseudomonas Strain by Siphovirus-li |
| 39459925 | 10.3390/antibiotics10050475 | 10.3390/v16101592 | Isolation and Antibiofilm Activity of Bacteriophages against Cutibacterium acnes |
| 39464247 | 10.12688/f1000research.52540.3 | 10.12688/f1000research.77421.3 | The first report on detecting SARS-CoV-2 inside bacteria of the human gut microb |
| 39466358 | 10.3390/antib12030052 | 10.1007/s12539-024-00664-5 | ABTrans: A Transformer-based Model for Predicting Interaction between Anti-Aβ An |
| 39467695 | 10.1016/j.jviromet.2017.08.006 | 10.4014/jmb.2406.06001 | Distributions of Fecal Indicators at Aquaculture Areas in a Bay of Republic of K |
| 39467702 | 10.1016/j.biopha.2020.110648 | 10.4014/jmb.2408.08026 | Innovative Bacterial Therapies and Genetic Engineering Approaches in Colorectal  |
| 39468301 | 10.1038/s41387-023-00235-5 | 10.1038/s44321-024-00149-4 | Diagnosing and engineering gut microbiomes. |
| 39468354 | 10.1038/srep14802 | 10.1038/s41565-024-01800-4 | Filamentous phages as tumour-targeting immunotherapeutic bionanofibres. |
| 39470273 | 10.1016/j.ijantimicag.2015.04.005 | 10.1128/spectrum.01527-24 | Phages ZC01 and ZC03 require type-IV pilus for Pseudomonas aeruginosa infection  |
| 39470283 | 10.1371/journal.pone.0134512 | 10.1128/spectrum.00679-24 | It takes two to tango: Preserving daptomycin efficacy against daptomycin-resista |
| 39472798 | 10.1016/j.meegid.2020.104635 | 10.1186/s12879-024-09921-w | Whole-genome sequencing-based analysis of Brucella species isolated from ruminan |
| 39474429 | 10.1093/clinchem/27.3.493 | 10.3389/fimmu.2024.1480091 | Making the effect visible - OX40 targeting nanobodies for in vivo imaging of act |
| 39474820 | 10.5580/b43 | 10.1021/acs.analchem.4c05177 | CRISPR/Cas9-Mediated Genome Editing of T4 Bacteriophage for High-Throughput Anti |
| 39475220 | 10.3389/fmicb.2020.00327 | 10.1042/EBC20240012 | Phage diversity in One Health. |
| 39475242 | 10.3389/fmicb.2020.591866 | 10.1128/mbio.02970-24 | Trehalose polyphleates participate in Mycobacterium abscessus fitness and pathog |
| 39475266 | 10.1080/15265161.2020.1795516 | 10.1042/EBC20240013 | Considerations for prioritising clinical research using bacteriophage. |
| 39475284 | 10.1016/j.virol.2021.09.004 | 10.1128/aem.00884-24 | Directed evolution of bacteriophages: thwarted by prolific prophage. |
| 39482746 | 10.1128/spectrum.01781-24 | 10.1186/s40560-024-00759-7 | Current status of bacteriophage therapy for severe bacterial infections. |
| 39491772 | 10.3390/ph16121638 | 10.1016/j.virusres.2024.199491 | Characterization of two lytic bacteriophages infecting carbapenem-resistant clin |
| 39492989 | 10.1101/gr.074492.107 | 10.3389/fcimb.2024.1412408 | Genomic and phenotypic characterization of a Clostridioides difficile strain of  |
| 39501333 | 10.1186/s13568-019-0810-9 | 10.1186/s12985-024-02553-1 | Comprehensive retrospect and future perspective on bacteriophage and cancer. |
| 39503487 | 10.1007/s12275-021-1394-z | 10.1128/aac.00565-24 | A peptide targeting outer membrane protein A of Acinetobacter baumannii exhibits |
| 39508962 | 10.1016/J.ENZMICTEC.2019.05.006 | 10.1007/s12602-024-10394-1 | The Synergistic and Chimeric Mechanism of Bacteriophage Endolysins: Opportunitie |
| 39511647 | 10.1038/srep26717 | 10.1186/s12985-024-02556-y | Characterization of phage HZY2308 against Acinetobacter baumannii and identifica |
| 39512587 | 10.1016/j.biopha.2020.111034 | 10.3389/fcimb.2024.1462620 | Phage-encoded depolymerases as a strategy for combating multidrug-resistant Acin |
| 39513860 | 10.1038/s41586-019-1451-5 | 10.3390/cells13211753 | A Virome and Proteomic Analysis of Placental Microbiota in Pregnancies with and  |
| 39516905 | 10.1111/lam.13663 | 10.1186/s12985-024-02554-0 | Characterization and complete genome sequence of highly lytic phage active again |
| 39518670 | 10.1002/advs.202103262 | 10.3390/jcm13216530 | Therapeutic Interventions for Pseudomonas Infections in Cystic Fibrosis Patients |
| 39518974 | 10.1002/ski2.93 | 10.3390/ijms252111422 | The Role of the Skin Microbiome in Acne: Challenges and Future Therapeutic Oppor |
| 39527365 | 10.1128/AEM.67.4.1558-1564.2001 | 10.1007/s13353-024-00918-4 | What, how, and why? - anti-EHEC phages and their application potential in medici |
| 39530158 | 10.1038/s41564-024-01705-x | 10.1080/22221751.2024.2420737 | The synergistic effect between phages and Ceftolozane/Tazobactam in Pseudomonas  |
| 39535660 | 10.3390/cancers13051037 | 10.1007/s12013-024-01608-y | Advancements in Cancer Therapy: Mycoviruses and Their Oncolytic Potential. |
| 39541273 | 10.1128/JB.00479-18 | 10.1371/journal.pone.0311630 | Development of a lambda Red based system for gene deletion in Chlamydia. |
| 39543151 | 10.1128/AAC.00952-15 | 10.1038/s41522-024-00603-8 | A Klebsiella-phage cocktail to broaden the host range and delay bacteriophage re |
| 39545100 | 10.1016/S1473-3099(21)00612-5 | 10.1155/2024/6252415 | Phage Therapy Against Antibiotic-Resistant and Multidrug-Resistant Infections In |
| 39545771 | 10.3389/fcimb.2023.1149848 | 10.1080/20415990.2024.2426824 | Phage therapeutic delivery methods and clinical trials for combating clinically  |
| 39549237 | 10.1146/annurev-arplant-080620-021907 | 10.1016/j.xpro.2024.103433 | A protocol for in vivo RNA labeling and visualization in tobacco pollen tubes. |
| 39550381 | 10.1128/JVI.79.19.12608-12613.2005 | 10.1038/s41467-024-54287-x | Rational design of uncleaved prefusion-closed trimer vaccines for human respirat |
| 39551144 | 10.3390/pathogens9070559 | 10.1016/j.jbc.2024.108007 | The antibacterial activity of a prophage-encoded fitness factor is neutralized b |
| 39551578 | 10.3389/fmed.2019.00224 | 10.1136/rmdopen-2024-004743 | Fibroblast-like synoviocyte targeting antibodies are associated with failure to  |
| 39559211 | 10.1016/B978-0-12-809633-8.02352-9 | 10.1016/j.heliyon.2024.e40076 | Relative fitness of wild-type and phage-resistant pyomelanogenic P. aeruginosa a |
| 39570312 | 10.5281/zenodo.14037293 | 10.1073/pnas.2413743121 | Comprehensive deletion scan of anti-CRISPR AcrIIA4 reveals essential and dispens |
| 39571005 | 10.1371/journal.pone.0251041 | 10.1371/journal.pntd.0012122 | Comparing microbiological and molecular diagnostic tools for the surveillance of |
| 39576765 | 10.1111/j.1558-5646.2007.00205.x | 10.1371/journal.pone.0314002 | Risk of infection due to airborne virus in classroom environments lacking mechan |
| 39578508 | 10.1038/s41467-018-02875-z | 10.1038/s41598-024-79924-9 | Phage cocktail amikacin combination as a potential therapy for bacteremia associ |
| 39587339 | 10.1002/erv.2878 | 10.1038/s42255-024-01157-x | Microviridae bacteriophages influence behavioural hallmarks of food addiction vi |
| 39587720 | 10.1016/S0016-5085(23)03109-8 | 10.1080/19490976.2024.2431645 | Comparison of Crohn's disease-associated adherent-invasive Escherichia coli (AIE |
| 39588913 | 10.4049/jimmunol.1502432 | 10.1080/19420862.2024.2432403 | Targeting RGMb interactions: Discovery and preclinical characterization of poten |
| 39590014 | 10.1371/journal.pone.0204164 | 10.3390/bios14110555 | Ultra-Selective and Sensitive Fluorescent Chemosensor Based on Phage Display-Der |
| 39592862 | 10.1093/nar/gkv007 | 10.1038/s41598-024-80909-x | Multiomics analysis of Staphylococcus aureus ST239 strains resistant to virulent |
| 39594628 | 10.1681/ASN.2004080711 | 10.3390/cells13221880 | Identification and Characterization of Fully Human FOLR1-Targeting CAR T Cells f |
| 39595576 | 10.4049/jimmunol.208.Supp.117.12 | 10.3390/biom14111399 | High-Affinity Fully Human Anti-EpCAM Antibody with Biased IL-2 Exhibits Potent A |
| 39596701 | 10.2307/2408678 | 10.3390/antibiotics13111006 | Isolation and Characterization of a Novel Jumbo Phage HPP-Temi Infecting Pseudom |
| 39597505 | 10.1111/apm.12951 | 10.3390/microorganisms12112115 | Pseudomonas aeruginosa in the Frontline of the Greatest Challenge of Biofilm Inf |
| 39597735 | 10.1093/nar/gkac1168 | 10.3390/microorganisms12112346 | Isolation, Characterization, and Genome Engineering of a Lytic Pseudomonas aerug |
| 39599555 | 10.3389/fpubh.2024.1364664 | 10.3390/pathogens13111002 | Intestinal Carriage of Two Distinct stx2f-Carrying Escherichia coli Strains by a |
| 39599826 | 10.3390/antibiotics8030126 | 10.3390/v16111711 | Isolation and Characterization of a Bacteriophage with Potential for the Control |
| 39599855 | 10.1016/j.virol.2015.09.022 | 10.3390/v16111741 | Biological Characterization and Evaluation of the Therapeutic Value of Vibrio Ph |
| 39604394 | 10.5281/zenodo.14021369 | 10.1038/s41467-024-54797-8 | Multi-biome analysis identifies distinct gut microbial signatures and their cros |
| 39604533 | 10.1039/B920931J | 10.1007/s00216-024-05662-6 | Evaluating the capacity of magnetic ionic liquids for separation and concentrati |
| 39609398 | 10.1371/journal.pcbi.1010746 | 10.1038/s41467-024-53994-9 | A blueprint for broadly effective bacteriophage-antibiotic cocktails against bac |
| 39609405 | 10.1038/s41564-021-00963-3 | 10.1038/s41467-024-54666-4 | Use of epigenetically modified bacteriophage and dual beta-lactams to treat a My |
| 39609616 | 10.18637/jss.v059.i05 | 10.1038/s42003-024-07290-3 | Host DNA depletion on frozen human respiratory samples enables successful metage |
| 39611592 | 10.1073/pnas.0704662104 | 10.1042/EBC20240116 | A roadmap of isolating and investigating bacteriophage infecting human gut anaer |
| 39613338 | 10.1007/s00262-023-03489-1 | 10.1136/jitc-2024-009931 | Antecedent viral immunization and efficacy of immune checkpoint blockade: an ext |
| 39614107 | 10.1159/000319442 | 10.1038/s41598-024-80326-0 | Using X-ray velocimetry to measure lung function and assess the efficacy of a ps |
| 39632378 | 10.16288/j.yczz.20-080 | 10.1080/19490976.2024.2434675 | Omic characterizing and targeting gut dysbiosis in children with autism spectrum |
| 39636383 | 10.1002/art.42474 | 10.1007/s11926-024-01171-8 | Newer Autoantibodies and Laboratory Assessments in Myositis. |
| 39641606 | 10.3389/fmicb.2021.811157 | 10.1128/aem.01426-24 | Rapid virucidal activity of an air sanitizer against aerosolized MS2 and Phi6 ph |
| 39644414 | 10.1186/s12941-023-00567-1 | 10.1007/s00403-024-03585-x | Cutibacterium acnes bacteriophage therapy: exploring a new frontier in acne vulg |
| 39644434 | 10.1007/s00253-021-11559-6 | 10.1007/s10120-024-01568-5 | Novel affibody molecules targeting the AXL extracellular structural domain for m |
| 39656008 | 10.1890/11-1952.1 | 10.1128/spectrum.00998-24 | Dysbiosis of gut microbiota in COVID-19 is associated with intestinal DNA phage  |
| 39656022 | 10.1021/acs.jmedchem.2c01391 | 10.1021/acs.jmedchem.4c02286 | Constrained β-Hairpins Targeting the EphA4 Ligand Binding Domain. |
| 39656423 | 10.1186/s12985-020-01485-w | 10.1007/s12275-024-00180-7 | Characterization of Newly Isolated Bacteriophages Targeting Carbapenem-Resistant |
| 39657619 | 10.1002/9781118910030 | 10.1093/infdis/jiae606 | Efficacy of Laundry Practices in Eliminating Mpox Virus From Fabrics. |
| 39665373 | 10.1371/journal.ppat.1001125 | 10.1093/ismejo/wrae245 | Strain phylogroup and environmental constraints shape Escherichia coli dynamics  |
| 39665540 | 10.1038/s41467-023-39863-x | 10.1128/ecosalplus.esp-0029-2023 | The rise, fall, and resurgence of phage therapy for urinary tract infection. |
| 39666461 | 10.1007/s00705-018-4034-0 | 10.1016/j.xpro.2024.103488 | Protocol for establishing CRISPR-Cas12a for efficient genome editing of Pseudomo |
| 39669579 | 10.1186/s12974-024-03036-4 | 10.3389/fimmu.2024.1401156 | High heterogeneity of cross-reactive immunoglobulins in multiple sclerosis presu |
| 39676708 | 10.1609/icwsm.v3i1.13937 | 10.1080/19490976.2024.2431648 | Abnormalities in gut virome signatures linked with cognitive impairment in older |
| 39676876 | 10.1016/j.nutres.2024.01.012 | 10.3389/fimmu.2024.1442788 | Exploring micronutrients and microbiome synergy: pioneering new paths in cancer  |
| 39679618 | 10.1016/j.celrep.2021.109132 | 10.1080/19490976.2024.2309684 | A universe of human gut-derived bacterial prophages: unveiling the hidden viral  |
| 39680919 | 10.1073/pnas.2313574121 | 10.1021/acs.chemrev.4c00681 | Engineering Phages to Fight Multidrug-Resistant Bacteria. |
| 39684210 | 10.1186/s12929-023-00946-y | 10.3390/ijms252312497 | Therapeutic and Diagnostic Potential of a Novel K1 Capsule Dependent Phage, JSSK |
| 39684465 | 10.1186/1944-3277-9-2 | 10.3390/ijms252312755 | Isolation, Characterization, and Unlocking the Potential of Mimir124 Phage for P |
| 39684595 | 10.1007/s10875-022-01293-7 | 10.3390/ijms252312885 | In Vitro Susceptibility of Clinical and Carrier Strains of Staphylococcus aureus |
| 39686816 | 10.1042/EBC20240013 | 10.1042/EBC20240037 | The new age of the phage. |
| 39690326 | 10.1101/2023.08.18.553620 | 10.1038/s41573-024-01086-0 | Chemical engineering of CRISPR-Cas systems for therapeutic application. |
| 39697343 | 10.1177/019262339902700112 | 10.3389/fimmu.2024.1493257 | SON-1010: an albumin-binding IL-12 fusion protein that improves cytokine half-li |
| 39699213 | 10.1093/nar/gkg034 | 10.1128/aac.00740-24 | In vitro resensitization of multidrug-resistant clinical isolates of Enterococcu |
| 39702256 | 10.1038/srep14802 | 10.1186/s12985-024-02580-y | Evaluation of effectiveness of bacteriophage purification methods. |
| 39702735 | 10.1038/s41587-024-02386-x | 10.1038/s41587-024-02516-5 | NIS-Seq enables cell-type-agnostic optical perturbation screening. |
| 39704503 | 10.1101/2024.06.20.599855 | 10.1128/mbio.02559-24 | Temperate phage-antibiotic synergy is widespread-extending to Pseudomonas-but va |
| 39707494 | 10.1002/ijc.31808 | 10.1186/s40168-024-01984-w | Gastrointestinal jumbo phages possess independent synthesis and utilization syst |
| 39714166 | 10.1371/journal.ppat.1005699 | 10.1128/jvi.01497-24 | Single-chain antibody gene therapy strategy based on high-throughput screening t |
| 39714187 | 10.1186/s13059-014-0550-8 | 10.1128/mbio.02957-24 | Phage-mediated virulence loss and antimicrobial susceptibility in carbapenem-res |
| 39714210 | 10.3389/fmicb.2011.00118 | 10.1128/msystems.01106-24 | Exploiting gasdermin-mediated pyroptosis for enhanced antimicrobial activity of  |
| 39715735 | 10.1107/S0907444912001308 | 10.1038/s41467-024-54901-y | Development of mirror-image monobodies targeting the oncogenic BCR::ABL1 kinase. |
| 39715753 | 10.1007/978-1-61779-379-0_19 | 10.1038/s41467-024-54902-x | Generating a mirror-image monobody targeting MCP-1 via TRAP display and chemical |
| 39718471 | 10.26091/ESRNZ.9037676.v1 | 10.1002/iub.2931 | Ethical bioprospecting and microbial assessments for sustainable solutions to th |
| 39719706 | 10.1186/1471-2105-10-421 | 10.1016/j.xgen.2024.100725 | CRISPR-Cas spacer acquisition is a rare event in human gut microbiome. |
| 39723818 | 10.1016/j.chom.2020.06.002 | 10.1128/jvi.01789-24 | Escherichia coli phage ΦPNJ-9 adheres to mucus via a variant Hoc protein. |
| 39724243 | 10.1111/nyas.14649 | 10.1007/s00203-024-04205-y | Breaking the resistance: integrative approaches with novel therapeutics against  |
| 39735565 | 10.1002/pep2.24261 | 10.7717/peerj.18722 | Antimicrobial activity and synergistic effect of phage-encoded antimicrobial pep |
| 39736630 | 10.2967/jnumed.106.036699 | 10.1186/s12885-024-13375-3 | Screening and identification of vascular endothelial cell targeting peptide in g |
| 39738265 | 10.1016/j.xphs.2022.09.022 | 10.1038/s41598-024-79478-w | Real-time monitoring by interferometric light microscopy of phage suspensions fo |
| 39738949 | 10.1016/j.jsb.2008.06.002 | 10.1007/978-3-031-65187-8_7 | Integrative Approaches to Study Virus Structures. |
| 39738955 | 10.1007/s00018-007-6451-1 | 10.1007/978-3-031-65187-8_13 | Nucleic Acid Packaging in Viruses. |
| 39738961 | 10.1017/S0033583508004666 | 10.1007/978-3-031-65187-8_19 | Theoretical Studies on Assembly, Physical Stability, and Dynamics of Viruses. |
| 39741220 | 10.1371/journal.pbio.0040003 | 10.1007/s12560-024-09623-1 | Magnetic Carbon Bead-Based Concentration Method for SARS-CoV-2 Detection in Wast |
| 39742266 | 10.3389/fchem.2021.755238 | 10.3389/fimmu.2024.1520103 | Development of a recombinant human IgG1 monoclonal antibody against the TRBV5-1  |
| 39745426 | 10.1016/j.chom.2022.12.001 | 10.1128/spectrum.01066-24 | Identification and characterization of Faecalibacterium prophages rich in divers |
| 39745428 | 10.3390/v10060338 | 10.1128/jvi.01872-24 | Quorum sensing inhibits phage infection by regulating biofilm formation of P. ae |
| 39745446 | 10.1016/S2589-7500(20)30062-5 | 10.1128/jcm.01443-24 | Assembly and performance of a cholera RDT prototype that detects both Vibrio cho |
| 39746545 | 10.1101/2021.10.04.463034 | 10.1016/j.mcpro.2024.100901 | Molecular Display of the Animal Meta-Venome for Discovery of Novel Therapeutic P |
| 39751948 | 10.1016/j.isci.2022.104353 | 10.1007/s00262-024-03893-1 | Therapeutic effect of fully human anti-Nrp-1 antibody on non-small cell lung can |
| 39753671 | 10.3791/2437 | 10.1038/s41564-024-01886-5 | Bacteria use exogenous peptidoglycan as a danger signal to trigger biofilm forma |
| 39754316 | 10.1097/CJI.0000000000000539 | 10.1002/ctm2.70161 | Disrupting EDEM3-induced M2-like macrophage trafficking by glucose restriction o |
| 39757682 | 10.3390/v13101901 | 10.2174/0113816128343976241117183624 | Phage Therapy: A Promising Treatment Strategy against Infections Caused by Multi |
| 39762450 | 10.1093/ilar.43.4.207 | 10.1038/s42003-024-07269-0 | Mucosal-adapted bacteriophages as a preventive strategy for a lethal Pseudomonas |
| 39764425 | 10.1016/j.hemonc.2013.06.004 | 10.1155/mi/9981131 | Inhibitory Effect of Human Anti-CA I Autoantibodies and Development of Monoclona |
| 39766339 | 10.1146/annurev-bioeng-071813-105206 | 10.3390/biom14121632 | Peptide-Mediated Transport Across the Intact Tympanic Membrane Is Intracellular, |
| 39766551 | 10.1016/j.scitotenv.2018.10.111 | 10.3390/antibiotics13121161 | Local Electric Field-Incorporated In-Situ Copper Ions Eliminating Pathogens and  |
| 39770308 | 10.1016/j.micres.2022.127069 | 10.3390/pathogens13121049 | Colistin Resistance Mechanism and Management Strategies of Colistin-Resistant Ac |
| 39770458 | 10.1128/JCM.03617-13 | 10.3390/ph17121616 | Isolation and Characterization of Lytic Bacteriophages Capable of Infecting Dive |
| 39771637 | 10.1080/10408347.2024.2390551 | 10.3390/s24247899 | Affinity Peptide-Based Circularly Permuted Fluorescent Protein Biosensors for No |
| 39772127 | 10.1128/mbio.02441-21 | 10.3390/v16121816 | Isolation and Characterization of a Lytic Phage PaTJ Against Pseudomonas aerugin |
| 39772150 | 10.3390/ph16121638 | 10.3390/v16121840 | Efficiency of Bacteriophage-Based Detection Methods for Non-Typhoidal Salmonella |
| 39772153 | 10.7717/peerj.6225 | 10.3390/v16121843 | A Concise Overview of Studies on Successful Real-World Applications of Bacteriop |
| 39772164 | 10.3390/v11010010 | 10.3390/v16121855 | Preparation of Phage Display cDNA Libraries for Identifying Immunogenic Tumor An |
| 39772204 | 10.1128/AEM.01979-20 | 10.3390/v16121897 | Exploring the Microbial Ecology of Water in Sub-Saharan Africa and the Potential |
| 39773393 | 10.1016/j.cell.2014.02.001 | 10.2478/aite-2025-0003 | CRISPR/Cas Systems as Diagnostic and Potential Therapeutic Tools for Enterohemor |
| 39775564 | 10.1016/j.jmb.2006.09.087 | 10.1371/journal.pone.0316466 | Plasmidome of Salmonella enterica serovar Infantis recovered from surface waters |
| 39776004 | 10.1016/j.scitotenv.2021.150572 | 10.1007/s12560-024-09620-4 | Environmental Dissemination of SARS-CoV-2: An Analysis Employing Crassphage and  |
| 39780179 | 10.3390/antibiotics9110754 | 10.1186/s12903-024-05399-9 | Phage therapy as an alternative strategy for oral bacterial infections: a system |
| 39786350 | 10.1371/journal.ppat.1008540 | 10.1099/mic.0.001521 | Microbe Profile: Salmonella Typhimurium: the master of the art of adaptation. |
| 39788944 | 10.1016/j.jmb.2007.05.022 | 10.1038/s41467-024-55193-y | Influenza A Virus H7 nanobody recognizes a conserved immunodominant epitope on h |
| 39794471 | 10.1016/j.cell.2013.10.045 | 10.1038/s41564-024-01913-5 | Engineered Mycobacterium tuberculosis triple-kill-switch strain provides control |
| 39795870 | 10.1016/j.micres.2022.127104 | 10.3390/ijms26010011 | The Combination of Phage Therapy and β-Lactam Antibiotics for the Effective Trea |
| 39796236 | 10.1016/j.ijfoodmicro.2012.03.006 | 10.3390/ijms26010381 | Phytochemicals Controlling Enterohemorrhagic Escherichia coli (EHEC) Virulence-C |
| 39798874 | 10.2147/DDDT.S90580 | 10.1016/j.jbc.2025.108176 | Specific recognition mechanism of an antibody to sulfated tyrosine and its poten |
| 39801028 | 10.1128/aac.00731-18 | 10.1111/1751-7915.70075 | From Isolation to Application: Utilising Phage-Antibiotic Synergy in Murine Bact |
| 39803864 | 10.1007/s00253-015-7247-0 | 10.1080/21505594.2025.2450462 | Characterization and genomic insights into bacteriophages Kpph1 and Kpph9 agains |
| 39806322 | 10.3389/fmicb.2019.02949 | 10.1186/s12866-024-03736-0 | "Sichuanvirus", a novel bacteriophage viral genus, able to lyse carbapenem-resis |
| 39806507 | 10.1128/spectrum.02473-21 | 10.1186/s12985-025-02626-9 | The virome composition of respiratory tract changes in school-aged children with |
| 39812873 | 10.1084/jem.20150585 | 10.1007/s10875-024-01849-9 | Hypomorphic RAG2 Deficiency Promotes Selection of Self-Reactive B Cells. |
| 39814459 | 10.1186/s13059-023-03153-y | 10.1261/rna.080347.124 | ASOBIOTICS 2024: an interdisciplinary symposium on antisense-based programmable  |
| 39817744 | 10.3390/v10040182 | 10.1128/spectrum.01908-24 | Enhanced bacteriostatic effects of phage vB_C4 and cell wall-targeting antibioti |
| 39817748 | 10.1093/bioinformatics/btac776 | 10.1128/jb.00343-24 | Structural conservation and functional role of TfpY-like proteins in type IV pil |
| 39818540 | 10.1038/s41375-022-01654-6 | 10.4274/tjh.galenos.2025.2024.0365 | Identification of TRAPPC4 as a Key Autoantigen in Immune-Related Pancytopenia: E |
| 39822166 | 10.1158/2767-9764.CRC-24-0258 | 10.1111/1751-7915.70081 | A Phage-Based Approach to Identify Antivirulence Inhibitors of Bacterial Type IV |
| 39824170 | 10.1038/nature17436 | 10.1016/j.molcel.2024.12.007 | Nucleic acid recognition during prokaryotic immunity. |
| 39826551 | 10.1038/s41587-023-01763-2 | 10.1016/j.cels.2024.12.008 | Subspecies phylogeny in the human gut revealed by co-evolutionary constraints ac |
| 39830964 | 10.1038/nprot.2009.10 | 10.7717/peerj.18785 | Benchmarking of a time-saving and scalable protocol for the extraction of DNA fr |
| 39833928 | 10.1186/s12879-022-07944-9 | 10.1186/s12985-024-02552-2 | Evaluation of host immune responses to Mycobacteriophage Fionnbharth by route of |
| 39837922 | 10.2174/138161210790963788 | 10.1038/s41598-025-86439-4 | Target-specific peptides for BK virus agnoprotein identified through phage displ |
| 39839260 | 10.2147/IDR.S404855 | 10.3389/fcimb.2024.1526312 | Rising prevalence and drug resistance of Corynebacterium striatum in lower respi |
| 39840412 | 10.3347/kjp.2013.51.1.93 | 10.2174/0118722083275669231227063413 | Construction of Camelus dromedaries Immune Single Domain Antibodies Library for  |
| 39840957 | 10.1101/2023.04.30.538883 | 10.1128/aac.01162-24 | Enhanced suppression of Stenotrophomonas maltophilia by a three-phage cocktail:  |
| 39843440 | 10.1021/acs.nanolett.3c00957 | 10.1038/s41467-025-56219-9 | Microenvironment-confined kinetic elucidation and implementation of a DNA nano-p |
| 39843757 | 10.1016/j.ajcnut.2022.12.015 | 10.1007/s40265-024-02107-3 | The Future of Microbiome Therapeutics. |
| 39844559 | 10.3390/antibiotics12020417 | 10.2174/0113892010347488250113171505 | Navigating Regulatory Frameworks and Compliances for Bacteriophages as Therapeut |
| 39846747 | 10.1186/s40168-024-01820-1 | 10.1128/jb.00428-24 | Gut phages and their interactions with bacterial and mammalian hosts. |
| 39847085 | 10.1038/s42255-022-00531-x | 10.1007/s00125-024-06356-5 | Active targeting of type 1 diabetes therapies to pancreatic beta cells using nan |
| 39847604 | 10.1016/j.chom.2020.11.007 | 10.1371/journal.ppat.1012903 | Nanobody screening and machine learning guided identification of cross-variant a |
| 39849127 | 10.3390/antibiotics11101406 | 10.1007/s00294-024-01307-4 | Whole-genome evaluation and prophages characterization associated with genome of |
| 39849917 | 10.1093/bioinformatics/btr507 | 10.1080/19420862.2025.2451296 | Engineered ipilimumab variants that bind human and mouse CTLA-4. |
| 39856391 | 10.1038/s41587-023-01799-4 | 10.1038/s41564-024-01906-4 | Longitudinal phage-bacteria dynamics in the early life gut microbiome. |
| 39858389 | 10.2174/0929867322666150209152851 | 10.3390/antibiotics14010104 | A VersaTile Approach to Reprogram the Specificity of the R2-Type Tailocin Toward |
| 39858539 | 10.1002/cyto.a.23690 | 10.3390/biom15010145 | Feasibility of Ex Vivo Ligandomics. |
| 39861840 | 10.1038/s41586-024-07487-w | 10.3390/v17010045 | Synthesis of Headful Packaging Phages Through Yeast Transformation-Associated Re |
| 39861872 | 10.1016/S0092-8674(01)00637-7 | 10.3390/v17010083 | Phage vB_KlebPS_265 Active Against Resistant/MDR and Hypermucoid K2 Strains of K |
| 39861891 | 10.1111/j.1365-2672.2006.02918.x | 10.3390/v17010101 | Selected Mechanisms of Action of Bacteriophages in Bacterial Infections in Anima |
| 39861901 | 10.1007/s13346-021-01085-3 | 10.3390/v17010112 | Inovirus-Encoded Peptides Induce Specific Toxicity in Pseudomonas aeruginosa. |
| 39861904 | 10.1128/AEM.00468-21 | 10.3390/v17010115 | Klebsiella pneumoniae Phage M198 and Its Therapeutic Potential. |
| 39861912 | 10.1128/aac.02071-21 | 10.3390/v17010123 | Phage Therapy as a Rescue Treatment for Recurrent Pseudomonas aeruginosa Bentall |
| 39861923 | 10.1038/s41598-017-08336-9 | 10.3390/v17010134 | Transcytosis of T4 Bacteriophage Through Intestinal Cells Enhances Its Immune Ac |
| 39865354 | 10.4161/mabs.25632 | 10.1002/pro.70019 | Engineered protein G variants for multifunctional antibody-based assemblies. |
| 39868244 | 10.1371/journal.pone.0009490 | 10.1101/2025.01.14.632786 | Pseudomonas superinfection drives Pf phage transmission within airway infections |
| 39880956 | 10.1002/9780470015902.a0021579 | 10.1038/s41586-024-08498-3 | CARD domains mediate anti-phage defence in bacterial gasdermin systems. |
| 39885527 | 10.1016/j.omtm.2020.08.014 | 10.1186/s12987-025-00624-1 | Increasing brain half-life of antibodies by additional binding to myelin oligode |
| 39885536 | 10.1016/j.jtbi.2007.08.006 | 10.1186/s12985-025-02637-6 | Characterization and genome analysis of lytic Vibrio phage VPK8 with potential i |
| 39890605 | 10.1128/JB.00189-18 | 10.1093/femsle/fnaf017 | Pseudomonas aeruginosa maintains an inducible array of novel and diverse prophag |
| 39891859 | 10.3390/v11010010 | 10.1007/s12602-024-10422-0 | Characterization of Extracellular Vesicles from Streptococcus thermophilus 065 a |
| 39892607 | 10.1080/10408398.2021.1905603 | 10.1016/j.jare.2025.01.034 | Detection of Staphylococcus aureus via IgY-based immunomagnetic separation and a |
| 39895136 | 10.3390/ph14030199 | 10.1021/acsabm.4c01638 | Anti-Infective Bacteriophage Immobilized Nitric Oxide-Releasing Surface for Prev |
| 39898971 | 10.1080/01652176.2022.2080298 | 10.1111/1541-4337.70124 | Phage-derived proteins: Advancing food safety through biocontrol and detection o |
| 39902180 | 10.3389/fpubh.2020.00295 | 10.3389/fcimb.2024.1496896 | Population genetic analysis of clinical Mycobacterium abscessus complex strains  |
| 39903766 | 10.1128/mBio.01652-19 | 10.1371/journal.pcbi.1012793 | Multi-strain phage induced clearance of bacterial infections. |
| 39905205 | 10.1093/nar/gkab1038 | 10.1038/s42003-025-07598-8 | Urinary bacteriophage cooperation with bacterial pathogens during human urinary  |
| 39907445 | 10.3389/fmicb.2021.707815 | 10.1128/spectrum.03010-24 | Study of the probability of resistance to phage infection in a collection of cli |
| 39910123 | 10.1016/j.apsb.2022.05.007 | 10.1038/s41598-025-86334-y | Efficacy of bacteriophages with Aloe vera extract in formulated cosmetics to com |
| 39912676 | 10.1038/nprot.2008.73 | 10.1128/spectrum.01601-24 | Synergistic action of mucoactive drugs and phages against Pseudomonas aeruginosa |
| 39912979 | 10.3390/molecules27061857 | 10.1007/s11845-025-03898-4 | Synergistic effects of zP-1 phage and ampicillin against methicillin-resistant S |
| 39915791 | 10.1016/j.copbio.2004.06.004 | 10.1186/s12951-025-03169-5 | Unveiling the new chapter in nanobody engineering: advances in traditional const |
| 39918338 | 10.12688/f1000research.4524.1 | 10.1128/mbio.02466-24 | Phage reprogramming of Pseudomonas aeruginosa amino acid metabolism drives effic |
| 39933917 | 10.1016/j.neuron.2024.07.026 | 10.26508/lsa.202201490 | Screening of homing and tissue-penetrating peptides by microdialysis and in vivo |
| 39934226 | 10.5812/ijcm.9763 | 10.1038/s41598-025-89143-5 | Targeted cancer treatment using a novel EGFR-specific Fc-fusion peptide based on |
| 39934535 | 10.3390/antibiotics3030270 | 10.1007/s11033-025-10332-6 | Engineering bacteriophages for targeted superbug eradication. |
| 39934835 | 10.1073/pnas.86.19.7566 | 10.1186/s13046-025-03319-5 | An IgE antibody targeting HER2 identified by clonal selection restricts breast c |
| 39945517 | 10.1073/pnas.062526099 | 10.1128/spectrum.02141-24 | Comparison of pharyngeal and invasive isolates of Streptococcus pyogenes by whol |
| 39945525 | 10.1186/s40168-020-00867-0 | 10.1128/msphere.00904-24 | Prophages are infrequently associated with antibiotic resistance in Pseudomonas  |
| 39955358 | 10.1371/journal.pone.0294236 | 10.1007/s00284-025-04110-7 | Comparative Genomic Analysis of 66 Bacteriophages Infecting Morganella morganii  |
| 39957412 | 10.1212/NXI.0000000000200068 | 10.1002/acn3.70012 | High-Throughput Immunoassays for Cavin-4 IgG: A Diagnostic Tool for Immune-Media |
| 39964597 | 10.3389/fmicb.2021.609459 | 10.1007/s12010-025-05182-8 | Unravelling the Antibiotic Resistance: Molecular Insights and Combating Therapie |
| 39964630 | 10.1016/j.micpath.2016.08.021 | 10.1007/s10096-025-05066-z | Septic arthritis - symptoms, diagnosis and new therapy. |
| 39966674 | 10.21105/joss.01686 | 10.1038/s41598-025-90414-4 | Comprehensive genomic insights into a highly pathogenic clone ST656 of mcr8.1 co |
| 39967671 | 10.1021/acs.bioconjchem.6b00469 | 10.3389/fimmu.2025.1531171 | Discovery and in vitro characterization of a human anti-CD36 scFv. |
| 39968173 | 10.1111/evo.12183 | 10.1016/j.crmicr.2025.100353 | Pseudomonas rossensis sp. nov., a novel psychrotolerant species produces antimic |
| 39969275 | 10.1038/nbt.3880 | 10.1099/mgen.0.001352 | Phenotypic and genetic heterogeneity of Acinetobacter baumannii in the course of |
| 39972061 | 10.1038/nmeth.f.303 | 10.1038/s41564-025-01937-5 | Intestinal crypt microbiota modulates intestinal stem cell turnover and tumorige |
| 39975350 | 10.1093/PNASNEXUS/PGAD406 | 10.1101/2025.02.03.636326 | Bacteriophage purification using CIMmultus monolithic OH-column chromatography f |
| 39976625 | 10.4248/IJOS11030 | 10.1099/mic.0.001535 | Genomic and transcriptomic insights into the virulence and adaptation of shock s |
| 39979461 | 10.1038/s41598-021-99696-w | 10.1038/s41598-025-90605-z | Antimicrobial cyclic peptides effectively inhibit multiple forms of Borrelia and |
| 39979834 | 10.3109/07853890108995959 | 10.1186/s12866-025-03785-z | Therapeutic potential of a newly isolated bacteriophage against multi-drug resis |
| 39982075 | 10.1371/journal.pone.0107307 | 10.1128/msphere.01014-24 | A new bacteriophage infecting Staphylococcus epidermidis with potential for remo |
| 39982880 | 10.1016/j.bjm.2018.03.004 | 10.1371/journal.pone.0315079 | Isolation and characterization of bacteriophage against clinical isolates of Amp |
| 39984516 | 10.1371/journal.pntd.0007380 | 10.1038/s41598-025-89307-3 | Modelling the effects of climate change on the interaction between bacteria and  |
| 39994360 | 10.1128/AAC.45.3.649-659.2001 | 10.1038/s41598-025-91073-1 | Isolation and characterization of new lytic bacteriophage PSA-KC1 against Pseudo |
| 39998161 | 10.1016/j.foodres.2023.113609 | 10.1128/spectrum.01577-24 | A streamlined procedure for advancing the detection and isolation of Listeria mo |
| 39998178 | 10.1093/nar/gks406 | 10.1128/mbio.03548-24 | Reduced prevalence of phage defense systems in Pseudomonas aeruginosa strains fr |
| 39998218 | 10.1007/s00216-023-04758-9 | 10.1128/mbio.03997-24 | Campylobacter jejuni resistance to human milk involves the acyl carrier protein  |
| 40001355 | 10.1089/cmb.2012.0021 | 10.3390/antibiotics14020110 | Genomic Insights into and Lytic Potential of Native Bacteriophages M8-2 and M8-3 |
| 40004222 | 10.1111/1751-7915.13728 | 10.3390/ijms26041755 | Re-Emergence of Bacteriophages and Their Products as Antibacterial Agents: An Ov |
| 40006944 | 10.1007/s12250-014-3546-3 | 10.3390/v17020189 | New Bacteriophage Pseudomonas Phage Ka2 from a Tributary Stream of Lake Baikal. |
| 40006955 | 10.1038/s41587-023-01773-0 | 10.3390/v17020200 | Development of Chimera AMP-Endolysin with Wider Spectra Against Gram-Negative Ba |
| 40007695 | 10.5604/01.3001.0013.2022 | 10.3389/abp.2025.14264 | Phages as potential life-saving therapeutic option in the treatment of multidrug |
| 40011806 | 10.1111/evo.14153 | 10.1186/s12866-025-03827-6 | Insights into diversity, host-range, and temporal stability of Bacteroides and P |
| 40011819 | 10.1016/j.chest.2020.07.089 | 10.1186/s12866-025-03813-y | Characterization and genome analysis of novel Klebsiella pneumoniae phage vbKpUK |
| 40013800 | 10.1007/s12275-019-9272-7 | 10.1128/jvi.01949-24 | Pilin regions that select for the small RNA phages in Pseudomonas aeruginosa typ |
| 40014690 | 10.5281/ZENODO.14833852 | 10.1126/science.adv9789 | TIGR-Tas: A family of modular RNA-guided DNA-targeting systems in prokaryotes an |
| 40021925 | 10.1016/j.resmic.2018.05.001 | 10.1038/s44259-025-00088-1 | R-pyocins as targeted antimicrobials against Pseudomonas aeruginosa. |
| 40022448 | 10.1038/s41598-021-98706-1 | 10.1016/j.ymthe.2025.02.037 | A universal viral capsid protein based one step RNA synthesis and packaging syst |
| 40025202 | 10.1093/oxfordjournals.molbev.a026203 | 10.1038/s41598-025-92032-6 | A novel Kayvirus species phage RuSa1 removes biofilm and lyses multiple clinical |
| 40025468 | 10.3389/fmicb.2022.898961 | 10.1186/s12866-025-03796-w | The high efficiency protective effectiveness of a newly isolated myoviruses bact |
| 40026247 | 10.1177/1352458517751861 | 10.1172/JCI171948 | Patterns of autoantibody expression in multiple sclerosis identified through dev |
| 40026251 | 10.2217/pme.11.7 | 10.1172/JCI187996 | Bacteriophage therapy for multidrug-resistant infections: current technologies a |
| 40029291 | 10.1126/science.aba1786 | 10.1158/0008-5472.CAN-24-1959 | Engineered SH3-Derived Sherpabodies Function as a Modular Platform for Targeted  |
| 40033410 | 10.1128/mBio.02392-21 | 10.1186/s12985-025-02679-w | Isolation and characterization of fMGyn-Pae01, a phiKZ-like jumbo phage infectin |
| 40035599 | 10.1038/s41467-022-30269-9 | 10.1128/aem.02402-24 | Phage-host interaction in Pseudomonas aeruginosa clinical isolates with function |
| 40036505 | 10.1038/s41586-021-03241-8 | 10.1093/nar/gkaf118 | Development of a quantitative metagenomic approach to establish quantitative lim |
| 40038403 | 10.1146/annurev-animal-022114-110911 | 10.1038/s41598-025-90770-1 | Discovery and functional characterization of canine PD-L1-targeted antibodies fo |
| 40038849 | 10.1016/S0168-9525(00)02024-2 | 10.1080/19420862.2025.2472009 | An antibody developability triaging pipeline exploiting protein language models. |
| 40045938 | 10.7717/peerj.590 | 10.1089/phage.2021.0018 | Isolation and Characterization of Three Lytic Bacteriophages to Overcome Multidr |
| 40050878 | 10.1186/s13052-021-01080-x | 10.1186/s13052-025-01917-9 | A missense mutation in PDHB gene: identification of the patient with pyruvate de |
| 40051517 | 10.3947/ic.2023.0067 | 10.3389/fpubh.2025.1490737 | Perception of phage therapy and research across selected professional and social |
| 40057622 | 10.3390/antibiotics12071143 | 10.1007/s00705-025-06257-x | Bacteriophage-derived depolymerase: a review on prospective antibacterial agents |
| 40060533 | 10.3390/v12111268 | 10.1101/2025.02.26.640152 | Pseudomonads coordinate innate defense against viruses and bacteria with a singl |
| 40066272 | 10.3389/fbioe.2021.643722 | 10.3389/fmicb.2025.1553979 | The landscape of biofilm models for phage therapy: mimicking biofilms in diabeti |
| 40072675 | 10.1089/mdr.2020.0431 | 10.1007/s44197-025-00382-1 | Temporal Dynamics of Microbial Community Composition and Antimicrobial Resistanc |
| 40075385 | 10.1016/j.ejmech.2020.112137 | 10.1186/s12896-025-00956-8 | Enhancement of plasma kallikrein specificity of antitrypsin variants identified  |
| 40079390 | 10.1038/s41467-018-04134-7 | 10.1021/acschembio.4c00803 | Single-Chain Nanobody Inhibition of Notch and Avidity Enhancement Utilizing the  |
| 40081940 | 10.1136/jitc-2020-000673 | 10.1136/jitc-2023-008594 | Novel anti-CD73-IL-2v bispecific fusion protein augments antitumor immunity by a |
| 40089540 | 10.1007/978-1-60327-164-6_14 | 10.1038/s41598-025-94040-y | Synergistic antibacterial activity of curcumin and phage against multidrug-resis |
| 40096354 | 10.1038/nature18849 | 10.1080/07853890.2025.2478317 | Exploring the role of gut microbiota in antibiotic resistance and prevention. |
| 40100143 | 10.1073/pnas.2108458118 | 10.1002/pro.70088 | High-throughput amino acid-level characterization of the interactions of plasmin |
| 40100169 | 10.1186/1471-2105-13-31 | 10.1002/pro.70090 | A synthetic heavy chain variable domain antibody library (VHL) provides highly f |
| 40105966 | 10.1038/s41423-021-00726-4 | 10.1007/s00262-025-03995-4 | A novel peptide targeting CCR7 inhibits tumor cell lymph node metastasis. |
| 40109477 | 10.1016/j.pharmthera.2022.108296 | 10.12182/20250160107 | [Preparation of Trop2-Targeted CAR-T Cells Based on Nanobodies and Their Antitum |
| 40111044 | 10.1007/s00705-022-05694-2 | 10.1128/mra.01289-24 | A complete genome of an obligately lytic Pseudomonas aeruginosa bacteriophage, M |
| 40113632 | 10.1093/nar/gkr485 | 10.1007/s00438-025-02239-5 | Molecular epidemiological study of Pseudomonas aeruginosa strains isolated from  |
| 40114780 | 10.1016/j.addr.2014.03.006 | 10.14356/kona.2025016 | Formulation of Bacteriophage for Inhalation to Treat Multidrug-Resistant Pulmona |
| 40130840 | 10.1053/jhin.2002.1281 | 10.1128/aem.02474-24 | Product formulation and rubbing time impact the inactivation of enveloped and no |
| 40130866 | 10.1038/s41467-024-54384-x | 10.1128/spectrum.02784-24 | Generation of nanobodies against the F protein of respiratory syncytial virus an |
| 40132540 | 10.1093/nar/gkab1136 | 10.1016/j.crmeth.2025.101008 | The development of a canine single-chain phage antibody library to isolate recom |
| 40133514 | 10.1212/NXI.0000000000001010 | 10.1007/s00415-025-13039-7 | Exploring autoantigens in autoimmune limbic encephalitis using phage immunopreci |
| 40134430 | 10.1158/1078-0432.CCR-21-3329 | 10.3389/fimmu.2025.1499810 | AI-enhanced profiling of phage-display-identified anti-TIM3 and anti-TIGIT novel |
| 40135773 | 10.1021/ci100275a | 10.1021/jacs.4c17452 | Adding a Twist to Lateral Flow Immunoassays: A Direct Replacement of Antibodies  |
| 40137775 | 10.1093/ismejo/wrae108 | 10.3390/pathogens14030291 | Can Bacteriophages Be Effectively Utilized for Disinfection in Animal-Derived Fo |
| 40140901 | 10.1038/npg.els.0005062 | 10.1186/s12916-025-04016-y | Gut virome and its implications in the pathogenesis and therapeutics of inflamma |
| 40141346 | 10.1093/nar/gkv495 | 10.3390/ijms26062705 | Activin A Inhibitory Peptides Suppress Fibrotic Pathways by Targeting Epithelial |
| 40141363 | 10.1093/bioinformatics/btt262 | 10.3390/ijms26062721 | A Novel Human Anti-FV mAb as a Potential Tool for Diagnostic and Coagulation Inh |
| 40141446 | 10.7717/peerj-cs.104 | 10.3390/ijms26062805 | A Two-Phage Cocktail Modulates Gut Microbiota Composition and Metabolic Profiles |
| 40142404 | 10.1038/s41564-017-0061-y | 10.3390/microorganisms13030511 | Isolation, Characterization, and Genomic Analysis of Bacteriophages Against Pseu |
| 40143121 | 10.1128/AAC.04469-14 | 10.3390/ph18030343 | In Vitro Interactions Between Bacteriophages and Antibacterial Agents of Various |
| 40143245 | 10.1128/mra.01117-23 | 10.3390/v17030314 | High-Performance Genome Annotation for a Safer and Faster-Developing Phage Thera |
| 40143297 | 10.1128/aem.00434-24 | 10.3390/v17030369 | Pseudomonas Phage Lydia and the Evolution of the Mesyanzhinovviridae Family. |
| 40143341 | 10.1128/jvi.00176-23 | 10.3390/v17030414 | The Application of DNA Viruses to Biotechnology. |
| 40148969 | 10.1099/jgv.0.001392 | 10.1186/s12985-025-02710-0 | Isolation, characterization, and genomic analysis of three novel Herelleviridae  |
| 40152610 | 10.1186/s13059-019-1758-4 | 10.1128/msystems.00201-25 | Unveiling the role of phages in shaping the periodontal microbial ecosystem. |
| 40153382 | 10.1371/journal.ppat.1009720 | 10.1371/journal.ppat.1012428 | Selection and characterization of a broadly neutralizing class of HCV anti-E2 VH |
| 40157986 | 10.3390/v12111268 | 10.1038/s41598-025-95398-9 | Characterization and therapeutic potential of newly isolated bacteriophages targ |
| 40160174 | 10.3389/fcimb.2021.66918 | 10.1080/19490976.2025.2481178 | Effects of bacteriophages on gut microbiome functionality. |
| 40162801 | 10.1111/ajt.15503 | 10.1128/spectrum.02149-24 | Genomic variation in Pseudomonas aeruginosa clinical respiratory isolates with d |
| 40165964 | 10.1093/cid/ciz782 | 10.3389/fimmu.2025.1563450 | Harnessing the human gut microbiota: an emerging frontier in combatting multidru |
| 40168365 | 10.1186/s40168-020-00935-5 | 10.1371/journal.pbio.3003071 | A hypermobile prophage in the genome of a key human gut bacterium. |
| 40172217 | 10.1038/s41467-023-38868-w | 10.1128/spectrum.01750-24 | Epitope mapping targeting the K205R protein of African swine fever virus using n |
| 40178652 | 10.3390/ijerph14121571 | 10.1007/s12560-025-09640-8 | In Vitro Efficacy of Foam Hand Sanitizers Against Enveloped and Non-Enveloped Vi |
| 40180606 | 10.3390/ijms19010054 | 10.1093/immhor/vlaf012 | In vitro and in vivo neutralization of Dengue virus by a single domain antibody. |
| 40182769 | 10.1007/s00294-015-0499-5 | 10.3389/fcimb.2025.1562402 | Regulatory effects on virulence and phage susceptibility revealed by sdiA mutati |
| 40186383 | 10.1038/ncb3139 | 10.1002/jbm.a.37908 | Dual-Functional Peptide DPI-VTK Promotes Mesenchymal Stem Cell Migration for Bon |
| 40188480 | 10.1038/s41579-019-0201-x | 10.1093/ismejo/wraf065 | Phage-phage competition and biofilms affect interactions between two virulent ba |
| 40197051 | 10.1093/nar/gkac341 | 10.1128/msystems.01364-24 | Improving gut virome comparisons using predicted phage host information. |
| 40197829 | 10.1093/nar/gkx452 | 10.1093/nar/gkaf236 | DragonRNA: Generality of DNA-primed RNA-extension activities by DNA-directed RNA |
| 40198373 | 10.1016/j.ijbiomac.2023.129146 | 10.1007/s00284-025-04212-2 | Integrating Modified Fe3O4 Nanoparticles and Nisin with T4 Bacteriophage for Enh |
| 40198880 | 10.1128/AAC.01429-23 | 10.1371/journal.ppat.1012971 | Phage therapy for Klebsiella pneumoniae: Understanding bacteria-phage interactio |
| 40200154 | 10.1016/j.micpath.2023.106199 | 10.1186/s12866-025-03913-9 | In silico genomic insights into bacteriophages infecting ESBL-producing Escheric |
| 40201976 | 10.1038/s41598-019-52258-7 | 10.1080/19420862.2025.2486390 | Nanoscale warriors against viral invaders: a comprehensive review of Nanobodies  |
| 40202338 | 10.3390/jof4030108 | 10.1128/spectrum.02634-24 | The Klebsiella pneumoniae tellurium resistance gene terC contributes to both tel |
| 40205515 | 10.1093/bioinformatics/btp348 | 10.1186/s40168-025-02081-2 | House dust microbiome differentiation and phage-mediated antibiotic resistance a |
| 40207161 | 10.15537/smj.2016.9.16139 | 10.3389/fmicb.2025.1568899 | Exploring the diversity and antimicrobial potential of actinomycetes isolated fr |
| 40207629 | 10.1038/s41573-020-0075-7 | 10.1093/nar/gkaf270 | Conjugation to a transferrin receptor 1-binding Bicycle peptide enhances ASO and |
| 40208028 | 10.1016/s1286-4579(00)90356-3 | 10.1128/iai.00618-24 | Filamentous bacteriophage M13 induces proinflammatory responses in intestinal ep |
| 40208916 | 10.21105/joss.01686 | 10.1371/journal.ppat.1012986 | Mystique, a broad host range Acinetobacter phage, reveals the impact of culturin |
| 40210629 | 10.4163/kjn.2013.46.2.186 | 10.1038/s41467-025-58856-6 | Characterization of the phyllosphere virome of fresh vegetables and potential tr |
| 40210708 | 10.1038/s41579-020-0340-0 | 10.1038/s41579-025-01169-8 | The global resistance problem and the clinical antibacterial pipeline. |
| 40221535 | 10.1007/s00705-020-04813-1 | 10.1038/s41598-025-96211-3 | Development of novel neutralizing single-chain fragment variable antibodies agai |
| 40223105 | 10.1016/j.joen.2013.08.022 | 10.1186/s12941-025-00790-y | Novel strategies for vancomycin-resistant Enterococcus faecalis biofilm control: |
| 40227106 | 10.1111/j.1348-0421.2009.00105.x | 10.1128/jb.00521-24 | Colony morphotype variation in Burkholderia: implications for success of applica |
| 40229393 | 10.1128/iai.5.4.622-624.1972 | 10.1038/s41598-025-96561-y | Rapid formulation of a genetically diverse phage cocktail targeting uropathogeni |
| 40231830 | 10.1186/1471-2180-9-19 | 10.1128/spectrum.03303-24 | Insertion sequence-mediated phage resistance contributes to attenuated colonizat |
| 40236058 | 10.1093/genetics/143.1.15 | 10.1101/2025.04.01.646652 | Filamentous cheater phages drive bacterial and phage populations to lower fitnes |
| 40237489 | 10.3390/v12101143 | 10.1128/aem.01788-24 | The human phageome: niche-specific distribution of bacteriophages and their clin |
| 40240293 | 10.1101/2024.03.29.587342 | 10.1093/femsre/fuaf014 | Pseudomonas aeruginosa as a model bacterium in antiphage defense research. |
| 40240928 | 10.3390/molecules16021776 | 10.1186/s12866-025-03903-x | Characterization and therapeutic potential of phage vB_Eco_ZCEC08 against multid |
| 40243472 | 10.3389/fmicb.2023.1250848 | 10.3390/ijms26072882 | The Microbiome and Metabolic Dysfunction-Associated Steatotic Liver Disease. |
| 40243587 | 10.1016/s0966-842x(01)02198-9 | 10.1099/mgen.0.001397 | Population structure and gene flux of Listeria monocytogenes ST121 reveal propha |
| 40244536 | 10.1021/acs.nanolett.2c04279 | 10.1007/s10549-025-07696-5 | Targeting breast cancer: the promise of phage-based nanomedicines. |
| 40248366 | 10.3389/fgene.2024.1494474 | 10.3389/fcimb.2025.1582553 | Metagenomic analysis reveals the diversity of the vaginal virome and its associa |
| 40250500 | 10.3390/pharmaceutics13081162 | 10.1016/j.ijpharm.2025.125602 | Powder aerosol formulation of Pseudomonas aeruginosa bacteriophage for pulmonary |
| 40251011 | 10.1186/s12985-020-01485-w | 10.1093/femsec/fiaf043 | Weberviruses are gut-associated phages that infect Klebsiella spp. |
| 40256450 | 10.1016/j.jinf.2024.106125 | 10.3389/fcimb.2025.1547250 | Evaluating the safety, pharmacokinetics and efficacy of phage therapy in treatin |
| 40258842 | 10.1038/s41586-024-07681-w | 10.1038/s41598-025-96924-5 | Comparison of phage and plasmid populations in the gut microbiota between Parkin |
| 40260965 | 10.1016/j.chom.2020.04.023 | 10.1002/pro.70114 | Optimization of synthetic human VH affinity and solubility through in vitro affi |
| 40261708 | 10.1371/journal.pone.0009490 | 10.1172/jci.insight.188146 | New Pseudomonas infections drive Pf phage transmission in CF airways. |
| 40264322 | 10.1093/gastro/goab046 | 10.2174/0113816128354250250326045943 | Harnessing the Human Microbiome for Innovative Drug Delivery Systems: Exploring  |
| 40265927 | 10.1007/978-1-0716-3523-0_11 | 10.1128/aac.01935-24 | Studies in vitro and in vivo of phage therapy medical products (PTMPs) Targeting |
| 40266526 | 10.1002/cpz1.182 | 10.1007/978-1-0716-4542-0_14 | Phage Display Isolation of VHH Antibodies Targeting Capsular Polysaccharides of  |
| 40266661 | 10.1016/B978-0-7020-6285-8.00140-4 | 10.1099/mgen.0.001399 | Genomic characterization of group B Streptococcus from Argentina: insights into  |
| 40268121 | 10.3390/ani10050872 | 10.1016/j.jfp.2025.100510 | Regulatory Landscape and the Potential of Bacteriophage Applications in the Unit |
| 40272156 | 10.1186/s12859-016-0976-y | 10.1128/jvi.02250-24 | SARS-CoV-2 biological clones are genetically heterogeneous and include clade-dis |
| 40276382 | 10.3389/fmicb.2016.00922 | 10.3389/fcimb.2025.1589236 | Rapid detection of drug resistance in Mycobacterium tuberculosis clinical isolat |
| 40277083 | 10.1038/s41564-020-0726-9 | 10.1093/nar/gkaf318 | Mechanism of Cas9 inhibition by AcrIIA11. |
| 40277368 | 10.1039/D2EW00126H | 10.1128/aem.01470-24 | CrAssphage distribution analysis in an Amazonian river based on metagenomic sequ |
| 40284401 | 10.1016/j.coviro.2021.12.009 | 10.3390/pharmaceutics17040405 | Development of Inhalable Bacteriophage Liposomes Against Pseudomonas aeruginosa. |
| 40284749 | 10.51594/estj.v5i7.1344 | 10.3390/microorganisms13040913 | Antibiotic-Resistant Pseudomonas aeruginosa: Current Challenges and Emerging Alt |
| 40284925 | 10.1111/mmi.13922 | 10.3390/v17040482 | Phage-Based Control of Listeria innocua in the Food Industry: A Strategy for Pre |
| 40284992 | 10.1038/s41598-023-44987-7 | 10.3390/v17040549 | Harnessing the Activity of Lytic Bacteriophages to Foster the Sustainable Develo |
| 40285003 | 10.1080/08927014.2023.2265817 | 10.3390/v17040560 | Phage Endolysins as Promising and Effective Candidates for Use Against Uropathog |
| 40291807 | 10.7883/yoken.JJID.2022.206 | 10.3389/fmicb.2025.1570665 | Characterization of the novel cross-genus phage vB_SmaS_QH3 and evaluation of it |
| 40293490 | 10.3390/v10020064 | 10.1007/s00103-025-04048-y | [Potential of bacteriophage therapy in Germany: evidence and clinical relevance] |
| 40294087 | 10.1097/HEP.0000000000000985 | 10.1097/MCO.0000000000001128 | Gut microbiota in patients with metabolic, dysfunction-associated steatotic live |
| 40298105 | 10.1093/bioinformatics/btab187 | 10.1002/pro.70146 | To be, or not to be cleaved: Directed evolution of a canonical serine protease i |
| 40298417 | 10.1093/nar/gki408 | 10.1128/mra.00275-25 | Genome sequences of two phages active against cystic fibrosis isolates of Pseudo |
| 40299201 | 10.1371/journal.pone.0064671 | 10.1007/s12602-025-10543-0 | Characteristics and Antibacterial Activity of Staphylococcus aureus Phage-Derive |
| 40300605 | 10.1093/gigascience/giaa008 | 10.1016/j.cub.2025.03.073 | Abundance measurements reveal the balance between lysis and lysogeny in the huma |
| 40301565 | 10.1016/j.micpath.2020.104685 | 10.1038/s41598-025-99116-3 | Inflammation, toxicity, and apoptosis reducing potential of bacteriophage Arioba |
| 40304385 | 10.21105/joss.03167 | 10.1128/msystems.00301-25 | Heterogeneity in recombination rates and accessory gene co-occurrence distinguis |
| 40304465 | 10.1159/000296306 | 10.1128/spectrum.02848-24 | Inhibitory effect of plant flavonoid cyanidin on oral microbial biofilm. |
| 40312318 | 10.1128/AAC.45.11.2977-2986.2001 | 10.1186/s12866-025-03978-6 | Lung-directed delivery of a ligand-mediated chimeric lysin has an enhanced abili |
| 40313938 | 10.1016/j.cell.2024.07.057 | 10.3389/fimmu.2025.1545308 | Sequestering survival: sponge-like proteins in phage evasion of bacterial immune |
| 40314735 | 10.1016/j.chembiol.2022.06.003 | 10.1007/s00103-025-04051-3 | [Basic knowledge of phages and their therapeutic application]. |
| 40323379 | 10.1093/ismeco/ycae082 | 10.1007/s00103-025-04060-2 | [Regulation of phage therapy medicinal products: developments, challenges and op |
| 40323507 | 10.1126/science.aan4236 | 10.1007/s00210-025-04155-2 | The microbiota-gut-brain-axis theory: role of gut microbiota modulators (GMMs) i |
| 40325370 | 10.1186/s12941-023-00653-4 | 10.1186/s10020-025-01226-1 | Bacteriophage-derived endolysins restore antibiotic susceptibility in β-lactam-  |
| 40325452 | 10.3389/fmicb.2021.638094 | 10.1186/s13756-025-01548-z | Isolation and identification of Klebsiella pneumoniae phage ΦK2046: optimizing i |
| 40327073 | 10.1007/s001050051037 | 10.1007/s00103-025-04056-y | [Medical ethical challenges of phage therapy-informed consent, study design and  |
| 40328935 | 10.1016/j.jaci.2019.05.020 | 10.1007/s00103-025-04059-9 | [Phage endolysins-a novel class of antibacterial agents with a wide range of app |
| 40329301 | 10.1038/s41592-022-01488-1 | 10.1186/s13062-025-00638-7 | Elucidation of short linear motif-based interactions of the MIT and rhodanese do |
| 40329529 | 10.1107/S0907444909052925 | 10.1016/j.ymthe.2025.04.042 | Locking CBL TKBD in its native conformation presents a novel therapeutic opportu |
| 40333625 | 10.1016/j.envres.2024.119218 | 10.3390/molecules30081682 | Facing Foodborne Pathogen Biofilms with Green Antimicrobial Agents: One Health A |
| 40338297 | 10.3390/antibiotics10070849 | 10.1007/s00103-025-04063-z | [Phage therapy in Germany-Update 2025]. |
| 40338461 | 10.1186/s12985-020-01485-w | 10.1007/s10123-025-00669-0 | Genomic characterization of a novel Pseudomonas aeruginosa bacteriophage represe |
| 40340326 | 10.1101/pdb.prot073411 | 10.1021/acsbiomaterials.4c02190 | Real-Time in Vivo Bacterial Imaging by Computed Tomography and Fluorescence Usin |
| 40341217 | 10.1001/jamaoncol.2016.1051 | 10.1038/s41401-025-01572-0 | Generating potent and persistent antitumor immunity via affinity-tuned CAR-T cel |
| 40343461 | 10.1177/0310057X0803600404 | 10.1007/s00103-025-04054-0 | [Phage therapeutics and pharmaceutical legislation: classification, manufacture, |
| 40347136 | 10.1186/s12859-020-03697-x | 10.1093/nar/gkaf323 | ReQuant: improved base modification calling by k-mer value imputation. |
| 40347294 | 10.3390/v13030506 | 10.1007/s00431-025-06173-x | Phage diversity in human breast milk: a systematic review. |
| 40351406 | 10.3390/ANTIBIOTICS12020389 | 10.1089/phage.2024.0009 | Phage-Encoded Antimicrobial Peptide gp28 Demonstrates LL-37-Like Antimicrobial A |
| 40357395 | 10.1128/IAI.01772-05 | 10.3389/fcimb.2025.1566495 | Wound repair and immune function in the Pseudomonas infected CF lung: before and |
| 40357396 | 10.1016/j.jmb.2017.12.007 | 10.3389/fcimb.2025.1563781 | Genomic analysis of prophages in 44 clinical strains of Pseudomonas aeruginosa i |
| 40358753 | 10.1007/s00108-021-01042-9 | 10.1007/s00103-025-04065-x | [Cost aspects and reimbursement requirements of phage therapy]. |
| 40362285 | 10.1002/prot.21165 | 10.3390/ijms26094045 | A Single-Domain VNAR Nanobody Binds with High-Affinity and Selectivity to the He |
| 40366171 | 10.1016/j.medj.2024.11.018 | 10.1128/jvi.00458-25 | Phage therapy: a promising approach for Staphylococcus aureus diabetic foot infe |
| 40368116 | 10.1042/bj20120537 | 10.1016/j.biotechadv.2025.108602 | Protease engineering: Approaches, tools, and emerging trends. |
| 40368965 | 10.1016/j.ijantimicag.2023.106856 | 10.1038/s41467-025-59806-y | Adjunctive phage therapy improves antibiotic treatment of ventilator-associated- |
| 40369432 | 10.3390/v13061013 | 10.1186/s12866-025-04005-4 | Characterization and purification of Pseudomonas aeruginosa phages for the treat |
| 40370404 | 10.3390/ijms24065596 | 10.3389/fcimb.2025.1556688 | Innovative strategies targeting oral microbial dysbiosis: unraveling mechanisms  |
| 40371968 | 10.1128/msphere.00354-23 | 10.1080/19490976.2025.2499575 | Virome drift in ulcerative colitis patients: faecal microbiota transplantation r |
| 40372520 | 10.1016/j.watres.2021.117183 | 10.1007/s12560-025-09635-5 | Presence of Potentially Infectious Human Enteric Viruses and Antibiotic Resistan |
| 40372723 | 10.1371/journal.pcbi.1002195 | 10.1093/gigascience/giaf037 | HVSeeker: a deep-learning-based method for identification of host and viral DNA  |
| 40377313 | 10.3390/ijms232416195 | 10.1128/spectrum.02849-24 | In silico and in vitro comparative analysis of 79 Acinetobacter baumannii clinic |
| 40379736 | 10.1038/s41429-024-00762-y | 10.1038/s41598-025-01704-w | In vitro activity of cefiderocol against Gram-negative aerobic bacilli in plankt |
| 40379875 | 10.1046/j.1365-2958.1998.00712.x | 10.1038/s41598-025-99981-y | Massive acquisition of conjugative and mobilizable integrated elements fuels Fae |
| 40383233 | 10.1038/s41586-024-08213-2 | 10.1016/j.addr.2025.115605 | Enabling technologies for in situ biomanufacturing using probiotic yeast. |
| 40383795 | 10.1007/s12223-012-0164-z | 10.1038/s41598-025-01489-y | Phage-antibiotic synergy to combat multidrug resistant strains of Gram-negative  |
| 40390585 | 10.1093/jpids/piab048 | 10.3346/jkms.2025.40.e161 | Antimicrobial Resistance - The 'Real' Pandemic We Are Unaware Of, Yet Nearby. |
| 40394359 | 10.3389/fcimb.2024.1428637 | 10.1007/s00103-025-04055-z | [Application of phages in farm animals, food and the environment as part of a On |
| 40396485 | 10.1016/j.xinn.2021.100141 | 10.1080/19490976.2025.2501194 | The influence of early life exposures on the infant gut virome. |
| 40400348 | 10.1128/msystems.00455-00419 | 10.1002/pro.70177 | AcrDB update: Predicted 3D structures of anti-CRISPRs in human gut viromes. |
| 40407098 | 10.1093/nar/gkab1038 | 10.1080/19490976.2025.2507775 | Adaptations in gut Bacteroidales facilitate stable co-existence with their lytic |
| 40407371 | 10.1016/j.cell.2007.11.009 | 10.1128/spectrum.03213-24 | The landscape of bacterial contractile injection systems across large-scale meta |
| 40411427 | 10.1007/978-1-60327-058-8_28 | 10.1002/pro.70145 | Synthetic antibodies targeting EphA2 induce diverse signaling-competent clusters |
| 40411603 | 10.1007/s00792-018-1052-5 | 10.1007/s00253-025-13513-2 | The impact of metagenomic analysis on the discovery of novel endolysins. |
| 40425675 | 10.1080/15548627.2019.1596481 | 10.1038/s41598-025-03044-1 | Paxilline derived from an endophytic fungus of Baphicacanthus cusia alleviates h |
| 40426494 | 10.1371/journal.pone.0168615 | 10.3390/antibiotics14050427 | Overcoming Pseudomonas aeruginosa in Chronic Suppurative Lung Disease: Prevalenc |
| 40426547 | 10.1016/j.pdpdt.2020.102002 | 10.3390/antibiotics14050481 | Pulsed Blue Light and Phage Therapy: A Novel Synergistic Bactericide. |
| 40429825 | 10.1101/2021.10.04.463034 | 10.3390/ijms26104683 | Efficient Design of Affilin® Protein Binders for HER3. |
| 40431627 | 10.1111/1462-2920.15476 | 10.3390/v17050615 | Klebsiella Lytic Phages Induce Pseudomonas aeruginosa PAO1 Biofilm Formation. |
| 40431639 | 10.1038/s41396-020-0726-z | 10.3390/v17050623 | Acinetobacter baumannii and Klebsiella pneumoniae Isolates Obtained from Intensi |
| 40431712 | 10.1038/s41591-019-0437-z | 10.3390/v17050701 | Treatment of E. coli Infections with T4-Related Bacteriophages Belonging to Clas |
| 40439402 | 10.15585/mmwr.rr7302a1 | 10.1128/cmr.00107-24 | Biologic drug development for treatment and prevention of sexually transmitted i |
| 40441534 | 10.1128/microbiolspec.gpp3-0018-2018 | 10.1016/j.jbc.2025.110295 | Structural and functional insights into Listeriamonocytogenes phage endolysin Pl |
| 40442286 | 10.1016/j.micinf.2021.104929 | 10.1038/s41598-025-04106-0 | The phi027 bacteriophage influences physiology and virulence of the lysogenic st |
| 40443649 | 10.1126/sciadv.adf3700 | 10.3389/fimmu.2025.1574958 | Bispecific antibody targeting shared indel-derived neoantigen of APC. |
| 40444030 | 10.5281/zenodo.5905965 | 10.12688/f1000research.109236.2 | Evidence of SARS-CoV-2 bacteriophage potential in human gut microbiota. |
| 40446071 | 10.1038/s41586-022-05647-4 | 10.1371/journal.pbio.3003203 | DnaJ mediates phage sensing by the bacterial NLR-related protein bNACHT25. |
| 40448542 | 10.1111/ajt.15503 | 10.1093/jac/dkaf163 | Reversal of phenotypic resistance in multi-drug resistant carbapenemase-producin |
| 40448711 | 10.1128/AEM.01746-19 | 10.1007/s00294-025-01318-9 | Whole genome sequence analysis of multidrug-resistant Salmonella enterica Typhim |
| 40448719 | 10.1038/s41598-021-81366-6 | 10.1007/s00262-025-04075-3 | Cancer therapy via neoepitope-specific monoclonal antibody cocktails. |
| 40448871 | 10.1128/IAI.67.4.1974-1981.1999 | 10.1007/s00294-025-01317-w | First characterization of the resistome, virulome and genomic diversity of Salmo |
| 40453094 | 10.3390/ijms21082999 | 10.3389/fimmu.2025.1574755 | Engineered sequestrins inhibit aggregation of pathogenic alpha-synuclein mutants |
| 40454480 | 10.1080/19490976.2022.2118811 | 10.1172/JCI184323 | Present and future of microbiome-targeting therapeutics. |
| 40461465 | 10.1093/ajcp/60.2.234 | 10.1038/s41522-025-00728-4 | Activity of GS-linked chimeric endolysin CHAPk-SH3bk against methicillin-resista |
| 40464639 | 10.1126/science.aba5257 | 10.1080/19490976.2025.2508426 | Implications of gut microbiota-mediated epigenetic modifications in intestinal d |
| 40467884 | 10.1186/gb-2011-12-6-r60 | 10.1038/s41598-025-04494-3 | Characterization of a plasmid dependent DNA phage targeting Escherichia coli har |
| 40469300 | 10.1182/blood.2019004701 | 10.3389/fimmu.2025.1572676 | Combined treatment with anti-PSMA antibody and human peripheral blood-derived NK |
| 40471671 | 10.3389/fpubh.2023.1228134 | 10.1097/WCO.0000000000001395 | Novel techniques for the diagnosis of neurological infections. |
| 40476553 | 10.3390/antib8020032 | 10.3892/mmr.2025.13583 | Development of an innovative approach for early diagnosis of cervical cancer usi |
| 40481890 | 10.1021/acsomega.8b02366 | 10.1007/s00253-025-13530-1 | Development of antibodies against severe fever with thrombocytopenia syndrome vi |
| 40487314 | 10.3389/fmicb.2017.00403 | 10.3389/fcimb.2025.1597009 | Systematic bacteriophage selection for the lysis of multiple Pseudomonas aerugin |
| 40488994 | 10.1186/s12951-020-0588-6 | 10.1007/s11033-025-10683-0 | Novel therapeutic strategies targeting infections caused by P. aeruginosa biofil |
| 40489497 | 10.37349/ei.2022.00054 | 10.1371/journal.pone.0325389 | Combining CD3/GD2 bispecific T cell engager with human Vγ9Vδ2 T cells facilitate |
| 40489625 | 10.2210/pdb9DBO/pdb | 10.1073/pnas.2424679122 | Conformation-specific synthetic intrabodies modulate mTOR signaling with subcell |
| 40492711 | 10.1038/nmicrobiol.2017.79 | 10.1128/spectrum.02882-24 | Phage steering in the presence of a competing bacterial pathogen. |
| 40493666 | 10.1016/b978-0-12-374407-4.00265-x | 10.1371/journal.pone.0325832 | Comparative genomics of Lentilactobacillus buchneri reveals strain-level hyperdi |
| 40496019 | 10.1002/advs.202404049 | 10.3389/fcimb.2025.1611857 | Optimizing phage therapy with artificial intelligence: a perspective. |
| 40498839 | 10.1101/2023.08.15.553228 | 10.1126/sciadv.ads5589 | Phage display enables machine learning discovery of cancer antigen-specific TCRs |
| 40503217 | 10.1017/S0950268805004723 | 10.1155/tbed/9937941 | Application of a Quantitative Real-Time PCR Assay for Early Detection of Salmone |
| 40507880 | 10.1136/jitc-2023-007253 | 10.3390/ijms26115068 | Anti-Tumor Activities of Anti-Siglec-15 Chimeric Heavy-Chain Antibodies. |
| 40507995 | 10.1093/protein/1.2.107 | 10.3390/ijms26115186 | An Anti-BCMA Affibody Affinity Protein for Therapeutic and Diagnostic Use in Mul |
| 40508063 | 10.3791/62950 | 10.3390/ijms26115254 | Inhibiting Infectious Bronchitis Virus PLpro Using Ubiquitin Variants. |
| 40508147 | 10.1016/j.virusres.2023.199178 | 10.3390/ijms26115337 | Phage-Antibiotic Synergy Enhances Biofilm Eradication and Survival in a Zebrafis |
| 40509211 | 10.1021/acsomega.2c07740 | 10.3390/molecules30112323 | Photocatalysis and Photodynamic Therapy in Diabetic Foot Ulcers (DFUs) Care: A N |
| 40515926 | 10.1038/s41586-020-2180-5 | 10.1007/978-1-0716-4615-1_31 | Applying Phage Display Technology to Obtain Specific Peptides Blocking Host-Viru |
| 40526416 | 10.1101/gr.gr-1531rr | 10.1099/mgen.0.001423 | Bacteriophages in Pseudomonas aeruginosa evade the CRISPR-Cas I-F system by depl |
| 40537692 | 10.1016/J.MICPATH.2024.107056 | 10.1007/s10123-025-00686-z | Characterization and genome analyses of the novel phages targeting extraintestin |
| 40539793 | 10.1093/bioinformatics/btx440 | 10.1128/mra.01044-23 | Viral whole-genome sequences of Pseudomonas jumbo phages, ΦNK1 and ΦBrmt, from s |
| 40540458 | 10.1111/jam.15809 | 10.1371/journal.pone.0325235 | SARS-CoV-2 survival on skin and its transfer from contaminated surfaces. |
| 40542350 | 10.3389/fimmu.2021.658420 | 10.1186/s10020-025-01286-3 | Effect of anti-CD4 mAb induced by inhibiting B cell disorder on immune reconstru |
| 40542420 | 10.1093/nar/gkab951 | 10.1186/s40168-025-02144-4 | Metagenomic analysis reveals gut phage diversity across three mammalian models. |
| 40542451 | 10.1038/srep16807 | 10.1186/s40168-025-02046-5 | Engrafting gut bacteriophages have potential to modulate microbial metabolism in |
| 40544449 | 10.3168/jds.2018-15044 | 10.1016/j.xpro.2025.103917 | Protocol to study the inter-relationship between phageome and lipidome in low-vo |
| 40553506 | 10.1093/cid/ciab784 | 10.1099/mgen.0.001428 | Fast and accurate in silico antigen typing with Kaptive 3. |
| 40558128 | 10.1371/journal.pone.0064671 | 10.3390/antibiotics14060538 | Efficacy of Endolysin LysAB1245 Combined with Colistin as Adjunctive Therapy Aga |
| 40562779 | 10.4161/19420862.2015.989047 | 10.1080/19420862.2025.2516676 | Developing drug-like single-domain antibodies (VHH) from in vitro libraries. |
| 40565548 | 10.1038/s41598-020-69944-6 | 10.3390/genes16060656 | Diversity and Role of Prophages in Pseudomonas aeruginosa: Resistance Genes and  |
| 40568115 | 10.1038/s41586-024-08547-x | 10.1101/2025.03.31.646159 | END nucleases: Antiphage defense systems targeting multiple hypermodified phage  |
| 40573368 | 10.3390/v15081665 | 10.3390/v17060778 | Dual Nature of Bacteriophages: Friends or Foes in Minimally Processed Food Produ |
| 40574860 | 10.1016/j.bcp.2018.04.014 | 10.3389/fimmu.2025.1599764 | Targeting CD16A on NK cells and GPC3 in hepatocellular carcinoma: development an |
| 40576476 | 10.1080/21505594.2015.1036218 | 10.1128/msystems.00282-25 | Characterization of the virulence shaping and adaptability in the methicillin-re |
| 40581770 | 10.1186/gb-2007-8-11-R254 | 10.1080/19420862.2025.2522838 | Discovery of broadly neutralizing VHHs against short-chain α-neurotoxins using a |
| 40585316 | 10.1186/1476-9433-2-2 | 10.1016/j.bioflm.2024.100245 | Combination of phages and antibiotics with enhanced killing efficacy against dua |
| 40586964 | 10.1080/01140671.2024.2414802 | 10.1007/s00284-025-04345-4 | The Impact of Antibiofilm Strategies in Controlling Microbial Colonization. |
| 40593506 | 10.1093/gigascience/giac076 | 10.1038/s41467-025-60598-4 | Phage therapy with nebulized cocktail BX004-A for chronic Pseudomonas aeruginosa |
| 40594778 | 10.1109/TNB.2022.3201237 | 10.1038/s41598-025-07501-9 | Design and numerical evaluation of a high sensitivity plasmonic biosensor based  |
| 40595615 | 10.1214/14-EJS890 | 10.1038/s41467-025-61268-1 | Macrophage-induced reduction of bacteriophage density limits the efficacy of in  |
| 40596331 | 10.1007/s00253-022-12339-6 | 10.1038/s41598-025-08032-z | Engineering M13 bacteriophage to display HER2 mimotopes on pVIII for vaccine dev |
| 40596635 | 10.1128/cmr.00024-23 | 10.1038/s41598-025-08759-9 | In vitro activity of phages against periprosthetic joint infection-associated st |
| 40596837 | 10.1016/j.ijantimicag.2023.106941 | 10.1186/s12864-025-11756-x | Genomic and functional insights into commensal streptococci with anti-pneumococc |
| 40596887 | 10.1016/j.clinthera.2023.06.009 | 10.1186/s12879-025-11258-x | Efficacy of phage therapy in Diabetic Foot Ulcers (DFUs): a systematic review. |
| 40600689 | 10.1016/j.addr.2019.08.010.Domesticating | 10.1002/jbm.b.35612 | Mineral-Binding Peptide Inhibits Ectopic Mineralization Secondary to Bone Morpho |
| 40600714 | 10.1093/bioinformatics/bts014 | 10.1128/spectrum.00013-25 | Biases and complementarity in gut viromes obtained from bulk and virus-like part |
| 40601145 | 10.1038/ng1201-365 | 10.1007/978-1-0716-4595-6_7 | Protein Microarray Analysis with GenePix. |
| 40601153 | 10.1074/mcp.M114.045328 | 10.1007/978-1-0716-4595-6_15 | Cytokine Antibody Microarray-Based Proteomic Strategies for Characterizing the D |
| 40604156 | 10.1038/nmeth.4468 | 10.1038/s42255-025-01318-6 | Multi-omic analysis reveals transkingdom gut dysbiosis in metabolic dysfunction- |
| 40604283 | 10.1101/2021.03.08.434280 | 10.1038/s41586-025-09204-7 | Functional amyloid proteins confer defence against predatory bacteria. |
| 40608147 | 10.1016/S1473-3099(21)00612-5 | 10.1007/s00430-025-00844-0 | Fighting biofilm: bacteriophages eliminate biofilm formed by multidrug-resistant |
| 40608189 | 10.1186/s12974-020-1705-z | 10.1007/s12017-025-08870-0 | Dysbiosis and Neurodegeneration in ALS: Unraveling the Gut-Brain Axis. |
| 40611420 | 10.1007/s00253-005-1922-5 | 10.2174/0109298665372719250616085616 | Engineered Bacteriophages: Advances in Phage Genome Redesign Strategies for Ther |
| 40615839 | 10.3109/10428194.2013.778407 | 10.1186/s12943-025-02393-9 | Targeting CD30L in B-cell non-Hodgkin lymphoma: novel peptide conjugates and the |
| 40617850 | 10.1371/journal.pcbi.1009442 | 10.1038/s41522-025-00760-4 | Multi-kingdom microbiota analysis reveals bacteria-viral interplay in IBS with d |
| 40618116 | 10.1016/j.chom.2020.06.011 | 10.1186/s12985-025-02856-x | Analysis of the overall development trends and hotspots in the research field of |
| 40618137 | 10.3389/fvets.2020.513770 | 10.1186/s12917-025-04877-8 | Isolation and characterization of Pseudomonas phage HJ01 and its therapeutic eff |
| 40619813 | 10.1109/TMBMC.2024.3476192 | 10.1093/bib/bbaf323 | Integrative systems biology approaches for analyzing microbiome dysbiosis and sp |
| 40621926 | 10.1371/journal.pone.0061217 | 10.1128/spectrum.01720-24 | Deciphering the comprehensive microbiome of glacier-fed Ganges and functional as |
| 40622660 | 10.1186/s12974-020-01961-8 | 10.1007/s12264-025-01443-y | Viewing Psychiatric Disorders Through Viruses: Simple Architecture, Burgeoning I |
| 40626364 | 10.1186/1471-2105-10-421 | 10.1172/jci.insight.183123 | Identification of bacteriophage DNA in human umbilical cord blood. |
| 40631381 | 10.1007/s13105-011-0115-1 | 10.1080/21505594.2025.2530660 | Moderate altitude exposure impacts extensive host-microbiota multi-kingdom conne |
| 40631624 | 10.1107/S0907444904019158 | 10.1021/acs.biochem.5c00142 | Pseudomonas aeruginosa Cryptic Prophage Endolysin Is a Highly Active Muramidase. |
| 40632445 | 10.1002/rmv.2041 | 10.1007/s12033-025-01466-w | Insight into Bacteriophage Therapy for Bacterial Infections and Cancer. |
| 40636261 | 10.1007/s004380051128 | 10.3389/fcimb.2025.1561443 | High-yield bioproduction of virus-free virus-like P4-EKORhE multi-lysin transduc |
| 40637714 | 10.1111/mmi.12048 | 10.7554/eLife.102743 | Bacteriophage infection drives loss of β-lactam resistance in methicillin-resist |
| 40637811 | 10.3390/v14102260 | 10.1007/s11262-025-02175-x | The C-terminus of the tail fiber protein of PB1-like phages is responsible for t |
| 40642983 | 10.1128/JB.184.16.4529-4535.2002 | 10.1128/spectrum.03332-24 | Characterization of a novel Phietavirus genus bacteriophage and its potential fo |
| 40649886 | 10.1093/nar/gkr485 | 10.3390/ijms26136106 | Study of lug Operon, SCCmec Elements, Antimicrobial Resistance, MGEs, and STs of |
| 40649960 | 10.1016/j.peptides.2012.09.021 | 10.3390/ijms26136183 | Phage-Microbiota Crosstalk: Implications for Central Nervous System Disorders. |
| 40652263 | 10.1007/978-1-61779-080-5_20 | 10.1186/s12985-025-02848-x | Efficacy of phage vB_Ps_ZCPS13 in controlling Pan-drug-resistant Pseudomonas aer |
| 40670809 | 10.3389/FMICB.2016.01761 | 10.1007/s00284-025-04370-3 | Unravelling the Gut-Microbiome-Brain Axis: Implications for Infant Neurodevelopm |
| 40671354 | 10.1038/s41551-024-01263-x | 10.1002/pro.70184 | Design of a water-soluble CD20 antigen with computational epitope scaffolding. |
| 40679920 | 10.1038/s41586-024-07461-6 | 10.1021/jacs.5c04424 | Macrocyclic Phage Display for Identification of Selective Protease Substrates. |
| 40684166 | 10.2217/fmb.14.64 | 10.1186/s12985-025-02859-8 | Isolation and characterization of a novel bacteriophage PUTH1 active against Pse |
| 40694848 | 10.1099/mgen.0.001361 | 10.1093/nar/gkaf652 | The extended mobility of plasmids. |
| 40698811 | 10.1046/j.1365-2958.2002.02984.x | 10.1128/aac.00579-25 | Complementary killing activities of Pbunavirus LS1 and Bruynoghevirus LUZ24 phag |
| 40700354 | 10.1101/2024.01.12.575420 | 10.1172/JCI177872 | Prophage-encoded methyltransferase drives adaptation of community-acquired methi |
| 40702445 | 10.1096/fj.10-158972 | 10.1186/s12866-025-04177-z | Filamentous prophages in the genomes of Acinetobacter baumannii from egypt: impa |
| 40707855 | 10.1002/cncr.11560 | 10.1007/s12033-025-01480-y | Characterization of a Phage Display-Selected scFv Against Neuropilin 1 (NRP1) Is |
| 40707891 | 10.1128/mmbr.00014-11 | 10.1186/s12879-025-11325-3 | Isolation and characterization of bacteriophages with lytic activity against mul |
| 40709915 | 10.3389/fmicb.2017.00252 | 10.1099/mgen.0.001437 | Vibrio cholerae lineage and pangenome diversity vary geographically across Bangl |
| 40711306 | 10.2174/1574884715666200330105411 | 10.3390/vetsci12070646 | Antimicrobial Potential of Bacteriophages JG005 and JG024 Against Pseudomonas ae |
| 40713701 | 10.1111/php.12014 | 10.1186/s12985-025-02739-1 | Identification and profiling of novel metagenome assembled uncultivated virus ge |
| 40715909 | 10.3389/fmicb.2025.1572400 | 10.1007/s11033-025-10773-z | A narrative overview of Staphylococcus haemolyticus: resistance traits, virulenc |
| 40715914 | 10.3390/vaccines9111300 | 10.1007/s10123-025-00698-9 | Domain antibody-displayed phages as a novel biofilm-targeted therapy for Staphyl |
| 40719460 | 10.1093/nargab/lqaa023 | 10.1128/msphere.00198-25 | The salivary virome during childhood dental caries. |
| 40720171 | 10.1038/s41592-022-01666-1 | 10.1093/bfgp/elaf011 | Genomic insights into bacteriophages: a new frontier in AMR detection and phage  |
| 40723871 | 10.1128/JB.00780-13 | 10.3390/biom15070999 | 3-O Sulfated Heparan Sulfate (G2) Peptide Ligand Impairs the Infectivity of Chla |
| 40723932 | 10.1007/s11274-020-02964-6 | 10.3390/antibiotics14070629 | The Ability of Bacteriophages to Reduce Biofilms Produced by Pseudomonas aerugin |
| 40723971 | 10.1006/meth.2001.1262 | 10.3390/antibiotics14070668 | Transcriptomic Analysis of Biofilm Formation Inhibition by PDIA Iminosugar in St |
| 40724203 | 10.1016/j.amjmed.2019.02.005 | 10.3390/ijerph22071139 | Exploration of Providers' Perceptions and Attitudes Toward Phage Therapy and Int |
| 40725204 | 10.1101/2024.10.29.620919 | 10.3390/ijms26146958 | The Impact of Fusobacterium nucleatum and the Genotypic Biomarker KRAS on Colore |
| 40730160 | 10.1021/acs.est.7b02703 | 10.1016/j.chom.2025.07.004 | The prototypic crAssphage is a linear phage-plasmid. |
| 40730656 | 10.1126/science.ads6055 | 10.1038/s41577-025-01206-w | Manipulation of the nucleotide pool in human, bacterial and plant immunity. |
| 40732096 | 10.3390/v16071000 | 10.3390/microorganisms13071587 | Characterization, Genomic Analysis and Application of Five Lytic Phages Against  |
| 40733529 | 10.1016/S1473-3099(24)00424-9 | 10.3390/v17070911 | Armed Phages: A New Weapon in the Battle Against Antimicrobial Resistance. |
| 40733556 | 10.1128/AAC.44.12.3317-3321.2000 | 10.3390/v17070938 | Therapeutic Optimization of Pseudomonas aeruginosa Phages: From Isolation to Dir |
| 40733588 | 10.1093/jac/dkw083 | 10.3390/v17070971 | Marine Bacteriophages as Next-Generation Therapeutics: Insights into Antimicrobi |
| 40733592 | 10.1021/cr400166n | 10.3390/v17070975 | A Beautiful Bind: Phage Display and the Search for Cell-Selective Peptides. |
| 40733628 | 10.1016/j.jenvman.2025.125399 | 10.3390/v17071012 | CrAssphage as a Human Enteric Viral Contamination Bioindicator in Marketed Bival |
| 40738105 | 10.1038/msb4100050 | 10.1016/j.chom.2025.07.005 | Metagenomic selections reveal diverse antiphage defenses in human and environmen |
| 40739242 | 10.1073/PNAS.1305923110/ | 10.1186/s12985-025-02885-6 | Isolation and characterization of phages ΦZC2 and ΦZC3 against carbapenem-resist |
| 40742547 | 10.1002/mlf2.12064 | 10.1007/s00203-025-04399-9 | Role of the microbiome in diabetic wound healing: implications for new therapeut |
| 40745439 | 10.1016/j.aca.2022.340157 | 10.1038/s41598-025-12574-7 | Identification of novel human IgE-binding peptides from a phage display library  |
| 40745479 | 10.1002/anie.202407131 | 10.1038/s41589-025-01971-8 | Structure-guided phage display discovery of antibodies for (S)Tn-glycans in prot |
| 40745494 | 10.1056/NEJMra040181 | 10.1007/s00132-025-04690-z | [Bacteriophages for the treatment of musculoskeletal infections-An overview of c |
| 40748062 | 10.1146/annurev-virology-091919-074551 | 10.1128/aem.00919-25 | Decoding the human phageome helps to unravel microbial dynamics in health and di |
| 40751137 | 10.3390/v10040178 | 10.1186/s12866-025-04228-5 | Characterization of a lytic phage and its efficacy against carbapenem-resistant  |
| 40751804 | 10.1007/s00705-022-05425-7 | 10.1007/s00253-025-13559-2 | Genomic characterization and pre-clinical evaluation of a new polyvalent lytic L |
| 40754853 | 10.1155/2021/8030297 | 10.1080/19490976.2025.2526719 | Single cell viral tagging of Faecalibacterium prausnitzii reveals rare bacteriop |
| 40757862 | 10.48550/arXiv.2303.08774 | 10.1128/aem.02014-24 | CRISPR-Cas9 enables efficient genome engineering of the strictly lytic, broad-ho |
| 40758691 | 10.1038/s42003-021-02034-z | 10.1371/journal.pone.0322021 | scFv intrabody targeting wildtype TDP-43 presents protective effects in a cellul |
| 40759399 | 10.1101/2024.02.02.578711 | 10.1016/j.addr.2025.115662 | Towards airway microbiome engineering for improving respiratory health. |
| 40762578 | 10.2147/DDDT.S94505 | 10.1128/spectrum.00716-25 | Use of the bacteriophage-derived endolysin CHAPK-SH3blys as a potent novel treat |
| 40763034 | 10.1093/jacamr/dlab179 | 10.1016/j.xpro.2025.104012 | Protocol for end-design-free rebooting of terminally redundant Pseudomonas phage |
| 40764322 | 10.1007/s12575-009-9008-x | 10.1038/s41598-025-07320-y | Phage-mediated TLR2 signaling attenuates intracellular Mycobacterium abscessus s |
| 40766552 | 10.1038/nmeth1083 | 10.1101/2025.07.28.667140 | Targeted disruption of phage liquid crystalline droplets abolishes antibiotic to |
| 40770084 | 10.1186/s13293-023-00490-2 | 10.1038/s41423-025-01326-2 | The gut microbiota in cancer immunity and immunotherapy. |
| 40770906 | 10.3389/fmicb.2023.1162380 | 10.1002/mbo3.70043 | Microbiota-Host Interactions: Exploring Their Dynamics and Contributions to Huma |
| 40771816 | 10.1093/nar/gkae973 | 10.3389/fimmu.2025.1605434 | Innovative microbial strategies in atopic dermatitis. |
| 40774387 | 10.1101/2024.09.06.611391 | 10.1016/j.jbc.2025.110564 | Identification and characterization of nanobodies specific for the human ubiquit |
| 40781808 | 10.3389/fmicb.2024.1469414 | 10.1080/17460913.2025.2535901 | The effect of bacteriophage in oral health: developing microbial ecology and eme |
| 40788302 | 10.1038/nature12155 | 10.7554/eLife.102352 | A biofilm-tropic Pseudomonas aeruginosa bacteriophage uses the exopolysaccharide |
| 40790594 | 10.3389/fmicb.2021.674068 | 10.1186/s12929-025-01169-z | Therapeutic application of a jumbo bacteriophage against metallo-β-lactamase pro |
| 40790871 | 10.3390/antibiotics9040155 | 10.1080/10717544.2025.2544683 | Inhalable nanoparticle-based delivery systems for the treatment of pulmonary inf |
| 40792102 | 10.1016/j.micres.2023.127369 | 10.3389/fcimb.2025.1644286 | Prevalence and genomic insights into type III-A CRISPR-Cas system acquisition in |
| 40794529 | 10.1146/annurev.biochem.71.110601.135414 | 10.1099/jmm.0.001997 | The relationship between respiratory tract infections caused by toxin-producing  |
| 40794809 | 10.3389/fmicb.2019.01674 | 10.1093/jac/dkaf293 | Phages connect the biological dots of antimicrobial resistance: from genesis and |
| 40796239 | 10.1021/acs.orglett.3c01799 | 10.1093/glycob/cwaf042 | Evaluation of multiplexed liquid glycan Array (LiGA) for serological detection o |
| 40804103 | 10.1586/14787210.2014.864553 | 10.1038/s41598-025-14811-5 | Isolation and characterization of novel bacteriophages targeting Stenotrophomona |
| 40806172 | 10.3389/fphys.2017.00984 | 10.3390/ijms26157040 | Hydroxyapatite Scaffold and Bioactive Factor Combination as a Tool to Improve Os |
| 40806179 | 10.1080/08916934.2017.1300884 | 10.3390/ijms26157048 | Anti-C1q Autoantibody-Binding Engineered scFv C1q-Mimicking Fragment Enhances Di |
| 40806682 | 10.1016/j.micpath.2024.106835 | 10.3390/ijms26157550 | Visible-Light-Driven Degradation of Biological Contaminants on the Surface of Te |
| 40807307 | 10.1021/acssynbio.5b00296 | 10.3390/molecules30153132 | Synthetic and Functional Engineering of Bacteriophages: Approaches for Tailored  |
| 40808547 | 10.1007/978-1-59745-198-7_203 | 10.1080/19420862.2025.2543769 | Pioneer: a synthetic human antibody phage display library for rapid therapeutic  |
| 40810510 | 10.1126/sciadv.abf8711 | 10.1128/mbio.01698-25 | AcrIF11 is a potent CRISPR-specific ADP-ribosyltransferase encoded by phage and  |
| 40810601 | 10.1038/s41564-020-00830-7 | 10.1128/spectrum.00855-25 | Overcoming phage resistance: efficacy of sequential phage-colistin therapy again |
| 40812186 | 10.3390/v12111268 | 10.1016/j.chom.2025.07.016 | Pseudomonads coordinate innate defense against viruses and bacteria with a singl |
| 40815144 | 10.1016/j.ijmmb.2023.100432 | 10.1128/spectrum.02019-25 | A novel broad host range phage phiA85 displays a synergistic effect with antibio |
| 40815168 | 10.7759/cureus.62717 | 10.1128/msystems.00797-25 | Genotypic and phenotypic characterization of Staphylococcus aureus isolated from |
| 40815439 | 10.3390/antibiotics8030103 | 10.1007/s42770-025-01762-2 | Pharmacological evaluation of phage-antibiotic synergism against clinical isolat |
| 40815472 | 10.21769/BioProtoc.2042 | 10.1128/msystems.00428-25 | Systematic evaluation of phenotypic variations induced by prophages in a clinica |
| 40817579 | 10.1016/B978-0-12-801238-3.66117-2 | 10.1002/adhm.202501426 | Biologically Active Implants Prevent Mortality in a Mouse Sepsis Model. |
| 40821985 | 10.1186/s12917-018-1703-x | 10.7717/peerj.19758 | The concentration of single-stranded DNA-binding proteins is a critical factor i |
| 40823824 | 10.1038/s41592-022-01585-1 | 10.1128/mbio.02135-25 | The evolutionary replacement of restriction-modification by Ssp antiviral system |
| 40823828 | 10.3791/4019 | 10.1128/mbio.01621-25 | Temperate phages increase antibiotic effectiveness in a Caenorhabditis elegans i |
| 40823833 | 10.4315/0362-028X-47.7.520 | 10.1128/mbio.01963-25 | Rapid, low-cost colorimetric detection of Salmonella Typhi bacteriophages for en |
| 40828859 | 10.1101/gr.849004 | 10.1371/journal.pgen.1011831 | Deciphering the RNA-based regulation mechanism of the phage-encoded AbiF system  |
| 40830371 | 10.1099/jgv.0.001840 | 10.1038/s41598-025-00449-w | Augmenting phage therapy using green nanotechnology for promising infection cont |
| 40833127 | 10.1016/j.tube.2022.102269 | 10.1128/jcm.00841-25 | Luciferase reporter mycobacteriophage (TM4::GeNL) enables rapid assessment of dr |
| 40836306 | 10.1093/bioinformatics/btq033 | 10.1186/s13059-025-03733-0 | Highly accurate prophage island detection with PIDE. |
| 40838716 | 10.3389/fmicb.2019.01984 | 10.1128/mmbr.00244-25 | Shiga toxin-producing Escherichia coli, food contamination, and bacteriophages a |
| 40839234 | 10.1080/10408398.2021.1937510 | 10.1007/s12560-025-09661-3 | Simultaneous Detection of HEV, HAstV and SaV in Bivalve Shellfish Using a Novel  |
| 40869015 | 10.1002/pro.4519 | 10.3390/ijms26167694 | Zeta CrAss-like Phages, a Separate Phage Family Using a Variety of Adaptive Mech |
| 40869155 | 10.1016/j.nut.2018.06.004 | 10.3390/ijms26167837 | Bacteriophages, Antibiotics and Probiotics: Exploring the Microbial Battlefield  |
| 40872794 | 10.1073/pnas.2206739119 | 10.3390/v17081080 | Biocontrol of Phage Resistance in Pseudomonas Infections: Insights into Directed |
| 40872802 | 10.3390/ijms221910350 | 10.3390/v17081088 | Pseudomonas Phage Banzai: Genomic and Functional Analysis of Novel Pbunavirus wi |
| 40872808 | 10.2174/138920110790725401 | 10.3390/v17081094 | Phage Therapy: Combating Evolution of Bacterial Resistance to Phages. |
| 40872831 | 10.3390/v13071268 | 10.3390/v17081118 | First Use of Phage Therapy in Canada for the Treatment of a Life-Threatening, Mu |
| 40873574 | 10.1038/nrclinonc.2017.148 | 10.3389/fimmu.2025.1625813 | Dual T/NK cell engagement via B7-H6-targeted bispecific antibodies and IL-15 era |
| 40877501 | 10.1016/j.jmb.2005.03.013 | 10.1007/978-1-0716-4742-4_4 | Effects of Nucleoside Modifications on mRNA Translation: Choosing the Right Modi |
| 40878383 | 10.1134/S0026261710010078 | 10.1093/g3journal/jkaf203 | Genomic correlates of tailocin sensitivity in Pseudomonas syringae. |
| 40879164 | 10.1186/1471-2180-11-258 | 10.1093/ismejo/wraf193 | Enrichment of horizontally transferred gene clusters in bacterial extracellular  |
| 40881285 | 10.3389/fmicb.2018.01685 | 10.3389/fmicb.2025.1535506 | Phenotypic and genomic analyses of the probiotic Enterococcus casseliflavus SHAM |
| 40889802 | 10.1038/nm.3931 | 10.1136/jitc-2024-011331 | Nanofilament immunotherapy induces potent antitumor vaccine responses. |
| 40890562 | 10.1128/spectrum.03884-23 | 10.1007/s12223-025-01322-z | Colistin resistance in the era of antimicrobial resistance: challenges and strat |
| 40891848 | 10.1128/aem.00700-24 | 10.1128/aem.01379-25 | Emergence of transmissible mcr-9.1 plasmids in clinical Cronobacter sakazakii: C |
| 40892293 | 10.1371/JOURNAL.PONE.0029446 | 10.1007/s00430-025-00852-0 | Antibiotic-resistant Acinetobacter baumannii can be killed by a combination of b |
| 40895545 | 10.4046/trd.2023.0107 | 10.3389/fimmu.2025.1646134 | Developing and validating anti-ADA2 single-chain antibodies coupled to alkaline  |
| 40897178 | 10.1093/bioinformatics/btp033 | 10.1016/j.xcrm.2025.102325 | Oral virome metagenomic catalog links Porphyromonas gingivalis phages to obesity |
| 40900037 | 10.1371/journal.ppat.1000894 | 10.1128/iai.00314-25 | Timely excision of prophage Φ13 is essential for the Staphylococcus aureus infec |
| 40900999 | 10.1093/nar/gkad382 | 10.3389/fcimb.2025.1617101 | EPEC autotransporter adhesin (Eaa): a novel adhesin identified in atypical enter |
| 40901954 | 10.5281/zenodo.3576630 | 10.1126/sciadv.adx9722 | The discovery of a Legionella phage explains a key determinant of human disease. |
| 40904102 | 10.6084/m9.figshare.c.7947691 | 10.1098/rstb.2024.0474 | Phage provoke growth delays and SOS response induction despite CRISPR-Cas protec |
| 40904105 | 10.6084/m9.figshare.c.7921350 | 10.1098/rstb.2024.0473 | Phage susceptibility to a minimal, modular synthetic CRISPR-Cas system in Pseudo |
| 40904107 | 10.1126/science.ads0768 | 10.1098/rstb.2024.0076 | Lineage-specific defence systems of pandemic Vibrio cholerae. |
| 40904112 | 10.6084/m9.figshare.c.7911170 | 10.1098/rstb.2024.0080 | Bacteria-phage infection network structure and genomic defence system content pr |
| 40904117 | 10.6084/m9.figshare.c.7921380 | 10.1098/rstb.2024.0073 | The H-NS homologues MvaT and MvaU repress CRISPR-Cas in Pseudomonas aeruginosa. |
| 40905702 | 10.1093/molbev/mst010 | 10.1128/mbio.01807-25 | Phenotypic heterogeneity of capsule production across opportunistic pathogens. |
| 40907025 | 10.1128/aac.00037-23 | 10.1097/AOG.0000000000006060 | Updates in Clinical Management of Recurrent Urinary Tract Infections. |
| 40909725 | 10.1101/gr.280248.124 | 10.1101/2025.08.30.673261 | Gabija restricts phages that antagonize a conserved host DNA repair complex. |
| 40910769 | 10.1093/nar/gkae1011 | 10.1128/spectrum.00597-25 | Isolation and characterization of bacteriophages from clinical enterohemorrhagic |
| 40914165 | 10.1101/gr.1239303 | 10.1016/j.xcrm.2025.102289 | Lung virome convergence precedes hospital-acquired pneumonia in intubated critic |
| 40916842 | 10.1186/s40659-024-00485-2 | 10.1080/22221751.2025.2558877 | Anti-plasmid defense in hypervirulent Klebsiella pneumoniae involves Type I-like |
| 40919817 | 10.1128/AAC.05251-11 | 10.1128/mbio.01685-25 | Prophage-encoded virulence factor, Gp05, contributes to endothelial cell dysfunc |
| 40920032 | 10.3389/fcimb.2024.1462620 | 10.1128/mbio.01822-25 | Reprogramming resistance: phage-antibiotic synergy targets efflux systems in ESK |
| 40921744 | 10.1038/s41587-023-02034-w | 10.1038/s41564-025-02088-3 | Multigenerational proteolytic inactivation of restriction upon subtle genomic hy |
| 40932609 | 10.1136/BMJOPEN-2018-022938 | 10.1007/s00203-025-04451-8 | Characterization of the novel Cutibacterium acnes phage KIT08 and its associated |
| 40936197 | 10.1021/ct400341p | 10.1080/19420862.2025.2553624 | Rational design of antibodies with pH-dependent antigen-binding properties using |
| 40942109 | 10.1016/j.jddst.2020.102174 | 10.3390/molecules30173585 | A Pre-Formulation Study for Delivering Nucleic Acids as a Possible Gene Therapy  |
| 40942166 | 10.3389/fmicb.2015.00343 | 10.3390/molecules30173641 | Bacteriophage Power: Next-Gen Biocontrol Strategies for Safer Meat. |
| 40943403 | 10.3389/fmolb.2021.672518 | 10.3390/ijms26178482 | Formation of 3D Human Osteoblast Spheroids Incorporating Extracellular Matrix-Mi |
| 40943617 | 10.3390/v17050615 | 10.3390/ijms26178699 | Bacteriophage-Based Approach Against Biofilm Infections Associated with Medical  |
| 40948444 | 10.1101/gr.1239303 | 10.1080/19490976.2025.2559019 | Use of proximity ligation shotgun metagenomics to investigate the dynamics of pl |
| 40948461 | 10.1002/adma.202405331 | 10.1080/19490976.2025.2560695 | The intratumoral microbiota in breast cancer: from basic research to clinical tr |
| 40951315 | 10.1093/nar/gkad382 | 10.3389/fcimb.2025.1636071 | CRISPR typing and phage content of colonizing Group B Streptococci from healthy  |
| 40956426 | 10.18632/oncotarget.23706 | 10.1007/s00203-025-04465-2 | Bacterial type IV secretion systems and spread of antimicrobial resistance: a st |
| 40957771 | 10.1016/j.ard.2025.04.027 | 10.1016/j.ard.2025.08.023 | Myositis-specific autoantibodies recognising Mi2 also target the AIRE protein at |
| 40960506 | 10.1093/ve/veaa060 | 10.1007/s00284-025-04478-6 | Isolation and Characterization of A Novel Pbunavirus with Promising Antibiofilm  |
| 40963058 | 10.1016/j.coi.2016.02.006 | 10.1007/s12223-025-01342-9 | Phage therapy and its role in cancer treatment and control. |
| 40965568 | 10.1128/aem.01353-24 | 10.1007/s00417-025-06961-z | Microbial keratitis in the age of resistance: unlocking the therapeutic potentia |
| 40965617 | 10.1021/acsnano.8b06395 | 10.1007/s10096-025-05262-x | Understanding phage Receptor-binding protein interaction with host surface recep |
| 40969760 | 10.1128/spectrum.02361-22 | 10.3389/fimmu.2025.1651594 | MS2 virus-like particles as a versatile platform for multi-disease vaccines: a r |
| 40970331 | 10.1093/cid/ciab1015 | 10.1080/21505594.2025.2562634 | Next-generation antimicrobials: A review of phage lysins as precision weapons ag |
| 40972224 | 10.3389/fmicb.2024.1293990/full | 10.1016/j.ebiom.2025.105942 | Efficacy of precisely tailored phage cocktails targeting carbapenem-resistant Ac |
| 40981438 | 10.1128/aem.45.2.701-702.1983 | 10.1128/mbio.02360-25 | Collaboration between a temperate phage and Pseudomonas aeruginosa quorum sensin |
| 40985708 | 10.1186/s42522-020-0011-0 | 10.1128/msphere.00376-25 | Comparative genomics of endemic Staphylococcus aureus ST1 in New Zealand. |
| 40986176 | 10.2217/nnm-2017-0151 | 10.1007/s10096-025-05269-4 | Application of three-dimensional bacteriophage cocktail biogel on infected burn  |
| 40989186 | 10.1016/j.resmic.2015.07.003 | 10.3389/fcimb.2025.1629120 | Genetic diversity of Microviridae phages in the human respiratory tract. |
| 40996036 | 10.1093/nar/gkac400 | 10.1128/msystems.00459-25 | Revealing the diversity of commensal corynebacteria from a single human skin sit |
| 40996673 | 10.1128/iai.46.2.394-400.1984 | 10.1007/s15010-025-02646-1 | Horizontal transfer of ΦHKU.vir and its role in the evolution of acapsular emm89 |
| 40998389 | 10.1021/acschembio.2c00565 | 10.1021/acs.accounts.5c00368 | Advances in Proximity-Assisted Bioconjugation. |
| 41000396 | 10.1093/ndt/gfy171 | 10.3389/fimmu.2025.1660226 | Gut microbiota therapy for chronic kidney disease. |
| 41003718 | 10.3390/antibiotics9040155 | 10.1007/s00203-025-04464-3 | A comprehensive review of advanced strategies to combat antimicrobial resistance |
| 41005479 | 10.1101/2025.1103.1106.641852 | 10.1016/j.jbc.2025.110761 | Mechanistic coupling of enzymatic activities at the replisome. |
| 41009364 | 10.1007/s40259-019-00392-z | 10.3390/ijms26188794 | Monoclonal Antibodies: Historical Perspective and Current Trends in Biological D |
| 41009471 | 10.1016/j.jgar.2021.10.022 | 10.3390/ijms26188899 | The Gut Microbiome and Colistin Resistance: A Hidden Driver of Antimicrobial Fai |
| 41012700 | 10.3390/ijms21217810 | 10.3390/v17091273 | Discovery of Landscape Phage Probes Against Cellular Communication Network Facto |
| 41017151 | 10.1016/j.jconrel.2024.03.041 | 10.1016/j.ymthe.2025.09.043 | Stroma-targeted gene delivery for efficient immunogene therapy against pancreati |
| 41019108 | 10.1101/cshperspect.a010074 | 10.1021/acscentsci.5c00562 | A Synthetic Phage-Peptide Conjugate as a Potent Antibacterial Agent for Pseudomo |
| 41020500 | 10.1186/1477-3155-9-58 | 10.1093/nar/gkaf984 | Metagenome-inspired libraries to engineer phage M13 for targeted killing of Gram |
| 41021605 | 10.1128/AAC.00840-20 | 10.1371/journal.ppat.1013536 | Acinetobacter phages use distinct strategies to breach the capsule barrier. |
| 41022989 | 10.1186/2052-0492-1-2 | 10.1038/s41598-025-17510-3 | A case report of bacteriophage therapy for the treatment of lung infection due t |
| 41023425 | 10.1016/j.cej.2021.129075 | 10.1007/s00604-025-07562-7 | Bacteriophages combined with hybridized nanoflower-based electrochemical biosens |
| 41024201 | 10.1038/s41598-019-41868-w | 10.1186/s12985-025-02935-z | A link to the past: classical phage ISP infects the recently described Staphyloc |
| 41025596 | 10.1002/adma.201905577 | 10.1242/dmm.052393 | Engineered bacteriophages for therapeutic and diagnostic applications. |
| 41025824 | 10.1038/s42003-024-07290-3 | 10.1128/spectrum.01178-25 | A comprehensive reference catalog of human skin DNA virome reveals novel viral d |
| 41026353 | 10.1039/c9np00050j | 10.1007/s10123-025-00727-7 | Combating multidrug-resistant uropathogenic E. coli using lytic phages, enhancin |
| 41026406 | 10.34133/bmef.0104 | 10.1007/s12602-025-10676-2 | Innovative Approaches to Combat Antimicrobial Resistance: A Review of Emerging T |
| 41028112 | 10.1038/s41598-020-69241-2 | 10.1038/s41598-025-98392-3 | Unveiling the probiotic potential of the genus Geobacillus through comparative g |
| 41029464 | 10.1007/s00705-013-1700-0 | 10.1186/s13062-025-00689-w | Phage-encoded protein PavP modulates Pseudomonas aeruginosa virulence by dual in |
| 41030102 | 10.3390/metabo12030242 | 10.1111/1750-3841.70589 | Dry-Aged Beef: A Global Review of Meat Quality Traits, Microbiome Dynamics, Safe |
| 41031824 | 10.3390/bioengineering12050469 | 10.1128/ecosalplus.esp-0004-2025 | Bacteriophage T4 genome packaging: mechanism and application. |
| 41032194 | 10.3390/microorganisms13020295 | 10.1007/s12602-025-10784-z | Phage-Microbiota Interactions in the Gut: Implications for Health and Therapeuti |
| 41036839 | 10.1016/j.foar.2019.10.004 | 10.1128/aem.00973-25 | Photoinactivation of influenza viruses by modulated indoor daylight spectrum and |
| 41036840 | 10.1093/nar/gky1085 | 10.1128/spectrum.01936-25 | Exploring phage-host interactions in Burkholderia cepacia complex bacterium to r |
| 41037223 | 10.3390/diagnostics3040344 | 10.1007/s13402-025-01105-1 | Development of a 177Lu-labeled EphA2-targeting cyclic peptide combined with an H |
| 41039237 | 10.3389/fcimb.2024.1428637 | 10.1186/s12866-025-04195-x | Characterization of bacteriophages PAA and PAM and evaluation of their antibioti |
| 41041320 | 10.1189/jlb.1103586 | 10.3389/fimmu.2025.1644391 | Generation of novel human anti-OX-40 mAbs endowed with different biological prop |
| 41044673 | 10.1016/j.mib.2017.09.004 | 10.1186/s12917-025-04989-1 | Newly isolated bacteriophages show efficacy and phage-antibiotic synergy in vitr |
| 41048514 | 10.1016/j.jmb.2016.08.003 | 10.3389/fmicb.2025.1675794 | The effect of cCMP and cUMP on growth of Pseudomonas aeruginosa. |
| 41055394 | 10.1128/AAC.00472-19 | 10.1128/mbio.02521-25 | Separation of Pseudomonas aeruginosa type IV pilus-dependent twitching motility  |
| 41056240 | 10.1016/j.jaci.2021.03.017 | 10.1371/journal.pone.0331847 | Dysglycemia and the airway microbiome in cystic fibrosis. |
| 41064643 | 10.1126/SCIADV.ABI6856 | 10.3389/fcimb.2025.1695284 | Perspectives in clinical microbiology for combating multi-drug resistant bacteri |
| 41065359 | 10.3390/antibiotics10070849 | 10.1128/jcm.00272-25 | In vitro activity of antibiotic monotherapy and combination therapy with bacteri |
| 41065368 | 10.1016/j.cmi.2023.10.014 | 10.1128/cmr.00233-24 | Current and future options for the treatment of serious infections due to carbap |
| 41065856 | 10.1038/s41598-024-76427-5 | 10.1007/s11033-025-10967-5 | Bacteriophages as a modern diagnostic tool: innovations, applications and challe |
| 41066428 | 10.1016/j.biologicals.2019.10.003 | 10.1371/journal.pone.0334139 | Bacteriophage as an anti-biofilm agent against Pseudomonas aeruginosa from wound |
| 41066664 | 10.1107/s0907444904019158 | 10.1021/acs.jmedchem.5c01378 | Design of Bicyclic Peptide Tandems Mimicking the Homodimeric GDF15 Protein to In |
| 41068567 | 10.1089/phage.2021.0017 | 10.1186/s12866-025-04328-2 | Utilizing the effectiveness of phage cocktail to combat Shigella and Salmonella  |
| 41071011 | 10.1007/s11095-014-1617-7 | 10.1128/mra.00795-25 | Complete genome sequences of four Phikmvirus bacteriophages from Kenyan sewage l |
| 41073553 | 10.1016/j.jconrel.2018.03.002 | 10.1038/s41598-025-19248-4 | Nanobody conjugated with dendrimer nanoparticles effectively neutralizes tick-bo |
| 41076507 | 10.3389/fcimb.2022.900918 | 10.1007/s12223-025-01324-x | Microbiota-based therapies in oral health and disorders. |
| 41076612 | 10.3390/v14020286 | 10.1007/s00705-025-06436-w | PSK1, a bacteriophage with antibacterial activity against extended-spectrum-beta |
| 41081916 | 10.1186/s12985-020-01485-w | 10.1007/s00203-025-04509-7 | Phage therapy for antimicrobial-resistant Klebsiella spp. infections: a review o |
| 41085275 | 10.3389/fmicb.2021.610656 | 10.1002/mbo3.70067 | Environmental Antimicrobial Resistance: Key Drivers, Hotspots, Innovative Strate |
| 41085282 | 10.1016/j.mtbio.2023.100898 | 10.1128/aem.01269-25 | Mucofilm: a nexus for phage-microbiome interactions in gut ecology. |
| 41085640 | 10.3390/antibiotics11070839 | 10.1007/s10096-025-05302-6 | Isolation and characterization of a lytic phage and its efficacy against multi-d |
| 41085803 | 10.1089/crispr.2021.0076 | 10.1007/s11274-025-04608-z | CRISPR-Cas systems in combating antimicrobial resistance: which system to choose |
| 41088149 | 10.1016/j.addr.2012.09.037 | 10.1186/s12951-025-03756-6 | Dendritic cell-targeted liposomes for cancer immunotherapy via inhibition of ary |
| 41088420 | 10.1186/s11658-025-00716-8 | 10.1186/s40001-025-03264-1 | Gut microbiota and metabolism in systemic lupus erythematosus: from dysbiosis to |
| 41089845 | 10.1128/msystems.00607-24 | 10.3389/fphar.2025.1653424 | Antibiotic-sparing strategies for multidrug-resistant organism (MDRO) infections |
| 41091245 | 10.2147/idr.S384980 | 10.1007/s11274-025-04591-5 | CRISPR-Cas opens a new era of antimicrobial therapy as a powerful gene editing t |
| 41094135 | 10.1186/s13059-022-02823-7 | 10.1038/s41586-025-09614-7 | Isolation, engineering and ecology of temperate phages from the human gut. |
| 41099532 | 10.1093/bioinformatics/btp352 | 10.1128/mbio.02011-25 | Short tandem gene duplications as potential agents of genetic memory. |
| 41099554 | 10.1111/j.1574-6976.2009.00200.x | 10.1128/aem.01163-25 | Crude preparation of a phage-encoded biofilm-dispersing factor expressed in E. c |
| 41102167 | 10.1016/j.bios.2015.05.073 | 10.1038/s41598-025-05069-y | Engineered phage-silver nanoparticle complexes as a new tool for targeted therap |
| 41105330 | 10.1038/s41598-019-51742-4 | 10.1007/s10096-025-05300-8 | Novel bacteriophages effectively target multidrug-resistant clinical isolates of |
| 41107717 | 10.1371/journal.pone.0074647 | 10.1186/s12866-025-04379-5 | Bile modulates phage-host interactions in multidrug-resistant Pseudomonas aerugi |
| 41108387 | 10.1038/s41564-018-0322-4 | 10.1007/s00203-025-04526-6 | Intranasal phage therapy overcomes antibody neutralization challenges in pulmona |
| 41114218 | 10.1128/JB.185.3.779-787.2003 | 10.1021/acsomega.5c04140 | Isolation and Characterization of Four New Coliphages against Extra Intestinal P |
| 41114507 | 10.1128/mbio.01447-22 | 10.1128/spectrum.01070-25 | Sublethal interaction factor (SIF), a growth-based method to analyze antibiotic  |
| 41115506 | 10.3760/cma.j.issn.1674-2397.2017.03.007 | 10.1016/j.virusres.2025.199645 | M13 phages engineered with chlamydia phage φCPG1 protein IN5 and arginine-glycin |
| 41117890 | 10.1016/J.CELL.2022.11.017 | 10.1007/s11033-025-11173-z | Phage therapy for Drug-Resistant infections: Mechanisms, Evidence, and emerging  |
| 41120127 | 10.1080/10618600.2022.2067548 | 10.1136/jitc-2025-011742 | Pan-microbial serological repertoire as a biomarker of immunotherapy response in |
| 41120828 | 10.1128/JVI.02457-16 | 10.1186/s12866-025-04251-6 | Phage vB_KpnM_JYSS3 encodes a novel polysaccharide depolymerase that exhibits sp |
| 41129223 | 10.1016/j.cell.2025.03.027 | 10.1073/pnas.2523344122 | All the world's a phage. |
| 41130953 | 10.1021/acs.jproteome.2c00145 | 10.1038/s41467-025-64426-7 | Targeted degradation of endogenous YAP by nanobody bioPROTAC inhibits tumor prog |
| 41131456 | 10.1007/s10238-009-0044-2 | 10.1186/s12866-025-04435-0 | Evaluating the therapeutic potential of a novel bacteriophage cocktail against c |
| 41135414 | 10.1016/j.jdent.2020.103556 | 10.1016/j.identj.2025.103963 | Control of Viral Aerosol Dispersion During Simulated Dental Procedures. |
| 41136732 | 10.3390/mps1030027 | 10.1038/s41564-025-02150-0 | Bacterial TIR-based immune systems sense phage capsids to initiate defense. |
| 41137958 | 10.1126/science.1208592 | 10.1007/s00253-025-13577-0 | Genetically encoded fluorescent probes to assist in the diagnosis of small cell  |
| 41143937 | 10.52965/001c.138205 | 10.1186/s10195-025-00892-5 | Editorial: Bacteriophage therapy in orthopedics-Key questions and emerging answe |
| 41152716 | 10.1128/mBio.01780-18 | 10.1186/s12864-025-12172-x | Prophage landscape in Enterococcus faecium: diversity, resistance genes, virulen |
| 41156596 | 10.23750/abm.v91i13-S.10834 | 10.3390/pathogens14100985 | Metagenomic Analysis of the Gastrointestinal Phageome and Incorporated Dysbiosis |
| 41156622 | 10.1093/cid/ciz782 | 10.3390/pathogens14101011 | Phage to ESKAPE: Personalizing Therapy for MDR Infections-A Comprehensive Clinic |
| 41157908 | 10.1007/s10858-009-9333-z | 10.1021/acschembio.5c00726 | Chemokine-Binding All-D-CLIPS Peptides Identified Using Mirror-Image Phage Displ |
| 41160105 | 10.3389/fphar.2023.1258062 | 10.1007/s10482-025-02196-4 | Microbiome modulation as a therapeutic strategy for alcohol-induced gut dysbiosi |
| 41161486 | 10.1038/s12276-025-01418-z | 10.1016/j.jare.2025.10.059 | Advanced immunodiagnostics for periodontal disease: Targeted detection of Kgp an |
| 41162498 | 10.1016/j.joen.2005.10.049 | 10.1038/s41598-025-21701-3 | Isolation, functional characterization and antibiofilm properties of a lytic Ent |
| 41162699 | 10.1038/s41586-024-07487-w | 10.1038/s41586-025-09661-0 | Nanobody-based recombinant antivenom for cobra, mamba and rinkhals bites. |
| 41163068 | 10.1146/annurev-virology-092818-015819 | 10.1186/s13104-025-07525-4 | Determination of bacteriophage ETEC-phage-TG to control pathogenic Escherichia c |
| 41165876 | 10.1093/jambio/lxac089 | 10.1007/s11274-025-04593-3 | Antivirulence drugs against Acinetobacter baumannii: where do they stand? |
| 41169678 | 10.3389/fmicb.2019.00574 | 10.3389/fvets.2025.1609955 | Controlling drug-resistant bacteria in Arabian horses: bacteriophage cocktails f |
| 41170983 | 10.1093/bioadv/vbad101 | 10.1128/mra.00993-25 | Complete genome sequence of Pseudomonas aeruginosa bacteriophage PaFZ4 isolated  |
| 41171134 | 10.1038/s41564-024-01715-9 | 10.1093/nar/gkaf1115 | gcMeta 2025: a global repository of metagenome-assembled genomes enabling cross- |
| 41171386 | 10.1186/s12915-020-00906-0 | 10.1007/s43032-025-02001-7 | From Gut to Reproductive Health: Exploring Microbiome Interactions and Future In |
| 41181319 | 10.1186/s12985-025-02626-9 | 10.3389/fcimb.2025.1693796 | From commensalism to pathogenesis: the hidden role of the respiratory virome. |
| 41181971 | 10.1093/bioinformatics/bty560 | 10.1128/spectrum.02277-25 | Amplification, purification, and lyophilization of mycobacteriophages for therap |
| 41188234 | 10.1093/bioinformatics/btab007 | 10.1038/s41467-025-64743-x | Genetic exchange networks bridge mobile DNA vehicles in the bacterial pathogen L |
| 41188260 | 10.1038/ni.1931 | 10.1038/s41392-025-02457-8 | A novel long-acting C5a-blocking cyclic peptide prevents sepsis-induced organ dy |
| 41190821 | 10.1038/s41467-021-27037-6 | 10.1128/spectrum.01098-25 | Isolation and characterization of a novel K3-type capsule-targeting phage for th |
| 41190822 | 10.1038/s41591-019-0437-z | 10.1128/mbio.01418-25 | mGem: Immune recognition and clearance of bacteriophages-implications for phage  |
| 41193697 | 10.1101/2025.08.05.668817 | 10.1038/s41575-025-01134-z | Gut virome dynamics: from commensal to critical player in health and disease. |
| 41195642 | 10.1016/j.bbih.2023.100603 | 10.1002/acn3.70238 | Insights Into the Antigenic Repertoire of Unclassified Synaptic Antibodies. |
| 41198758 | 10.1007/s10482-017-0844-4 | 10.1038/s41598-025-22703-x | Isolation and characterization of bacteriophages for carbapenem resistant Entero |
| 41200031 | 10.1021/acs.est.5b04713 | 10.3389/fpubh.2025.1664322 | Understanding the impact of different hand drying methods on viral aerosols form |
| 41200194 | 10.1159/000247298 | 10.3389/fimmu.2025.1667195 | Endolysin significantly improves symptoms with atopic dermatitis: bridging the g |
| 41200551 | 10.3390/ph16121638 | 10.3389/fcimb.2025.1690404 | Synthetic cells for phage therapy: a perspective. |
| 41206039 | 10.1021/acs.jmedchem.2c00123 | 10.1093/nar/gkaf1052 | Affinity-selected peptide ligands specifically bind i-motif DNA and modulate c-M |
| 41206046 | 10.1016/j.ijpharm.2024.123853 | 10.1093/nar/gkaf1165 | Virion content unpacked by long-read sequencing: stress-induced changes in trans |
| 41206754 | 10.1128/AAC.37.9.1966 | 10.1093/femsre/fuaf057 | Resistance to last-resort antibiotics in enterococci. |
| 41208101 | 10.1128/JB.00331-12 | 10.1002/mbo3.70115 | Exploration of Human Skin Phageome to Reveal Endolysins and Novel Antimicrobial  |
| 41208786 | 10.1093/jac/dkh465 | 10.1097/JS9.0000000000003917 | Therapeutic options and prognostic risk factors in diabetic foot osteomyelitis:  |
| 41212273 | 10.1016/J.ENVINT.2021.106641 | 10.1007/s10661-025-14786-w | The environmental threat of macrolide resistance: mechanisms, dissemination path |
| 41215733 | 10.2139/ssrn.4477726 | 10.1111/omi.70014 | Defense Systems and Prophage Detection in Streptococcus mutans Strains. |
| 41217208 | 10.1016/j.scitotenv.2023.168461 | 10.1128/spectrum.00731-25 | Characterization, genomics, and applications of the Cronobacter sakazakii bacter |
| 41219972 | 10.1038/s41467-022-31457-3 | 10.1186/s12929-025-01190-2 | Technological advancements in antibody-based therapeutics for treatment of disea |
| 41222156 | 10.1093/genetics/164.4.1243 | 10.1093/genetics/iyaf171 | Hogness at one hundred. |
| 41222722 | 10.1007/s00266-025-04909-6 | 10.1007/s00203-025-04540-8 | Clostridium botulinum serotype B: microbial genetics, toxin biosynthesis, curren |
| 41222983 | 10.3389/fmicb.2022.817228 | 10.1128/aac.01312-25 | Second-generation lysocins as therapeutics for treating Pseudomonas aeruginosa i |
| 41225150 | 10.3389/fbioe.2020.539319 | 10.1038/s42003-025-08925-9 | Harnessing droplet microfluidics and morphology-based deep learning for the labe |
| 41226509 | 10.1126/sciadv.adu1823 | 10.3390/ijms262110470 | Technologies for Monoclonal Antibody Discovery and Development. |
| 41229989 | 10.3390/ijms26115337 | 10.2147/IDR.S547655 | Efficacy of Phage Cocktails Against Biofilms Formed by Antibiotic-Resistant Bact |
| 41230949 | 10.1016/j.envint.2024.108801 | 10.1099/mic.0.001613 | Interpretation guidance for MHRA regulatory considerations for phage therapeutic |
| 41233465 | 10.1128/mbio.02867-23 | 10.1038/s41598-025-23563-1 | Hypervirulent Klebsiella pneumoniae causing aortitis retains its capsule and muc |
| 41233473 | 10.7717/peerj.10645 | 10.1038/s41598-025-23545-3 | Isolation and characterization of biofilm-disrupting proteus phage Premi. |
| 41234515 | 10.1111/j.1749-4486.2009.01973.x | 10.3389/fcimb.2025.1631359 | Regulation of phage therapy medicinal products: developments, challenges, and op |
| 41244966 | 10.1038/s41591-021-01403-9 | 10.1128/asmcr.00058-24 | Resolution of acute rejection in a bilateral double-lung transplanted cystic fib |
| 41247565 | 10.1038/S41429-024-00778-4 | 10.1007/s10482-025-02208-3 | Advances in combating antimicrobial resistance in MRSA: a comprehensive review o |
| 41249907 | 10.1093/nar/gkw290 | 10.1186/s12864-025-12246-w | Unexplored diversity and molecular genetic signatures of chimallin and phuz enco |
| 41250062 | 10.1007/s10096-022-04425-4 | 10.1186/s12941-025-00834-3 | Genomic insights into novel ST7947 carbapenem-resistant hypervirulent Klebsiella |
| 41251272 | 10.3390/microorganisms10020238 | 10.1002/vms3.70694 | Isolation, Identification and Typing of Nine Strains of Brucella in Arun Banner. |
| 41251374 | 10.1016/j.tim.2020.05.017 | 10.1128/aac.00699-25 | Optimizing phage-antibiotic combinations: impact of administration order against |
| 41252216 | 10.1186/1471-2105-12-77 | 10.1172/jci.insight.196619 | PhIP-Seq uncovers marked heterogeneity in acute rheumatic fever autoantibodies. |
| 41253829 | 10.1038/s41467-019-10201-4 | 10.1038/s41522-025-00841-4 | Two unrelated Pseudomonas aeruginosa phages require the exopolysaccharide Psl fo |
| 41254584 | 10.1016/j.str.2017.07.016 | 10.1186/s12915-025-02445-y | Insights into the molecular determinants of host specificity in Pseudomonas aeru |
| 41255842 | 10.1093/jac/dks261 | 10.1007/s13205-025-04528-7 | Complete genome sequence of lytic Pseudomonas aeruginosa phage vB_PaeS_Tums_P6. |
| 41256655 | 10.1073/pnas.1919888117 | 10.1101/2025.10.05.680490 | Bacteriophage density influences the rate of resistance evolution. |
| 41257541 | 10.1016/j.jprot.2015.11.001 | 10.1186/s12864-025-12308-z | Genomic islands and plasmid borne antimicrobial resistance genes drive the evolu |
| 41257876 | 10.1007/s43440-020-00131-0 | 10.1038/s41598-025-24324-w | Identification of internalizing ScFvs for EGFR inhibition and apoptosis inductio |
| 41258013 | 10.1007/s10482-017-0844-4 | 10.1038/s41467-025-66062-7 | Experimental phage evolution results in expanded host ranges against antibiotic  |
| 41258817 | 10.1186/1471-2180-13-171 | 10.1128/spectrum.01818-25 | Novel lytic phages improve the antibiofilm activity of dalbavancin, daptomycin,  |
| 41261852 | 10.1016/j.scitotenv.2023.168840 | 10.1093/nar/gkaf1122 | KlebPhaCol: a community-driven resource for Klebsiella research identified a nov |
| 41266316 | 10.1016/0003-2697(82)90673-X | 10.1038/s41467-025-65014-5 | Directed evolution of phages in biofilms enhances Pseudomonas aeruginosa control |
| 41267074 | 10.1158/2159-8290.CD-23-0984 | 10.1186/s12967-025-07316-2 | De novo design of a two-step approach targeting Claudin-6 for enhanced drug deli |
| 41267780 | 10.1186/s12967-025-06321-9 | 10.3389/fcimb.2025.1692582 | The gut microbiome as a major source of drug-resistant infections: emerging stra |
| 41267794 | 10.1038/s41467-023-43732-y | 10.1155/bmri/5571277 | Novel Strategies to Profile SARS-CoV-2 and Human Lung Proteome: Inflammatory Pat |
| 41267900 | 10.1111/j.2517-6161.1995.tb02031.x | 10.1093/nargab/lqaf148 | Genomic islands in Pseudomonas encode modular hotspots of defence and anti-defen |
| 41268522 | 10.1038/s41467-023-42413-0 | 10.1039/d5sc04923g | A phage-selective trigger hints at an SOS-independent mechanism of prophage indu |
| 41269221 | 10.1016/s0378-1119(98)00130-9 | 10.1099/mic.0.001634 | Eliminating the type I restriction endonuclease from Pseudomonas aeruginosa PAO1 |
| 41269653 | 10.1016/j.micres.2022.127222 | 10.1007/s13258-025-01702-2 | Comprehensive in silico analysis of Acinetobacter isolates from South Korea reve |
| 41275070 | 10.1089/omi.2011.0118 | 10.1038/s41467-025-66733-5 | Human gut prophage landscape identifies a prophage-mediated fucosylation mechani |
| 41275230 | 10.34133/research.0523 | 10.1186/s12951-025-03868-z | A high-affinity CEA-targeted nanobody for 68Ga PET imaging and 177Lu-based radio |
| 41277891 | 10.1093/nar/gkad326 | 10.1128/mra.00893-25 | Complete genome sequence of vB_PaBD_211, a lytic Pseudomonas aeruginosa phage is |
| 41278478 | 10.1128/aem.00468-21 | 10.3389/fcimb.2025.1691215 | Combating Klebsiella pneumoniae: from antimicrobial resistance mechanisms to pha |
| 41283692 | 10.1186/s40168-016-0154-5 | 10.1128/aem.01899-25 | Prophages and their interactions with lytic phages in the human gut microbiota a |
| 41292073 | 10.1038/s41598-019-47910-1 | 10.1080/19420862.2025.2591461 | Discovery and characterization of two anti-PD-1 antibodies with a unique binding |
| 41292853 | 10.1016/j.jmb.2017.12.007 | 10.1101/2025.11.11.687635 | The Lysis Cassette of Jumbophage phiKZ. |
| 41296881 | 10.1038/s41598-017-09317-8 | 10.1128/aem.01917-25 | Human gut strains of Desulfovibrio piger exhibit spontaneous induction of multip |
| 41296916 | 10.3390/ijms25168690 | 10.1002/rmv.70080 | Gut Virome: What's the Role in Irritable Bowel Syndrome? |
| 41299176 | 10.21105/joss.01686 | 10.1038/s41586-025-09786-2 | Long-read metagenomics reveals phage dynamics in the human gut microbiome. |
| 41299243 | 10.1038/s41586-024-07991-z | 10.1186/s12859-025-06294-y | GrafGen: distance-based inference of population ancestry for Helicobacter pylori |
| 41301547 | 10.1016/j.nbt.2009.03.012 | 10.3390/biom15111628 | Protein Engineering and Drug Discovery: Importance, Methodologies, Challenges, a |
| 41301664 | 10.34172/bi.2021.10 | 10.3390/antibiotics14111167 | Mechanisms and Evolution of Antimicrobial Resistance in Ophthalmology: Surveilla |
| 41304933 | 10.1128/spectrum.00280-25 | 10.3390/ph18111688 | Phage Encapsulation and Delivery Technology: A Strategy for Treating Drug-Resist |
| 41305340 | 10.1146/annurev-med-080219-122208 | 10.3390/pathogens14111102 | Novel Therapies for Prosthetic Joint Infections Caused by Methicillin-Resistant  |
| 41305429 | 10.1016/S0378-1097(97)00415-1 | 10.3390/v17111406 | Potential Vaccine or Antimicrobial Reagents: Simple Systems for Producing Lambda |
| 41305464 | 10.1371/journal.pone.0031698 | 10.3390/v17111441 | Rational Design of a Potent Two-Phage Cocktail Against a Contemporary Acinetobac |
| 41306047 | 10.1016/j.biomaterials.2013.05.063 | 10.1021/acsabm.5c01489 | Potential of Nitric Oxide and Bacteriophages as Combined Antibacterial Agents to |
| 41307449 | 10.1016/j.ijantimicag.2025.107612 | 10.1021/acs.langmuir.5c03695 | Silver Nanoparticles Templated by the M13 Phage Exhibit High Antibacterial Activ |
| 41309396 | 10.1002/btm2.10600 | 10.4014/jmb.2509.09050 | PEGylation Overcomes Pharmacological Barriers to Improve Systemic Pharmacokineti |
| 41313537 | 10.1016/j.tim.2021.01.003 | 10.1007/s12602-025-10855-1 | Gut Microbiome in Obesity: A Narrative Review of Mechanisms, Interventions, and  |
| 41315055 | 10.1038/s41598-020-57615-5 | 10.1007/s00248-025-02620-2 | Bioactive Plasmid- and Phage-Encoded Antimicrobial Peptides (AMPs) in the Human  |
| 41315190 | 10.1093/molbev/msu300 | 10.1038/s41467-025-65208-x | Unveiling the global urban virome through wastewater metagenomics. |
| 41316526 | 10.1093/jimb/kuab088 | 10.1002/mnfr.70329 | Listeria monocytogenes-Can We Reduce or Eliminate It From Food Commodities? |
| 41330323 | 10.1016/j.cub.2019.04.024 | 10.1016/j.cub.2025.10.055 | Phage-bacteria dynamics: The tragedy of the commons at hyperspeed. |
| 41331246 | 10.1080/10618600.2015.1131161 | 10.1038/s41467-025-65939-x | Prolonged disease remission of the chronic immunological skin disorder hidradeni |
| 41335395 | 10.3389/fmicb.2016.01519 | 10.1007/s10096-025-05375-3 | Phages and quorum sensing: findings to consider in phage therapy. |
| 41338184 | 10.1038/s41596-025-01174-4 | 10.1016/j.ymthe.2025.11.021 | Development of a high-affinity anti-ROR1 variable region for broad anti-cancer i |
| 41341577 | 10.1016/s1995-7645(12)60055-8 | 10.3389/fimmu.2025.1707358 | Development of nanobody-based DAS-ELISA and Au nanoparticle-based immunochromato |
| 41342459 | 10.1038/s42003-023-04746-w | 10.1080/19420862.2025.2597610 | AbDrop-a scalable microfluidics-enabled platform for rapid discovery and functio |
| 41345089 | 10.3389/fmicb.2016.00882 | 10.1038/s41467-025-64608-3 | Considerations and perspectives on phage therapy from the transatlantic taskforc |
| 41345505 | 10.1128/AEM.07097-11 | 10.1038/s41598-025-30556-7 | Synergy between ciprofloxacin and temperate phages overcomes therapeutic limitat |
| 41346111 | 10.1158/1535-7163.MCT-21-0846 | 10.1016/j.ymthe.2025.12.002 | On-target/off-tumor toxicities following infusion of low-affinity Nectin-4-speci |
| 41346627 | 10.1128/iai.00283-22 | 10.3389/fimmu.2025.1681461 | Neutrophils, not macrophages, aid phage-mediated control of pulmonary Pseudomona |
| 41347517 | 10.1111/jam.15647 | 10.1128/aac.00925-25 | Impact of Pseudomonas aeruginosa biofilm exopolysaccharide composition on bacter |
| 41347520 | 10.1128/AAC.01609-19 | 10.1128/aac.01506-25 | Whole-body distribution of three Pseudomonas phages characterized by a translati |
| 41348832 | 10.1038/s41385-019-0250-5 | 10.1371/journal.pone.0337760 | Human-derived fecal virome transplantation (FVT) reshapes the murine gut microbi |
| 41350265 | 10.1038/s41592-019-0456-1 | 10.1038/s41597-025-06171-6 | Bronchoalveolar lavage fluid metagenomic datasets: a multidimensional clinical b |
| 41355985 | 10.1128/msphere.00345-22 | 10.3389/fcimb.2025.1702890 | Harnessing phages to tackle antimicrobial resistance: a Saudi Arabian perspectiv |
| 41358742 | 10.1089/phage.2023.0045 | 10.1128/jb.00375-25 | Steering the course: targeting and exploiting surface receptors in phage therapy |
| 41358758 | 10.1002/pro.3902 | 10.1128/mbio.02758-25 | Manganese activates the CBASS immunity to protect bacteria from phage infection. |
| 41358816 | 10.1093/ve/veac070 | 10.1093/femsre/fuaf061 | Phage cocktails: state-of-the-art technologies and strategies for effective desi |
| 41362956 | 10.1186/s40168-017-0298-y | 10.1080/19490976.2025.2597614 | Extensive cultivation of human gut phages revealing undescribed Bacteroidaceae p |
| 41363802 | 10.4161/bact.25098 | 10.1128/mbio.02654-25 | Clinical and environmental wastewater-based bacteriophage surveillance for high- |
| 41365303 | 10.1093/GIGASCIENCE/GIAF004 | 10.1016/j.crmeth.2025.101250 | A signature-protein-based approach for accurate and efficient profiling of the h |
| 41365923 | 10.1371/journal.pone.0161879 | 10.1038/s41467-025-67361-9 | De novo design of epitope-specific antibodies via a structure-driven computation |
| 41369844 | 10.1016/j.medj.2024.05.017 | 10.1007/s11033-025-11322-4 | Biological characterization and genome analysis of Pseudomonas phage ZAM-Pa99 as |
| 41370631 | 10.1145/1961189.1961199 | 10.1093/bib/bbaf656 | PBIP: a deep learning framework for predicting phage-bacterium interactions at t |
| 41379369 | 10.1074/jbc.RA119.009894 | 10.1007/s12223-025-01379-w | Detection and identification of pathogens using agents targeting the bacterial c |
| 41381457 | 10.1038/s41587-020-0603-3 | 10.1038/s41467-025-61946-0 | Gut Phage Biobank: a collection of bacteriophages targeting human commensal bact |
| 41381787 | 10.1007/S00604-020-04423-3/FIGURES/5 | 10.1007/s00604-025-07750-5 | Bacteriophage binding receptor like-peptides and MXene-AgNPs modified label-free |
| 41382009 | 10.3389/fmicb.2022.821989 | 10.1186/s12866-025-04513-3 | Characterization and genome analysis of jumbo Escherichia phage UE-S1 and the an |
| 41382030 | 10.1038/s41598-024-51316-z | 10.1186/s12866-025-04588-y | Phage-mediated control of melioidosis in Southern China: molecular insights and  |
| 41383045 | 10.1080/08830185.2017.1298749 | 10.1080/2162402X.2025.2583553 | Virus nanoparticle intratumoral vaccines for HER2+ malignancies. |
| 41383603 | 10.1002/jcc.21334 | 10.3389/fimmu.2025.1696587 | A novel TNFR2 agonist peptide for the expansion of CD4+Foxp3+ regulatory T cells |
| 41384994 | 10.1038/sj.bmt.1705912 | 10.1007/s00432-025-06393-6 | Phage therapy and the microbiome in hematologic malignancies: opportunities, mec |
| 41387457 | 10.1182/bloodadvances.2018019026 | 10.1038/s41522-025-00882-9 | CRISPR-engineered microbiome: living therapeutics revolutionize blood cancer imm |
| 41387875 | 10.1093/nar/gky427 | 10.1186/s12917-025-05182-0 | Reverse vaccinology-based identification of immunogenic membrane proteins from z |
| 41390877 | 10.1038/s41598-017-18096-1 | 10.1038/s41598-025-32351-w | Characterization of broad host range bacteriophages vKpIN31 and vKpIN32 against  |
| 41392062 | 10.1126/sciimmunol.adi3487 | 10.1007/s11307-025-02070-9 | Identification of a Novel TIM-3 Targeting Peptides Probe to Indicate the Immunom |
| 41394736 | 10.1093/nar/gkm216 | 10.1101/2025.11.26.690771 | Structural atlas of Pakpunavirus P7-1 reveals determinants of virion stability a |
| 41395946 | 10.1101/2022.05.22.492996 | 10.1128/msystems.01290-25 | Hidradenitis suppurativa patients exhibit a distinctive and highly individualize |
| 41399705 | 10.3390/microorganisms8111716 | 10.1016/j.bioflm.2025.100333 | Temperate bacteriophage induced in Pseudomonas aeruginosa biofilms can modulate  |
| 41401934 | 10.3390/vaccines11050919 | 10.1080/21645515.2025.2599632 | Bacteriophages as vaccine platforms: Opportunities and challenges in translation |
| 41402443 | 10.1093/nar/gkab496 | 10.1038/s44259-025-00167-3 | Gene-specific reversal of carbapenem-resistant Pseudomonas aeruginosa via phage- |
| 41405200 | 10.1038/s41467-024-47192-w | 10.1128/msystems.01384-25 | Model-informed development of bacteriophage therapy: bridging in vitro and in vi |
| 41406010 | 10.1371/journal.pgen.1004056 | 10.1099/mgen.0.001591 | Predicting clinical outcome of Escherichia coli O157:H7 infections using explain |
| 41411372 | 10.1126/science.adj3166 | 10.1371/journal.pntd.0013674 | A colorimetric method for detecting virulent bacteriophage to Vibrio cholerae in |
| 41416169 | 10.1007/s00484-021-02204-y | 10.12182/20250960203 | [Advances in Novel Disinfection Technologies for Biofilm-Associated Nosocomial I |
| 41420149 | 10.1074/jbc.M110.127571 | 10.1186/s12866-025-04525-z | Genomic and functional characterization of a novel lytic phage vB-AbaM-fThrA wit |
| 41421023 | 10.1101/2025.07.08.663546 | 10.1016/j.mib.2025.102698 | Nucleus-forming phages: from subcellular organization and viral-host interplay t |
| 41422109 | 10.1186/gb-2009-10-10-r110 | 10.1038/s41467-025-67441-w | Neisseria meningitidis filamentous phage MDA promotes colonisation by selecting  |
| 41423823 | 10.1016/j.cell.2015.12.035 | 10.1002/mbo3.70206 | Uncovering Insights Into the Biology of Mycobacterium tuberculosis Using Genetic |
| 41425571 | 10.1016/j.imlet.2019.06.009 | 10.3389/fimmu.2025.1712231 | Screening and identification of human HPV18VLP neutralizing antibodies from wome |
| 41428763 | 10.1371/journal.ppat.1013013 | 10.1371/journal.ppat.1013807 | Colanic acid-mediated phage resistance enhances virulence in high-risk global cl |
| 41429182 | 10.1038/s41564-023-01575-9 | 10.1111/1758-2229.70267 | Antibiotic Resistance Crisis: From Bacterial Bioprospecting to Artificial Intell |
| 41430121 | 10.1007/s11605-021-05188-7 | 10.1186/s12866-025-04433-2 | High alcohol-producing Escherichia coli causes obesity and steatotic liver disea |
| 41430395 | 10.1016/j.micres.2022.127040 | 10.1007/s00210-025-04917-y | Small-colony variants of Staphylococcus aureus: hidden threat in chronic and rec |
| 41432409 | 10.1073/pnas.120163297 | 10.1128/aac.01341-25 | A recombinant lysogenic bacteriophage inhibits Salmonella virulence. |
| 41433304 | 10.1093/nar/gkae1011 | 10.1128/iai.00422-25 | Human body temperature cues widespread changes in virulence gene expression in u |
| 41436840 | 10.1242/jcs.02566 | 10.1038/s41598-025-33556-9 | A novel fibronectin-binding peptide reveals dynamic intermediate structures duri |
| 41443416 | 10.1074/jbc.AC120.014918 | 10.1016/j.jbc.2025.111083 | A high diversity naïve variable new antigen receptor, vNAR, phage library for ra |
| 41446284 | 10.1186/s12941-024-00671-w | 10.3389/fcimb.2025.1653521 | Complete genome assembly and functional characterization of Brucella melitensis  |
| 41450572 | 10.3390/antibiotics12121734 | 10.3389/fcimb.2025.1690417 | Global trends in carbapenem-resistant gram-negative bacteria research (2020-2025 |
| 41452380 | 10.1016/S1389-1723(01)80276-0 | 10.1007/s00726-025-03492-z | NGS and the design of an optimized phage display workflow for peptide discovery. |
| 41459975 | 10.1073/pnas.1315156111 | 10.1128/spectrum.02218-25 | A novel anti-Toxoplasma peptide suppresses parasite invasion and rescues host au |
| 41465309 | 10.1007/978-1-4939-7447-4_14 | 10.3390/ijms262411881 | Ilama VHH as a Substitute for Rabbit Polyclonal Antibodies in ELISpot Applicatio |
| 41465590 | 10.1101/2023.10.02.560326 | 10.3390/ijms262412166 | Characterisation of the Novel Cutibacterium acnes Phage KIT09 and First Report o |
| 41466100 | 10.3390/antibiotics13100926 | 10.4014/jmb.2509.09030 | Clinical and Translational Perspectives on Bacteriophage Therapy for Nontubercul |
| 41471197 | 10.1016/j.watres.2022.119070 | 10.3390/pathogens14121242 | Innovations in Biofilm Prevention and Eradication in Medical Sector: An Integrat |
| 41471203 | 10.3390/ph14030184 | 10.3390/pathogens14121248 | Characterisation of a Novel Pseudomonas Phage and Its Effect on the Survival of  |
| 41471986 | 10.1016/j.cell.2017.10.045 | 10.3390/microorganisms13122783 | More Is Not Always Better: Co-Occurrence Analysis of Anti-Phage Systems Reveals  |
| 41472273 | 10.1128/jvi.01025-25 | 10.3390/v17121603 | First Brazilian Symposium on Viruses of Microorganisms (BrVoM 2025). |
| 41472293 | 10.1128/mBio.01501-19 | 10.3390/v17121623 | Study of the Activity of the Staphylococcus aureus Phage vB_SaS_GE1 Against MRSA |
| 41474711 | 10.1093/molbev/msac220 | 10.1371/journal.pone.0340071 | Whole-genome sequencing of Burkholderia glumae strains from Thailand reveals pot |
| 41476966 | 10.1038/s41467-021-20930-0 | 10.3389/fimmu.2025.1684904 | Isolation of a nanobody specific to the PstS-1 protein and evaluation of its imm |
| 41481419 | 10.1038/s41596-019-0162-6 | 10.1016/j.celrep.2025.116759 | A prophage-expressed type IV pilus component provides anti-phage defense. |
| 41481455 | 10.1016/j.chembiol.2012.07.023 | 10.1073/pnas.2524899122 | E2 variants for probing E3 ubiquitin ligase activities. |
| 41484238 | 10.1093/nar/gkw361 | 10.1038/s41598-025-33040-4 | A droplet microfluidics-based platform for generating target-specific, natively- |
| 41484353 | 10.1093/nar/gkae1011 | 10.1038/s42003-025-09458-x | Nanobodies as tools for studying human frataxin biology. |
| 41493557 | 10.1093/cid/cix349 | 10.1007/s00203-025-04649-w | Virophages: mechanisms, ecological Roles, and therapeutic potential in combating |
| 41495838 | 10.1016/s2666-5247(24)00002-8 | 10.1186/s13062-025-00726-8 | A novel synergistic action of phage vB_PaeP_GZMU_A1002 with allicin against carb |
| 41496549 | 10.1101/676825 | 10.1080/19420862.2025.2611472 | Multidimensional maturation of antibody variable domains with machine-learning a |
| 41498541 | 10.1016/j.cmi.2020.04.039 | 10.1128/spectrum.02050-25 | Biological characterization of multidrug-resistant Pseudomonas aeruginosa phage  |
| 41501250 | 10.1007/s12033-018-0123-2 | 10.1038/s41598-025-33939-y | Multi-kingdom gut microbiota characterization in Chinese patients with idiopathi |
| 41501621 | 10.3390/ph17121639 | 10.1186/s12866-025-04653-6 | Effects of phage-based treatments against an OXA-48-producing Klebsiella pneumon |
| 41503791 | 10.1016/j.chom.2019.01.017 | 10.1080/19490976.2025.2611645 | Gut virome dysbiosis contributes to premature ovarian insufficiency by modulatin |
| 41505076 | 10.1042/EBC20240019 | 10.1007/s12602-025-10853-3 | Designing the Next Generation of Endolysins: A Triple Strategy Integrating Bioin |
| 41508051 | 10.1016/j.cmi.2021.05.047 | 10.1186/s40249-025-01399-1 | Antibody landscapes of arboviral exposure across China revealed by high-throughp |
| 41510198 | 10.3390/ph14101019 | 10.1093/jacamr/dlaf257 | Pharmacodynamic individualization of phage therapy against a KPC-5-producing Pse |
| 41513696 | 10.1128/jcm.22.6.996-1006.1985 | 10.1038/s41467-025-68136-y | Timely bespoke phage-antibiotic combination to treat refractory Pseudomonas aeru |
| 41513960 | 10.3390/microorganisms9102172 | 10.1038/s41598-026-35081-9 | Identify and characterize a carbapenem-resistant Salmonella enteritidis phage de |
| 41513995 | 10.1038/351456a0 | 10.1038/s41564-025-02217-y | Large-scale testing of antimicrobial lethality at single-cell resolution predict |
| 41516055 | 10.1186/1471-2105-7-85 | 10.3390/ijms27010172 | Analysis of Pro- and Anti-Inflammatory Gene Response Patterns in Patients Receiv |
| 41517839 | 10.1021/acs.nanolett.5b03716 | 10.1002/advs.202512844 | Bacteriophage-Mimetic DNA Origami Needle for Targeted Membrane Penetration and C |
| 41518514 | 10.1016/j.virusres.2020.198196 | 10.1007/s13770-025-00786-x | Bacteriophage Cocktail in Hydrogel Dressing Modulates Macrophage Responses and I |
| 41520056 | 10.1007/s00228-023-03542-z | 10.1007/s00253-025-13695-9 | Addition of lactoferrin increases efficacy of three Kayviruses and limits the in |
| 41522440 | 10.1002/jcla.24655 | 10.3934/microbiol.2025045 | Mechanisms of antimicrobial resistance: From genetic evolution to clinical manif |
| 41526167 | 10.1016/j.cell.2024.06.012 | 10.1136/jitc-2025-013317 | Fully human anti-B7-H4 antibody induces lysosome-dependent ferroptosis to revers |
| 41530788 | 10.1093/ofid/ofaa389 | 10.1186/s13054-026-05839-8 | Hospital-adapted inhaled phage therapy for ventilator-associated pneumonia cause |
| 41533592 | 10.7554/eLife.93180.3 | 10.1093/nar/gkaf1461 | Optogenetic BlueGENEs engineered into a human safe harbor locus. |
| 41542775 | 10.1038/s41467-021-25282-3 | 10.1172/JCI192885 | Bispecific antibodies and CAR T cells targeting a TP53 mutation-associated neoan |
| 41550919 | 10.1038/s41571-023-00754-1 | 10.3389/fimmu.2025.1638585 | VHH-based CAR-T cells targeting Claudin 18.2 show high efficacy in pancreatic ca |
| 41558812 | 10.1182/bloodadvances.2024013212 | 10.1136/jitc-2025-013246 | Non-superagonist CD28-based dual-signal T cell engager targeting. |
| 41559333 | 10.1126/science.277.5331.1453 | 10.1038/s41598-026-36188-9 | The Lysis cassette of jumbophage PhiKZ. |
| 41561086 | 10.1002/iub.2908 | 10.3389/fcimb.2025.1740322 | Gut microbiota modulation in gastrointestinal disorders: current evidence and th |
| 41562899 | 10.1186/s12879-022-07379-2 | 10.3390/medsci14010009 | Bacteriophages in Hip and Knee Periprosthetic Joint Infections: A Promising Tool |
| 41566387 | 10.3389/fgene.2019.00972 | 10.1186/s12951-026-04038-5 | Engineering bacteriophages for gut health: precision antimicrobials and beyond. |
| 41568963 | 10.1002/pro.4792 | 10.1128/mbio.03561-25 | Pseudomonas aeruginosa DEV phage exploits the essential LptD outer membrane prot |
| 41571673 | 10.1038/s41598-023-39401-1 | 10.1038/s41522-025-00883-8 | Gut microbiome-driven colorectal cancer via immune, metabolic, neural, and endoc |
| 41571681 | 10.1093/bioinformatics/btp163 | 10.1038/s41467-026-68710-y | A comprehensive catalogue of receptor-binding domains in extracellular contracti |
| 41572308 | 10.1093/gigascience/giac110 | 10.1186/s12985-026-03069-6 | Bacteriophages in gut metagenomes: from analysis to application. |
| 41574279 | 10.1093/jas/skab157 | 10.1155/tbed/4488875 | Evolutionary Origins and Virulence Determinants of ST25 Hypervirulent Klebsiella |
| 41574901 | 10.1099/mgen.0.000323 | 10.1099/mgen.0.001625 | Global population structure of Shiga toxin-producing Escherichia coli O103:H2 an |
| 41575630 | 10.1038/s41467-020-18614-2 | 10.1007/s15010-025-02718-2 | A review on antibiotic and non-antibiotic decolonization strategies of multidrug |
| 41576076 | 10.5061/dryad.pzgmsbd23 | 10.1073/pnas.2525963123 | A fully synthetic Golden Gate assembly system for engineering a Pseudomonas aeru |
| 41586306 | 10.1038/s41551-019-0423-2 | 10.3389/fcimb.2025.1721411 | Bacteriophage FNU1 negates Fusobacterium nucleatum induced cell growth, migratio |
| 41586516 | 10.1016/S0022-2836(05)80360-2 | 10.1128/mra.01277-25 | Genome sequence of Pseudomonas aeruginosa bacteriophage. |
| 41586524 | 10.1101/2025.05.12.653612 | 10.1128/msystems.01282-25 | Recovery and microbial host assignment of mobile genetic elements in complex mic |
| 41586922 | 10.1099/mgen.0.000800 | 10.1007/s00705-025-06489-x | Novel Autographivirales phages Kiwi, Nika and Pie targeting Klebsiella pneumonia |
| 41587897 | 10.1017/S002217240001158X | 10.1021/acsinfecdis.5c01032 | Recombinant Human IgG1 Enhances Complement-Mediated Bacteriolysis and Macrophage |
| 41588195 | 10.1016/j.jsb.2021.107702 | 10.1038/s41589-025-02136-3 | De novo design of potent CRISPR-Cas13 inhibitors. |
| 41589898 | 10.1038/s41591-025-03678-8 | 10.1128/aem.02095-25 | Phage cocktails containing a dual-receptor Phikzvirus suppress resistance evolut |
| 41592858 | 10.1021/acsinfecdis.6b00154 | 10.4014/jmb.2509.09038 | Substrate Specificity and Immunological Implications of Cutibacterium acnes Phag |
| 41593042 | 10.3389/fimmu.2021.741513 | 10.1080/19490976.2026.2616066 | The enteric DNA virome differs in infants at risk for atopic disease. |
| 41593069 | 10.1093/bioinformatics/btp616 | 10.1038/s41467-026-68726-4 | Large-scale capsid-mediated mobilisation of bacterial genomic DNA in the gut mic |
| 41594112 | 10.1093/nar/gki408 | 10.3390/antibiotics15010075 | Pseudomonas aeruginosa Phage Cocktails: Rational Design and Efficacy Against Mou |
| 41594637 | 10.1038/nature14234 | 10.3390/biom16010097 | Identification of Key Sequence Motifs Essential for the Recognition of m6A Modif |
| 41597449 | 10.1128/spectrum.00626-24 | 10.3390/medicina62010163 | Mechanisms of Pseudomonas aeruginosa Resilience Against Antibiotic Treatment and |
| 41599062 | 10.3357/AMHP.6351.2025 | 10.3390/pathogens15010078 | UV-C Irradiation Effectiveness on Mpox-Virus-Contaminated Surfaces. |
| 41599331 | 10.1038/nmeth.4067 | 10.3390/molecules31020282 | Screening for Peptides to Bind and Functionally Inhibit SARS-CoV-2 Fusion Peptid |
| 41599372 | 10.3390/gels10040284 | 10.3390/molecules31020324 | Bacteriophage Therapy: Overcoming Antimicrobial Resistance Through Advanced Deli |
| 41600803 | 10.1016/j.tibtech.2006.03.003 | 10.3390/v18010038 | The Forgotten History of Bacteriophages in Bulgaria: An Overview and Molecular P |
| 41600807 | 10.1186/1745-6150-1-29 | 10.3390/v18010042 | Genomic, Evolutionary and Phenotypic Insights into Pseudomonas Phage Adele, a No |
| 41600861 | 10.1016/j.coviro.2021.12.004 | 10.3390/v18010097 | Broth Optical Density-Based Assessment for Phage Therapy: Turbidity Reduction, A |
| 41600893 | 10.1016/j.cell.2020.06.025 | 10.3390/v18010132 | Immune Imprinting Identified in Phage-Display Antibody Libraries Derived from Ea |
| 41601692 | 10.1093/oncolo/oyaf057 | 10.3389/fimmu.2025.1699400 | An antibody uniquely binding short 2'-O-methyl RNA oligonucleotide duplexes: for |
| 41608682 | 10.3390/ani11041112 | 10.3389/fmicb.2025.1719066 | Fluoroquinolone resistance in ESKAPE pathogens: evolutionary pathways, one healt |
| 41608690 | 10.3390/md17090499 | 10.3389/fmicb.2025.1752980 | Engineered Pseudomonas aeruginosa phages with quorum-quenching enzyme or depolym |
| 41610126 | 10.1021/acs.jpcb.8b12419 | 10.1371/journal.pone.0341602 | Discovery and computational characterization of ZIKV envelope-targeted peptides  |
| 41612191 | 10.1128/msphere.00904-24 | 10.1186/s12864-026-12585-2 | Genome-wide co-occurrence patterns link mobile genetic elements, antimicrobial r |
| 41615624 | 10.1007/S00705-022-05694-2/FIGURES/1 | 10.1007/s10096-025-05395-z | Isolation and characterisation of a novel Stenotrophomonas maltophilia phage vB_ |
| 41617027 | 10.1101/2021.10.04.463034 | 10.1016/j.jbc.2026.111210 | Engineered IgA-Fc fusion protein with bioactive nanobody neutralizes SARS-CoV-2  |
| 41617693 | 10.2307/sysbio/15.2.141 | 10.1038/s41467-026-68684-x | High-throughput methods leveraging robotics and computer vision for the developm |
| 41617703 | 10.1128/JCM.01512-08 | 10.1038/s41522-025-00887-4 | Mucosa-associated bacteria and metabolites in inflammatory bowel disease: from i |
| 41618007 | 10.1080/03639045.2018.1449855 | 10.1007/s11274-026-04783-7 | Bacterial ghosts (BGs): A promising approach as candidate vaccine. |
| 41619738 | 10.1128/iai.00085-0001 | 10.1016/j.chom.2026.01.003 | Chemical inhibition of a bacterial immune system. |
| 41625259 | 10.1016/j.coviro.2021.11.005 | 10.1016/j.onehlt.2025.101316 | In vitro efficacy of antibiotics and bacteriophages against Pseudomonas aerugino |
| 41627460 | 10.3389/fmicb.2023.1213625 | 10.1007/s00203-026-04730-y | Understanding the bacteriome, phageome and phage-associated bacteriome in health |
| 41627487 | 10.1016/j.bsheal.2023.01.001 | 10.1007/s00203-026-04721-z | Therapeutic milestones against multidrug resistant Acinetobacter baumannii: from |
| 41629776 | 10.1186/s12985-025-02885-6 | 10.1186/s12866-025-04698-7 | Prophylactic and therapeutic efficacy of Acinetobacter phage RM_A1 against carba |
| 41632588 | 10.4161/21597073.2014.960346 | 10.1080/22221751.2026.2627075 | mRNA mediated expression of novel fusion phage tail protein with antimicrobial p |
| 41634296 | 10.1136/thoraxjnl-2016-209265 | 10.1038/s41598-026-38106-5 | Bovine serum albumin nanoparticles improve bacteriophage stability and antimicro |
| 41634948 | 10.1002/jlcr.3792 | 10.1002/psc.70071 | Bismuth Bicycles. |
| 41636510 | 10.1128/iai.63.3.1055-1061.1995 | 10.1128/msystems.01002-25 | Tools and approaches to study the human gut virome: from the bench to bioinforma |
| 41641960 | 10.1038/s41579-025-01200-y | 10.1128/jvi.02071-25 | The bacteriophage-encoded regulator PemR attenuates Pseudomonas aeruginosa virul |
| 41642666 | 10.1016/j.jim.2012.02.017 | 10.1172/JCI199277 | A Trypanosoma cruzi trans-sialidase peptide demonstrates high serological preval |
| 41644603 | 10.1021/acsbiomaterials.1c00013 | 10.1038/s41598-026-35899-3 | Isolation, characterisation and potential applications of a novel bacteriophage  |
| 41645056 | 10.1002/mbo3.384 | 10.1186/s12866-025-04672-3 | Characterization of broad-host-range bacteriophages targeting multidrug-resistan |
| 41648009 | 10.1093/femsre/fuad042 | 10.3389/fmicb.2025.1723885 | Multidrug-resistant Pseudomonas aeruginosa infections: current status, challenge |
| 41649278 | 10.1126/sciadv.adc9130 | 10.1128/msystems.01173-25 | Assessment of genome evolution in Bifidobacterium adolescentis indicates genetic |
| 41650276 | 10.17504/protocols.io.btv8nn9w | 10.1126/sciadv.aeb6265 | Animal-associated jumbo phages as widespread and active modulators of gut microb |
| 41652486 | 10.1016/j.mib.2003.09.004 | 10.1186/s12985-026-03066-9 | Phage vB_AbaM_MU1 for biocontrol of carbapenem-resistant Acinetobacter baumannii |
| 41652492 | 10.3390/ijms241310537 | 10.1186/s12985-026-03067-8 | Can phage-antibiotic combinations overcome uropathogenic Escherichia coli regrow |
| 41653009 | 10.3389/fcimb.2020.572909 | 10.1080/17460913.2026.2627823 | Combatting antibiotic resistance: challenges and emerging therapeutic strategies |
| 41653918 | 10.1016/j.celrep.2023.112432 | 10.1016/j.molcel.2026.01.004 | Molecular basis for anti-jumbo phage immunity by AVAST type 5. |
| 41654550 | 10.1016/j.cmi.2023.08.022 | 10.1038/s41467-026-69154-0 | Combined bacteriophage and antibiotic therapy for refractory peritoneal dialysis |
| 41656415 | 10.1128/genomea.00659-15 | 10.1007/s10096-026-05432-5 | Characterization of prophage carrying blaKPC-184 in a ST307 Klebsiella pneumonia |
| 41659645 | 10.1101/2024.04.20.590411 | 10.64898/2026.01.26.700923 | Phage-Mediated Iron Acquisition by Pseudomonas aeruginosa. |
| 41660980 | 10.1371/journal.ppat.1004384 | 10.1128/spectrum.02191-25 | Atypical El Tor Vibrio cholerae from the second major global seventh-pandemic ch |
| 41661104 | 10.1038/nmeth.2089 | 10.1128/iai.00503-25 | Acquisition of toxin-encoding lysogenic bacteriophage elements enhances the viru |
| 41662980 | 10.1002/bip.22095 | 10.1016/j.ijantimicag.2026.107738 | Phage resistance bidirectionally altered antibiotic susceptibility in Klebsiella |
| 41663479 | 10.1111/1574-6976.12072 | 10.1038/s41598-026-39153-8 | Isolation and characterization of lytic bacteriophages with therapeutic potentia |
| 41665341 | 10.1016/j.mam.2022.101117 | 10.1128/jb.00610-25 | NeuO-mediated O-acetylation of uropathogenic Escherichia coli K1 capsule enhance |
| 41665752 | 10.1128/AEM.00145-20 | 10.1007/s10517-026-06582-4 | A Novel Bacteriophage Targeting Adherent-Invasive Escherichia coli: A Potential  |
| 41667461 | 10.1093/bioinformatics/btt656 | 10.1038/s41467-026-69247-w | Ecological partitioning enables phage-antibiotic cooperation in a human Pseudomo |
| 41668450 | 10.1093/jac/dky365 | 10.4014/jmb.2601.01019 | Comparative Combinatorial Effects of Endolysins LNT103 with Ten Conventional Ant |
| 41670374 | 10.1016/j.virusres.2022.198997 | 10.1128/spectrum.02655-25 | Inactivating conditions of therapeutic mycobacteriophages. |
| 41670440 | 10.3389/fmicb.2018.00066 | 10.1099/mgen.0.001630 | Dynamics of a large multidrug-resistant plasmid encoding New Delhi metallo-β-lac |
| 41671333 | 10.1002/jcc.21334 | 10.1021/acs.bioconjchem.5c00577 | On-Resin DIAMSAR-Conjugated CD38-Targeted Peptides and Their Inverso and Dimeric |
| 41677854 | 10.1016/j.snb.2023.134810 | 10.1007/s00203-026-04727-7 | Prophage: agent provocateur? |
| 41685809 | 10.1107/S2059798317000067 | 10.1021/acsnano.5c19041 | Utilizing Constrained Bicyclic Peptides for In Vitro Diagnostics. |
| 41690950 | 10.1002/psp4.12757 | 10.1038/s41522-025-00908-2 | A theoretical exploration of protocols for treating prosthetic joint infections  |
| 41691253 | 10.1080/19490976.2025.2499575 | 10.1186/s12985-026-03091-8 | Characterizing the gut virome in ulcerative colitis and crohn's disease: signatu |
| 41691301 | 10.1097/00005072-199906000-00011 | 10.1186/s13195-026-01985-x | Timing matters: early administration of a high-affinity antibody targeting the t |
| 41693862 | 10.1002/advs.202405087 | 10.3389/fcimb.2025.1726935 | Metagenomic and metatranscriptomic profiling of bronchoalveolar lavage fluid ide |
| 41698972 | 10.1021/acssensors.1c01222 | 10.1038/s41598-026-37008-w | An engineered M13 phage-rGO electrochemical biosensor for rapid detection of vir |
| 41699059 | 10.32614/RJ-2016-025 | 10.1038/s41590-026-02432-7 | Demographic and genetic factors shape the epitope specificity of the human antib |
| 41699453 | 10.1186/S12985-025-02885-6/METRICS | 10.1186/s12866-026-04737-x | Large-genome phage vB_Eco_ZCEC15 targets gastrointestinal MDR E. coli: evidence  |
| 41703256 | 10.1038/s41564-020-00817-4 | 10.1038/s41598-026-40091-8 | Evaluation of bacteriophage efficacy against Pseudomonas aeruginosa in ex vivo a |
| 41704535 | 10.1016/j.aqrep.2023.101597 | 10.3389/fimmu.2025.1716916 | VNAR: shark single-domain antibodies for the new era of medical biotechnology. |
| 41709134 | 10.1002/phar.2358 | 10.1186/s12866-025-04243-6 | Isolation, characterization, and genomic analysis of novel bacteriophage AEV23 a |
| 41709141 | 10.1146/annurev-micro-090816-093830 | 10.1186/s12866-025-04539-7 | Identification of novel prophages and variants of integrative and conjugative el |
| 41710227 | 10.1007/s12088-012-0250-6 | 10.1007/s12088-024-01444-x | Transcriptomics-Driven Analysis of LDPE Degradation by Pseudomonas Aeruginosa WD |
| 41710912 | 10.1038/s43856-024-00594-9 | 10.1093/jacamr/dlag018 | Exploring the perspectives of antimicrobial stewardship pharmacists in England o |
| 41712005 | 10.3389/fmicb.2023.1081715 | 10.1007/s00705-026-06544-1 | Isolation, characterization, and therapeutic assessment of novel phage vB_LSKP32 |
| 41712449 | 10.1007/s00705-019-04349-z | 10.1099/jgv.0.002198 | Isolation, characterization and genomic analysis of a novel lytic bacteriophage  |
| 41714337 | 10.1186/s40813-023-00336-8 | 10.1038/s41598-026-39877-7 | Cocktail of genetically diverse lytic phages reduces uropathogenic Escherichia c |
| 41716420 | 10.1002/advs.202301166 | 10.3389/fimmu.2026.1667180 | Pathogenesis and intervention strategies for metabolic dysfunction-associated fa |
| 41721592 | 10.1016/S1473-3099(20)30307-8 | 10.1111/jgh.70308 | Phage Therapy: Targeting the Gut Microbiota for the Treatment of Acute Pancreati |
| 41723417 | 10.1016/j.snb.2021.129708 | 10.1186/s12951-026-04207-6 | Electron transfer-driven nanozymes integrated "colorimetric-photothermal" nanobo |
| 41724747 | 10.1099/00221287-143-6-2065 | 10.1038/s41598-026-40701-5 | Pseudolysogeny-mediated evolutionary trade-offs favor phage therapy by limiting  |
| 41727556 | 10.3390/medicina59101719 | 10.3389/bjbs.2026.15559 | Antimicrobial Resistance: The Answers. |
| 41728112 | 10.1016/j.vaccine.2021.12.008 | 10.3389/fcimb.2026.1755353 | Bacterial meningitis in adults: therapeutic challenges in the era of antibiotic  |
| 41729322 | 10.1093/bioinformatics/btx157 | 10.1007/s00705-026-06549-w | Isolation, characterization and evaluation of a novel phage against Elizabethkin |
| 41730964 | 10.3390/jpm12101644 | 10.1038/s41598-026-40342-8 | Label-free saliva screening platform using M13 bacteriophage-based 3D plasmonic  |
| 41733371 | 10.1016/0003-2697(92)90349-c | 10.1128/mbio.03801-25 | A teichoic acid-like wall modification associated with immune suppression is soc |
| 41736797 | 10.1038/s41421-024-00648-1 | 10.3389/fcimb.2026.1692727 | A computational pipeline to discover potential cross-reactive antibodies: a case |
| 41737826 | 10.1371/journal.pgen.1003269 | 10.1177/26416549251406410 | Discovery and characterization of a novel Pseudomonas phage of a new genus. |
| 41738762 | 10.3389/fgene.2019.00858 | 10.1128/spectrum.02834-25 | A CRISPR array orchestrates virulence and host response in Porphyromonas gingiva |
| 41742824 | 10.1002/gch2.202300088 | 10.1080/17576180.2026.2631639 | Affinity-maturation engineering via phage display to optimize anti-idiotype anti |
| 41743509 | 10.2174/1381612820666140905112311 | 10.1177/26416549251384322 | Isolation of Pseudomonas aeruginosa Phages vB_Psu_NEU2023 and vB_Psu_NEU2024 Lea |
| 41743708 | 10.4103/jpbs.jpbs83823 | 10.3389/fimmu.2026.1735735 | PhIP-Seq: unveiling the complexity of antibody repertoires in health and disease |
| 41746166 | 10.1038/s41467-024-45336-6 | 10.1128/iai.00543-25 | Bacteriophage-mediated reduction of uropathogenic E. coli from the urogenital ep |
| 41746586 | 10.15252/embr.201643250 | 10.1007/s40290-026-00601-5 | The Combat Against Antimicrobial Resistance: An Overview of EU Recent Health Pol |
| 41748485 | 10.1007/s00216-021-03375-8 | 10.1021/acs.analchem.5c06003 | Development of an Anti-Immunocomplex Antibody and Non-competitive Immunoassay fo |
| 41748831 | 10.1186/S12934-025-02702-3/ | 10.1007/s00253-026-13749-6 | Evaluation of the delivery of an anti-Listeria endolysin via CRISPR-Cas9 enginee |
| 41749264 | 10.1126/science.aad5872 | 10.1186/s12967-026-07692-3 | Cross-kingdom microbial interactions in the gut during inflammatory bowel diseas |
| 41749306 | 10.1080/19490976.2023.2249143 | 10.1186/s12967-026-07900-0 | Distinct gut virome profiles are associated with response to anti-PD-1 therapy i |
| 41750375 | 10.1002/prot.25869 | 10.3390/biom16020307 | Cell-Based Immunization Combined with Single-Round Cell Panning Enables Discover |
| 41750402 | 10.1128/msphere.01014-24 | 10.3390/biom16020334 | The Evolution of Symbiosis in Staphylococcus epidermidis: From a Protective Mutu |
| 41750423 | 10.1111/j.1751-7915.2008.00028.x | 10.3390/antibiotics15020125 | Phage-Based Approaches to Chronic Pseudomonas aeruginosa Lung Infection in Cysti |
| 41751890 | 10.5114/ada.2019.87443 | 10.3390/ijms27041753 | In Vitro and Clinical Evaluation of the Anti-Wrinkle Efficacy of Medipep-6PN, a  |
| 41754522 | 10.3389/fmicb.2019.02484 | 10.3390/v18020179 | Diverse Temperate Coliphages of the Urinary Tract. |
| 41754558 | 10.1038/s44259-025-00117-z | 10.3390/v18020214 | Isolation and Genomic Characterization of Two Lytic Cutibacterium acnes Phages D |
| 41754583 | 10.1093/ve/veac086 | 10.3390/v18020240 | Modeling the Phage Properties Best for Therapy. |
| 41754904 | 10.5812/jjm.8(4)2015.16592 | 10.3390/pharmaceutics18020162 | Inhaled Antibiotic and Biologic Formulations Targeting Pseudomonas aeruginosa. |
| 41754927 | 10.1039/D3QM01048A | 10.3390/pharmaceutics18020185 | Nano-Enabled Delivery of Phage-Based Antibacterials Against ESKAPE Pathogens. |
| 41756291 | 10.1080/2162402X.2023.2297504 | 10.3389/fimmu.2026.1740184 | A fully human IgG1 antibody targeting MICA α1 domain inhibits interaction with N |
| 41759553 | 10.1093/bioinformatics/btt656 | 10.1128/spectrum.03077-25 | Enzyme-enhanced RNA isolation from biofilm-producing bacteria. |
| 41759557 | 10.1080/19490976.2024.2309684 | 10.1128/spectrum.03276-25 | Alterations in the gut virome of children with allergic rhinitis: enrichment of  |
| 41767409 | 10.1002/adfm.202402868 | 10.1155/bmri/5328382 | Pseudomonas aeruginosa Biofilms in Cystic Fibrosis: Interactions, Methods, and T |
| 41769334 | 10.1016/j.jaci.2016.09.017 | 10.3389/fcimb.2026.1693905 | Microbiome dysbiosis and therapeutic restoration in atopic dermatitis. |
| 41769340 | 10.1101/gr.074492.107 | 10.3389/fcimb.2026.1753740 | Phage isolation and functional characterization reveal strong antibiofilm activi |
| 41770946 | 10.1128/aac.01699-18 | 10.1080/14728222.2026.2639679 | Lipopolysaccharide-targeting treatments for multidrug-resistant Pseudomonas aeru |
| 41773871 | 10.1128/spectrum.01601-24 | 10.1128/aem.00050-26 | Intra-strain and inter-strain heterogeneity shape phage-host interactions and ph |
| 41773876 | 10.1529/biophysj.106.102962 | 10.1128/spectrum.03284-25 | Precision of a phage susceptibility spot assay assessed with 154 clinical Staphy |
| 41774077 | 10.1038/s41591-024-02938-3 | 10.1084/jem.20250959 | Immune profiling links autoimmune hepatitis to human herpesvirus 6 and relaxin r |
| 41774177 | 10.21037/atm-22-928 | 10.1007/s00203-026-04774-0 | Phage therapy for treatment of bacterial vaginosis. |
| 41774772 | 10.1128/AEM.65.7.2954-2960.1999 | 10.1371/journal.ppat.1014039 | Type VI secretion system degeneration accelerates intestinal epithelial cell dea |
| 41776320 | 10.18637/jss.v028.i05 | 10.1038/s41598-026-41637-6 | Comprehensive antigen profiling predicts post-surgical neuropathic pain in women |
| 41776548 | 10.1111/aor.12254 | 10.1186/s12929-026-01218-1 | Phage-antibiotic synergy restores β-lactam efficacy in MDR Klebsiella quasipneum |
| 41777892 | 10.1158/0008-5472.CAN-11-3468 | 10.3389/fimmu.2026.1769287 | BDCA2 plays a central role in the binding, internalization and response of plasm |
| 41782866 | 10.3389/fmicb.2021.634511 | 10.3389/fimmu.2026.1771414 | Synergistic carcinogenesis of the nasopharyngeal microbiome and Epstein-Barr vir |
| 41792595 | 10.1046/j.1464-410X.2002.02560.x | 10.1186/s12866-026-04843-w | Evaluating Proteus mirabilis phage vB_PmiA_PM1 efficacy against catheter-associa |
| 41798745 | 10.3389/fmicb.2018.00850 | 10.3389/fcimb.2026.1749949 | A lytic bacteriophage vB_KpnP-6K2 inhibits ST11-KL64 Klebsiella pneumoniae induc |
| 41798747 | 10.1038/s43856-025-00790-1 | 10.3389/fcimb.2026.1775191 | Predicting inter-microbial host specificity in oral biofilms using a lightweight |
| 41798749 | 10.1016/j.virusres.2022.198889 | 10.3389/fcimb.2026.1760018 | Characterization of phage AbpL with a terminally redundant genome and its therap |
| 41803419 | 10.1007/s42995-022-00160-z | 10.1038/s42003-026-09823-4 | Global genomic diversity of temperate P2-like viruses. |
| 41805848 | 10.1007/s00705-025-06257-x | 10.1007/s00705-026-06542-3 | Genome characterization and receptor-binding protein identification of Klebsiell |
| 41805891 | 10.1186/s12985-020-01485-w | 10.1007/s00203-026-04788-8 | Deploying bacteriophage combinatorial therapy to eradicate resistant Klebsiella  |
| 41805917 | 10.3389/fmicb.2022.856473 | 10.1007/s00203-026-04786-w | pTJK, a rare Mammaliicoccus lentus phage with broad-host-range, antibiofilm, and |
| 41805923 | 10.1038/NCOMMS5498 | 10.1007/s00438-026-02393-4 | Genomic characterization of Pseudomonas aeruginosa infecting Abidjanvirus Lucjan |
| 41806028 | 10.3390/ANTIBIOTICS14040334 | 10.1007/s00203-026-04803-y | Alternative approaches in combating antimicrobial resistance in animals. |
| 41806052 | 10.1016/j.chempr.2023.05.019 | 10.1007/s10661-026-15135-1 | Fecal Contamination in Drinking Water: A review of detection techniques, pathoge |
| 41808009 | 10.1038/nprot.2009.182 | 10.1186/s11658-025-00852-1 | GPA33 forms a distinct diagnostic target class to Claudin 18.2 in oesophageal ad |
| 41808040 | 10.4014/jmb.2205.05009 | 10.1186/s12866-026-04933-9 | A temperate phage encoding a catalytically active endolysin: characterization of |
| 41811064 | 10.1093/nar/gkae268 | 10.1128/msphere.00775-25 | Evolutionary dynamics and virulence factor variability in invasive Streptococcus |
| 41813891 | 10.1002/jemt.20829 | 10.1038/s41586-026-10191-6 | Intestinal interoceptive dysfunction drives age-associated cognitive decline. |
| 41813903 | 10.1093/nar/gkad330 | 10.1038/s41586-026-10136-z | Capturing dynamic phage-pathogen coevolution by clinical surveillance. |
| 41816995 | 10.1038/s41467-022-33071-9 | 10.1002/advs.202516916 | Alternating High-Fat and Polysaccharide Diets Modulates Gut Phage-Bacterial Inte |
| 41817597 | 10.1038/s41467-024-49461-0 | 10.1172/jci.insight.203645 | Human antibody repertoire among kidney donors with and without HIV. |
| 41820596 | 10.1039/C5RA03399C | 10.1038/s41598-026-43492-x | Variability analysis of a low-cost paper dipstick nucleic acid extraction method |
| 41820852 | 10.1128/AEM.02641-08 | 10.1186/s12866-026-04913-z | Environmental isolation and characterization of Escherichia coli phages from Bur |
| 41822327 | 10.1007/s00011-004-1257-1 | 10.3389/fcimb.2026.1758422 | Searching for the perfect match: can non-antibiotic antimicrobials improve bacte |
| 41823362 | 10.1002/mmr3.70001 | 10.1111/1751-7915.70330 | Precision Microbial Therapeutics for Infertility: Next-Generation Probiotics, En |
| 41824364 | 10.1016/j.onehlt.2022.100414 | 10.1080/22221751.2026.2645857 | Phage-derived depolymerase targeting the K27 capsule impairs Klebsiella pneumoni |
| 41824923 | 10.1038/s41591-025-04014-w | 10.1212/NXI.0000000000200551 | Development of a Diagnostic Autoantibody Assay to a Consensus Motif for the Risk |
| 41834980 | 10.1073/pnas.1801233115 | 10.12182/20260160205 | [Research on Bacteriophage Resistance: Coevolutionary Arms Race Between Bacteria |
| 41835539 | 10.1177/0022034509359125 | 10.1021/acsomega.5c12013 | A Carboxymethyl Chitosan Hydrogel Loaded with Bacteriophage-Derived Bacteriostat |
| 41836398 | 10.3390/cancers16234008 | 10.3389/fimmu.2026.1795736 | The intratumoral microbiome in colorectal cancer: origins, microenvironmental in |
| 41838339 | 10.3390/v13101901 | 10.1007/s12223-026-01458-6 | Bacteriophage-based control of Pseudomonas spp.: research trends and biotechnolo |
| 41839859 | 10.1186/1471-2105-8-209 | 10.1038/s41467-026-70381-8 | Dynamics of phage-host interactions in Bacteroides fragilis resolved by single-c |
| 41843109 | 10.3390/ijms26115235 | 10.1007/s00203-026-04817-6 | Beyond new pills: integrative strategies to overcome multidrug-resistant bacteri |
| 41848831 | 10.1089/sur.2021.154 | 10.1007/s00203-026-04829-2 | Molecular mechanisms of virulence in Enterococcus faecium: integrating Esp, Acm, |
| 41849201 | 10.1099/mgen.0.001090 | 10.1099/mgen.0.001651 | Mind the gap! Typing Escherichia coli O157:H7 in the pre- and post-genomic revol |
| 41849206 | 10.3201/eid2503.180899 | 10.1099/mgen.0.001677 | Phylodynamic analysis of Salmonella Enteritidis ST183 in Aotearoa New Zealand fi |
| 41851503 | 10.1128/mBio.02146-17 | 10.1038/s44318-026-00740-0 | Simultaneous inhibition of bacterial virulence and anti-phage defense systems by |
| 41853116 | 10.1093/jacamr/dlac046 | 10.1128/asmcr.00108-25 | Clearance of hypermutator XDR Pseudomonas osteomyelitis and hardware infection w |
| 41857394 | 10.1038/s41467-024-51021-5 | 10.1038/s41590-026-02459-w | Improved VSV-Ebola-GP booster vaccination approach promotes antibody affinity ma |
| 41862452 | 10.1093/nar/gkz380 | 10.1038/s41467-026-70613-x | High-resolution phage-host assignment through key proteins using large language  |
| 41869406 | 10.1016/j.mtbio.2023.100612 | 10.2147/IJN.S551541 | Filamentous Phage for Therapeutic Applications in Non-Small Cell Lung Cancer and |
| 41872068 | 10.1371/journal.pgen.1009204 | 10.1080/19490976.2026.2647529 | Intra-species competition combats vancomycin-resistant enterococci. |
| 41874175 | 10.1007/978-1-0716-3523-0_11 | 10.1128/spectrum.02894-25 | Identification and functional insights into new phage tail-like bacteriocins tar |
| 41876525 | 10.1111/j.1365-2958.2012.08031.x | 10.1038/s41467-026-70808-2 | Phage-steering permits antibody-mediated clearance of E. coli K1 from the gut. |
| 41878262 | 10.1128/AAC.01746-18 | 10.3389/fcimb.2026.1750702 | Pathobiology of ESKAPE Biofilms in implant infections: current understanding and |
| 41878266 | 10.1186/s40168-024-01914-w | 10.3389/fcimb.2026.1598786 | Temporal dynamics of gut microbiota and virome in preterm infants: insights from |
| 41879899 | 10.1016/j.jmb.2017.12.007 | 10.1007/s10482-026-02282-1 | Characterization, genomic insights and anti-biofilm potential of phage vB_PaeM_P |
| 41882673 | 10.1186/s12866-021-02125-1 | 10.1186/s12967-026-08013-4 | Disentangling environmental and disease-specific signatures in the gut microbiom |
| 41897305 | 10.3390/antibiotics9110833 | 10.3390/biom16030369 | A High-Affinity Nanobody Selectively Recognizing KPC-2/KPC-3: Biochemical and St |
| 41899469 | 10.1080/10934529.2020.1830653 | 10.3390/cimb48030318 | Exploring the Antimicrobial Potential of a Novel Phage-Derived Lytic Protein Aga |
| 41900309 | 10.1128/aac.00578-23 | 10.3390/microorganisms14030549 | Synergistic Efficiency of a Novel Temperate Phage YF1204 and Amikacin Against Ca |
| 41901210 | 10.1038/s41591-025-03678-8 | 10.3390/ph19030363 | Encapsulation of Bacteriophages in Alginate Beads: Improved Viability Under Hars |
| 41902263 | 10.1038/s41522-024-00552-2 | 10.3390/v18030355 | Engineered Bacteriophages: A Next-Generation Platform for Precision Antimicrobia |
| 41902276 | 10.1136/bmjgh-2024-016474 | 10.3390/v18030368 | Bacteriophages as Food Biocontrol Agents: A One Health Framework for Manufacturi |
| 41902300 | 10.3390/vaccines13030237 | 10.3390/v18030392 | Bacteriophages as Antibacterial Agents Against Bovine Pathobionts Associated wit |
| 41903528 | 10.1126/science.aar4120 | 10.1016/j.chom.2026.03.004 | Bacterial 2',3'-cGAMP activates a SAVED effector to form membrane-disrupting fil |
| 41908588 | 10.3390/antibiotics9110827 | 10.2147/IDR.S577526 | Management of Diabetic Foot Infections Using Phage Therapy. |
| 41909847 | 10.3389/fcimb.2022.999418 | 10.3389/fcimb.2026.1779296 | Phage characterization analysis in respiratory samples from infected patients ba |
| 41910255 | 10.1038/nprot.2006.24 | 10.1128/mbio.00243-26 | The repertoire of resistance mutations selected by a Pseudomonas aeruginosa type |
| 41912269 | 10.1136/jitc-2023-008677 | 10.1136/jitc-2025-014185 | HFB301001, an OX40-based immunotherapy, drives Treg clearance and CTL activation |
| 41914750 | 10.1038/s41467-022-30269-9 | 10.1128/msphere.00103-26 | Predicted and inducible prophages display contrasting virulence gene profiles wi |
| 41917361 | 10.1186/s13059-015-0676-3 | 10.1007/978-1-0716-5218-3_13 | Deep Protease Profiling to Define the Substrate Specificity of ADAMTS Proteases. |
| 41917404 | 10.1017/S0950268820001788 | 10.1007/978-3-032-04153-1_20 | Glycoconjugate Vaccines Against Nosocomial Klebsiella pneumoniae Infections. |
| 41917457 | 10.1186/s12866-019-1443-5 | 10.1038/s41598-026-46878-z | Extensive screening of ten bacteriophage cocktails revealed an optimal combinati |
| 41920025 | 10.1128/AEM.01371-21 | 10.1128/aem.02304-25 | Assessing antibacterial, antiviral, and antifungal efficacy of non-porous materi |
| 41922334 | 10.1093/bioinformatics/btp324 | 10.1038/s41467-026-71174-9 | Whole-proteome phage immunoprecipitation sequencing reveals germ cell tumor-spec |
| 41922762 | 10.7717/peerj.16505 | 10.1038/s41586-026-10340-x | Evolution of pandemic cholera at its global source. |
| 41925202 | 10.1016/j.cgh.2025.12.006 | 10.14309/ctg.0000000000001030 | Phage-Display Immunoprecipitation Sequencing Reveals Distinct Antibody Signature |
| 41928387 | 10.1080/19490976.2025.2569739 | 10.1080/19490976.2026.2653288 | Neglected kingdoms: the gut virome, mycobiome and their role in inflammatory bow |
| 41933291 | 10.1080/13543776.2019.1584612 | 10.1080/19490976.2026.2653575 | The functional and catalytic landscape of urease reveals a conserved target agai |
| 41942347 | 10.1016/j.micres.2023.127446 | 10.1080/17460913.2026.2654374 | Combatting multidrug resistance in Klebsiella pneumoniae: mechanisms, global tre |
| 41944896 | 10.1111/1751-7915.70075 | 10.1007/s00203-026-04844-3 | Biological characteristics and genome analysis of Enterococcus faecalis phage vB |
| 41945876 | 10.1021/acs.nanolett.3c02728 | 10.1002/advs.202517369 | Hierarchical Targeting of TREM2+ Myeloid Cells via Acid-Triggered OMVs Reprogram |
| 41949138 | 10.4292/wjgpt.v8.i3.162 | 10.25259/IJMR_2923_2025 | Bacteriophage research in India and its implications for human health: A scoping |
| 41951679 | 10.1080/19490976.2025.2557979 | 10.1038/s41522-026-00981-1 | Phage therapy targeting DNA-encapsulated membrane vesicle-producing intestinal s |
| 41951946 | 10.3389/fcimb.2023.1137947 | 10.1007/s10096-026-05462-z | Bacteriophage-mediated reduction of Pseudomonas aeruginosa biofilm on titanium s |
| 41954628 | 10.1038/s44259-025-00145-9 | 10.1007/s00103-026-04231-9 | [Molecular mechanisms underlying the development and spread of antibiotic resist |
| 41959331 | 10.1128/ecosalplus.ESP-0034-2018 | 10.64898/2026.03.10.710608 | A broad-spectrum phage-encoded mechanism to disarm bacterial type IV filaments. |
| 41962742 | 10.3791/59010 | 10.1016/j.virs.2026.03.018 | Nanobody targeting glycan cap confers broad orthoebolavirus neutralization. |
| 41973218 | 10.1128/JB.181.16.4725-4733.1999 | 10.1007/s00103-026-04232-8 | [Antibiotics and phages: effects of combined therapy on susceptibility and resis |
| 41973501 | 10.64898/2026.03.25.712926 | 10.1099/mic.0.001692 | Identification of an R1-type pyocin previously misannotated as a prophage in Pse |
| 41973928 | 10.1186/s12929-015-0138-y | 10.1073/pnas.2517953123 | A modified CRISPR/Cas9 approach in silencing the triplication in Down syndrome:  |
| 41974192 | 10.1186/s13073-025-01575-w | 10.1093/ecco-jcc/jjag015 | Mapping adaptive immune responses toward fungal antigens in inflammatory bowel d |
| 41975274 | 10.1038/s41467-023-39029-9 | 10.1080/19490976.2026.2655793 | Compositional and functional differences of gut microbiome and metabolome inform |
| 41977264 | 10.1021/acs.jmedchem.5c01836 | 10.3390/ijms27073077 | Linker Engineering in Stapled Peptides for Enhanced Membrane Permeability: Scree |
| 41985061 | 10.1021/acs.jcim.8b00248 | 10.1093/bib/bbag183 | A bio-inspired computational pipeline for antibody screening and repurposing. |
| 41986244 | 10.1038/s41592-022-01488-1 | 10.1021/acs.biochem.6c00058 | Phage Display Driven Identification and Computational Mapping of Macrocyclic Pep |
| 41987056 | 10.1111/j.1365-2672 | 10.1186/s12866-026-05046-z | Assessing non-porous antimicrobial surfaces against bacteria, phages and fungi:  |
| 41988191 | 10.1080/19420862.2021.1980942 | 10.3389/fimmu.2026.1806908 | Discovering novel therapeutic VHHs for emerging viruses: perspectives from VEEV  |
| 41991710 | 10.1016/j.gpb.2022.01.004 | 10.1007/s00253-026-13814-0 | The combination of mupirocin and Kayvirus broadens the decolonization effect aga |
| 41992102 | 10.1093/jac/dks196 | 10.1186/s12866-026-05022-7 | AbCro, a novel transcription factor, promotes biofilm formation and virulence in |
| 41992105 | 10.1016/j.mimet.2024.106986 | 10.1186/s11658-026-00926-8 | High-temperature ssBP-LAMP breaks the barrier of nonspecific amplification and u |
| 41992356 | 10.1039/c7nr06966a | 10.1186/s13062-026-00795-3 | A nanobody against CD63 for non-destructive exosome labeling. |
| 41994204 | 10.1038/s41598-023-42505-3 | 10.3389/fcimb.2026.1774993 | Carbapenem-resistant Acinetobacter baumannii bloodstream infections and specific |
| 41994271 | 10.1007/s12275-014-4087-z | 10.3389/fmicb.2026.1748742 | Next-generation bacteriophage therapeutic systems: CRISPR-based engineering, nea |
| 41998424 | 10.1155/2014/307942 | 10.1007/s00011-026-02247-0 | Macrophages with ITIH4 overexpression attenuate inflammatory responses and regul |
| 41998453 | 10.1038/s41467-021-22016-3 | 10.1007/s11274-026-04951-9 | Klebsiella pneumoniae in the global AMR: resistance mechanisms and genomic adapt |
| 42000726 | 10.1038/s41596-024-00999-9 | 10.1038/s41467-026-71981-0 | Multi-kingdom profiling reveals altered gut phage-bacteria-metabolite interactio |
| 42000836 | 10.1158/2326-6066.CIR-22-0953 | 10.1038/s41598-026-47884-x | Differential T cell reactivation by two PD-L1 nanobodies through blockade alone  |
| 42001946 | 10.3791/51312 | 10.1016/j.jbc.2026.111476 | Antibodies blocking PlGF or VEGF interactions with the NRP1 receptor mediate ant |
| 42006142 | 10.3109/1040841X.2011.621064 | 10.3389/fcimb.2026.1790430 | A conserved KL2-capsule-related phage-resistant mechanism in carbapenem-resistan |
| 42007720 | 10.3390/v10110619 | 10.1128/aem.02514-25 | Evaluation of ultraviolet irradiation at 254 nm and 222 nm in inactivating human |
| 42007992 | 10.3389/fcimb.2022.832672 | 10.1007/s00203-026-04906-6 | Divergent mechanistic pathways of diarrheagenic bacterial infections at the host |
| 42009645 | 10.1093/bioinformatics/btp033 | 10.1038/s41467-026-72155-8 | Structural basis of QueC-family protein function in qatABCD anti-phage defense. |
| 42013857 | 10.1016/S0022-2836(05)80360-2 | 10.1016/j.crmeth.2026.101406 | Genetic modification of intractable bacterial clones by heat shock-facilitated p |
| 42015835 | 10.1038/s41571-024-00908-9 | 10.1002/chem.202503523 | Living Microbial Drugs. |
| 42016201 | 10.1002/9780471729259.mc06e01s25 | 10.1016/j.bioactmat.2026.04.013 | AI-assisted phage formulation delivered via injectable hydrogels for localized c |
| 42018214 | 10.3389/fonc.2025.1604808 | 10.1007/s10388-026-01203-5 | A GLUT1-targeted peptide tracer for precision molecular imaging of esophageal sq |
| 42024499 | 10.1371/journal.ppat.1001042 | 10.1016/j.celrep.2026.117302 | Unmasking pathogen traits for chronic colonization in neurogenic bladder. |
| 42026124 | 10.1080/01621459.1927.10502953 | 10.1038/s41564-026-02324-4 | Emergence of distinct Streptococcus pyogenes emm1 and emm12 lineages in China. |
| 42026455 | 10.1126/science.8066462 | 10.1186/s12866-026-05053-0 | Genomic characterization of Pseudomonas aeruginosa clonal lineage ST162 isolated |
| 42029769 | 10.1016/j.biocel.2014.03.006 | 10.1007/s00203-026-04839-0 | Pseudomonas aeruginosa: associated pathogenesis, epidemiology, resistance mechan |
| 42032982 | 10.1182/blood.2024025694 | 10.11817/j.issn.1672-7347.2025.250361 | [Gut microbiota involved in cancer invasion and metastasis]. |
| 42033508 | 10.1038/s41522-023-00385-5 | 10.1007/s00203-026-04846-1 | Phage endolysin therapy: a modern antimicrobial strategy against highly drug-res |
| 42033527 | 10.1128/spectrum.00390-25 | 10.1007/s11033-026-11858-z | Decoding and exploiting intratumoral microbiota: from microenvironment modulatio |
| 42037385 | 10.21105/joss.01686 | 10.1128/spectrum.04084-25 | Multiple prophage acquisition events over the course of an outbreak drive lysoge |
| 42038555 | 10.1128/mmbr.00069-15 | 10.1155/ijm/8509161 | From Sewage to Salvage: Complete Characterization of Arefeen1 Phage Against MDR  |
| 42039195 | 10.1038/s41598-025-85420-5 | 10.3389/fimmu.2026.1749584 | What is the impact of the virome and mycobiome on female reproductive tract heal |
| 42041253 | 10.1586/14760584.2013.825450 | 10.1128/mmbr.00008-25 | Typhoid toxin: reframing enteric fever. |
| 42041415 | 10.3390/vetsci12100959 | 10.3390/bios16040194 | Fluorescence Immunosensor with Phage Antibodies for Heat Shock Protein 70 Detect |
| 42043219 | 10.1080/21597081.2016.1251379 | 10.3390/v18040430 | Characterization of Klebsiella Phages Isolated Against a Clinical Host with High |
| 42048130 | 10.1089/phage.2022.29037.inp | 10.1099/mic.0.001626 | Phages for One Health: regulatory and product life cycle considerations. |
| 42056714 | 10.1016/j.micres.2022.127032 | 10.1080/21505594.2026.2664980 | Acinetobacter baumannii: Mechanisms of antibiotic resistance, quorum sensing reg |
| 42058179 | 10.1007/s12223-021-00946-1 | 10.3389/fcimb.2026.1697070 | Spot-on phage therapy: stable formulations, smarter dosing for topical phage app |
| 42058217 | 10.1126/science.abi4882 | 10.3389/fimmu.2026.1797096 | Biofilm adaptation and mucosal immune dysregulation in recalcitrant chronic rhin |
| 42059665 | 10.1128/spectrum.02409-22 | 10.1128/spectrum.04009-25 | Synergistic effects of halo-plaque forming phage cocktails against polymicrobial |
| 42061408 | 10.1182/blood-2006-04-017061 | 10.1016/j.xcrm.2026.102782 | Engineering functionality-optimized fully human B7-H3 CAR T cells for enhanced s |
| 42062473 | 10.1093/nar/gkm216 | 10.1038/s42003-026-10148-5 | Structural atlas of Pakpunavirus P7-1 reveals determinants of virion stability a |
| 42065815 | 10.3389/fcimb.2024.1324895 | 10.1007/s10096-026-05519-z | Bacteriophage-induced outer membrane protein remodelling drives the phenotypic s |
| 42071311 | 10.2147/IDR.S326230 | 10.1002/mbo3.70303 | Phage Therapy as an Alternative Strategy Against Pseudomonas aeruginosa: A Narra |
| 42074308 | 10.1016/j.chom.2021.03.018 | 10.3390/ijms27083662 | Phage Therapy in Gastrointestinal Diseases: Current Status and Challenges. |
| 42075680 | 10.1016/j.jtbi.2011.02.007 | 10.3390/pathogens15040353 | Factors Governing the Cross-Species Virulence of Shiga Toxin-Producing Escherich |
| 42075738 | 10.3389/fmicb.2020.00110 | 10.3390/pathogens15040411 | Antibacterial Efficacy of Pseudomonas aeruginosa Bacteriophages on a Drosophila  |
| 42079579 | 10.1038/s41586-022-04439-0 | 10.3389/fimmu.2026.1812063 | Discovery of co-stimulatory anti-CD28 VHHs for developing cancer immune therapeu |
| 42080567 | 10.1128/spectrum.00835-25 | 10.1128/spectrum.00507-26 | The building blocks of phage therapy: from lytic phage identification to preclin |
| 42082564 | 10.3390/idr17050104 | 10.1038/s41598-026-50942-z | Oral yeast-displayed SARS-CoV-2 spike protein vaccine enhanced by trimerization  |
| 42088277 | 10.1016/j.ijbiomac.2025.146159 | 10.3389/fmicb.2026.1807725 | Newly isolated Pakpunavirus: efficacy and safety assessment in light of alternat |
| 42090420 | 10.1038/s41423-021-00754-0 | 10.1155/bmri/8304153 | Multiomics Approaches for Bacteriophage-Based Biocontrol Applications: A Review  |
| 42090589 | 10.3389/fmicb.2017.00981 | 10.1080/17460913.2026.2667121 | Meta-analysis of preclinical evidence supporting phage therapy against Stenotrop |
| 42091760 | 10.3390/s130201763 | 10.1007/s42770-026-01947-3 | Integrated Morphological, Functional, and Genomic Analysis of a Novel Lytic Phag |
| 42096338 | 10.1128/AEM.02229-13 | 10.1099/mic.0.001693 | Isolation and characterization of broad-range Staphylococcus epidermidis sepunav |
| 42098130 | 10.3390/v10070351 | 10.1038/s41467-026-72590-7 | From hype to hope: reanimating phage therapy through evidence-based multidiscipl |
| 42098310 | 10.1038/nmeth.1923 | 10.1038/s42003-026-10221-z | HIV-driven virome dysbiosis unveils distinct virome features and inter-viral cor |
| 42099231 | 10.1371/journal.ppat.1006421 | 10.3892/mmr.2026.13898 | Applications of humanized mice in Mycobacterium tuberculosis infections (Review) |
| 42100797 | 10.1021/acschembio.9b00560 | 10.1021/acs.jmedchem.5c03413 | Peptides Targeting GDNF Family Receptor Alpha 1 (GFRα1) Mimic Glial Cell Line-De |
| 42102162 | 10.3390/antibiotics8030103 | 10.1093/ismejo/wrag116 | Short-term antagonism between bacteriophages and macrophages decreases with bact |
| 42108342 | 10.1002/eji.201242606 | 10.1007/978-1-0716-5037-0_4 | ImmTAC: A Novel Platform of T-Cell Receptor-Based Soluble Bispecifics. |
| 42117717 | 10.1093/nar/gkx1033 | 10.1128/spectrum.02207-25 | Genomic profiling of Morganella morganii: insights into antibiotic resistance ge |
| 42124705 | 10.21203/rs.3.rs-6158033/v1 | 10.64898/2026.02.24.707611 | CBASS limits bacteriophage production while maintaining cell viability in Pseudo |
| 42125497 | 10.3389/fcell.2025.1480233 | 10.3389/fcimb.2026.1817579 | The association between periodontal disease and pancreatic cancer: epidemiology, |
| 42127010 | 10.1111/j.1462-2920.2009.01927.x | 10.1371/journal.pone.0349089 | A novel isolated phage targeting Pseudomonas aeruginosa demonstrates therapeutic |
| 42127816 | 10.1126/science.aba5257 | 10.1016/j.chom.2026.04.008 | The human skin virome: Ecological dynamics, aberrant profiles, and therapeutic o |
| 42129087 | 10.1038/s42003-021-01881-0 | 10.1007/978-1-0716-5041-7_5 | Construction of Naïve and Immune Human Fab Phage Display Library. |
| 42129088 | 10.1038/s41598-022-16378-x | 10.1007/978-1-0716-5041-7_6 | Generation and Panning of a Naïve Human scFv Phage Display Library. |
| 42129089 | 10.1016/j.chom.2017.08.011 | 10.1007/978-1-0716-5041-7_7 | Screening of Monoclonal Antibodies from Integrated Phage and Mammalian Cell Disp |
| 42129095 | 10.1038/s41423-021-00654-3 | 10.1007/978-1-0716-5041-7_13 | High-Throughput Profiling of Antibody-Binding Epitopes Using AbMap. |
| 42132423 | 10.1128/mbio.03550-22 | 10.1128/jvi.00035-26 | Generation of HBV cccDNA using single-stranded M13 phage DNA for authentic minic |
| 42136738 | 10.1038/s41598-023-42505-3 | 10.3389/fcimb.2026.1819965 | Phage and endolysin-based inhibition of Klebsiella pneumoniae: from mechanisms t |
| 42138049 | 10.1101/2025.04.29.651274 | 10.1080/21505594.2026.2672206 | Phylogenomic framework and virulence gene boundaries of emerging Shiga toxin-pro |
| 42141502 | 10.1101/pdb.prot108601 | 10.1002/pro.70620 | A rapid phage-free platform for antigen-specific VNAR screening with BATCH syste |
| 42143256 | 10.1093/nar/gkab301 | 10.1186/s12866-026-05127-z | Draft genome sequencing of Proteus mirabilis strain Indica (ST286) reveals antim |
| 42148631 | 10.1093/sysbio/syq010 | 10.1128/mra.00353-26 | Complete genome sequence of Pseudomonas aeruginosa phage OmaKarin. |
| 42151149 | 10.1007/s00449-003-0347-8 | 10.1038/s41467-026-73464-8 | Scalable and sustainable manufacturing of functional DNA nanoassemblies via self |
| 42151178 | 10.1093/nar/gkab1006 | 10.1038/s41467-026-73047-7 | Systematic discovery of motif-based interactions of the auxiliary domains of USP |
| 42151789 | 10.3382/ps.2014-03943 | 10.1186/s12866-026-05141-1 | Isolation and characterization of a bacteriophage targeting Proteus mirabilis fo |
| 42151807 | 10.1021/acsami.3c01065 | 10.1186/s12866-026-05164-8 | Isolation and characterization of novel bacteriophage, vB_AbaA_SWMUZ8, targeting |
| 42153618 | 10.1038/s41592-020-0771-6 | 10.1080/17460913.2026.2675855 | Genomic impact of prophages on carbapenem-resistant Klebsiella pneumoniae: distr |
| 42153737 | 10.1371/journal.ppat.1002923 | 10.1128/jvi.01363-25 | A polyvalent phage shapes bacterial dynamics. |
| 42154079 | 10.1371/journal.ppat.1007011 | 10.1007/s00203-026-04938-y | Multidrug-resistant tuberculosis: a comprehensive review of pathogenesis, drug r |
| 42154739 | 10.1186/s12913-022-07577-3 | 10.1371/journal.pone.0349568 | Phage therapy for recurrent urinary tract infections: A qualitative study using  |
| 42156793 | 10.3791/52687 | 10.1038/s41598-026-48091-4 | Human cathelicidin peptide LL-37 compacts nucleic acids and alters neutrophil ex |
| 42156951 | 10.3390/ph14050465 | 10.1038/s41598-026-52857-1 | Characterization and evaluation of the efficacy of phage E21 therapy in a wound  |
| 42165624 | 10.1016/j.ijpharm.2025.126299 | 10.1128/spectrum.02713-25 | Characterization and comparative genomic analysis of a novel bacteriophage again |
| 42165805 | 10.1136/gutjnl-2020-321747 | 10.1099/mgen.0.001731 | The effects of bacteriophage cocktail treatment on healthy gut microbiota: an in |
| 42165977 | 10.1016/J.CELLIN.2025.100237 | 10.1007/s12223-026-01467-5 | A comprehensive study on Salmonella enterica serovar Richmond in farmed fish Pan |
| 42168489 | 10.1038/srep38828 | 10.1038/s41598-026-52935-4 | CApEsid biOfilm: a suggested pipeline for clinical phage microbiology for biofil |
| 42171956 | 10.1093/procel/pwaf085 | 10.1186/s43556-026-00473-w | Intratumoral microbiota in cancer: molecular mechanism and therapeutic strategie |
| 42183845 | 10.3389/fphar.2024.1466888 | 10.1007/s00203-026-04972-w | Synergistic strategies to rescue the last-resort antibiotic colistin. |
| 42191833 | 10.1371/journal.pone.0208735 | 10.1038/s41598-026-55068-w | Genomic characterization of Enterotoxigenic Escherichia coli lineage 2 (CS2 + CS |
| 42194065 | 10.1002/pro.5127 | 10.3390/biom16050716 | High-Affinity Nanobody Against the LEDGF PWWP Domain Inhibits Chromatin Binding  |
| 42195290 | 10.3389/fmicb.2017.00293 | 10.3390/life16050734 | Isolation and Genomic Characterization of Lytic Caudoviricetes Bacteriophage vB_ |
| 42196448 | 10.3389/fmolb.2021.729513 | 10.3390/ijms27104474 | Production and Characterization of Recombinant Single-Chain Variable Fragment (s |
| 42197413 | 10.1007/s11274-023-03548-w | 10.3390/microorganisms14051028 | Engineered Phage Modulates Quorum Sensing and Biofilm Formation in Pseudomonas a |
| 42197833 | 10.3390/bios14020098 | 10.3390/s26103024 | Affinity Peptide-Based Circularly Permuted Fluorescent Protein Biosensors Loaded |
| 42198401 | 10.3389/fimmu.2025.1499810 | 10.3390/ph19050727 | Phage Therapy in Combating Multidrug-Resistant Gram-Negative Pathogens: A Scopin |
| 42198683 | 10.1186/s12931-018-0750-y | 10.3390/pathogens15050557 | Host-Pathogen Interactions in Cystic Fibrosis Lung Disease: Adaptation, Persiste |
| 42198722 | 10.3389/fimmu.2021.730986 | 10.3390/v18050519 | Genomic Diversity of Vaginal Lactobacillus crispatus Prophages from South Africa |
| 42198729 | 10.1093/bioinformatics/btab007 | 10.3390/v18050526 | Isolation of Bacteriophages with Lytic Activity from Biological Samples of Left  |
| 42198737 | 10.1073/pnas.1100299108 | 10.3390/v18050534 | Phage Therapy Beyond Static Pharmaceuticals: A Framework for Controlled Evolutio |
| 42204159 | 10.1093/nar/gkab1113 | 10.1038/s41467-026-73316-5 | Autoantibodies to IL-1Ra and PGRN in severe COVID-19 are associated with inflamm |
| 42206754 | 10.1128/aac.00954-00917 | 10.1111/1751-7915.70389 | Isolation of a Novel Lytic Pseudomonas aeruginosa Phage Henu5 and Fitness Costs  |
| 42207692 | 10.1016/s0378-1119(98)00130-9 | 10.1128/jb.00520-25 | Pseudomonas aeruginosa biofilm-deficient mutants undergo parallel evolution duri |
| 42209914 | 10.1021/bi00677a021 | 10.1007/s10895-026-04820-6 | Label-Free Fluorescent Detection of T4 PNK Using a DNA Mimic Green Fluorescent P |
| 42210496 | 10.1128/msphere.00780-19 | 10.1002/mbo3.70320 | Fungal-Bacterial Interactions in Polymicrobial Infections: Hidden Threats. |
| 42213357 | 10.1208/s12249-020-01673-5 | 10.1007/s12223-026-01517-y | Isolation, genomic characterization, and biofilm eradication activity of vB_PaP_ |
| 42213731 | 10.1093/nar/28.1.33 | 10.1371/journal.pone.0350027 | Phage-plasmid-like elements are found throughout diverse environments and encode |
| 42214370 | 10.3390/v12111268 | 10.1128/spectrum.03397-25 | Harnessing lytic phages for biofilm control in carbapenem-resistant Klebsiella p |
| 42221581 | 10.1093/nar/gkr485 | 10.3389/fcimb.2026.1796701 | Emergence of a methicillin-susceptible Staphylococcus aureus ST672 clone associa |
| 42223509 | 10.1080/19420862.2023.2213793 | 10.1093/protein/gzag012 | Examining selection dynamics and limitations in multi-round protein selection of |
| 42225613 | 10.1038/s41596-024-01045-4 | 10.1038/s41392-026-02765-7 | Dual epitope anti-LILRB4 synthetic T-cell receptor and antigen receptor (STAR)-T |
| 42227741 | 10.1016/j.virusres.2023.199293 | 10.1128/msystems.00188-26 | Optimizing methods for virome analysis based on studies of a synthetic viral com |
| 42228533 | 10.2210/pdb9Z5W/pdb | 10.1073/pnas.2531008123 | PANCS-spec-Binders: A system for rapidly discovering isoform- or epitope-specifi |
| 42231337 | 10.3390/v15051208 | 10.1186/s12985-026-03147-9 | Antibacterial potential of five phages in controlling Enterococcus faecalis and  |
| 42233644 | 10.1093/nar/gkae268 | 10.1128/msystems.01498-25 | Expanding vaginal microbiome pangenomes via a custom MIDAS database reveals Lact |
| 42236487 | 10.1016/j.cels.2020.04.003 | 10.1038/s41467-026-74031-x | Prevalent gut phages encode modular adhesins mediating epithelial binding and en |
| 42237234 | 10.3389/fmicb.2023.1117017 | 10.1186/s12866-026-05145-x | WGS reveals high-risk clones of Pseudomonas aeruginosa harbouring extensive anti |
| 42237848 | 10.1371/journal.pone.0228164 | 10.1080/19420862.2026.2672771 | Generation of human sequence antibodies in OmniChicken against the highly conser |
| 42240952 | 10.1136/bmjopen-2022-065401 | 10.1007/s40290-026-00614-0 | Regulating the Irregular: Phage Therapy and the Case for a Regulatory Sandbox Ap |
| 42247470 | 10.1038/nmeth1083 | 10.1371/journal.pbio.3003834 | Disrupting phage liquid crystalline droplets restores antibiotic susceptibility  |
| 42250148 | 10.3390/microorganisms10112211 | 10.1007/s00203-026-04971-x | Biotherapeutic strategies for quorum quenching in Salmonella Typhi: a review. |
| 42256221 | 10.3389/fmicb.2018.02247 | 10.3389/fcimb.2026.1826972 | From dysbiosis to precision medicine: targeting the microbial-metabolic axis in  |
| 42262436 | 10.3389/fcimb.2024.1408569 | 10.1007/s00203-026-04988-2 | CRISPR-based gene editing for antimicrobial resistance control in human medicine |
| 42273738 | 10.1111/hae.13820 | 10.1080/19420862.2026.2685362 | Discovery and optimization of marstacimab, a human monoclonal antibody targeting |
| 42275032 | 10.1128/iai.00435-22 | 10.1093/ismejo/wrag139 | Global transmission and distribution of phage-encoded cholera toxin genes constr |
| 42276819 | 10.1186/s12951-025-03712-4 | 10.1080/21505594.2026.2687214 | Biofilm-mediated antibiotic tolerance in bacterial pathogens: Integrated molecul |
| 42278616 | 10.3390/life14050557 | 10.3390/ijms27115092 | Evolving Approaches to Bacterial Identification: A Review of Classical and Moder |
| 42282511 | 10.64898/2026.01.04.697583 | 10.64898/2026.06.04.730250 | Balancing of immune activation and suppression during phage infection. |
| 42283445 | 10.1016/j.cels.2017.08.001 | 10.1021/acs.biochem.6c00189 | Synthetic Substrate Discovery for Hck Kinase via Phage Display. |
| 42283824 | 10.1016/j.micres.2025.128278 | 10.1007/s00203-026-04980-w | Bacteriophage therapy for multidrug-resistant bacterial infections: recent advan |
| 42284414 | 10.5281/zenodo.14550073 | 10.1126/sciadv.aeb7044 | Integrated evaluation of antibody responses to mosquitoes and mosquito-borne pat |
| 42285989 | 10.3389/fgene.2025.1560601 | 10.1038/s41522-026-01050-3 | Decoding phage communication: molecular networks, evolutionary dynamics, and the |
| 42286276 | 10.1089/phage.2022.0001 | 10.1007/s40259-026-00789-7 | Giving Antibiotics a Second Chance: Evolutionary Trade-Offs and Phage-Driven Res |
| 42286914 | 10.1098/rstb.2007.2182 | 10.1093/ismejo/wrag114 | Rapid adaptation accelerates competitive suppression in a parasite community. |
| 42288735 | 10.1007/s12275-011-1512-4 | 10.1186/s12866-026-05289-w | Comparison and correlation of in vitro and in vivo approaches for determining Ps |
| 42290341 | 10.1038/s41598-018-25714-z | 10.1080/17460913.2026.2686571 | Combinatorial antimicrobial potential of secondary metabolites and bacteriophage |
| 42291333 | 10.3389/fimmu.2023.1103617 | 10.3389/fcimb.2026.1857968 | When bacteriophages encounter macrophages during their journey through the human |
| 42292354 | 10.1021/bc034221g | 10.3389/fimmu.2026.1843118 | Physicochemical convergence in antibody CDR3-VH repertoires recognizing phosphor |
| 42294707 | 10.1099/mgen.0.000339 | 10.1128/spectrum.03962-25 | From screening to treatment: in vitro and in vivo efficacy of phage-meropenem co |
| 42294726 | 10.3389/fmicb.2016.01383 | 10.1128/spectrum.04096-25 | Systematic combinatorial optimization of three-phage cocktails against multidrug |
| 42301365 | 10.1086/315239 | 10.1007/s00203-026-04998-0 | Shiga toxin-centered pathophysiology defines the therapeutic limits of enterohem |
| 42301484 | 10.20524/aog.2022.0703 | 10.1007/s00203-026-04996-2 | Helicobacter pylori phages: resource landscape, translational challenges, and en |
| 42302013 | 10.1093/nar/gkab1107 | 10.1371/journal.pone.0350919 | Study protocol on antimicrobial resistance burden, transmission dynamics, and th |
| 42304522 | 10.3389/fmicb.2020.591866 | 10.1186/s40249-026-01470-5 | Rapid drug susceptibility testing of Mycobacterium tuberculosis against first-li |
| 42307077 | 10.1186/s13036-025-00479-y | 10.1002/biot.70260 | Butyrate-Producing Bacteria in Intestinal Disease Therapy: Potential and Challen |
| 42307405 | 10.1099/vir.0.013615-0 | 10.1590/0074-02760250343 | Novel epitope-based diagnostic probes selected by phage display for the serologi |
| 42311629 | 10.1070/PU2003v046n02ABEH001308 | 10.1021/acsestwater.5c01533 | Role of Nitrate-Driven Radical Formation in Microorganism Inactivation under 222 |
| 42313053 | 10.1093/bioinformatics/bty191 | 10.1128/mra.00086-26 | Genome sequence of the Pseudomonas aeruginosa bacteriophage Shea. |
| 42316926 | 10.1093/nar/gkac920 | 10.1002/mbo3.70321 | Hospital-Associated Antimicrobial Resistant Bacteria on 95 Mobile Phones: An Int |
| 42318992 | 10.1016/j.vaccine.2018.11.004 | 10.1155/tbed/3021186 | A Fully Human Derived Monoclonal Antibody Provides Potent Pre- and Postexposure  |
| 42321788 | 10.1167/tvst.13.12.35 | 10.1186/s12967-026-08457-8 | A novel Tie2xVEGF bispecific antibody fusion demonstrates enhanced therapeutic e |
| 42324603 | 10.1016/j.xcrm.2024.101478 | 10.1080/19490976.2026.2689168 | Cross-kingdom microbiome interactions along the gut-lung axis: immune-microecolo |
| 42324716 | 10.1021/acsinfecdis.4c00039 | 10.1002/mbo3.70344 | Human Gut Phageome Analysis Uncovers Thousands of Highly Modular Endolysins. |
| 42330089 | 10.18637/jss.v033.i03 | 10.1371/journal.pcbi.1014408 | Towards modeling phage therapy. |
| 42332304 | 10.1016/j.micpath.2015.08.014 | 10.1007/s10482-026-02364-0 | Emerging threats and zoonotic implications of antibiotic-resistant Staphylococcu |
| 42340134 | 10.3389/fpubh.2020.578089 | 10.1155/bmri/7063234 | Acinetobacter baumannii in the Age of Antimicrobial Resistance: Clinical Impact, |
| 42347171 | 10.1016/j.chom.2019.05.001 | 10.3390/pathogens15060559 | Bacteriophage-Based Therapeutics for Bacterial Sexually Transmitted Infections:  |
| 42347211 | 10.1038/s41467-024-51617-x | 10.3390/pathogens15060599 | Prophages in Skin Pathogens: From Virulence to Therapy. |
| 42347511 | 10.1016/j.mimet.2020.105965 | 10.3390/toxins18060257 | Recombinant Human Fab Antibodies Differentially Neutralize Shiga Toxin in Renal  |
| 42352352 | 10.1016/j.jphotobiol.2015.09.002 | 10.3390/biom16060886 | A Competent Antiviral, Antimicrobial, Nontoxic Nanostructured Lipid Carrier Syst |
| 42352353 | 10.3389/fphar.2024.1491363 | 10.3390/biom16060887 | Innovative Strategies to Abolish Microbial Persistence in Biofilm Fortresses. |
| 42353184 | 10.3390/v16071032 | 10.3390/ijms27125466 | Phage-Encoded Depolymerase DepKP144 with Therapeutic Potential Against Both K1-  |
| 42353661 | 10.3390/v14071490 | 10.3390/antibiotics15060537 | Single Treatment of Mature 3D Single-, Dual- and Poly-Species Biofilms Using a C |
| 42353674 | 10.1089/mdr.2017.0147 | 10.3390/antibiotics15060550 | The ESKAPE Challenge: Understanding Resistance and Exploring Alternative Treatme |
| 42353720 | 10.1186/s12859-023-05311-2 | 10.3390/antibiotics15060596 | Synergistic Bactericidal Effects of R- and F-Type Pyocin Cocktails Against Clini |
| 42354442 | 10.1021/acsami.3c19443 | 10.3390/gels12060544 | Alginate-Chitosan Gel Microbeads for PhiKZ Encapsulation as a Model of Bacteriop |
| 42357673 | 10.1371/journal.pone.0266928 | 10.3390/v18060664 | Protecting Newborns from Multidrug-Resistant Infections: The Emerging Role of Ba |
| 42362550 | 10.1186/s40168-018-0410-y | 10.1038/s41522-026-01069-6 | Remodelling of the gut virome after long-term fasting. |
| 42362811 | 10.1093/bioinformatics/btp033 | 10.1038/s41564-026-02407-2 | END nucleases are antiphage defence systems targeting multiple phages with modif |
| 42362974 | 10.3390/v14020342 | 10.1007/s00253-026-13898-8 | A new Kayvirus vB_SauM-MUHD-1 combats Methicillin-resistant Staphylococcus aureu |
| 42363638 | 10.1186/s10020-025-01226-1 | 10.1080/07853890.2026.2681295 | Inhalable bacteriophage endolysins: a novel therapeutic strategy for drug-resist |
| 42365575 | 10.1016/j.jes.2025.08.010 | 10.1007/s10482-026-02367-x | Pathogens in the bay: environmental Staphylococcus saprophyticus strains mirror  |
| 42367797 | 10.1128/aem.00919-25 | 10.3389/fimmu.2026.1851108 | Innate immune recognition and immunomodulatory effects of bacteriophages: implic |
| 42367834 | 10.6019/EMPIAR-10110 | 10.64898/2026.06.18.732992 | Intracellular barriers and receptor masking limit success of a Pseudomonas aerug |
| 42376079 | 10.1016/bs.mim.2019.11.007 | 10.5455/OVJ.2026.v16.i3.3 | Prevalence, risk factors, and innovative therapies for methicillin-resistant Sta |
| 42377392 | 10.1016/j.tifs.2023.104275 | 10.1007/s11033-026-12205-y | Bacterial extracellular membrane vesicles as multifunctional defense systems: Ro |
| 42377507 | 10.1016/j.jmb.2017.12.007 | 10.1007/s00203-026-05037-8 | Antibiofilm efficacy and genomic characterization of a lytic bacteriophage targe |
| 42382096 | 10.1016/j.cell.2019.09.015 | 10.3389/fcimb.2026.1856292 | Advances in mycobacteriophage research: from lytic mechanisms to one health appl |
| 42382097 | 10.1186/s43014-023-00193-6 | 10.3389/fcimb.2026.1837303 | Isolation and characterization of lytic Shigella bacteriophages with rapid in vi |
| 42389543 | 10.1007/978-1-0716-1154-8_11 | 10.3389/fimmu.2026.1793368 | Development of bispecific antibodies with enhanced neutralization activity again |
| 42395820 | 10.1155/2017/7542540 | 10.1039/d6ra01532h | Effect of vacuum plasma treatment duration on physicochemical, mechanical, and b |
| 42400832 | 10.1038/nature21687 | 10.1007/978-1-0716-5249-7_1 | Incorporation of Butyryl-Lysine into Phage-Displayed Peptide Libraries. |
| 42400833 | 10.1007/978-1-0716-3381-6_2 | 10.1007/978-1-0716-5249-7_2 | Construction and Functional Validation of a High-Diversity Naive Phage Antibody  |
| 42400835 | 10.1038/nprot.2007.151 | 10.1007/978-1-0716-5249-7_4 | Generation of a CDR H3 Randomized Monoclonal Antibody Library by Kunkel Mutagene |
| 42400840 | 10.1093/nar/gku404 | 10.1007/978-1-0716-5249-7_9 | Application of Phage-Displayed Peptide Library for Epitope Mapping. |
| 42404584 | 10.7759/cureus.71542 | 10.1155/ijm/4451708 | Pseudomonas aeruginosa Virulence Bacteriophage Isolated From Inflammatory Mouse  |
| 42405768 | 10.1093/molbev/msab166 | 10.1128/msphere.00386-26 | Enteric populations of Escherichia coli are likely to be resistant to phages due |
| 42418062 | 10.1099/IJSEM.0.006300 | 10.1007/s42770-026-02010-x | Stenotrophomonas mexicanensis subsp. fluminensis subsp. nov., a new subspecies i |
| 42423743 | 10.1111/jvh.13886 | 10.1007/s00280-026-04911-y | Anti-PD-1 single-chain variable fragments in cancer immunotherapy: from molecula |
| 42427226 | 10.1002/anie.202517565 | 10.1002/cbic.70401 | Genetically Encoding Propiolamide Warhead for the Construction of Phage Displaye |
| 42427398 | 10.1016/j.burns.2006.06.010 | 10.1039/d6ra03599j | Pepholin, a bacteriophage holin-derived antimicrobial peptide with membrane-disr |
| 42450332 | 10.1002/prot.70123 | 10.3390/ijms27136067 | Cyclic Peptides as Modulators of Protein-Protein Interactions: A Survival Guide  |
| 42451116 | 10.55627/mic.003.002.0989 | 10.3390/nu18132112 | Probiotic-Plant Bioactive Synergy in Gut Health: Mechanisms, Antimicrobial Activ |
| 42458884 | 10.1016/j.omtm.2025.101561 | 10.1002/bies.70164 | Engineering CAR-Tregs with Phage-Selected scFv Enables a New Paradigm for Immune |
| 42459653 | 10.1172/jci.insight.136012 | 10.3389/fimmu.2026.1805950 | Engineering a juxtamembrane-targeting CAR T-cell against mesothelin: a novel bin |
| 42459698 | 10.1128/jb.00375-25 | 10.3389/fimmu.2026.1856088 | Immuno-phage synergy driven by fitness costs: turning bacterial phage resistance |
| 42461251 | 10.1038/srep41237 | 10.1099/mgen.0.001774 | Phylogenomic analysis of a methicillin-resistant Staphylococcus aureus ST764 iso |
| 42467470 | 10.1038/ncomms5269 | 10.1099/jgv.0.002292 | Data mining reveals the diversity of prophage endolysins targeting pathogenic en |
| 42469629 | 10.1128/MMBR.00011-16 | 10.1186/s12866-026-05262-7 | Isolation, characterization, and genomic analysis of a novel lytic bacteriophage |
| 42470537 | 10.3389/fpubh.2019.00235 | 10.1007/s11033-026-12374-w | Genomic regulation of the diphtheria toxin gene and Its implications for molecul |
| 42483832 | 10.3390/biom13050853 | 10.1093/nar/gkag703 | Structural adaptations for enhanced translation kinetics in evolved ribosomes. |
| 42485076 | 10.64898/2026.02.11.702040 | 10.1099/mgen.0.001789 | The pQBR mercury resistance plasmids: a model set of sympatric environmental mob |
| 42487119 | 10.1186/s12935-024-03259-8 | 10.1186/s12917-026-05628-z | Neutralizing nanobodies against porcine epidemic diarrhea virus: discovery and c |
| 42488001 | 10.1016/j.chom.2026.01.013 | 10.3389/fendo.2026.1878037 | "Envbiotics" -- a novel framework for microbiota-targeted therapeutic strategies |
| 42488416 | 10.1038/s41598-023-42448-9 | 10.3389/fcimb.2026.1879718 | Bacteriophage therapy beyond antibiotics: emerging innovations for infectious an |
| 42489162 | 10.1038/s41929-025-01436-0 | 10.1002/pro.70726 | De novo design of proteinaceous binders targeting the LEDGF PWWP domain. |
| 42489333 | 10.1038/s41591-021-01398-3 | 10.1080/19420862.2026.2700812 | Conditional activation of IL-12 through a Fibronectin-EDB dependent switch gate. |
| 42492495 | 10.64898/2025.12.19.695335 | 10.1016/j.cell.2026.06.030 | Bacteriophage genome-wide transposon mutagenesis. |
| 42494847 | 10.1186/s13073-016-0279-y | 10.3389/fcimb.2026.1851410 | Phage-antibiotic synergy attenuates Acinetobacter baumannii resistance in refrac |
| 42495612 | 10.3390/ijms25052903 | 10.3389/fimmu.2026.1873405 | Immunotherapy for tuberculosis: emerging modalities, cross-disciplinary innovati |
| 42506689 | 10.4149/BLL_2022_116 | 10.55095/achot2026/018 | [Bacteriophage Therapy in Orthopaedics and Trauma]. |
| 42509246 | 10.1164/ajrccm/143.5_Pt_1.1121 | 10.1038/s41467-026-75735-w | Personalized Phage Therapy in an ICU Patient with Polymicrobial Pulmonary Infect |
| 42509730 | 10.1038/s41586-025-09721-5 | 10.3390/biom16070936 | Screening and Engineering of Hetero-Bivalent Nanobody Targeting Interleukin-33 w |
| 42514089 | 10.1093/infdis/jiw632 | 10.3390/microorganisms14071585 | Short-Term Bacteriophage Exposure Is Associated with Shifts in Antibiotic Suscep |
| 42515042 | 10.1016/S0002-8223(97)00217-4 | 10.3390/pathogens15070711 | Targeting Foodborne Pathogens with Bacteriophages: Mechanisms, Applications, and |
| 42520047 | 10.1093/nar/gkab1038 | 10.1371/journal.ppat.1013832 | A novel stress response pathway mediates biofilm architecture in Pseudomonas aer |
| 42522025 | 10.4161/bact.1.3.17629 | 10.1186/s12866-026-05119-z | Efficacy of phage vB_EcoP_ZCEC16 in controlling Escherichia coli contamination i |
| 42523748 | 10.7150/ijbs.27231 | 10.3389/fcimb.2026.1824616 | Application of autoantibody markers based on phage display immunoprecipitation s |
| 42525191 | 10.1016/j.drup.2018.10.003 | 10.1007/s42770-026-02036-1 | Decoding the genome of Acinetobacter baumannii from a urinary tract infection ca |
| 42528685 | 10.3389/fphar.2025.1641036 | 10.3389/fcimb.2026.1891884 | Microbial dysbiosis and wound healing in diabetic foot ulcers: a mini review wit |
| 42529160 | 10.1146/annurev-virology-010720-052252 | 10.3389/fimmu.2026.1882961 | M13 phage-based antigen presentation and immune response activation in vaccine d |
| 42530739 | 10.3390/bioengineering13020144 | 10.1007/s00203-026-05085-0 | Quorum-sensing, microbiome interactions, and emerging artificial intelligence-as |
| 42533067 | 10.1016/j.fsisyn.2023.100449 | 10.1038/s41564-026-02409-0 | Combined phage therapy and faecal microbiota transplantation to treat recurrent  |
| 42533315 | 10.1186/1471-2180-9-148 | 10.1186/s12866-026-05452-3 | Targeting nontuberculous mycobacteria with phages: optimization of in vitro host |
| 42534931 | 10.1080/08927014.2021.1955866 | 10.3389/fpubh.2026.1868215 | Targeted phage aerosol for environmental control of CR-Kpn in the ICU: a prospec |