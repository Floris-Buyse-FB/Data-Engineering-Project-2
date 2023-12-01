import random

def generate_personalized_email(naam, campaigns, doelen, strategien,handtekening):
    email_template = """Beste {klant_naam}

{begroeting}

{reden_voor_contact}

  Hier zijn de top 3 campagnes die ik ten zeerste aanbeveel:
  1. **{campagne1_naam}:**
    - Doel: {campagne1_doel}.
    - Strategie: {campagne1_strategie}.

  2. **{campagne2_naam}:**
    - Doel: {campagne2_doel}.
    - Strategie: {campagne2_strategie}.

  3. **{campagne3_naam}:**
    - Doel: {campagne3_doel}.
    - Strategie: {campagne3_strategie}.


{afspraak}

Bedankt voor je tijd en ik kijk ernaar uit om samen te werken aan het verder laten groeien van jouw bedrijf.

Met vriendelijke groet,


{handtekening}
  """

    begroeting_library = [
        'Ik hoop dat deze e-mail je in goede gezondheid bereikt. Graag wil ik je bedanken voor je voortdurende vertrouwen in onze diensten. Wij bij Voka, zijn altijd op zoek naar manieren om onze samenwerking te versterken en jouw bedrijfsdoelstellingen te ondersteunen.',
        'Ik vertrouw erop dat deze boodschap je welzijn weerspiegelt. Dank je wel voor het voortdurende vertrouwen in onze diensten. Als toegewijde medewerkers bij Voka, streven we voortdurend naar manieren om onze samenwerking te optimaliseren en jouw bedrijfsdoelen te ondersteunen.',
        'Hopelijk ontvang je deze e-mail in goede gezondheid. Wij waarderen je voortdurende vertrouwen in onze diensten. Als team van Voka zijn we constant bezig met het vinden van manieren om onze samenwerking te versterken en jouw bedrijfsdoelen te realiseren.',
        'Deze boodschap bereikt je hopelijk in uitstekende conditie. Hartelijk dank voor het aanhoudende vertrouwen in onze diensten. Als professionals bij Voka, zoeken we voortdurend naar manieren om onze samenwerking te verbeteren en jouw bedrijfsdoelstellingen te ondersteunen.',
        'Moge deze e-mail je bereiken terwijl het goed met je gaat. Ik ben dankbaar voor het voortdurende vertrouwen in onze diensten. Als betrokken team van Voka, zetten we ons voortdurend in om onze samenwerking te versterken en jouw bedrijfsdoelstellingen te faciliteren.',
        'Ik hoop dat deze woorden je in goede gezondheid bereiken. Bedankt voor het blijvende vertrouwen in onze diensten. Als medewerkers van Voka, blijven we actief werken aan het versterken van onze samenwerking en het ondersteunen van jouw bedrijfsdoelstellingen.'
    ]

    reden_voor_contact_library = [
        'Ons team heeft nauwlettend uw bedrijf geanalyseerd en wij zijn ervan overtuigd dat de volgende campagnes perfect bij uw doelstellingen zullen passen.',
        'Na grondig onderzoek van uw bedrijf, zijn wij ervan overtuigd dat de voorgestelde campagnes naadloos aansluiten bij uw doelen.',
        'Op basis van onze analyse denken wij dat de voorgestelde campagnes een waardevolle aanvulling zullen zijn op uw huidige strategieën.',
        'Wij hebben uw bedrijf zorgvuldig geëvalueerd en zijn ervan overtuigd dat de onderstaande campagnes de juiste richting uitgaan voor uw groei en succes.',
        'Door een diepgaande analyse van uw onderneming zijn wij ervan overtuigd dat de geselecteerde campagnes uw bedrijfsdoelen effectief zullen ondersteunen.',
    ]


    afspraak_library = [
      'Ik geloof sterk dat de voorgestelde campagnes een aanzienlijke invloed kunnen hebben op de resultaten van uw bedrijf en de betrokkenheid van uw klanten kunnen verhogen. Laten we bijeenkomen om deze ideeën nader te bespreken en af te stemmen op de specifieke behoeften van uw onderneming.',
      'De potentiële impact van deze campagnes op uw bedrijfsresultaten en klantenbetrokkenheid is aanzienlijk. Laten we samen zitten om deze concepten in detail te bespreken en aan te passen aan de specifieke behoeften van uw onderneming.',
      'Mijn overtuiging is sterk dat deze campagnes een substantiële invloed kunnen hebben op uw bedrijfsprestaties en de betrokkenheid van uw klanten. Kunnen we in de komende week een afspraak maken om deze ideeën grondig te bespreken en op maat te maken voor uw onderneming?',
      'De impact die deze campagnes kunnen hebben op uw bedrijfsresultaten en klantenbetrokkenheid is aanzienlijk. Zullen we samenkomen om deze ideeën verder uit te werken en af te stemmen op de unieke behoeften van uw onderneming? Laat me weten wanneer u beschikbaar bent voor een overleg in de komende week.',
      'Ik ben overtuigd van de potentie van deze campagnes om aanzienlijke verbeteringen te brengen in uw bedrijfsresultaten en klantenbetrokkenheid. Laten we binnenkort samenkomen om deze ideeën te bespreken en aan te passen aan uw specifieke bedrijfsbehoeften.',
    ]


    begroeting = begroeting_library[random.randint(0, len(begroeting_library)-1)]
    reden_voor_contact= reden_voor_contact_library[random.randint(0, len(reden_voor_contact_library)-1)]
    afspraak = afspraak_library[random.randint(0, len(afspraak_library)-1)]
    email_template = email_template.format(
        klant_naam=naam,
        begroeting=begroeting,
        reden_voor_contact=reden_voor_contact,
        campagne1_naam=campaigns[0],
        campagne1_doel=doelen[0],
        campagne1_strategie=strategien[0],
        campagne2_naam=campaigns[1],
        campagne2_doel=doelen[1],
        campagne2_strategie=strategien[1],
        campagne3_naam=campaigns[2],
        campagne3_doel=doelen[2],
        campagne3_strategie=strategien[2],
        afspraak=afspraak,
        handtekening=handtekening
    )
    return email_template