# SEO meta (GEO-T08): hand-written descriptions (<=200 chars) and unique keywords per page (3-5 terms, <=100 chars).
DESC = {
    '/': 'POLYMER Powder Coatings makes epoxy, polyester and hybrid powder coatings in China: Qualicoat Class 1 polyester, colour matching, special finishes, MOQ 1,000 kg, 10-day lead time.',
    '/industries/architectural-aluminium/': 'Qualicoat Class 1 polyester powder coatings for architectural aluminium profiles and facades: RAL and custom colours, matched to the approved panel batch after batch.',
    '/industries/metal-furniture/': 'Powder coatings for metal furniture, shelving and metalwork: hybrid for indoor ranges, polyester outdoors, with colour and texture kept consistent across repeat orders.',
    '/industries/appliances/': 'Hybrid and polyester powder coatings for appliances and commercial refrigeration: stable whites, custom colours and smooth high-gloss finishes for steady production.',
    '/industries/electrical-enclosures/': 'Powder coatings for electrical cabinets and new-energy enclosures: RAL 7035 and standard colours, sand textures, hybrid indoors and polyester outdoors.',
    '/industries/equipment/': 'Powder coatings for agricultural and industrial equipment: polyester outdoors, epoxy or hybrid indoors, with brand colours matched and kept stable between batches.',
    '/industries/automotive-wheels/': 'Powder coatings for selected automotive parts and wheels: specification and system confirmed first, then parts evaluated by sample and line trial.',
    '/industries/coating-applicators/': 'Powder coatings for job-shop applicators: epoxy, polyester and hybrid from one supplier, accurate colour matching, special finishes and lead times within 10 days.',
}

KEYWORDS = {
    '/': 'powder coating manufacturer China, polyester powder coating, epoxy powder coating, hybrid powder coating, Qualicoat',
    '/products/': 'powder coating products, polyester powder, epoxy powder, hybrid powder, low-cure powder coating',
    '/products/polyester/': 'polyester powder coating, outdoor powder coating, Qualicoat Class 1, architectural powder coating',
    '/products/hybrid/': 'hybrid powder coating, epoxy-polyester powder, indoor powder coating, appliance powder coating',
    '/products/epoxy/': 'epoxy powder coating, indoor functional coating, electrical cabinet powder, epoxy powder paint',
    '/finishes/': 'powder coating finishes, texture powder coating, metallic powder coating, RAL colours, gloss levels',
    '/selector/': 'powder coating selector, choose powder coating system, epoxy or polyester, indoor outdoor powder',
    '/industries/': 'powder coating applications, industrial powder coating, powder coating by industry, metal finishing',
    '/industries/architectural-aluminium/': 'aluminium profile powder coating, facade powder coating, Qualicoat polyester, window frame coating',
    '/industries/metal-furniture/': 'metal furniture powder coating, shelving powder coating, steel furniture paint, sand texture powder',
    '/industries/appliances/': 'appliance powder coating, refrigeration powder coating, white powder coating, hybrid powder',
    '/industries/electrical-enclosures/': 'electrical cabinet powder coating, enclosure powder coating, RAL 7035 powder, battery enclosure coating',
    '/industries/equipment/': 'agricultural machinery powder coating, industrial equipment coating, machine powder paint, polyester powder',
    '/industries/automotive-wheels/': 'wheel powder coating, automotive parts powder coating, metallic wheel powder, alloy wheel coating',
    '/industries/coating-applicators/': 'powder for coating applicators, job shop powder coating, colour matching powder, custom powder colours',
    '/distributors/': 'powder coating distributor, powder coating importer, powder coating supplier China, OEM powder coating',
    '/quality/': 'Qualicoat Class 1, ISO 9001 powder coating, ISO 14001, RoHS powder coating, powder coating quality control',
    '/company/': 'Fujian Polymer, POLYMER powder coatings, powder coating factory China, Zhangzhou powder coating',
    '/downloads/': 'powder coating TDS, powder coating SDS, powder coating certificates, powder coating catalogue',
    '/request-sample/': 'powder coating sample, colour matching sample, test panel, powder coating trial',
    '/contact/': 'contact powder coating manufacturer, powder coating quote, powder coating enquiry, POLYMER sales',
    '/faq/': 'powder coating FAQ, powder coating MOQ, powder coating lead time, powder coating certificates',
    '/white-paper/powder-coating-specification-guide/': 'powder coating specification, powder coating white paper, powder coating buying guide, Qualicoat',
    '/how-to/': 'powder coating guide, powder coating how-to, powder coating tips, powder coating application',
    '/insights/': 'powder coating insights, powder coating buying guide, powder coating articles, powder coating sourcing',
    '/privacy/': 'POLYMER privacy notice, cookies, data protection',
    '/ru/': 'порошковая краска, полиэфирная порошковая краска, эпоксидная порошковая краска, порошковая краска из Китая',
    '/es/': 'pintura en polvo, pintura en polvo poliéster, pintura en polvo epoxi, pintura en polvo China',
    '/how-to/avoid-batch-colour-differences/': 'powder coating batch colour difference, colour consistency, powder coating batches, delta E',
    '/how-to/check-powder-coating-cure/': 'powder coating cure test, MEK test, undercured powder coating, curing schedule',
    '/how-to/choose-epoxy-polyester-or-hybrid/': 'epoxy vs polyester powder, hybrid powder coating, choose powder coating system',
    '/how-to/consistent-texture-finishes/': 'sand texture powder, wrinkle powder coating, hammer tone powder, texture consistency',
    '/how-to/estimate-powder-coverage-consumption/': 'powder coating coverage, powder consumption calculation, transfer efficiency, m2 per kg',
    '/how-to/measure-powder-coating-film-thickness/': 'powder coating film thickness, DFT measurement, thickness gauge, microns',
    '/how-to/prepare-colour-matching-request/': 'powder coating colour matching, colour sample request, RAL matching, custom colour',
    '/how-to/read-powder-coating-tds/': 'powder coating TDS, technical data sheet, curing schedule, powder coating properties',
    '/how-to/run-line-trial-new-powder/': 'powder coating line trial, new powder trial, spray trial, production test',
    '/how-to/store-handle-powder-coatings/': 'powder coating storage, powder shelf life, handling powder coatings, storage temperature',
    '/insights/bonded-vs-dry-blend-metallic-powder/': 'bonded metallic powder, dry blend metallic, metallic powder coating, bonding',
    '/insights/how-to-source-powder-coatings-from-china/': 'source powder coating China, powder coating supplier, importing powder coatings',
    '/insights/polyester-vs-epoxy-vs-hybrid-powder-coating/': 'polyester vs epoxy, hybrid powder coating, powder coating comparison',
    '/insights/qualicoat-class-1-explained/': 'Qualicoat Class 1, Qualicoat approval, architectural powder coating standard',
    '/insights/sand-wrinkle-hammer-texture-powder-coatings/': 'texture powder coating, sand texture, wrinkle finish, hammer tone finish',
}

TITLE = {'/privacy/': 'Privacy & Cookies Notice | POLYMER Powder Coatings'}

# GEO-C07: content dates. UPDATED = date of the last site-wide content review; bump it whenever pages change.
UPDATED = '2026-11-05'
PUBLISHED_DEFAULT = '2026-10-27'          # full site v1 went live
PUBLISHED_PREFIX = {'/white-paper/': '2026-11-05', '/insights/': '2026-10-28', '/ru/': '2026-10-28', '/es/': '2026-10-28'}


def published(path):
    for p, d in PUBLISHED_PREFIX.items():
        if path.startswith(p):
            return d
    return PUBLISHED_DEFAULT
